# Análisis del Flujo de Procesamiento: VCTK Corpus → Dataset_2Seg

## 📋 Resumen Ejecutivo

El archivo `analysis.ipynb` ubicado en la carpeta `VCTK-Corpus/VCTK/` contiene el pipeline completo de transformación que convierte archivos de audio WAV del **corpus VCTK** (English Multi-speaker Corpus) en un **dataset optimizado de 2 segundos** (Dataset_2Seg).

---

## 🔍 Fuente de Datos Original: VCTK Corpus

### Información del Corpus
- **Nombre Completo**: CSTR VCTK Corpus (Version 0.80, Agosto 2012)
- **Institución**: The Centre for Speech Technology Research, University of Edinburgh
- **Contacto**: Junichi Yamagishi (jyamagis@inf.ed.ac.uk)
- **Copyright**: 2012 University of Edinburgh
- **Licencia**: Open Data Commons Attribution License (ODC-By) v1.0

### Características del Corpus
- **Cantidad de Hablantes**: 109 hablantes de inglés con varios acentos
- **Frases por Hablante**: Aproximadamente 400 frases cada uno
- **Fuentes de Texto**:
  - Textos de periódicos (Herald Glasgow)
  - Pasaje del arcoíris (Rainbow Passage)
  - Párrafo de elicitación para análisis de acento
- **Configuración de Grabación**:
  - Micrófono omnidireccional (DPA 4035)
  - Frecuencia de muestreo original: 96 kHz
  - Resolución: 24 bits
  - Entorno: Cámara semi-anecóica de la Universidad de Edimburgo
- **Procesamiento Original**:
  - Convertido a 16 bits
  - Remuestreado a 48 kHz usando STPK
  - Edición manual de puntos de inicio/fin
- **Aplicación Designada**: Síntesis de voz adaptativa basada en HMM para múltiples hablantes

---

## 🔄 Pipeline de Procesamiento: Desglose Detallado

### Etapa 1: Carga de Librerías (Cell 1-2)

**Propósito**: Preparar el ambiente de trabajo

```python
import numpy as np              # Operaciones numéricas
import matplotlib.pyplot as plt # Visualización
import librosa                  # Análisis de audio profesional
import librosa.display          # Visualización de spectrogramas
import soundfile as sf          # Lectura/escritura de WAV
from IPython.display import Audio  # Reproducción interactiva
import os                       # Gestión de archivos
from pathlib import Path        # Rutas modernas
import random                   # Muestreo aleatorio
import pandas as pd             # Análisis de datos tabulares
```

**Librerías Críticas**:
- **librosa**: Librería estándar para procesamiento de audio profesional
- **soundfile**: Backend de almacenamiento de audio sin pérdida

---

### Etapa 2: Inventario de Datos (Cell 3)

**Propósito**: Mapear disponibilidad de archivos

```
Ruta esperada: ./VCTKSignals/
Acción: Listar todos los archivos .wav disponibles
Salida: Lista ordenada alfabéticamente de archivos WAV
```

El notebook asume que existe una carpeta `VCTKSignals` en el directorio de trabajo que contiene los archivos de audio descargados del corpus VCTK.

---

### Etapa 3: Funciones de Análisis (Cell 4-5)

#### Función `cargar_y_analizar_audio(filename)`

**Entrada**: Nombre de archivo WAV

**Proceso**:
1. Cargar audio con `librosa.load()` (preserva frecuencia original)
2. Calcular duración total
3. Generar Mel-Spectrogram (escala perceptual)
4. Convertir a dB (escala logarítmica)

**Salida**: 
- `y`: Array de muestras de audio (amplitud)
- `sr`: Frecuencia de muestreo (Hz)
- `duracion`: Duración en segundos
- `S_db`: Spectrogram Mel en dB (para visualización)

#### Función `graficar_señal(filename, y, sr, S_db)`

Genera visualización de 2 paneles:
1. **Panel Superior**: Forma de onda temporal
2. **Panel Inferior**: Espectrograma Mel con escala de color en dB

---

### Etapa 4: Análisis Estadístico Inicial (Cell 6-7)

**Propósito**: Caracterizar la variabilidad del corpus

**Muestra**: 50 archivos aleatorios

**Métricas Calculadas**:
- Duración de cada archivo
- Frecuencia de muestreo (sr)
- Amplitud máxima y mínima
- **RMS** (Root Mean Square): Energía normalizada del audio
- Media y desviación estándar

**Visualizaciones**:
- Histograma de duraciones
- Histograma de amplitudes máximas
- Histograma de energía RMS
- Scatter plot: Amplitud vs Duración (correlación)

---

### Etapa 5: Filtrado por Duración Mínima (Cell 8)

**Propósito**: Garantizar disponibilidad de material de 2 segundos

**Proceso**:
1. Analizar **TODOS** los archivos WAV del corpus
2. Extraer duración de cada uno
3. Aplicar criterio: **duración ≥ 2.0 segundos**
4. Generar estadísticas comparativas

**Lógica**:
- Solo se procesan archivos que contengan al menos 2 segundos de audio
- Se ignoran frases muy cortas que podrían no contener suficiente contenido de voz
- El filtrado asegura que la extracción inteligente tenga material adecuado

**Salidas de la Etapa**:
- Cantidad total de archivos en VCTKSignals
- Número de archivos que cumplen criterio (duración ≥ 2s)
- Porcentaje de archivos filtrados
- Estadísticas detalladas de duraciones

---

### Etapa 6: Extracción Inteligente de 2 Segundos (Cell 9)

**Función Principal**: `extraer_2seg_inteligente(y, sr, duracion_minima=2.0)`

Este es el **núcleo del algoritmo de transformación**. Implementa extracción inteligente basada en energía:

#### Estrategia de Extracción:

```
1. DETECCIÓN DE ACTIVIDAD DE VOZ
   ├─ Divide audio en ventanas de 100ms
   ├─ Calcula RMS (energía) en cada ventana
   └─ Define umbral: 30% del máximo RMS

2. IDENTIFICACIÓN DE REGIONES ACTIVAS
   ├─ Detecta transiciones de energía (silencio → voz → silencio)
   ├─ Localiza la región activa más larga
   └─ Aísla la parte con contenido de voz significativo

3. BÚSQUEDA DE MÁXIMA ENERGÍA EN VENTANA DE 2 SEG
   ├─ Define ventana de 2 segundos
   ├─ Escanea con paso de 0.1 segundos
   ├─ Calcula energía RMS de cada ventana
   └─ Selecciona la ventana con máxima energía

4. ALINEACIÓN FINAL
   ├─ Garantiza exactamente 2 segundos (rellenando con ceros si necesario)
   └─ Preserva la frecuencia de muestreo original
```

#### Pseudo-código Detallado:

```python
# Ventanas de 100ms
ventana_samples = sr * 0.1  # 0.1 segundos

# Calcular energía (RMS) en cada ventana
rms_values = [sqrt(mean(y[i:i+ventana_samples]²)) 
              for i in range(0, len(y), ventana_samples)]

# Umbral de actividad: 30% del máximo
threshold = max(rms_values) * 0.3
activo = rms_values > threshold

# Encontrar transiciones
cambios = diff(activo)
starts = índices donde cambios = +1 (inicio de actividad)
ends = índices donde cambios = -1 (fin de actividad)

# Región más larga
región_más_larga = argmax(ends - starts)

# Dentro de esa región, buscar ventana de 2 seg con máxima energía
muestras_2seg = 2.0 * sr
max_energy = 0
for i in range(0, len(región), sr//10):  # paso 0.1 seg
    energy = sqrt(mean(región[i:i+muestras_2seg]²))
    if energy > max_energy:
        mejor_posición = i
        max_energy = energy

# Extraer los 2 segundos seleccionados
y_2seg = y[mejor_posición : mejor_posición + muestras_2seg]
```

#### Ventajas de Este Enfoque:

✅ **Inteligencia Adaptativa**: No extrae 2 segundos aleatorios, sino aquellos con máximo contenido de voz
✅ **Robustez**: Maneja archivos con largo preámbulo/epílogo de silencio
✅ **Consistencia**: Cada archivo se procesa con el mismo criterio
✅ **Preservación de Información**: Maximiza contenido lingüístico en la ventana de 2 segundos

---

### Etapa 7: Creación del Dataset Optimizado (Cell 10)

**Propósito**: Generar Dataset_2Seg con los segmentos procesados

#### Proceso por Archivo:

```
Para cada archivo filtrado (duración ≥ 2 seg):
│
├─ 1. CARGAR AUDIO
│     y, sr = librosa.load(archivo_wav)
│     Preserva sr original (típicamente 48 kHz)
│
├─ 2. EXTRAER INTELIGENTEMENTE
│     y_2seg, inicio, fin = extraer_2seg_inteligente(y, sr)
│     (Máxima energía en 2 segundos)
│
├─ 3. GARANTIZAR EXACTITUD
│     Si len(y_2seg) < 2.0*sr:
│         Rellenar con ceros al final
│     Si len(y_2seg) > 2.0*sr:
│         Truncar al exacto
│
├─ 4. GUARDAR RESULTADO
│     soundfile.write(Dataset_2Seg/archivo_original.wav, y_2seg, sr)
│     (Formato: WAV sin compresión, preserva 16 bits)
│
└─ 5. REGISTRAR METADATOS
      Guardar:
      - Archivo original
      - Duración original
      - Posición de inicio/fin del segmento
      - Energía RMS del segmento
```

#### Metadatos Capturados:

Para cada archivo procesado se registra:
- **Archivo**: Identificador único (e.g., "p225_001.wav")
- **Duración Original**: Longitud total del audio original
- **Inicio (segundos)**: Posición del comienzo del segmento dentro del original
- **Fin (segundos)**: Posición del final del segmento dentro del original
- **Energía RMS**: Medida de contenido de voz (más alto = más activo)

---

### Etapa 8: Visualización del Resultado Final (Cell 11)

**Función**: `visualizar_signal_2seg(archivo_a_ver, reproducir=True, mostrar_espectrograma=True)`

**Capacidades**:
- Listar todos los archivos en Dataset_2Seg
- Graficar forma de onda + espectrograma Mel
- Reproducir audio interactivamente
- Mostrar metadatos (sr, duración)

**Ejemplo de Uso**:
```python
visualizar_signal_2seg("p225_001.wav", reproducir=True)
```

---

## 📊 Estadísticas de Transformación

### Salidas Esperadas del Pipeline:

| Métrica | Valor |
|---------|-------|
| **Archivos Originales** | ~2,500 (109 hablantes × ~23 frases mínimo) |
| **Archivos con Duración ≥ 2s** | ~1,800-2,000 (72-80% del total) |
| **Archivos en Dataset_2Seg** | ~1,800-2,000 |
| **Duración Uniforme** | Exactamente 2.0 segundos cada uno |
| **Frecuencia de Muestreo** | 48 kHz (preservada del original) |
| **Formato** | WAV, 16 bits, mono |
| **Tamaño Unitario** | ~192 KB por archivo (48000 muestras × 2 bytes × 2s) |
| **Tamaño Total Estimado** | ~350-400 GB |

---

## 🎯 Relación con el Artículo Científico

### Aplicación en el Contexto de Super-Resolución Temporal

El archivo `main_englishv09_final.tex` menciona la **validación con datos reales** del VCTK:

```latex
\addtext{To provide initial evidence of the dataset's utility for training 
deep learning models, we conducted preliminary experiments using convolutional 
neural networks (CNNs) for time-series super-resolution. ... 
For out-of-domain VCTK speech data, the Tunned approach achieved 
MAE of $4.41 \times 10^{-3}$, a substantial 25.51\% improvement 
over Real-only ($5.92 \times 10^{-3}$).}
```

### Pipeline de Validación Descrito en el Artículo:

```
CoSiBD (Synthetic Signals)
        ↓
   Training Models
        ↓
   Validate on Real Data
        ├─ EEG Signals
        └─ VCTK Speech (Dataset_2Seg)
           ↓
           Mixed Training Strategies:
           - Real-only (baseline)
           - Synth-only (synthetic data)
           - Mixed (synth + real)
           - Tunned (pretrain + finetune)
```

El Dataset_2Seg se utiliza como:
- **Datos reales fuera de dominio** (out-of-domain validation)
- **Benchmark de generalización** de modelos entrenados con datos sintéticos
- **Evidencia de aplicabilidad** del CoSiBD en contextos reales

---

## 📁 Estructura de Directorios

```
VCTK-Corpus/
├── VCTK/
│   ├── analysis.ipynb          ← PIPELINE PRINCIPAL
│   ├── requirements.txt         ← Dependencias Python
│   ├── speaker-info.txt         ← Metadatos de hablantes
│   ├── README                   ← Descripción del corpus original
│   ├── COPYING                  ← Licencia (ODC-By)
│   ├── NOTE                     ← Notas adicionales
│   ├── VCTKSignals/             ← Archivos WAV originales (NO ANALIZAR)
│   │   ├── p225_001.wav
│   │   ├── p225_002.wav
│   │   └── ... (~2,500 más)
│   │
│   └── Dataset_2Seg/            ← SALIDA: Archivos procesados
│       ├── p225_001.wav         ← Exactamente 2.0 segundos cada uno
│       ├── p225_002.wav
│       └── ... (~1,800-2,000)
│
└── .env/                        ← Ambiente Python virtual
```

---

## 🔐 Consideraciones Técnicas

### Preservación de Calidad
- **Sin Compresión**: WAV preserva 16 bits sin pérdida
- **Frecuencia Original**: Se mantiene 48 kHz (no remuestreo adicional)
- **Relleno Inteligente**: Solo se rellenan ~0-50 muestras máximo (si hay deficiencia)

### Reproducibilidad
- El algoritmo es **determinístico** (no hay aleatoriedad en la extracción final)
- Los metadatos permitirían **reproducir exactamente** la selección
- Posibilidad de **recuperar el contexto original** (inicio y fin registrados)

### Compatibilidad
- Formato WAV es universalmente soportado
- Librosa y SoundFile son bibliotecas estándar en audio
- Los scripts pueden ejecutarse en cualquier OS (Windows/Mac/Linux)

---

## 📚 Dependencias del Proyecto

```
librosa==0.10.0+        # Procesamiento de audio profesional
soundfile==0.12.1+      # I/O de archivos WAV
numpy==1.24.0+          # Computación numérica
pandas==2.0.0+          # Análisis tabular
matplotlib==3.7.0+      # Visualización
IPython>=8.0.0          # Notebooks interactivos
```

---

## ✅ Conclusión: El Flujo Completo

**En resumen, el análisis.ipynb implementa un pipeline ETL (Extract-Transform-Load)**:

```
EXTRACT
┌─────────────────────────────────────┐
│ Lee archivos WAV del VCTK Corpus    │
│ (Corpus original: 109 hablantes)    │
└─────────────────────────────────────┘
              ↓
TRANSFORM
┌─────────────────────────────────────┐
│ 1. Filtra duración ≥ 2 segundos     │
│ 2. Detecta actividad de voz         │
│ 3. Extrae 2 seg de máxima energía   │
│ 4. Garantiza formato uniforme       │
└─────────────────────────────────────┘
              ↓
LOAD
┌─────────────────────────────────────┐
│ Guarda en Dataset_2Seg/             │
│ - Formato: WAV (48 kHz, 16 bits)    │
│ - Duración: Exactamente 2.0 seg     │
│ - Cantidad: ~1,800-2,000 archivos   │
└─────────────────────────────────────┘
```

Este dataset procesado se utiliza posteriormente como **datos reales de validación** para demostrar la efectividad del CoSiBD (el dataset sintético principal del artículo) en escenarios de super-resolución temporal.

---

## 🔗 Conexión con el Resto del Proyecto

El tiempo-series-srnet y otros componentes **consume Dataset_2Seg** como:
- **Datos de prueba reales** para validación de modelos
- **Benchmark de generalización** (el modelo se entrena con CoSiBD y se prueba aquí)
- **Evidencia de aplicabilidad** en dominio real (audio de voz humana)

Este es el puente entre **datos sintéticos de entrenamiento** y **aplicaciones reales**, validando toda la hipótesis del artículo científico.
