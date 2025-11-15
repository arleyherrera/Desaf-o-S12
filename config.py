"""
config.py
Archivo de configuración centralizada para el proyecto de clasificación de noticias.

Buenas prácticas:
- Configuración centralizada
- Constantes en mayúsculas
- Documentación clara
- Separación por secciones

Autor: 
Fecha: Noviembre 2025
"""

import os
from pathlib import Path

# ============================================================================
# RUTAS DEL PROYECTO
# ============================================================================

# Directorio raíz del proyecto
ROOT_DIR = Path(__file__).parent.absolute()

# Directorios de datos
DATA_DIR = ROOT_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
SPLITS_DIR = DATA_DIR / 'splits'

# Directorios de modelos y resultados
MODELS_DIR = ROOT_DIR / 'models'
RESULTS_DIR = ROOT_DIR / 'results'
TEST_SETS_DIR = ROOT_DIR / 'test_sets'

# Crear directorios si no existen
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, SPLITS_DIR,
                  MODELS_DIR, RESULTS_DIR, TEST_SETS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================================
# ARCHIVOS DE DATOS
# ============================================================================

# Datasets originales
MIND_TSV = RAW_DATA_DIR / 'MIND.tsv'
GOOGLE_TSV = RAW_DATA_DIR / 'GOOGLE.tsv'

# Datasets procesados
COMBINED_RAW_CSV = PROCESSED_DATA_DIR / 'combined_raw.csv'
PREPROCESSED_CSV = PROCESSED_DATA_DIR / 'dataset_preprocessed.csv'

# Splits
TRAIN_CSV = SPLITS_DIR / 'train.csv'
VAL_CSV = SPLITS_DIR / 'val.csv'
TEST_CSV = SPLITS_DIR / 'test.csv'

# Test sets para instructor
TEST_PUBLIC_CSV = TEST_SETS_DIR / 'test_public.csv'
TEST_LABELS_CSV = TEST_SETS_DIR / 'test_labels.csv'

# ============================================================================
# ARCHIVOS DE MODELOS
# ============================================================================

BEST_MODEL_PATH = MODELS_DIR / 'best_model.pkl'
VECTORIZER_PATH = MODELS_DIR / 'vectorizer.pkl'

# ============================================================================
# CONFIGURACIÓN DE PREPROCESAMIENTO
# ============================================================================

# Columnas esperadas en los datasets
DATASET_COLUMNS = ['doc_id', 'category', 'subcategory', 'title']

# Mapeo de categorías a clases binarias
# Clase 0: Actualidad (Current News)
ACTUALIDAD_CATEGORIES = {
    # MIND categories
    'news',
    'finance',
    'weather',
    'northamerica',
    'middleeast',
    # GOOGLE categories
    'World',
    'U.S.',
    'Business',
    'Science',
    'Technology'
}

# Clase 1: Interés General (General Interest)
INTERES_GENERAL_CATEGORIES = {
    # MIND categories
    'sports',
    'lifestyle',
    'video',
    'foodanddrink',
    'autos',
    'health',
    'tv',
    'music',
    'entertainment',
    'movies',
    'kids',
    'travel',
    'games',
    # GOOGLE categories
    'Sport',
    'Entertainment',
    'Health'
}

# Nombres de clases
CLASS_NAMES = ['Actualidad', 'Interés General']

# ============================================================================
# CONFIGURACIÓN DE DIVISIÓN DE DATOS
# ============================================================================

# Semilla aleatoria para reproducibilidad
RANDOM_STATE = 42

# Porcentajes de división
TRAIN_SIZE = 0.70
VAL_SIZE = 0.20
TEST_SIZE = 0.10

# Verificación
assert abs(TRAIN_SIZE + VAL_SIZE + TEST_SIZE - 1.0) < 1e-6, "Los porcentajes deben sumar 1.0"

# ============================================================================
# CONFIGURACIÓN DE VECTORIZACIÓN
# ============================================================================

# Parámetros de TF-IDF
TFIDF_CONFIG = {
    'max_features': 10000,
    'ngram_range': (1, 2),
    'min_df': 2,
    'max_df': 0.95,
    'stop_words': 'english'
}

# ============================================================================
# CONFIGURACIÓN DE MODELOS
# ============================================================================

# Parámetros de Naive Bayes
NAIVE_BAYES_CONFIG = {
    'alpha': 1.0
}

# Parámetros de Logistic Regression
LOGISTIC_REGRESSION_CONFIG = {
    'C': 1.0,
    'max_iter': 1000,
    'class_weight': 'balanced'
}

# Parámetros de Linear SVM
LINEAR_SVM_CONFIG = {
    'C': 1.0,
    'max_iter': 2000,
    'class_weight': 'balanced'
}

# Parámetros de Random Forest
RANDOM_FOREST_CONFIG = {
    'n_estimators': 100,
    'max_depth': 50,
    'class_weight': 'balanced'
}

# ============================================================================
# CONFIGURACIÓN DE EVALUACIÓN
# ============================================================================

# Métrica principal para selección de modelo
PRIMARY_METRIC = 'f1'

# Métricas a calcular
METRICS_TO_COMPUTE = [
    'accuracy',
    'precision',
    'recall',
    'f1',
    'roc_auc'
]

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================

# Nivel de logging
LOG_LEVEL = 'INFO'

# Formato de logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Archivo de log
LOG_FILE = ROOT_DIR / 'training.log'

# ============================================================================
# CONFIGURACIÓN DE OPTIMIZACIÓN DE HIPERPARÁMETROS
# ============================================================================

# Número de folds para cross-validation
CV_FOLDS = 5

# Grid de búsqueda para Logistic Regression
LR_PARAM_GRID = {
    'C': [0.1, 1.0, 10.0],
    'max_iter': [1000, 2000]
}

# Grid de búsqueda para Linear SVM
SVM_PARAM_GRID = {
    'C': [0.1, 1.0, 10.0]
}

# Grid de búsqueda para Random Forest
RF_PARAM_GRID = {
    'n_estimators': [50, 100, 200],
    'max_depth': [30, 50, None]
}

# ============================================================================
# CONFIGURACIÓN DE VISUALIZACIÓN
# ============================================================================

# DPI para gráficos
FIGURE_DPI = 300

# Tamaño de figura por defecto
DEFAULT_FIGSIZE = (12, 6)

# Colores para clases
CLASS_COLORS = ['#FF6B6B', '#4ECDC4']

# ============================================================================
# UTILIDADES
# ============================================================================

def get_config_summary() -> str:
    """
    Retorna un resumen de la configuración actual.

    Returns:
        String con resumen de configuración
    """
    summary = f"""
    ============================================================
    CONFIGURACIÓN DEL PROYECTO
    ============================================================

    Rutas:
      - Directorio raíz: {ROOT_DIR}
      - Datos: {DATA_DIR}
      - Modelos: {MODELS_DIR}
      - Resultados: {RESULTS_DIR}

    Datasets:
      - MIND: {MIND_TSV}
      - Google: {GOOGLE_TSV}

    División de datos:
      - Train: {TRAIN_SIZE*100:.0f}%
      - Validation: {VAL_SIZE*100:.0f}%
      - Test: {TEST_SIZE*100:.0f}%
      - Random State: {RANDOM_STATE}

    Clases:
      - Clase 0 (Actualidad): {len(ACTUALIDAD_CATEGORIES)} categorías
      - Clase 1 (Interés General): {len(INTERES_GENERAL_CATEGORIES)} categorías

    Vectorización:
      - Método: TF-IDF
      - Max features: {TFIDF_CONFIG['max_features']}
      - N-gramas: {TFIDF_CONFIG['ngram_range']}

    Evaluación:
      - Métrica principal: {PRIMARY_METRIC}
      - Métricas: {', '.join(METRICS_TO_COMPUTE)}

    ============================================================
    """
    return summary


def validate_paths() -> bool:
    """
    Valida que las rutas necesarias existan.

    Returns:
        True si todas las rutas existen, False en caso contrario
    """
    required_paths = [DATA_DIR, MODELS_DIR, RESULTS_DIR]

    for path in required_paths:
        if not path.exists():
            print(f"⚠️ Ruta no encontrada: {path}")
            return False

    return True


if __name__ == "__main__":
    print(get_config_summary())

    if validate_paths():
        print("✓ Todas las rutas están configuradas correctamente")
    else:
        print("⚠️ Algunas rutas no existen. Se crearán automáticamente.")
