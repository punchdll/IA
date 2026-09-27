# Iris MLP - Clasificación de flores Iris con Red Neuronal

## Descripción

Este proyecto implementa un clasificador multiclase utilizando una red neuronal
MLP (Multilayer Perceptron) para clasificar flores del dataset Iris en tres
especies: Setosa, Versicolor y Virginica.

## Arquitectura del Modelo

```
Entrada (4 características)
        │
        ▼
┌─────────────────────┐
│  Dense (8 neuronas) │  ← Activación ReLU
│  + Bias             │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Dense (8 neuronas) │  ← Activación ReLU
│  + Bias             │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Dense (3 neuronas) │  ← Activación Softmax
│  + Bias             │     (probabilidades por clase)
└─────────────────────┘
        │
        ▼
Salida (3 probabilidades que suman 1.0)
```

### Parámetros totales

| Capa | Pesos | Bias | Total |
|------|-------|------|-------|
| Dense 1 | 4 × 8 = 32 | 8 | 40 |
| Dense 2 | 8 × 8 = 64 | 8 | 72 |
| Dense 3 | 8 × 3 = 24 | 3 | 27 |
| **Total** | | | **139** |

## Pipeline de Datos

1. **Carga**: Se lee `iris.csv` con `numpy.loadtxt` (150 registros, 5 columnas)
2. **Separación**: `X` = 4 columnas de características, `Y` = columna de clase
3. **Partición**: 80% entrenamiento (120 muestras) / 20% validación (30 muestras)
4. **Estratificación**: Se mantiene la proporción de clases en ambos conjuntos
5. **Semilla fija**: `random_state=42` para reproducibilidad

## Entrenamiento

| Aspecto | Configuración |
|---------|---------------|
| Optimizador | Adam (learning rate inicial: 0.001) |
| Función de pérdida | Sparse Categorical Crossentropy |
| Métrica | Accuracy |
| Callbacks | EarlyStopping + ReduceLROnPlateau |

### Callbacks

- **EarlyStopping**: Detiene el entrenamiento si `val_loss` no mejora en 5
  épocas. Restaura los mejores pesos automáticamente.
- **ReduceLROnPlateau**: Reduce el learning rate a la mitad si `val_loss` no
  mejora en 2 épocas. Límite mínimo: 1e-6.

## Estructura del Proyecto

```
Iris_MLP/
├── notebook.ipynb      # Notebook principal con todo el código
├── iris.csv            # Dataset (150 muestras, 4 características)
├── pyproject.toml      # Dependencias del proyecto
├── uv.lock             # Lockfile de uv
└── README.md           # Este archivo
```

## Requisitos

- Python 3.12
- TensorFlow 2.21+
- Keras 3.15+
- scikit-learn 1.9+

## Uso

```bash
# Instalar dependencias
uv sync

# Ejecutar el notebook
uv run jupyter notebook notebook.ipynb
```

## Dataset

El dataset Iris contiene 150 muestras con 4 características numéricas:

| Característica | Descripción |
|----------------|-------------|
| sepal.length   | Longitud del sépalo (cm) |
| sepal.width    | Ancho del sépalo (cm) |
| petal.length   | Longitud del pétalo (cm) |
| petal.width    | Ancho del pétalo (cm) |

Clases: `0 = Setosa`, `1 = Versicolor`, `2 = Virginica` (50 muestras cada una).
