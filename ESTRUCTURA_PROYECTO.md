# Estructura del Proyecto - Clasificador de Noticias NLP

## Estructura de Directorios

```
Proyecto/
│
├── .claude/                          # Configuración de Claude Code
│   └── settings.local.json
│
├── data/                             # Datasets y datos procesados
│   ├── raw/                          # Datos originales (no versionados)
│   │   ├── GOOGLE.tsv               # Dataset Google News (11 MB)
│   │   └── MIND.tsv                 # Dataset Microsoft News (9.2 MB)
│   │
│   ├── processed/                    # Datos procesados (no versionados)
│   │   └── dataset_preprocessed.csv # Dataset combinado y limpio (23 MB)
│   │
│   └── splits/                       # División train/val/test (no versionados)
│       ├── train.csv                # 145,178 registros (70%)
│       ├── val.csv                  # 41,427 registros (20%)
│       └── test.csv                 # 20,734 registros (10%)
│
├── models/                           # Modelos entrenados
│   ├── best_model.pkl               # Logistic Regression (79 KB)
│   └── vectorizer.pkl               # TF-IDF Vectorizer (329 KB)
│
├── notebooks/                        # Jupyter Notebooks (exploración)
│   ├── 01_EDA.ipynb                 # Análisis Exploratorio de Datos
│   ├── 02_preprocessing.ipynb       # Preprocesamiento y limpieza
│   ├── 03_data_splitting.ipynb      # División de datos estratificada
│   └── 04_model_training_evaluation.ipynb  # Entrenamiento y evaluación
│
├── results/                          # Resultados y visualizaciones
│   ├── # Análisis Exploratorio (EDA)
│   ├── category_distribution.png    # Distribución de categorías originales
│   ├── class_distribution.png       # Distribución de clases binarias
│   ├── class_by_source.png          # Clases por fuente de datos
│   ├── split_distribution.png       # Distribución train/val/test
│   ├── text_length_distribution.png # Distribución de longitud de textos
│   ├── split_summary.csv            # Resumen de división
│   │
│   ├── # Métricas de Entrenamiento
│   ├── training_metrics.json        # Métricas de los 4 modelos
│   ├── model_comparison_training.csv # Comparación de modelos
│   │
│   ├── # Evaluación Final (Test Set)
│   ├── final_test_metrics.json      # Métricas finales (F1=88.62%)
│   ├── confusion_matrix_final_test.png  # Matriz de confusión
│   ├── roc_curve_final_test.png     # Curva ROC (AUC=93.79%)
│   ├── classification_report_test.txt   # Reporte detallado
│   │
│   ├── # Predicciones y Análisis de Errores (no versionados)
│   ├── test_predictions_final.csv   # Predicciones del test set (2.7 MB)
│   └── test_errors.csv              # Análisis de errores (348 KB)
│
├── src/                              # Código fuente modular
│   ├── __init__.py                  # Inicialización del paquete
│   ├── preprocessing.py             # Limpieza y preprocesamiento de texto
│   ├── feature_engineering.py       # Vectorización TF-IDF
│   ├── models.py                    # Creación de modelos ML
│   └── evaluation.py                # Métricas y visualizaciones
│
├── test_sets/                        # Conjuntos de test para instructor
│   ├── test_public.csv              # Test sin etiquetas (1.7 MB)
│   └── test_labels.csv              # Etiquetas del test (554 KB)
│
├── .gitignore                        # Archivos ignorados por Git
├── config.py                         # Configuración centralizada del proyecto
├── requirements.txt                  # Dependencias Python
│
├── # Scripts de Ejecución (Producción)
├── train.py                          # Entrenamiento de modelos
├── evaluate.py                       # Evaluación en test set
├── predict.py                        # Predictor para nuevas noticias
├── run_pipeline.py                   # Pipeline completo automatizado
├── run_notebooks.py                  # Ejecutor de notebooks
│
├── # Documentación
├── README.md                         # Documentación principal del proyecto
├── QUICKSTART.md                     # Guía de inicio rápido
├── CUMPLIMIENTO_REQUISITOS_NLP.md   # Verificación de requisitos NLP
└── ESTRUCTURA_PROYECTO.md            # Este archivo
```

---

## Archivos Principales

### Scripts de Producción

#### 1. `train.py` - Entrenamiento de Modelos
- Carga datasets train/val
- Vectoriza textos con TF-IDF
- Entrena 4 modelos ML
- Selecciona el mejor modelo (F1-Score)
- Guarda modelo y vectorizador

**Uso:**
```bash
python train.py
```

**Salida:**
- `models/best_model.pkl`
- `models/vectorizer.pkl`
- `results/training_metrics.json`
- `results/model_comparison_training.csv`

---

#### 2. `evaluate.py` - Evaluación Final
- Carga modelo entrenado
- Evalúa en test set independiente
- Calcula métricas completas
- Genera visualizaciones
- Analiza errores

**Uso:**
```bash
python evaluate.py
```

**Salida:**
- `results/final_test_metrics.json`
- `results/confusion_matrix_final_test.png`
- `results/roc_curve_final_test.png`
- `results/classification_report_test.txt`
- `results/test_predictions_final.csv`
- `results/test_errors.csv`

---

#### 3. `predict.py` - Predictor
- Clasificación de nuevas noticias
- Soporte para texto individual o batch
- Muestra probabilidades de clase

**Uso:**
```bash
# Predicción individual
python predict.py --text "Breaking news about stock market" --proba

# Predicción desde archivo CSV
python predict.py --file news.csv --output predictions.csv
```

---

#### 4. `run_pipeline.py` - Pipeline Completo
- Ejecuta el pipeline end-to-end
- Preprocesamiento → Entrenamiento → Evaluación
- Ideal para reproducibilidad

**Uso:**
```bash
python run_pipeline.py
```

---

### Módulos Principales (`src/`)

#### 1. `preprocessing.py`
- Limpieza de texto
- Normalización
- Mapeo de categorías a clases binarias

**Funciones:**
- `clean_text()` - Limpia y normaliza texto
- `map_category_to_class()` - Mapea categorías a binario

---

#### 2. `feature_engineering.py`
- Vectorización TF-IDF
- Configuración de vocabulario (10,000 términos)
- N-gramas (unigramas + bigramas)

**Funciones:**
- `create_tfidf_vectorizer()` - Crea vectorizador
- `save_vectorizer()` - Guarda vectorizador

---

#### 3. `models.py`
- Creación de modelos ML
- Configuración optimizada para texto
- Manejo de desbalance de clases

**Funciones:**
- `create_naive_bayes()`
- `create_logistic_regression()`
- `create_linear_svm()`
- `create_random_forest()`
- `save_model()`, `load_model()`

---

#### 4. `evaluation.py`
- Cálculo de métricas (Accuracy, Precision, Recall, F1, ROC-AUC)
- Generación de visualizaciones
- Matrices de confusión
- Curvas ROC

**Funciones:**
- `calculate_metrics()`
- `plot_confusion_matrix()`
- `plot_roc_curve()`
- `generate_classification_report()`

---

### Configuración

#### `config.py`
Configuración centralizada del proyecto:

- **Rutas de datos y modelos**
- **División de datos** (70/20/10)
- **Mapeo de categorías** (26 → 2 clases)
- **Configuración TF-IDF** (max_features, n-gramas)
- **Parámetros de modelos ML**
- **Métricas de evaluación**

---

### Notebooks (`notebooks/`)

#### 1. `01_EDA.ipynb` - Análisis Exploratorio
- Exploración de datasets MIND y GOOGLE
- Estadísticas descriptivas
- Distribución de categorías
- Visualizaciones

#### 2. `02_preprocessing.ipynb` - Preprocesamiento
- Combinación de datasets
- Limpieza de duplicados
- Mapeo de categorías a binario
- Guardado de dataset procesado

#### 3. `03_data_splitting.ipynb` - División de Datos
- División estratificada 70/20/10
- Generación de test_public.csv
- Generación de test_labels.csv
- Verificación de balanceo

#### 4. `04_model_training_evaluation.ipynb` - Entrenamiento
- Vectorización TF-IDF
- Entrenamiento de 4 modelos
- Evaluación en validation set
- Comparación de modelos
- Visualizaciones

---

## Datasets

### Datos Originales (20 MB total)
- **MIND.tsv**: 93,239 noticias de Microsoft News
- **GOOGLE.tsv**: 119,100 noticias de Google News

### Dataset Combinado
- **Total**: 207,339 noticias (después de limpieza)
- **Categorías originales**: 26
- **Clases binarias**: 2
  - Actualidad (39.33%): news, finance, business, science, technology, etc.
  - Interés General (60.67%): sports, entertainment, lifestyle, travel, etc.

### División de Datos
- **Train**: 145,178 noticias (70%)
- **Validation**: 41,427 noticias (20%)
- **Test**: 20,734 noticias (10%)

---

## Modelos Entrenados

### Mejor Modelo: Logistic Regression
- **Archivo**: `models/best_model.pkl` (79 KB)
- **Vectorizador**: `models/vectorizer.pkl` (329 KB)
- **Vocabulario**: 10,000 términos (TF-IDF)
- **N-gramas**: Unigramas + Bigramas

### Métricas Finales (Test Set)
```
Accuracy:   86.68%
Precision:  92.02%
Recall:     85.45%
F1-Score:   88.62%  ← Métrica principal
ROC-AUC:    93.79%
```

---

## Resultados y Visualizaciones

### Métricas JSON
- `training_metrics.json` - Métricas de los 4 modelos en validation
- `final_test_metrics.json` - Métricas finales en test set

### Visualizaciones PNG
- **EDA**: Distribución de categorías, clases, splits, longitud de textos
- **Evaluación**: Matriz de confusión, curva ROC

### Reportes CSV/TXT
- `model_comparison_training.csv` - Comparación de 4 modelos
- `classification_report_test.txt` - Reporte detallado por clase
- `split_summary.csv` - Resumen de división de datos

### Predicciones (CSV grandes - no versionados)
- `test_predictions_final.csv` - 20,734 predicciones
- `test_errors.csv` - 2,762 errores analizados

---

## Dependencias

Ver `requirements.txt`:
- `pandas` - Manipulación de datos
- `numpy` - Operaciones numéricas
- `scikit-learn` - Machine Learning
- `matplotlib` - Visualizaciones
- `seaborn` - Gráficos estadísticos
- `jupyter` - Notebooks interactivos

---

## Control de Versiones

### `.gitignore`
- Datasets grandes (`.tsv`, `.csv` en `data/`)
- Archivos de predicciones (CSV grandes)
- Cache de Python (`__pycache__`)
- Logs
- Checkpoints de notebooks

### Archivos versionados
- Código fuente (`src/`, scripts `.py`)
- Modelos entrenados (`models/*.pkl`)
- Configuración (`config.py`, `requirements.txt`)
- Documentación (`.md`)
- Notebooks (`.ipynb`)
- Visualizaciones PNG
- Métricas JSON

---

## Flujo de Trabajo Recomendado

### Opción A: Ejecución con Scripts (Producción)
```bash
# 1. Entrenar modelos
python train.py

# 2. Evaluar en test set
python evaluate.py

# 3. Predecir nuevas noticias
python predict.py --text "Your news here" --proba
```

### Opción B: Ejecución con Notebooks (Exploración)
```bash
# Ejecutar todos los notebooks
python run_notebooks.py
```

### Opción C: Pipeline Completo (Reproducibilidad)
```bash
# Pipeline end-to-end automatizado
python run_pipeline.py
```

---

## Tamaños de Archivos

### Archivos Pequeños (versionados)
- Scripts Python: ~10-14 KB cada uno
- Modelos: 79 KB (modelo) + 329 KB (vectorizador)
- Visualizaciones PNG: 100-400 KB cada una
- Métricas JSON: < 1 KB
- Documentación MD: 8-12 KB

### Archivos Grandes (no versionados)
- Datasets TSV: 9-11 MB cada uno
- Datasets procesados CSV: 23 MB
- Splits CSV: 2-16 MB
- Predicciones CSV: 2-3 MB

### Total del Proyecto
- **Con datos**: ~100 MB
- **Sin datos**: ~5 MB (solo código y modelos)

---

## Notas Importantes

1. **Reproducibilidad**: `RANDOM_STATE=42` en todos los procesos aleatorios
2. **División estratificada**: Mantiene proporción de clases en train/val/test
3. **Manejo de desbalance**: `class_weight='balanced'` en modelos
4. **Validación independiente**: Test set nunca usado en entrenamiento
5. **Modularidad**: Código organizado en módulos reutilizables
6. **Logging**: Todos los scripts con logging detallado
7. **Documentación**: Docstrings en todas las funciones

---

**Proyecto organizado siguiendo mejores prácticas de:**
- Machine Learning
- Procesamiento Natural de Lenguaje (NLP)
- Ingeniería de Software
- Ciencia de Datos

---

**Última actualización:** 14 de Noviembre, 2025
