from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urlparse
from collections import Counter
import json
import time

URL_BASE = "https://flores.go.cr"

# Dominios permitidos para el crawler: el sitio principal y el portal
# municipal de actas/sesiones, que vive en un subdominio aparte.
DOMINIOS_PERMITIDOS = {
    "flores.go.cr",
    "portalmuni.flores.go.cr",
}

IGNORAR = [
    "facebook.com", "twitter.com", "instagram.com", "youtube.com",
    "mailto:", "tel:", ".pdf", ".gif", ".zip",
    "wp-admin", "wp-login", "feed", "xmlrpc",
    # Plugin de calendario: genera una URL distinta por cada instancia de evento recurrente
    "mc-events", "my-calendar", "cid=mc-print-view",
    # Archivos de bajo valor para el contexto del chatbot
    "/tag/", "/page/", "/author/", "index.php",
    "@",  # links "mailto:" mal armados en el sitio que el navegador resuelve como URL relativa
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

def es_dominio_permitido(url):
    """True si la URL pertenece a alguno de los dominios que el crawler
    tiene permitido recorrer (sitio principal o el portal de actas)."""
    return dominio_normalizado(url) in DOMINIOS_PERMITIDOS

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

def obtener_contenido(driver, url, reintentos=2):
    try:
        driver.get(url)
        # Esperar que cargue el body
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Si el sitio devuelve un error genérico de WordPress (a veces
        # transitorio por límite de peticiones), esperamos un poco y reintentamos
        intento = 0
        while "wordpress" in (driver.title or "").lower() and "error" in (driver.title or "").lower() and intento < reintentos:
            intento += 1
            print(f"      ⏳ 'WordPress › Error' detectado, reintento {intento}/{reintentos} en 5s...")
            time.sleep(5)
            driver.get(url)
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

        # Extraer imágenes, junto con el encabezado más cercano (su "contexto" temático).
        # Ignoramos encabezados de widgets que se repiten en muchas páginas y no
        # describen el contenido real (ej. "Entradas relacionadas", el lector de
        # accesibilidad "Spoken Word").
        BUSCAR_CONTEXTO_JS = """
            function buscarContexto(el) {
                const RUIDO = ['entradas relacionadas', 'spoken word', 'related posts', 'you may also like'];
                function esRuido(texto) {
                    const t = texto.toLowerCase();
                    return RUIDO.some(r => t.indexOf(r) !== -1);
                }
                let nodo = el;
                while (nodo && nodo.tagName !== 'BODY') {
                    let hermano = nodo.previousElementSibling;
                    while (hermano) {
                        let candidato = null;
                        if (/^H[1-6]$/.test(hermano.tagName)) {
                            candidato = hermano.innerText.trim();
                        } else {
                            const interno = hermano.querySelector('h1,h2,h3,h4,h5,h6');
                            if (interno) candidato = interno.innerText.trim();
                        }
                        if (candidato && !esRuido(candidato)) {
                            return candidato;
                        }
                        hermano = hermano.previousElementSibling;
                    }
                    nodo = nodo.parentElement;
                }
                return null;
            }
            return buscarContexto(arguments[0]);
        """

        BUSCAR_ENLACE_JS = """
            const a = arguments[0].closest('a');
            if (!a) return null;
            const href = a.getAttribute('href') || '';
            if (!href || href.startsWith('javascript:') || href === '#') return null;
            return a.href;
        """

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
                try:
                    contexto = driver.execute_script(BUSCAR_CONTEXTO_JS, img)
                except Exception:
                    contexto = None
                try:
                    enlace = driver.execute_script(BUSCAR_ENLACE_JS, img)
                except Exception:
                    enlace = None
                imagenes.append({"src": src, "alt": alt, "contexto": contexto, "enlace": enlace})
                vistas.add(src)

        # Extraer texto
        for tag in ["header", "nav", "footer", "script", "style", "noscript"]:
            for el in driver.find_elements(By.TAG_NAME, tag):
                driver.execute_script("arguments[0].remove()", el)

        texto = driver.find_element(By.TAG_NAME, "body").text

        # Cortar el banner de consentimiento de cookies (aparece pegado al
        # final del texto en casi todas las páginas del sitio, en inglés,
        # inyectado por un plugin de terceros - no es contenido real).
        MARCA_COOKIES = "We respect your privacy"
        idx_cookies = texto.find(MARCA_COOKIES)
        if idx_cookies != -1:
            texto = texto[:idx_cookies].rstrip()

        # Detectar páginas "404 suaves": no dan error de servidor ni de título,
        # pero muestran el mensaje típico de WordPress de página no encontrada.
        FRASES_404 = [
            "no se ha podido encontrar esa página",
            "no se ha podido encontrar la página",
            "page not found",
        ]
        if any(frase in texto.lower() for frase in FRASES_404):
            print(f"   ⚠️ Página 404 detectada (contenido de 'no encontrada'), se descarta: {url}")
            return "", []

        print(f"   🔎 DEBUG: {len(texto)} caracteres de texto, {len(imagenes)} imágenes crudas, título de página: '{driver.title}'")
        for img in imagenes[:3]:
            print(f"      🖼️  contexto='{img.get('contexto')}' | alt='{img.get('alt')[:40]}'")
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
                    and es_dominio_permitido(href)
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
    # Portal de actas y sesiones del Concejo Municipal (subdominio aparte)
    "http://portalmuni.flores.go.cr/actas/bgeneral.php",
    "http://portalmuni.flores.go.cr/actas/buscar.php",
]

def main():
    print("🚀 Iniciando scraping con Selenium...")
    driver = crear_driver()

    # Usamos una lista (no un set) para que el orden de visita sea siempre
    # el mismo entre corridas: primero las URLs conocidas en su orden original,
    # y después las que se van descubriendo, en el orden en que aparecen.
    ya_vistas_o_en_cola = set()
    por_visitar = []
    for u in URLS_CONOCIDAS:
        u = u.rstrip("/")
        if u not in ya_vistas_o_en_cola:
            por_visitar.append(u)
            ya_vistas_o_en_cola.add(u)

    visitadas = set()
    paginas = []

    try:
        while por_visitar:
            url = por_visitar.pop(0)
            if url in visitadas:
                continue

            print(f"📄 [{len(visitadas)+1}] {url}")
            texto, imagenes = obtener_contenido(driver, url)

            tiene_botones_de_navegacion = any(img.get("enlace") for img in imagenes)
            if texto and (len(texto) > 100 or tiene_botones_de_navegacion):
                paginas.append({
                    "url": url,
                    "contenido": texto,
                    "imagenes": imagenes
                })
                print(f"   ✅ {len(imagenes)} imágenes encontradas")

            nuevos_enlaces = sorted(obtener_enlaces(driver, url))
            for enlace in nuevos_enlaces:
                if enlace not in ya_vistas_o_en_cola:
                    por_visitar.append(enlace)
                    ya_vistas_o_en_cola.add(enlace)
            visitadas.add(url)
            time.sleep(1)  # pausa breve para no saturar al servidor

    finally:
        driver.quit()

    # Filtrar imágenes "widget": las que se repiten idénticas en muchas
    # páginas distintas son elementos fijos de barra lateral/plugins, no
    # contenido específico de cada página (ej. banners, iconos de accesibilidad).
    UMBRAL_REPETICION = 5
    conteo_por_src = Counter()
    for pagina in paginas:
        for img in pagina.get("imagenes", []):
            conteo_por_src[img.get("src")] += 1
    srcs_widget = {src for src, n in conteo_por_src.items() if n >= UMBRAL_REPETICION}

    if srcs_widget:
        print(f"\n🧹 Filtrando {len(srcs_widget)} imágenes tipo widget (repetidas en {UMBRAL_REPETICION}+ páginas)...")
        for pagina in paginas:
            pagina["imagenes"] = [
                img for img in pagina.get("imagenes", [])
                if img.get("src") not in srcs_widget
            ]

    with open("conocimiento.json", "w", encoding="utf-8") as f:
        json.dump(paginas, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Listo. Se procesaron {len(paginas)} páginas.")
    print(f"   Archivo guardado: conocimiento.json")

main()