from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

with open("conocimiento.json", "r", encoding="utf-8") as f:
    import json
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
    app.run(debug=False, host='0.0.0.0', port=5000)