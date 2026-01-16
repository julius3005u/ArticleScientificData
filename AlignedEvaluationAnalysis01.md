A continuación tienes la **Fase 1 de la revisión rigurosa**:
👉 **comprobación directa entre *AnswersToRequirements.txt* y *main_englishv09_final.tex*** para los **ítems de mayor riesgo editorial y científico**.
No asumo buena fe automática: **busco inconsistencias, vacíos y sobre-afirmaciones**.

---

# FASE 1 — VERIFICACIÓN CRUZADA CRÍTICA

## Ítems prioritarios: E2, R1-5, R1-6, R1-3, R2-2

---

## 1️⃣ Editor E2 — *Dataset citation & repository reference*

### Lo que afirmas en AnswersToRequirements

> “A proper DOI reference to the Zenodo repository has been included in the manuscript and references.”

### Lo que **realmente aparece** en `main_englishv09_final.tex`

He revisado:

* sección *Data Records*
* sección *Availability of data and materials*
* archivo `referencias.bib`

**Problemas detectados:**

❌ **NO hay una cita formal tipo “dataset” siguiendo DataCite/Nature**
❌ El DOI **no aparece como referencia bibliográfica normalizada**
❌ En el texto se usa el enlace web de Zenodo, no el **DOI citável**

Ejemplo típico que encontré (resumo):

* “The dataset is available at Zenodo: [https://zenodo.org/records/15138853”](https://zenodo.org/records/15138853”)

👉 **Esto NO cumple E2** según estándares *Scientific Data*.

### Por qué esto es grave

Para *Scientific Data*, los datasets **deben citarse como objetos científicos**, igual que un artículo:

* con referencia numerada,
* con DOI,
* con entrada en la bibliografía.

Un editor puede marcar esto como **“not properly addressed”**, aunque el enlace exista.

### Corrección necesaria (no opcional)

1. **Agregar entrada en `referencias.bib`**, por ejemplo:

```bibtex
@dataset{YourDataset2025,
  author       = {...},
  title        = {...},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.15138853},
}
```

2. **Citarla explícitamente en el texto**, por ejemplo:

> “The dataset is publicly available on Zenodo [XX].”

📌 **Conclusión E2:**
👉 **NO está completamente resuelto**, tu respuesta al editor es **demasiado optimista**.

---

## 2️⃣ R1-5 — *Aliasing & anti-aliasing filters*

### Lo que dices en la respuesta

> “Anti-aliasing filters have been incorporated… both filtered and unfiltered versions are provided.”

### Lo que aparece en el manuscrito

✔️ Sí aparece una descripción del filtro:

* Butterworth
* orden 8
* cutoff = 0.9 × Nyquist

❌ **Pero NO aparece claramente definido cuál versión es la “default”**
❌ NO hay advertencia fuerte sobre el uso incorrecto de la versión sin filtro
❌ NO hay metadatos visibles que impidan confusión

Ejemplo del texto:

> “We provide both filtered and unfiltered low-resolution signals…”

Desde el punto de vista de un revisor:

> *“Entonces el dataset sigue conteniendo aliasing, solo que ustedes lo admiten.”*

### Qué falta para cerrar bien este punto

Debes **reformular explícitamente** algo como:

> “All benchmark and recommended low-resolution signals are anti-aliased by default.
> Unfiltered versions are provided strictly for ablation and educational purposes and are clearly labeled as such.”

Y eso **debe aparecer en el artículo**, no solo en el repositorio.

📌 **Conclusión R1-5:**
👉 Técnicamente correcto, **editorialmente vulnerable**.
👉 Tal como está, **puede volver a ser objetado**.

---

## 3️⃣ R1-6 — *Sampling rate, Hz, and time axis*

### Lo que afirmas en Answers

> “The sampling frequency is approximately 398 Hz.”

### Lo que aparece en el artículo

❌ **NO se declara explícitamente que el dominio [0, 4π] esté en segundos**
❌ Se usa lenguaje de “Hz” sin anclar la unidad temporal
❌ No se justifica por qué 4π representa un tiempo físico

Esto es exactamente el tipo de afirmación que un revisor técnico puede desmontar en una línea:

> *“Hz requires seconds.”*

### Qué deberías hacer (imprescindible)

En el manuscrito debe aparecer **una frase inequívoca**, por ejemplo:

> “We define the time axis in seconds and fix the signal duration to T = 4π s (≈12.57 s), yielding an effective sampling frequency of 5000/T ≈ 398 Hz.”

Sin esto:

* tu respuesta **sobre-interpreta** lo que el texto realmente sostiene.

📌 **Conclusión R1-6:**
👉 **NO está realmente cerrado**.
👉 Riesgo **alto** de nueva objeción.

---

## 4️⃣ R1-3 — *Noise modeling realism*

### Lo que dices

> “Noise types are inspired by realistic acquisition artifacts such as Gaussian noise, powerline interference, and bursts.”

### Lo que aparece en el manuscrito

✔️ Se mencionan los tipos de ruido
❌ **NO se especifica suficientemente**:

* amplitudes relativas,
* duración de bursts,
* distribución de frecuencias,
* relación con el escalamiento temporal (50/60 Hz vs dominio sintético)

Esto deja la afirmación “realistic” **sin sustento cuantitativo**.

### Riesgo claro

Un revisor puede decir:

> *“You claim realism, but parameters are arbitrary.”*

### Qué haría un artículo sólido

* O bajas el lenguaje: “structured noise inspired by…”
* O añades **tabla breve** con parámetros del ruido.

📌 **Conclusión R1-3:**
👉 Parcialmente abordado.
👉 Lenguaje **demasiado fuerte** para el nivel de detalle actual.

---

## 5️⃣ R2-2 — *SCORR, LSD, and performance claims*

### Lo que afirmas

> “SCORR (0.98 ± 0.10)… consistent improvements of 9.64% and 25.51%…”

### Lo que aparece en el artículo

❌ El **±0.10 es matemáticamente problemático**
❌ No se especifica:

* número de corridas,
* intervalos de confianza,
* independencia de datos,
* prueba estadística mínima

Esto es **exactamente** el tipo de punto que provoca una segunda ronda de revisión.

### Estado real

El manuscrito **NO justifica** las palabras:

* “consistent”
* “quantitative evidence validates”

📌 **Conclusión R2-2:**
👉 **No cerrado**.
👉 Riesgo **crítico**.

---

# VEREDICTO HONESTO (como pediste)

👉 Tu **documento de respuestas está mejor escrito que el manuscrito final que lo respalda**.
👉 Varias respuestas **afirman más de lo que el artículo realmente demuestra**.
👉 Un editor técnico cuidadoso **puede detectar esto**.

Esto explica por qué el trabajo volvió a revisión la primera vez.

---


