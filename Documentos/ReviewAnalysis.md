Temas detectados al dataset por los revisores

+----------------------+----------------------+----------------------+
| Ámbito               | Asunto               | Observaciones        |
+----------------------+----------------------+----------------------+
| Temas generales o    | No se aportan        | Justificación a      |
| conceptuales         | evidencias que       | priori con           |
|                      | sustenten que los    | referencias y        |
|                      | datos sintéticos se  | ejemplos             |
|                      | parezcan a datos     |                      |
|                      | reales de los        | Justificación a      |
|                      | dominios mencionados | posteriores con      |
|                      | (biomedical,         | resultados           |
|                      | industrial, ...).    |                      |
|                      | Sería bueno tener un | Suavizar esos        |
|                      | estudio que compare  | aspectos (decidir    |
|                      | nuestros datos con   | con cuáles nos       |
|                      | datos reales         | quedamos)            |
|                      | analizando aspectos  |                      |
|                      | como variabilidad,   |                      |
|                      | estabilidad,         |                      |
|                      | realismo,            |                      |
|                      | reproducibilidad,    |                      |
|                      | flexibilidad,        |                      |
|                      | complejidad o        |                      |
|                      | propiedades          |                      |
|                      | estadísticas.        |                      |
+----------------------+----------------------+----------------------+
| No se aplican        | ¿Tiene sentido       |                      |
| filtros              | hacerlo?             |                      |
| anti-aliasing antes  |                      |                      |
| del subsampling      | Yo entiendo que no   |                      |
|                      | tiene sentido        |                      |
|                      | transformar la super |                      |
|                      | antes de crear la    |                      |
|                      | sub, porque luego    |                      |
|                      | queremos volver de   |                      |
|                      | la sub a la super    |                      |
|                      | original.            |                      |
+----------------------+----------------------+----------------------+
| Las señales de más   | JULIO-pdte           |                      |
| alta resolución      |                      |                      |
| tienen frecuencias   |                      |                      |
| más altas            |                      |                      |
+----------------------+----------------------+----------------------+
| Se indica que el     | Nosotros decimos que |                      |
| impacto del ruido en | hay un impacto del   |                      |
| el espectro de la    | ruido (sinusoidal    |                      |
| señal se basa en una | deterministico) en   |                      |
| posible mala         | el espectro. Él      |                      |
| caracterización del  | critica que es       |                      |
| ruido artificial     | posible debido a la  |                      |
| añadido, que es      | mala caracterización |                      |
| sinusoidal           | del ruido, al no ser |                      |
| determinístico, no   | Gaussiano o de tipo  |                      |
| Gausiano o de tipo   | broadband.           |                      |
| broadband            |                      |                      |
|                      | JULIO-pdte           |                      |
+----------------------+----------------------+----------------------+
| No se compara el     | Revisar si existe    |                      |
| dataset con          | algun bechmark       |                      |
| benchmarks           | concreto             |                      |
| existentes           |                      |                      |
|                      | Entiendo que es una  |                      |
|                      | comparación con      |                      |
|                      | otros datasets       |                      |
|                      | sintéticos           |                      |
|                      |                      |                      |
|                      | Comparar como        |                      |
|                      | reconstruyen señales |                      |
|                      | reales otros         |                      |
|                      | datasets             |                      |
|                      | sinténticos, frente  |                      |
|                      | al nuestro           |                      |
+----------------------+----------------------+----------------------+
| Se usa una semilla   | Creo que se puede    |                      |
| aleatoria para       | defender porque es   |                      |
| generar datos, lo    | una herramienta para |                      |
| que limita la        | generar datos. El    |                      |
| reproducibilidad     | dataset de           |                      |
|                      | referencia puede ser |                      |
|                      | el publicado por     |                      |
|                      | nosotros             |                      |
+----------------------+----------------------+----------------------+
| Específico del paper | Según el editor, hay | Entiendo que es el   |
|                      | datasets citados y   | nuestro propio.      |
|                      | referenciados en el  |                      |
|                      | paper de forma no    |                      |
|                      | correcta.            |                      |
+----------------------+----------------------+----------------------+
| La validación es muy | Se puede adelantar   |                      |
| básica, sin incluir  | algo de la nueva     |                      |
| resultados           | investigación, algún |                      |
| científicos,         | resultado y figuras  |                      |
| particularmente      |                      |                      |
| cuantitativos ni     |                      |                      |
| visuales. Sería      |                      |                      |
| bueno si esto fuera  |                      |                      |
| parte de un proyecto |                      |                      |
| más completo de      |                      |                      |
| reconstrucción de    |                      |                      |
| series temporales.   |                      |                      |
| Particularmente,     |                      |                      |
| dado que en la       |                      |                      |
| motivación de indica |                      |                      |
| el tema de           |                      |                      |
| deep-learning, esos  |                      |                      |
| estudios deberían    |                      |                      |
| usar algún tipo de   |                      |                      |
| red como CNN, RNN o  |                      |                      |
| LSTM.                |                      |                      |
+----------------------+----------------------+----------------------+
| Hay que explicar un  | JULIO                |                      |
| poco con texto       |                      |                      |
| cuando se cite por   |                      |                      |
| primera vez nuestro  |                      |                      |
| trabajo del congreso |                      |                      |
+----------------------+----------------------+----------------------+
| El modelo de ruido   | JULIO                |                      |
| no está documentado  |                      |                      |
+----------------------+----------------------+----------------------+
| El código refleja un | JULIO                |                      |
| modelo de ruido de   |                      |                      |
| tipo sinusoidal      |                      |                      |
| "single-tone" que no |                      |                      |
| está justificado     |                      |                      |
+----------------------+----------------------+----------------------+
| No se discute acerca | JULIO                |                      |
| de la frecuencia de  |                      |                      |
| muestreo             |                      |                      |
+----------------------+----------------------+----------------------+
| Se omiten las        | JULIO                |                      |
| unidades en los ejes |                      |                      |
| y las etiquetas. Se  |                      |                      |
| deberían incluir     |                      |                      |
| leyendas             |                      |                      |
| interpretables en    |                      |                      |
| las figuras.         |                      |                      |
+----------------------+----------------------+----------------------+
| La sección de        | Revisar para         |                      |
| "Technical           | intentar localizar   |                      |
| Validation" está     |                      |                      |
| llena de frases      | JULIO                |                      |
| vagas y tecnicismos  |                      |                      |
| sin una definición   |                      |                      |
| clara ni un análisis |                      |                      |
| sustancioso.         |                      |                      |
| Particularmente, las |                      |                      |
| últimas frases de la |                      |                      |
| mayoría de los       |                      |                      |
| párrafos hacer       |                      |                      |
| afirmaciones vagas   |                      |                      |
| no soportadas de     |                      |                      |
| forma cuantitativa o |                      |                      |
| con referencias.     |                      |                      |
+----------------------+----------------------+----------------------+
| Las decisiones clave | JULIO                |                      |
| de modelado no están |                      |                      |
| documentadas, sino   |                      |                      |
| que se requiere      |                      |                      |
| revisar el código    |                      |                      |
| para intentar        |                      |                      |
| entenderlas          |                      |                      |
+----------------------+----------------------+----------------------+
| No se definen        | JULIO                |                      |
| términos como        |                      |                      |
| "samples", "points"  |                      |                      |
| o "signals". Además, |                      |                      |
| parece que se usan   |                      |                      |
| "samples" y          |                      |                      |
| "signals" como       |                      |                      |
| sinónimos, lo cual   |                      |                      |
| contradice la        |                      |                      |
| nomenclatura         |                      |                      |
| estándar en el campo |                      |                      |
| de procesamiento de  |                      |                      |
| señales              |                      |                      |
+----------------------+----------------------+----------------------+
| No está bien         | JULIO                |                      |
| justificado porqué   |                      |                      |
| las señales          |                      |                      |
| propuestas son       |                      |                      |
| relevantes en        |                      |                      |
| aplicaciones del     |                      |                      |
| mundo real           |                      |                      |
| (Motivación)         |                      |                      |
+----------------------+----------------------+----------------------+
| La figura 1 contiene | JULIO                |                      |
| demasiado texto. Hay |                      |                      |
| que sacarlo de la    |                      |                      |
| figura y explicarlo  |                      |                      |
| en el cuerpo del     |                      |                      |
| artículo             |                      |                      |
+----------------------+----------------------+----------------------+
| El código            | JULIO                |                      |
| proporcionado en el  |                      |                      |
| paper es muy básico, |                      |                      |
| solo sirviendo para  |                      |                      |
| leer y dibujar       |                      |                      |
| datos, esperándose   |                      |                      |
| algo más en un       |                      |                      |
| artículo científico. |                      |                      |
+----------------------+----------------------+----------------------+
| No se explica la     | JULIO                |                      |
| semilla aleatoria y  |                      |                      |
| porque se elige así  |                      |                      |
| para lograr          |                      |                      |
| variabilidad         |                      |                      |
+----------------------+----------------------+----------------------+
| Hay erratas e        | Lo puedo revisar yo  |                      |
| inconsistencias por  | todo al final        |                      |
| el paper, habiendo   |                      |                      |
| párrafos que         |                      |                      |
| explican varias      |                      |                      |
| veces lo mismo en    |                      |                      |
| relación al          |                      |                      |
| propósito del        |                      |                      |
| dataset y su         |                      |                      |
| composición          |                      |                      |
+----------------------+----------------------+----------------------+
| Alcance y novedad    | El revisor indica    | Plantear explícitamente|
| del dataset como     | que, como Data       | que este Data        |
| contribución         | Descriptor aislado,  | Descriptor se        |
| independiente        | la aportación es     | complementará con    |
|                      | limitada y que sería | validación más       |
|                      | más fuerte como      | profunda (modelos    |
|                      | parte de un trabajo  | y comparación con    |
|                      | metodológico más     | datos reales), y     |
|                      | amplio.              | reforzar la          |
|                      |                      | motivación y el      |
|                      |                      | posicionamiento del  |
|                      |                      | dataset frente a     |
|                      |                      | otros trabajos       |
|                      |                      | existentes.          |
----------------------+----------------------+----------------------+
| Específico de los    | Los datos se         | Estoy de acuerdo     |
| datos                | proporcionan como    |                      |
|                      | arrays de numpy      | JULIO                |
|                      | (Python), y sería    |                      |
|                      | mejor un formato más |                      |
|                      | estándar, tipo CSV o |                      |
|                      | JSON                 |                      |
+----------------------+----------------------+----------------------+
| Las señales carecen  | Chungo, llevaría     |                      |
| de metadatos o       | tiempo               |                      |
| anotaciones que      |                      |                      |
| describan los        | JULIO                |                      |
| diferentes           |                      |                      |
| segmentos, lo cual   |                      |                      |
| limita su uso en     |                      |                      |
| otros potenciales    |                      |                      |
| dominios             |                      |                      |
+----------------------+----------------------+----------------------+
| Se incluye un        | Si es así, yo estoy  |                      |
| conjunto de          | de acuerdo           |                      |
| validación           |                      |                      |
| predefinido sin      | JULIO                |                      |
| documentar. Además,  |                      |                      |
| ello resulta una     |                      |                      |
| imposición           |                      |                      |
| arbitraria que       |                      |                      |
| limita su            |                      |                      |
| flexibilidad         |                      |                      |
+----------------------+----------------------+----------------------+
| Específico del       | Se debería hacer un  | JULIO                |
| código               | esfuerzo en          |                      |
|                      | clarificar la        |                      |
|                      | documentación e      |                      |
|                      | intentar hacerlo más |                      |
|                      | limpio               |                      |
+----------------------+----------------------+----------------------+
| Resultados           | Los revisores        | Incluir en la        |
| cuantitativos y      | señalan que se       | revisión alguna      |
| experimentales       | mencionan métricas   | tabla y/o figuras    |
|                      | como RMSE, MAE,      | con resultados       |
|                      | PSNR y SSIM pero no  | cuantitativos        |
|                      | se presentan valores | (por ejemplo,        |
|                      | numéricos ni         | comparando distintos |
|                      | comparaciones con    | modelos baseline o   |
|                      | métodos base o       | distintas            |
|                      | datos reales.        | configuraciones) y,  |
|                      |                      | si es posible, algún |
|                      |                      | experimento simple   |
|                      |                      | que conecte el       |
|                      |                      | dataset con modelos  |
|                      |                      | de deep learning.    |
----------------------+----------------------+----------------------+
