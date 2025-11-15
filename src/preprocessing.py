"""
preprocessing.py
Módulo de preprocesamiento de texto para el clasificador de noticias.

Autor: Equipo de Desarrollo
Fecha: Noviembre 2024
"""

import re
import pandas as pd
from typing import Union, List


def clean_text(text: str) -> str:
    """
    Limpia y normaliza el texto.

    Args:
        text: Texto a limpiar

    Returns:
        Texto limpio y normalizado
    """
    if pd.isna(text):
        return ""

    # Convertir a string
    text = str(text)

    # Normalizar espacios múltiples
    text = re.sub(r'\s+', ' ', text)

    # Eliminar espacios al inicio y final
    text = text.strip()

    return text


def map_to_binary_class(category: str,
                        actualidad_categories: set,
                        interes_general_categories: set) -> int:
    """
    Mapea una categoría a clase binaria.

    Args:
        category: Categoría original
        actualidad_categories: Set de categorías de actualidad
        interes_general_categories: Set de categorías de interés general

    Returns:
        0 para Actualidad, 1 para Interés General, -1 si no se encuentra
    """
    if category in actualidad_categories:
        return 0
    elif category in interes_general_categories:
        return 1
    else:
        return -1


def remove_duplicates(df: pd.DataFrame,
                     column: str = 'title',
                     keep: str = 'first') -> pd.DataFrame:
    """
    Elimina duplicados del DataFrame basado en una columna.

    Args:
        df: DataFrame de pandas
        column: Columna para detectar duplicados
        keep: 'first', 'last', o False

    Returns:
        DataFrame sin duplicados
    """
    return df.drop_duplicates(subset=[column], keep=keep)


def validate_dataset(df: pd.DataFrame,
                    required_columns: List[str]) -> bool:
    """
    Valida que el DataFrame tenga las columnas requeridas.

    Args:
        df: DataFrame a validar
        required_columns: Lista de columnas requeridas

    Returns:
        True si todas las columnas están presentes, False de lo contrario
    """
    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        print(f"⚠️ Columnas faltantes: {missing_columns}")
        return False

    return True


def get_text_stats(text: str) -> dict:
    """
    Calcula estadísticas de un texto.

    Args:
        text: Texto a analizar

    Returns:
        Diccionario con estadísticas (longitud, número de palabras, etc.)
    """
    text = str(text)

    return {
        'length': len(text),
        'word_count': len(text.split()),
        'avg_word_length': sum(len(word) for word in text.split()) / max(len(text.split()), 1)
    }


def preprocess_dataset(df: pd.DataFrame,
                      text_column: str = 'title',
                      category_column: str = 'category',
                      actualidad_categories: set = None,
                      interes_general_categories: set = None) -> pd.DataFrame:
    """
    Pipeline completo de preprocesamiento del dataset.

    Args:
        df: DataFrame original
        text_column: Nombre de la columna de texto
        category_column: Nombre de la columna de categoría
        actualidad_categories: Set de categorías de actualidad
        interes_general_categories: Set de categorías de interés general

    Returns:
        DataFrame preprocesado
    """
    df_processed = df.copy()

    # Limpiar texto
    print("Limpiando texto...")
    df_processed['text_clean'] = df_processed[text_column].apply(clean_text)

    # Eliminar textos vacíos
    df_processed = df_processed[df_processed['text_clean'] != '']

    # Mapear categorías si se proporcionan
    if actualidad_categories and interes_general_categories:
        print("Mapeando categorías a clases binarias...")
        df_processed['label'] = df_processed[category_column].apply(
            lambda x: map_to_binary_class(x, actualidad_categories, interes_general_categories)
        )

        # Eliminar categorías no mapeadas
        df_processed = df_processed[df_processed['label'] != -1]

    # Eliminar duplicados
    print("Eliminando duplicados...")
    df_processed = remove_duplicates(df_processed, column='text_clean')

    print(f"Preprocesamiento completo. Registros finales: {len(df_processed):,}")

    return df_processed


if __name__ == "__main__":
    # Ejemplo de uso
    print("Módulo de preprocesamiento de texto")
    print("Importar este módulo en notebooks o scripts para usar sus funciones")
