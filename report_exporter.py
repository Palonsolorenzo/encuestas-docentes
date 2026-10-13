"""
Módulo para la exportación de informes ejecutivos en formato Excel (.xlsx).
Incluye resumen de titulación, plan de acciones de mejora (< 3.5),
matriz comparativa y detalle por asignatura con formato condicional.
"""

import io
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def generate_degree_excel_report(degree_data: dict, subjects_list: list) -> bytes:
    """
    Genera un archivo Excel profesional con múltiples pestañas y formato ejecutivo.
    Retorna los bytes del archivo para su descarga directa.
    """
    output = io.BytesIO()
    wb = openpyxl.Workbook()
    
    # Estilos estándar
    header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid") # Azul corporativo
    sub_header_fill = PatternFill(start_color="3B82F6", end_color="3B82F6", fill_type="solid")
    alert_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid") # Rojo suave < 3.5
    warning_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid") # Ámbar 3.5-3.99
    success_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid") # Verde >= 4.0
    
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_bold = Font(name="Calibri", size=11, bold=True)
    font_regular = Font(name="Calibri", size=10)
    font_title = Font(name="Calibri", size=14, bold=True, color="1E3A8A")
    font_kpi_value = Font(name="Calibri", size=16, bold=True, color="1E3A8A")
    
    thin_border = Border(
        left=Side(style='thin', color='D1D5DB'),
        right=Side(style='thin', color='D1D5DB'),
        top=Side(style='thin', color='D1D5DB'),
        bottom=Side(style='thin', color='D1D5DB')
    )
    
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    align_right = Alignment(horizontal="right", vertical="center")

    # ==========================================
    # HOJA 1: RESUMEN TITULACIÓN
    # ==========================================
    ws_resumen = wb.active
    ws_resumen.title = "Resumen Titulación"
    ws_resumen.views.sheetView[0].showGridLines = True
    
    ws_resumen["A1"] = f"INFORME EJECUTIVO DE ENCUESTAS DOCENTES: {degree_data['degree_name'].upper()}"
    ws_resumen["A1"].font = font_title
    
    # Tarjetas de KPIs
    kpis = [
        ("Titulación", degree_data["degree_name"]),
        ("Total Asignaturas", degree_data["total_subjects"]),
        ("Total Evaluaciones", degree_data["total_responses"]),
        ("Media Global Titulación", f"{degree_data['degree_global_mean']:.2f} / 5.00"),
        ("Ítems Críticos (< 3.5)", len(degree_data["all_improvement_actions"]))
    ]
    
    for col_idx, (label, val) in enumerate(kpis, start=1):
        cell_lbl = ws_resumen.cell(row=3, column=col_idx, value=label)
        cell_lbl.font = Font(name="Calibri", size=9, bold=True, color="6B7280")
        cell_lbl.alignment = align_center
        cell_lbl.fill = PatternFill(start_color="F3F4F6", end_color="F3F4F6", fill_type="solid")
        cell_lbl.border = thin_border
        
        cell_val = ws_resumen.cell(row=4, column=col_idx, value=val)
        cell_val.font = font_kpi_value
        cell_val.alignment = align_center
        cell_val.border = thin_border

    # Tabla: Ranking de Asignaturas
    ws_resumen.cell(row=7, column=1, value="RANKING DE ASIGNATURAS DE LA TITULACIÓN").font = font_bold
    headers_ranking = ["Posición", "Asignatura", "Total Respuestas", "Media Global", "Ítems < 3.5", "Estado Calidad"]
    
    for c_idx, h in enumerate(headers_ranking, start=1):
        cell = ws_resumen.cell(row=8, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border
        
    for r_idx, s in enumerate(degree_data["subjects_ranking"], start=1):
        curr_row = 8 + r_idx
        ws_resumen.cell(row=curr_row, column=1, value=r_idx).alignment = align_center
        ws_resumen.cell(row=curr_row, column=2, value=s["subject_name"]).alignment = align_left
        ws_resumen.cell(row=curr_row, column=3, value=s["total_responses"]).alignment = align_center
        
        c_mean = ws_resumen.cell(row=curr_row, column=4, value=s["global_mean"])
        c_mean.alignment = align_center
        c_mean.number_format = '0.00'
        
        c_items = ws_resumen.cell(row=curr_row, column=5, value=s["items_under_35_count"])
        c_items.alignment = align_center
        
        status_text = "Requiere Plan de Mejora" if s["items_under_35_count"] > 0 else "Satisfactorio"
        c_status = ws_resumen.cell(row=curr_row, column=6, value=status_text)
        c_status.alignment = align_center
        
        # Color según estado
        if s["items_under_35_count"] > 0:
            c_items.fill = alert_fill
            c_status.fill = alert_fill
        else:
            c_items.fill = success_fill
            c_status.fill = success_fill
            
        for c in range(1, 7):
            ws_resumen.cell(row=curr_row, column=c).border = thin_border
            ws_resumen.cell(row=curr_row, column=c).font = font_regular

    # Tabla: Resumen por Dimensiones Pedagógicas
    row_dim_start = 10 + len(degree_data["subjects_ranking"])
    ws_resumen.cell(row=row_dim_start, column=1, value="VALORACIÓN POR DIMENSIONES PEDAGÓGICAS").font = font_bold
    
    headers_dim = ["Dimensión Pedagógica", "Nº Ítems", "Media Titulación", "Estado"]
    for c_idx, h in enumerate(headers_dim, start=1):
        cell = ws_resumen.cell(row=row_dim_start + 1, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = sub_header_fill
        cell.alignment = align_center
        cell.border = thin_border
        
    for r_idx, dim_info in enumerate(degree_data["dimensions_summary"], start=1):
        curr_row = row_dim_start + 1 + r_idx
        ws_resumen.cell(row=curr_row, column=1, value=dim_info["dimension"]).alignment = align_left
        ws_resumen.cell(row=curr_row, column=2, value=dim_info["items_count"]).alignment = align_center
        
        c_m = ws_resumen.cell(row=curr_row, column=3, value=dim_info["mean"])
        c_m.alignment = align_center
        c_m.number_format = '0.00'
        
        dim_status = "Crítico (< 3.5)" if dim_info["mean"] < 3.5 else "Adecuado"
        c_st = ws_resumen.cell(row=curr_row, column=4, value=dim_status)
        c_st.alignment = align_center
        if dim_info["mean"] < 3.5:
            c_m.fill = alert_fill
            c_st.fill = alert_fill
        else:
            c_m.fill = success_fill
            c_st.fill = success_fill
            
        for c in range(1, 5):
            ws_resumen.cell(row=curr_row, column=c).border = thin_border
            ws_resumen.cell(row=curr_row, column=c).font = font_regular

    # ==========================================
    # HOJA 2: PLAN DE MEJORA (< 3.5)
    # ==========================================
    ws_mejora = wb.create_sheet(title="Plan de Mejora (< 3.5)")
    ws_mejora.views.sheetView[0].showGridLines = True
    
    ws_mejora["A1"] = f"PLAN DE ACCIONES DE MEJORA CORRECTIVAS (ÍTEMS CON MEDIA < 3.5 PUNTOS)"
    ws_mejora["A1"].font = font_title
    
    headers_mejora = [
        "Asignatura", "Cód. Ítem", "Nombre del Ítem", "Dimensión", "Puntuación Media",
        "Severidad", "Diagnóstico del Problema", "Acción Inmediata (Corto Plazo)",
        "Acción Estructural (Medio Plazo)", "Indicador de Seguimiento (KPI)", "Responsable Sugerido"
    ]
    
    for c_idx, h in enumerate(headers_mejora, start=1):
        cell = ws_mejora.cell(row=3, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border
        
    for r_idx, act in enumerate(degree_data["all_improvement_actions"], start=1):
        curr_row = 3 + r_idx
        ws_mejora.cell(row=curr_row, column=1, value=act["subject_name"]).alignment = align_left
        ws_mejora.cell(row=curr_row, column=2, value=act["item_code"]).alignment = align_center
        ws_mejora.cell(row=curr_row, column=3, value=act["item_title"]).alignment = align_left
        ws_mejora.cell(row=curr_row, column=4, value=act["dimension"]).alignment = align_left
        
        c_score = ws_mejora.cell(row=curr_row, column=5, value=act["mean_score"])
        c_score.alignment = align_center
        c_score.number_format = '0.00'
        c_score.fill = alert_fill
        c_score.font = font_bold
        
        ws_mejora.cell(row=curr_row, column=6, value=act["alert_severity"]).alignment = align_center
        ws_mejora.cell(row=curr_row, column=7, value=act["diagnosis"]).alignment = align_left
        ws_mejora.cell(row=curr_row, column=8, value=act["action_short_term"]).alignment = align_left
        ws_mejora.cell(row=curr_row, column=9, value=act["action_medium_term"]).alignment = align_left
        ws_mejora.cell(row=curr_row, column=10, value=act["kpi"]).alignment = align_left
        ws_mejora.cell(row=curr_row, column=11, value=act["responsible"]).alignment = align_left
        
        for c in range(1, len(headers_mejora) + 1):
            ws_mejora.cell(row=curr_row, column=c).border = thin_border
            if c != 5:
                ws_mejora.cell(row=curr_row, column=c).font = font_regular

    # ==========================================
    # HOJA 3: MATRIZ DE ÍTEMS (ASIGNATURAS VS ÍTEMS)
    # ==========================================
    ws_matriz = wb.create_sheet(title="Matriz de Ítems")
    ws_matriz.views.sheetView[0].showGridLines = True
    
    ws_matriz["A1"] = f"MATRIZ COMPARATIVA DE ÍTEMS POR ASIGNATURA ({degree_data['degree_name']})"
    ws_matriz["A1"].font = font_title
    
    matriz_headers = ["Asignatura", "Media Global"] + [f"IT{i:02d}" for i in range(1, 24)]
    for c_idx, h in enumerate(matriz_headers, start=1):
        cell = ws_matriz.cell(row=3, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border
        
    for r_idx, s in enumerate(subjects_list, start=1):
        curr_row = 3 + r_idx
        ws_matriz.cell(row=curr_row, column=1, value=s["subject_name"]).alignment = align_left
        
        c_gm = ws_matriz.cell(row=curr_row, column=2, value=s["global_mean"])
        c_gm.alignment = align_center
        c_gm.number_format = '0.00'
        c_gm.font = font_bold
        
        for i in range(1, 24):
            item_obj = next((it for it in s["items"] if it["item_id"] == i), None)
            val = item_obj["mean"] if item_obj else None
            cell = ws_matriz.cell(row=curr_row, column=2 + i, value=val)
            cell.alignment = align_center
            cell.border = thin_border
            cell.font = font_regular
            if val is not None and not pd.isna(val):
                cell.number_format = '0.00'
                if val < 3.5:
                    cell.fill = alert_fill
                elif val < 4.0:
                    cell.fill = warning_fill
                else:
                    cell.fill = success_fill
                    
        ws_matriz.cell(row=curr_row, column=1).border = thin_border
        ws_matriz.cell(row=curr_row, column=2).border = thin_border

    # Fila de Medias de Titulación en la matriz
    deg_row = 4 + len(subjects_list)
    ws_matriz.cell(row=deg_row, column=1, value="MEDIA TITULACIÓN").font = font_bold
    ws_matriz.cell(row=deg_row, column=1).alignment = align_left
    ws_matriz.cell(row=deg_row, column=1).border = thin_border
    ws_matriz.cell(row=deg_row, column=1).fill = sub_header_fill
    ws_matriz.cell(row=deg_row, column=1).font = font_header
    
    c_dgm = ws_matriz.cell(row=deg_row, column=2, value=degree_data["degree_global_mean"])
    c_dgm.font = font_header
    c_dgm.alignment = align_center
    c_dgm.border = thin_border
    c_dgm.fill = sub_header_fill
    c_dgm.number_format = '0.00'
    
    for i in range(1, 24):
        deg_it = next((it for it in degree_data["degree_items"] if it["item_id"] == i), None)
        val = deg_it["degree_mean"] if deg_it else None
        cell = ws_matriz.cell(row=deg_row, column=2 + i, value=val)
        cell.alignment = align_center
        cell.border = thin_border
        cell.font = font_header
        cell.fill = sub_header_fill
        if val is not None and not pd.isna(val):
            cell.number_format = '0.00'

    # Autoajuste de anchos de columna
    for ws in [ws_resumen, ws_mejora, ws_matriz]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or '')
                if len(val_str) > max_len and '\n' not in val_str:
                    max_len = len(val_str)
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 10), 45)
            
    # Ajustar ancho especial para matriz
    for i in range(3, 26):
        ws_matriz.column_dimensions[get_column_letter(i)].width = 9

    wb.save(output)
    output.seek(0)
    return output.getvalue()
