"""
Script para ejecutar todos los notebooks en orden.
"""
import subprocess
import sys
from pathlib import Path

notebooks = [
    "notebooks/01_EDA.ipynb",
    "notebooks/02_preprocessing.ipynb",
    "notebooks/03_data_splitting.ipynb",
    "notebooks/04_model_training_evaluation.ipynb"
]

print("="*70)
print("EJECUTANDO NOTEBOOKS EN ORDEN")
print("="*70)

for i, notebook in enumerate(notebooks, 1):
    print(f"\n[{i}/{len(notebooks)}] Ejecutando: {notebook}")
    print("-"*70)

    cmd = [
        "jupyter", "nbconvert",
        "--to", "notebook",
        "--execute",
        "--inplace",
        notebook
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"OK Completado: {notebook}")
    except subprocess.CalledProcessError as e:
        print(f"ERROR en {notebook}")
        print(f"Error: {e.stderr}")
        sys.exit(1)

print("\n" + "="*70)
print("TODOS LOS NOTEBOOKS EJECUTADOS EXITOSAMENTE")
print("="*70)
