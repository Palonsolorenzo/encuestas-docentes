"""
Módulo de procesamiento y consolidación de datos de encuestas docentes.
Soporta carga de múltiples archivos Excel, detección flexible de formatos (microdatos o agregados),
cálculo de métricas por asignatura y agregación a nivel de titulación.
"""

import os
import re
import numpy as np
import pandas as pd
from recommendations import SURVEY_ITEMS, get_item_info

def clean_subject_name(filename: str) -> str:
    """Limpia el nombre del archivo para obtener un nombre legible de la asignatura."""
    name = os.path.splitext(os.path.basename(filename))[0]
    # Eliminar prefijos comunes entre corchetes o paréntesis como (NUT2-2526-2) o [2025]
    name = re.sub(r'^[\[\(][^\]\)]+[\]\)]\s*[-_]?\s*', '', name)
    # Limpiar guiones bajos o múltiples espacios
    name = name.replace('_', ' ').strip()
    return name

def is_ns_value(val) -> bool:
    """Verifica si un valor corresponde a 'No sabe / No contesta'."""
    if pd.isna(val):
        return False
    val_str = str(val).strip().upper()
    return val_str in ['N/S', 'NS', 'NO SABE', 'NO SABE NO CONTESTA', 'NO SABE / NO CONTESTA', 'N/C', 'NC', '-', 'NA', 'N/A']

def parse_likert_cell(val):
    """
    Convierte una celda a valor numérico 1-5 o np.nan.
    Retorna tupla: (numeric_val, is_ns)
    """
    if pd.isna(val):
        return np.nan, False
    
    # Comprobar si es N/S
    if is_ns_value(val):
        return np.nan, True
    
    # Intentar conversión numérica
    try:
        num = float(val)
        if 1.0 <= num <= 5.0:
            return num, False
    except (ValueError, TypeError):
        pass
        
    # Si viene texto con número inicial (ej. '1 - Totalmente en desacuerdo')
    val_str = str(val).strip()
    match = re.match(r'^([1-5])(\.0)?(\s*[-:)]|\b)', val_str)
    if match:
        return float(match.group(1)), False
        
    return np.nan, False

def load_subject_excel(file_path_or_buffer, filename_hint: str = None) -> dict:
    """
    Carga y procesa un archivo Excel de encuesta de una asignatura.
    Extrae el nombre de la asignatura del nombre del archivo y la titulación de la pestaña.
    """
    filename = filename_hint or getattr(file_path_or_buffer, 'name', 'Asignatura.xlsx')
    subject_name = clean_subject_name(filename)
    
    # Leer el archivo Excel
    excel_file = pd.ExcelFile(file_path_or_buffer)
    sheet_names = excel_file.sheet_names
    
    if not sheet_names:
        raise ValueError(f"El archivo {filename} no contiene hojas.")
        
    # El nombre de la titulación se identifica con la pestaña (primera pestaña o pestaña activa)
    degree_name = sheet_names[0].strip()
    
    # Cargar el contenido de la hoja
    df_raw = excel_file.parse(sheet_names[0])
    
    # Procesar estructura
    items_data, total_responses = extract_survey_items(df_raw)
    
    # Métricas agregadas de la asignatura
    valid_means = [it['mean'] for it in items_data if not np.isnan(it['mean'])]
    subject_mean = float(np.mean(valid_means)) if valid_means else 0.0
    items_under_35 = [it for it in items_data if it['mean'] < 3.5 and not np.isnan(it['mean'])]
    
    return {
        "filename": filename,
        "subject_name": subject_name,
        "degree_name": degree_name,
        "sheet_name": sheet_names[0],
        "total_responses": total_responses,
        "global_mean": round(subject_mean, 2),
        "items_under_35_count": len(items_under_35),
        "items": items_data,
        "items_under_35": items_under_35
    }

def extract_survey_items(df: pd.DataFrame) -> tuple:
    """
    Detecta la disposición de los datos (columnas=ítems o filas=ítems) y calcula
    estadísticas para los 23 ítems.
    """
    # CASO A: Microdatos en columnas (cada fila un alumno, columnas representan ítems)
    # Buscamos columnas numéricas o columnas que contengan los 23 ítems
    cleaned_df = df.dropna(how='all')
    
    # Analizamos si el formato es filas=ítems (~23 filas)
    if 20 <= len(cleaned_df) <= 26 and any('media' in str(c).lower() or 'puntuac' in str(c).lower() for c in cleaned_df.columns):
        return _extract_from_aggregated_rows(cleaned_df)
    
    # Por defecto asumimos formato tabular: filas = respuestas, columnas = ítems
    return _extract_from_response_columns(cleaned_df)

def _extract_from_response_columns(df: pd.DataFrame) -> tuple:
    """
    Procesa un DataFrame donde cada fila es una encuesta respondida por un alumno
    y las columnas corresponden a los 23 ítems evaluados.
    """
    # Identificar qué columnas contienen respuestas
    survey_cols = []
    
    for col in df.columns:
        col_str = str(col).strip()
        # Ignorar columnas típicas de metadatos
        if col_str.lower() in ['id', 'timestamp', 'fecha', 'hora', 'marca temporal', 'estudiante', 'alumno', 'comentarios', 'observaciones']:
            continue
        survey_cols.append(col)
    
    # Si tenemos más o menos columnas, intentamos quedarnos con 23 columnas o hasta 23
    selected_cols = survey_cols[:23] if len(survey_cols) >= 23 else survey_cols
    total_responses = len(df)
    
    items_data = []
    
    for i in range(1, 24):
        item_info = get_item_info(i)
        
        if (i - 1) < len(selected_cols):
            col_name = selected_cols[i - 1]
            raw_series = df[col_name]
            
            # Si el nombre de la columna trae texto personalizado de la pregunta
            col_header_str = str(col_name).strip()
            custom_title = col_header_str if len(col_header_str) > 5 and not col_header_str.isdigit() else item_info["short_title"]
            
            numeric_vals = []
            ns_count = 0
            
            for v in raw_series:
                num, is_ns = parse_likert_cell(v)
                if is_ns:
                    ns_count += 1
                elif not np.isnan(num):
                    numeric_vals.append(num)
            
            valid_count = len(numeric_vals)
            if valid_count > 0:
                mean_val = float(np.mean(numeric_vals))
                median_val = float(np.median(numeric_vals))
                std_val = float(np.std(numeric_vals))
                
                # Desglose Likert
                pct_disagree = round((sum(1 for x in numeric_vals if x in [1.0, 2.0]) / valid_count) * 100, 1)
                pct_neutral = round((sum(1 for x in numeric_vals if x == 3.0) / valid_count) * 100, 1)
                pct_agree = round((sum(1 for x in numeric_vals if x in [4.0, 5.0]) / valid_count) * 100, 1)
            else:
                mean_val = np.nan
                median_val = np.nan
                std_val = np.nan
                pct_disagree = 0.0
                pct_neutral = 0.0
                pct_agree = 0.0
                
            total_evals = valid_count + ns_count
            ns_pct = round((ns_count / total_evals * 100), 1) if total_evals > 0 else 0.0
            
            # Clasificación de alerta
            alert_severity = _classify_alert(mean_val)
            
            items_data.append({
                "item_id": i,
                "code": item_info["code"],
                "dimension": item_info["dimension"],
                "short_title": custom_title,
                "full_text": item_info["text"],
                "mean": round(mean_val, 2) if not np.isnan(mean_val) else np.nan,
                "median": round(median_val, 2) if not np.isnan(median_val) else np.nan,
                "std": round(std_val, 2) if not np.isnan(std_val) else np.nan,
                "valid_count": valid_count,
                "ns_count": ns_count,
                "ns_pct": ns_pct,
                "pct_disagree": pct_disagree,
                "pct_neutral": pct_neutral,
                "pct_agree": pct_agree,
                "under_threshold": (mean_val < 3.5) if not np.isnan(mean_val) else False,
                "alert_severity": alert_severity,
                "diagnosis": item_info["diagnosis_under_35"],
                "action_short_term": item_info["action_short_term"],
                "action_medium_term": item_info["action_medium_term"],
                "kpi": item_info["kpi"],
                "responsible": item_info["responsible"]
            })
        else:
            # Rellenar con ítem vacío si faltan columnas
            items_data.append(_create_empty_item(i, item_info))
            
    return items_data, total_responses

def _extract_from_aggregated_rows(df: pd.DataFrame) -> tuple:
    """Procesa un DataFrame que ya viene resumido con una fila por ítem."""
    items_data = []
    # Localizar columna con la media
    mean_col = None
    for c in df.columns:
        if any(term in str(c).lower() for term in ['media', 'promedio', 'valoracion', 'puntuacion', 'valor']):
            mean_col = c
            break
            
    total_resp_est = 0
    row_idx = 0
    
    for i in range(1, 24):
        item_info = get_item_info(i)
        if row_idx < len(df) and mean_col is not None:
            row = df.iloc[row_idx]
            val = row[mean_col]
            num, _ = parse_likert_cell(val)
            mean_val = num if not np.isnan(num) else 3.5
            row_idx += 1
        else:
            mean_val = np.nan
            
        alert_severity = _classify_alert(mean_val)
        items_data.append({
            "item_id": i,
            "code": item_info["code"],
            "dimension": item_info["dimension"],
            "short_title": item_info["short_title"],
            "full_text": item_info["text"],
            "mean": round(mean_val, 2) if not np.isnan(mean_val) else np.nan,
            "median": round(mean_val, 2) if not np.isnan(mean_val) else np.nan,
            "std": 0.0,
            "valid_count": 0,
            "ns_count": 0,
            "ns_pct": 0.0,
            "pct_disagree": 0.0,
            "pct_neutral": 0.0,
            "pct_agree": 100.0 if mean_val >= 3.5 else 0.0,
            "under_threshold": (mean_val < 3.5) if not np.isnan(mean_val) else False,
            "alert_severity": alert_severity,
            "diagnosis": item_info["diagnosis_under_35"],
            "action_short_term": item_info["action_short_term"],
            "action_medium_term": item_info["action_medium_term"],
            "kpi": item_info["kpi"],
            "responsible": item_info["responsible"]
        })
        
    return items_data, total_resp_est

def _classify_alert(mean_val) -> str:
    """Clasifica la severidad según la puntuación media."""
    if np.isnan(mean_val):
        return "Sin datos"
    if mean_val < 3.0:
        return "Crítico (< 3.0)"
    elif mean_val < 3.5:
        return "En riesgo (3.0 - 3.49)"
    elif mean_val < 4.2:
        return "Aceptable (3.5 - 4.19)"
    else:
        return "Excelente (>= 4.2)"

def _create_empty_item(i: int, item_info: dict) -> dict:
    return {
        "item_id": i,
        "code": item_info["code"],
        "dimension": item_info["dimension"],
        "short_title": item_info["short_title"],
        "full_text": item_info["text"],
        "mean": np.nan,
        "median": np.nan,
        "std": np.nan,
        "valid_count": 0,
        "ns_count": 0,
        "ns_pct": 0.0,
        "pct_disagree": 0.0,
        "pct_neutral": 0.0,
        "pct_agree": 0.0,
        "under_threshold": False,
        "alert_severity": "Sin datos",
        "diagnosis": item_info["diagnosis_under_35"],
        "action_short_term": item_info["action_short_term"],
        "action_medium_term": item_info["action_medium_term"],
        "kpi": item_info["kpi"],
        "responsible": item_info["responsible"]
    }

def consolidate_degree_data(subjects_list: list) -> dict:
    """
    Consolida los resultados de múltiples asignaturas a nivel de Titulación.
    """
    if not subjects_list:
        return {}
        
    degree_name = subjects_list[0]["degree_name"]
    total_subjects = len(subjects_list)
    total_responses_all = sum(s["total_responses"] for s in subjects_list)
    
    # Calcular media global de la titulación
    subject_means = [s["global_mean"] for s in subjects_list if s["global_mean"] > 0]
    degree_global_mean = round(float(np.mean(subject_means)), 2) if subject_means else 0.0
    
    # Calcular medias por ítem a nivel de titulación
    degree_items = []
    for i in range(1, 24):
        item_info = get_item_info(i)
        item_means_across_subjects = []
        for s in subjects_list:
            item_obj = next((it for it in s["items"] if it["item_id"] == i), None)
            if item_obj and not np.isnan(item_obj["mean"]):
                item_means_across_subjects.append(item_obj["mean"])
                
        if item_means_across_subjects:
            deg_item_mean = round(float(np.mean(item_means_across_subjects)), 2)
        else:
            deg_item_mean = np.nan
            
        # Cuántas asignaturas tienen este ítem < 3.5
        subjects_failing = []
        for s in subjects_list:
            item_obj = next((it for it in s["items"] if it["item_id"] == i), None)
            if item_obj and not np.isnan(item_obj["mean"]) and item_obj["mean"] < 3.5:
                subjects_failing.append({
                    "subject_name": s["subject_name"],
                    "mean": item_obj["mean"]
                })
                
        degree_items.append({
            "item_id": i,
            "code": item_info["code"],
            "dimension": item_info["dimension"],
            "short_title": item_info["short_title"],
            "full_text": item_info["text"],
            "degree_mean": deg_item_mean,
            "alert_severity": _classify_alert(deg_item_mean),
            "under_threshold": (deg_item_mean < 3.5) if not np.isnan(deg_item_mean) else False,
            "failing_subjects_count": len(subjects_failing),
            "failing_subjects": subjects_failing,
            "diagnosis": item_info["diagnosis_under_35"],
            "action_short_term": item_info["action_short_term"],
            "action_medium_term": item_info["action_medium_term"],
            "kpi": item_info["kpi"],
            "responsible": item_info["responsible"]
        })
        
    # Ranking de asignaturas
    sorted_subjects = sorted(subjects_list, key=lambda x: x["global_mean"], reverse=True)
    
    # Ítems críticos a nivel de titulación (< 3.5)
    degree_critical_items = [it for it in degree_items if it["under_threshold"]]
    
    # Lista consolidada de todas las acciones de mejora necesarias (todas las asignaturas e ítems < 3.5)
    all_improvement_actions = []
    for s in subjects_list:
        for it in s["items_under_35"]:
            all_improvement_actions.append({
                "subject_name": s["subject_name"],
                "item_code": it["code"],
                "item_title": it["short_title"],
                "dimension": it["dimension"],
                "mean_score": it["mean"],
                "alert_severity": it["alert_severity"],
                "diagnosis": it["diagnosis"],
                "action_short_term": it["action_short_term"],
                "action_medium_term": it["action_medium_term"],
                "kpi": it["kpi"],
                "responsible": it["responsible"]
            })
            
    # Ordenar acciones por menor nota primero (mayor urgencia)
    all_improvement_actions.sort(key=lambda x: x["mean_score"])
    
    # Matriz comparativa (DataFrame: Asignaturas en filas, Ítems en columnas)
    matrix_rows = []
    for s in subjects_list:
        row = {"Asignatura": s["subject_name"], "Media Global": s["global_mean"]}
        for it in s["items"]:
            row[f"{it['code']}: {it['short_title']}"] = it["mean"]
        matrix_rows.append(row)
        
    df_matrix = pd.DataFrame(matrix_rows)
    
    # Análisis por dimensiones pedagógicas a nivel titulación
    dimension_scores = {}
    for it in degree_items:
        dim = it["dimension"]
        if not np.isnan(it["degree_mean"]):
            dimension_scores.setdefault(dim, []).append(it["degree_mean"])
            
    dimensions_summary = [
        {
            "dimension": dim,
            "mean": round(float(np.mean(scores)), 2),
            "items_count": len(scores)
        }
        for dim, scores in dimension_scores.items()
    ]
    dimensions_summary.sort(key=lambda x: x["mean"])

    return {
        "degree_name": degree_name,
        "total_subjects": total_subjects,
        "total_responses": total_responses_all,
        "degree_global_mean": degree_global_mean,
        "subjects_ranking": sorted_subjects,
        "degree_items": degree_items,
        "degree_critical_items": degree_critical_items,
        "all_improvement_actions": all_improvement_actions,
        "matrix_df": df_matrix,
        "dimensions_summary": dimensions_summary
    }
