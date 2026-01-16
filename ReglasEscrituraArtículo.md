# Reglas de trabajo (notebook → LaTeX)

Estas reglas están pensadas para maximizar fluidez de escritura en LaTeX y minimizar riesgo editorial (inconsistencias, promesas no verificables, re-trabajo).

## Reglas

- **Una sola fuente de verdad por requisito.** Cada `[E#] / [R#-#]` debe tener exactamente: (A) postura, (B) bloque paste‑ready, (C) evidencia reproducible. Si algo cambia, actualizas primero esa tríada antes de tocar el LaTeX.
- **Cierre operativo antes de escribir.** No escribas “texto bonito” en LaTeX hasta que el requisito esté cerrado en 1–2 frases: *qué se cambia* y *por qué*. Eso evita re‑trabajo.
- **Mapeo fijo a secciones del .tex.** Para cada requisito, decide un único destino: `Abstract / Methods / Data Records / Technical Validation / Code Availability / Figures/Tables`. No repartas un mismo requisito en muchas partes salvo que sea inevitable.
- **Bloques paste‑ready como unidades atómicas.** Copia/pega el bloque (B) tal cual y luego haces solo dos ajustes: (i) estilo local (conectores, referencias cruzadas), (ii) ubicación exacta. Evita reescribir desde cero.
- **Regla de coherencia “afirmación ↔ evidencia”.** Si el bloque (B) afirma números/criterios (“fs≈398 Hz”, “SCORR>0.97”, “2,000/500”), debe existir un artefacto reproducible (C) que lo pueda regenerar o al menos verificar leyendo archivos del repo.
- **No prometer artefactos no versionados.** Nada de “ver figura X” si esa figura no se genera desde repo o no está garantizada en el árbol del proyecto. En el LaTeX, referencia solo lo que puedas reconstruir.
- **Cambios mínimos por iteración.** Itera por requisitos, no por secciones. Una pasada típica: seleccionas 3–5 requisitos, los integras en LaTeX, recompilas, y vuelves al notebook si aparece inconsistencia.
- **Congelar lenguaje sensible.** Términos que ya dieron problemas (p. ej., “train/val/test split”) quedan “congelados”: una formulación oficial y no se improvisa en LaTeX. Si necesitas variar, lo decides primero en el notebook.
- **Evitar “tono de trabajo interno”.** En LaTeX y en el notebook final: cero “TODO”, “pending”, “next steps”, “we plan”. Todo debe leerse como hecho verificable.
- **Regla de trazabilidad: una frase de ubicación.** Cada requisito debe incluir “LOCATION IN ARTICLE” o equivalente (aunque sea informal) y en LaTeX respetas esa ubicación. Si cambias de lugar, actualizas la ubicación en el archivo de respuestas.
- **Recompilar con checklist corto.** Después de integrar un bloque: (1) compila, (2) revisa que no rompiste referencias/bibliografía, (3) verifica que no contradices otra sección, (4) valida que el “claim” tenga soporte.
- **Mantener el “contrato” de reproducibilidad.** Si el notebook no guarda imágenes embebidas, la regla es: si el revisor cuestiona algo visual, lo regeneras ejecutando celdas, pero no pegas capturas en el rebuttal; lo conviertes en un resultado reproducible.
