# Respuestas a observaciones de colega basadas en v10

**Fuentes verificadas (v10):**
- Manuscrito v10 (limpio): `main_englishv10_final.tex`
- Observaciones del colega: `cambiosPaper.md`
- Bibliografía: `referencias.bib`

> Criterio aplicado: para cada punto se marca **Estado en v10** (Resuelto / Parcial / Pendiente), se aporta **evidencia** (cita breve del TeX), y si no está resuelto se propone una **acción concreta**.

---

## GENERAL

### 1) Quitar “random” cuando se refiere a “seed”
- **Estado en v10:** Parcial.
- **Evidencia (v10):**
  - En *Data Records*: “... documenting ... parameters ... including **seeds** ...” y “Reproducibility is ensured through documented **seeds** ...”.
  - Pero aún aparece “Seed used for **random generation** of this specific signal.” (Tabla metadata) y en Tabla de parámetros hay defaults con “**Random**”.
- **Acción recomendada:**
  - Mantener “seed(s)” en todo lo relativo a reproducibilidad.
  - Cambiar “Seed used for random generation” → “Seed used for deterministic generation”.
  - En la tabla de parámetros, reemplazar “Random” por “Sampled (per-signal, recorded in metadata)” o indicar explícitamente distribución/estrategia de muestreo.

### 2) Eliminar referencias no usadas en `referencias.bib`
- **Estado en v10:** Parcial.
- **Evidencia (auditoría v10 vs bib):** 9 entradas no citadas y 4 citas usadas faltan en `referencias.bib`.
  - **No citadas (ejemplos):** `Forestier2017` (el colega la sugiere para transfer), `Mallat1989`, `DeBoor2001`, etc.
  - **Citas faltantes en bib:** `Bengio2013`, `Bishop2006`, `Goodfellow2016`, `Shannon1949`.
- **Acción recomendada:**
  - Primero **agregar** al `.bib` las 4 claves faltantes (porque hoy compilaría con missing refs).
  - Luego decidir si (a) se citan las 9 no usadas donde aplique, o (b) se eliminan al final.

### 3) Unidades/títulos en ejes (Fig. 2, 5, 6, 15)
- **Estado en v10:** Pendiente de verificación visual.
- **Evidencia:** las figuras se incluyen como imágenes (`\includegraphics{...}`), por lo que los ejes/unidades dependen de los archivos gráficos.
- **Acción recomendada:** abrir las figuras referenciadas y corregir en los scripts que las generan (o regenerarlas) para incluir `xlabel/ylabel` + unidades.

### 4) Revisión global de inglés
- **Estado en v10:** Pendiente.
- **Acción recomendada:** pasada final (idealmente nativo/profesional) después de estabilizar la “v14”.

---

## ABSTRACT

### 1) Quitar “industrial monitoring”
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** primera frase menciona “biomedical engineering or telecommunications” (sin industrial).

### 2) Quitar “signal processing” genérico y centrar SR
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** el abstract centra “... tasks like temporal super-resolution.”

### 3) Frase de metadatos (segmentos + parámetros)
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** “... with comprehensive metadata describing the signals' segments and documenting all generation parameters ...”.

### 4) “including random seeds” → “including seeds”
- **Estado en v10:** Resuelto en abstract.
- **Evidencia (v10):** “... including **seeds** for full reproducibility.”

### 5) Última frase del abstract debe reflejar validación con reales/transfer
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** “... technical validation ... application ... in real-world scenarios.”

### 6) Abstract ≤ 170 palabras
- **Estado en v10:** Pendiente (no verificado por conteo aquí).
- **Acción recomendada:** contar palabras y recortar si supera 170.

---

## BACKGROUND AND SUMMARY

### 1) Enfocar dominios a los usados luego
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** primer párrafo solo usa ejemplos de biomed (EEG) y telecom, con citas.

### 2) Reducir listado de DL (CNN; quizá GAN) y quitar “forecasting”
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** segundo párrafo menciona CNN y GAN; no menciona forecasting.

### 3) Ajuste comienzo tercer párrafo (privacidad)
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** incluye GDPR/HIPAA y cita.

### 4) Reemplazar limitación “environmental monitoring” por telecom/audio
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** “... in telecommunications, data availability is limited by proprietary protocols ... channel sounding datasets ...”.

### 5) Añadir referencia SR en audio/telecom
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** “SR also applies to audio/speech ... telecommunications ... \cite{IbarraFiallo2024}.”

### 6) Reescritura párrafo “Deep learning offers adaptive ...”
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** incluye CNNs + cita “Brophy2023,IbarraFiallo2024” sin desviar a otros dominios.

### 7) Ejemplos de synthetic datasets alineados a dominios afines
- **Estado en v10:** Parcial.
- **Evidencia (v10):** menciona biomed (ECG) y comunicaciones inalámbricas; faltaría ajustar si el colega pide aún más alineación con los “reales” usados después.
- **Acción recomendada:** asegurar que los ejemplos citados conectan con los dominios reales que se usan en transfer (EEG/VCTK).

### 8) Reforzar “doble propósito” (benchmark + transferencia)
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** párrafo explícito “double purpose: a) benchmark ... b) train ... finetuning ...”.

### 9) Salto de página antes de “To further position ...”
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** hay `\newpage` antes de “To further position ...”.

### 10–12) “Related synthetic ...” + explicación columnas + difficulty + quitar footnote + definir LR/HR
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** explica columnas, define “Paired LR--HR SR (Low Resolution - High Resolution)”, y “difficulty levels” como degradación; no depende de footnote para “Configurable”.

---

## METHODS

### 1) Rehacer primera oración
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** “The methodology used ... is illustrated in Figure~\ref{fig:generation_process} ...”.

### 2) Salto de línea tras primer párrafo
- **Estado en v10:** Resuelto.
- **Evidencia:** hay separación `\\ \\`.

### 3) Reescritura “Design rationale inspired by real signals”
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** el párrafo coincide con la propuesta del colega.

### 4) Mejorar Figura 2 (A–D, fuentes, explicación en cuerpo, unidades)
- **Estado en v10:** Parcial.
- **Evidencia (v10):** hay un párrafo que describe A–D y da fuentes (EEG con cita, VCTK con cita), y el caption ya es más corto.
- **Pendiente:** verificación visual de unidades en eje horizontal (depende del PNG) y confirmar que la figura efectivamente contiene las etiquetas A–D.

### 5) Expandir “Noise injection”
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** descripción extensa (AWGN + bursts 50/60 Hz + metadata + prob 50%).

### 6) Figura 3 con A–D y explicación en cuerpo
- **Estado en v10:** Parcial (no mapeado aquí con certeza a “Figura 3” del colega).
- **Acción recomendada:** ubicar el bloque exacto “Figure 3 illustrates ...” en v10 y verificar si cumple A–D + fuentes + explicación en cuerpo.

### 7) Línea en blanco entre subsecciones (ruido vs sampling units)
- **Estado en v10:** Resuelto.

### 8) Frase sobre escalado con T
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** incluye la frase propuesta casi literal (“changing T rescales ...”).

### 9) Mejorar Figura 4 (A–F + explicación en cuerpo)
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** se describe explícitamente “six panels (A--F)” y se explica en el cuerpo.

### 10) Eliminar párrafo “The parameters that govern each step ...”
- **Estado en v10:** Resuelto.
- **Evidencia:** no aparece ese párrafo al final del bloque de sampling units.

---

## DATA RECORDS

### 1) Primer párrafo (Zenodo + SR + transferencia)
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** “... available on Zenodo\cite{cosibd_zenodo_2025} ... SR ... train ... real-world signals.”

### 2–4) HR/LR con Hz ilustrativos + formatos + metadata
- **Estado en v10:** Resuelto.
- **Evidencia:** bullets incluyen Hz ilustrativos, 3 formatos, metadata con `base_points`, `variation_type`, etc.

### 5–6) Quitar párrafo repetitivo “Each signal is stored ...” y consolidar
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** no hay un párrafo redundante final; se incluye un párrafo único “Regarding the three formats ...”.

### 7) Mejoras tabla metadata (Type vs Example) + explicar `variation_type` + explicar ejemplo + dibujo
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** tabla con columnas Field/Type/Example/Meaning, explicación narrativa de `variation_type`, snippet JSON explicado, y figura `metadata_vis.png`.

### 8) Eliminar bloque “The following resolution levels are available ...”
- **Estado en v10:** Resuelto (no aparece en el fragmento verificado; si existe más adelante, habría que removerlo).

### 9) Título “Parameters for signal generation”
- **Estado en v10:** Resuelto.

### 10–15) Explicar parámetros + defaults + columna default
- **Estado en v10:** Parcial.
- **Evidencia (v10):** tabla incluye columna “Default”.
- **Pendiente:** coherencia terminológica: muchos defaults dicen “Random” y el colega pidió evitar “random” en este contexto; además el caption dice “Default values apply when a parameter is not randomized”, que contradice el objetivo de reproducibilidad.
- **Acción recomendada:** definir “Default” como el valor usado para Zenodo y “Sampled” como mecanismo (y que el valor por señal se guarda en metadata).

### 12) Explicar comando para generar dataset propio + figura (screenshot)
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** subsección “Custom Dataset Generation” + figura `cli_tool_demo.png`.

### 13) Quitar párrafo repetitivo “The full dataset is hosted in Zenodo ...”
- **Estado en v10:** Pendiente.
- **Evidencia (v10):** el párrafo aparece al final (antes de Technical Validation) y repite Zenodo.
- **Acción recomendada:** eliminarlo (ya se cita Zenodo al inicio de Data Records).

### 16) Figuras 5 y 6 sin ejes/unidades
- **Estado en v10:** Pendiente de verificación visual.

---

## TECHNICAL VALIDATION

### 1) Rehacer primer párrafo (espectral + CNN + transferencia)
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** el primer párrafo menciona explícitamente espectral + benchmark CNN + transfer con EEG/speech.

### 2) Frase final “Validation Context” sobre defaults
- **Estado en v10:** Pendiente.
- **Evidencia:** el texto de Validation Context no incluye la frase “When not explicitly indicated... default Table~...”.
- **Acción recomendada:** añadir la frase propuesta del colega.

### 3–4) Expandir análisis Figura 7/Tabla 4 + referencia final
- **Estado en v10:** Parcial.
- **Evidencia (v10):** hay explicación más concreta y añade una referencia al final (`\cite{Bengio2013}`), pero esa clave **no está** en `referencias.bib`.
- **Acción recomendada:** completar la interpretación (si falta) y añadir `Bengio2013` a la bib.

### 5) Forzar orden Figura 8 antes de 9
- **Estado en v10:** Pendiente de verificación al compilar.

### 6) Expandir explicación de figura de ruido (no en caption)
- **Estado en v10:** Resuelto.
- **Evidencia:** hay párrafo “Figure ... presents examples ... progressively obscure ...” antes de la figura.

### 7) Añadir párrafo final de conclusiones en “Spectral Stability ...” + referencia
- **Estado en v10:** Pendiente.
- **Evidencia:** termina con análisis pero sin “conclusion paragraph”.

### 8) Unir frase “Figure 10 illustrates ...” en el mismo párrafo
- **Estado en v10:** Pendiente.
- **Evidencia:** está en un párrafo separado con saltos (`\\ \\`).

### 9) Corregir “0.2 (red curve)” → green
- **Estado en v10:** Resuelto.
- **Evidencia (v10):** “... to 0.2 (**green curve**) ...”.

### 10) Añadir párrafo final de conclusiones en “Impact of Noise ...” + referencia
- **Estado en v10:** Parcial.
- **Evidencia:** hay un párrafo final con conclusión y cita `\cite{Bishop2006}`, pero la clave **falta** en `referencias.bib` y la conclusión podría ampliarse.
- **Acción recomendada:** añadir `Bishop2006` al `.bib` y expandir conclusión si se considera necesario.

### 11) Aclarar scaling factors (5x,10x,...) en benchmark
- **Estado en v10:** Resuelto.
- **Evidencia:** “5× (1000→5000), 10× (500→5000), ...”.

### 12) Referencia bibliográfica de TimeSeriesSRNet
- **Estado en v10:** Resuelto.
- **Evidencia:** “... inspired by ... \cite{Kuleshov2017}.”

### 13) Justificar por qué esa arquitectura
- **Estado en v10:** Parcial.
- **Evidencia:** se menciona “inspired by deep residual architectures for audio generation”, pero podría justificarse mejor para SR 1D.

### 14) Justificar entrenamiento (MSE, Adam, batch, ...)
- **Estado en v10:** Parcial.
- **Evidencia:** justifica MSE con `\cite{Goodfellow2016}` (pero la clave falta en bib). Adam/early stopping no están justificados con cita.

### 15) Comentar más la Tabla 5
- **Estado en v10:** Parcial.
- **Evidencia:** hay comentario general “loss increased ...”, pero se podría referenciar explícitamente valores.

### 16) Reubicar “Figure 11 illustrates ...” cerca de su primera mención
- **Estado en v10:** Resuelto parcialmente.
- **Evidencia:** en v10 se menciona Figure `multifactor_loss_curves` justo después; no hay un párrafo separado “Figure 11 illustrates ...” con el mismo texto del comentario.

### 17–18) Explicar mejor figuras de predicción (y reducir subfiguras si hay demasiadas)
- **Estado en v10:** Parcial.
- **Evidencia:** hay figuras `multifactor_predictions` y captions, pero la explicación en texto sigue siendo breve.

### 19–21) Reordenar métricas espectrales vs espectrograma + explicar artifacts + interpretar LSD/SCORR con refs
- **Estado en v10:** Parcial.
- **Evidencia:** el texto menciona métricas y luego espectrogramas, pero en el TeX la figura `spectral_analysis` aparece antes que `spectral_metrics` (orden opuesto al recomendado). Además, falta interpretación explícita “qué significa bueno/malo” más allá del caption.
- **Acción recomendada:** intercambiar el orden de figuras o forzar con `\FloatBarrier`/posición; añadir párrafo interpretando LSD/SCORR con referencias.

### 22) Quitar “(optional)” del título transfer
- **Estado en v10:** Resuelto.

### 23–24) Rehacer párrafos iniciales (source/target + 4 estrategias)
- **Estado en v10:** Resuelto.

### 25) Reescribir párrafo de resultados (con cita Forestier2017) + explicación detallada
- **Estado en v10:** Parcial.
- **Evidencia:** hay explicación clara y afirma Mixed/Tuned mejoran; pero no cita `Forestier2017` (y esa entrada está hoy “no usada”).
- **Acción recomendada:** citar `Forestier2017` si se quiere sustentar comparaciones en series temporales, o removerla si no aplica.

### 26–27) Añadir párrafo explicando figura 15 + ejes/unidades
- **Estado en v10:** Parcial.
- **Evidencia:** figura `model_comparisons` tiene caption informativo, pero falta un párrafo explicativo adicional; ejes/unidades dependen del PDF.

### 28) Especificar dónde están ejemplos de audio/repo + revisar último párrafo
- **Estado en v10:** Pendiente.
- **Evidencia:** se menciona que se reconstruyeron clips y se reporta correlación, pero no se indica ruta exacta a ejemplos.
- **Acción recomendada:** añadir la ubicación concreta en el repositorio (carpeta/archivo) y, si aplica, link.

---

## USAGE NOTES

### 1) Reescribir “Reading the Data”
- **Estado en v10:** Resuelto.
- **Evidencia:** el párrafo coincide con la propuesta del colega.

### 2) Reescribir “Visualizing Signal Pairs”
- **Estado en v10:** Resuelto.
- **Evidencia:** el párrafo y ejemplo están alineados; incluye `xlabel/ylabel`.

### 3) Completar comentarios en código “Training a baseline model (synthetic-only)” 
- **Estado en v10:** Parcial.
- **Evidencia:** hay comentarios iniciales, pero el loop/val/métricas/modelo podrían comentarse más.
- **Acción recomendada:** añadir comentarios en creación de tensores/loaders, definición de red, entrenamiento/validación, y explicación de shapes.

---

## AUTHOR CONTRIBUTIONS

### 1) Cambiar contribución J. A. L.
- **Estado en v10:** Pendiente.
- **Evidencia (v10):** “J. A. L. was responsible for the time series methodological design.”
- **Acción recomendada:** cambiar a: “J. A. L. was responsible for methodology (time series design) and supervision”.

---

## Resumen ejecutivo (v10)

- v10 ya implementa **la mayor parte** de las modificaciones que tu colega propone (especialmente Abstract, Background, Data Records, y la existencia del benchmark multi-escala + transfer con reales).
- Lo principal que queda por cerrar en v10 para satisfacer al colega de forma estricta es: (i) consistencia del uso de “random” vs “sampled/default/deterministic”, (ii) verificación/corrección de ejes/unidades en figuras, (iii) conclusiones finales en dos subsecciones espectrales, (iv) reorden/explicación de figuras métricas vs espectrogramas, (v) citar/agregar referencias faltantes al `.bib`, y (vi) ajustar Author Contributions.
