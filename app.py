from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

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
    "municipalidad": ["municipalidad", "omil", "concejo", "recursos-humanos", "cecudi"],
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
                alt = img.get("alt", "")
                # Filtrar logos, iconos y duplicados
                if (src not in vistas
                        and len(src) > 10
                        and not any(x in src.lower() for x in [
                            "logo", "icon", "favicon", "banner", "widget",
                            "avatar", "spinner", "placeholder"
                        ])):
                    imagenes.append({"src": src, "alt": alt})
                    vistas.add(src)

    return jsonify({"seccion": seccion, "imagenes": imagenes[:6]})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        historial = data.get('historial', [])
        pregunta = data.get('pregunta', '')

        historial.append({"role": "user", "content": pregunta})

        cliente = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        respuesta = cliente.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=historial
        )

        respuesta_texto = respuesta.content[0].text
        historial.append({"role": "assistant", "content": respuesta_texto})

        return jsonify({
            "respuesta": respuesta_texto,
            "historial": historial
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def health():
    return "Chatbot Municipalidad de Flores - OK"

if __name__ == '__main__':
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

# Cargar imágenes manuales
with open("imagenes.json", "r", encoding="utf-8") as f:
    imagenes_manuales = json.load(f)

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

@app.route('/imagenes/<seccion>', methods=['GET'])
def obtener_imagenes(seccion):
    imagenes = imagenes_manuales.get(seccion, [])
    return jsonify({"seccion": seccion, "imagenes": imagenes})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        historial = data.get('historial', [])
        pregunta = data.get('pregunta', '')

        historial.append({"role": "user", "content": pregunta})

        cliente = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        respuesta = cliente.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=historial
        )

        respuesta_texto = respuesta.content[0].text
        historial.append({"role": "assistant", "content": respuesta_texto})

        return jsonify({
            "respuesta": respuesta_texto,
            "historial": historial
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def health():
    return "Chatbot Municipalidad de Flores - OK"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)    app.run(debug=False, host='0.0.0.0', port=5000)