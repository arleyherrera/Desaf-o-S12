"""
evaluation.py
Módulo de evaluación de modelos para el clasificador de noticias.

Autor: Equipo de Desarrollo
Fecha: Noviembre 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score, roc_curve
)
from typing import Dict, Any, Optional, Tuple


def evaluate_model(model,
                  X_test,
                  y_test,
                  model_name: str = "Model") -> Dict[str, float]:
    """
    Evalúa un modelo y retorna métricas completas.

    Args:
        model: Modelo entrenado
        X_test: Features de test
        y_test: Etiquetas verdaderas de test
        model_name: Nombre del modelo

    Returns:
        Diccionario con métricas de evaluación
    """
    # Predicciones
    y_pred = model.predict(X_test)

    # Probabilidades o scores
    if hasattr(model, 'predict_proba'):
        y_proba = model.predict_proba(X_test)[:, 1]
    elif hasattr(model, 'decision_function'):
        y_proba = model.decision_function(X_test)
    else:
        y_proba = None

    # Calcular métricas
    metrics = {
        'model_name': model_name,
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='binary'),
        'recall': recall_score(y_test, y_pred, average='binary'),
        'f1': f1_score(y_test, y_pred, average='binary'),
    }

    if y_proba is not None:
        metrics['roc_auc'] = roc_auc_score(y_test, y_proba)

    return metrics


def print_evaluation_report(metrics: Dict[str, float],
                           y_test,
                           y_pred,
                           class_names: Optional[list] = None):
    """
    Imprime un reporte completo de evaluación.

    Args:
        metrics: Diccionario con métricas
        y_test: Etiquetas verdaderas
        y_pred: Predicciones
        class_names: Nombres de las clases
    """
    if class_names is None:
        class_names = ['Clase 0', 'Clase 1']

    print("=" * 70)
    print(f"REPORTE DE EVALUACIÓN - {metrics.get('model_name', 'Model')}")
    print("=" * 70)

    print(f"\nMétricas generales:")
    print(f"  Accuracy:  {metrics['accuracy']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  Recall:    {metrics['recall']:.4f}")
    print(f"  F1-Score:  {metrics['f1']:.4f}")

    if 'roc_auc' in metrics:
        print(f"  ROC-AUC:   {metrics['roc_auc']:.4f}")

    print(f"\nReporte de clasificación detallado:")
    print(classification_report(y_test, y_pred, target_names=class_names, digits=4))
    print("=" * 70)


def plot_confusion_matrix(y_test,
                         y_pred,
                         class_names: Optional[list] = None,
                         title: str = "Matriz de Confusión",
                         figsize: Tuple[int, int] = (8, 6),
                         save_path: Optional[str] = None):
    """
    Grafica la matriz de confusión.

    Args:
        y_test: Etiquetas verdaderas
        y_pred: Predicciones
        class_names: Nombres de las clases
        title: Título del gráfico
        figsize: Tamaño de la figura
        save_path: Ruta para guardar el gráfico (opcional)
    """
    if class_names is None:
        class_names = ['Clase 0', 'Clase 1']

    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=figsize)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names,
                cbar_kws={'label': 'Frecuencia'})
    plt.ylabel('Clase Real')
    plt.xlabel('Clase Predicha')
    plt.title(title)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en: {save_path}")

    plt.show()


def plot_roc_curve(y_test,
                  y_proba,
                  model_name: str = "Model",
                  figsize: Tuple[int, int] = (8, 6),
                  save_path: Optional[str] = None):
    """
    Grafica la curva ROC.

    Args:
        y_test: Etiquetas verdaderas
        y_proba: Probabilidades o scores predichos
        model_name: Nombre del modelo
        figsize: Tamaño de la figura
        save_path: Ruta para guardar el gráfico (opcional)
    """
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    auc = roc_auc_score(y_test, y_proba)

    plt.figure(figsize=figsize)
    plt.plot(fpr, tpr, label=f'{model_name} (AUC = {auc:.4f})', linewidth=2)
    plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier', linewidth=1)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'Curva ROC - {model_name}')
    plt.legend(loc='lower right')
    plt.grid(alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en: {save_path}")

    plt.show()


def compare_models(results: Dict[str, Dict[str, Any]],
                  metric: str = 'f1',
                  figsize: Tuple[int, int] = (12, 6),
                  save_path: Optional[str] = None):
    """
    Compara múltiples modelos visualmente.

    Args:
        results: Diccionario con resultados de cada modelo
        metric: Métrica para comparar
        figsize: Tamaño de la figura
        save_path: Ruta para guardar el gráfico (opcional)
    """
    model_names = list(results.keys())
    values = [results[name]['metrics'][metric] for name in model_names]

    plt.figure(figsize=figsize)
    bars = plt.bar(model_names, values, color='steelblue', edgecolor='black', alpha=0.7)
    plt.ylabel(metric.upper())
    plt.title(f'Comparación de Modelos - {metric.upper()}')
    plt.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')

    # Añadir valores en las barras
    for bar, value in zip(bars, values):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.4f}',
                ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en: {save_path}")

    plt.show()


def create_comparison_table(results: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """
    Crea una tabla comparativa de modelos.

    Args:
        results: Diccionario con resultados de cada modelo

    Returns:
        DataFrame con comparación de modelos
    """
    comparison_data = []

    for model_name, result in results.items():
        metrics = result['metrics']
        row = {
            'Model': model_name,
            'Accuracy': f"{metrics['accuracy']:.4f}",
            'Precision': f"{metrics['precision']:.4f}",
            'Recall': f"{metrics['recall']:.4f}",
            'F1-Score': f"{metrics['f1']:.4f}",
            'ROC-AUC': f"{metrics.get('roc_auc', 0):.4f}"
        }
        comparison_data.append(row)

    return pd.DataFrame(comparison_data)


def analyze_errors(y_test,
                  y_pred,
                  X_test_texts: Optional[pd.Series] = None,
                  n_examples: int = 10) -> pd.DataFrame:
    """
    Analiza los errores de clasificación.

    Args:
        y_test: Etiquetas verdaderas
        y_pred: Predicciones
        X_test_texts: Textos de test (opcional)
        n_examples: Número de ejemplos a mostrar

    Returns:
        DataFrame con análisis de errores
    """
    # Identificar errores
    errors_mask = y_test != y_pred
    error_indices = np.where(errors_mask)[0]

    print(f"Total de errores: {len(error_indices)} ({len(error_indices)/len(y_test)*100:.2f}%)")

    if len(error_indices) == 0:
        print("No hay errores para analizar")
        return pd.DataFrame()

    # Crear DataFrame de errores
    error_data = {
        'index': error_indices[:n_examples],
        'true_label': y_test.iloc[error_indices[:n_examples]].values if hasattr(y_test, 'iloc') else y_test[error_indices[:n_examples]],
        'predicted_label': y_pred[error_indices[:n_examples]]
    }

    if X_test_texts is not None:
        error_data['text'] = X_test_texts.iloc[error_indices[:n_examples]].values if hasattr(X_test_texts, 'iloc') else X_test_texts[error_indices[:n_examples]]

    errors_df = pd.DataFrame(error_data)

    return errors_df


if __name__ == "__main__":
    # Ejemplo de uso
    print("Módulo de evaluación de modelos")
    print("Importar este módulo en notebooks o scripts para usar sus funciones")
