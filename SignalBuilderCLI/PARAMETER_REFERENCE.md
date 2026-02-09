# 🔧 Quick Reference - Parámetros de Amplitud Spline

## Valores Antiguos (ANTES - Problemáticos)

### SignalBuilderC/amplitude_envelopes.py
```python
# Línea ~24
amplitude = (2 * rng.random() - 1.0) * rng.integers(3, 16)  # ±[3,15]

# Línea ~42
tau = float(rng.choice([1, 3, 5, 8, 10, 12, 15, 20]))

# Línea ~44  
use_tension = rng.choice([True, False], p=[0.3, 0.7])  # 30% suave
```

## Valores Nuevos (DESPUÉS - Optimizados)

### SignalBuilderC/amplitude_envelopes.py
```python
# Línea ~24
amplitude = (2 * rng.random() - 1.0) * rng.integers(1, 9)  # ±[1,8]

# Línea ~42
tau = float(rng.uniform(0.5, 2.5))

# Línea ~44
use_tension = rng.choice([True, False], p=[0.5, 0.5])  # 50% suave
```

---

## Parámetros Personalizables (SignalBuilderCLI)

```python
def generate_random_amplitude_envelope(
    t: np.ndarray,
    rng: np.random.Generator = None,
    
    # PARÁMETROS OPTIMIZADOS (nuevos defaults)
    p_tension_spline: float = 0.5,      # ← 50% suave
    tau_amp_min: float = 0.5,           # ← Min tau
    tau_amp_max: float = 2.5,           # ← Max tau
    amp_min: int = 1,                   # ← Min amplitud
    amp_max: int = 8,                   # ← Max amplitud
):
```

---

## Perfiles de Ajuste Preestablecidos

### Perfil "Suave" (Ultra-conservador)
```python
envelope, knots, values, tau, type = generate_random_amplitude_envelope(
    t, rng=rng,
    p_tension_spline=0.7,      # 70% transiciones suaves
    tau_amp_min=0.3,           # Muy bajo
    tau_amp_max=1.5,           # Bajo
    amp_min=1,
    amp_max=5,                 # Amplitudes pequeñas
)
```

### Perfil "Balanceado" (Actual - Recomendado)
```python
envelope, knots, values, tau, type = generate_random_amplitude_envelope(
    t, rng=rng,
    p_tension_spline=0.5,      # 50/50
    tau_amp_min=0.5,           # Suave
    tau_amp_max=2.5,           # Moderado
    amp_min=1,
    amp_max=8,                 # Natural
)
```

### Perfil "Variado" (Más oscilaciones)
```python
envelope, knots, values, tau, type = generate_random_amplitude_envelope(
    t, rng=rng,
    p_tension_spline=0.3,      # 30% suave, 70% bruska
    tau_amp_min=0.5,
    tau_amp_max=3.5,           # Permite oscilaciones más altas
    amp_min=1,
    amp_max=10,                # Amplitudes más altas
)
```

---

## Comparativa de Resultados

| Perfil | Max Amp | Tau Max | Carácter | Cuándo Usar |
|--------|---------|---------|----------|------------|
| Suave | 1.5 | 1.5 | Muy suave, monótono | Señales simples |
| **Balanceado** | **1.9** | **2.5** | **Natural** | **Recomendado** |
| Variado | 3.0 | 3.5 | Dinámico, oscilante | Complejidad alta |

---

## Verificación Rápida

Después de regenerar, ejecuta:
```bash
python test_amplitude_fix.py
```

Espera ver:
```
Mean max value:  1.89 (should be moderate)  ✓
Mean tau:        1.16 (should be 0.5-2.5)   ✓
Tension splines: 6/10 (≈50%)                ✓
Step functions:  4/10 (≈50%)                ✓
```

---

## Cambios Rápidos

### Si necesitas UUID para cambios:
```python
# Agrega a metadata
"amplitude_config": {
    "p_tension_spline": 0.5,
    "tau_amp_min": 0.5,
    "tau_amp_max": 2.5,
    "amp_min": 1,
    "amp_max": 8,
    "version": "2026-01-13-optimized"
}
```

### Para revertir a valores antiguos (no recomendado):
```python
# En SignalBuilderC
amplitude = (2 * rng.random() - 1.0) * rng.integers(3, 16)
tau = float(rng.choice([1, 3, 5, 8, 10, 12, 15, 20]))
use_tension = rng.choice([True, False], p=[0.3, 0.7])

# En SignalBuilderCLI
generate_random_amplitude_envelope(t, rng,
    p_tension_spline=0.3,
    tau_amp_min=1.0,
    tau_amp_max=20.0,
    amp_min=3,
    amp_max=15,
)
```

---

## Referencias Rápidas

- 📄 Reporte completo: `SIGNAL_AMPLITUDE_FIX_REPORT.md`
- 📊 Análisis técnico: `AMPLITUDE_FIXES_ANALYSIS.md`
- 🎯 Resumen cambios: `CHANGES_SUMMARY_AMPLITUDES.md`
- ✅ Checklist: `CHECKLIST_AMPLITUDE_FIXES.md`
- 🧪 Validación: `test_amplitude_fix.py`
- 📈 Comparación visual: `compare_amplitude_fixes.py`

---

**Actualizado:** 13-01-2026
