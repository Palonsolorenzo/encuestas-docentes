# 🎓 Sistema de Explotación de Encuestas Docentes & Planes de Mejora

Aplicación interactiva desarrollada en **Streamlit** para la auditoría de calidad académica y explotación de los resultados de las encuestas docentes a nivel de **Titulación** y de **Asignatura**.

---

## 🚀 Cómo Iniciar la Aplicación

Simplemente haz doble clic en el archivo:
👉 **`ejecutar_aplicacion.bat`**

O desde la terminal en este directorio:
```cmd
"C:\Users\palonso\.venv_informes_notas\Scripts\streamlit.exe" run app.py
```

La aplicación se abrirá automáticamente en tu navegador web predeterminado (normalmente en `http://localhost:8501`).

---

## 📋 Estructura de los Archivos Excel de Entrada

Para cargar los datos de las asignaturas, la aplicación espera un archivo Excel (`.xlsx` o `.xls`) por cada asignatura:

1. **Nombre del archivo:** Identifica el **nombre de la asignatura** (ejemplos: `Dirección Estratégica.xlsx`, `Microeconomía Intermedia.xlsx`, `(ADE-2025) Contabilidad.xlsx`).
2. **Nombre de la pestaña (hoja):** Identifica el **nombre de la titulación** (ejemplos: `Grado en ADE`, `Grado en Nutrición Humana y Dietética`, etc.).
3. **Contenido de la hoja:**
   - Evaluaciones de los **23 ítems** de la encuesta docente.
   - Escala de valoración de **1 a 5**:
     - `1`: Peor valoración / Totalmente en desacuerdo.
     - `5`: Mejor valoración / Totalmente de acuerdo.
     - `N/S`: No sabe / No contesta (se contabiliza en porcentaje de respuesta neutra/desconocimiento, pero se excluye de la media aritmética para no sesgar el resultado).
   - Formatos compatibles:
     - **Microdatos (por defecto):** Cada fila es una encuesta cumplimentada por un alumno y las columnas corresponden a los ítems evaluados.
     - **Agregados:** Hoja resumida con las filas correspondientes a los 23 ítems.

> 💡 **Datos de prueba incluidos:** En la carpeta `datos_ejemplo/` dispones de 6 archivos Excel realistas con perfiles docentes variados para probar la aplicación de inmediato o pulsar el botón **"🧪 Cargar Demo"** en la barra lateral.

---

## 🔍 Funcionalidades de la Aplicación

### 1. 🏛️ Visión Global de la Titulación
- **Panel de KPIs:** Total de asignaturas, volumen de encuestas respondidas, media global de la titulación, asignaturas con alertas e ítems críticos.
- **Conclusiones Ejecutivas Automatizadas:** Diagnóstico narrativo que destaca las principales fortalezas de la carrera y los puntos débiles prioritarios.
- **Ranking de Asignaturas:** Gráfico de barras horizontal ordenado por media, con línea de corte en el umbral de calidad.
- **Rendimiento por Dimensiones Pedagógicas:** Evaluación de las 6 áreas clave (Planificación, Metodología, Campus Virtual, Evaluación, Tutorías y Satisfacción Global).
- **Mapa de Calor (Heatmap) Transversal:** Matriz interactiva de asignaturas vs los 23 ítems con semáforo visual.

### 2. 📘 Diagnóstico Individual por Asignatura
- Selector desplegable para auditar cualquier asignatura en detalle.
- Comparativa directa de la media de la asignatura frente a la media de la titulación (+/- puntos).
- Gráfico de barras de los 23 ítems con código de colores según nivel de alerta.
- **Desglose de respuestas Likert:** Gráfico acumulado (% en desacuerdo [1-2], % neutro [3], % de acuerdo [4-5], % N/S).
- Tabla interactiva con el registro completo de ítems, desviaciones típicas y porcentajes.

### 3. 🛠️ Plan de Acciones de Mejora (< 3,5 puntos)
- Detección automática de todos los ítems con nota media inferior a **3,5 puntos** (umbral ajustable en la barra lateral).
- **Fichas Técnicas de Mejora Pedagógica** con:
  - Diagnóstico pedagógico de la causa raíz.
  - **Acción Inmediata (Corto Plazo / Próximo Semestre):** Medidas docentes rápidas y aplicables.
  - **Acción Estructural (Medio Plazo):** Medidas de coordinación curricular y departamento.
  - **Indicador de Éxito (KPI):** Métrica verificable de consecución.
  - **Responsable Asignado:** Profesor/a, Coordinación de Grado, o Soporte Virtual.
- Filtro interactivo por asignatura y por dimensión pedagógica.

### 4. 📊 Matriz Comparativa y Exportación a Excel
- Vista completa tabular con formato condicional semafórico (rojo, ámbar, verde).
- **Exportación en Excel Profesional (`.xlsx`)** con 4 hojas:
  - *Resumen Titulación*: KPIs, ranking y dimensiones.
  - *Plan de Mejora (< 3.5)*: Fichero listo para comisiones de calidad y auditorías ANECA/DOCENTIA.
  - *Matriz de Ítems*: Tabla cruzada con formato de colores aplicado.
  - *Detalle por Asignatura*.

---

## 📂 Estructura de Archivos del Proyecto

```
Encuestas alumnos/
├── app.py                     # Aplicación web principal (Streamlit)
├── data_processor.py          # Lógica de carga, limpieza y consolidación de datos
├── recommendations.py         # Catálogo de los 23 ítems y propuestas de mejora
├── report_exporter.py         # Generador de informes ejecutivos en Excel
├── sample_generator.py        # Generador de datos sintéticos de demostración
├── ejecutar_aplicacion.bat    # Lanzador en un clic para Windows
├── requirements.txt           # Dependencias requeridas
├── datos_ejemplo/             # Archivos Excel de prueba para Grado en ADE
└── README.md                  # Documentación del sistema
```
