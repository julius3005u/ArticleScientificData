# Correcciones en SignalBuilderC y SignalBuilderCLI - Amplitudes y Splines

## 📋 Resumen de Cambios

Se han corregido problemas críticos en la generación de transiciones de amplitud con interpoladores splines en ambos módulos (SignalBuilderC y SignalBuilderCLI).

### Problema Principal
Las transiciones de amplitud mostraban valores de tensión muy altos frecuentemente, cuando deberían ser más suaves y menos frecuentes.

---

## 🔧 Cambios Implementados

### SignalBuilderC (`amplitude_envelopes.py`)

| Parámetro | Antes | Después | Mejora |
|-----------|-------|---------|--------|
| **Rango de amplitud** | ±(3-15) | ±(1-8) | Picos más controlados |
| **Valores de tau** | {1,3,5,8,10,12,15,20} | [0.5, 2.5] uniform | Transiciones suaves, no agresivas |
| **Spline suave (tension)** | 30% | **50%** | Mejor balance variedad |
| **Step function (bruska)** | 70% | **50%** | Better distribution |
| **Max amplitude promedio** | ~8-15 | **~1.89** | **75% reducción** |

**Cambios de código:**
```python
# ANTES
amplitude = (2 * rng.random() - 1.0) * rng.integers(3, 16)
tau = float(rng.choice([1, 3, 5, 8, 10, 12, 15, 20]))
use_tension = rng.choice([True, False], p=[0.3, 0.7])

# AHORA
amplitude = (2 * rng.random() - 1.0) * rng.integers(1, 9)
tau = float(rng.uniform(0.5, 2.5))
use_tension = rng.choice([True, False], p=[0.5, 0.5])
```

### SignalBuilderCLI (`amplitude_envelopes.py`)

Actualizado con parámetros mejorados y flexibles:

```python
def generate_random_amplitude_envelope(
    t: np.ndarray, 
    rng: np.random.Generator = None,
    p_tension_spline: float = 0.5,          # ↑ De 0.3 a 0.5
    tau_amp_min: float = 0.5,               # ↓ De 1 a 0.5
    tau_amp_max: float = 2.5,               # ↓ De 20 a 2.5
    amp_min: int = 1,                       # ↓ De 3 a 1
    amp_max: int = 8,                       # ↓ De 15 a 8
):
```

**Ventaja:** Ahora puedes sobrescribir parámetros si necesitas ajustes adicionales:

```python
# Ejemplo: usar valores más conservadores
envelope, knots, values, tau, type = generate_random_amplitude_envelope(
    t,
    rng=rng,
    p_tension_spline=0.6,      # 60% suave, 40% bruska
    tau_amp_min=0.3,           # Aún más suave
    tau_amp_max=1.5,           # Límite más bajo
)
```

---

## ✅ Validación de Cambios

Se ejecutó análisis en 10 envelopes generadas:

```
Envelope  1: Type=zero_order | min=1.31  | max=3.25  | range=1.93
Envelope  2: Type=tension    | min=0.47  | max=0.56  | range=0.09
Envelope  3: Type=tension    | min=0.75  | max=0.84  | range=0.09
Envelope  4: Type=tension    | min=2.96  | max=5.34  | range=2.38
Envelope  5: Type=tension    | min=1.18  | max=2.95  | range=1.77
Envelope  6: Type=tension    | min=0.10  | max=0.14  | range=0.04
Envelope  7: Type=zero_order | min=1.22  | max=2.19  | range=0.97
Envelope  8: Type=zero_order | min=0.42  | max=0.56  | range=0.13
Envelope  9: Type=tension    | min=1.04  | max=2.63  | range=1.59
Envelope 10: Type=zero_order | min=0.35  | max=0.46  | range=0.10

Mean max value:         1.89 ✓
Mean min value:         0.98
Mean range:             0.91
Tension splines:        6/10 ✓
Step functions:         4/10 ✓
Mean tau (tension):     1.16 (within [0.5, 2.5]) ✓
```

**Interpretación:**
- ✓ Máximos promedio muy reducido (1.89 vs 8-15 antes)
- ✓ Distribución ~50% tension / 50% step
- ✓ Valores de tau bien controlados en rango suave

---

## 🧪 Script de Validación

Para reproducir el análisis o validar futuros cambios:

```bash
cd /path/to/ArticleScientificData
python test_amplitude_fix.py
```

Genera: `amplitude_analysis.png` con gráficos de distribuciones

---

## 🎯 Impacto en Señales Generadas

### Antes (Problema)
- Picos de amplitud: 8-15 muy frecuentes
- Transiciones oscilantes con tau agresivo
- 30% splines suaves, 70% bruscas

### Después (Solución)
- Picos de amplitud: ~1-5 naturales ✓
- Transiciones suaves con tau controlado ✓
- 50% splines suaves, 50% bruscas ✓
- **Resultado:** Señales más realistas sin fluctuaciones artificiales

---

## 📝 Próximos Pasos (Opcional)

### Si necesitas más suavidad:
```python
# En SignalBuilderC/amplitude_envelopes.py
tau = float(rng.uniform(0.3, 1.5))  # Aún más conservador
```

### Si necesitas más variedad:
```python
# En SignalBuilderCLI (cuando llames la función)
envelope, knots, values, tau, type = generate_random_amplitude_envelope(
    t, rng=rng,
    p_tension_spline=0.7,      # 70% transiciones suaves
    tau_amp_min=0.2,           # Ultra-suave
    tau_amp_max=3.0,           # Pero permite algo más
)
```

---

## 📂 Archivos Modificados

1. **`SignalBuilderC/amplitude_envelopes.py`**
   - Parámetros hardcoded mejorados
   - `generate_random_amplitude_envelope()`

2. **`SignalBuilderCLI/amplitude_envelopes.py`**
   - Parámetros flexibles y mejores defaults
   - `generate_random_amplitude_envelope()` con argumentos opcionales

3. **`test_amplitude_fix.py`** (nuevo)
   - Script de validación
   - Genera análisis estadístico y visualización

---

## 🔄 Regeneración de Datasets

Después de estos cambios, si quieres regenerar datasets existentes con los nuevos parámetros:

**SignalBuilderC:**
```bash
cd SignalBuilderC
python -m signal_generator  # O tu script de generación
```

**SignalBuilderCLI:**
```bash
cd SignalBuilderCLI
python generate_signals_cli.py --count 5000  # O tus parámetros
```

Las nuevas señales tendrán transiciones más naturales y valores de amplitud controlados.
