"""
Módulo src para el Clasificador de Noticias.

Contiene funciones de preprocesamiento, feature engineering, modelos y evaluación.
"""

from .preprocessing import (
    clean_text,
    map_to_binary_class,
    remove_duplicates,
    preprocess_dataset
)

from .feature_engineering import (
    create_tfidf_vectorizer,
    vectorize_text,
    add_text_features
)

from .models import (
    create_naive_bayes,
    create_logistic_regression,
    create_linear_svm,
    create_random_forest,
    get_default_models,
    train_model,
    save_model,
    load_model
)

from .evaluation import (
    evaluate_model,
    print_evaluation_report,
    plot_confusion_matrix,
    plot_roc_curve,
    compare_models,
    create_comparison_table,
    analyze_errors
)

__all__ = [
    # preprocessing
    'clean_text',
    'map_to_binary_class',
    'remove_duplicates',
    'preprocess_dataset',
    # feature_engineering
    'create_tfidf_vectorizer',
    'vectorize_text',
    'add_text_features',
    # models
    'create_naive_bayes',
    'create_logistic_regression',
    'create_linear_svm',
    'create_random_forest',
    'get_default_models',
    'train_model',
    'save_model',
    'load_model',
    # evaluation
    'evaluate_model',
    'print_evaluation_report',
    'plot_confusion_matrix',
    'plot_roc_curve',
    'compare_models',
    'create_comparison_table',
    'analyze_errors'
]
