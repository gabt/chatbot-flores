from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urlparse
import json
import time

URL_BASE = "https://www.flores.go.cr"

IGNORAR = [
    "facebook.com", "twitter.com", "instagram.com", "youtube.com",
    "mailto:", "tel:", ".pdf", ".gif", ".zip",
    "wp-admin", "wp-login", "feed", "xmlrpc"
]

def debe_ignorar(url):
    for patron in IGNORAR:
        if patron in url.lower():
            return True
    return False

def crear_driver():
    opciones = Options()
    opciones.add_argument("--headless")  # sin ventana visible
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")
    opciones.add_argument("--window-size=1920,1080")
    opciones.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opciones
    )
    return driver

def obtener_contenido(driver, url):
    try:
        driver.get(url)
        # Esperar que cargue el body
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(2)  # esperar JavaScript

        # Extraer imágenes
        imagenes = []
        vistas = set()
        for img in driver.find_elements(By.TAG_NAME, "img"):
            src = img.get_attribute("src") or ""
            alt = img.get_attribute("alt") or ""
            if (src.startswith("http")
                    and src not in vistas
                    and not debe_ignorar(src)
                    and not any(x in src.lower() for x in [
                        "logo", "icon", "favicon", "banner",
                        "avatar", "spinner", "placeholder", "widget"
                    ])):
                imagenes.append({"src": src, "alt": alt})
                vistas.add(src)

        # Extraer texto
        for tag in ["header", "nav", "footer", "script", "style", "noscript"]:
            for el in driver.find_elements(By.TAG_NAME, tag):
                driver.execute_script("arguments[0].remove()", el)

        texto = driver.find_element(By.TAG_NAME, "body").text
        return texto, imagenes

    except Exception as e:
        print(f"  ⚠️ Error en {url}: {e}")
        return "", []

def obtener_enlaces(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        enlaces = set()
        for a in driver.find_elements(By.TAG_NAME, "a"):
            href = a.get_attribute("href") or ""
            if (urlparse(href).netloc == urlparse(URL_BASE).netloc
                    and not debe_ignorar(href)):
                enlaces.add(href.split("#")[0].rstrip("/"))
        return enlaces
    except:
        return set()

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
    "https://www.flores.go.cr/contribuyente/servicios/",
    "https://www.flores.go.cr/contribuyente/pago-en-linea/",
    "https://www.flores.go.cr/transparencia/",
    "https://www.flores.go.cr/transparencia/contratacion-administrativa/",
    "https://www.flores.go.cr/contactenos/",
    "https://www.flores.go.cr/contactenos/directorio/",
    "https://www.flores.go.cr/blog/",
]

def main():
    print("🚀 Iniciando scraping con Selenium...")
    driver = crear_driver()

    por_visitar = set(URLS_CONOCIDAS)
    visitadas = set()
    paginas = []

    try:
        while por_visitar:
            url = por_visitar.pop()
            if url in visitadas:
                continue

            print(f"📄 [{len(visitadas)+1}] {url}")
            texto, imagenes = obtener_contenido(driver, url)

            if texto and len(texto) > 100:
                paginas.append({
                    "url": url,
                    "contenido": texto,
                    "imagenes": imagenes
                })
                print(f"   ✅ {len(imagenes)} imágenes encontradas")

            nuevos_enlaces = obtener_enlaces(driver, url)
            por_visitar.update(nuevos_enlaces - visitadas)
            visitadas.add(url)

    finally:
        driver.quit()

    with open("contenido_municipal.json", "w", encoding="utf-8") as f:
        json.dump(paginas, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Listo. Se procesaron {len(paginas)} páginas.")
    print(f"   Archivo guardado: contenido_municipal.json")

main()