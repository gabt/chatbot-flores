# Resumen para continuar - Chatbot Municipalidad de Flores

## Stack
Claude (orquestador) + Python + Selenium (scraping) + Flask + Gunicorn + Render.com (backend) +
GitHub + GitHub Pages (frontend) + PowerShell (terminal local) + HTML/CSS/JS vanilla + JSON
(conocimiento.json) + Claude API (motor del chat) + WordPress (CMS del sitio real, fuente de datos).

## URLs
- Sitio: https://gabt.github.io/chatbot-flores
- Backend: https://chatbot-flores.onrender.com
- GitHub: https://github.com/gabt/chatbot-flores
- Sitio real: https://flores.go.cr + http://portalmuni.flores.go.cr (portal de actas, sin HTTPS)

## Arquitectura actual
- `scraper.py`: recorre ambos dominios, filtra widgets repetidos, cookies, "Leer Contenido",
  404 suaves, corrige URLs con "localhost" mal configuradas; captura src/alt/contexto/enlace
  por imagen. Cola FIFO determinística, reintentos, pausas de 1s entre páginas.
- `conocimiento.json`: ~166 páginas limpias.
- `app.py`: rutas `/chat`, `/imagenes/<seccion>` (legado), `/paginas` (devuelve todo crudo,
  la usa el frontend para el árbol).
- `index.html`: navegación en árbol lateral (sidebar) que refleja la jerarquía real del sitio.

## Documentos de seguimiento (ambos en Markdown por ahora, se pasan a Word al final)
- `mapa_organizado.md`: el árbol de navegación completo, mapeado a mano con el usuario.
- `resumen_para_continuar.md`: este archivo.
- `recomendaciones_informe_final.md`: **NUEVO HOY** - observaciones sobre el SITIO REAL (no
  bugs nuestros) para mencionar como recomendaciones de mejora en el informe final. Hasta ahora:
  (1) "Nuestros Valores" tiene el texto encerrado en una imagen (mal para accesibilidad/SEO);
  (2) el mapa de "Ubicación" usa un widget de Waze poco práctico en escritorio (mejor pensado
  para celular). Seguir agregando entradas acá cuando aparezcan, separado de los fixes técnicos.

## Funcionalidades clave agregadas hoy en index.html
1. **Zoom en imágenes de contenido**: cualquier imagen sin link de navegación (fotos, diagramas)
   ahora es clickeable para abrir la versión de tamaño completo en pestaña nueva (cursor de lupa).
   Fue necesario porque imágenes como el Mapa Organizacional se ven ilegibles en miniatura.
2. **Detección de listas reales**: texto con varias líneas cortas seguidas ahora se renderiza
   como `<ul><li>` (viñetas) en vez de líneas sueltas con `<br>`.
3. **Heurística de subtítulos refinada**: una línea corta solo se pone en negrita (subtítulo) si
   la línea SIGUIENTE es un párrafo largo real - esto evita que ítems de lista (ej. "Gestión de
   Cobros", "Patentes") se confundan con títulos reales (ej. "Administración Tributaria").
4. **Corrección de URLs "localhost"**: 4 imágenes del sitio real tenían el dominio mal puesto
   (apuntaban a "localhost/muniflorespw" en vez de "flores.go.cr") - corregido en datos y scraper.
5. **Cierre automático del menú en celular**: al elegir un nodo final (sin hijos) o "Inicio" en
   pantalla chica (≤800px), el sidebar se cierra solo para mostrar el contenido de una vez.
6. **circuloVerde opt-in por nodo**: el círculo de fondo verde para íconos clickeables ya NO es
   automático - solo se aplica a nodos marcados a mano con `circuloVerde: true` (por ahora solo
   "Formularios"), porque otros nodos (ej. "Servicios") ya traen su propio círculo blanco
   embebido en la imagen y se veía mal duplicado.
7. **Imágenes clickeables por "link confiable"**: se generalizó de "solo portalmuni" a cualquier
   imagen cuyo `enlace` no sea una IP directa ni una URL de vista previa de WordPress.
8. **ETIQUETAS_MANUALES**: diccionario para corregir etiquetas mal puestas en el sitio real
   (ej. dice "Servicios" en vez de "Bienes Inmuebles" en el atributo alt de esa imagen).

## Mecanismos opt-in por nodo (agregados hoy, reutilizables en cualquier página de contenido)
Todos son opcionales y se activan solo agregando la propiedad al nodo en el árbol de `index.html`
- no afectan ninguna otra página a menos que se agreguen explícitamente.
9. **`galeriaAlFinal: true`**: invierte el orden por defecto (galería antes del texto) - útil
   cuando las fotos ilustran un evento descrito en el texto, en vez de ser la imagen principal.
10. **`imagenesEnTexto: [{ contieneEnlace, despuesDeTexto }]`**: saca una imagen puntual de la
    galería general y la inserta justo después del párrafo que la menciona en el texto.
11. **`lineasOmitir: [...]`**: quita líneas exactas del texto scrapeado (ej. título de la página
    repetido como primera o última línea del contenido, puro ruido redundante con el `<h2>`).
12. **`tablaTexto: { anclaInicio, anclaFin, titulo, columnas, filas }`**: reemplaza un tramo de
    texto plano (ancla a ancla) por una tabla HTML real con datos curados a mano - para cuando
    el sitio real tiene una tabla de verdad (ej. Nombre/Puesto) que el scraper aplanó a líneas
    sueltas, perdiendo la estructura de columnas.
13. **`listasEnlaces: { anclaInicio, anclaFin, categorias: [{ titulo, enlaces: [{texto, href}] }] }`**:
    mismo espíritu que `tablaTexto`, pero para cuando el sitio real tiene texto con hipervínculo
    (ej. una lista de leyes/reglamentos, cada una linkeada a un PDF en Drive) que el scraper no
    captura en absoluto, porque solo extrae `href` de imágenes, nunca de texto (ver sección de
    "Mejora futura de arquitectura" más abajo). `anclaFin: null` extrae hasta el final del texto.
14. **`tipo: 'especial-blog'` / `renderBlog`**: para listados tipo blog (ej. categorías del blog
    real). El scraper desfasa el "contexto" de cada imagen una posición en este tipo de listado
    (la imagen de cada post viene ANTES de su título en el HTML real) y pierde la primera imagen
    por completo. Se resuelve con `nodo.posts` (array curado a mano: imagen, título, resumen,
    fecha, link), confirmado contra el sitio real vía `web_fetch`. Reutilizable tal cual para
    cualquier categoría de "Noticias y Comunicados".

## Progreso de la revisión nodo por nodo

### Municipalidad → Información General ✅ COMPLETO
✅ Alcaldía Municipal - perfecto
✅ Organigrama - CAMBIADO a nodo agrupador puro (su página real es solo un menú redundante)
✅ Mapa Organizacional - funciona con zoom (imagen chica en miniatura, grande al hacer click)
✅ Niveles - CAMBIADO a nodo agrupador puro (mismo motivo que Organigrama)
✅ Nivel Político - perfecto
✅ Nivel de Fiscalización - perfecto
✅ Nivel Sustantivo - arreglado el problema de listas (ver funcionalidades 2 y 3 arriba)
✅ Nivel de Apoyo - tiene un caso de lista ANIDADA (ej. "Gestión Financiera" con sub-ítems)
   que se muestra como lista plana sin la jerarquía real - LIMITACIÓN ACEPTADA por ahora
   (ver sección de abajo), no bloqueante.
✅ Salarios Base 2021 - NO PROBADO TODAVÍA
✅ Misión y Visión - perfecto (ya validado en sesión anterior)
✅ Nuestros Valores - funciona con zoom (mismo patrón que Mapa Organizacional)
✅ Ubicación - CAMBIADO a tipo 'externo' → abre Google Maps directo (la página real solo tiene
   un iframe de Waze que no podemos scrapear, y encima daba error intermitente de WordPress)

### Municipalidad → Concejo Municipal ✅ COMPLETO
✅ Información del Concejo - perfecto, subtítulos y funciones se detectan bien
✅ Miembros del Concejo Municipal - CAMBIADO a función bespoke (`renderMiembros`): antes
   colapsaba todo en una lista plana sin jerarquía (Regidores/Síndicos/Distrito se mezclaban
   con los nombres). Ahora muestra la estructura real (Regidores Propietarios/Suplentes,
   Síndicos por Distrito con Propietario/Suplente) CON la bandera de partido político correcta
   junto a cada nombre - la asociación nombre↔bandera se confirmó leyendo la tabla real del
   sitio (el scraper deduplica imágenes por `src` y pierde el emparejamiento fila a fila de
   una tabla, mismo síntoma que el caso de "Documentación" más abajo).
✅ Actas del Concejo - confirmado, botones hardcodeados coinciden con el sitio real

### Municipalidad → Comités Municipales ✅ COMPLETO
✅ Comités Municipales (nodo padre) - CAMBIADO a agrupador puro (mismo patrón de Organigrama)
✅ Comité Cantonal de la Persona Joven - agregado `galeriaAlFinal: true` (las fotos del "Vive
   Flores Fest" ilustran el evento descrito en el texto, van después no antes)
✅ Comité Cantonal de Deportes y Recreación - varios fixes: `tablaTexto` para la Junta Directiva
   (Nombre/Puesto, antes lista plana), `imagenesEnTexto` para insertar el logo/link de YouTube
   justo donde el texto lo menciona, `lineasOmitir` para el título duplicado. Se investigó un
   supuesto link de Facebook faltante - descartado, el usuario confirmó que no existe en el
   sitio real (fue una confusión con el Facebook de "Persona Joven", que es un comité distinto).

### Municipalidad → Marco Normativo ✅ COMPLETO
✅ Marco Normativo (nodo padre) - CAMBIADO a agrupador puro
✅ Documentación - CAMBIO GRANDE: se descubrió que ~28 ítems de esta página son en realidad
   links de texto a documentos de Drive (leyes, reglamentos, políticas, manuales) que el scraper
   nunca capturó (ver "Mejora futura de arquitectura" abajo). Se resolvió con `listasEnlaces`,
   usando los links reales leídos directo del sitio vía `web_fetch`. También se descubrió que la
   página real creció (nuevas secciones "Recursos Humanos" y "Normativas") desde que la
   scrapeamos - la última modificación fue apenas 3 días antes de esta sesión.
✅ Plan Regulador de Flores (bajo Marco Normativo) - `galeriaAlFinal` + `lineasOmitir` para el
   título duplicado. ⚠️ Esta misma URL (`plan-regulador-de-flores`) está referenciada por otros
   DOS nodos todavía sin revisar: "Plan Regulador" (bajo Planes y Proyectos) y "Plan Regulador de
   Flores" (bajo Contribuyente > Servicios) - muy probablemente necesiten el mismo fix.

### Municipalidad → Transparencia (nodo top-level aparte) ✅ COMPLETO
✅ Confirmado: el "Transparencia" chiquito dentro del dropdown de Municipalidad es un atajo
   externo a propósito (con nota de "ver la sección completa más abajo") - NO es un bug, es un
   nodo distinto al "Transparencia" de nivel superior (que sí tiene todos los hijos mapeados).
✅ Todos los hijos externos (Acceso a la Información, Información Institucional, Rendición de
   cuentas, Participación ciudadana, Datos Abiertos, Red de Transparencia) muestran correctamente
   "Abrir en el sitio real".
✅ Los 4 hijos que reutilizan contenido real (Servicios y Procesos Institucionales, Presupuesto
   Municipal, Toma de Decisiones, Planes y Cumplimiento) muestran contenido real (Excel/PDF según
   corresponda), confirmado por el usuario.

### Municipalidad → Planes y Proyectos ✅ COMPLETO
✅ Plan Anual Operativo - tenía placeholder "enlace pendiente" pese a que el link real ya estaba
   capturado en `conocimiento.json` desde el principio (nunca se conectó al nodo). Conectado.
✅ Plan de Desarrollo Urbano Cantonal - confirmado como enlace roto de verdad (sin `enlace` en
   la imagen real), consistente con lo ya mapeado.
✅ Plan de Conservación y Desarrollo Vial - mismo caso que Plan Anual Operativo, link real ya
   capturado pero no conectado. Conectado.
✅ Plan Regulador - mismo fix de `galeriaAlFinal` + `lineasOmitir` que el de Marco Normativo
   (comparten la misma URL scrapeada, pero son nodos distintos en el árbol). ⚠️ Queda un TERCER
   nodo con esta misma URL sin revisar todavía: "Plan Regulador de Flores" bajo
   Contribuyente > Servicios.

### Municipalidad → Gestión Ambiental ✅ COMPLETO
✅ CAMBIO GRANDE: se descubrió que el scraper desfasa el "contexto" de cada imagen una posición
   en listados tipo blog (la imagen de cada post viene ANTES de su propio título en el HTML real,
   así que el contexto capturado corresponde al título del post ANTERIOR), y además pierde la
   primera imagen del listado por completo. Se resolvió con una función bespoke NUEVA y
   reutilizable: `tipo: 'especial-blog'` / `renderBlog(nodo, pane)`, con los posts curados a mano
   (imagen, título, resumen, fecha, link) confirmados directo contra el sitio real vía
   `web_fetch`. Muy probablemente el mismo mecanismo sirva tal cual para "Noticias y Comunicados"
   más adelante (mismo tipo de listado de blog).

### Municipalidad → Recursos Humanos ✅ COMPLETO
✅ Nuestro prototipo se ve MEJOR que el sitio real en este momento - el sitio real está
   visiblemente en obras (íconos gigantescos, ítem "Complementos Salariales" desaparecido). Es
   evidencia adicional de que el sitio está en cambios activos (ver nota de arquitectura del
   scraper más arriba). Nada que ajustar de nuestro lado.

## 🎉 MUNICIPALIDAD (dropdown completo) - TERMINADO 2026-07-27
Las 7 secciones de Municipalidad están revisadas y confirmadas: Información General, Concejo
Municipal, Comités Municipales, Marco Normativo, Transparencia (el atajo), Planes y Proyectos,
Gestión Ambiental, Recursos Humanos.

### Siguiente paso inmediato: sección "Contribuyente"
Según `mapa_organizado.md`: Artesanos (Plataforma/Solicitud), Servicios (Formularios, Trámites,
Mapa Catastral, Plan Regulador de Flores - mismo caso pendiente de arriba, Plan Cantonal de
Desarrollo Humano Local, Recolección de desechos), Pago en línea (Calendario de pagos - marcado
como caído), Preguntas Frecuentes (marcado como caído), Amnistía Tributaria.

**PAUSADO 2026-07-26**: el usuario notó inconsistencias en el sitio real que sugieren que lo
están actualizando activamente (ver nota de "Documentación" arriba, modificada 3 días antes de
esta sesión) y decidió parar acá para retomar con cabeza fresca, verificando primero qué cambió
antes de seguir con Planes y Proyectos.

## Limitación conocida, aceptada por ahora (posible mejora futura)
Las listas ANIDADAS del sitio real (ítem padre con sub-ítems debajo, y la lista sigue en el
mismo nivel después) se muestran como lista PLANA en nuestro prototipo, sin la jerarquía real -
porque el scraper extrae solo texto plano (body.text de Selenium), que no conserva la
profundidad de anidación de los `<li>`. Decisión: aceptar por ahora (es cosmético, la
información sigue siendo correcta). Arreglo de fondo posible más adelante: cambiar el scraper
para recorrer el HTML real (no solo .text) y capturar la profundidad de anidación de cada `<li>`,
reconstruyendo listas con sub-listas indentadas correctamente - requiere reescribir la
extracción de texto del scraper y volver a correr el scraping completo.

## Notas de comportamiento del sitio real (no son bugs nuestros)
El sitio real (flores.go.cr) es frágil: errores de WordPress intermitentes, páginas 404, un
link roto a IP directa, error de Composer/PHP (falta extensión "exif"), portal de actas sin
HTTPS. Cuando aparezca algo raro, verificar primero si es del sitio real antes de asumir bug.

**Actualización 2026-07-26**: además de frágil, el sitio parece estar en actualización ACTIVA
en este momento (no solo caídas intermitentes). Evidencia concreta: "Documentación" (Marco
Normativo) se modificó apenas 3 días antes de esta sesión y ya tiene contenido que no estaba en
nuestro `conocimiento.json` original (dos secciones nuevas completas). Si en las próximas
sesiones aparecen más diferencias entre el sitio real y lo scrapeado, verificar primero la fecha
de "modified_time" de la página (visible al hacer `web_fetch`) antes de asumir que es un bug del
scraper o del prototipo - puede ser simplemente que el contenido cambió después del scrape.

## Cuidado con volver a scrapear
Ya hubo una caída del sitio real que coincidió con una sesión larga de scraping. El scraper
tiene pausas de 1s entre páginas y reintentos limitados; evitar corridas de varias horas
seguidas si no es necesario, preferir usar conocimiento.json ya existente antes que re-scrapear.

## Mejora futura de arquitectura (si se reutiliza este mismo stack)
Detectado 2026-07-26 en "Documentación" (Marco Normativo): esa página real tiene ~28 ítems que
son TODOS links de texto a documentos de Google Drive (leyes, reglamentos, políticas, manuales),
y el scraper actual no captura ninguno. La causa: el scraper extrae el contenido de cada página
como un solo string de texto plano (`body.text` de Selenium), que descarta toda la estructura
HTML - incluidos los `<a>` sobre texto (solo se captura `href` de imágenes, vía
`BUSCAR_ENLACE_JS`, nunca de texto con hipervínculo).

Mismo síntoma de fondo que el caso de las banderas de partido en "Miembros del Concejo
Municipal": ahí se perdió la asociación fila-a-fila de una tabla real; acá se pierde la
asociación línea-a-link de una lista real. En ambos casos la causa raíz es la misma: extraer
texto plano tira la estructura HTML a la basura.

**Decisión tomada:** NO rediseñar el scraper ahora. Es un cambio de arquitectura real, no un
ajuste chico - requeriría (1) cambiar la extracción en `scraper.py` para recorrer el DOM en vez
de pedir solo `.text`, (2) cambiar el formato de `conocimiento.json` (de un string "contenido" a
algo estructurado con texto+links), (3) reescribir `formatearTexto`/`renderContenido` en
`index.html` para consumir esa nueva estructura, y (4) volver a scrapear - con el riesgo de que
páginas ya aprobadas hayan cambiado en el sitio real desde el último scrape (como pasó con esta
misma página, modificada hace apenas 3 días) y haya que re-revisarlas.

Por ahora, cada vez que aparezca este patrón (una página cuyo contenido real depende de que el
texto tenga links), se resuelve con hardcode puntual por nodo (mecanismo `listasEnlaces`, mismo
espíritu que `tablaTexto` para las tablas).

**Si en el futuro se arma un proyecto nuevo con este mismo stack (Selenium + Claude + scraping
de texto plano)**, vale la pena diseñar la extracción desde el inicio para que capture texto CON
su estructura (ej. una lista de fragmentos `{texto, enlace}` en vez de un string plano), en vez
de parchar esto después.

## Contexto del proyecto (agregado 2026-07-26)
Este es un proyecto académico: el usuario es tutor de un estudiante de secundaria (su sobrino),
quien hará una pasantía replicando este trabajo. El usuario está haciendo el trabajo completo
primero, y luego le va a dar una guía al estudiante para que lo replique. Es esperable que el
estudiante, al replicar, se encuentre con diferencias ("doesn't look the way it's supposed to")
- es parte normal de este tipo de trabajo con un sitio real que sigue cambiando.

Pendientes para más adelante (no ahora, mientras se termina el repaso nodo por nodo):
1. Una guía de replicación paso a paso para el estudiante.
2. Un borrador de informe final que el estudiante pueda completar.

Prioridad actual: concluir el repaso nodo por nodo lo más eficientemente posible (el usuario
quiere cerrar esto "ASAP").

## Plan de fondo (más allá de hoy)
El usuario quiere revisar TODO el árbol nodo por nodo (en progreso, ver arriba) y también
probarlo en celular (el responsive y el auto-cierre del menú YA se probaron y confirmaron
funcionando bien en celular real).
