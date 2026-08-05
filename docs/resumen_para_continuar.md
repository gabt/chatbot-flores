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
