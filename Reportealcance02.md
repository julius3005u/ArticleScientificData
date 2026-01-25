# Reporte de Alineación con Scope de *Scientific Data* (Revisión Editorial #02)

**Rol:** Editor / Revisor (Scientifc Data) - Enfoque estricto en el "Data Descriptor".  
**Documento Auditado:** `main_englishv10_final.tex`  
**Fecha:** 25 de Enero, 2026

---

## 1. Resumen de la Auditoría

El manuscrito v10 ha mejorado significativamente en estructura y metadatos. Sin embargo, persisten secciones (especialmente en **Technical Validation**) que mantienen un tono de "Artículo de Investigación". Un *Data Descriptor* debe responder "¿Qué es el dato?" y "¿Es técnicamente válido?"; no debe responder "¿Qué tan bueno es un algoritmo entrenado con él?".

El documento actual corre el riesgo de ser marcado como **"Out of Scope"** por cruzar la línea hacia la validación de *estrategias de aprendizaje* (Transfer Learning) en lugar de limitarse a la validación de la *utilidad de los datos*.

---

## 2. Análisis Sección por Sección

### A. Abstract
*   **Estado:** Aceptable.
*   **Observación:** La frase "We report a technical validation that includes... a whole study of the application... for time-series resolution" es limítrofe. Sugiere que el "estudio de aplicación" es el aporte principal.
*   **Acción:** Reescribir para enfatizar la *reproducibilidad* y la *cobertura* del dataset, no el estudio de aplicación.

### B. Background & Summary
*   **Estado:** Seguro.
*   **Observación:** La discusión sobre arquitecturas (CNNs, GANs) sirve de contexto y justifica la necesidad de datos masivos. No desplaza el foco.

### C. Methods
*   **Texto Marcado:** *"To address the concern that the dataset is 'too artificial', we derived..."*
*   **Diagnóstico:** **FUERA DE TONO.** Rompe la "cuarta pared" académica. Parece una respuesta a un revisor (Rebuttal) incrustada en el paper. Un Data Descriptor no defiende el dato contra críticas pasadas; describe el dato tal cual es.
*   **Acción:** **Reescribir (Neutral).** Cambiar a: *"To ensure the dataset reflects realistic challenges, simulator degrees of freedom were derived from qualitative observations..."*

### D. Technical Validation (Punto Crítico)
Esta sección contiene los mayores riesgos de rechazo por Scope.

#### Subsección: "Multi-Scale Super-Resolution Benchmark"
*   **Texto Marcado:** Detalle excesivo sobre hiperparámetros de entrenamiento (Adam, weight decay $10^{-5}$, patience, MPS backend).
*   **Diagnóstico:** **Riesgo Moderado.** Demasiado detalle sobre el *modelo* diluye la importancia del *dato*.
*   **Acción:** **Reducir.** Simplificar a "Standard training protocols were used..." y mover detalles finos al repositorio de código o Material Suplementario.

#### Subsección: "Illustrative Transfer Learning Experiments"
*   **Texto Marcado (1):** *"Four training strategies were systematically evaluated: (1) Real-only... (2) Synth-only... (3) Mixed... (4) Tuned..."*
*   **Diagnóstico:** **FUERA DE SCOPE.** Esto es diseño experimental de un paper de Machine Learning, no de un Data Descriptor.
*   **Acción:** **Condensar.** Mencionar simplemente que se realizaron pruebas de entrenamiento mixto para validar la interoperabilidad.

*   **Texto Marcado (2):** *"The results... demonstrate that integrating CoSiBD improves model performance..."*
*   **Texto Marcado (3):** *"Mixed and Tuned strategies consistently outperformed the Real-only baseline."*
*   **Diagnóstico:** **CRÍTICO - FUERA DE SCOPE.** Scientific Data no publica claims de mejora de rendimiento ("outperformed"). Publicar esto implica que los revisores deben evaluar si la mejora es estadísticamente significativa, lo cual no es su trabajo en esta revista.
*   **Acción:** **Reescribir (Utilidad).** Cambiar el foco de "Gana el modelo" a "El dato es útil". Ejemplo: *"The effective convergence of models trained on mixed attributes suggests structural compatibility between CoSiBD and real-world domains."*

---

## 3. Lista de Acciones Requeridas (Scope Compliance)

| Fragmento / Sección | Diagnóstico | Acción Recomendada |
| :--- | :--- | :--- |
| **Methods:** *"To address the concern that the dataset is 'too artificial'..."* | Argumentativo / Defensivo | **Reescribir.** Eliminar la referencia a la "preocupación". Describir el diseño positivamente ("The design incorporates..."). |
| **Methods:** *"Rationale for structured 50/60Hz interference..."* | Argumentativo | **Reescribir.** Cambiar a *"Structured Interference Design"*. Eliminar justificaciones defensivas, solo describir la característica. |
| **Tech Val:** *"All models employed the TimeSeriesSRNet... five-layer encoder-decoder..."* | Foco en Modelo | **Reducir.** Mover detalles de arquitectura a Referencias o Suplementario. El dato es agnóstico al modelo. |
| **Tech Val:** *"Each model was trained using MSE loss, Adam optimizer..."* | Foco en Entrenamiento | **Reducir.** *"Models were trained using standard regression protocols (see Code Availability)."* |
| **Tech Val:** *"Four training strategies were systematically evaluated..."* | Hiper-análisis de ML | **Reescribir.** *"Validation included cross-domain training to assess feature transferability."* |
| **Tech Val:** *"Mixed and Tuned strategies consistently outperformed..."* | Claim de Resultado (Research Paper) | **ELIMINAR / REESCRIBIR.** *"Models incorporating synthetic data achieved convergence on real-world test sets, indicating valid feature extraction."* (Eliminar palabras de comparación de rango como "outperformed", "better"). |
| **Tech Val:** *"Table 6 (MAE comparison)"* | Benchmark Competitivo | **Mover a Suplementario** o simplificar radicalmente para mostrar solo "Convergencia" y no "Ranking". |

---

## 4. Conclusión Editorial

Para garantizar la aceptación, el manuscrito debe **despersonalizarse** (eliminar tono defensivo en Métodos) y **neutralizarse** (eliminar lenguaje de competencia en Technical Validation).

El editor de *Scientific Data* busca verificar:
1.  Que el dato se puede bajar y abrir (Data Records).
2.  Que el dato no es ruido aleatorio (Technical Validation - Frecuencia/Espectro).
3.  Que el dato *sirve* para lo que dice servir (Technical Validation - Transferencia).

Cualquier frase que intente vender el dataset como "el secreto para obtener mejores resultados en ML" es una invitación a que el paper sea derivado a una revista de ML (y rechazado aquí por Scope).

**Recomendación:** Aplicar una "limpieza de tono" final para eliminar comparaciones de rendimiento y justificaciones defensivas.
