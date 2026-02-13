# Respuestas a observaciones de colega basadas en v13 (con contraste v10)

**Fuentes verificadas (v13):**
- Manuscrito limpio: `V13ScientificData/main_english_v13_final.tex`
- Manuscrito con cambios: `V13ScientificData/main_english_v13.tex`
- Respuesta a revisores (v13): `V13ScientificData/Response_to_Reviewers_CoSiBD_v13.ipynb`
- Observaciones del colega: `cambiosPaper.md`

**Fuentes verificadas (baseline v10 / comparativa):**
- Manuscrito v10 (limpio): `main_englishv10_final.tex`
- Comparativa v13 vs v10: `ComparativaV13_vs_V10.md`

> Criterio aplicado: para cada punto se marca **Estado en v13** (Resuelto / Parcial / Pendiente), se aporta **evidencia** (cita breve + ubicación), y si no está resuelto se propone una **acción concreta**.

---

## 0) Chequeo de coherencia: notebook v13 vs TeX v13

**Hallazgo principal:** el notebook `Response_to_Reviewers_CoSiBD_v13.ipynb` describe cambios y secciones (p. ej., “transfer experiments”, “baseline SR benchmark”, etc.) que **no aparecen** en `main_english_v13_final.tex` (no se encuentran cadenas como “Multi-Scale Super-Resolution Benchmark”, “Illustrative Transfer Experiments”, “TimeSeriesSRNet”, etc.).

- **Estado:** Pendiente (hay divergencia entre lo que se afirma en el notebook y lo que contiene el TeX v13_final actualmente en el repo).
- **Evidencia (notebook):** declara “Revision package: `main_english_v13_final` + dataset/code updates” y desarrolla respuestas con supuestas ubicaciones por páginas, y menciona explícitamente secciones ampliadas.
- **Evidencia (TeX v13_final):** `main_english_v13_final.tex` incluye *Technical Validation* con subsecciones espectrales y luego pasa a *Usage Notes*; no incluye un bloque de benchmark SR multi-escala ni experimentos de transferencia.
- **Acción recomendada:** decidir cuál es la “fuente de verdad”:
  1) si el TeX v13_final es el correcto, entonces el notebook v13 debe actualizarse para reflejar **exactamente** lo que está en el TeX, o
  2) si el notebook refleja el contenido deseado, entonces el TeX v13_final debe incorporar esas secciones (y sus figuras/tablas) para que todo sea consistente.

**Nota (baseline v10):** varios cambios que el colega pide (y que el notebook v13 sugiere) ya están implementados en `main_englishv10_final.tex`, pero no se observan reflejados consistentemente en `main_english_v13_final.tex`. Ejemplos:
- Abstract v10 ya incluye (i) metadata/segmentos, (ii) “seeds” sin “random”, y (iii) una frase de validación en escenarios reales.
- Background v10 ya incluye una limitación explícita en telecom y una narrativa clara de “doble propósito” (benchmark + transferencia).

**Evidencia adicional de “contenido SR benchmark/transfer” existente en otras versiones (no en v13_final actual):**
- `v12ArticleScientificData/main_english_v12.tex` contiene `\subsection*{Multi-Scale Super-Resolution Benchmark}`.
- `backup_tex/main_englishv09_final.tex` (y otros backups v09) contiene `Multi-Scale Super-Resolution Benchmark`, menciones a `TimeSeriesSRNet`, y bloques de “transfer/real-world” (EEG/VCTK).

**Implicación práctica:** antes de cerrar respuestas, conviene confirmar si el `V13ScientificData/main_english_v13_final.tex` corresponde efectivamente al “v13 final” que se pretende someter (o si es una copia incompleta respecto a v10/v12/v09 y al notebook).

**Inconsistencia específica adicional (Zenodo/cita en primer uso):**
- El notebook afirma que Zenodo se cita “at first mention in Data Records”.
- En el TeX v13_final, el primer párrafo de *Data Records* menciona Zenodo sin `\cite{cosibd_zenodo_2025}`, y la cita aparece más adelante en un párrafo final (“The full dataset is publicly available on Zenodo \cite{cosibd_zenodo_2025} …”).

---

## GENERAL

### 1) Eliminar “random” cuando se refiere a “seed”
- **Estado en v13:** Pendiente.
- **Evidencia (v13_final):** aparecen múltiples menciones a “random seeds”, “unique random seed”, “Random Seed” en *Methods*/*Data Records*.
  - Ej.: “All generation parameters, including **random seeds**, …” (Methods, después de `fig:r1_5_sampling_units`).
  - Ej.: “Reproducibility is ensured through documented **random seeds** …” (Data Records).
  - Ej.: Tabla de parámetros incluye fila “**Random Seed** & 10000--12499 …”.
- **Acción recomendada (concreto):**
  - Sustituir consistentemente “random seed(s)” → “seed(s)” cuando el foco es **reproducibilidad/determinismo**.
  - Ajustar frases donde “random” sí describe el *muestreo de parámetros* (si se quiere mantener) sin mezclarlo con “seed”. Por ejemplo:
    - “Each signal is generated using a unique **seed** …”
    - “Parameter values are **sampled** within the defined ranges …”
  - En tabla, cambiar “Random Seed” → “Seed” y en descripción “Per-signal seed enabling deterministic regeneration.”

- **Nota (baseline v10):** el abstract v10 ya usa el framing pedido: “... documenting all generation parameters, including **seeds for full reproducibility**.” Mantener esta redacción (o equivalente) en v13 ayuda a que el manuscrito sea consistente y más defendible.

### 2) Eliminar referencias bibliográficas no usadas (`referencias.bib`)
- **Estado en v13:** Parcial (es factible y cuantificado, pero debe hacerse al final de estabilizar el contenido del TeX).
- **Evidencia (auditoría rápida sobre v13_final + referencias.bib):**
  - Claves citadas detectadas en `main_english_v13_final.tex`: 26
  - Entradas en `referencias.bib`: 35
  - Entradas no citadas actualmente: 9
  - No hay citas faltantes en bib.
  - Primeras 9 no usadas (todas): `Forestier2017`, `IbarraFiallo2024`, `Kaniraja2024`, `Kuleshov2017`, `Luciw2014`, `Marple1987`, `Morales2022`, `Rabiner1975`, `Yamagishi2019`.
- **Acción recomendada:**
  - **No borrar aún** si se planea incorporar (como sugiere `cambiosPaper.md`) secciones de SR benchmark/transfer.
  - Además, varias de esas claves “no usadas en v13_final” sí se usan en el baseline v10 o en backups (p. ej., `IbarraFiallo2024` en Background v10; `Yamagishi2019` en ejemplos/transfer en v09; `Kuleshov2017`, `Kaniraja2024`, `Luciw2014` en v09).
  - Tras decidir la “fuente de verdad” (qué secciones quedan finalmente), recién ahí eliminar entradas no citadas o reintroducir las citas donde corresponda.

### 3) Unidades/títulos en ejes Figuras (2,5,6,15)
- **Estado en v13:** Pendiente de verificación visual (no se puede confirmar solo con el TeX, porque son PNG/PDF incluidos).
- **Evidencia (v13_final):** las figuras se incluyen como imágenes (`\includegraphics{...}`), por lo que los ejes/unidades dependen de cómo se generaron los archivos.
- **Acción recomendada (concreto):**
  - Identificar los archivos exactos de las figuras equivalentes en v13 (por `\includegraphics{...}`) y abrirlas para comprobar ejes.
  - Si faltan, regenerarlas desde los scripts/notebooks que las producen, añadiendo `xlabel/ylabel` y unidades en el propio plot.
  - Si no hay scripts reproducibles para alguna figura, alternativa: editar la imagen fuente (Illustrator/Inkscape) o regenerar con un script mínimo.

### 4) Revisión global de inglés
- **Estado en v13:** Pendiente (no hay evidencia de una pasada editorial global; solo cambios puntuales).
- **Acción recomendada:** realizar una pasada final con foco Scientific Data: concisión, consistencia terminológica (time-series vs temporal signals), y evitar overclaiming. Idealmente revisión nativa/profesional, como indica la observación.

---

## ABSTRACT

### 1) Quitar “industrial monitoring” de la primera frase
- **Estado en v13:** Pendiente.
- **Evidencia (v13_final, abstract):** “... biomedical engineering, telecommunications, and **industrial monitoring** ...”
- **Acción recomendada:** reescribir primera frase alineada con los dominios usados después (biomed + telecom/audio) y eliminar industrial si no se sostiene en el cuerpo.
- **Nota (baseline v10):** el abstract v10 ya está alineado (solo “biomedical engineering or telecommunications”). Si v13 debe ser una mejora, debería preservar este enfoque.

### 2) Quitar referencia genérica a “signal processing” y centrar en SR
- **Estado en v13:** Parcial.
- **Evidencia (v13_final, abstract):** “... including temporal super-resolution and related **signal processing** tasks.”
- **Acción recomendada:** cambiar por una formulación enfocada (p. ej., “... particularly temporal super-resolution”).

### 3) Rehacer frase de metadatos (segmentos + parámetros)
- **Estado en v13:** Pendiente (el abstract no menciona metadatos/segmentos explícitamente).
- **Acción recomendada:** añadir una frase corta del tipo: “... with comprehensive metadata describing segment structure and documenting generation parameters ...”.
- **Nota (baseline v10):** esto ya está implementado literal en v10: “... with comprehensive metadata describing the signals' segments and documenting all generation parameters ...”.

### 4) Cambiar “including random seeds” → “including seeds”
- **Estado en v13:** N/A en abstract (no se mencionan seeds en el abstract actual), pero el problema existe en el resto del manuscrito.
- **Acción recomendada:** si se añade una mención en abstract, usar “seeds” sin “random”.

### 5) Última frase debe reflejar validación con datos reales/transferencia
- **Estado en v13:** Pendiente.
- **Evidencia (v13_final, abstract):** la validación se describe solo como espectral (“Technical validation focuses on spectral characteristics...”).
- **Acción recomendada:** si realmente existe en la revisión v13 (según notebook) una validación con transferencia, incorporarla también al TeX y reflejarla en abstract. Si no existe en TeX, evitar afirmarlo.
- **Nota (baseline v10):** el abstract v10 ya contiene la idea: “We report a technical validation that includes ... real-world scenarios.” Si ese claim se mantiene en v13, debe estar sustentado en el cuerpo del manuscrito (y ser consistente con notebook/figuras/tablas).

### 6) Abstract ≤ 170 palabras
- **Estado en v13:** Pendiente.
- **Evidencia (conteo aproximado):** ~212 palabras (v13_final).
- **Acción recomendada:** recortar 20–25% eliminando redundancias (p. ej., frases sobre cómo se genera el dataset pueden reducirse a una sola oración) y centrar: qué es, qué trae (pares LR–HR + metadata), y qué se valida.
- **Nota (baseline v10):** incluso si v10 ya incluye gran parte de lo pedido, v13 debería conservar esas piezas clave pero con una redacción más compacta para cumplir el límite.

---

## BACKGROUND AND SUMMARY

### 1) Enfocar dominios a los que se muestran luego
- **Estado en v13:** Pendiente.
- **Evidencia (v13_final):** incluye finanzas/forecasting, industrial monitoring y environmental science (además de biomed y telecom).
- **Acción recomendada:** reescribir primer párrafo eliminando dominios no usados en experimentos/validación final.

### 2) Reducir listado de DL (centrar CNN; quizá GAN) y quitar “forecasting”
- **Estado en v13:** Pendiente.
- **Evidencia (v13_final):** menciona CNN, RNN/LSTM, GAN y explícitamente “forecasting”.
- **Acción recomendada:** dejar CNN (+ GAN si se quiere sostener con cita) y retirar forecasting si no hay resultados de forecasting.

### 3) Ajuste de inicio del tercer párrafo (privacidad, etc.)
- **Estado en v13:** Parcial.
- **Evidencia (v13_final):** ya menciona GDPR/HIPAA, consistente con la sugerencia.
- **Acción recomendada:** pulir redacción para flujo y coherencia con dominios que realmente se discuten.

### 4) Sustituir ejemplo “environmental monitoring” por limitación en telecom/audio
- **Estado en v13:** Pendiente.
- **Evidencia (v13_final):** se mantiene environmental monitoring en limitaciones.
- **Acción recomendada:** reemplazar por limitación realista de telecom/audio (p. ej., licencias/derechos en audio, privacidad, o dificultad de obtener pares LR–HR en condiciones consistentes) y añadir referencia apropiada.
- **Nota (baseline v10):** v10 ya usa exactamente el tipo de limitación sugerida: “in telecommunications, data availability is limited by proprietary protocols and the high cost of acquiring ... datasets ...”.

### 5) Añadir referencia nueva sobre potencial SR en audio/telecom
- **Estado en v13:** Parcial (se menciona telecom/env/industrial, pero sin referencia específica de SR en audio/telecom).
- **Acción recomendada:** añadir una cita específica sobre SR/audio o SR en comunicaciones, y ajustar el texto para no dispersarse en dominios no tratados.
- **Nota (baseline v10):** v10 ya incluye una cita explícita para audio/telecom SR: “SR also applies to audio/speech enhancement and telecommunications ... \cite{IbarraFiallo2024}.”

### 6–8) Reforzar narrativa “doble propósito” (benchmark + transferencia)
- **Estado en v13:** Parcial.
- **Evidencia (v13_final):** se presenta como benchmark reproducible; no se explicita doble propósito (pretrain/finetune con reales) en Background.
- **Acción recomendada:** incorporar el “double purpose” tal como propone el colega, pero solo si el manuscrito efectivamente contiene (o contendrá) evidencia/experimentos de transferencia.
- **Nota (baseline v10):** el “double purpose” está implementado de forma explícita en Background v10 (con redacción muy cercana a lo que pide el colega). Si v13 pretende ser superior, debería preservar esa narrativa y respaldarla con Technical Validation.

### 9–12) Saltos de página, reescritura “To further position…”, tabla comparativa
- **Estado en v13:** Parcial.
- **Evidencia (v13_final):** existe sección “Related synthetic time-series resources” + tabla comparativa + texto de “practical gap”.
- **Puntos aún pendientes:**
  - La nota al pie de “Configurable” sigue presente.
  - Falta explicación más profunda de columnas y “difficulty levels” (se menciona pero no se explica formalmente).
  - Definición explícita de LR/HR (siglas) no aparece como tal.
- **Acción recomendada:**
  - Quitar footnote y mover explicación al cuerpo.
  - Añadir un párrafo explicando columnas y qué significa “difficulty” (degradación por resolución/ruido/estructura).
  - Definir LR/HR en el texto (“Low Resolution (LR)”, “High Resolution (HR)”).

---

## METHODS

### 1) Rehacer primera oración
- **Estado en v13:** Resuelto.
- **Evidencia (v13_final, Methods):** “The methodology used … is illustrated in Figure~\ref{fig:generation_process}.”

### 2) Salto de línea tras primer párrafo
- **Estado en v13:** Resuelto (hay separación `\\ \\`).

### 3) Reescritura “Design rationale inspired by real signals”
- **Estado en v13:** Parcial.
- **Evidencia (v13_final):** aparece bloque “Signal design principles” con lista (i)–(iv) y figura `fig:design_rationale_motivations`.
- **Pendiente:** parte importante de la explicación está en el caption de la figura.
- **Acción recomendada:** mover la interpretación de la figura al cuerpo principal, dejando caption descriptivo corto.

### 4) Mejorar figura motivacional (etiquetas A–D, fuentes, referencias, unidades)
- **Estado en v13:** Pendiente.
- **Evidencia:** la figura motivacional es un único archivo `r1_3_real_signal_motivations.png` con caption largo; no hay subfiguras A–D declaradas en TeX.
- **Acción recomendada:** convertir a subfiguras con `subcaption` (A–D), y añadir párrafo en Methods que explique origen de cada subfigura y su referencia.

### 5) Expandir “Noise injection”
- **Estado en v13:** Resuelto.
- **Evidencia:** el pipeline incluye noise injection + subsección de rationale + Figura `fig:r1_4_powerline_noise`.

### 6) Explicar mejor figura 3 (si aplica)
- **Estado en v13:** Pendiente / No mapeable directamente.
- **Nota:** en v13_final, las figuras con subfiguras múltiples que podrían corresponder han cambiado; hay que mapear qué figura es “Figura 3” en numeración actual.

### 7) Línea en blanco entre subsecciones
- **Estado en v13:** N/A (estructura actual no coincide exactamente con la observación).

### 8) Frase sobre escalado con T
- **Estado en v13:** Resuelto.
- **Evidencia:** sección “Sampling units and frequency interpretation” contiene exactamente la idea: cambiar $T$ rescala Hz preservando secuencia discreta.

### 9) Mejorar Figura 4 (subfiguras A–F + explicación en cuerpo)
- **Estado en v13:** Pendiente (no hay figura declarada como 4 con 6 subfiguras en el TeX actual).

### 10) Eliminar último párrafo “The parameters that govern each step…”
- **Estado en v13:** Pendiente.
- **Evidencia:** el párrafo existe tras `fig:r1_5_sampling_units`.
- **Acción recomendada:** eliminarlo o moverlo a Data Records/Code availability para evitar repetición.

---

## DATA RECORDS

### 1) Rehacer primer párrafo (Zenodo + SR + transferencia)
- **Estado en v13:** Parcial.
- **Evidencia (v13_final):** menciona Zenodo sin `\cite` en la primera frase y describe SR, pero no menciona entrenamiento para SR en señales reales.
- **Acción recomendada:** reescribir párrafo inicial con cita a Zenodo en primera mención y añadir la motivación SR + (si aplica) conexión a uso con reales.

### 2–4) Reescritura de lista HR/LR con Hz ilustrativos, formatos, metadata
- **Estado en v13:** Parcial.
- **Evidencia:** existe itemize HR/LR + formatos + metadata (base_points, variation_type, etc.).
- **Pendiente:** sigue usando “random seeds” y algunas partes no incluyen Hz ilustrativos como en propuesta.

### 5–6) Quitar párrafo repetitivo de “Each signal is provided…” y mover a un párrafo antes
- **Estado en v13:** Pendiente.
- **Evidencia:** el párrafo existe (se repite el contenido de formatos).
- **Acción recomendada:** consolidar en un solo párrafo (idealmente el sugerido por el colega) y evitar repetición.

### 7) Mejoras en “Metadata schema and example”
- **Estado en v13:** Parcial.
- **Evidencia:** tabla `tab:metadata_schema` existe y ejemplo en verbatim existe.
- **Pendiente:**
  - La tabla mezcla “Type / example” en una misma columna; el colega pide columnas separadas.
  - Falta explicación explícita de la tipología completa de etiquetas en `variation_type`.
  - Falta explicación narrativa del ejemplo y un dibujo que lo ilustre.

### 8) Eliminar bloque “The following resolution levels are available…”
- **Estado en v13:** Pendiente.
- **Evidencia:** el bloque está presente.

### 9) Añadir título “Parameters for signal generation” antes de Table 3
- **Estado en v13:** Pendiente.

### 10–15) Mejorar explicación de parámetros + defaults + columna default
- **Estado en v13:** Pendiente.
- **Evidencia:** tabla `tab:Parameter` solo tiene Parameter/Range/Description y usa lenguaje “Random Seed” / “Random” / “Configurable”.
- **Acción recomendada:** añadir columna “Default” y explicar explícitamente que los defaults son los usados para Zenodo.

### 16) Figuras 5 y 6 sin ejes/unidades
- **Estado en v13:** Pendiente de mapeo.
- **Nota:** en el TeX actual aparecen figuras `fig:amplitud` y `fig:simples`; no se puede verificar ejes sin abrir las imágenes.

---

## TECHNICAL VALIDATION

### 1) Primer párrafo debe mencionar espectral + CNN + transferencia
- **Estado en v13:** Pendiente.
- **Evidencia:** el párrafo inicial actual solo describe análisis espectral.
- **Acción recomendada:** solo incluir CNN/transfer si el TeX incorpora efectivamente esas subsecciones (ahora mismo no están).

### 2) Añadir frase final en “Validation Context” sobre defaults
- **Estado en v13:** Parcial.
- **Evidencia:** hay contexto y motivación; falta la frase explícita sobre defaults (cuando no se indique, se usa Table~\ref{tab:Parameter}).

### 3–4) Expandir interpretación de Figura 7/Tabla 4 + añadir referencia
- **Estado en v13:** Pendiente.
- **Evidencia:** interpretación actual es general.
- **Acción recomendada:** añadir un párrafo analítico y una referencia que sustente la conclusión.

### 5) Forzar orden Figura 8 antes de 9
- **Estado en v13:** Pendiente de verificación al compilar.

### 6–7) Expandir explicación de figura de ruido + conclusiones con referencias
- **Estado en v13:** Parcial.
- **Evidencia:** se introduce la figura `fig:noise_ruido` pero la explicación en texto es mínima y no hay un párrafo de conclusiones al final de la subsección.

### 8–10) “Impact of noise …”: unir frase y corregir color 0.2
- **Estado en v13:** Pendiente.
- **Evidencia:** el texto actual dice “0.2 (red curve)”; el colega reporta inconsistencia visual.
- **Acción recomendada:** abrir `graphs/noise.png` y confirmar color; corregir el texto acorde (probablemente “green curve”). Añadir un párrafo final de conclusiones + referencia.

### 11–28) Multi-Scale SR benchmark + TimeSeriesSRNet + transferencia + Figuras 11–15
- **Estado en v13:** Pendiente (no existen esas secciones en el TeX v13_final actual).
- **Evidencia:** no aparecen en `main_english_v13_final.tex` cadenas ni labels asociables.
- **Acción recomendada:** decidir si se incorporan en el manuscrito. Si sí, entonces:
  - crear subsección “Multi-Scale Super-Resolution Benchmark” y definir scaling factors,
  - introducir referencia/justificación de TimeSeriesSRNet,
  - comentar tablas/figuras según las observaciones,
  - y añadir “Illustrative Transfer Experiments” sin “optional”.

---

## USAGE NOTES

### 1) Reescribir “Reading the Data”
- **Estado en v13:** Resuelto en esencia.
- **Evidencia:** se explica consolidated .txt, una fila por señal, y se da ejemplo de carga.

### 2) Reescribir “Visualizing Signal Pairs”
- **Estado en v13:** Resuelto en esencia.
- **Evidencia:** ejemplo con matplotlib y ejes etiquetados (“Sample index”, “Amplitude”).

### 3) Completar ejemplo “Training a baseline model (synthetic-only)” con comentarios
- **Estado en v13:** Pendiente (no existe esa subsección en el TeX v13_final actual).
- **Acción recomendada:** si se añade, incluir el snippet y comentar como pide el colega.

---

## AUTHOR CONTRIBUTIONS

### 1) Cambiar contribución de J. A. L.
- **Estado en v13:** Pendiente.
- **Evidencia (v13_final):** “J. A. L. was responsible for the time series methodological design.”
- **Acción recomendada:** reemplazar por: “J. A. L. was responsible for methodology (time series design) and supervision”.

---

## Resumen ejecutivo (estado global)

- Hay varios puntos **ya bien encaminados** en v13 (noise model, sampling units/Hz scaling, tabla comparativa de recursos, ejemplos básicos de uso).
- Sin embargo, muchas observaciones del colega quedan **Pendientes** o **Parciales** en el `main_english_v13_final.tex` actual (abstract demasiado largo, dominios aún dispersos en Background, uso de “random seed”, footnote de Configurable, y ausencia en TeX de secciones SR benchmark/transfer que el notebook sí afirma).
- Además, el baseline `main_englishv10_final.tex` ya cumple varias de las mejoras editoriales solicitadas (abstract con metadata/segmentos + “seeds” sin “random” + mención de escenarios reales; Background con limitación telecom + cita SR audio/telecom + narrativa de doble propósito). Esto sugiere que el mayor riesgo ahora no es “inventar nuevos cambios”, sino **alinear v13 para no perder mejoras ya logradas** y para que notebook/TeX/claims sean coherentes.

Siguiente paso recomendado: alinear primero TeX v13_final con el contenido que realmente se quiere defender (y con el notebook v13), y luego cerrar el resto de puntos editoriales (terminología seed, recorte abstract, limpieza de bib, figuras con ejes/unidades).
