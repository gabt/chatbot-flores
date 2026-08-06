from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os
import json
import re
import unicodedata
from collections import Counter
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Cargar conocimiento del sitio municipal (incluye páginas reales scrapeadas
# y entradas de referencia externa agregadas a mano, ver conocimiento.json /
# docs/resumen_para_continuar.md, sección "Sesión 2026-08-06")
with open("conocimiento.json", "r", encoding="utf-8") as f:
    documentos = json.load(f)

# ---------------------------------------------------------------------------
# RAG real (2026-08-06): antes, construir_contexto() armaba UN bloque fijo
# con los ~173 documentos completos y ese mismo bloque se mandaba en CADA
# mensaje, sin importar la pregunta (~51,000 tokens siempre). Ahora se busca
# primero qué documentos son relevantes a la pregunta puntual (retrieval por
# palabras clave, sin librerías nuevas) y solo esos se arman como contexto.
# Esto baja los tokens por mensaje y deja que conocimiento.json siga creciendo
# sin que cada mensaje se vuelva más caro.
# ---------------------------------------------------------------------------

PALABRAS_VACIAS = {
    "de", "la", "el", "en", "que", "y", "a", "los", "se", "del", "las", "un", "por",
    "con", "no", "una", "su", "para", "es", "al", "lo", "como", "mas", "pero",
    "sus", "le", "ya", "o", "este", "si", "porque", "esta", "entre", "cuando",
    "muy", "sin", "sobre", "tambien", "me", "hasta", "hay", "donde", "quien",
    "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra", "otros",
    "ese", "eso", "ante", "ellos", "e", "esto", "mi", "antes", "algunos",
    "unos", "yo", "otro", "otras", "otra", "tanto", "esa", "estos", "mucho",
    "quienes", "nada", "muchos", "cual", "poco", "ella", "estar", "estas", "algunas",
    "algo", "nosotros", "tu", "te", "ti", "tus", "ellas", "cuanto", "cuanta",
    "cuales", "puedo", "podria", "quiero", "quisiera", "necesito", "hola",
    "buenas", "favor", "gracias", "informacion",
}


def normalizar(texto):
    """minusculas + sin tildes, para que 'jose' y 'josé' matcheen igual."""
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto


def tokenizar(texto):
    texto = normalizar(texto)
    palabras = re.findall(r"[a-z0-9]+", texto)
    return [p for p in palabras if len(p) > 2 and p not in PALABRAS_VACIAS]


LARGO_RAIZ = 6


def raiz(palabra):
    """Achica una palabra a sus primeros LARGO_RAIZ caracteres (stemming bien
    simple, sin librerías ni diccionario de sinónimos que mantener a mano) -
    para que variantes de una misma palabra matcheen entre sí, ej. 'alcalde',
    'alcaldes', 'alcaldia', 'alcaldesa' comparten la raíz 'alcald'. Esto NO
    resuelve sinónimos de raíz distinta (ej. 'basura' vs 'residuos'); para eso
    haría falta búsqueda semántica (embeddings) - ver nota en
    docs/resumen_para_continuar.md. Lo que sí soluciona: la gran mayoría de
    plurales, géneros y conjugaciones típicas del español."""
    return palabra[:LARGO_RAIZ]


# Se pre-calcula UNA sola vez al arrancar (no en cada request) el índice de
# palabras y raíces de cada documento, para no repetir ese trabajo en cada
# pregunta.
def _construir_indice(doc):
    palabras_url = tokenizar(doc.get("url", ""))
    palabras_contenido = tokenizar(doc.get("contenido", ""))
    return {
        "doc": doc,
        "url_exacto": Counter(palabras_url),
        "url_raiz": Counter(raiz(p) for p in palabras_url),
        "contenido_exacto": Counter(palabras_contenido),
        "contenido_raiz": Counter(raiz(p) for p in palabras_contenido),
    }


_DOCS_INDEXADOS = [_construir_indice(doc) for doc in documentos]


def buscar_documentos_relevantes(pregunta, top_n=6):
    """Retrieval por palabras clave (+ raíz): puntúa cada documento según
    cuántas palabras de la pregunta aparecen en su url/contenido. La URL pesa
    más (suele traer el tema en el slug, ej. 'recoleccion-de-desechos'), el
    match EXACTO pesa más que el match por RAÍZ (así 'patente' no le gana a
    'patentes' de pura casualidad, pero igual matchean si hace falta).
    Devuelve los top_n documentos con mejor puntaje (score > 0). Si ninguno
    matchea, devuelve una lista vacía y el chatbot recurre a la búsqueda web."""
    palabras = tokenizar(pregunta)
    if not palabras:
        return []
    raices = [raiz(p) for p in palabras]

    puntuados = []
    for item in _DOCS_INDEXADOS:
        score = 0
        for palabra, r in zip(palabras, raices):
            score += item["url_exacto"].get(palabra, 0) * 6
            score += item["url_raiz"].get(r, 0) * 3
            score += item["contenido_exacto"].get(palabra, 0) * 2
            score += item["contenido_raiz"].get(r, 0) * 1
        if score > 0:
            puntuados.append((score, item["doc"]))

    puntuados.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in puntuados[:top_n]]


def construir_contexto(docs):
    contexto = ""
    for doc in docs:
        contexto += f"\n\n--- Página: {doc['url']} ---\n"
        contexto += doc["contenido"][:3000]
    return contexto


SYSTEM_PROMPT_BASE = """Sos un asistente virtual de la Municipalidad de Flores, Costa Rica.
Respondés preguntas de ciudadanos de forma clara, amable y en español.

Tenés dos fuentes de información:
1. La INFORMACIÓN DEL SITIO WEB MUNICIPAL que se te da abajo (páginas reales de flores.go.cr y
   entradas de referencia agregadas a mano) - basate en ella primero, es la más confiable para
   trámites y datos propios de la Municipalidad de Flores.
2. Una herramienta de búsqueda web, para preguntas que la información de abajo NO cubre: por
   ejemplo comparaciones con OTRAS municipalidades del país, rankings nacionales, información de
   un barrio específico que no aparece abajo, o cualquier otro dato externo puntual. Usala cuando
   haga falta, y decile a la persona de dónde sacaste el dato.

Si no encontrás la respuesta ni en la información de abajo ni buscando, decilo con honestidad y
sugerí llamar al 2265-7109 en vez de inventar una respuesta.

Sé breve y concreto: respondé puntualmente lo que se pregunta, sin agregar datos que no se
pidieron. Por ejemplo, si preguntan "¿quién es el alcalde?", respondé el nombre y el cargo -
no hace falta agregar su formación académica ni quién es la vicealcaldesa a menos que lo pidan.
Si hay más información relevante disponible, podés OFRECER dar más detalles al final ("¿querés
que te cuente más sobre...?") en vez de volcarla toda de una.

Formato: podés usar **negrita** (así, con doble asterisco) para resaltar lo más importante -
nombres, cifras, plazos - se muestra en negrita de verdad en el chat. Evitá otro formato Markdown
(encabezados, viñetas, tablas): este chat solo interpreta negrita y saltos de línea, el resto se
vería como texto crudo.

INFORMACIÓN DEL SITIO WEB MUNICIPAL (relevante a esta pregunta puntual):
{contexto}
"""

# Mapa de secciones a palabras clave en URLs (se usa en /imagenes/<seccion>, sin cambios)
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

    docs_relevantes = buscar_documentos_relevantes(pregunta, top_n=6)
    contexto = construir_contexto(docs_relevantes)
    if not contexto:
        contexto = ("(No se encontró ninguna página local relacionada con esta pregunta puntual "
                    "- usá la búsqueda web si hace falta para responderla.)")
    system_prompt = SYSTEM_PROMPT_BASE.format(contexto=contexto)

    mensajes = historial + [{"role": "user", "content": pregunta}]

    try:
        respuesta_api = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=2048,
            system=system_prompt,
            messages=mensajes,
            tools=[
                {
                    "type": "web_search_20250305",
                    "name": "web_search",
                    # Tope de búsquedas por pregunta, para no disparar el costo
                    # ($0.01 por búsqueda + tokens de los resultados).
                    "max_uses": 3,
                    # NOTA 2026-08-06: se había agregado "user_location" con
                    # country: "CR" para sesgar resultados a Costa Rica, pero
                    # la API respondió "Country code CR is not supported" y
                    # eso tumbaba TODAS las preguntas (no solo las externas),
                    # porque esta herramienta viaja en cada mensaje. Se quita
                    # por ahora; ver si el proyecto quiere investigar qué
                    # códigos de país sí soporta antes de volver a intentarlo.
                }
            ],
        )

        # La respuesta puede traer varios bloques de texto intercalados con la
        # búsqueda (ej.: texto ANTES de buscar + búsqueda + texto DESPUÉS,
        # continuando la misma idea). Hay que unir TODOS los bloques de texto
        # en orden - quedarse solo con el último corta la respuesta a la mitad
        # (bug real detectado 2026-08-06: se perdía el nombre del alcalde
        # porque venía en el primer bloque, antes de la búsqueda).
        bloques_texto = [b for b in respuesta_api.content if b.type == "text"]
        if bloques_texto:
            texto_respuesta = "".join(b.text for b in bloques_texto).strip()

            # Juntamos las citas de TODOS los bloques (no solo el último) por
            # si la búsqueda se usó más de una vez en la misma respuesta.
            fuentes = []
            vistos = set()
            for b in bloques_texto:
                for c in (getattr(b, "citations", None) or []):
                    url = getattr(c, "url", None)
                    if url and url not in vistos:
                        vistos.add(url)
                        fuentes.append(url)
            if fuentes:
                texto_respuesta += "\n\nFuentes consultadas:\n" + "\n".join(f"- {u}" for u in fuentes)
        else:
            texto_respuesta = "Disculpá, no pude generar una respuesta. Intentá de nuevo o llamá al 2265-7109."
    except Exception as e:
        return jsonify({"error": f"Error al consultar la API de Claude: {str(e)}"}), 500

    nuevo_historial = mensajes + [{"role": "assistant", "content": texto_respuesta}]

    return jsonify({
        "respuesta": texto_respuesta,
        "historial": nuevo_historial,
        # Informativo (el frontend no lo necesita): qué páginas locales se
        # usaron para esta respuesta, útil para depurar/demostrar el RAG.
        "fuentes_locales": [d["url"] for d in docs_relevantes],
    })


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
