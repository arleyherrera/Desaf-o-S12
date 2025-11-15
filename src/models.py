"""
models.py
Módulo de definición y entrenamiento de modelos para el clasificador de noticias.

Autor: Equipo de Desarrollo
Fecha: Noviembre 2024
"""

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from typing import Dict, Any, Optional
import pickle


RANDOM_STATE = 42


def create_naive_bayes(alpha: float = 1.0) -> MultinomialNB:
    """
    Crea un clasificador Naive Bayes.

    Args:
        alpha: Parámetro de suavizado

    Returns:
        Modelo Naive Bayes
    """
    return MultinomialNB(alpha=alpha)


def create_logistic_regression(C: float = 1.0,
                               max_iter: int = 1000,
                               class_weight: str = 'balanced') -> LogisticRegression:
    """
    Crea un clasificador de Regresión Logística.

    Args:
        C: Inverso de la fuerza de regularización
        max_iter: Número máximo de iteraciones
        class_weight: Pesos de clases ('balanced' o None)

    Returns:
        Modelo de Regresión Logística
    """
    return LogisticRegression(
        C=C,
        max_iter=max_iter,
        class_weight=class_weight,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )


def create_linear_svm(C: float = 1.0,
                     max_iter: int = 2000,
                     class_weight: str = 'balanced') -> LinearSVC:
    """
    Crea un clasificador SVM lineal.

    Args:
        C: Parámetro de regularización
        max_iter: Número máximo de iteraciones
        class_weight: Pesos de clases ('balanced' o None)

    Returns:
        Modelo Linear SVM
    """
    return LinearSVC(
        C=C,
        max_iter=max_iter,
        class_weight=class_weight,
        random_state=RANDOM_STATE
    )


def create_random_forest(n_estimators: int = 100,
                        max_depth: Optional[int] = 50,
                        class_weight: str = 'balanced') -> RandomForestClassifier:
    """
    Crea un clasificador Random Forest.

    Args:
        n_estimators: Número de árboles
        max_depth: Profundidad máxima de árboles
        class_weight: Pesos de clases ('balanced' o None)

    Returns:
        Modelo Random Forest
    """
    return RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        class_weight=class_weight,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )


def get_default_models() -> Dict[str, Any]:
    """
    Retorna un diccionario con modelos por defecto.

    Returns:
        Diccionario con modelos predefinidos
    """
    models = {
        'Naive Bayes': create_naive_bayes(),
        'Logistic Regression': create_logistic_regression(),
        'Linear SVM': create_linear_svm(),
        'Random Forest': create_random_forest()
    }

    return models


def train_model(model, X_train, y_train, verbose: bool = True):
    """
    Entrena un modelo.

    Args:
        model: Modelo a entrenar
        X_train: Features de entrenamiento
        y_train: Etiquetas de entrenamiento
        verbose: Mostrar mensajes

    Returns:
        Modelo entrenado
    """
    if verbose:
        print(f"Entrenando {type(model).__name__}...")

    model.fit(X_train, y_train)

    if verbose:
        print(f"  Entrenamiento completado")

    return model


def optimize_hyperparameters(model_type: str,
                            X_train, y_train,
                            param_grid: Dict[str, list],
                            cv: int = 5,
                            scoring: str = 'f1',
                            verbose: int = 1):
    """
    Optimiza hiperparámetros usando Grid Search.

    Args:
        model_type: Tipo de modelo ('nb', 'lr', 'svm', 'rf')
        X_train: Features de entrenamiento
        y_train: Etiquetas de entrenamiento
        param_grid: Grilla de parámetros
        cv: Número de folds para cross-validation
        scoring: Métrica de scoring
        verbose: Nivel de verbosidad

    Returns:
        Mejor modelo encontrado
    """
    # Crear modelo base
    if model_type == 'nb':
        base_model = create_naive_bayes()
    elif model_type == 'lr':
        base_model = create_logistic_regression()
    elif model_type == 'svm':
        base_model = create_linear_svm()
    elif model_type == 'rf':
        base_model = create_random_forest()
    else:
        raise ValueError(f"Tipo de modelo no soportado: {model_type}")

    # Grid Search
    grid_search = GridSearchCV(
        base_model,
        param_grid,
        cv=cv,
        scoring=scoring,
        n_jobs=-1,
        verbose=verbose
    )

    print(f"Optimizando hiperparámetros para {model_type}...")
    grid_search.fit(X_train, y_train)

    print(f"Mejores parámetros: {grid_search.best_params_}")
    print(f"Mejor score ({scoring}): {grid_search.best_score_:.4f}")

    return grid_search.best_estimator_


def save_model(model, filepath: str):
    """
    Guarda un modelo en disco.

    Args:
        model: Modelo a guardar
        filepath: Ruta del archivo
    """
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)
    print(f"Modelo guardado en: {filepath}")


def load_model(filepath: str):
    """
    Carga un modelo desde disco.

    Args:
        filepath: Ruta del archivo

    Returns:
        Modelo cargado
    """
    with open(filepath, 'rb') as f:
        model = pickle.load(f)
    print(f"Modelo cargado desde: {filepath}")
    return model


if __name__ == "__main__":
    # Ejemplo de uso
    print("Módulo de modelos de clasificación")
    print("Modelos disponibles:")
    for name in get_default_models().keys():
        print(f"  - {name}")
