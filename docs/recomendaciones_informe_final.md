# Recomendaciones para el informe final - Sitio Municipalidad de Flores

Este documento recopila observaciones sobre el sitio REAL (flores.go.cr) encontradas durante
la construcción del prototipo, que podrían mencionarse como recomendaciones de mejora en el
informe final — a diferencia de los arreglos técnicos que hicimos en nuestro propio prototipo.

## 1. Contenido de texto encerrado en imágenes (accesibilidad/SEO)
**Página:** Municipalidad → Información General → Nuestros Valores
(https://flores.go.cr/municipalidad/informacion-general/valores/)

Los "Valores Institucionales" (Honestidad, Liderazgo, Trabajo en equipo, etc.) están mostrados
como texto dentro de una imagen/gráfica de diseño, no como texto real (HTML).

**Por qué importa:**
- No es accesible para lectores de pantalla (personas con discapacidad visual no pueden
  acceder a esta información).
- No se puede seleccionar, copiar ni buscar (Ctrl+F) dentro de la página.
- No es indexable correctamente por buscadores como Google (peor SEO).

**Recomendación:** Convertir este contenido a texto HTML real, manteniendo el diseño visual
como elemento decorativo aparte si se desea, en vez de que el texto en sí sea parte de la imagen.

## 2. Mapa embebido de Waze poco funcional en escritorio
**Página:** Municipalidad → Información General → Ubicación
(https://flores.go.cr/municipalidad/informacion-general/ubicacion/)

La página muestra un mapa interactivo embebido de Waze. Es una app pensada principalmente para
uso en celular (navegación mientras se conduce); en una computadora de escritorio, el widget
embebido es más limitado y menos natural de usar (no tiene sentido "navegar" desde una PC fija).

**Recomendación:** Considerar un mapa embebido de Google Maps (más universal para escritorio y
celular por igual), o al menos ofrecer un link directo a Google Maps como alternativa junto al
widget de Waze, para quienes lo consulten desde una computadora.

## 3. Link mal puesto en un ítem de la lista de Reglamentos
**Página:** Municipalidad → Marco Normativo → Documentación
(https://flores.go.cr/municipalidad/marco-normativo/documentacion/)

En la lista de Reglamentos, el ítem "Reglamento de activos de la Municipalidad de Flores" tiene
el punto final de la oración convertido en un segundo hipervínculo separado, que apunta por error
a un PDF completamente distinto ("Reglamento para karaoke y similares", documento que además ya
tiene su propio ítem correcto y separado en la misma lista).

**Por qué importa:** alguien que haga clic justo en ese punto final terminará en un documento
equivocado, sin ninguna indicación visual de que el link no corresponde al título que acompaña.

**Recomendación:** Revisar el editor de esa entrada en el CMS y quitar el hipervínculo suelto del
punto final, dejando un único link correcto por ítem (el que ya apunta al reglamento de activos).

## 4. Falta un sistema real de "Pago en Línea" (consulta de deuda + pago con cédula)
**Página:** Contribuyente → Pago en línea → Calendario de pagos
(https://flores.go.cr/contribuyente/calendario-de-pagos/)

**Actualizado 2026-08-06 (a pedido de Gerardo, tutor):** hoy la sección "Pago en línea" del sitio
real solo muestra un calendario con las fechas en que vencen los tributos (cuándo hay que pagar),
pero NO permite que el ciudadano ingrese con su cédula, vea cuánto debe exactamente, y pague desde
ahí. Para eso, hoy en día el ciudadano tiene que ir presencialmente o pagar en el banco sin poder
consultar su estado de cuenta actualizado en línea primero.

**Por qué importa:** es una fricción evitable para el ciudadano (no sabe cuánto debe hasta que
llega a la ventanilla o al banco) y para la propia Municipalidad (más carga de atención presencial
y telefónica solo para consultas de saldo).

**Recomendación:** no hace falta construir un sistema desde cero. El Instituto de Fomento y
Asesoría Municipal (IFAM) ya ofrece una plataforma compartida — "Sistema de Consultas y Pagos
(Tributos Municipales)", en `comercio.ifam.go.cr/<municipalidad>` — que ya usan municipalidades
más pequeñas como San Ramón, Acosta y Río Cuarto: el ciudadano se identifica con su número de
cédula, ve el "Total Adeudado" desglosado por servicio y período, y paga con tarjeta de débito o
crédito (Visa/Mastercard) a través del Banco Nacional. Otras municipalidades (San Carlos, San
José, Aserrí, Coronado, Garabito) tienen soluciones similares propias o de otros proveedores. La
vía más rápida y de menor costo para Flores sería solicitar directamente a IFAM sumarse a ese
sistema compartido, en vez de desarrollar uno propio desde cero.

*Fuentes consultadas: comercio.ifam.go.cr/sanramon, aserri.go.cr/pago-en-linea, munigarabito.go.cr,
coromuni.go.cr, msj.go.cr/trampago, munisc.go.cr (consultado 2026-08-06).*

---

*Documento actualizado por última vez el 2026-08-06. El punto 4 se agregó a pedido explícito de
Gerardo (tutor) como parte de la investigación de "RAG externo" del chatbot — ver también la
entrada `conocimiento-externo://pago-en-linea-recomendacion` en `conocimiento.json`, donde el
chatbot tiene esta misma información disponible para responder preguntas de ciudadanos.*
