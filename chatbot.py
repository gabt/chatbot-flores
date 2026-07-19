import json
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

with open("conocimiento.json", "r", encoding="utf-8") as f:
    documentos = json.load(f)

def construir_contexto():
    contexto = ""
    for doc in documentos:
        contexto += f"\n\n--- Página: {doc['url']} ---\n"
        contexto += doc["contenido"][:2000]
    return contexto

CONTEXTO = construir_contexto()

SYSTEM_PROMPT = f"""Eres un asistente virtual de la Municipalidad de Flores, Costa Rica.
Respondés preguntas de los ciudadanos basándote ÚNICAMENTE en la siguiente información 
extraída del sitio web oficial de la municipalidad.

Si la respuesta no está en el contenido proporcionado, decís amablemente que no tenés 
esa información disponible y sugerís contactar directamente a la municipalidad.

Siempre respondés en español, de forma clara y amable.

INFORMACIÓN DEL SITIO WEB MUNICIPAL:
{CONTEXTO}
"""

def chatear(historial, pregunta):
    cliente = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    historial.append({"role": "user", "content": pregunta})
    respuesta = cliente.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=historial
    )
    respuesta_texto = respuesta.content[0].text
    historial.append({"role": "assistant", "content": respuesta_texto})
    return respuesta_texto, historial

def main():
    print("🤖 Chatbot de la Municipalidad de Flores")
    print("Escribí 'salir' para terminar\n")
    historial = []
    while True:
        pregunta = input("Vos: ").strip()
        if pregunta.lower() == "salir":
            break
        if not pregunta:
            continue
        respuesta, historial = chatear(historial, pregunta)
        print(f"\nChatbot: {respuesta}\n")

main()