from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Cargar conocimiento del sitio municipal
with open("conocimiento.json", "r", encoding="utf-8") as f:
    documentos = json.load(f)

def construir_contexto():
    contexto = ""
    for doc in documentos:
        contexto += f"\n\n--- Página: {doc['url']} ---\n"
        contexto += doc["contenido"][:2000]
    return contexto

CONTEXTO = construir_contexto()

SYSTEM_PROMPT = f"""Sos un asistente virtual de la Municipalidad de Flores, Costa Rica.
Respondés preguntas de ciudadanos de forma clara, amable y en español.
Basate ÚNICAMENTE en la siguiente información del sitio web municipal.
Si no sabés algo, sugerís llamar al 2265-7109.

INFORMACIÓN DEL SITIO WEB MUNICIPAL:
{CONTEXTO}
"""

# Mapa de secciones a palabras clave en URLs
SECCIONES = {
    "municipalidad": ["municipalidad", "omil", "concejo", "recursos-humanos", "cecudi", "alcald"],
    "canton": ["canton", "historia", "poblacional", "organizaciones"],
    "contribuyente": ["contribuyente", "pago", "servicios", "patentes", "bienes"],
    "transparencia": ["transparencia", "presupuesto", "contratacion", "informes"],
    "noticias": ["blog", "noticias", "comunicados"],
    "contacto": ["contactenos", "directorio"]
}

@app.route('/imagenes/<seccion>', methods=['GET'])
def obtener_imagenes(seccion):
    palabras_clave = SECCIONES.get(seccion, [])
    imagenes = []
    vistas = set()

    for doc in documentos:
        url = doc.get("url", "")
        coincide = any(clave in url for clave in palabras_clave)
        if coincide:
            for img in doc.get("imagenes", []):
                src = img.get("src", "")
                alt