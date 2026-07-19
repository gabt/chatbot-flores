import json
import re

def limpiar_texto(texto):
    # Eliminar líneas vacías múltiples
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    # Eliminar espacios extras
    texto = re.sub(r' {2,}', ' ', texto)
    return texto.strip()

def main():
    with open("contenido_municipal.json", "r", encoding="utf-8") as f:
        paginas = json.load(f)

    documentos = []
    for pagina in paginas:
        texto_limpio = limpiar_texto(pagina["contenido"])
        if len(texto_limpio) > 100:  # ignorar páginas casi vacías
            documentos.append({
                "url": pagina["url"],
                "contenido": texto_limpio
            })

    with open("conocimiento.json", "w", encoding="utf-8") as f:
        json.dump(documentos, f, ensure_ascii=False, indent=2)

    print(f"✅ Procesadas {len(documentos)} páginas útiles.")
    print("Archivo guardado: conocimiento.json")

main()