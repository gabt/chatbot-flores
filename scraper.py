import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import time

URL_BASE = "https://www.flores.go.cr"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# URLs conocidas del mapa de sitio
URLS_CONOCIDAS = [
    "https://www.flores.go.cr/",
    "https://www.flores.go.cr/municipalidad/informacion-general/",
    "https://www.flores.go.cr/municipalidad/mision-vision/",
    "https://www.flores.go.cr/municipalidad/organigrama/",
    "https://www.flores.go.cr/municipalidad/ubicacion/",
    "https://www.flores.go.cr/municipalidad/recursos-humanos/omil/",
    "https://www.flores.go.cr/municipalidad/concejo-municipal/",
    "https://www.flores.go.cr/municipalidad/concejo-municipal/miembros/",
    "https://www.flores.go.cr/canton-de-flores/",
    "https://www.flores.go.cr/canton-de-flores/historia/",
    "https://www.flores.go.cr/canton-de-flores/informacion-poblacional/",
    "https://www.flores.go.cr/contribuyente/servicios/",
    "https://www.flores.go.cr/contribuyente/pago-en-linea/",
    "https://www.flores.go.cr/contribuyente/calendario-de-pagos/",
    "https://www.flores.go.cr/contribuyente/preguntas-frecuentes/",
    "https://www.flores.go.cr/transparencia/",
    "https://www.flores.go.cr/transparencia/contratacion-administrativa/",
    "https://www.flores.go.cr/transparencia/informes-economicos/",
    "https://www.flores.go.cr/transparencia/presupuesto-municipal/",
    "https://www.flores.go.cr/contactenos/",
    "https://www.flores.go.cr/contactenos/directorio/",
    "https://www.flores.go.cr/blog/",
    "https://www.flores.go.cr/mapa-del-sitio/",
]

IGNORAR = [
    "facebook.com", "twitter.com", "instagram.com", "youtube.com",
    "mailto:", "tel:", ".pdf", ".jpg", ".png", ".gif", ".zip",
    "wp-admin", "wp-login", "feed", "xmlrpc"
]

def debe_ignorar(url):
    for patron in IGNORAR:
        if patron in url.lower():
            return True
    return False

def obtener_texto_e_imagenes(url):
    try:
        respuesta = requests.get(url, timeout=15, headers=HEADERS)
        respuesta.encoding = "utf-8"
        soup = BeautifulSoup(respuesta.text, "html.parser")

        imagenes = []
        for img in soup.find_all("img", src=True):
            src = urljoin(url, img["src"])
            alt = img.get("alt", "")
            if src.startswith("http") and not debe_ignorar(src):
                imagenes.append({"src": src, "alt": alt})

        for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            tag.decompose()

        texto = soup.get_text(separator="\n", strip=True)
        return texto, imagenes
    except Exception as e:
        print(f"  ⚠️ Error en {url}: {e}")
        return "", []

def obtener_enlaces(url):
    try:
        respuesta = requests.get(url, timeout=15, headers=HEADERS)
        soup = BeautifulSoup(respuesta.text, "html.parser")
        enlaces = set()
        for a in soup.find_all("a", href=True):
            href = urljoin(url, a["href"])
            if (urlparse(href).netloc == urlparse(URL_BASE).netloc
                    and not debe_ignorar(href)):
                enlaces.add(href.split("#")[0].rstrip("/"))
        return enlaces
    except:
        return set()

def main():
    # Combinar URLs conocidas con descubrimiento automático
    por_visitar = set(URLS_CONOCIDAS)
    visitadas = set()
    paginas = []

    print("🚀 Iniciando scraping mejorado con URLs conocidas...")
    print(f"   URLs iniciales: {len(por_visitar)}\n")

    while por_visitar:
        url = por_visitar.pop()
        if url in visitadas:
            continue

        print(f"📄 [{len(visitadas)+1}] {url}")
        texto, imagenes = obtener_texto_e_imagenes(url)

        if texto and len(texto) > 100:
            paginas.append({
                "url": url,
                "contenido": texto,
                "imagenes": imagenes
            })

        nuevos_enlaces = obtener_enlaces(url)
        por_visitar.update(nuevos_enlaces - visitadas)
        visitadas.add(url)
        time.sleep(1)

    with open("contenido_municipal.json", "w", encoding="utf-8") as f:
        json.dump(paginas, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Listo. Se procesaron {len(paginas)} páginas.")
    print(f"   Archivo guardado: contenido_municipal.json")

main()