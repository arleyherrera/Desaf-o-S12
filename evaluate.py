"""
evaluate.py
Script para evaluar el mejor modelo en el conjunto de test.

Buenas prácticas aplicadas:
- Evaluación completa con todas las métricas
- Generación de visualizaciones
- Análisis de errores
- Guardado de predicciones
- Reporte detallado

Uso:
    python evaluate.py

Autor: 
Fecha: Noviembre 2025
"""

import logging
import sys
import json
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score, roc_curve
)

# Importar módulos propios
from config import *
from src.models import load_model
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
            logging.FileHandler(RESULTS_DIR / 'evaluation.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logging()


# ============================================================================
# FUNCIONES DE EVALUACIÓN
# ============================================================================

def load_test_data():
    """
    Carga el conjunto de test.

    Returns:
        DataFrame de test

    Raises:
        FileNotFoundError: Si el archivo no existe
    """
    logger.info("Cargando conjunto de test...")

    try:
        test_df = pd.read_csv(TEST_CSV)
        logger.info(f"  OK Test: {len(test_df):,} registros")

        # Verificar distribución de clases
        class_dist = test_df['label'].value_counts()
        logger.info(f"  Distribución de clases:")
        for label, count in class_dist.items():
            pct = count / len(test_df) * 100
            class_name = CLASS_NAMES[label]
            logger.info(f"    Clase {label} ({class_name}): {count:,} ({pct:.2f}%)")

        return test_df

    except FileNotFoundError as e:
        logger.error(f"ERROR Error al cargar datos: {e}")
        raise


def load_trained_model():
    """
    Carga el modelo y vectorizador entrenados.

    Returns:
        Tuple con (model, vectorizer)

    Raises:
        FileNotFoundError: Si los archivos no existen
    """
    logger.info("Cargando modelo entrenado...")

    try:
        model = load_model(BEST_MODEL_PATH)
        logger.info(f"  OK Modelo cargado: {type(model).__name__}")

        vectorizer = load_model(VECTORIZER_PATH)
        logger.info(f"  OK Vectorizador cargado")
        logger.info(f"  OK Vocabulario: {len(vectorizer.vocabulary_):,} términos")

        return model, vectorizer

    except FileNotFoundError as e:
        logger.error(f"ERROR Error: {e}")
        logger.error("Ejecuta train.py primero para entrenar el modelo")
        raise


def evaluate_on_test(model, vectorizer, test_df):
    """
    Evalúa el modelo en el conjunto de test.

    Args:
        model: Modelo entrenado
        vectorizer: Vectorizador TF-IDF
        test_df: DataFrame de test

    Returns:
        Tuple con (y_test, y_pred, y_proba, metrics)
    """
    logger.info("\n" + "=" * 70)
    logger.info("EVALUACIÓN EN CONJUNTO DE TEST")
    logger.info("=" * 70)

    # Preparar datos
    X_test_text = test_df['text']
    y_test = test_df['label'].values

    # Vectorizar
    logger.info("Vectorizando textos de test...")
    X_test = vectorizer.transform(X_test_text)
    logger.info(f"  OK X_test: {X_test.shape}")

    # Predicciones
    logger.info("Generando predicciones...")
    y_pred = model.predict(X_test)

    # Probabilidades o scores
    if hasattr(model, 'predict_proba'):
        y_proba = model.predict_proba(X_test)[:, 1]
    elif hasattr(model, 'decision_function'):
        y_proba = model.decision_function(X_test)
    else:
        y_proba = None

    # Calcular métricas
    logger.info("Calculando métricas...")
    metrics = {
        'model_name': type(model).__name__,
        'test_size': len(y_test),
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='binary'),
        'recall': recall_score(y_test, y_pred, average='binary'),
        'f1': f1_score(y_test, y_pred, average='binary'),
    }

    if y_proba is not None:
        metrics['roc_auc'] = roc_auc_score(y_test, y_proba)

    # Mostrar resultados
    logger.info(f"\n Resultados en Test Set:")
    logger.info(f"  Accuracy:  {metrics['accuracy']:.4f}")
    logger.info(f"  Precision: {metrics['precision']:.4f}")
    logger.info(f"  Recall:    {metrics['recall']:.4f}")
    logger.info(f"  F1-Score:  {metrics['f1']:.4f}")
    if 'roc_auc' in metrics:
        logger.info(f"  ROC-AUC:   {metrics['roc_auc']:.4f}")

    return y_test, y_pred, y_proba, metrics


def plot_confusion_matrix_test(y_test, y_pred):
    """
    Grafica la matriz de confusión del test set.

    Args:
        y_test: Etiquetas verdaderas
        y_pred: Predicciones
    """
    logger.info("\nGenerando matriz de confusión...")

    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES,
                cbar_kws={'label': 'Frecuencia'}, annot_kws={'size': 16})
    plt.ylabel('Clase Real', fontsize=14)
    plt.xlabel('Clase Predicha', fontsize=14)
    plt.title('Matriz de Confusión - Conjunto de Test', fontsize=16, fontweight='bold')
    plt.tight_layout()

    save_path = RESULTS_DIR / 'confusion_matrix_final_test.png'
    plt.savefig(save_path, dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()

    logger.info(f"  OK Matriz guardada: {save_path}")


def plot_roc_curve_test(y_test, y_proba):
    """
    Grafica la curva ROC del test set.

    Args:
        y_test: Etiquetas verdaderas
        y_proba: Probabilidades/scores predichos
    """
    if y_proba is None:
        logger.warning("  WARNING No se pueden calcular probabilidades para ROC")
        return

    logger.info("Generando curva ROC...")

    fpr, tpr, _ = roc_curve(y_test, y_proba)
    auc = roc_auc_score(y_test, y_proba)

    plt.figure(figsize=(10, 8))
    plt.plot(fpr, tpr, label=f'Modelo (AUC = {auc:.4f})', linewidth=3, color='#FF6B6B')
    plt.plot([0, 1], [0, 1], 'k--', label='Clasificador Aleatorio', linewidth=2)
    plt.xlabel('False Positive Rate', fontsize=14)
    plt.ylabel('True Positive Rate', fontsize=14)
    plt.title('Curva ROC - Conjunto de Test', fontsize=16, fontweight='bold')
    plt.legend(loc='lower right', fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()

    save_path = RESULTS_DIR / 'roc_curve_final_test.png'
    plt.savefig(save_path, dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()

    logger.info(f"  OK Curva ROC guardada: {save_path}")


def analyze_errors(test_df, y_test, y_pred):
    """
    Analiza los errores de clasificación.

    Args:
        test_df: DataFrame de test
        y_test: Etiquetas verdaderas
        y_pred: Predicciones

    Returns:
        DataFrame con análisis de errores
    """
    logger.info("\n" + "=" * 70)
    logger.info("ANÁLISIS DE ERRORES")
    logger.info("=" * 70)

    # Crear DataFrame de resultados
    results_df = test_df.copy()
    results_df['predicted_label'] = y_pred
    results_df['predicted_class'] = results_df['predicted_label'].map(
        {i: name for i, name in enumerate(CLASS_NAMES)}
    )
    results_df['correct'] = (results_df['label'] == results_df['predicted_label'])

    # Identificar errores
    errors_df = results_df[~results_df['correct']].copy()
    correct_df = results_df[results_df['correct']].copy()

    logger.info(f"\nPredicciones correctas: {len(correct_df):,} ({len(correct_df)/len(results_df)*100:.2f}%)")
    logger.info(f"Predicciones incorrectas: {len(errors_df):,} ({len(errors_df)/len(results_df)*100:.2f}%)")

    if len(errors_df) > 0:
        logger.info(f"\nTipos de errores:")

        # Falsos positivos y falsos negativos
        fp = errors_df[errors_df['predicted_label'] == 1]  # Predijo Interés General siendo Actualidad
        fn = errors_df[errors_df['predicted_label'] == 0]  # Predijo Actualidad siendo Interés General

        logger.info(f"  Falsos Positivos: {len(fp):,} (predijo Interés General, era Actualidad)")
        logger.info(f"  Falsos Negativos: {len(fn):,} (predijo Actualidad, era Interés General)")

        # Mostrar ejemplos
        logger.info(f"\n Ejemplos de errores:")
        sample_errors = errors_df.sample(min(5, len(errors_df)))
        for idx, row in sample_errors.iterrows():
            logger.info(f"\n  Texto: '{row['text'][:80]}...'")
            logger.info(f"    Real: {row['class_name']} | Predicho: {row['predicted_class']}")

    # Guardar predicciones completas
    save_path = RESULTS_DIR / 'test_predictions_final.csv'
    results_df.to_csv(save_path, index=False)
    logger.info(f"\nOK Predicciones guardadas: {save_path}")

    # Guardar solo errores
    if len(errors_df) > 0:
        errors_path = RESULTS_DIR / 'test_errors.csv'
        errors_df.to_csv(errors_path, index=False)
        logger.info(f"OK Errores guardados: {errors_path}")

    return results_df, errors_df


def save_final_metrics(metrics):
    """
    Guarda las métricas finales en JSON.

    Args:
        metrics: Diccionario con métricas
    """
    logger.info("\nGuardando métricas finales...")

    final_metrics = {
        'timestamp': datetime.now().isoformat(),
        'dataset': 'test',
        **{k: float(v) if isinstance(v, np.floating) else v
           for k, v in metrics.items()}
    }

    save_path = RESULTS_DIR / 'final_test_metrics.json'
    with open(save_path, 'w') as f:
        json.dump(final_metrics, f, indent=4)

    logger.info(f"  OK Métricas guardadas: {save_path}")


def generate_classification_report(y_test, y_pred):
    """
    Genera y guarda el reporte de clasificación detallado.

    Args:
        y_test: Etiquetas verdaderas
        y_pred: Predicciones
    """
    logger.info("\n" + "=" * 70)
    logger.info("REPORTE DE CLASIFICACIÓN DETALLADO")
    logger.info("=" * 70)

    report = classification_report(y_test, y_pred, target_names=CLASS_NAMES, digits=4)
    logger.info(f"\n{report}")

    # Guardar reporte
    save_path = RESULTS_DIR / 'classification_report_test.txt'
    with open(save_path, 'w') as f:
        f.write("REPORTE DE CLASIFICACIÓN - CONJUNTO DE TEST\n")
        f.write("=" * 70 + "\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(report)

    logger.info(f"\nOK Reporte guardado: {save_path}")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal del script de evaluación."""

    logger.info("\n" + "=" * 70)
    logger.info("CLASIFICADOR DE NOTICIAS - EVALUACIÓN FINAL")
    logger.info("Actualidad vs Interés General")
    logger.info("=" * 70)
    logger.info(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # 1. Cargar datos de test
        test_df = load_test_data()

        # 2. Cargar modelo entrenado
        model, vectorizer = load_trained_model()

        # 3. Evaluar en test set
        y_test, y_pred, y_proba, metrics = evaluate_on_test(model, vectorizer, test_df)

        # 4. Generar visualizaciones
        logger.info("\n" + "=" * 70)
        logger.info("GENERANDO VISUALIZACIONES")
        logger.info("=" * 70)
        plot_confusion_matrix_test(y_test, y_pred)
        plot_roc_curve_test(y_test, y_proba)

        # 5. Análisis de errores
        results_df, errors_df = analyze_errors(test_df, y_test, y_pred)

        # 6. Reporte de clasificación
        generate_classification_report(y_test, y_pred)

        # 7. Guardar métricas finales
        save_final_metrics(metrics)

        # 8. Resumen final
        logger.info("\n" + "=" * 70)
        logger.info("EVALUACIÓN COMPLETADA EXITOSAMENTE")
        logger.info("=" * 70)
        logger.info(f"\n Métricas Finales:")
        logger.info(f"  - Accuracy:  {metrics['accuracy']:.4f}")
        logger.info(f"  - Precision: {metrics['precision']:.4f}")
        logger.info(f"  - Recall:    {metrics['recall']:.4f}")
        logger.info(f"  - F1-Score:  {metrics['f1']:.4f}")
        if 'roc_auc' in metrics:
            logger.info(f"  - ROC-AUC:   {metrics['roc_auc']:.4f}")

        logger.info(f"\n Archivos generados:")
        logger.info(f"  - Métricas: {RESULTS_DIR / 'final_test_metrics.json'}")
        logger.info(f"  - Predicciones: {RESULTS_DIR / 'test_predictions_final.csv'}")
        logger.info(f"  - Errores: {RESULTS_DIR / 'test_errors.csv'}")
        logger.info(f"  - Matriz confusión: {RESULTS_DIR / 'confusion_matrix_final_test.png'}")
        logger.info(f"  - Curva ROC: {RESULTS_DIR / 'roc_curve_final_test.png'}")
        logger.info(f"  - Reporte: {RESULTS_DIR / 'classification_report_test.txt'}")

        logger.info("\nOK Proyecto completado exitosamente")

        return 0

    except Exception as e:
        logger.error(f"\nERROR Error crítico durante la evaluación: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
