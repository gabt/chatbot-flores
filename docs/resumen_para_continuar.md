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

## 🚦 PRÓXIMO PASO INMEDIATO (leer esto primero en una sesión nueva)
El repaso nodo por nodo del sitio real (Municipalidad, Contribuyente, Noticias y Comunicados,
Contáctenos) quedó 100% cerrado el 2026-08-05 (día 3 de la pasantía). El plan de trabajo de 7
jornadas (día 4 al día 10) sigue detallado con objetivo/alcance técnico/metodología/entregable por
día en `docs/Tareas-Pendientes.docx` **y sigue pendiente de arrancar** (no se tocó hoy).

**Instrucción de Gerardo (PRIORIDAD) — ✅ investigación y primera carga resueltas el 2026-08-06,
ver sección "Sesión 2026-08-06" más abajo para el detalle completo.** Texto original de la
instrucción (se deja tal cual para registro): *"Investigar como el chatbot puede mezclar
información externa para responder, hacer RAG, añadiendo a conocimiento.jason. RANKINGS de la
muni, comparaciónes entre municipalidades (flores y belen por ejemplo) donde botan la basura,
cuantas toneladas de basura se generan, cuales fuentes de agua existen, están protegidas o no,
etc. el barrio santísima trinidad en x dirección que tipo de zonificación tiene (industrial,
comercial, vivienda, etc) que el chatbot pueda responder preguntas externas a la información de
la web pero que todo se encuentre en conocimiento.jason. Preguntarle a las personas que que
preguntas le harían a la municipalidad, tipo que cuanto deben pagar en x cosa. Pago en Línea
(investigar y tratar de resolverlo, recomendarle a la muni que instalen ese sistema de que cada
ciudadano pueda tener su usuario, tal vez con la cédula y que ahi aparezca lo que debe y poder
pagar desde ahi)"*

**Siguiente sesión: retomar el plan de Día 4** (Planos por APC, Salarios Base 2021, los 6 ítems
de `mapa_organizado.md`) — quedó pausado hoy para atender la prioridad de Gerardo primero, a
pedido explícito de Jeiron. Pendiente puntual que quedó abierto de la prioridad de Gerardo:
confirmar la ubicación real de "barrio Santísima Trinidad" (ver sección de hoy) y completar la
lista de preguntas ciudadanas con lo que Jeiron recoja al preguntarle a personas reales hoy.

Resumen rápido de cada día:

- **Día 4** — Cerrar "Planos por APC" (sin implementar todavía, sin decisión tomada), verificar
  "Salarios Base 2021" (marcado como no probado), y resolver los 6 ítems ambiguos de
  `mapa_organizado.md` ("Otros ítems del PDF original sin reconciliar todavía").
- **Día 5** — QA funcional completo de Municipalidad + Contribuyente (~45 nodos), en 2
  navegadores, comparado contra el sitio real.
- **Día 6** — QA funcional completo de Noticias y Comunicados + Contáctenos, más integridad
  referencial del árbol (ids huérfanos, navegación interna) y pruebas del buscador del directorio.
- **Día 7** — Responsive (3 anchos de viewport) + accesibilidad (alt text, contraste de color,
  navegación por teclado).
- **Día 8** — Auditoría de enlaces externos (Dropbox, Drive, CFIA, Contraloría) y contraste de
  los ~166 URLs de `conocimiento.json` contra el estado actual del sitio real.
- **Día 9** — README técnico de arquitectura, limpieza/comentado de código, aplicar la decisión
  de Gerardo sobre `index_prueba.html` (fusionar con el real o archivar) si ya respondió.
- **Día 10** — Matriz de pruebas formal (tabla con los 80+ nodos del árbol) + regresión final de
  extremo a extremo + cierre documental.

**Nota de alcance:** por pedido explícito de Jeiron, el "informe final" de la pasantía queda
fuera de este plan de 7 días - no forma parte del trabajo técnico programado día a día.

**Sobre `index_prueba.html`:** es un rediseño visual experimental completo (hero con foto, menú
de pastillas en vez de sidebar, paleta cálida, escudo real, sin emojis) que vive en un archivo
aparte y está pendiente de aprobación de Gerardo Brenes Trejos (tutor) vía GitHub Pages. Todo
contenido nuevo (Noticias y Comunicados, Directorio ampliado) se replica en ambos archivos a la
vez para no duplicar trabajo si se aprueba, pero los cambios puramente visuales/de navegación
siguen existiendo solo ahí hasta que haya una decisión.

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

### Municipalidad → Transparencia ✅ COMPLETO (⚠️ ARQUITECTURA CAMBIÓ 2026-08-05, ver más abajo)
⚠️ **DESACTUALIZADO** - lo descrito abajo (nodo top-level "Transparencia" con ~15 hijos mapeados
   uno por uno) fue la versión de sesiones anteriores. **El 2026-08-05 se revirtió por completo**
   a pedido del usuario: ya NO existe el nodo top-level "Transparencia" con submenú. Ahora es
   UN SOLO nodo "Transparencia" dentro del dropdown de Municipalidad, tipo `externo`, que apunta
   a `https://flores.go.cr/transparencia_accesibilidad/`. Ver sección "Sesión 2026-08-05" más
   abajo para el detalle completo y el motivo de la decisión. Se deja el texto original acá tal
   cual (tachado en la práctica) como registro histórico de lo que se probó y no se usó:
   ~~Todos los hijos externos (Acceso a la Información, Información Institucional, Rendición de
   cuentas, Participación ciudadana, Datos Abiertos, Red de Transparencia) muestran correctamente
   "Abrir en el sitio real". Los 4 hijos que reutilizan contenido real (Servicios y Procesos
   Institucionales, Presupuesto Municipal, Toma de Decisiones, Planes y Cumplimiento) muestran
   contenido real (Excel/PDF según corresponda).~~

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

### Estado de "Contribuyente" — 🎉 100% TERMINADO (2026-08-05)
Artesanos (Plataforma/Solicitud), Servicios completo (Formularios, Trámites, Mapa Catastral,
Plan Regulador de Flores, Plan Cantonal de Desarrollo Humano Local, Recolección de desechos),
Pago en línea (Calendario de pagos), Amnistía Tributaria, y **Preguntas Frecuentes** (cerrado en
esta sesión, ver sección 7 más abajo).

**PAUSADO 2026-07-26** (nota de sesión anterior, ya resuelto en la sesión del 2026-08-05): el
usuario había notado inconsistencias en el sitio real que sugerían actualización activa. Se
retomó normalmente.

### Estado de "Noticias y Comunicados" — 🎉 TERMINADO (2026-08-05)
Estaba roto (`tipo: 'especial-noticias'` sin implementar). Cerrado con el mismo patrón de
"Gestión Ambiental" (`especial-blog`), 6 categorías, 21 posts curados y confirmados contra el
sitio real. Ver sección 8 más abajo.

### Estado de "Contáctenos" — 🎉 TERMINADO (2026-08-05)
El formulario de contacto y los datos básicos (dirección/teléfono/correo/horario) ya estaban
bien. El Directorio Institucional tenía un gap grande: solo mostraba 8 de ~53 contactos reales.
Ampliado al directorio completo. Ver sección 9 más abajo.

## 🎉 REPASO NODO POR NODO DEL SITIO REAL — COMPLETO (2026-08-05)
Con el cierre de Contáctenos, las 4 secciones del menú principal (Municipalidad, Contribuyente,
Noticias y Comunicados, Contáctenos) quedan revisadas y confirmadas contra el sitio real.

## Sesión 2026-08-05: PDFs propios, cierre de Contribuyente, Transparencia simplificada
Resumen de lo trabajado hoy (se omiten a propósito 3 ítems que Jeiron pidió excluir por estar
ya registrados en otro lado: el arreglo del link de "Solicitud de Artesanos", el cierre del
"Plan Regulador de Flores", y la revisión de "Formularios" y "Trámites").

### 1. Tres PDFs propios reemplazan links frágiles a Dropbox
Jeiron subió 3 PDFs reales (`ZONIFICAC-ACTUL-PRF.pdf`, el de Amnistía Tributaria, y el Plan de
Desarrollo Humano Local) y ahora viven en la carpeta `pdfs/` del repo, en vez de depender de
links externos a Dropbox:
- `pdfs/mapa-zonificacion.pdf` → nodo "Mapa de Zonificación" (antes `roto`, ahora `descarga`).
- `pdfs/amnistia-tributaria.pdf` → nodo "Amnistía Tributaria".
- `pdfs/plan-desarrollo-humano-local.pdf` → nodo "Plan Cantonal de Desarrollo Humano Local".

⚠️ Nota de troubleshooting para la próxima vez: al principio dieron 404 en GitHub Pages porque
los PDFs se habían subido al repo con sus nombres de archivo originales, no con los nombres
exactos que espera el código (`mapa-zonificacion.pdf`, etc.). Se resolvió con `Rename-Item` +
`git add` (git lo detecta como "renamed", no hace falta re-subirlos de cero).

### 2. "Plan de Desarrollo Urbano Cantonal" resuelto (ya no está `roto`)
Investigado y confirmado por Jeiron: en el sitio real, ese link apunta al MISMO PDF que "Plan de
Desarrollo Humano Local" (el sitio real simplemente le pone una etiqueta distinta al mismo
archivo de Dropbox). Se conectó al mismo `pdfs/plan-desarrollo-humano-local.pdf` que ya
teníamos - no hizo falta ningún PDF nuevo.

### 3. Botón "Ver en el sitio real" ahora en TODA la web
Antes solo aparecía en los tipos `contenido`, `externo` y `descarga`, y en Miembros del Concejo
y Blog. Se agregó donde faltaba:
- Alcaldía Municipal, Contáctenos, Directorio Institucional (funciones bespoke que no lo tenían).
- Tipo `roto`: ahora acepta un campo opcional `hrefReal` - si la página SÍ funciona en el sitio
  real pero todavía no la tenemos incorporada al prototipo, muestra igual el botón (con aviso
  claro de que está pendiente de incorporar, no que está rota). Activado para "Preguntas
  Frecuentes" (`hrefReal: 'https://flores.go.cr/contribuyente/preguntas/'`).

### 4. Corregido el mensaje engañoso de "esto es contenido externo"
Jeiron notó (con capturas) que el mensaje de las páginas tipo `externo` decía básicamente "esto
vive fuera del sitio real", cuando en realidad son páginas del propio `flores.go.cr` que
simplemente no tenemos incorporadas como contenido embebido - no son ajenas al sitio real.

**Arreglo (en la función `renderExterno`, no nodo por nodo - aplica automático a toda la web):**
ahora detecta el dominio del link. Si es `flores.go.cr` o `*.flores.go.cr` (incluye
`portalmuni.flores.go.cr`) dice *"Esta información SÍ es parte del sitio real de la Municipalidad
de Flores - vive en otra sección de flores.go.cr que todavía no incorporamos dentro de este
prototipo"* con botón "Ver esta sección en flores.go.cr ↗". Si es un dominio de verdad ajeno
(CFIA, Google Maps, Contraloría) mantiene el mensaje de sistema externo real, con botón "Abrir
el sistema externo ↗". Este único cambio de función corrige automáticamente el mensaje en las
~9 secciones que usan tipo `externo` en toda la web (Ubicación, Plataforma Artesanos, Catastro/
Planificación/Patentes bajo Formularios, APC Requisitos, Mapa Catastral, Transparencia, etc.).

### 5. Transparencia: se probó embeber contenido real, pero se revirtió a un solo link
Se intentó convertir varios hijos de "Transparencia" (Acceso a la Información, Rendición de
cuentas, Presupuesto público, etc.) de `externo` a `contenido` embebido, usando texto ya
scrapeado en `conocimiento.json`. **Jeiron decidió revertir todo esto** y simplificar: eliminado
por completo el nodo top-level "Transparencia" con su submenú de ~15 hijos. Ahora queda UN SOLO
nodo "Transparencia", dentro del dropdown de Municipalidad, tipo `externo`, apuntando a
`https://flores.go.cr/transparencia_accesibilidad/` (URL confirmada por Jeiron, distinta a la
que se venía usando antes). Si en el futuro se quiere retomar la idea de contenido embebido para
Transparencia, el texto ya scrapeado para varias de esas páginas existe en `conocimiento.json`
bajo las URLs `transparencia/*.php` - no hay que volver a scrapear, solo reconectar los nodos.

### 6. Infraestructura nueva agregada (queda disponible aunque hoy no se usa activamente)
Se agregó al código un mecanismo de **navegación interna** (`tipo: 'interno'`, propiedad
`destino: '<id de otro nodo>'`, función `irANodo()`): permite que un nodo, en vez de redirigir
afuera del prototipo, salte directamente a otro nodo que ya existe en el propio árbol
(expandiendo el sidebar automáticamente hasta ahí). Se usó primero para el atajo de Transparencia
y después se revirtió junto con el resto de esa sección (ver punto 5), pero el mecanismo en sí
quedó en el código, reutilizable para casos similares en el futuro (ej. si otro nodo resulta ser
un "atajo" a una sección que ya existe en otra parte del árbol).

### 7. Preguntas Frecuentes cerrado — Contribuyente queda 100% (2026-08-05, sesión de cierre)
La página índice `/contribuyente/preguntas/` en el sitio real SÍ funciona (no está `roto` como
se pensaba) y lista las 6 categorías con botones "Más información". Se confirmó vía `web_fetch`
que 4 de los 6 links reales de esas categorías NO usan las URLs `/contribuyente/preguntas/<slug>/`
que se habían anotado antes, sino un subdominio de contenido antiguo distinto:
`flores.go.cr/rfw/Frecuentes/<Nombre>.html`. Las URLs reales confirmadas, botón por botón:
- Bienes Inmuebles → `rfw/Frecuentes/bienes.html` ✅ (ya estaba en `conocimiento.json`, contenido completo)
- Acueducto → `rfw/Frecuentes/Acueducto.html` ✅ (ya estaba en `conocimiento.json`, contenido completo)
- Catastro → `rfw/Frecuentes/catastro.html` ✅ (ya estaba en `conocimiento.json`, contenido completo)
- Cobros → `/contribuyente/cobros` ✅ (ya estaba en `conocimiento.json`, contenido completo)
- Cementerio Municipal → el botón de la página real SÍ apunta a `/contribuyente/preguntas/...cementerio-municipal/`,
  pero esa página está vacía en el sitio real (solo bookmarks de editor, sin texto) - dentro de
  ella hay un link secundario a `rfw/Frecuentes/cementerio.html` que SÍ tiene el contenido real
  completo (adjudicación/traspaso/eliminación de derecho). No estaba en `conocimiento.json` -
  **agregado ahora** vía `web_fetch` al sitio real.
- Patentes Municipales → mismo patrón: el botón real apunta a `/contribuyente/preguntas/patentes/`
  (vacía en el sitio real), que a su vez señala a `rfw/Frecuentes/patentes.html`, que sí tiene el
  contenido real completo (requisitos de actividades comerciales, traspaso, traslado, espectáculos
  públicos). No estaba en `conocimiento.json` - **agregado ahora** vía `web_fetch`.

**Cambios aplicados:** 2 entradas nuevas en `conocimiento.json` (`rfw/Frecuentes/cementerio.html`
y `rfw/Frecuentes/patentes.html`). El nodo `preguntas-frecuentes` en `index.html` pasó de
`tipo: 'roto'` a `tipo: 'contenido'` (usa el texto real ya scrapeado de `/contribuyente/preguntas`,
que es el índice con las 6 tarjetas) con 6 hijos tipo `contenido`, mismo patrón que "Formularios".
Verificado localmente con Playwright (servidor local + `conocimiento.json` de prueba): las 6
categorías cargan su contenido real correctamente al hacer clic.

**Pendiente de decisión con Jeiron:** el "Índice de Preguntas Frecuentes" real (`/contribuyente/preguntas/`)
solo tiene pregunta-teaser + botón para 4 de las 6 categorías (Cementerio y Patentes muestran la
tarjeta pero su página de destino real está vacía, como se explicó arriba) - no es un bug nuestro,
es así en el sitio real. No requiere acción, es solo para tenerlo presente si Jeiron pregunta por
qué esas dos páginas del sitio real "no tienen nada" cuando las compare en `flores.go.cr` directo.

### 8. Noticias y Comunicados cerrado (2026-08-05, sesión de cierre)
El nodo `noticias` tenía `tipo: 'especial-noticias'`, un tipo que NUNCA se implementó en el
switch de `mostrarNodo()` (no existe `case 'especial-noticias'`), así que caía al `default:
renderGrupo(nodo, pane)` - y como el nodo no tenía `children`, mostraba únicamente "Elegí una
opción del menú de la izquierda para ver su contenido" sin ninguna opción real que elegir. Es
decir, la sección estaba rota (no solo pendiente de pulir).

Se resolvió reutilizando el mismo mecanismo ya probado en "Gestión Ambiental" (`tipo:
'especial-blog'` + `renderBlog`, posts curados a mano). `noticias` pasó a ser un nodo padre puro
con 6 hijos, uno por categoría real del blog, confirmadas y actualizadas directo contra
`flores.go.cr` vía `web_fetch` el mismo día: Sin categoría (3 posts), Cantón de Flores (4),
Municipalidad (7, categoría agregadora - ver nota abajo), Comunicados (3), Gestión Ambiental (3,
mismos posts que "Municipalidad > Gestión Ambiental", repetidos porque el sitio real también la
expone desde acá), Leyes (1). Detalle completo en `mapa_organizado.md`.

**Nota sobre "Municipalidad" como categoría:** en el sitio real, dos posts ("III Congreso
Iberoamericano de Áreas Metropolitanas" y "La Oficina de Promoción Humana Cantonal...") están
etiquetados ÚNICAMENTE con la categoría "Municipalidad" - no aparecen en ninguna otra categoría.
El resto de los posts que muestra esa categoría en el sitio real están duplicados de Comunicados
y Gestión Ambiental (el sitio real permite que un post tenga más de una categoría a la vez). Se
mantuvo tal cual el comportamiento real y se dejó una `nota` visible en el nodo explicándolo, en
vez de "limpiar" la duplicación y arriesgarnos a que no coincida con lo que Jeiron ve al comparar
contra `flores.go.cr` directo.

**Verificado con Playwright** (servidor local + `conocimiento.json` de prueba): las 6 categorías
cargan sus posts correctamente, ARBOL parsea sin errores, 21 posts en total repartidos en 6
categorías.

**Aplicado en paralelo a `index_prueba.html`** (mismo contenido/estructura, adaptado a su
render de pastillas en vez de sidebar) - a pedido de Jeiron, para que si Gerardo aprueba el
rediseño visual no haya que repetir este trabajo de contenido ahí.

### 9. Contáctenos cerrado - Directorio Institucional ampliado (2026-08-05, sesión de cierre)
Al revisar "Contáctenos" nodo por nodo (la única sección del menú principal que faltaba pasar
por el repaso formal), se confirmó lo siguiente contra el sitio real vía `web_fetch`:

- **Página "Contáctenos" (`renderContacto`)**: los datos hardcodeados (dirección, teléfono
  2265-7109, correo info@flores.go.cr, horario lunes a viernes 7am-3pm) ya estaban correctos -
  confirmados contra el footer del sitio real y contra `/municipalidad/informacion-general`
  (que es de donde sale el horario). La página real en sí es solo un formulario de contacto
  (Nombre/Correo/Mensaje), consistente con lo que ya decía la nota del prototipo. Sin cambios.

- **Directorio Institucional (`renderDirectorio`) - GAP GRANDE encontrado y corregido**: el
  prototipo solo mostraba 8 contactos hardcodeados. El directorio real
  (`/contactenos/directorio/`) tiene **53 contactos con cargo/nombre/extensión/correo**, más
  **7 líneas directas adicionales** (fax, WhatsApp de Comunicación, línea general del Concejo,
  líneas directas de Cementerio/Policía/Gestión Comunal/Inspecciones Constructivas) que no
  siguen el mismo formato de fila y se separaron en una segunda lista "Otros contactos y líneas
  directas". Se reconstruyó completo desde el HTML real (confirmado contra `conocimiento.json`,
  que ya tenía el directorio scrapeado completo pero nunca se conectó al nodo - mismo patrón de
  "dato ya capturado pero no conectado" que otros casos documentados en sesiones anteriores).
  Se agregó también un buscador simple (`#directorio-buscar`, filtra por texto en cualquier
  columna) porque 53 filas es demasiado para escanear a simple vista.

  **Nota de calidad de datos (no es un bug nuestro):** dos filas del directorio real tienen el
  correo desalineado del nombre de esa fila (Contabilidad/Andrea Arroyo muestra el correo de
  "lloban", y Proveeduría/Laura Loban muestra el correo de "vbarrantes") - así aparece tal cual
  en `flores.go.cr`. Se dejó igual (no se "corrigió" adivinando el correo correcto) y se agregó
  una nota visible en el prototipo explicándolo, para que no se confunda con un error nuestro.

**Verificado con Playwright**: 53 filas cargan en la tabla, el buscador filtra correctamente
(probado con "Alcaldía" → 3 resultados: Alcaldía, Vicealcaldía y cualquier otra fila que
contenga el texto), la página de Contáctenos sigue mostrando los datos correctos.

**Aplicado en paralelo a `index_prueba.html`**, mismo criterio que el punto anterior.

Con este cierre, las 4 secciones del menú principal del sitio real (Municipalidad,
Contribuyente, Noticias y Comunicados, Contáctenos) quedan 100% revisadas nodo por nodo.

### Pendiente para la próxima sesión
1. **Detalles estéticos solicitados por Jeiron pero NO implementados todavía en el `index.html`
   real**: quitar emojis del sitio (empezando por el emoji al lado de "Municipalidad de Flores"
   en el encabezado, que se reemplazaría por el escudo oficial del cantón), y cambiar la paleta
   de colores (hoy predominan los azules) por tonos que combinen con "Flores" y el cantón:
   marrones, amarillos, verdes, algo de rosa, celeste cielo, blanco. **Esto SÍ se implementó,
   pero solo en el prototipo experimental `index_prueba.html`** (rediseño de navegación con
   pastillas en vez de sidebar, pendiente de que Gerardo lo revise y apruebe antes de tocar el
   `index.html` real) - ver contexto aparte, no documentado en detalle acá a pedido de Jeiron.

## Sesión 2026-08-06: Prioridad de Gerardo — RAG con información externa

A pedido explícito de Jeiron, hoy se atendió PRIMERO la instrucción de Gerardo (ver texto completo
en "PRÓXIMO PASO INMEDIATO" arriba) antes que el plan técnico de Día 4, que queda pendiente para
la próxima sesión.

### 1. Investigación de información externa (rankings, residuos, agua, zonificación, pago en línea)
Se investigó cada punto pedido por Gerardo vía búsqueda web. Resultado honesto: parte de la
información SÍ se encontró con fuente confiable, y parte NO está disponible públicamente (se deja
así documentado, sin inventar cifras):

- **Rankings municipales**: el Índice de Gestión de Servicios Municipales (IGSM) de la Contraloría
  General de la República evaluó las 82 municipalidades en 2023 - ninguna alcanzó nivel "avanzado"
  y Belén se destacó puntualmente en servicios sociales, pero **no se encontró la calificación
  exacta de Flores** en fuentes públicas indexadas (se documentó cómo pedirla directo a la CGR:
  igsm@cgr.go.cr, 2501-8715/8482).
- **Basura Flores vs Belén**: según el informe "Indicadores Cantonales de Gestión Integral de
  Residuos 2023-2024" (IFAM + Ministerio de Salud), Flores genera ~0.3 kg de residuos por persona
  por día - una de las cifras MÁS BAJAS del país (entre los 10 cantones con menor generación per
  cápita). **No se encontraron cifras de Belén** en ese mismo informe, ni el total de toneladas
  mensuales/anuales de ninguno de los dos cantones, ni el nombre del relleno sanitario de destino.
- **Fuentes de agua**: se confirmó que Flores administra SU PROPIO acueducto municipal (a
  diferencia de otros cantones de Heredia que dependen de ESPH o AyA). **No se encontró** el
  listado específico de nacientes/pozos ni un mapa público de áreas de protección - sí se confirmó
  que existen "zonas de protección de pozo" relevantes para trámites de construcción (mencionadas
  en los formularios reales), aunque sin listado público.
- **Zonificación de "barrio Santísima Trinidad"**: se revisó el PDF real
  `pdfs/mapa-zonificacion.pdf` (Mapa de Zonificación Actualizada del Plan Regulador de Flores, al
  18 de mayo 2018) - es una imagen a color sin etiquetas de texto de barrios, así que no se puede
  buscar "Trinidad" directamente ahí. Al investigar la ubicación del barrio, **surgió una
  contradicción sin resolver**: una fuente (Moovit) lo asocia con Flores, pero otra (Waze) ubica un
  barrio con el mismo nombre en San Josecito, San Rafael de Heredia (cantón vecino, NO Flores).
  ⚠️ **Pendiente: Jeiron debe confirmar la ubicación real de este barrio** (dirección o punto de
  referencia) para poder darle la zonificación exacta usando el Mapa Catastral del Cantón (SIG) en
  una próxima sesión.
- **Pago en línea**: se encontró que IFAM ya ofrece una plataforma compartida ("Sistema de
  Consultas y Pagos de Tributos Municipales", `comercio.ifam.go.cr/<municipalidad>`) que usan
  municipalidades pequeñas como San Ramón, Acosta y Río Cuarto - login por cédula, ver deuda total
  desglosada, pagar con tarjeta vía Banco Nacional. Se agregó como recomendación concreta (ver
  punto 3 abajo).

### 2. Carga a `conocimiento.json` (RAG)
Se agregaron **5 entradas nuevas** a `conocimiento.json` (168 → 173 entradas), con `url` sintética
(prefijo `conocimiento-externo://...`, no colisiona con ningún fragmento real usado por
`buscarPagina()` en `index.html`/`index_prueba.html`, así que no afecta la navegación en árbol -
solo alimenta el contexto del chatbot vía `construir_contexto()` en `app.py`). Cada entrada incluye
sus fuentes y, cuando el dato no se pudo confirmar, una instrucción explícita para que el chatbot
lo admita en vez de inventar una respuesta. Marcadas con `"fuente_tipo": "externo_rag_manual"`
para distinguirlas de las páginas scrapeadas.

⚠️ **Cuidado importante:** `scraper.py` SOBREESCRIBE `conocimiento.json` por completo en cada
corrida (`json.dump` sin merge). Si se vuelve a correr el scraper completo, estas 5 entradas RAG
se PERDERÍAN y habría que volver a agregarlas a mano (o mover esta lógica a un archivo aparte que
se combine en `app.py` al arrancar - posible mejora futura, no implementada hoy para respetar el
pedido literal de Gerardo de que "todo se encuentre en conocimiento.json").

### 3. `recomendaciones_informe_final.md` actualizado
Se agregó el punto 4 (Pago en Línea) con la recomendación concreta de sumarse a la plataforma de
IFAM en vez de desarrollar un sistema propio desde cero, con fuentes. El documento ya no está tan
desactualizado como antes de hoy.

### 4. Lista de preguntas ciudadanas
Como Jeiron va a hacer la encuesta él mismo hoy ("preguntarle a las personas qué preguntas le
harían a la municipalidad"), se le entregó un borrador de 21 preguntas típicas (impuestos,
patentes, catastro, acueducto, basura, pagos, trámites, concejo) en
`docs/preguntas_ciudadanas_borrador.md`, para usar como punto de partida y ajustar con lo que la
gente realmente responda.

### 5. Sin cambios en index.html / index_prueba.html
Todo el trabajo de hoy fue en `conocimiento.json` (datos del chatbot) y documentación - no hubo
cambios de código ni de contenido visible en el árbol de navegación, así que no aplicó la regla de
"replicar todo cambio en ambos archivos". Ambos siguen idénticos entre sí en lo que ya estaba.

### 6. CORRECCIÓN DE ALCANCE (mismo día, más tarde): Jeiron aclaró que el pedido de Gerardo no era
### solo Flores-vs-Belén ni solo el barrio Trinidad - esos eran EJEMPLOS, no el alcance completo
El pedido real es que el chatbot pueda responder sobre CUALQUIER municipalidad del país y
CUALQUIER barrio, no solo los casos investigados a mano en el punto 1-2. Esto llevó a repensar la
arquitectura completa (ver puntos 7 y 8).

### 7. ¿`conocimiento.json` es RAG? No, no lo era hasta hoy
Se detectó que `construir_contexto()` en `app.py` armaba UN bloque fijo con los 173 documentos
completos (recortados a 2000 caracteres cada uno) UNA sola vez al arrancar el servidor, y ese
mismo bloque completo (~51,000 tokens) se mandaba en CADA pregunta del chatbot, sin importar el
tema. Eso es "context stuffing", no RAG real (RAG = buscar primero qué es relevante a la pregunta
puntual, y mandar solo eso). Esto ya costaba dinero real ANTES de tocar nada hoy: ~$0.10 en tokens
de contexto por cada mensaje (precio Sonnet 5 a agosto 2026, $2/MTok input), sin contar que
`historial` se reenvía completo en cada turno.

### 8. `app.py` reescrito: RAG real por palabras clave + búsqueda web en vivo
Se reescribió `app.py` (probado localmente: importa bien, `buscar_documentos_relevantes()` da
resultados sensatos, y una llamada de prueba a la API con key inválida confirma que el payload
-incluyendo el bloque `tools` de búsqueda web- pasa la validación del servidor, solo falla en
autenticación como se esperaba):

- **Retrieval por palabras clave** (`buscar_documentos_relevantes()`, sin librerías nuevas):
  normaliza (minúsculas, sin tildes) la pregunta y el contenido de cada documento, tokeniza
  quitando palabras vacías, puntúa cada documento por coincidencias (la URL pesa 3x porque suele
  traer el tema en el slug), y devuelve los 6 documentos más relevantes. Prueba real: la pregunta
  "cuánto cuesta una patente comercial" da un contexto de ~2,900 tokens en vez de ~51,000 (94%
  menos) - y ese ahorro CRECE con cada entrada nueva que se agregue a `conocimiento.json`, porque
  ya no todo se manda siempre.
- **Búsqueda web en vivo** (`tools=[{"type": "web_search_20250305", ...}]` en la llamada a la API
  de Claude): para preguntas que el contenido local no cubre (comparación con OTRA municipalidad,
  zonificación de un barrio no investigado, rankings nacionales, etc.), el chatbot puede buscar en
  internet en el momento, en vez de depender de que alguien haya escrito esa respuesta a mano de
  antemano. Tope de 3 búsquedas por pregunta (`max_uses: 3`) para controlar el costo ($0.01 por
  búsqueda). Ubicación aproximada seteada a Heredia, CR, para sesgar los resultados a Costa Rica.
  Las respuestas que usan búsqueda web ahora agregan automáticamente un bloque "Fuentes
  consultadas:" con los links citados.
- El endpoint `/chat` ahora también devuelve `"fuentes_locales"` (qué páginas de `conocimiento.json`
  se usaron) en la respuesta JSON - el frontend no lo necesita, pero sirve para depurar/demostrar
  que el RAG está funcionando cuando le muestren esto a Gerardo.
- `/paginas` y `/imagenes/<seccion>` quedaron sin cambios (los sigue usando el árbol de navegación
  de `index.html`/`index_prueba.html`, no dependen de este cambio).

⚠️ **No se pudo probar el endpoint `/chat` completo end-to-end** (necesita una API key real de
Anthropic, que no está en este entorno). Jeiron debe probarlo localmente (`python app.py` con su
`.env`) o en Render antes de darlo por cerrado - especialmente confirmar que la búsqueda web
efectivamente se dispara para preguntas externas.

⚠️ **Hallazgo colateral, útil para el QA de Día 5/6**: la página real
`recoleccion-de-desechos` en `conocimiento.json` tiene solo 35 caracteres de contenido scrapeado
("Recolección de desechos y reciclaje", nada más) - por eso el RAG no encuentra nada útil para
preguntas tipo "qué día pasa el camión de la basura". No es un bug del RAG, es que esa página real
no tiene ese texto capturado (puede estar en una imagen, o simplemente no estar publicado en el
sitio real). Vale la pena revisarlo cuando toque el QA de Contribuyente.

⚠️ **Nota de arquitectura para más adelante**: el retrieval de hoy es por palabras clave (rápido,
gratis, sin dependencias) - funciona bien para este tamaño de corpus (173 documentos) pero tiene
límites (ej. sinónimos: si alguien pregunta "impuesto de la casa" y el documento dice "bienes
inmuebles", puede no matchear). Si en el futuro hace falta mejor precisión, el siguiente paso
sería retrieval semántico con embeddings (más preciso con paráfrasis, pero agrega costo y una
dependencia nueva) - no fue necesario hoy.

### 9. INCIDENTE 2026-08-06 (mismo día, después del primer push): el chat quedó CAÍDO en producción
Jeiron hizo `git push` del `app.py` nuevo y Render lo desplegó, pero el chat dejó de responder por
completo en `index.html` Y `index_prueba.html` - hasta preguntas básicas como "quién es el
alcalde" (que funcionaban antes de hoy). Diagnóstico hecho en conjunto con Jeiron desde su
PowerShell (`Invoke-RestMethod` con `try/catch` leyendo `$_.Exception.Response` para sacar el
cuerpo del error, porque PowerShell esconde el body en errores HTTP por defecto):

```
{"error":"Error al consultar la API de Claude: Error code: 400 - {'type': 'error', 'error':
{'type': 'invalid_request_error', 'message': 'tools.0.web_search_20250305: Country code CR is
not supported.'}}"}
```

**Causa:** se había agregado `user_location: {..., "country": "CR"}` a la herramienta de búsqueda
web para sesgar resultados a Costa Rica, pero la API no soporta ese código de país - y como la
herramienta de búsqueda viaja en TODOS los mensajes (no solo los externos), esto tumbaba el 100%
de las preguntas, no solo las que necesitaban buscar. **Arreglo:** se quitó el bloque
`user_location` completo de `app.py` (quedó documentado con un comentario en el código explicando
por qué). Verificado localmente de la misma forma que antes (llamada con API key inválida): volvió
a dar 401 (autenticación) en vez de 400 (formato inválido), confirmando que el payload ya es
válido. Pendiente: Jeiron vuelve a hacer `git add`/`commit`/`push` de este `app.py` corregido y
prueba de nuevo con el mismo `Invoke-RestMethod` antes de dar por cerrado el tema.

**Lección para la próxima vez que se toque `app.py`:** antes de pedirle a Jeiron que haga push,
probar TODOS los parámetros nuevos (no solo la forma general del payload) contra la documentación
oficial o con más cuidado - el error de "country CR no soportado" se pudo haber evitado
verificando la lista de países soportados antes, en vez de asumir que cualquier código ISO de
2 letras funciona. Si en el futuro se quiere volver a sesgar la búsqueda a Costa Rica, investigar
primero qué códigos de país acepta `user_location` antes de agregarlo de nuevo.

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
