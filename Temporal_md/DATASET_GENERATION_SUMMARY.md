# ✅ Base de Datos de Señales - Generación Correcta

## 📊 Estructura Final

### Archivos de Señales (Arrays consolidados)

| Archivo | Shape | Muestras | Descripción |
|---------|-------|----------|-------------|
| `signals_high_resolution_5000.npz` | (2500, 5000) | 5000 | Resolución original |
| `signals_subsampled_simple_150.npz` | (2500, 150) | 150 | Submuestreada 1/33.33 |
| `signals_subsampled_simple_250.npz` | (2500, 250) | 250 | Submuestreada 1/20 |
| `signals_subsampled_simple_500.npz` | (2500, 500) | 500 | Submuestreada 1/10 |
| `signals_subsampled_simple_1000.npz` | (2500, 1000) | 1000 | Submuestreada 1/5 |

### Metadatos Consolidados

📄 **`signals_metadata_consolidated_2500.json`** (8.8 MB)
- UN ÚNICO archivo JSON
- 2500 entradas (una por señal)
- Referencias a todos los archivos de submuestreos
- Parámetros de amplitud optimizados
- Información temporal y frecuencial

---

## 🔧 Parámetros Técnicos

### Dominio Temporal
- **Intervalo:** 0 a 4π
- **Valor exacto:** 0 a 12.566370614359172
- **Propósito:** Aplicación de fórmulas científicas

### Submuestreo
- **Método:** Simple (decimación)
- **NO filtrado:** Preserva información original sin distorsión
- **Objetivo:** Reconstrucción fiel de la señal

### Amplitud Optimizada
- **Tau range:** [0.5, 2.5] (no {1,3,5,8,10,12,15,20})
- **Amplitud:** ±[1, 8] (no ±[3, 15])
- **Balance de splines:** 50% tension / 50% step (no 30/70)
- **Mejora:** 52.6% reducción en picos

---

## 📋 Cómo Usar

### Cargar datos de alta resolución
```python
import numpy as np
import json

# Cargar señales
data_hr = np.load('signals_high_resolution_5000.npz')
signals_5000 = data_hr['signals']  # Shape: (2500, 5000)
t_high = data_hr['t']              # Time axis

# Cargar metadatos
with open('signals_metadata_consolidated_2500.json', 'r') as f:
    metadata = json.load(f)

# Acceder a una señal
signal_1 = signals_5000[0]  # Primera señal
signal_meta = metadata['signals'][0]
print(f"Tau amplitud: {signal_meta['amplitude_parameters']['tau_amplitude']}")
print(f"Subversiones: {signal_meta['subsampled_versions'].keys()}")
```

### Cargar submuestreo específico
```python
# Cargar submuestreo de 250 muestras
data_250 = np.load('signals_subsampled_simple_250.npz')
signals_250 = data_250['signals']  # Shape: (2500, 250)
t_250 = data_250['t']              # Time axis correspondiente

# Acceder a la i-ésima señal submuestreada
signal_i_250 = signals_250[i]  # i = 0 a 2499
```

---

## ✅ Validación

- ✓ 2500 señales generadas
- ✓ Rango temporal: 0 a 4π
- ✓ 4 versiones submuestreadas (150, 250, 500, 1000)
- ✓ Método de submuestreo: SIMPLE (sin filtros)
- ✓ Metadatos consolidados en UN archivo JSON
- ✓ Parámetros de amplitud optimizados

---

## ⚠️ Importante

**NO usar** `signals_subsampled_filtered_*.npz`
- Estos tienen artefactos de filtrado
- Para reconstrucción fiel, usar SOLO las versiones "simple"

---

**Fecha de generación:** 14 de enero de 2026
**Estado:** ✅ Completado correctamente
