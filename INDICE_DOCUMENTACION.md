# Índice de Documentación - Clasificador de Noticias NLP

## 📚 Guía de Lectura de la Documentación

Este proyecto cuenta con documentación completa y bien organizada. A continuación se presenta el orden recomendado de lectura según tu objetivo.

---

## 🚀 Para Empezar Rápidamente

### 1. [QUICKSTART.md](QUICKSTART.md) ⭐ EMPIEZA AQUÍ
**Duración: 5 minutos**

Guía de inicio rápido que te permite:
- Instalar dependencias
- Ejecutar el proyecto en 3 pasos
- Ver resultados inmediatos

**Lee esto primero si quieres:**
- Ejecutar el proyecto rápidamente
- Ver el clasificador en acción
- No tienes mucho tiempo

---

## 📖 Para Entender el Proyecto Completo

### 2. [README.md](README.md) ⭐ DOCUMENTACIÓN PRINCIPAL
**Duración: 15 minutos**

Documentación principal del proyecto que incluye:
- Descripción general del proyecto
- Características y funcionalidades
- Instrucciones de instalación detalladas
- Guía de uso completa
- Explicación de resultados
- Arquitectura del proyecto
- Contribuciones y licencia

**Lee esto si quieres:**
- Entender el proyecto completo
- Ver todas las funcionalidades
- Conocer la arquitectura
- Aprender a usar todas las características

---

## 🏗️ Para Entender la Estructura

### 3. [ESTRUCTURA_PROYECTO.md](ESTRUCTURA_PROYECTO.md) ⭐ PARA DESARROLLADORES
**Duración: 10 minutos**

Documentación detallada de la estructura del proyecto:
- Árbol completo de directorios
- Descripción de cada archivo
- Flujos de trabajo recomendados
- Tamaños de archivos
- Control de versiones

**Lee esto si quieres:**
- Navegar el código fácilmente
- Entender dónde está cada cosa
- Contribuir al proyecto
- Modificar o extender el código

---

## ✅ Para Verificar Requisitos NLP

### 4. [CUMPLIMIENTO_REQUISITOS_NLP.md](CUMPLIMIENTO_REQUISITOS_NLP.md) ⭐ VERIFICACIÓN
**Duración: 10 minutos**

Documento de verificación completa que demuestra:
- Cumplimiento de los 4 requisitos principales
- Técnicas de NLP utilizadas
- Resultados y métricas finales
- Ejemplos de predicciones en vivo
- Referencias técnicas

**Lee esto si quieres:**
- Verificar que cumple con requisitos académicos
- Ver evidencia de técnicas NLP
- Revisar métricas y resultados
- Entender las predicciones del modelo

---

## 📋 Para Información del Test Set

### 5. [TEST_SET_INFO.md](TEST_SET_INFO.md) ⭐ TEST SET
**Duración: 5 minutos**

Documentación completa sobre los archivos del test set:
- Script/notebook empleado para generación
- Descripción de test_public.csv (sin etiquetas)
- Descripción de test_labels.csv (con etiquetas para instructor)
- Formato y estructura de los archivos
- Verificación de integridad
- Ejemplos de uso

**Lee esto si quieres:**
- Entender cómo se generó el test set
- Saber qué contiene cada archivo CSV
- Verificar la estructura de los datos
- Usar los archivos para evaluación

---

## 📊 Notebooks Jupyter (Exploración Paso a Paso)

### 6. Notebooks Interactivos
**Duración: 30-60 minutos**

Para aprender el proceso completo de manera interactiva:

#### [notebooks/01_EDA.ipynb](notebooks/01_EDA.ipynb)
- Análisis exploratorio de datos
- Estadísticas descriptivas
- Visualizaciones de distribuciones

#### [notebooks/02_preprocessing.ipynb](notebooks/02_preprocessing.ipynb)
- Preprocesamiento de texto
- Limpieza de datos
- Mapeo de categorías

#### [notebooks/03_data_splitting.ipynb](notebooks/03_data_splitting.ipynb)
- División estratificada de datos
- Generación de test sets
- Verificación de balanceo

#### [notebooks/04_model_training_evaluation.ipynb](notebooks/04_model_training_evaluation.ipynb)
- Vectorización TF-IDF
- Entrenamiento de modelos
- Evaluación y comparación
- Visualizaciones de resultados

**Lee estos si quieres:**
- Ver el análisis paso a paso
- Entender cada etapa del proceso
- Reproducir los experimentos
- Aprender técnicas de NLP

---

## 📋 Archivos de Configuración

### 7. Archivos Técnicos

#### [config.py](config.py)
Configuración centralizada del proyecto:
- Rutas de datos y modelos
- Parámetros de TF-IDF
- Configuración de modelos ML
- Mapeo de categorías

#### [requirements.txt](requirements.txt)
Dependencias del proyecto:
- pandas, numpy
- scikit-learn
- matplotlib, seaborn
- jupyter

#### [.gitignore](.gitignore)
Control de versiones:
- Archivos ignorados
- Datos grandes no versionados

---

## 🎯 Flujos de Lectura Recomendados

### Para Usuarios (Solo quiero usar el clasificador)
```
1. QUICKSTART.md (5 min)
2. Ejecutar: python predict.py --text "Your news" --proba
```

### Para Estudiantes (Entender el proyecto completo)
```
1. QUICKSTART.md (5 min)
2. README.md (15 min)
3. CUMPLIMIENTO_REQUISITOS_NLP.md (10 min)
4. notebooks/ (30-60 min) - para entender paso a paso
```

### Para Desarrolladores (Modificar o extender el código)
```
1. README.md (15 min)
2. ESTRUCTURA_PROYECTO.md (10 min)
3. config.py + src/ (revisar código fuente)
4. Notebooks (opcional, para entender el proceso)
```

### Para Evaluadores/Instructores (Verificar requisitos)
```
1. CUMPLIMIENTO_REQUISITOS_NLP.md (10 min) ⭐ PRIORIDAD
2. TEST_SET_INFO.md (5 min) ⭐ TEST SET
3. README.md (15 min)
4. test_sets/test_public.csv y test_labels.csv (archivos del test)
5. notebooks/03_data_splitting.ipynb (script de generación)
6. results/final_test_metrics.json (ver métricas)
7. results/classification_report_test.txt (reporte detallado)
8. Ejecutar: python predict.py --text "..." --proba (demo en vivo)
```

---

## 📂 Resultados y Visualizaciones

### Métricas Finales
- [results/final_test_metrics.json](results/final_test_metrics.json) - Métricas JSON
- [results/classification_report_test.txt](results/classification_report_test.txt) - Reporte detallado
- [results/model_comparison_training.csv](results/model_comparison_training.csv) - Comparación de modelos

### Visualizaciones
- [results/confusion_matrix_final_test.png](results/confusion_matrix_final_test.png) - Matriz de confusión
- [results/roc_curve_final_test.png](results/roc_curve_final_test.png) - Curva ROC
- [results/class_distribution.png](results/class_distribution.png) - Distribución de clases
- [results/category_distribution.png](results/category_distribution.png) - Distribución de categorías

---

## 🔍 Búsqueda Rápida

### ¿Cómo instalar el proyecto?
→ [README.md#Instalación](README.md) o [QUICKSTART.md](QUICKSTART.md)

### ¿Cómo entrenar un modelo?
→ [README.md#Uso](README.md) o ejecutar `python train.py`

### ¿Cómo hacer predicciones?
→ [README.md#Predicciones](README.md) o ejecutar `python predict.py --help`

### ¿Qué técnicas de NLP se usaron?
→ [CUMPLIMIENTO_REQUISITOS_NLP.md#Técnicas](CUMPLIMIENTO_REQUISITOS_NLP.md)

### ¿Cuáles son las métricas finales?
→ [CUMPLIMIENTO_REQUISITOS_NLP.md#Métricas](CUMPLIMIENTO_REQUISITOS_NLP.md) o `results/final_test_metrics.json`

### ¿Dónde está el código de preprocesamiento?
→ [src/preprocessing.py](src/preprocessing.py)

### ¿Dónde está la configuración de TF-IDF?
→ [config.py](config.py) líneas 126-135

### ¿Cómo se mapean las categorías?
→ [config.py](config.py) líneas 76-113

### ¿Dónde están los modelos entrenados?
→ [models/best_model.pkl](models/best_model.pkl) y [models/vectorizer.pkl](models/vectorizer.pkl)

### ¿Dónde están los datasets?
→ `data/raw/` (originales) y `data/splits/` (train/val/test)

---

## 📝 Resumen de Cada Documento

| Documento | Propósito | Audiencia | Tiempo |
|-----------|-----------|-----------|--------|
| **QUICKSTART.md** | Inicio rápido en 3 pasos | Todos | 5 min |
| **README.md** | Documentación completa del proyecto | Todos | 15 min |
| **ESTRUCTURA_PROYECTO.md** | Estructura y organización de archivos | Desarrolladores | 10 min |
| **CUMPLIMIENTO_REQUISITOS_NLP.md** | Verificación de requisitos NLP | Evaluadores/Estudiantes | 10 min |
| **TEST_SET_INFO.md** | Información del test set y archivos CSV | Evaluadores/Instructores | 5 min |
| **INDICE_DOCUMENTACION.md** | Este archivo (guía de navegación) | Todos | 5 min |
| **Notebooks (4 archivos)** | Análisis paso a paso interactivo | Estudiantes/Investigadores | 60 min |
| **config.py** | Configuración centralizada | Desarrolladores | 5 min |
| **src/*.py (4 módulos)** | Código fuente modular | Desarrolladores | 30 min |

---

## 🎓 Para Presentaciones Académicas

Si necesitas presentar el proyecto, usa este orden:

### Presentación Corta (5-10 minutos)
1. Problema: Clasificar noticias de Actualidad vs Interés General
2. Datos: 207,339 noticias (MIND + GOOGLE)
3. Técnicas NLP: TF-IDF, N-gramas, Logistic Regression
4. Resultados: F1=88.62%, ROC-AUC=93.79%
5. Demo en vivo: `python predict.py --text "..." --proba`

### Presentación Detallada (20-30 minutos)
1. **Introducción** (5 min)
   - Problema y objetivos
   - Datasets utilizados

2. **Metodología** (10 min)
   - Preprocesamiento de texto
   - Vectorización TF-IDF
   - Modelos ML (4 modelos)
   - División estratificada (70/20/10)

3. **Resultados** (10 min)
   - Métricas finales (mostrar JSON)
   - Visualizaciones (matriz confusión, ROC)
   - Análisis de errores
   - Demo en vivo

4. **Conclusiones** (5 min)
   - Mejor modelo: Logistic Regression
   - Cumplimiento de requisitos NLP
   - Código reproducible y modular

---

## 📞 Contacto y Soporte

- Reportar problemas: Abrir issue en el repositorio
- Preguntas: Ver README.md o QUICKSTART.md
- Documentación técnica: Ver config.py y src/

---

**Última actualización:** 14 de Noviembre, 2025

**Nota:** Todos los archivos Markdown (.md) pueden leerse directamente en GitHub con formato, o en cualquier editor de texto.
