# Información del Test Set - Clasificador de Noticias

## 📋 Archivos del Test Set Generados

Este proyecto incluye los archivos requeridos del test set para evaluación:

---

## 1️⃣ Script/Notebook de Generación

### Notebook Empleado para Generar el Test Set

**Archivo:** [`notebooks/03_data_splitting.ipynb`](notebooks/03_data_splitting.ipynb)

**Descripción:**
- Notebook Jupyter que realiza la división estratificada del dataset
- Genera los conjuntos train (70%), validation (20%) y test (10%)
- Crea los archivos `test_public.csv` y `test_labels.csv`

**Proceso de Generación:**

1. **Carga del dataset preprocesado** (207,339 noticias)
2. **División estratificada** usando `train_test_split` con `stratify=y`
3. **Generación de archivos del test set:**
   - `test_public.csv`: Contiene solo `doc_id` y `text` (sin etiquetas)
   - `test_labels.csv`: Contiene `doc_id`, `label` y `class_name` (con etiquetas)

**Código relevante del notebook (Celda 7):**

```python
# ============================================================
# 5. GENERAR TEST SET PÚBLICO Y ETIQUETAS
# ============================================================

# test_public.csv - Sin etiquetas (para evaluación)
test_public = test_df[['doc_id', 'text']].copy()

# test_labels.csv - Con etiquetas (para el instructor)
test_labels = test_df[['doc_id', 'label', 'class_name']].copy()

# Guardar archivos
test_public.to_csv('../test_sets/test_public.csv', index=False)
test_labels.to_csv('../test_sets/test_labels.csv', index=False)
```

**Ubicación en el notebook:**
- Líneas 821-887 del archivo `notebooks/03_data_splitting.ipynb`

---

## 2️⃣ Archivo Test Público (sin etiquetas)

### `test_sets/test_public.csv`

**Descripción:**
- Conjunto de test público SIN etiquetas
- Diseñado para que los estudiantes hagan predicciones

**Características:**
- **Tamaño:** 1.7 MB
- **Registros:** 20,734 noticias (10% del dataset total)
- **Columnas:** 2
  - `doc_id`: Identificador único de la noticia
  - `text`: Texto de la noticia

**Formato:**
```csv
doc_id,text
N5275,Bobby Orr defended Don Cherry
GOOGLE81018,What Omicron's BA.4 and BA.5 variants mean for the pandemic
GOOGLE96384,"Bechtolsheimer Purchases Lola Cars Brand, Technical Assets – Sportscar365"
N52726,Giants' Pat Shurmur again defends his late fourth quarter punt
...
```

**Estructura:**
| Columna | Tipo | Descripción |
|---------|------|-------------|
| `doc_id` | string | ID único (N##### para MIND, GOOGLE##### para Google News) |
| `text` | string | Texto completo de la noticia |

**Estadísticas:**
- Total de noticias: 20,734
- Longitud promedio: ~100-150 caracteres
- Sin valores nulos

---

## 3️⃣ Archivo Test con Etiquetas (para instructor)

### `test_sets/test_labels.csv`

**Descripción:**
- Conjunto de test CON etiquetas
- Diseñado para que el instructor valide las predicciones

**Características:**
- **Tamaño:** 554 KB
- **Registros:** 20,734 noticias (mismo dataset que test_public.csv)
- **Columnas:** 3
  - `doc_id`: Identificador único de la noticia
  - `label`: Etiqueta numérica (0 o 1)
  - `class_name`: Nombre de la clase

**Formato:**
```csv
doc_id,label,class_name
N5275,1,Interés General
GOOGLE81018,0,Actualidad
GOOGLE96384,1,Interés General
N52726,1,Interés General
...
```

**Estructura:**
| Columna | Tipo | Descripción |
|---------|------|-------------|
| `doc_id` | string | ID único (coincide con test_public.csv) |
| `label` | int | 0 = Actualidad, 1 = Interés General |
| `class_name` | string | "Actualidad" o "Interés General" |

**Distribución de Clases:**
```
Clase 0 (Actualidad):        8,154 noticias (39.33%)
Clase 1 (Interés General): 12,580 noticias (60.67%)
```

---

## 📊 Verificación de Integridad

### Validación de los Archivos

```python
import pandas as pd

# Cargar archivos
test_public = pd.read_csv('test_sets/test_public.csv')
test_labels = pd.read_csv('test_sets/test_labels.csv')

# Verificar que los doc_id coincidan
assert len(test_public) == len(test_labels)
assert (test_public['doc_id'] == test_labels['doc_id']).all()

print("✓ Los archivos son consistentes")
print(f"  - test_public.csv: {len(test_public):,} registros")
print(f"  - test_labels.csv: {len(test_labels):,} registros")
```

**Resultado de la verificación:**
```
✓ Los archivos son consistentes
  - test_public.csv: 20,734 registros
  - test_labels.csv: 20,734 registros
```

---

## 🎯 Uso de los Archivos

### Para Estudiantes (usando test_public.csv)

```bash
# Hacer predicciones sobre el test público
python predict.py --file test_sets/test_public.csv --output my_predictions.csv
```

### Para Instructores (usando test_labels.csv)

```python
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score

# Cargar etiquetas reales
true_labels = pd.read_csv('test_sets/test_labels.csv')

# Cargar predicciones del estudiante
student_preds = pd.read_csv('my_predictions.csv')

# Comparar
accuracy = accuracy_score(true_labels['label'], student_preds['prediction'])
print(f"Accuracy del estudiante: {accuracy:.2%}")
```

### Evaluación Completa (script incluido)

El proyecto incluye el script [`evaluate.py`](evaluate.py) que ya realiza la evaluación completa:

```bash
python evaluate.py
```

**Este script:**
1. Carga el test set completo (con etiquetas)
2. Usa el modelo entrenado para hacer predicciones
3. Compara con las etiquetas reales
4. Genera métricas completas (Accuracy, Precision, Recall, F1, ROC-AUC)
5. Crea visualizaciones (matriz de confusión, curva ROC)
6. Analiza errores

---

## 📁 Ubicación de los Archivos

```
Proyecto/
│
├── notebooks/
│   └── 03_data_splitting.ipynb    ← Script de generación del test set
│
├── test_sets/
│   ├── test_public.csv             ← Test sin etiquetas (1.7 MB)
│   └── test_labels.csv             ← Test con etiquetas (554 KB)
│
├── evaluate.py                     ← Script de evaluación
│
└── results/
    ├── final_test_metrics.json     ← Métricas de evaluación
    ├── test_predictions_final.csv  ← Predicciones del modelo
    └── test_errors.csv             ← Análisis de errores
```

---

## 🔍 Inspección de los Archivos

### Inspeccionar test_public.csv

```bash
# Ver primeras líneas
head -n 10 test_sets/test_public.csv

# Contar registros
wc -l test_sets/test_public.csv

# Ver tamaño
ls -lh test_sets/test_public.csv
```

### Inspeccionar test_labels.csv

```bash
# Ver primeras líneas
head -n 10 test_sets/test_labels.csv

# Contar por clase
cut -d',' -f2 test_sets/test_labels.csv | sort | uniq -c

# Ver distribución
cut -d',' -f3 test_sets/test_labels.csv | sort | uniq -c
```

---

## 📈 Resultados de Evaluación Obtenidos

Usando el test set generado, el modelo obtuvo:

```
MÉTRICAS FINALES EN TEST SET (20,734 noticias)
==============================================

Accuracy:   86.68%
Precision:  92.02%
Recall:     85.45%
F1-Score:   88.62%
ROC-AUC:    93.79%

Distribución de predicciones:
- Clase 0 (Actualidad):        8,154 casos reales
- Clase 1 (Interés General): 12,580 casos reales

Predicciones correctas:    17,972 (86.68%)
Predicciones incorrectas:   2,762 (13.32%)
```

**Archivos de resultados generados:**
- `results/final_test_metrics.json` - Métricas en formato JSON
- `results/classification_report_test.txt` - Reporte detallado
- `results/confusion_matrix_final_test.png` - Visualización
- `results/roc_curve_final_test.png` - Curva ROC

---

## ✅ Resumen para Entrega

### Archivos Requeridos Incluidos:

1. ✅ **Script de generación del test set:**
   - [`notebooks/03_data_splitting.ipynb`](notebooks/03_data_splitting.ipynb)
   - Líneas 821-887: Código de generación de test_public.csv y test_labels.csv

2. ✅ **Test público (sin etiquetas):**
   - [`test_sets/test_public.csv`](test_sets/test_public.csv)
   - 20,734 noticias
   - Columnas: `doc_id`, `text`

3. ✅ **Test con etiquetas (para instructor):**
   - [`test_sets/test_labels.csv`](test_sets/test_labels.csv)
   - 20,734 noticias
   - Columnas: `doc_id`, `label`, `class_name`

---

## 🔗 Referencias Adicionales

- **Documentación del proyecto:** [`README.md`](README.md)
- **Guía de inicio rápido:** [`QUICKSTART.md`](QUICKSTART.md)
- **Estructura del proyecto:** [`ESTRUCTURA_PROYECTO.md`](ESTRUCTURA_PROYECTO.md)
- **Verificación de requisitos:** [`CUMPLIMIENTO_REQUISITOS_NLP.md`](CUMPLIMIENTO_REQUISITOS_NLP.md)

---

## 📝 Notas Importantes

1. **División estratificada:** Los archivos mantienen la proporción de clases del dataset original (39.33% Actualidad, 60.67% Interés General)

2. **Reproducibilidad:** La división usa `random_state=42` para garantizar que siempre se generen los mismos archivos

3. **Consistencia:** Los `doc_id` en `test_public.csv` y `test_labels.csv` están en el mismo orden

4. **Sin overlap:** El test set es completamente independiente de train y validation (nunca visto durante el entrenamiento)

5. **Formato estándar:** Archivos CSV con codificación UTF-8, compatibles con pandas, Excel, etc.

---

**Fecha de generación:** 14 de Noviembre, 2025
**Generado por:** Notebook `03_data_splitting.ipynb`
**Dataset fuente:** MIND.tsv + GOOGLE.tsv (207,339 noticias después de limpieza)
**División:** 70% train / 20% val / 10% test (estratificada)
