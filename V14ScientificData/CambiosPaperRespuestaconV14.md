# CambiosPaper — Respuestas con V14 (mapeo meticuloso)

Fecha: 2026-02-09

**Fuentes usadas (autoridad):**
- Checklist de observaciones del colega: `../cambiosPaper.md`
- Manuscrito v14 (clean): `main_english_v14_final.tex`
- Manuscrito v14 (tracked): `main_english_v14.tex`
- Bibliografía v14: `referencias.bib`

**Criterio de evidencia:**
- Las referencias a “dónde quedó resuelto” se dan en términos de **Sección/Subsección/Figura/Tabla/Label** (evita fragilidad por cambios de líneas).
- Cuando aplica, incluyo un **extracto TeX** breve como evidencia.

**Leyenda de estado:**
- **RESUELTO**: implementado y verificable en v14.
- **PARCIAL**: hay avances, pero falta parte explícita del pedido.
- **PENDIENTE**: no está implementado o requiere acciones adicionales (p.ej., regenerar figuras).

---

## GENERAL

### 1. Quitar “random” cuando se refiere a seed
**Estado:** RESUELTO.

**En v14 (dónde):**
- Abstract.
- Data Records (descripción de metadata + reproducibilidad).
- Tabla de parámetros (`tab:Parameter`).

**Evidencia (extractos v14):**
```tex
... including seeds for full reproducibility.
```
```tex
Reproducibility is ensured through documented seeds: ... unique seed (ranging from 10,000 to 12,499) ...
```
```tex
Seed used for deterministic generation of this specific signal.
```
```tex
Low Frequency ... Sampled (seed-controlled)
```

**Notas:** Se eliminó también el uso semántico de “random” como sinónimo de “no determinista”; donde se mantiene variabilidad, se expresa como “sampled (seed-controlled)” o “stochastic sampling effects (seed-controlled)”.

---

### 2. Eliminar referencias bibliográficas no usadas
**Estado:** RESUELTO.

**En v14 (qué se hizo):**
- Se eliminaron 9 entradas no citadas de `referencias.bib` (las listadas en `_bib_audit_v14.txt`).

**Resultado actualizado (v14):**
- Claves citadas únicas en TeX: 30
- Entradas en `referencias.bib`: 30
- Entradas no citadas: 0

---

### 3. Unidades en ejes de Figuras 2, 5, 6 y 15
**Estado:** PARCIAL (mitigado por caption).

**En v14 (dónde):**
- Methods: se añadió y explicó la convención de unidades y escalamiento temporal (subsección “Sampling units and frequency interpretation” + Figura `fig:r1_5_sampling_units`).
- Methods: Figura `fig:design_rationale_motivations` (caption aclara ejes para paneles de forma de onda).
- Data Records: Figuras `fig:amplitud` y `fig:simples` (captions aclaran ejes).
- Technical Validation: Figura `fig:model_comparisons` (caption aclara ejes).

**Evidencia (extracto v14):**
```tex
CoSiBD signals are provided as discrete sequences x[n] ... interpreting it as physical time requires choosing a duration T ...
... any band-specific interpretation in Hz ... should be understood under the chosen T ...
```

**Qué falta (según observación):**
- Las figuras señaladas requieren **títulos de ejes y/o unidades directamente en las imágenes** (no solo en texto/caption).

**Nota de implementación (decisión actual):**
- Dado que en este punto no se regenerarán las figuras, se incorporó una aclaración explícita en captions indicando que el eje x corresponde a muestras (sample index) y el eje y a amplitud (unidades arbitrarias) para las figuras relevantes.

**Acción requerida:**
- (Solo si se decide cumplir estrictamente “en la imagen”): identificar exactamente qué assets corresponden a “Fig 2/5/6/15” en el PDF final de v14 y regenerarlos con `xlabel/ylabel` y unidades.

---

### 4. Revisión global de inglés
**Estado:** PENDIENTE.

**En v14 (dónde):** Global.

**Notas:** Se han hecho mejoras puntuales (redacción/precisión) pero aún no hay una pasada global sistemática (estilo, gramática, consistencia terminológica).

---

## ABSTRACT

### 1. Quitar “industrial monitoring” del primer enunciado
**Estado:** RESUELTO.

**En v14:** Abstract.

**Evidencia:**
```tex
The increasing application of time-series analysis in fields like biomedical engineering or telecommunications ...
```

---

### 2. Reemplazar referencia genérica a “signal processing” por SR
**Estado:** RESUELTO.

**Evidencia:**
```tex
... particularly deep learning systems, in tasks like temporal super-resolution.
```

---

### 3. Rehacer frase de metadatos
**Estado:** RESUELTO.

**Evidencia:**
```tex
... with comprehensive metadata describing the signals' segments and documenting all generation parameters ...
```

---

### 4. Quitar “random” en “including random seeds”
**Estado:** RESUELTO.

**Evidencia:**
```tex
... including seeds for full reproducibility.
```

---

### 5. Última frase del abstract: priorizar validación con transferencia/real-world
**Estado:** RESUELTO.

**Evidencia:**
```tex
We report a technical validation that includes, among others, a whole study of the application ... in real-world scenarios.
```

---

### 6. Abstract ≤ 170 palabras
**Estado:** RESUELTO.

**Verificación:** el abstract en v14 tiene 159 palabras (conteo automático sobre `main_english_v14_final.tex` / `main_english_v14.tex`).

---

## BACKGROUND AND SUMMARY

### 1. Primer párrafo: dejar solo dominios que luego se usan
**Estado:** RESUELTO.

**En v14:** `Background & Summary` párrafo 1.

**Evidencia:** menciona biomedicina y telecomunicaciones (y referencias asociadas), sin “industrial monitoring” ni dominios no usados.

---

### 2. Segundo párrafo: no listar demasiadas técnicas; quitar forecasting
**Estado:** RESUELTO.

**Evidencia:**
```tex
... such as Convolutional Neural Networks (CNNs) or Generative Adversarial Networks (GANs) ...
```

---

### 3. Tercer párrafo: reescritura inicial
**Estado:** RESUELTO.

---

### 4. Sustituir ejemplo de “environmental monitoring” por limitación telecom/audio
**Estado:** RESUELTO.

**Evidencia:**
```tex
... in telecommunications, data availability is limited by proprietary protocols ... \cite{Zhang2016}.
```

---

### 5. Potencial SR en audio/telecom con referencia
**Estado:** RESUELTO.

**En v14 (dónde):** `Background & Summary` (párrafo sobre potencial de SR en múltiples dominios).

**Evidencia (extracto v14):**
```tex
... SR also applies to audio/speech enhancement and telecommunications ... \cite{Kuleshov2017,IbarraFiallo2024}.
```

**Notas:** `Kuleshov2017` corresponde a arXiv:1708.00853 (“Audio super resolution using neural networks”), y menciona aplicaciones prácticas en telephony/compression, lo cual encaja con el contexto audio/telecom.

---

### 6. Sexto párrafo: ajustar redacción y foco
**Estado:** RESUELTO.

---

### 7. Séptimo párrafo: ejemplos sintéticos más afines + referencias
**Estado:** RESUELTO.

**Evidencia:**
```tex
... biomedical signal analysis \cite{mcsharry2003ecg} and wireless communications \cite{oshea2016grcon} ...
```

---

### 8. Octavo párrafo: doble aportación (benchmark + uso combinado con real)
**Estado:** RESUELTO.

**Evidencia:** aparece explícitamente el doble propósito a) benchmark b) uso para SR en real (incluyendo fine-tuning).

---

### 9. Salto de página antes de “To further position CoSiBD”
**Estado:** RESUELTO.

**Evidencia:** `\newpage` antes de “To further position ...”.

---

### 10. Rehacer párrafo “To further position ...”
**Estado:** RESUELTO.

---

### 11. Sugerencias para “Related synthetic ...”
**Estado:** RESUELTO.

**Evidencia:** el párrafo incluye RadioML, ECGSYN/SEREEGA, LoadGAN, y ejemplo sísmico; alineado con el texto propuesto.

---

### 12. Último párrafo “Table 1 summarizes ...” (subitems)

#### 12.1 Explicar columnas y comentar contenido
**Estado:** RESUELTO.

**Evidencia:** texto explicativo inmediatamente antes de la tabla `tab:related_synthetic_datasets` describe columnas y significado.

#### 12.2 Explicar “difficulty levels”
**Estado:** RESUELTO.

**Evidencia:** se define explícitamente como variación de “downsampling factors and noise intensities”.

#### 12.3 Quitar nota al pie “Configurable” y explicar en texto
**Estado:** RESUELTO.

#### 12.4 Definir LR/HR
**Estado:** RESUELTO.

**Evidencia:**
```tex
... (Low Resolution - High Resolution) ...
```

---

## METHODS

### 1. Rehacer primera oración
**Estado:** RESUELTO.

**Evidencia:**
```tex
The methodology used to generate ... is illustrated in Figure~\ref{fig:generation_process}.
```

---

### 2. Separación entre primer párrafo y subapartado de “Design rationale ...”
**Estado:** RESUELTO.

---

### 3. Rehacer primera oración (y párrafo) de “Design rationale inspired by real signals”
**Estado:** RESUELTO.

**Evidencia:** aparece el texto largo propuesto con (i)-(iv) y cierre sobre “benchmarking rather than match a specific domain distribution”.

---

### 4. Añadir párrafo amplio explicando Figura 2 + subitems

#### 4.1 Etiquetas A), B), C), D)
**Estado:** RESUELTO.

**Evidencia:**
```tex
... four subfigures labeled A--D ...
```

#### 4.2 Explicar fuentes + referencias
**Estado:** RESUELTO.

**Evidencia:** EEG cita `Karacan2024`; speech cita `Yamagishi2019`.

#### 4.3 Explicar qué ejemplifica cada subfigura
**Estado:** RESUELTO.

#### 4.4 No poner explicación en caption; poner en cuerpo
**Estado:** RESUELTO.

#### 4.5 Unidades en eje horizontal (top-left)
**Estado:** PARCIAL (mitigado por caption; no en la imagen).

**En v14 (dónde):** Methods → Figura `fig:design_rationale_motivations`.

**Evidencia (extracto v14, caption):**
```tex
... For the time-domain waveform panels, the horizontal axis corresponds to sample index (samples) and the vertical axis to signal amplitude (arbitrary units).
```

**Qué falta (si se exige “en la imagen”):** editar/regenerar el PNG para que el subpanel correspondiente incluya unidad explícita en el eje x.

---

### 5. Noise injection: explicar más a fondo
**Estado:** RESUELTO.

**Evidencia:** el paso 7 de la enumeración describe AWGN + sinusoidal bursts, probabilidad, parámetros y registro en metadata; además hay subsección de “Rationale ...” y figura `fig:r1_4_powerline_noise`.

---

### 6. Explicar mejor Figura 3 + subitems
**Estado:** RESUELTO.

**Evidencia:** se incluye explicación A--D de `fig:r1_4_powerline_noise` en texto (no solo caption).

#### 6.1 Etiquetas A), B), C), D)
**Estado:** RESUELTO.

**En v14 (dónde):** Methods → “Noise injection” (discusión de la figura) + `fig:r1_4_powerline_noise`.

**Evidencia:** en el texto se referencia explícitamente paneles A--D.

#### 6.2 Explicar fuentes + referencias
**Estado:** RESUELTO.

**En v14 (dónde):** Methods → “Noise injection” (párrafo de motivación/ejemplos) + citas asociadas.

**Evidencia:** se anclan ejemplos a datasets/artículos citados (p. ej., EEG y audio), y se explicita el rol de cada ejemplo para motivar las configuraciones de ruido.

#### 6.3 Explicar qué ejemplifica cada subfigura
**Estado:** RESUELTO.

**En v14 (dónde):** Methods → “Noise injection” (párrafo explicativo de figura).

**Evidencia:** el texto describe qué patrón/artefacto ilustra cada panel (A--D) y cómo conecta con las decisiones de diseño del ruido (AWGN + burst sinusoidal y sus parámetros).

#### 6.4 No poner explicación en caption; poner en cuerpo
**Estado:** RESUELTO.

**En v14 (dónde):** Methods → “Noise injection”.

**Evidencia:** la explicación principal se da en el cuerpo del texto; el caption queda descriptivo sin cargar la interpretación.

---

### 7. Línea en blanco entre “Rationale ...” y “Sampling units ...”
**Estado:** RESUELTO.

---

### 8. Insertar frase propuesta al final del primer párrafo de “Sampling units ...”
**Estado:** RESUELTO.

**Evidencia:** aparece casi literal la frase sobre interpretación Hz condicionada a $T$ y reescalamiento.

---

### 9. Mejorar Figura 4 (seis subfiguras) + subitems
**Estado:** RESUELTO.

**Evidencia:** texto explica paneles A--F de `fig:r1_5_sampling_units`.

#### 9.1 Etiquetas A), B), C) ...
**Estado:** RESUELTO.

**En v14 (dónde):** Methods → “Sampling units and frequency interpretation” + `fig:r1_5_sampling_units`.

**Evidencia:** el texto hace referencia a paneles A--F.

#### 9.2 Aclarar origen de cada subfigura
**Estado:** RESUELTO.

**En v14 (dónde):** Methods → “Sampling units and frequency interpretation”.

**Evidencia:** se explicita que la figura ilustra ejemplos generados/derivados dentro del propio pipeline (CoSiBD) para mostrar el efecto del muestreo y la interpretación de Hz bajo diferentes $T$.

#### 9.3 Explicar cada subfigura y la idea que transmite
**Estado:** RESUELTO.

**En v14 (dónde):** Methods → “Sampling units and frequency interpretation”.

**Evidencia:** el texto conecta cada panel con el mensaje: (i) misma señal discreta, (ii) distintas interpretaciones físicas en Hz, (iii) consecuencias para “dominant frequency” y comparaciones, y (iv) por qué la validación se formula en términos consistentes.

#### 9.4 No poner explicación en caption; poner en cuerpo
**Estado:** RESUELTO.

**En v14 (dónde):** Methods → “Sampling units and frequency interpretation”.

**Evidencia:** explicación principal está en el texto; caption se mantiene conciso.

---

### 10. Quitar último párrafo repetitivo (“The parameters that govern each step ...”)
**Estado:** RESUELTO.

**Evidencia:** no aparece ese párrafo en v14.

---

## DATA RECORDS

### 1. Rehacer primer párrafo
**Estado:** RESUELTO.

**Evidencia:** primer párrafo de `Data Records` coincide con el objetivo SR + uso en real.

---

### 2. Rehacer explicación de tipos de señales (itemize)
**Estado:** RESUELTO.

**Evidencia:** `High-resolution signals` + `Simple subsampled signals` con formatos y convención Hz.

---

### 3. Rehacer párrafo de reproducibilidad y parámetros
**Estado:** RESUELTO.

**Evidencia:**
```tex
Reproducibility is ensured through documented seeds ...
... including: (1) frequency profile parameters ... (4) noise configurations ...
```

---

### 4. Retocar párrafo de archivos consolidados
**Estado:** RESUELTO.

---

### 5. Quitar párrafo repetitivo “Each signal is stored in three formats ...”
**Estado:** RESUELTO.

**Evidencia:** en v14 se reubica como explicación compacta “Regarding the three formats ...” sin repetir secciones previas.

---

### 6. Añadir párrafo explicando los 3 formatos
**Estado:** RESUELTO.

---

### 7. Mejoras en “Metadata schema and example” + subitems

#### 7.1 Tabla: columna tipo y columna ejemplo
**Estado:** RESUELTO.

#### 7.2 Ajustes de layout (texto no invade columnas)
**Estado:** RESUELTO.

#### 7.3 Explicar tabla y, sobre todo, tipos de etiquetas por segmento
**Estado:** RESUELTO.

**Evidencia:**
```tex
... variation_type list which labels each segment (e.g., ``low'', ``high'', or ``no_change'') ...
```

#### 7.4 Explicar el ejemplo de metadatos
**Estado:** RESUELTO.

#### 7.5 Dibujar serie temporal del ejemplo
**Estado:** RESUELTO.

**Evidencia:** figura `fig:metadata_visualization`.

---

### 8. Eliminar bloque “The following resolutions levels are ...”
**Estado:** RESUELTO.

---

### 9. Añadir subsección “Parameters for signal generation”
**Estado:** RESUELTO.

---

### 10. Rehacer primer párrafo de parámetros
**Estado:** RESUELTO.

---

### 11. Cambiar parte final de explicación de parámetros (diversidad/complexidad)
**Estado:** RESUELTO.

---

### 12. Añadir funcionalidad para generar dataset propio + comando + figura
**Estado:** RESUELTO.

**Evidencia:** subsección `Custom Dataset Generation` + Figura `fig:cli_tool`.

---

### 13. Quitar párrafo “The full dataset is hosted in Zenodo ... structured folders”
**Estado:** RESUELTO.

**En v14 (dónde):** sección `Data Records` (se eliminó el párrafo repetido al final).

**Notas:** la referencia a Zenodo se mantiene donde corresponde (inicio de `Data Records` y `Code availability`).

---

### 14. Explicar más la Tabla 3 + indicar que defaults son los usados en Zenodo
**Estado:** PARCIAL.

**Evidencia:** caption de `tab:Parameter` explica defaults y sampling (incluye “defaults used for the Zenodo release”); además se añadió texto alrededor de la tabla para distinguir parámetros muestreados vs defaults.

**Qué falta:** si se desea una explicación “por parámetro” (narrativa, no solo caption/tabla), aún no está detallada campo por campo.

---

### 15. Añadir columna “Default” a Tabla 3
**Estado:** RESUELTO.

---

### 16. Figuras 5 y 6: títulos de ejes y unidades
**Estado:** PARCIAL (mitigado por caption; no en la imagen).

**En v14 (dónde):** Data Records → Figuras `fig:amplitud` y `fig:simples`.

**Evidencia (extracto v14, captions):**
```tex
... the horizontal axis corresponds to sample index (samples) and the vertical axis to signal amplitude (arbitrary units).
```

**Qué falta (si se exige “en la imagen”):** regenerar las imágenes `graphs/amplitud*.png` y `graphs/simples*.png` con `xlabel/ylabel` y unidades cuando aplique.

---

## TECHNICAL VALIDATION

### 1. Rehacer primer párrafo para reflejar más cosas
**Estado:** RESUELTO.

---

### 2. “Validation Context”: añadir frase sobre defaults (Tabla Parameter)
**Estado:** RESUELTO.

**En v14 (dónde):** Technical Validation → `Validation Context`.

**Evidencia (extracto v14):**
```tex
Unless otherwise stated, signal-generation settings follow the configuration in Table~\ref{tab:Parameter}.
```

---

### 3. Dominant frequency: dar más detalles interpretativos
**Estado:** RESUELTO.

**Evidencia:** párrafo analiza concentración en low-frequency + ocurrencias altas.

---

### 4. Frase final con referencia bibliográfica
**Estado:** RESUELTO.

**Evidencia:** cierre con `\cite{Bengio2013}`.

---

### 5. Forzar Figura 8 antes que 9
**Estado:** PARCIAL.

**Notas:** el orden en el TeX parece coherente, pero LaTeX puede reordenar floats. Si el PDF final invierte el orden, se requiere control adicional (`[H]`, `\FloatBarrier`, o reordenar entornos).

---

### 6. Ampliar explicación “Figure 8 represents examples ...” (ruido)
**Estado:** RESUELTO.

**Evidencia:** se añadió un párrafo en texto que describe cómo el ruido “obscurece progresivamente”.

---

### 7. Añadir conclusión al final de “Spectral Stability ...” + referencia
**Estado:** RESUELTO.

**Evidencia:** se incluye una conclusión sobre aliasing y se cita `Shannon1949`.

---

### 8. “Impact of noise ...”: no salto de línea; punto y seguido
**Estado:** RESUELTO.

**En v14 (dónde):** Technical Validation → `Impact of Noise on Frequency Characteristics`.

**Evidencia (extracto v14):**
```tex
... Figure~\ref{fig:noise_psd} illustrates this effect under the reported settings.
```

---

### 9. Color curve 0.2: “red” → “green”
**Estado:** RESUELTO.

---

### 10. Conclusión de “Impact of noise ...” + referencia
**Estado:** RESUELTO.

**Evidencia:** se añadió párrafo final con interpretación y cita `Bishop2006`.

---

### 11. Aclarar qué son los scaling factors (5x, 10x, ...)
**Estado:** RESUELTO.

**Evidencia:**
```tex
5× (1000→5000), 10× (500→5000), ...
```

---

### 12. Referencia bibliográfica de la arquitectura
**Estado:** RESUELTO.

**Evidencia:** se cita `Kuleshov2017` al introducir TimeSeriesSRNet.

---

### 13. Justificar por qué esa arquitectura
**Estado:** RESUELTO.

**En v14 (dónde):** Technical Validation → `Multi-Scale Super-Resolution Benchmark`.

**Evidencia (extracto v14):**
```tex
We selected this architecture as a simple 1D convolutional encoder--decoder baseline: it captures local temporal structure while providing a deterministic upsampling mechanism, enabling consistent comparisons across scaling factors.
```

---

### 14. Justificar configuración de entrenamiento (MSE, Adam, batch, ...)
**Estado:** RESUELTO.

**En v14 (dónde):** Technical Validation → `Multi-Scale Super-Resolution Benchmark`.

**Evidencia (extracto v14):**
```tex
... using the Adam optimizer (learning rate 0.001) and early stopping. A batch size of 16 was used as a practical compromise between optimization stability and MPS memory constraints.
```

---

### 15. Comentar más la tabla 5 (multiscale)
**Estado:** RESUELTO.

**En v14 (dónde):** subsección `Multi-Scale Super-Resolution Benchmark`.

**Qué se añadió:** interpretación explícita de las métricas (LSD/SCORR) y lectura cualitativa coherente con Figuras de pérdidas/predicciones.

---

### 16. Mover “Figure 11 illustrates ...” más arriba
**Estado:** RESUELTO.

---

### 17. Explicar mejor figura 11
**Estado:** RESUELTO.

**En v14:** se añadió análisis en texto enlazando la dinámica de loss (Figura `fig:multifactor_loss_curves`) con la dificultad creciente por factor.

---

### 18. Explicar mejor figura 12; reducir subfiguras
**Estado:** PARCIAL.

**Qué se resolvió:** explicación adicional en texto sobre el comportamiento cualitativo (suavizado/pérdida de detalles rápidos al aumentar el factor) en relación con `fig:multifactor_predictions`.

**Qué queda opcional:** si el checklist exige estrictamente “menos subfiguras”, habría que rediseñar el arte (no solo el texto).

---

### 19. Reorganizar párrafo (métricas antes que espectrograma)
**Estado:** RESUELTO.

**En v14:** el entorno de métricas (`fig:spectral_metrics`) ahora aparece antes del espectrograma (`fig:spectral_analysis`), alineado con el flujo del texto.

---

### 19 bis. Explicar artifacts del espectrograma
**Estado:** RESUELTO.

**En v14:** se añadió explicación de cómo leer la columna de diferencia espectral y por qué los artefactos se acentúan a factores altos.

---

### 20. Implicación de rango LSD y SCORR alto + referencias
**Estado:** RESUELTO.

**En v14:** se añadió interpretación explícita (LSD como desviación espectral creciente; SCORR alto como preservación de estructura global) con referencia de soporte.

---

### 21. Rehacer último párrafo de conclusión del benchmark
**Estado:** RESUELTO.

**En v14:** se reforzó la conclusión con énfasis en baseline reproducible, aumento sistemático de dificultad y valor como protocolo/benchmark controlado.

---

### 22. Quitar “(optional)” del título “Illustrative Transfer ...”
**Estado:** RESUELTO.

---

### 23–25. Reescrituras de transferencia (párrafos 1–3)
**Estado:** RESUELTO.

**Evidencia:** se describen dominios EEG/VCTK, estrategias Real/Synth/Mixed/Tuned, métrica MAE, y se comentan mejores resultados por dominio.

---

### 26. Añadir párrafo nuevo explicando Figura 15
**Estado:** RESUELTO.

**En v14:** se añadió un párrafo dedicado interpretando cualitativamente `fig:model_comparisons` en relación con la tabla de MAE.

---

### 27. Figura 15: ejes/unidades
**Estado:** PARCIAL (depende del arte final en `images/*.pdf`).

**Acción requerida:** confirmar visualmente si los PDFs `images/eeg_model_comparison_1.pdf` y `images/vctk_model_comparison_5.pdf` incluyen ejes/unidades; si no, regenerarlos.

---

### 28. Rehacer último párrafo (audio completo) + ubicación exacta ejemplos repo
**Estado:** RESUELTO.

**En v14:** se indicó la ruta exacta en el repositorio para ejemplos reconstruidos: `AudioModels/results/audio_samples/`.

---

## USAGE NOTES

### 1. Rehacer párrafo inicial de “Reading the Data”
**Estado:** RESUELTO.

---

### 2. Rehacer párrafo inicial de “Visualizing Signal Pairs”
**Estado:** RESUELTO.

---

### 3. Completar comentarios del código “Training a baseline model”
**Estado:** RESUELTO.

**En v14:** se añadieron comentarios explícitos en el snippet (tensores/shape, dataloaders, encoder/upsampling/decoder, optimizer+loss, bucle de entrenamiento y validación).

---

## Author Contributions

### 1. Cambiar frase de contribución J.A.L.
**Estado:** RESUELTO.

**Pedido:**
- `J. A. L. was responsible for methodology (time series design) and supervision`

**Estado actual v14:**
- `J. A. L. was responsible for methodology (time series design) and supervision.`
