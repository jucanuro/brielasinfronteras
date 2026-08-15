/**
 * Tailwind CSS 4 detecta el contenido automaticamente, pero se deja este
 * archivo explicito para el editor/IDE y por si hace falta acotar rutas.
 * Los tokens de diseno (colores, tipografia) se definen en `@theme` dentro
 * de src/styles/main.css a partir de la Fase 2 (Diseno).
 */
export default {
  content: ["../src/**/templates/**/*.html", "../src/**/*.py", "./src/js/**/*.js"],
};
