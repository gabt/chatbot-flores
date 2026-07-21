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

URL_BASE = "https://flores.go.cr"

IGNORAR = [
    "facebook.com", "twitter.com", "instagram.com", "youtube.com",
    "mailto:", "tel:", ".pdf", ".gif", ".zip",
    "wp-admin", "wp-login", "feed", "xmlrpc",
    # Plugin de calendario: genera una URL distinta por cada instancia de evento recurrente
    "mc-events", "my-calendar", "cid=mc-print-view",
    # Archivos de bajo valor para el contexto del chatbot
    "/tag/", "/page/", "/author/", "index.php"
]

def debe_ignorar(url):
    for patron in IGNORAR:
        if patron in url.lower():
            return True
    return False

def dominio_normalizado(url):
    """Devuelve el dominio sin el prefijo 'www.' para poder comparar
    www.flores.go.cr y flores.go.cr como el mismo sitio."""
    netloc = urlparse(url).netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc

def crear_driver():
    opciones = Options()
    opciones.add_argument("--headless=new")  # sin ventana visible
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")
    opciones.add_argument("--window-size=1920,1080")
    opciones.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    # Evitar que el sitio detecte que es un navegador automatizado
    opciones.add_argument("--disable-blink-features=AutomationControlled")
    opciones.add_experimental_option("excludeSwitches", ["enable-automation"])
    opciones.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opciones
    )
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
    )
    return driver

def obtener_contenido(driver, url):
    try:
        driver.get(url)
        # Esperar que cargue el body
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Esperar hasta que desaparezca la pantalla de carga "Un momento…"
        # (reintenta hasta 15 segundos, revisando cada medio segundo)
        for _ in range(30):
            if "un momento" not in (driver.title or "").lower():
                cuerpo = driver.find_element(By.TAG_NAME, "body").text
                if len(cuerpo) > 100:
                    break
            time.sleep(0.5)
        else:
            time.sleep(2)  # último intento por las dudas

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
                        "logo", "icon", "favicon",
                        "spinner", "placeholder", "widget"
                    ])):
                imagenes.append({"src": src, "alt": alt})
                vistas.add(src)

        # Extraer texto
        for tag in ["header", "nav", "footer", "script", "style", "noscript"]:
            for el in driver.find_elements(By.TAG_NAME, tag):
                driver.execute_script("arguments[0].remove()", el)

        texto = driver.find_element(By.TAG_NAME, "body").text
        print(f"   🔎 DEBUG: {len(texto)} caracteres de texto, {len(imagenes)} imágenes crudas, título de página: '{driver.title}'")
        return texto, imagenes

    except Exception as e:
        print(f"  ⚠️ Error en {url}: {type(e).__name__}: {e}")
        return "", []

def obtener_enlaces(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        for _ in range(30):
            if "un momento" not in (driver.title or "").lower():
                break
            time.sleep(0.5)
        enlaces = set()
        for a in driver.find_elements(By.TAG_NAME, "a"):
            href = a.get_attribute("href") or ""
            if (href
                    and dominio_normalizado(href) == dominio_normalizado(URL_BASE)
                    and not debe_ignorar(href)):
                enlaces.add(href.split("#")[0].rstrip("/"))
        print(f"   🔎 DEBUG: {len(enlaces)} enlaces internos encontrados en esta página")
        return enlaces
    except Exception as e:
        print(f"  ⚠️ Error obteniendo enlaces en {url}: {type(e).__name__}: {e}")
        return set()

# URLs conocidas del mapa de sitio
URLS_CONOCIDAS = [
    "https://flores.go.cr/",
    "https://flores.go.cr/municipalidad/informacion-general/",
    "https://flores.go.cr/municipalidad/mision-vision/",
    "https://flores.go.cr/municipalidad/organigrama/",
    "https://flores.go.cr/municipalidad/ubicacion/",
    "https://flores.go.cr/municipalidad/recursos-humanos/omil/",
    "https://flores.go.cr/municipalidad/concejo-municipal/",
    "https://flores.go.cr/municipalidad/concejo-municipal/miembros/",
    "https://flores.go.cr/alcaldia-municipal/",
    "https://flores.go.cr/canton-de-flores/",
    "https://flores.go.cr/canton-de-flores/historia/",
    "https://flores.go.cr/contribuyente/servicios/",
    "https://flores.go.cr/contribuyente/pago-en-linea/",
    "https://flores.go.cr/transparencia/",
    "https://flores.go.cr/transparencia/contratacion-administrativa/",
    "https://flores.go.cr/contactenos/",
    "https://flores.go.cr/contactenos/directorio/",
    "https://flores.go.cr/blog/",
]

def main():
    print("🚀 Iniciando scraping con Selenium...")
    driver = crear_driver()

    por_visitar = set(u.rstrip("/") for u in URLS_CONOCIDAS)
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

    with open("conocimiento.json", "w", encoding="utf-8") as f:
        json.dump(paginas, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Listo. Se procesaron {len(paginas)} páginas.")
    print(f"   Archivo guardado: conocimiento.json")

main()