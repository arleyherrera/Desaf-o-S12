"""
feature_engineering.py
Módulo de ingeniería de características para el clasificador de noticias.

Autor: Equipo de Desarrollo
Fecha: Noviembre 2024
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from typing import Tuple, Optional


def create_tfidf_vectorizer(max_features: int = 10000,
                            ngram_range: Tuple[int, int] = (1, 2),
                            min_df: int = 2,
                            max_df: float = 0.95,
                            stop_words: str = 'english') -> TfidfVectorizer:
    """
    Crea un vectorizador TF-IDF con configuración optimizada.

    Args:
        max_features: Número máximo de features
        ngram_range: Rango de n-gramas (min, max)
        min_df: Frecuencia mínima de documentos
        max_df: Frecuencia máxima de documentos (proporción)
        stop_words: Idioma de stop words o None

    Returns:
        Vectorizador TF-IDF configurado
    """
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        min_df=min_df,
        max_df=max_df,
        strip_accents='unicode',
        lowercase=True,
        stop_words=stop_words
    )

    return vectorizer


def create_count_vectorizer(max_features: int = 10000,
                           ngram_range: Tuple[int, int] = (1, 1),
                           min_df: int = 2,
                           stop_words: str = 'english') -> CountVectorizer:
    """
    Crea un vectorizador de conteo (Bag of Words).

    Args:
        max_features: Número máximo de features
        ngram_range: Rango de n-gramas (min, max)
        min_df: Frecuencia mínima de documentos
        stop_words: Idioma de stop words o None

    Returns:
        Vectorizador Count configurado
    """
    vectorizer = CountVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        min_df=min_df,
        strip_accents='unicode',
        lowercase=True,
        stop_words=stop_words
    )

    return vectorizer


def vectorize_text(train_texts: pd.Series,
                  val_texts: Optional[pd.Series] = None,
                  test_texts: Optional[pd.Series] = None,
                  vectorizer_type: str = 'tfidf',
                  **vectorizer_params):
    """
    Vectoriza textos usando el vectorizador especificado.

    Args:
        train_texts: Textos de entrenamiento
        val_texts: Textos de validación (opcional)
        test_texts: Textos de test (opcional)
        vectorizer_type: 'tfidf' o 'count'
        **vectorizer_params: Parámetros para el vectorizador

    Returns:
        Tupla con (vectorizador, X_train, X_val, X_test)
        X_val y X_test son None si no se proporcionan
    """
    # Crear vectorizador
    if vectorizer_type == 'tfidf':
        vectorizer = create_tfidf_vectorizer(**vectorizer_params)
    elif vectorizer_type == 'count':
        vectorizer = create_count_vectorizer(**vectorizer_params)
    else:
        raise ValueError(f"Tipo de vectorizador no soportado: {vectorizer_type}")

    # Fit en train y transform
    print(f"Vectorizando con {vectorizer_type.upper()}...")
    X_train = vectorizer.fit_transform(train_texts)
    print(f"  X_train: {X_train.shape}")

    X_val = None
    X_test = None

    if val_texts is not None:
        X_val = vectorizer.transform(val_texts)
        print(f"  X_val: {X_val.shape}")

    if test_texts is not None:
        X_test = vectorizer.transform(test_texts)
        print(f"  X_test: {X_test.shape}")

    print(f"Vocabulario: {len(vectorizer.vocabulary_):,} términos")

    return vectorizer, X_train, X_val, X_test


def get_top_features(vectorizer, n: int = 20, class_index: Optional[int] = None):
    """
    Obtiene las top features por importancia.

    Args:
        vectorizer: Vectorizador entrenado
        n: Número de top features
        class_index: Índice de clase (para modelos con coef_)

    Returns:
        Lista de top features
    """
    feature_names = vectorizer.get_feature_names_out()

    if hasattr(vectorizer, 'idf_'):
        # Para TF-IDF, ordenar por IDF
        indices = np.argsort(vectorizer.idf_)[::-1][:n]
        return [(feature_names[i], vectorizer.idf_[i]) for i in indices]
    else:
        # Para Count, retornar primeras n features
        return feature_names[:n].tolist()


def add_text_features(df: pd.DataFrame, text_column: str = 'text') -> pd.DataFrame:
    """
    Añade features adicionales basadas en el texto.

    Args:
        df: DataFrame con columna de texto
        text_column: Nombre de la columna de texto

    Returns:
        DataFrame con features adicionales
    """
    df_enhanced = df.copy()

    # Longitud de caracteres
    df_enhanced['char_length'] = df_enhanced[text_column].apply(len)

    # Número de palabras
    df_enhanced['word_count'] = df_enhanced[text_column].apply(lambda x: len(str(x).split()))

    # Promedio de longitud de palabras
    df_enhanced['avg_word_length'] = df_enhanced[text_column].apply(
        lambda x: np.mean([len(word) for word in str(x).split()]) if len(str(x).split()) > 0 else 0
    )

    # Número de palabras únicas
    df_enhanced['unique_words'] = df_enhanced[text_column].apply(
        lambda x: len(set(str(x).lower().split()))
    )

    # Ratio de palabras únicas
    df_enhanced['unique_word_ratio'] = df_enhanced['unique_words'] / df_enhanced['word_count'].replace(0, 1)

    print(f"Features adicionales añadidas: char_length, word_count, avg_word_length, unique_words, unique_word_ratio")

    return df_enhanced


if __name__ == "__main__":
    # Ejemplo de uso
    print("Módulo de ingeniería de características")
    print("Importar este módulo en notebooks o scripts para usar sus funciones")
