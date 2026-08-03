# Guía de continuidad para Jeiron - Chatbot Municipalidad de Flores

Bienvenido al proyecto. Esta guía es para vos: explica cómo retomar el trabajo que Gerardo
(tu tutor) viene haciendo con Claude, sin necesidad de que él esté siempre presente.

## 1. El proyecto en una frase
Un chatbot/sitio prototipo que replica la información real de flores.go.cr (Municipalidad de
Flores), con un asistente de IA (Claude) integrado. El trabajo actual es un **repaso nodo por
nodo**: comparar cada opción del menú de nuestro prototipo contra la página real del sitio,
y arreglar cualquier diferencia.

## 2. Los archivos - qué es cada uno
Todos viven en el repositorio de GitHub (`github.com/gabt/chatbot-flores`). Al empezar una
sesión nueva con Claude, subís estos 5 archivos (siempre las versiones más recientes de tu
repo local, no copias viejas):

| Archivo | Para qué sirve |
|---|---|
| `index.html` | El código del sitio. Todo lo que Claude te ayuda a arreglar vive acá. |
| `conocimiento.json` | Los datos scrapeados del sitio real (~166 páginas). Rara vez hace falta tocarlo directamente. |
| `mapa_organizado.md` | El mapa completo del menú del sitio real, mapeado a mano. Es la "lista de tareas" - qué falta revisar. |
| `resumen_para_continuar.md` | **El más importante para arrancar.** Tiene el historial técnico completo: qué se revisó, qué se arregló, qué mecanismos existen, y dónde quedamos. |
| `recomendaciones_informe_final.md` | Errores propios del SITIO REAL (no nuestros) para mencionar en el informe final - cosas como texto atrapado en imágenes, links mal puestos, etc. |

## 3. Cómo arrancar una sesión nueva con Claude
1. Abrí una conversación nueva con Claude.
2. Subí los 5 archivos de la tabla de arriba.
3. Decile algo como: *"Acá está el proyecto del chatbot de la Municipalidad de Flores. Leé
   `resumen_para_continuar.md` para ponerte al día y decime en qué nodo quedamos."*
4. Claude va a leer el resumen y decirte exactamente dónde quedó Gerardo (al momento de esta
   guía: a punto de empezar la sección **Contribuyente**).

## 4. La metodología de repaso (cómo trabajamos hasta ahora)
Para cada nodo del menú (ej. "Formularios", "Trámites"):
1. Le pedís a Claude el siguiente nodo a revisar (o él te lo va proponiendo en orden).
2. Vos abrís esa misma sección en **nuestro prototipo** (gabt.github.io/chatbot-flores) Y en
   el **sitio real** (flores.go.cr), y comparás.
3. Le contás a Claude en texto simple qué diferencias ves (screenshots ayudan mucho - Claude
   puede leer capturas de pantalla directamente).
4. Claude investiga la causa (a veces revisa el código, a veces le hace `web_fetch` al sitio
   real para confirmar datos exactos) y te propone o aplica un arreglo.
5. Claude te da las 3 líneas de PowerShell para subir el cambio:
   ```powershell
   git add index.html
   git commit -m "mensaje descriptivo del cambio"
   git push
   ```
6. Confirmás en el sitio ya desplegado (esperá 1-2 min por GitHub Pages, y hacé `Ctrl+F5` si
   el navegador te muestra la versión vieja por caché).
7. Pasás al siguiente nodo.

## 5. Cosas importantes que ya aprendimos (para no perder tiempo redescubriéndolas)
- El sitio real (flores.go.cr) es frágil e inconsistente: a veces se cae, a veces cambia
  contenido de un día para otro. Si algo se ve raro, **primero verificá si el problema está
  en el sitio real** antes de asumir que es un bug nuestro.
- El scraper (que ya scrapeó todo, no hace falta correrlo de nuevo) tiene algunas limitaciones
  conocidas: pierde la asociación exacta entre una imagen y su texto en ciertos casos (tablas,
  listas de blog, listas de nombres). Cuando encuentres algo así, Claude ya tiene mecanismos
  reutilizables para resolverlo sin tocar el scraper (ver `resumen_para_continuar.md`, sección
  "Mecanismos opt-in por nodo") - Claude sabe usarlos, solo hace falta que le describas bien la
  diferencia que ves.
- Evitá pedir que se vuelva a scrapear el sitio completo salvo que sea realmente necesario - es
  lento y en una ocasión coincidió con una caída del sitio real.

## 6. Dónde quedamos ahora mismo (2026-07-27)
✅ **Terminado:** toda la sección "Municipalidad" (Información General, Concejo Municipal,
Comités Municipales, Marco Normativo, Transparencia, Planes y Proyectos, Gestión Ambiental,
Recursos Humanos).

▶️ **Sigue:** sección **"Contribuyente"** - Artesanos, Servicios (Formularios, Trámites, Mapa
Catastral, Plan Regulador de Flores, Recolección de desechos), Pago en línea, Preguntas
Frecuentes, Amnistía Tributaria. El detalle completo está en `mapa_organizado.md`.

## 7. Si te trabás
Si Claude te pide una decisión que no sabés cómo tomar (ej. "¿arreglamos esto con hardcode o
ajustando el scraper?"), es buen momento para consultarle a Gerardo. No hay prisa en decidir
mal - Claude siempre explica las opciones y sus tradeoffs antes de pedir que elijas.

¡Éxitos con la pasantía!
