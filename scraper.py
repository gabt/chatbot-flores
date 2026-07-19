import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import time

URL_BASE = "https://www.flores.go.cr"

def obtener_texto(url):
    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.encoding = "utf-8"
        soup = BeautifulSoup(respuesta.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        texto = soup.get_text(separator="\n", strip=True)
        return texto
    except Exception as e:
        print(f"Error en {url}: {e}")
        return ""

def obtener_enlaces(url):
    try:
        respuesta = requests.get(url, timeout=10)
        soup = BeautifulSoup(respuesta.text, "html.parser")
        enlaces = set()
        for a in soup.find_all("a", href=True):
            href = urljoin(url, a["href"])
            if urlparse(href).netloc == urlparse(URL_BASE).netloc:
                enlaces.add(href.split("#")[0])
        return enlaces
    except:
        return set()

def main():
    visitadas = set()
    por_visitar = {URL_BASE}
    paginas = []

    print("Iniciando scraping...")

    while por_visitar and len(visitadas) < 50:
        url = por_visitar.pop()
        if url in visitadas:
            continue

        print(f"Procesando: {url}")
        texto = obtener_texto(url)

        if texto:
            paginas.append({"url": url, "contenido": texto})

        nuevos_enlaces = obtener_enlaces(url)
        por_visitar.update(nuevos_enlaces - visitadas)
        visitadas.add(url)
        time.sleep(1)

    with open("contenido_municipal.json", "w", encoding="utf-8") as f:
        json.dump(paginas, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Listo. Se procesaron {len(paginas)} páginas.")
    print("Archivo guardado: contenido_municipal.json")

main()