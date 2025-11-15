# Clasificador de Noticias: Actualidad vs Interés General

Proyecto de Procesamiento de Lenguaje Natural para clasificar noticias en dos categorías: **Actualidad** (noticias de eventos actuales) e **Interés General** (contenido de entretenimiento, deportes, lifestyle, etc.).

## Descripción del Proyecto

Este proyecto implementa un sistema de clasificación de texto binario utilizando técnicas de Machine Learning para categorizar automáticamente titulares de noticias provenientes de los datasets MIND (Microsoft News Dataset) y Google News.

### Clases de Clasificación

- **Clase 0 - Actualidad**: Noticias de eventos actuales, política, economía, negocios, ciencia y tecnología
- **Clase 1 - Interés General**: Deportes, entretenimiento, lifestyle, salud, viajes, comida, autos, etc.

## Estructura del Proyecto

```
proyecto-clasificador-noticias/
├── README.md                          # Este archivo
├── requirements.txt                   # Dependencias del proyecto
├── config.py                          # Configuración centralizada
├── .gitignore                         # Archivos ignorados por Git
│
├── Scripts Python (Ejecución Automatizada):
│   ├── run_pipeline.py               # Pipeline completo automatizado
│   ├── train.py                      # Script de entrenamiento
│   ├── evaluate.py                   # Script de evaluación
│   └── predict.py                    # Script de predicción
│
├── data/
│   ├── raw/                          # Datasets originales (MIND.tsv, GOOGLE.tsv)
│   ├── processed/                    # Datos procesados
│   │   ├── combined_raw.csv          # Dataset combinado sin procesar
│   │   └── dataset_preprocessed.csv  # Dataset preprocesado y limpio
│   └── splits/                       # Splits de entrenamiento/validación/test
│       ├── train.csv                 # 70% - Conjunto de entrenamiento
│       ├── val.csv                   # 20% - Conjunto de validación
│       └── test.csv                  # 10% - Conjunto de test
│
├── notebooks/                        # Notebooks Jupyter (Exploración)
│   ├── 01_EDA.ipynb                  # Análisis Exploratorio de Datos
│   ├── 02_preprocessing.ipynb        # Preprocesamiento y mapeo de categorías
│   ├── 03_data_splitting.ipynb       # División estratificada del dataset
│   └── 04_model_training_evaluation.ipynb  # Entrenamiento y evaluación
│
├── src/                              # Módulos Python reutilizables
│   ├── __init__.py                   # Inicialización del paquete
│   ├── preprocessing.py              # Funciones de preprocesamiento
│   ├── feature_engineering.py        # Vectorización y features
│   ├── models.py                     # Definición de modelos
│   └── evaluation.py                 # Métricas y evaluación
│
├── models/                           # Modelos entrenados
│   ├── best_model.pkl                # Mejor modelo entrenado
│   └── vectorizer.pkl                # Vectorizador TF-IDF
│
├── results/                          # Gráficos, métricas y reportes
│   ├── training_metrics.json         # Métricas de todos los modelos
│   ├── final_test_metrics.json       # Métricas finales en test
│   ├── model_comparison_training.csv # Comparación de modelos
│   ├── test_predictions_final.csv    # Predicciones completas
│   ├── test_errors.csv               # Análisis de errores
│   ├── classification_report_test.txt # Reporte detallado
│   └── *.png                         # Visualizaciones (matrices, curvas ROC, etc.)
│
└── test_sets/                        # Archivos de test para instructor
    ├── test_public.csv               # Test sin etiquetas
    └── test_labels.csv               # Test con etiquetas (solo docente)
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd proyecto-clasificador-noticias
```

### 2. Crear entorno virtual (recomendado)

```bash
# Usando venv
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

Este proyecto ofrece **dos formas de ejecución**: scripts automatizados (recomendado para producción) o notebooks interactivos (recomendado para exploración y aprendizaje).

### 🚀 Opción 1: Scripts Automatizados (Recomendado)

#### Ejecución Completa del Pipeline

Para ejecutar todo el flujo de trabajo de principio a fin:

```bash
python run_pipeline.py
```

Este script ejecutará automáticamente:
1. Carga y preprocesamiento de datos
2. División estratificada (70/20/10)
3. Entrenamiento de modelos
4. Evaluación en conjunto de test
5. Generación de reportes y visualizaciones

#### Ejecución por Pasos

**Paso 1: Entrenar modelos**
```bash
python train.py
```
- Lee los datos de `data/splits/`
- Vectoriza con TF-IDF
- Entrena 4 modelos (Naive Bayes, Logistic Regression, SVM, Random Forest)
- Selecciona el mejor basado en F1-Score
- Guarda modelo y vectorizador en `models/`

**Paso 2: Evaluar en test set**
```bash
python evaluate.py
```
- Carga el mejor modelo entrenado
- Evalúa en conjunto de test
- Genera métricas, visualizaciones y análisis de errores
- Guarda resultados en `results/`

**Paso 3: Hacer predicciones**

Predicción de un texto individual:
```bash
python predict.py --text "Breaking news about the economy" --proba
```

Predicción desde archivo CSV:
```bash
python predict.py --file noticias.csv --output predicciones.csv --column titulo
```

#### Opciones Avanzadas

Ejecutar pipeline saltando pasos ya completados:
```bash
# Saltar preprocesamiento (usar datos existentes)
python run_pipeline.py --skip-preprocessing

# Saltar entrenamiento (usar modelo existente)
python run_pipeline.py --skip-training
```

### 📓 Opción 2: Notebooks Interactivos (Jupyter)

Para exploración paso a paso y análisis detallado:

#### 1. Análisis Exploratorio de Datos (EDA)

```bash
jupyter notebook notebooks/01_EDA.ipynb
```

**Salidas:**
- Estadísticas descriptivas de los datasets
- Distribución de categorías
- Análisis de longitud de texto
- Detección de duplicados
- Visualizaciones guardadas en `results/`

#### 2. Preprocesamiento

```bash
jupyter notebook notebooks/02_preprocessing.ipynb
```

**Tareas:**
- Mapeo de categorías originales a clases binarias
- Limpieza de duplicados
- Normalización de texto
- Generación de `dataset_preprocessed.csv`

**Mapeo de categorías:**
- **Actualidad**: news, finance, weather, World, U.S., Business, Science, Technology
- **Interés General**: sports, lifestyle, entertainment, health, travel, Sport, Entertainment, Health, etc.

#### 3. División Estratificada del Dataset

```bash
jupyter notebook notebooks/03_data_splitting.ipynb
```

**Criterios técnicos:**
- Split estratificado para mantener proporción de clases
- 70% entrenamiento, 20% validación, 10% test
- Sin duplicados entre conjuntos
- Reproducibilidad garantizada (random_state=42)

**Salidas:**
- `train.csv` (70%)
- `val.csv` (20%)
- `test.csv` (10%)
- `test_public.csv` (sin etiquetas para evaluación)
- `test_labels.csv` (solo etiquetas para revisión del docente)

#### 4. Entrenamiento y Evaluación de Modelos

```bash
jupyter notebook notebooks/04_model_training_evaluation.ipynb
```

**Modelos implementados:**
1. Naive Bayes (MultinomialNB)
2. Logistic Regression
3. Linear SVM
4. Random Forest

**Vectorización:**
- TF-IDF con top 10,000 features
- Unigramas y bigramas (n-grams: 1-2)
- Eliminación de stop words

**Métricas de evaluación:**
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- Matriz de confusión

## Resultados

### Conjuntos de Datos

| Dataset | Registros | Porcentaje |
|---------|-----------|------------|
| Training | ~149,000 | 70% |
| Validation | ~42,500 | 20% |
| Test | ~21,300 | 10% |
| **Total** | ~212,800 | 100% |

### Distribución de Clases

- **Clase 0 (Actualidad)**: ~30-35%
- **Clase 1 (Interés General)**: ~65-70%

*Nota: Los porcentajes exactos se mantienen estratificados en todos los splits*

### Mejor Modelo

El mejor modelo será seleccionado automáticamente basado en el F1-Score en el conjunto de validación. Los resultados específicos se encuentran en:

- `results/model_comparison.csv` - Comparación de todos los modelos
- `results/final_metrics.json` - Métricas del mejor modelo en test
- `models/best_model.pkl` - Modelo entrenado guardado

## Reproducibilidad

Este proyecto garantiza reproducibilidad mediante:

1. **Random state fijo**: `RANDOM_STATE = 42` en todos los procesos estocásticos
2. **Documentación completa**: Notebooks con explicaciones paso a paso
3. **Versionamiento de dependencias**: `requirements.txt` con versiones específicas
4. **Scripts documentados**: Código comentado y autoexplicativo

### Para reproducir los resultados:

```bash
# 1. Instalar dependencias exactas
pip install -r requirements.txt

# 2. Ejecutar notebooks en orden
jupyter notebook

# 3. Los resultados serán idénticos debido al random_state fijo
```

## Archivos para el Instructor

### test_public.csv
Conjunto de test sin etiquetas, listo para evaluación ciega:
- Columnas: `doc_id`, `text`
- ~21,300 registros

### test_labels.csv
Etiquetas verdaderas del conjunto de test (solo para revisión del docente):
- Columnas: `doc_id`, `label`, `class_name`
- ~21,300 registros

## Métricas de Evaluación

### En Conjunto de Validación
Los modelos son evaluados y comparados usando el conjunto de validación (20%).

### En Conjunto de Test
Evaluación final del mejor modelo en datos nunca vistos durante el entrenamiento.

Las métricas incluyen:
- **Accuracy**: Proporción de predicciones correctas
- **Precision**: De todas las predicciones positivas, cuántas son correctas
- **Recall**: De todos los casos positivos reales, cuántos fueron identificados
- **F1-Score**: Media armónica de precision y recall
- **ROC-AUC**: Área bajo la curva ROC

## Posibles Extensiones

### Mejoras futuras:
1. **Modelos avanzados**: BERT, RoBERTa, GPT para embeddings contextuales
2. **Ensemble methods**: Combinar múltiples modelos
3. **Análisis de errores detallado**: Estudiar casos mal clasificados
4. **Clasificación multiclase**: Usar subcategorías en lugar de binario
5. **API de predicción**: Servicio REST para clasificar nuevas noticias
6. **Dashboard interactivo**: Visualización web de resultados

## Autores

Proyecto desarrollado para la asignatura de Procesamiento de Lenguaje Natural.

## Licencia

Este proyecto es de uso académico.

## Contacto

Para preguntas o sugerencias sobre el proyecto, por favor contactar al equipo de desarrollo.

---

**Fecha de creación**: Noviembre 2024
**Última actualización**: Noviembre 2024
