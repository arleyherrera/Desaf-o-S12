"""
run_pipeline.py
Script maestro para ejecutar el pipeline completo de principio a fin.

Este script automatiza todo el proceso:
1. Carga y preprocesamiento de datos
2. División estratificada
3. Entrenamiento de modelos
4. Evaluación en conjunto de test
5. Generación de reportes

Buenas prácticas:
- Pipeline automatizado completo
- Logging detallado
- Manejo robusto de errores
- Checkpoints para recuperación
- Generación automática de reportes

Uso:
    python run_pipeline.py [--skip-preprocessing] [--skip-training]

Autor: 
Fecha: Noviembre 2025
"""

import logging
import sys
import time
import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Importar configuración y módulos
from config import *
from src.preprocessing import (
    clean_text,
    map_to_binary_class,
    remove_duplicates
)


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

def setup_logging():
    """Configura el sistema de logging para el pipeline."""
    log_file = ROOT_DIR / 'pipeline.log'

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logging()


# ============================================================================
# PASO 1: CARGA Y PREPROCESAMIENTO
# ============================================================================

def step_01_load_and_preprocess():
    """Carga y preprocesa los datasets originales."""

    logger.info("\n" + "=" * 70)
    logger.info("PASO 1: CARGA Y PREPROCESAMIENTO DE DATOS")
    logger.info("=" * 70)

    try:
        # Cargar datasets originales
        logger.info("\n1.1 Cargando datasets...")

        if not MIND_TSV.exists() or not GOOGLE_TSV.exists():
            raise FileNotFoundError(f"Datasets no encontrados en {RAW_DATA_DIR}")

        df_mind = pd.read_csv(MIND_TSV, sep='\t', header=None, names=DATASET_COLUMNS)
        df_mind['source'] = 'MIND'
        logger.info(f"  ✓ MIND: {len(df_mind):,} registros")

        df_google = pd.read_csv(GOOGLE_TSV, sep='\t', header=None, names=DATASET_COLUMNS)
        df_google['source'] = 'GOOGLE'
        logger.info(f"  ✓ GOOGLE: {len(df_google):,} registros")

        # Combinar datasets
        logger.info("\n1.2 Combinando datasets...")
        df_combined = pd.concat([df_mind, df_google], ignore_index=True)
        logger.info(f"  ✓ Total combinado: {len(df_combined):,} registros")

        # Guardar dataset combinado
        df_combined.to_csv(COMBINED_RAW_CSV, index=False)
        logger.info(f"  ✓ Guardado: {COMBINED_RAW_CSV}")

        # Mapeo de categorías
        logger.info("\n1.3 Mapeando categorías a clases binarias...")
        df_combined['label'] = df_combined['category'].apply(
            lambda x: map_to_binary_class(x, ACTUALIDAD_CATEGORIES, INTERES_GENERAL_CATEGORIES)
        )

        # Eliminar categorías no mapeadas
        unmapped = (df_combined['label'] == -1).sum()
        if unmapped > 0:
            logger.warning(f"  ⚠️ Eliminando {unmapped} registros con categorías no mapeadas")
            df_combined = df_combined[df_combined['label'] != -1]

        # Crear nombre de clase
        df_combined['class_name'] = df_combined['label'].map({i: name for i, name in enumerate(CLASS_NAMES)})

        # Distribución de clases
        logger.info(f"  Distribución de clases:")
        for label, name in enumerate(CLASS_NAMES):
            count = (df_combined['label'] == label).sum()
            pct = count / len(df_combined) * 100
            logger.info(f"    Clase {label} ({name}): {count:,} ({pct:.2f}%)")

        # Limpieza de texto
        logger.info("\n1.4 Limpiando texto...")
        df_combined['text'] = df_combined['title'].apply(clean_text)

        # Eliminar textos vacíos
        empty = (df_combined['text'] == '').sum()
        if empty > 0:
            logger.warning(f"  ⚠️ Eliminando {empty} textos vacíos")
            df_combined = df_combined[df_combined['text'] != '']

        # Eliminar duplicados
        logger.info("\n1.5 Eliminando duplicados...")
        before = len(df_combined)
        df_combined = df_combined.drop_duplicates(subset=['text'], keep='first')
        after = len(df_combined)
        logger.info(f"  ✓ Eliminados {before - after:,} duplicados")

        # Guardar dataset preprocesado
        df_processed = df_combined[['doc_id', 'text', 'label', 'class_name', 'source', 'category']].copy()
        df_processed.to_csv(PREPROCESSED_CSV, index=False)
        logger.info(f"\n✓ Dataset preprocesado guardado: {PREPROCESSED_CSV}")
        logger.info(f"  Total de registros: {len(df_processed):,}")

        return df_processed

    except Exception as e:
        logger.error(f"❌ Error en preprocesamiento: {e}", exc_info=True)
        raise


# ============================================================================
# PASO 2: DIVISIÓN ESTRATIFICADA
# ============================================================================

def step_02_split_data(df):
    """Divide el dataset en train, val y test de forma estratificada."""

    logger.info("\n" + "=" * 70)
    logger.info("PASO 2: DIVISIÓN ESTRATIFICADA DEL DATASET")
    logger.info("=" * 70)

    try:
        # Separar features y labels
        X = df[['doc_id', 'text', 'source', 'category']]
        y = df['label']

        logger.info(f"\nTotal de muestras: {len(X):,}")
        logger.info(f"Distribución objetivo:")
        logger.info(f"  - Training: {TRAIN_SIZE*100:.0f}%")
        logger.info(f"  - Validation: {VAL_SIZE*100:.0f}%")
        logger.info(f"  - Test: {TEST_SIZE*100:.0f}%")

        # Primer split: separar test (10%)
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y,
            test_size=TEST_SIZE,
            stratify=y,
            random_state=RANDOM_STATE
        )

        # Segundo split: dividir temp en train y val
        val_size_adjusted = VAL_SIZE / (TRAIN_SIZE + VAL_SIZE)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp,
            test_size=val_size_adjusted,
            stratify=y_temp,
            random_state=RANDOM_STATE
        )

        logger.info(f"\nSplits generados:")
        logger.info(f"  - Training: {len(X_train):,} ({len(X_train)/len(X)*100:.1f}%)")
        logger.info(f"  - Validation: {len(X_val):,} ({len(X_val)/len(X)*100:.1f}%)")
        logger.info(f"  - Test: {len(X_test):,} ({len(X_test)/len(X)*100:.1f}%)")

        # Crear DataFrames completos
        train_df = X_train.copy()
        train_df['label'] = y_train.values
        train_df['class_name'] = train_df['label'].map({i: name for i, name in enumerate(CLASS_NAMES)})

        val_df = X_val.copy()
        val_df['label'] = y_val.values
        val_df['class_name'] = val_df['label'].map({i: name for i, name in enumerate(CLASS_NAMES)})

        test_df = X_test.copy()
        test_df['label'] = y_test.values
        test_df['class_name'] = test_df['label'].map({i: name for i, name in enumerate(CLASS_NAMES)})

        # Guardar splits
        logger.info(f"\nGuardando splits...")
        train_df.to_csv(TRAIN_CSV, index=False)
        logger.info(f"  ✓ {TRAIN_CSV}")

        val_df.to_csv(VAL_CSV, index=False)
        logger.info(f"  ✓ {VAL_CSV}")

        test_df.to_csv(TEST_CSV, index=False)
        logger.info(f"  ✓ {TEST_CSV}")

        # Generar archivos de test para instructor
        test_public = test_df[['doc_id', 'text']].copy()
        test_public.to_csv(TEST_PUBLIC_CSV, index=False)
        logger.info(f"  ✓ {TEST_PUBLIC_CSV} (sin etiquetas)")

        test_labels = test_df[['doc_id', 'label', 'class_name']].copy()
        test_labels.to_csv(TEST_LABELS_CSV, index=False)
        logger.info(f"  ✓ {TEST_LABELS_CSV} (solo etiquetas)")

        logger.info(f"\n✓ División estratificada completada")

        return train_df, val_df, test_df

    except Exception as e:
        logger.error(f"❌ Error en división de datos: {e}", exc_info=True)
        raise


# ============================================================================
# PASO 3: ENTRENAMIENTO
# ============================================================================

def step_03_train_models():
    """Ejecuta el script de entrenamiento."""

    logger.info("\n" + "=" * 70)
    logger.info("PASO 3: ENTRENAMIENTO DE MODELOS")
    logger.info("=" * 70)

    try:
        # Importar y ejecutar train.py
        import train

        logger.info("\nEjecutando script de entrenamiento...")
        exit_code = train.main()

        if exit_code == 0:
            logger.info("✓ Entrenamiento completado exitosamente")
        else:
            raise RuntimeError("El entrenamiento falló")

    except Exception as e:
        logger.error(f"❌ Error en entrenamiento: {e}", exc_info=True)
        raise


# ============================================================================
# PASO 4: EVALUACIÓN
# ============================================================================

def step_04_evaluate():
    """Ejecuta el script de evaluación."""

    logger.info("\n" + "=" * 70)
    logger.info("PASO 4: EVALUACIÓN EN CONJUNTO DE TEST")
    logger.info("=" * 70)

    try:
        # Importar y ejecutar evaluate.py
        import evaluate

        logger.info("\nEjecutando script de evaluación...")
        exit_code = evaluate.main()

        if exit_code == 0:
            logger.info("✓ Evaluación completada exitosamente")
        else:
            raise RuntimeError("La evaluación falló")

    except Exception as e:
        logger.error(f"❌ Error en evaluación: {e}", exc_info=True)
        raise


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def parse_arguments():
    """Parsea argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description='Pipeline completo para clasificación de noticias'
    )
    parser.add_argument('--skip-preprocessing', action='store_true',
                       help='Saltar preprocesamiento (usar datos existentes)')
    parser.add_argument('--skip-training', action='store_true',
                       help='Saltar entrenamiento (usar modelo existente)')
    return parser.parse_args()


def main():
    """Función principal del pipeline."""

    args = parse_arguments()

    start_time = time.time()

    logger.info("\n" + "=" * 70)
    logger.info("PIPELINE COMPLETO - CLASIFICADOR DE NOTICIAS")
    logger.info("Actualidad vs Interés General")
    logger.info("=" * 70)
    logger.info(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Random State: {RANDOM_STATE}")

    try:
        # Paso 1: Preprocesamiento
        if not args.skip_preprocessing:
            df_processed = step_01_load_and_preprocess()
            train_df, val_df, test_df = step_02_split_data(df_processed)
        else:
            logger.info("\n⏭️  Saltando preprocesamiento (usando datos existentes)")

        # Paso 3: Entrenamiento
        if not args.skip_training:
            step_03_train_models()
        else:
            logger.info("\n⏭️  Saltando entrenamiento (usando modelo existente)")

        # Paso 4: Evaluación
        step_04_evaluate()

        # Resumen final
        elapsed_time = time.time() - start_time
        logger.info("\n" + "=" * 70)
        logger.info("PIPELINE COMPLETADO EXITOSAMENTE")
        logger.info("=" * 70)
        logger.info(f"\n⏱️  Tiempo total: {elapsed_time/60:.2f} minutos")

        logger.info(f"\n📁 Archivos generados:")
        logger.info(f"  Datos:")
        logger.info(f"    - {PREPROCESSED_CSV}")
        logger.info(f"    - {TRAIN_CSV}")
        logger.info(f"    - {VAL_CSV}")
        logger.info(f"    - {TEST_CSV}")
        logger.info(f"    - {TEST_PUBLIC_CSV}")
        logger.info(f"    - {TEST_LABELS_CSV}")
        logger.info(f"  Modelos:")
        logger.info(f"    - {BEST_MODEL_PATH}")
        logger.info(f"    - {VECTORIZER_PATH}")
        logger.info(f"  Resultados:")
        logger.info(f"    - {RESULTS_DIR}/training_metrics.json")
        logger.info(f"    - {RESULTS_DIR}/final_test_metrics.json")
        logger.info(f"    - {RESULTS_DIR}/model_comparison_training.csv")
        logger.info(f"    - {RESULTS_DIR}/test_predictions_final.csv")
        logger.info(f"    - {RESULTS_DIR}/*.png (visualizaciones)")

        logger.info("\n✅ Proyecto completado. Revisa los archivos en results/")

        return 0

    except KeyboardInterrupt:
        logger.warning("\n⚠️  Pipeline interrumpido por el usuario")
        return 130

    except Exception as e:
        logger.error(f"\n❌ Error crítico en el pipeline: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
