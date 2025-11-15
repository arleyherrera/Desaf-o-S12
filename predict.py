"""
predict.py
Script para realizar predicciones en nuevas noticias.

Buenas prácticas aplicadas:
- Interfaz simple para predicciones
- Validación de entradas
- Soporte para predicciones individuales y en batch
- Explicación de predicciones

Uso:
    # Predicción individual
    python predict.py --text "Breaking news about the economy"

    # Predicción desde archivo CSV
    python predict.py --file news_data.csv --output predictions.csv

Autor: 
Fecha: Noviembre 2025
"""

import logging
import sys
import argparse
from pathlib import Path

import pandas as pd
import numpy as np

# Importar módulos propios
from config import *
from src.models import load_model
from src.preprocessing import clean_text


# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


# ============================================================================
# CLASE PREDICTOR
# ============================================================================

class NewsClassifier:
    """Clasificador de noticias que encapsula modelo y vectorizador."""

    def __init__(self, model_path=None, vectorizer_path=None):
        """
        Inicializa el clasificador.

        Args:
            model_path: Ruta al modelo (por defecto usa config)
            vectorizer_path: Ruta al vectorizador (por defecto usa config)
        """
        self.model_path = model_path or BEST_MODEL_PATH
        self.vectorizer_path = vectorizer_path or VECTORIZER_PATH
        self.model = None
        self.vectorizer = None
        self.class_names = CLASS_NAMES

    def load(self):
        """Carga el modelo y vectorizador."""
        logger.info("Cargando modelo y vectorizador...")

        try:
            self.model = load_model(self.model_path)
            self.vectorizer = load_model(self.vectorizer_path)
            logger.info(f"  OK Modelo: {type(self.model).__name__}")
            logger.info(f"  OK Vocabulario: {len(self.vectorizer.vocabulary_):,} terminos")
            return True

        except FileNotFoundError as e:
            logger.error(f"ERROR Error: {e}")
            logger.error("Ejecuta train.py primero para entrenar el modelo")
            return False

    def predict_single(self, text, return_proba=False):
        """
        Predice la clase de un texto individual.

        Args:
            text: Texto a clasificar
            return_proba: Si True, retorna también probabilidades

        Returns:
            Dict con predicción y detalles
        """
        if self.model is None or self.vectorizer is None:
            raise RuntimeError("Modelo no cargado. Ejecuta load() primero")

        # Limpiar texto
        text_clean = clean_text(text)

        # Vectorizar
        X = self.vectorizer.transform([text_clean])

        # Predecir
        prediction = self.model.predict(X)[0]
        class_name = self.class_names[prediction]

        result = {
            'text': text[:100] + '...' if len(text) > 100 else text,
            'prediction': int(prediction),
            'class': class_name
        }

        # Agregar probabilidades si están disponibles
        if return_proba:
            if hasattr(self.model, 'predict_proba'):
                probas = self.model.predict_proba(X)[0]
                result['probabilities'] = {
                    self.class_names[i]: float(prob)
                    for i, prob in enumerate(probas)
                }
                result['confidence'] = float(max(probas))
            elif hasattr(self.model, 'decision_function'):
                score = self.model.decision_function(X)[0]
                result['score'] = float(score)

        return result

    def predict_batch(self, texts, return_proba=False):
        """
        Predice la clase de múltiples textos.

        Args:
            texts: Lista de textos a clasificar
            return_proba: Si True, retorna también probabilidades

        Returns:
            Lista de dicts con predicciones
        """
        if self.model is None or self.vectorizer is None:
            raise RuntimeError("Modelo no cargado. Ejecuta load() primero")

        logger.info(f"Prediciendo {len(texts)} textos...")

        # Limpiar textos
        texts_clean = [clean_text(text) for text in texts]

        # Vectorizar
        X = self.vectorizer.transform(texts_clean)

        # Predecir
        predictions = self.model.predict(X)

        results = []
        for i, (text, pred) in enumerate(zip(texts, predictions)):
            result = {
                'id': i,
                'text': text[:100] + '...' if len(text) > 100 else text,
                'prediction': int(pred),
                'class': self.class_names[pred]
            }

            # Agregar probabilidades
            if return_proba:
                if hasattr(self.model, 'predict_proba'):
                    probas = self.model.predict_proba(X[i])[0]
                    result['probabilities'] = {
                        self.class_names[j]: float(prob)
                        for j, prob in enumerate(probas)
                    }
                    result['confidence'] = float(max(probas))

            results.append(result)

        return results

    def predict_from_csv(self, input_path, output_path=None, text_column='text'):
        """
        Predice desde un archivo CSV.

        Args:
            input_path: Ruta al CSV de entrada
            output_path: Ruta al CSV de salida (opcional)
            text_column: Nombre de la columna con texto

        Returns:
            DataFrame con predicciones
        """
        logger.info(f"Leyendo CSV: {input_path}")

        # Leer CSV
        df = pd.read_csv(input_path)

        if text_column not in df.columns:
            raise ValueError(f"Columna '{text_column}' no encontrada en el CSV")

        # Predecir
        results = self.predict_batch(df[text_column].tolist(), return_proba=True)

        # Crear DataFrame de resultados
        results_df = pd.DataFrame(results)

        # Guardar si se especifica ruta de salida
        if output_path:
            results_df.to_csv(output_path, index=False)
            logger.info(f"OK Predicciones guardadas: {output_path}")

        return results_df


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def parse_arguments():
    """Parsea los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description='Clasificador de noticias: Actualidad vs Interés General'
    )

    # Argumentos mutuamente excluyentes
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--text', type=str, help='Texto individual a clasificar')
    group.add_argument('--file', type=str, help='Archivo CSV con textos')

    # Argumentos opcionales
    parser.add_argument('--output', type=str, help='Archivo de salida para predicciones (solo con --file)')
    parser.add_argument('--column', type=str, default='text', help='Nombre de la columna con texto en CSV')
    parser.add_argument('--proba', action='store_true', help='Mostrar probabilidades')

    return parser.parse_args()


def print_prediction(result):
    """
    Imprime el resultado de una predicción de manera formateada.

    Args:
        result: Dict con resultado de predicción
    """
    print("\n" + "=" * 70)
    print("RESULTADO DE LA PREDICCION")
    print("=" * 70)
    print(f"\nTexto: {result['text']}")
    print(f"\nClasificacion: {result['class']}")
    print(f"   (Clase {result['prediction']})")

    if 'probabilities' in result:
        print(f"\nProbabilidades:")
        for class_name, prob in result['probabilities'].items():
            bar_length = int(prob * 40)
            bar = '#' * bar_length + '-' * (40 - bar_length)
            print(f"   {class_name:20s}: {bar} {prob:.2%}")
        print(f"\n   Confianza: {result['confidence']:.2%}")
    elif 'score' in result:
        print(f"\nScore de decision: {result['score']:.4f}")

    print("=" * 70)


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal del script de predicción."""

    args = parse_arguments()

    print("\n" + "=" * 70)
    print("CLASIFICADOR DE NOTICIAS - PREDICCIÓN")
    print("Actualidad vs Interés General")
    print("=" * 70)

    try:
        # Crear e inicializar clasificador
        classifier = NewsClassifier()

        if not classifier.load():
            return 1

        # Predicción individual
        if args.text:
            result = classifier.predict_single(args.text, return_proba=args.proba)
            print_prediction(result)

        # Predicción desde archivo
        elif args.file:
            input_path = Path(args.file)

            if not input_path.exists():
                logger.error(f"ERROR Archivo no encontrado: {input_path}")
                return 1

            # Determinar ruta de salida
            if args.output:
                output_path = Path(args.output)
            else:
                output_path = input_path.parent / f"{input_path.stem}_predictions.csv"

            # Predecir
            results_df = classifier.predict_from_csv(
                input_path,
                output_path,
                text_column=args.column
            )

            # Mostrar resumen
            print(f"\nResumen:")
            print(f"  Total de textos: {len(results_df):,}")
            print(f"\n  Distribucion de predicciones:")
            for class_idx, class_name in enumerate(CLASS_NAMES):
                count = (results_df['prediction'] == class_idx).sum()
                pct = count / len(results_df) * 100
                print(f"    {class_name}: {count:,} ({pct:.2f}%)")

            print(f"\nOK Resultados guardados en: {output_path}")

        print("\nOK Prediccion completada exitosamente\n")
        return 0

    except Exception as e:
        logger.error(f"\nERROR Error durante la prediccion: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
