# Análisis Detallado de Revisión - CoSiBD Paper
## Scientific Data - SDATA-25-02814

---

## COMENTARIOS DEL EDITOR

### Editor Comment 1: Formato de datos estandarizado
**Solicitado:** "Please also share the data in a more standardised format other than numpy arrays - consider csv/json (whatever is standard for the field)."

**Estado en el paper actual:** ✅ **RESUELTO**
- Líneas 153-162: Se menciona que los datos están en tres formatos: .npz, .txt, y .json
- Línea 173-178: Se describe explícitamente que cada señal está disponible en tres formatos
- Líneas 296-297: Confirma la distribución como archivos .txt consolidados

**Evidencia:**
> "Each signal is provided in three formats: (1) NumPy compressed format (.npz)... (2) plain-text format (.txt)... and (3) JSON format (.json)"

---

### Editor Comment 2: Citaciones de datos
**Solicitado:** "Please add data citations for the datasets on repositories to the reference list... Please add the reference numbers to wherever the datasets are mentioned in the text - the main position should be the first part of the Data Records"

**Estado en el paper actual:** ✅ **RESUELTO**
- Línea 214-215: Se menciona Zenodo con referencia [25]
- Línea 355: Referencia al dataset en Zenodo con DOI
- Referencia 25 (línea 401): "Ibarra-Fiallo, J., Lara, J. A. & Agudelo Moreno, D. Cosibd, 10.5281/zenodo.18295713 (2025). Version v2. Dataset."

**Evidencia:**
> "The full dataset is publicly available on Zenodo²⁵"

---

## REVISOR #1

### R1.1: Calidad de los datos - Falta de validación con datos reales
**Comentario:** "The authors show no evidence that the proposed synthetic signal model generates time series that resemble at least some real-world time series from any of the referenced domains."

**Estado en el paper actual:** ⚠️ **PARCIALMENTE RESUELTO**
- Líneas 88-93: Se describe la inspiración en señales fisiológicas y de voz
- Figura 2: Muestra características motivadas por señales reales
- **FALTA:** No hay comparación cuantitativa con datos reales

**Recomendación:** Agregar una sección breve o párrafo que:
1. Explique explícitamente que este es un dataset sintético de propósito general
2. Mencione que la validación con datos específicos de dominio está fuera del alcance
3. Sugiera esto como trabajo futuro

---

### R1.2: Modelo de ruido no documentado
**Comentario:** "The noise model is undocumented, and provided code shows a single-tone sinusoid noise model that is not justified"

**Estado en el paper actual:** ✅ **RESUELTO**
- Líneas 113-115: Describe dos tipos de ruido (Gaussiano y sinusoidal estructurado)
- Líneas 116-123: Nueva sección completa justificando el ruido de 50/60 Hz
- Figura 3: Ilustra visualmente la motivación del ruido estructurado
- Líneas 118-122: Explica la interpretación física del ruido

**Evidencia:**
> "To reflect this common acquisition artifact, CoSiBD includes an optional structured sinusoidal component in addition to Gaussian noise."

---

### R1.3: Frecuencia de muestreo y anti-aliasing
**Comentario:** "Most concerningly, the dataset fails to define or discuss sampling frequency, does not apply anti-aliasing filters before subsampling"

**Estado en el paper actual:** ✅ **MAYORMENTE RESUELTO**
- Líneas 126-135: Nueva sección extensa sobre "Sampling units and frequency interpretation"
- Figura 4: Ilustra la convención de muestreo y unidades
- Líneas 108-111: Explica el método de submuestreo (decimación uniforme)
- Líneas 129-132: Define la convención de frecuencia de muestreo

**NOTA IMPORTANTE:** El paper ahora documenta claramente que:
1. Usa decimación uniforme simple (sin anti-aliasing)
2. Esto es una decisión de diseño explícita
3. Las frecuencias se reportan bajo una convención ilustrativa

**Evidencia:**
> "In CoSiBD, paired low-resolution sequences are obtained via simple uniform decimation (uniform subsampling) of the high-resolution signals. The low-resolution observation is formed by subsampling the original sequence without pre-filtering."

---

### R1.4: Unidades en ejes de tiempo
**Comentario:** "omits units on time axes"

**Estado en el paper actual:** ✅ **RESUELTO**
- Todas las figuras relevantes ahora tienen ejes etiquetados
- Figura 4: Explica explícitamente la convención de unidades
- Líneas 126-135: Sección completa sobre unidades y convenciones

---

### R1.5: Validación técnica superficial
**Comentario:** "Although the authors include a section titled 'Technical Validation', the analyses presented are superficial, qualitative, and in some cases conceptually flawed"

**Estado en el paper actual:** ⚠️ **MEJORADO PERO AÚN LIMITADO**
- Sección de validación mejorada con más detalles
- Líneas 221-230: Añade contexto sobre parámetros experimentales
- Figuras 7, 8, 9, 10: Análisis cuantitativos con estadísticas
- Tabla 3: Estadísticas resumidas de frecuencias dominantes

**LIMITACIONES RESTANTES:**
- El revisor tiene razón: la validación sigue siendo principalmente descriptiva
- No hay benchmarks contra otros datasets sintéticos
- No hay validación con modelos SR reales

**Recomendación:** Considerar agregar:
1. Un párrafo reconociendo las limitaciones del enfoque de validación
2. Mencionar que la validación se enfoca en caracterización del dataset, no en su utilidad definitiva
3. Esto es consistente con otros datasets sintéticos en la literatura

---

### R1.6: Anotaciones de señales con metadatos
**Comentario:** "With respect to the metadata, given that the signals consist of multiple segments with changing frequency content, it would be desirable to have annotations of the signals themselves"

**Estado en el paper actual:** ✅ **RESUELTO**
- Líneas 155-158: Describe metadatos por señal incluyendo change-points, etiquetas de segmento
- Tabla 1: Lista completa de campos de metadatos incluyendo `base_points`, `high_freq_points`, `variation_type`
- Líneas 180-200: Ejemplo de metadata mostrando estos campos

**Evidencia:**
> "Per-signal generative metadata—including frequency profiles with explicit change-points (base_points, high_freq_points), segment labels (variation_type)..."

---

### R1.7: Conjuntos de validación predefinidos
**Comentario:** "The dataset includes predefined validation sets, but their selection criteria are undocumented. Predefining validation sets imposes arbitrary usage assumptions and limits flexibility."

**Estado en el paper actual:** ✅ **RESUELTO**
- Líneas 286-292: Ahora NO hay splits predefinidos
- Se explica explícitamente que los usuarios deben crear sus propias particiones

**Evidencia:**
> "The dataset is distributed as a single, unified collection without a predefined train/validation/test split. Users can create partitions appropriate to their objectives"

---

### R1.8: Cobertura y completitud
**Comentario:** "There is no indication that the dataset captures the diversity, complexity, or statistical properties of real-world signals from any of the domains the manuscript mentions."

**Estado en el paper actual:** ⚠️ **PARCIALMENTE ABORDADO**
- El paper ahora es más claro sobre ser un dataset sintético de propósito general
- Se enfoca en características estructurales, no en replicar dominios específicos

**Recomendación:** Similar a R1.1 - aclarar el alcance y propósito

---

### R1.9: Definición de términos
**Comentario:** "The authors use the terms 'samples', 'points' and 'signals' without defining them"

**Estado en el paper actual:** ⚠️ **MEJORADO PERO VERIFICAR**
- El paper usa estos términos más consistentemente
- Línea 126: Define claramente x[n] como secuencias discretas
- **REVISAR:** Asegurar que los términos se usen consistentemente en todo el documento

---

## REVISOR #2

### R2.1: Alcance y motivación
**Comentario:** "The current dataset design focuses mainly on synthetic sinusoidal signals with random frequency and amplitude variations. While technically correct, this approach is limited in its capacity to represent realistic time-series phenomena."

**Estado en el paper actual:** ⚠️ **PARCIALMENTE ABORDADO**
- Líneas 88-93: Mejora la motivación del diseño
- Figura 2: Ilustra propiedades inspiradas en señales reales
- **FALTA:** Comparación explícita con benchmarks existentes

**Recomendación:** Agregar párrafo comparando con datasets existentes (RadioML, ECGSYN, etc.)

---

### R2.2: Resultados experimentales ausentes
**Comentario:** "The manuscript lists evaluation metrics such as RMSE, MAE, PSNR, and SSIM but does not present any numerical results or baseline comparisons."

**Estado en el paper actual:** ❌ **NO RESUELTO**
- No hay resultados experimentales de SR en el paper
- El paper es un Data Descriptor, no un estudio de métodos

**ANÁLISIS:** Esto es apropiado para Scientific Data. Los Data Descriptors describen datasets, no presentan resultados algorítmicos. El revisor puede no estar familiarizado con el formato.

**Recomendación:** Aclarar en el abstract/introducción que este es un Data Descriptor.

---

### R2.3: Figuras sin etiquetas
**Comentario:** "Figures 2 and 3 have no axis labels or units, making it impossible to interpret the plots"

**Estado en el paper actual:** ✅ **RESUELTO**
- Todas las figuras ahora tienen ejes etiquetados
- Figura 4 añadida para explicar convenciones

---

### R2.4: Reproducibilidad - seeds fijas
**Comentario:** "The random number generation in the code does not use fixed seeds, which prevents reproducibility"

**Estado en el paper actual:** ✅ **RESUELTO**
- Líneas 163-166: Documenta seeds únicas por señal (10,000-12,499)
- Tabla 2: Lista seed range
- Línea 208: Cada señal tiene seed único

**Evidencia:**
> "Reproducibility is ensured through documented random seeds: each high-resolution signal is generated using a unique seed (ranging from 10,000 to 12,499)"

---

### R2.5: Errores tipográficos
**Comentario:** "The manuscript contains typos (e.g., frecuency bands in Fig.1, step 7)"

**Estado en el paper actual:** ⚠️ **REVISAR**
- **ACCIÓN REQUERIDA:** Revisar cuidadosamente todas las figuras y texto para errores tipográficos

---

## REVISOR #3

### R3.1: Impacto demostrativo del dataset
**Comentario:** "The study lacks a demonstrative impact of the data. Given the motivation of the data is for use with deep learning methods. Experiments where CNNs, RNNs and LSTMs are trained with simulated data and validated on real-world data would have been more convincing."

**Estado en el paper actual:** ❌ **NO APLICABLE**
- Este es un Data Descriptor, no un estudio algorítmico
- Scientific Data publica descripciones de datasets

**ANÁLISIS:** El revisor solicita algo fuera del alcance de un Data Descriptor. Sin embargo, sería útil clarificar esto.

**Recomendación:** Mencionar en el paper que trabajos futuros usarán el dataset para entrenar modelos.

---

### R3.2: Comparación con señales del mundo real
**Comentario:** "Would be great to see side-by-side comparison of how the objectives of variability, stability, and realism, maintaining reproducibility and flexibility compares to those measured from real-world signals."

**Estado en el paper actual:** ⚠️ **PARCIALMENTE ABORDADO**
- Figura 2 motiva el diseño con propiedades de señales reales
- No hay comparación cuantitativa directa

**Recomendación:** Similar a R1.1 y R2.1 - aclarar alcance

---

## RESUMEN DE ESTADO

### ✅ Completamente Resueltos (9 puntos):
1. Editor: Formatos de datos estandarizados
2. Editor: Citaciones de datos
3. R1.2: Modelo de ruido documentado
4. R1.3: Frecuencia de muestreo y convenciones
5. R1.4: Unidades en ejes
6. R1.6: Metadatos con anotaciones
7. R1.7: Sin splits predefinidos
8. R2.3: Figuras etiquetadas
9. R2.4: Seeds reproducibles

### ⚠️ Parcialmente Resueltos / Necesitan Clarificación (6 puntos):
1. R1.1: Validación con datos reales
2. R1.5: Validación técnica superficial
3. R1.8: Cobertura de dominios
4. R1.9: Definición de términos
5. R2.1: Alcance y motivación
6. R3.2: Comparación con señales reales

### ❌ No Aplicables / Fuera de Alcance (2 puntos):
1. R2.2: Resultados experimentales (apropiado para Data Descriptor)
2. R3.1: Impacto demostrativo (apropiado para Data Descriptor)

### 🔍 Requiere Verificación (1 punto):
1. R2.5: Errores tipográficos

---

## RECOMENDACIONES PRIORITARIAS

### Alta Prioridad:
1. **Revisar todo el documento para errores tipográficos** (especialmente figuras)
2. **Agregar párrafo clarificando alcance**: Este es un dataset sintético de propósito general, no una réplica de señales específicas de dominio
3. **Verificar uso consistente de terminología**: "samples", "signals", "points"

### Media Prioridad:
4. **Mejorar sección de validación**: Agregar párrafo reconociendo que la validación es descriptiva/caracterizadora, no una evaluación de utilidad
5. **Comparación con datasets existentes**: Breve párrafo en Background comparando con RadioML, ECGSYN, LoadGAN, etc.

### Baja Prioridad:
6. **Mencionar trabajos futuros**: Una oración sobre planes de usar el dataset para entrenar modelos SR

---

## VERIFICACIÓN DE GUIDELINES DE SCIENTIFIC DATA

### ✅ Requisitos cumplidos:
- Título sin puntuación, capitalización correcta
- Sin acrónimos en el título (excepto "CoSiBD" en texto)
- Abstract de un párrafo, 150-200 palabras
- Secciones en orden correcto
- Referencias en estilo Nature
- Datos citados en Data Records
- Code Availability section presente
- Figuras en archivos separados (verificar)
- Tablas editables (verificar en .docx)

### ⚠️ Verificar:
- Longitud del abstract (contar palabras)
- Todas las figuras citadas en orden ascendente
- Todas las referencias tienen DOIs donde disponible
- ORCIDs de autores (en el sistema, no en el paper)

