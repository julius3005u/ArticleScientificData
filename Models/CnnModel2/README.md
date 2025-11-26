# 🚀 CNN Super-Resolución - Experimento CnnModel2

## 📋 Descripción

Este experimento entrena una red neuronal convolucional (CNN) para super-resolución de señales temporales usando el dataset **CoSiBD (Correlated Signal Builder Database)**. El modelo aprende a reconstruir señales de alta resolución (5,000 muestras) a partir de versiones submuestreadas (1,000 muestras).

**Objetivo:** Validar que el dataset CoSiBD puede ser usado efectivamente para entrenar modelos de super-resolución, demostrando su utilidad para la comunidad científica.

## 🗂️ Estructura del Proyecto

```
CnnModel2/
├── data/
│   ├── train/
│   │   ├── high_res/          # 2,000 señales × 5,000 samples
│   │   └── low_res/           # 2,000 señales × 1,000 samples
│   └── validation/
│       ├── high_res/          # 500 señales × 5,000 samples
│       └── low_res/           # 500 señales × 1,000 samples
├── models/
│   └── best_model.pth         # Mejor checkpoint (generado durante entrenamiento)
├── results/
│   ├── loss_curves.png        # Curvas de entrenamiento/validación
│   ├── prediction_examples.png # Comparación visual de predicciones
│   ├── loss_history.csv       # Historial de pérdidas por época
│   └── experiment_summary.txt # Resumen del experimento
├── temana.py                  # Biblioteca de utilidades para manejo de datos
├── cnnTrain2.ipynb            # Notebook principal de entrenamiento
└── README.md                  # Este archivo
```

## 🏗️ Arquitectura del Modelo

**TimeSeriesSRNet** - Red encoder-decoder parametrizable:

### Encoder (Extracción de características)
- Conv1D: 1 → 64 canales (kernel=9, stride=1, padding=4)
- BatchNorm + ReLU
- Conv1D: 64 → 128 canales (kernel=5, stride=1, padding=2)
- BatchNorm + ReLU
- Conv1D: 128 → 256 canales (kernel=5, stride=1, padding=2)
- BatchNorm + ReLU

### Upsampler (Reconstrucción)
- Linear Upsample: Factor 5x (1,000 → 5,000 samples)
- Conv1D: 256 → 128 canales (kernel=5, padding=2)
- BatchNorm + ReLU
- Conv1D: 128 → 64 canales (kernel=5, padding=2)
- BatchNorm + ReLU
- Conv1D: 64 → 1 canal (kernel=9, padding=4)

**Parámetros totales:** ~500K parámetros

## ⚙️ Configuración del Experimento

| Parámetro | Valor |
|-----------|-------|
| **Input Size** | 1,000 samples |
| **Output Size** | 5,000 samples |
| **Upsample Factor** | 5x |
| **Training Samples** | 2,000 señales |
| **Validation Samples** | 500 señales |
| **Batch Size** | 16 |
| **Learning Rate** | 0.001 |
| **Optimizer** | Adam (weight_decay=1e-5) |
| **Loss Function** | MSE (Mean Squared Error) |
| **Epochs** | 50 |
| **Device** | CUDA (si está disponible) / CPU |

## 🚀 Uso

### 1. Entrenamiento

Abre y ejecuta el notebook `cnnTrain2.ipynb` en Jupyter:

```bash
cd Models/CnnModel2
jupyter notebook cnnTrain2.ipynb
```

El notebook está organizado en secciones:
1. Configuración e importaciones
2. Parámetros del experimento
3. Definición del modelo TimeSeriesSRNet
4. Carga de datos desde `data/`
5. Creación de DataLoaders
6. Configuración de entrenamiento (loss + optimizer)
7. Loop de entrenamiento con checkpointing
8. Visualización de curvas de pérdida
9. Carga del mejor modelo
10. Predicciones en validación
11. Guardado de resultados

**Tiempo estimado de entrenamiento:** 10-30 minutos (dependiendo de GPU/CPU)

### 2. Inferencia en Nuevas Señales

```python
import torch
import numpy as np
from temana import MyDataset

# Cargar modelo entrenado
checkpoint = torch.load('models/best_model.pth')
model = TimeSeriesSRNet(upsample_factor=10)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# Cargar señal de baja resolución (1,000 samples)
low_res_signal = np.loadtxt('path/to/signal_sub1000.txt')

# Hacer predicción
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with torch.no_grad():
    input_tensor = torch.tensor(low_res_signal, dtype=torch.float32)
    input_tensor = input_tensor.unsqueeze(0).unsqueeze(0).to(device)
    high_res_pred = model(input_tensor).cpu().numpy().flatten()

# high_res_pred contiene 5,000 samples
print(f"Predicción generada: {high_res_pred.shape}")
```

## 📊 Resultados Esperados

Al ejecutar el notebook completo, se generarán:

1. **Modelo entrenado:** `models/best_model.pth` (checkpoint con mejor validation loss)
2. **Curvas de pérdida:** `results/loss_curves.png` (evolución de train/val loss)
3. **Ejemplos visuales:** `results/prediction_examples.png` (5 ejemplos comparando low-res, predicción, ground-truth)
4. **Historial CSV:** `results/loss_history.csv` (pérdidas por época para análisis posterior)
5. **Resumen:** `results/experiment_summary.txt` (configuración y resultados del experimento)

### Métricas de Evaluación

- **MSE (Mean Squared Error):** Función de pérdida principal
- **Comparación visual:** Superposición de señales predichas vs. ground truth
- **Best validation loss:** Se reporta al final del entrenamiento

## 🔬 Detalles del Dataset

Las señales provienen de **SignalBuilderC**, un generador de señales correlacionadas del proyecto CoSiBD:

- **Señales de alta resolución:** Archivos `.txt` con 5,000 muestras cada uno
- **Señales submuestreadas:** Versiones simplificadas con 1,000 muestras (factor 5x)
- **Formato:** Archivos de texto plano con un valor por línea
- **Nomenclatura:** 
  - Alta resolución: `signal_XXXX.txt`
  - Baja resolución: `signal_XXXX_sub1000.txt`

**División train/val:**
- Train: Señales 0000-1999 (2,000 pares)
- Validation: Señales 2000-2499 (500 pares)

## 📚 Dependencias

```python
torch>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
tqdm>=4.65.0
```

Instalar con:
```bash
pip install torch numpy matplotlib tqdm
```

## 🎯 Próximos Pasos

1. **Evaluación cuantitativa adicional:**
   - Calcular PSNR (Peak Signal-to-Noise Ratio)
   - Calcular SNR (Signal-to-Noise Ratio)
   - Comparar con métodos baseline (interpolación lineal, spline)

2. **Ablation studies:**
   - Probar diferentes arquitecturas (más/menos capas)
   - Experimentar con kernel sizes
   - Probar diferentes factores de upsampling

3. **Generalización:**
   - Validar con datos reales (EEG, VCTK) del manuscrito
   - Transfer learning a otros dominios

4. **Optimización:**
   - Learning rate scheduling
   - Data augmentation (ruido, desplazamientos)
   - Regularización adicional

## 📄 Relación con el Manuscrito

Este experimento apoya las siguientes secciones del manuscrito:

- **Preliminary Application Results:** Demuestra uso efectivo del dataset CoSiBD
- **Technical Validation:** Valida la calidad de las señales generadas
- **Usage Notes:** Proporciona ejemplo concreto de aplicación ML

**Reviewer Requirements Addressed:**
- R1-3: Validación con datos reales (preparación para EEG/VCTK)
- R2-2: Resultados cuantitativos para demostrar utilidad del dataset
- R3-1: Experimentos CNN adicionales más allá de los preliminares

## 👥 Autores

Creado como parte del proyecto **CoSiBD (Correlated Signal Builder Database)** para el manuscrito en Scientific Data.

## 📝 Notas

- El modelo es completamente parametrizable: ajustar `INPUT_SIZE` y `OUTPUT_SIZE` en el notebook
- Los checkpoints se guardan automáticamente cuando mejora la validation loss
- El notebook está diseñado para ser ejecutado de principio a fin sin interacción manual
- Todos los paths son relativos al directorio `CnnModel2/`

---

**Última actualización:** 22 de noviembre de 2024
