"""
train.py
Script principal para entrenar el clasificador de noticias.

Buenas prácticas aplicadas:
- Logging detallado
- Manejo de errores
- Configuración centralizada
- Código modular y reutilizable
- Documentación completa
- Validación de datos
- Guardado automático de modelos y métricas

Uso:
    python train.py

Autor: 
Fecha: Noviembre 2025
"""

import logging
import sys
import json
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.metrics import classification_report

# Importar módulos propios
from config import *
from src.preprocessing import clean_text, map_to_binary_class
from src.feature_engineering import create_tfidf_vectorizer
from src.models import (
    create_naive_bayes,
    create_logistic_regression,
    create_linear_svm,
    create_random_forest,
    save_model
)
from src.evaluation import evaluate_model, print_evaluation_report


# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================

def setup_logging():
    """Configura el sistema de logging."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logging()


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def load_data():
    """
    Carga los conjuntos de datos de entrenamiento y validación.

    Returns:
        Tuple con (train_df, val_df)

    Raises:
        FileNotFoundError: Si los archivos no existen
    """
    logger.info("Cargando datos...")

    try:
        train_df = pd.read_csv(TRAIN_CSV)
        val_df = pd.read_csv(VAL_CSV)

        logger.info(f"  OK Train: {len(train_df):,} registros")
        logger.info(f"  OK Validation: {len(val_df):,} registros")

        return train_df, val_df

    except FileNotFoundError as e:
        logger.error(f"ERROR Error al cargar datos: {e}")
        logger.error("Asegúrate de ejecutar los notebooks de preprocesamiento primero")
        raise


def validate_data(df, dataset_name="Dataset"):
    """
    Valida la integridad de los datos.

    Args:
        df: DataFrame a validar
        dataset_name: Nombre del dataset para logging
    """
    logger.info(f"Validando {dataset_name}...")

    # Verificar valores faltantes
    missing = df.isnull().sum().sum()
    if missing > 0:
        logger.warning(f"  ⚠️ {dataset_name} tiene {missing} valores faltantes")
    else:
        logger.info(f"  OK Sin valores faltantes")

    # Verificar distribución de clases
    if 'label' in df.columns:
        class_dist = df['label'].value_counts()
        logger.info(f"  Distribución de clases:")
        for label, count in class_dist.items():
            pct = count / len(df) * 100
            logger.info(f"    Clase {label}: {count:,} ({pct:.2f}%)")


def vectorize_data(train_df, val_df):
    """
    Vectoriza los textos usando TF-IDF.

    Args:
        train_df: DataFrame de entrenamiento
        val_df: DataFrame de validación

    Returns:
        Tuple con (vectorizer, X_train, y_train, X_val, y_val)
    """
    logger.info("Vectorizando textos con TF-IDF...")

    # Crear vectorizador
    vectorizer = create_tfidf_vectorizer(**TFIDF_CONFIG)

    # Separar features y labels
    X_train_text = train_df['text']
    y_train = train_df['label'].values

    X_val_text = val_df['text']
    y_val = val_df['label'].values

    # Vectorizar
    X_train = vectorizer.fit_transform(X_train_text)
    X_val = vectorizer.transform(X_val_text)

    logger.info(f"  OK X_train: {X_train.shape}")
    logger.info(f"  OK X_val: {X_val.shape}")
    logger.info(f"  OK Vocabulario: {len(vectorizer.vocabulary_):,} términos")

    return vectorizer, X_train, y_train, X_val, y_val


def train_models(X_train, y_train, X_val, y_val):
    """
    Entrena múltiples modelos de clasificación.

    Args:
        X_train: Features de entrenamiento
        y_train: Labels de entrenamiento
        X_val: Features de validación
        y_val: Labels de validación

    Returns:
        Dict con resultados de cada modelo
    """
    logger.info("=" * 70)
    logger.info("ENTRENAMIENTO DE MODELOS")
    logger.info("=" * 70)

    results = {}

    # Definir modelos
    models_to_train = {
        'Naive Bayes': create_naive_bayes(**NAIVE_BAYES_CONFIG),
        'Logistic Regression': create_logistic_regression(**LOGISTIC_REGRESSION_CONFIG),
        'Linear SVM': create_linear_svm(**LINEAR_SVM_CONFIG),
        'Random Forest': create_random_forest(**RANDOM_FOREST_CONFIG)
    }

    # Entrenar cada modelo
    for model_name, model in models_to_train.items():
        logger.info(f"\n Entrenando: {model_name}")
        start_time = time.time()

        try:
            # Entrenar
            model.fit(X_train, y_train)
            train_time = time.time() - start_time
            logger.info(f"  OK Entrenamiento completado en {train_time:.2f}s")

            # Evaluar
            metrics = evaluate_model(model, X_val, y_val, model_name)

            # Predicciones
            y_pred = model.predict(X_val)

            # Guardar resultados
            results[model_name] = {
                'model': model,
                'metrics': metrics,
                'y_pred': y_pred,
                'train_time': train_time
            }

            # Log métricas
            logger.info(f"  Métricas en validación:")
            logger.info(f"    Accuracy:  {metrics['accuracy']:.4f}")
            logger.info(f"    Precision: {metrics['precision']:.4f}")
            logger.info(f"    Recall:    {metrics['recall']:.4f}")
            logger.info(f"    F1-Score:  {metrics['f1']:.4f}")
            if 'roc_auc' in metrics:
                logger.info(f"    ROC-AUC:   {metrics['roc_auc']:.4f}")

        except Exception as e:
            logger.error(f"  ERROR Error al entrenar {model_name}: {e}")
            continue

    return results


def select_best_model(results):
    """
    Selecciona el mejor modelo basado en la métrica principal.

    Args:
        results: Dict con resultados de cada modelo

    Returns:
        Tuple con (nombre_mejor_modelo, datos_mejor_modelo)
    """
    logger.info("\n" + "=" * 70)
    logger.info("SELECCIÓN DEL MEJOR MODELO")
    logger.info("=" * 70)

    best_model_name = max(results.keys(),
                         key=lambda x: results[x]['metrics'][PRIMARY_METRIC])
    best_model_data = results[best_model_name]

    logger.info(f"\n Mejor modelo: {best_model_name}")
    logger.info(f"   {PRIMARY_METRIC.upper()}: {best_model_data['metrics'][PRIMARY_METRIC]:.4f}")

    return best_model_name, best_model_data


def save_results(vectorizer, best_model_name, best_model_data, results):
    """
    Guarda los modelos, vectorizador y métricas.

    Args:
        vectorizer: Vectorizador TF-IDF
        best_model_name: Nombre del mejor modelo
        best_model_data: Datos del mejor modelo
        results: Resultados de todos los modelos
    """
    logger.info("\n" + "=" * 70)
    logger.info("GUARDANDO RESULTADOS")
    logger.info("=" * 70)

    try:
        # Guardar mejor modelo
        save_model(best_model_data['model'], BEST_MODEL_PATH)
        logger.info(f"  OK Modelo guardado: {BEST_MODEL_PATH}")

        # Guardar vectorizador
        save_model(vectorizer, VECTORIZER_PATH)
        logger.info(f"  OK Vectorizador guardado: {VECTORIZER_PATH}")

        # Guardar métricas de entrenamiento
        training_metrics = {
            'timestamp': datetime.now().isoformat(),
            'best_model': best_model_name,
            'validation_metrics': {k: float(v) if isinstance(v, np.floating) else v
                                  for k, v in best_model_data['metrics'].items()
                                  if k != 'model_name'},
            'all_models': {
                name: {k: float(v) if isinstance(v, np.floating) else v
                      for k, v in data['metrics'].items() if k != 'model_name'}
                for name, data in results.items()
            }
        }

        metrics_path = RESULTS_DIR / 'training_metrics.json'
        with open(metrics_path, 'w') as f:
            json.dump(training_metrics, f, indent=4)
        logger.info(f"  OK Métricas guardadas: {metrics_path}")

        # Crear tabla comparativa
        comparison_data = []
        for model_name, result in results.items():
            metrics = result['metrics']
            row = {
                'Model': model_name,
                'Accuracy': f"{metrics['accuracy']:.4f}",
                'Precision': f"{metrics['precision']:.4f}",
                'Recall': f"{metrics['recall']:.4f}",
                'F1-Score': f"{metrics['f1']:.4f}",
                'ROC-AUC': f"{metrics.get('roc_auc', 0):.4f}",
                'Train Time (s)': f"{result['train_time']:.2f}"
            }
            comparison_data.append(row)

        comparison_df = pd.DataFrame(comparison_data)
        comparison_path = RESULTS_DIR / 'model_comparison_training.csv'
        comparison_df.to_csv(comparison_path, index=False)
        logger.info(f"  OK Comparación guardada: {comparison_path}")

    except Exception as e:
        logger.error(f"  ERROR Error al guardar resultados: {e}")
        raise


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal del script de entrenamiento."""

    logger.info("\n" + "=" * 70)
    logger.info("CLASIFICADOR DE NOTICIAS - ENTRENAMIENTO")
    logger.info("Actualidad vs Interés General")
    logger.info("=" * 70)
    logger.info(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Random State: {RANDOM_STATE}")

    try:
        # 1. Cargar datos
        train_df, val_df = load_data()

        # 2. Validar datos
        validate_data(train_df, "Training Set")
        validate_data(val_df, "Validation Set")

        # 3. Vectorizar textos
        vectorizer, X_train, y_train, X_val, y_val = vectorize_data(train_df, val_df)

        # 4. Entrenar modelos
        results = train_models(X_train, y_train, X_val, y_val)

        if not results:
            logger.error("ERROR No se entrenó ningún modelo exitosamente")
            return 1

        # 5. Seleccionar mejor modelo
        best_model_name, best_model_data = select_best_model(results)

        # 6. Guardar resultados
        save_results(vectorizer, best_model_name, best_model_data, results)

        # 7. Resumen final
        logger.info("\n" + "=" * 70)
        logger.info("ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
        logger.info("=" * 70)
        logger.info(f"\n Resumen:")
        logger.info(f"  - Modelos entrenados: {len(results)}")
        logger.info(f"  - Mejor modelo: {best_model_name}")
        logger.info(f"  - {PRIMARY_METRIC.upper()}: {best_model_data['metrics'][PRIMARY_METRIC]:.4f}")
        logger.info(f"\n Archivos generados:")
        logger.info(f"  - Modelo: {BEST_MODEL_PATH}")
        logger.info(f"  - Vectorizador: {VECTORIZER_PATH}")
        logger.info(f"  - Métricas: {RESULTS_DIR / 'training_metrics.json'}")
        logger.info(f"  - Comparación: {RESULTS_DIR / 'model_comparison_training.csv'}")
        logger.info("\nOK Siguiente paso: Ejecutar evaluate.py para evaluación en test set")

        return 0

    except Exception as e:
        logger.error(f"\nERROR Error crítico durante el entrenamiento: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
