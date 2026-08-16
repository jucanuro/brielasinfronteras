# BRIEF DE DISENO — Sitio publico ONG Briela Sin Fronteras

Prerequisito: el admin ya esta terminado. Los modelos existen y funcionan.
Esta fase construye el sitio publico completo, conectado a la base de datos.

## Regla numero uno
CERO contenido quemado en plantillas. Cada texto, imagen, cifra, area, proyecto y
testimonio se lee de la base de datos via los modelos existentes. Si una seccion
no tiene datos, se oculta con elegancia (no deja hueco ni muestra placeholder feo).
Antes de escribir plantillas, revisa los modelos reales en src/ y usa sus campos
exactos. No inventes nombres de campo.

## Jerarquia de color (decision del cliente, no negociable)
El logo es un circulo amarillo con lemniscata azul. En el SITIO la jerarquia se
invierte respecto al logo:

--azul-bsf      #12369B   dominante: header, hero, botones primarios, titulares
--azul-noche    #081A45   profundidad: footer, overlay del video, secciones oscuras
--blanco        #FFFFFF   respiracion: fondo principal, texto sobre azul
--nieve         #F2F5FB   fondo alterno con tinte azul frio
--amarillo-bsf  #FCD434   acento quirurgico
--tinta         #0E1220   texto sobre fondo claro

REGLA DURA DEL AMARILLO: nunca supera el 5% de la superficie visible en pantalla.
Se permite en: subrayado del titular del hero, estado activo de navegacion, el
boton "Quiero donar", iconos de las cifras de impacto, borde inferior de card en
hover, y el trazo de la lemniscata. Prohibido como fondo de seccion, de card, de
footer o de boton primario. Si dudas, usa azul.

Ajusta los hex al logo real que esta en el repo o en SiteSettings.

## Ritmo de secciones
Alterna fondos para dar respiracion: blanco -> nieve -> blanco -> azul-noche ->
blanco. Nunca dos secciones oscuras seguidas. El footer en azul-noche cierra.

## Tipografia
- Display: Bricolage Grotesque, pesos 700/800, tracking cerrado, para titulares
- Cuerpo: Instrument Sans (respaldo Public Sans)
- Datos: Space Mono SOLO en cifras de impacto, fechas, numero de beneficiarios
Escala clara y deliberada: h1 muy grande, h2 grande, cuerpo comodo (17-18px).
Nada de tres tamanos indistinguibles. Carga las fuentes con font-display:swap y
preconnect; que no bloqueen el render.

## Elemento firma
La lemniscata del logo como hilo conductor. Trazo SVG continuo, azul sobre fondos
claros y amarillo sobre azul-noche, que:
- se dibuja al hacer scroll (stroke-dasharray animado) enlazando seccion a seccion
- enmarca el bloque de cifras de impacto
- aparece como microinteraccion sutil al pasar sobre las cards de proyecto
Es el UNICO lugar donde se gasta audacia. Todo lo demas: disciplinado y silencioso.
Si prefers-reduced-motion esta activo, el trazo se dibuja completo sin animacion.

## Secciones a construir

HEADER
Fijo, transparente sobre el hero, con fondo azul solido al hacer scroll (transicion
suave). Logo desde SiteSettings. Navegacion: Nosotros, Areas de trabajo, Proyectos,
Testimonios, Contacto. Boton "Quiero donar" en amarillo, unico elemento amarillo del
header. Menu movil a pantalla completa en azul-noche con Alpine.js.

HERO
Video a pantalla completa desde HomePage. Overlay: degradado de azul-noche al 75%
en la base a transparente arriba, para legibilidad del texto blanco.
Titular, subtitulo y hasta 2 botones desde BD. El titular lleva una palabra clave
subrayada con trazo amarillo dibujado a mano (SVG).
Requisitos tecnicos innegociables: poster AVIF/WebP como elemento LCP precargado;
video muted autoplay loop playsinline preload=none con IntersectionObserver;
WebM/VP9 + MP4/H.264; en movil y con reduced-motion solo el poster.
Meta: LCP < 2.5s y CLS < 0.1 en movil.

CIFRAS DE IMPACTO
Desde HomePage. Numeros en Space Mono, grandes, con animacion de conteo al entrar
en viewport. Etiquetas en mayusculas pequenas con tracking abierto. La lemniscata
enmarca el bloque. Fondo nieve.

CONOCENOS
Mision y vision en dos columnas asimetricas (no dos cajas iguales). Valores desde
BD como lista con iconos, no como grid de tarjetas genericas. Fondo blanco.

AREAS DE TRABAJO
Desde BD, con la imagen y el color_acento de cada area. Layout editorial: imagen
grande, nombre en display, descripcion corta, enlace a su pagina. Al hacer hover la
imagen se satura y aparece el enlace. Cada area lleva a /areas-de-trabajo/<slug>/.

PROYECTOS
Cards desde BD, elegantes: imagen destacada con relacion 4:3, etiqueta del area con
su color, titulo en display, ubicacion y numero de beneficiarios en mono, estado
como pildora. Hover: elevacion sutil + borde inferior amarillo + trazo de lemniscata.
Muestra los destacados en la home y enlaza a /proyectos/ con filtros por area y
estado. Grid responsive de 1 / 2 / 3 columnas.

TESTIMONIOS
Desde BD. Fondo azul-noche, texto blanco. Carrusel con Alpine.js, navegable con
teclado y con swipe en movil. Comillas grandes en amarillo. Foto circular, nombre en
display, rol en mono.

COMO QUIERES AYUDAR HOY
Las tres vias como tres bloques claramente distintos, no tres cards identicas:
"Quiero ser voluntario", "Quiero donar", "Colaborar como empresa".
Solo el bloque de donar usa amarillo. Cada uno abre su formulario correspondiente
(modal o pagina, lo que quede mejor). Los formularios ya existen en la app contacto:
conectalos, no los reescribas.

FOOTER
Azul-noche. Muy superior al actual: logo, frase corta, navegacion completa en
columnas, areas de trabajo enlazadas, datos legales (nombre legal, RUC, direccion),
correos por area, redes sociales desde SiteSettings, y suscripcion al boletin.
Linea final con copyright dinamico por ano.

## Calidad minima
- Movil primero. Correcto de 320px a 2560px.
- Contraste AA como minimo en todo texto. Ojo con amarillo sobre blanco: no se usa
  para texto, solo para elementos graficos.
- Navegacion completa con teclado, foco visible en azul o amarillo segun el fondo.
- prefers-reduced-motion respetado en todas las animaciones.
- Imagenes de Wagtail en WebP con srcset y loading=lazy salvo el poster del hero.
- Un solo h1 por pagina.

## Contenido para la demo
Antes de terminar, crea un comando de gestion "seed_demo" que cargue contenido real
del sitio actual (brielasinfronteras.org): mision, vision, los 6 valores, las 4
areas (educacion, salud, medio ambiente, ciencia y tecnologia), los 3 testimonios
de Lucero, Jacqueline y Angie, las cifras +300 personas / +25 voluntarios / 1 ano de
fundacion, y al menos 4 proyectos de ejemplo claramente marcados como tales.
El sitio debe verse completo y creible al levantarlo. Nunca lorem ipsum.

## Proceso obligatorio
1. Lee los modelos existentes y confirma los nombres de campo reales.
2. Escribe un plan de diseno corto: paleta final, escala tipografica, wireframe
   ASCII de la home, y como se aplica el elemento firma.
3. Critica ese plan: si alguna parte serviria igual para cualquier otra ONG,
   cambiala y explica que cambiaste y por que.
4. Recien entonces escribe codigo, siguiendo el plan revisado.
5. Al terminar, corre Lighthouse en movil y reporta los numeros por escrito.

## Prohibido
- Bootstrap, DaisyUI, Flowbite o cualquier libreria de componentes
- React o cualquier framework JS pesado (solo Alpine.js)
- Degradados morados, stock photos genericas, sombras difusas por todas partes
- Amarillo como fondo de seccion, card, footer o boton primario
- Texto quemado en plantillas
- Inventar contenido de la ONG

## Orden de entrega
Primero el plan de diseno y su critica, para que lo apruebe.
Luego header + footer + plantilla maestra + tokens.
Luego la home completa.
Luego las paginas internas.
Detente despues del plan de diseno y espera mi visto bueno.
