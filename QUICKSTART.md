# Guía de Inicio Rápido

## Para Usuarios Impacientes 🚀

### Opción 1: Ejecución Automática Completa (5-10 minutos)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar pipeline completo
python run_pipeline.py
```

¡Listo! El proyecto completo se ejecutará automáticamente y generará todos los resultados.

---

### Opción 2: Ejecución Manual por Pasos

Si ya ejecutaste los notebooks y tienes los datos preparados:

```bash
# 1. Entrenar modelos (requiere data/splits/*.csv)
python train.py

# 2. Evaluar en test set
python evaluate.py

# 3. Hacer predicciones
python predict.py --text "Your news text here" --proba
```

---

## Estructura de Archivos Generados

Después de ejecutar el pipeline, encontrarás:

```
📁 data/splits/
   ├── train.csv           ✅ Datos de entrenamiento
   ├── val.csv             ✅ Datos de validación
   └── test.csv            ✅ Datos de prueba

📁 models/
   ├── best_model.pkl      ✅ Mejor modelo entrenado
   └── vectorizer.pkl      ✅ Vectorizador TF-IDF

📁 results/
   ├── training_metrics.json              ✅ Métricas de entrenamiento
   ├── final_test_metrics.json            ✅ Métricas finales
   ├── test_predictions_final.csv         ✅ Predicciones
   ├── confusion_matrix_final_test.png    ✅ Matriz de confusión
   └── roc_curve_final_test.png           ✅ Curva ROC

📁 test_sets/
   ├── test_public.csv     ✅ Test sin etiquetas (para instructor)
   └── test_labels.csv     ✅ Test con etiquetas (para instructor)
```

---

## Ejemplos de Uso del Predictor

### Predicción Individual

```bash
python predict.py --text "The stock market crashed today" --proba
```

Salida esperada:
```
📰 Texto: The stock market crashed today
🏷️  Clasificación: Actualidad
   (Clase 0)
📊 Probabilidades:
   Actualidad          : ████████████████████████████████ 92.35%
   Interés General     : ████░░░░░░░░░░░░░░░░░░░░░░░░░░░ 7.65%
```

### Predicción desde CSV

```bash
# Crear archivo de ejemplo
echo "text" > news.csv
echo "Breaking: New economic policy announced" >> news.csv
echo "Top 10 vacation destinations for summer" >> news.csv

# Predecir
python predict.py --file news.csv --output predictions.csv --proba
```

---

## Solución de Problemas Comunes

### Error: "FileNotFoundError: data/raw/MIND.tsv"
**Solución**: Asegúrate de que los archivos MIND.tsv y GOOGLE.tsv estén en la carpeta `data/raw/`

### Error: "ModuleNotFoundError: No module named..."
**Solución**: Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "Modelo no cargado. Ejecuta train.py primero"
**Solución**: Entrena el modelo primero:
```bash
python train.py
```

### Los resultados son diferentes cada vez
**Solución**: Esto no debería pasar. El proyecto usa `RANDOM_STATE=42` para garantizar reproducibilidad. Verifica que no hayas modificado `config.py`.

---

## Verificar que Todo Funciona

Ejecuta este comando para verificar la configuración:

```bash
python -c "from config import get_config_summary; print(get_config_summary())"
```

---

## Siguiente Paso

Lee el [README.md](README.md) completo para entender a fondo el proyecto y sus componentes.

---

**Tiempo estimado total**: 10-15 minutos para ejecución completa del pipeline.
