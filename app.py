from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

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
    "municipalidad": ["municipalidad", "omil", "concejo", "recursos-humanos", "cecudi", "alcald", "actas", "portalmuni"],
    "canton": ["canton", "historia", "poblacional", "organizaciones"],
    "contribuyente": ["contribuyente", "pago", "servicios", "patentes", "bienes"],
    "transparencia": ["transparencia", "presupuesto", "contratacion", "informes"],
    "noticias": ["blog", "noticias", "comunicados"],
    "contacto": ["contactenos", "directorio"]
}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True) or {}
    pregunta = data.get("pregunta", "").strip()
    historial = data.get("historial", []) or []

    if not pregunta:
        return jsonify({"error": "Falta el campo 'pregunta'"}), 400

    mensajes = historial + [{"role": "user", "content": pregunta}]

    try:
        respuesta_api = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=mensajes
        )
        texto_respuesta = respuesta_api.content[0].text
    except Exception as e:
        return jsonify({"error": f"Error al consultar la API de Claude: {str(e)}"}), 500

    nuevo_historial = mensajes + [{"role": "assistant", "content": texto_respuesta}]

    return jsonify({"respuesta": texto_respuesta, "historial": nuevo_historial})

@app.route('/paginas', methods=['GET'])
def obtener_paginas():
    """Devuelve todas las páginas scrapeadas (url, contenido, imagenes) tal
    cual están en conocimiento.json. Lo usa el frontend para la navegación
    en árbol, buscando la página exacta que corresponde a cada nodo."""
    return jsonify(documentos)

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
                alt = img.get("alt", "")
                contexto = img.get("contexto", "")
                enlace = img.get("enlace", "")
                if src and src not in vistas:
                    vistas.add(src)
                    imagenes.append({"src": src, "alt": alt, "contexto": contexto, "enlace": enlace})

    return jsonify({"seccion": seccion, "total": len(imagenes), "imagenes": imagenes})
