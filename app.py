"""
Aplicación Web Interactiva para la Explotación de Encuestas Docentes Universitarias
Permite el análisis a nivel de titulación y de asignatura, identifica ítems críticos (< 3.5)
y propone planes de acciones de mejora correctivas.
"""

import os
import io
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from recommendations import SURVEY_ITEMS, get_item_info, get_dimension_color
from data_processor import load_subject_excel, consolidate_degree_data
from sample_generator import generate_sample_files_bundle
from report_exporter import generate_degree_excel_report

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Explotación de Encuestas Docentes | Auditoría de Calidad",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Personalizados
st.markdown("""
<style>
    /* Estilos generales */
    .main-header {
        font-size: 2.1rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.1rem;
    }
    .sub-header {
        font-size: 1.0rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%);
        border: 1px solid #DBEAFE;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        margin-bottom: 12px;
    }
    .metric-card-alert {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border: 1px solid #FECACA;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        margin-bottom: 12px;
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 800;
        color: #1E3A8A;
    }
    .metric-value-alert {
        font-size: 1.9rem;
        font-weight: 800;
        color: #DC2626;
    }
    .metric-label {
        font-size: 0.82rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .action-card {
        background-color: #FFFFFF;
        border-left: 5px solid #DC2626;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        padding: 18px;
        margin-bottom: 16px;
        border-top: 1px solid #F3F4F6;
        border-right: 1px solid #F3F4F6;
        border-bottom: 1px solid #F3F4F6;
    }
    .badge-critical {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
    }
    .badge-ok {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado de sesión
if "uploaded_subjects" not in st.session_state:
    st.session_state.uploaded_subjects = []
if "is_demo_loaded" not in st.session_state:
    st.session_state.is_demo_loaded = False

# ==========================================
# BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/university.png", width=64)
    st.title("Gestión de Encuestas")
    st.markdown("---")
    
    st.subheader("📁 Carga de Archivos")
    st.markdown(
        "Cargue los archivos Excel de las asignaturas. "
        "El **nombre del archivo** identifica la asignatura y el **nombre de la pestaña** la titulación."
    )
    
    uploaded_files = st.file_uploader(
        "Arrastre o seleccione archivos Excel:",
        type=["xlsx", "xls"],
        accept_multiple_files=True,
        help="Cada archivo debe corresponder a una asignatura con 23 ítems evaluados de 1 a 5."
    )
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🧪 Cargar Demo", use_container_width=True, help="Carga datos realistas de prueba para el Grado en ADE"):
            demo_bundle = generate_sample_files_bundle("Grado en ADE")
            parsed_subjects = []
            for fname, buf in demo_bundle:
                try:
                    s_data = load_subject_excel(buf, filename_hint=fname)
                    parsed_subjects.append(s_data)
                except Exception as e:
                    st.error(f"Error en {fname}: {e}")
            st.session_state.uploaded_subjects = parsed_subjects
            st.session_state.is_demo_loaded = True
            st.rerun()

    with col_btn2:
        if st.button("🗑️ Limpiar", use_container_width=True):
            st.session_state.uploaded_subjects = []
            st.session_state.is_demo_loaded = False
            st.rerun()

    # Procesar archivos subidos manualmente
    if uploaded_files:
        parsed_subjects = []
        for uf in uploaded_files:
            try:
                s_data = load_subject_excel(uf, filename_hint=uf.name)
                parsed_subjects.append(s_data)
            except Exception as e:
                st.error(f"Error procesando {uf.name}: {e}")
                
        if parsed_subjects:
            st.session_state.uploaded_subjects = parsed_subjects
            st.session_state.is_demo_loaded = False

    st.markdown("---")
    st.subheader("⚙️ Configuración")
    threshold = st.slider(
        "Umbral de Alerta para Acciones de Mejora:",
        min_value=3.0,
        max_value=4.0,
        value=3.5,
        step=0.1,
        help="Los ítems con puntuación media inferior a este umbral activarán planes de mejora correctivos."
    )
    
    st.markdown("---")
    st.caption("Sistema de Auditoría de Encuestas Docentes v1.0\nEscala Likert 1-5 (1: Mínimo, 5: Máximo, N/S excluido)")

# ==========================================
# CABECERA PRINCIPAL
# ==========================================
st.markdown('<div class="main-header">🎓 Explotación de Encuestas Docentes Universitarias</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Auditoría integral de satisfacción académica a nivel de Titulación y Asignatura con generación automática de Planes de Mejora (< 3.5 puntos)</div>', unsafe_allow_html=True)

# Comprobar si hay datos cargados
subjects_list = st.session_state.uploaded_subjects

if not subjects_list:
    st.info(
        "👋 **Bienvenido al Sistema de Explotación de Encuestas Docentes**\n\n"
        "Para comenzar a explotar los resultados:\n"
        "1. **Cargue los archivos Excel** de cada una de las asignaturas usando el panel lateral izquierdo.\n"
        "2. O bien haga clic en **'🧪 Cargar Demo'** para explorar de inmediato el cuadro de mando con un conjunto de asignaturas de prueba del *Grado en ADE*.\n\n"
        "**Requisitos de los archivos Excel:**\n"
        "- **Nombre del archivo:** Corresponde al nombre de la asignatura (ej. `Microeconomía.xlsx`).\n"
        "- **Nombre de la pestaña:** Identifica el Grado o Máster (ej. `Grado en ADE`).\n"
        "- **Contenido:** 23 ítems evaluados en escala de 1 a 5 (con soporte para `N/S: No sabe / No contesta`)."
    )
    st.stop()

# Agrupar por titulación si hubiese múltiples
degrees_available = list(set(s["degree_name"] for s in subjects_list))
if len(degrees_available) > 1:
    selected_degree = st.selectbox("Seleccione la Titulación a analizar:", degrees_available)
    filtered_subjects = [s for s in subjects_list if s["degree_name"] == selected_degree]
else:
    selected_degree = degrees_available[0]
    filtered_subjects = subjects_list

# Consolidar datos de la titulación seleccionada
degree_data = consolidate_degree_data(filtered_subjects)

# Actualizar el umbral dinámico si el usuario movió el slider
for s in filtered_subjects:
    s["items_under_35"] = [it for it in s["items"] if it["mean"] < threshold and not np.isnan(it["mean"])]
    s["items_under_35_count"] = len(s["items_under_35"])
    
all_actions = []
for s in filtered_subjects:
    for it in s["items_under_35"]:
        all_actions.append({
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
all_actions.sort(key=lambda x: x["mean_score"])
degree_data["all_improvement_actions"] = all_actions

# ==========================================
# PESTAÑAS PRINCIPALES DE NAVEGACIÓN
# ==========================================
tab_titulacion, tab_asignatura, tab_mejoras, tab_matriz = st.tabs([
    "🏛️ 1. Visión Titulación",
    "📘 2. Análisis por Asignatura",
    "🛠️ 3. Plan de Acciones de Mejora (< 3.5)",
    "📊 4. Matriz Comparativa y Exportación"
])

# -------------------------------------------------------------------------
# TAB 1: VISIÓN GLOBAL DE LA TITULACIÓN
# -------------------------------------------------------------------------
with tab_titulacion:
    st.subheader(f"Resumen Global: {selected_degree}")
    
    # Tarjetas Métricas Superiores
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Asignaturas Evaluadas</div>
            <div class="metric-value">{degree_data['total_subjects']}</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Evaluaciones</div>
            <div class="metric-value">{degree_data['total_responses']}</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        deg_mean = degree_data['degree_global_mean']
        color_val = "#1E3A8A" if deg_mean >= threshold else "#DC2626"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Media Global Titulación</div>
            <div class="metric-value" style="color: {color_val};">{deg_mean:.2f} <span style="font-size:1.1rem; color:#6B7280;">/ 5</span></div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        failing_subjs = sum(1 for s in filtered_subjects if s['items_under_35_count'] > 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Asignaturas con Alertas</div>
            <div class="metric-value">{failing_subjs} <span style="font-size:1.0rem; color:#6B7280;">/ {degree_data['total_subjects']}</span></div>
        </div>
        """, unsafe_allow_html=True)
    with k5:
        n_criticos = len(all_actions)
        card_class = "metric-card-alert" if n_criticos > 0 else "metric-card"
        val_class = "metric-value-alert" if n_criticos > 0 else "metric-value"
        st.markdown(f"""
        <div class="{card_class}">
            <div class="metric-label">Total Ítems en Alerta (< {threshold})</div>
            <div class="{val_class}">{n_criticos}</div>
        </div>
        """, unsafe_allow_html=True)

    # Conclusiones Ejecutivas de la Titulación
    st.markdown("### 📋 Conclusiones Ejecutivas de la Titulación")
    
    # Análisis automatizado cualitativo
    top_subject = degree_data["subjects_ranking"][0]
    bottom_subject = degree_data["subjects_ranking"][-1]
    
    # Identificar ítems transversales más fuertes y más débiles
    sorted_deg_items = sorted([it for it in degree_data["degree_items"] if not np.isnan(it["degree_mean"])], key=lambda x: x["degree_mean"])
    weakest_items = sorted_deg_items[:3]
    strongest_items = sorted_deg_items[-3:][::-1]
    
    col_conc1, col_conc2 = st.columns(2)
    with col_conc1:
        st.markdown(f"""
        **🌟 Principales Fortalezas:**
        - **Asignatura líder:** **{top_subject['subject_name']}** con una valoración sobresaliente de **{top_subject['global_mean']:.2f} / 5.0**.
        - **Aspectos mejor valorados en la titulación:**
        """)
        for it in strongest_items:
            st.markdown(f"  - **{it['code']}: {it['short_title']}** ({it['degree_mean']:.2f} pts) — *{it['dimension']}*")
            
    with col_conc2:
        st.markdown(f"""
        **⚠️ Puntos de Atención Prioritaria:**
        - **Asignatura con mayor necesidad de apoyo:** **{bottom_subject['subject_name']}** ({bottom_subject['global_mean']:.2f} / 5.0, con {bottom_subject['items_under_35_count']} ítems < {threshold}).
        - **Aspectos transversales con menor puntuación:**
        """)
        for it in weakest_items:
            alerta = "🚨 **Requiere intervención**" if it['degree_mean'] < threshold else "⚠️ **A vigilar**"
            st.markdown(f"  - **{it['code']}: {it['short_title']}** ({it['degree_mean']:.2f} pts) — {alerta}")

    st.markdown("---")

    # Gráficos de Titulación
    c_graf1, c_graf2 = st.columns([6, 4])
    
    with c_graf1:
        st.markdown("#### 🏆 Ranking de Asignaturas de la Titulación")
        df_rank = pd.DataFrame([
            {
                "Asignatura": s["subject_name"],
                "Media": s["global_mean"],
                "Alertas": s["items_under_35_count"],
                "Color": "#DC2626" if s["global_mean"] < threshold else ("#D97706" if s["items_under_35_count"] > 0 else "#2563EB")
            }
            for s in degree_data["subjects_ranking"]
        ])
        
        fig_rank = px.bar(
            df_rank,
            x="Media",
            y="Asignatura",
            orientation="h",
            text="Media",
            color="Color",
            color_discrete_map="identity",
            labels={"Media": "Puntuación Media (1-5)", "Asignatura": ""}
        )
        fig_rank.add_vline(x=threshold, line_dash="dash", line_color="#DC2626", annotation_text=f"Umbral ({threshold})", annotation_position="top right")
        fig_rank.update_layout(
            height=340,
            yaxis=dict(autorange="reversed"),
            xaxis=dict(range=[1, 5.2]),
            margin=dict(l=10, r=20, t=20, b=20),
            showlegend=False
        )
        st.plotly_chart(fig_rank, use_container_width=True)

    with c_graf2:
        st.markdown("#### 🎯 Rendimiento por Dimensión Pedagógica")
        df_dims = pd.DataFrame(degree_data["dimensions_summary"])
        fig_dim = px.bar(
            df_dims,
            x="dimension",
            y="mean",
            text="mean",
            color="mean",
            color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
            range_color=[3.0, 4.6],
            labels={"mean": "Media", "dimension": "Dimensión"}
        )
        fig_dim.add_hline(y=threshold, line_dash="dash", line_color="#DC2626")
        fig_dim.update_layout(
            height=340,
            yaxis=dict(range=[1, 5.2]),
            margin=dict(l=10, r=20, t=20, b=20),
            xaxis_tickangle=-35,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_dim, use_container_width=True)

    # Mapa de Calor Transversal (Heatmap)
    st.markdown("#### 🗺️ Mapa de Calor: Asignaturas vs 23 Ítems de la Encuesta")
    st.caption("Permite visualizar de un vistazo qué asignaturas concentran debilidades y qué ítems fallan de forma recurrente.")
    
    # Preparar matriz numérica
    heatmap_matrix = []
    heatmap_subjs = [s["subject_name"] for s in filtered_subjects]
    heatmap_items = [f"IT{i:02d}" for i in range(1, 24)]
    
    for s in filtered_subjects:
        row_vals = []
        for i in range(1, 24):
            item_obj = next((it for it in s["items"] if it["item_id"] == i), None)
            row_vals.append(item_obj["mean"] if item_obj else np.nan)
        heatmap_matrix.append(row_vals)

    fig_heat = px.imshow(
        heatmap_matrix,
        x=heatmap_items,
        y=heatmap_subjs,
        labels=dict(x="Ítems de Encuesta", y="Asignatura", color="Puntuación"),
        color_continuous_scale=[
            (0.0, "#EF4444"),   # Rojo
            (0.5, "#FCD34D"),   # Ámbar
            (1.0, "#34D399")    # Verde
        ],
        zmin=2.5,
        zmax=5.0,
        aspect="auto"
    )
    fig_heat.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# -------------------------------------------------------------------------
# TAB 2: ANÁLISIS DETALLADO POR ASIGNATURA
# -------------------------------------------------------------------------
with tab_asignatura:
    st.subheader("Diagnóstico Individual por Asignatura")
    
    subj_names = [s["subject_name"] for s in filtered_subjects]
    selected_subject_name = st.selectbox("Seleccione la Asignatura:", subj_names)
    
    current_subject = next(s for s in filtered_subjects if s["subject_name"] == selected_subject_name)
    
    # Métricas de la asignatura seleccionada
    sa1, sa2, sa3, sa4 = st.columns(4)
    with sa1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Media Asignatura</div>
            <div class="metric-value">{current_subject['global_mean']:.2f} <span style="font-size:1.0rem; color:#6B7280;">/ 5</span></div>
        </div>
        """, unsafe_allow_html=True)
    with sa2:
        diff_deg = current_subject['global_mean'] - degree_data['degree_global_mean']
        diff_str = f"+{diff_deg:.2f}" if diff_deg >= 0 else f"{diff_deg:.2f}"
        diff_color = "#166534" if diff_deg >= 0 else "#DC2626"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Comparativa con Titulación</div>
            <div class="metric-value" style="color: {diff_color};">{diff_str} pts</div>
        </div>
        """, unsafe_allow_html=True)
    with sa3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Muestra de Respuestas</div>
            <div class="metric-value">{current_subject['total_responses']}</div>
        </div>
        """, unsafe_allow_html=True)
    with sa4:
        n_alerts_subj = current_subject['items_under_35_count']
        card_c = "metric-card-alert" if n_alerts_subj > 0 else "metric-card"
        val_c = "metric-value-alert" if n_alerts_subj > 0 else "metric-value"
        st.markdown(f"""
        <div class="{card_c}">
            <div class="metric-label">Ítems < {threshold} pts</div>
            <div class="{val_c}">{n_alerts_subj}</div>
        </div>
        """, unsafe_allow_html=True)

    # Gráfico de barras de los 23 ítems de esta asignatura
    st.markdown(f"#### 📊 Evaluación de los 23 Ítems en **{current_subject['subject_name']}**")
    
    df_items_subj = pd.DataFrame(current_subject["items"])
    df_items_subj["Etiqueta"] = df_items_subj["code"] + ": " + df_items_subj["short_title"]
    df_items_subj["Color"] = df_items_subj["mean"].apply(
        lambda m: "#DC2626" if m < threshold else ("#D97706" if m < 4.0 else "#16A34A")
    )
    
    fig_subj_items = px.bar(
        df_items_subj,
        x="code",
        y="mean",
        text="mean",
        color="Color",
        color_discrete_map="identity",
        hover_data={"short_title": True, "dimension": True, "mean": ":.2f", "code": False},
        labels={"mean": "Media", "code": "Ítem"}
    )
    fig_subj_items.add_hline(
        y=threshold,
        line_dash="dash",
        line_color="#DC2626",
        annotation_text=f"Umbral Mínimo ({threshold})",
        annotation_position="top left"
    )
    fig_subj_items.update_layout(
        height=360,
        yaxis=dict(range=[1, 5.2]),
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False
    )
    st.plotly_chart(fig_subj_items, use_container_width=True)

    # Desglose de respuestas Likert
    if current_subject["total_responses"] > 0 and current_subject["items"][0]["valid_count"] > 0:
        st.markdown("#### 👥 Distribución Porcentual de Respuestas por Ítem (Escala Likert)")
        fig_dist = go.Figure()
        
        fig_dist.add_trace(go.Bar(
            name="% Desacuerdo (1-2)",
            x=df_items_subj["code"],
            y=df_items_subj["pct_disagree"],
            marker_color="#EF4444"
        ))
        fig_dist.add_trace(go.Bar(
            name="% Neutro (3)",
            x=df_items_subj["code"],
            y=df_items_subj["pct_neutral"],
            marker_color="#FBBF24"
        ))
        fig_dist.add_trace(go.Bar(
            name="% De Acuerdo (4-5)",
            x=df_items_subj["code"],
            y=df_items_subj["pct_agree"],
            marker_color="#10B981"
        ))
        fig_dist.add_trace(go.Bar(
            name="% No Sabe (N/S)",
            x=df_items_subj["code"],
            y=df_items_subj["ns_pct"],
            marker_color="#9CA3AF"
        ))
        
        fig_dist.update_layout(
            barmode="stack",
            height=300,
            yaxis=dict(title="% Respuestas", range=[0, 100]),
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    # Tabla resumen de los 23 ítems
    with st.expander("🔍 Ver tabla detallada con los 23 ítems y textos completos"):
        df_display = df_items_subj[[
            "code", "short_title", "dimension", "mean", "std", "ns_pct", "alert_severity"
        ]].copy()
        df_display.columns = ["Código", "Ítem", "Dimensión", "Media", "Desv. Típica", "% N/S", "Estado"]
        st.dataframe(df_display, use_container_width=True, hide_index=True)

# -------------------------------------------------------------------------
# TAB 3: PLAN DE ACCIONES DE MEJORA (< 3.5)
# -------------------------------------------------------------------------
with tab_mejoras:
    st.subheader(f"🛠️ Plan de Acciones de Mejora Correctivas (Ítems < {threshold})")
    
    if not all_actions:
        st.success(f"🎉 **¡Enhorabuena!** No se han detectado ítems con valoración inferior a {threshold} puntos en ninguna asignatura de la titulación.")
    else:
        st.markdown(
            f"Se han identificado **{len(all_actions)} casos** de ítems por debajo del umbral de calidad exigido ({threshold} puntos) "
            "en las asignaturas analizadas. A continuación se presentan las propuestas de acciones de mejora concretas, "
            "indicadores de seguimiento y responsabilidades asignadas."
        )
        
        # Filtros para el plan de mejoras
        col_filtro1, col_filtro2 = st.columns(2)
        with col_filtro1:
            filtro_asig = st.selectbox("Filtrar por Asignatura:", ["Todas"] + sorted(list(set(a["subject_name"] for a in all_actions))))
        with col_filtro2:
            filtro_dim = st.selectbox("Filtrar por Dimensión:", ["Todas"] + sorted(list(set(a["dimension"] for a in all_actions))))
            
        filtered_actions = all_actions
        if filtro_asig != "Todas":
            filtered_actions = [a for a in filtered_actions if a["subject_name"] == filtro_asig]
        if filtro_dim != "Todas":
            filtered_actions = [a for a in filtered_actions if a["dimension"] == filtro_dim]

        st.markdown(f"**Mostrando {len(filtered_actions)} fichas de mejora:**")
        
        # Mostrar fichas ejecutivas de mejora
        for act in filtered_actions:
            sev_color = "#DC2626" if "Crítico" in act["alert_severity"] else "#D97706"
            
            st.markdown(f"""
            <div class="action-card" style="border-left-color: {sev_color};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div>
                        <strong style="font-size: 1.15rem; color: #1E3A8A;">{act['subject_name']}</strong> — 
                        <span style="font-size: 1.05rem; font-weight: 600;">{act['item_code']}: {act['item_title']}</span>
                        <div style="font-size: 0.85rem; color: #6B7280;">Dimensión: {act['dimension']}</div>
                    </div>
                    <div>
                        <span class="badge-critical" style="background-color: {'#FEE2E2' if act['mean_score'] < 3.0 else '#FEF3C7'}; color: {'#991B1B' if act['mean_score'] < 3.0 else '#92400E'};">
                            Media: {act['mean_score']:.2f} / 5.00 ({act['alert_severity']})
                        </span>
                    </div>
                </div>
                <div style="margin-top: 10px; margin-bottom: 8px; color: #374151;">
                    <strong>🔍 Diagnóstico:</strong> {act['diagnosis']}
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 12px; background: #F8FAFC; padding: 12px; border-radius: 6px;">
                    <div>
                        <strong style="color: #1E40AF;">⚡ Acción Inmediata (Próximo Semestre):</strong><br>
                        <span style="font-size: 0.92rem;">{act['action_short_term']}</span>
                    </div>
                    <div>
                        <strong style="color: #475569;">🏛️ Acción Estructural (Medio Plazo):</strong><br>
                        <span style="font-size: 0.92rem;">{act['action_medium_term']}</span>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 0.85rem; color: #4B5563;">
                    <div><strong>🎯 KPI de Éxito:</strong> {act['kpi']}</div>
                    <div><strong>👤 Responsable:</strong> {act['responsible']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# -------------------------------------------------------------------------
# TAB 4: MATRIZ COMPARATIVA Y EXPORTACIÓN
# -------------------------------------------------------------------------
with tab_matriz:
    st.subheader("Matriz Cruzada de Calidad & Descarga de Informes")
    
    st.markdown(
        "Esta matriz permite comparar de forma tabular todas las asignaturas frente a los 23 ítems evaluados. "
        "Las celdas se colorean automáticamente: <span style='color:#DC2626; font-weight:bold;'>Rojo</span> para notas < 3.5, "
        "<span style='color:#D97706; font-weight:bold;'>Ámbar</span> para notas 3.5 - 3.99, y "
        "<span style='color:#16A34A; font-weight:bold;'>Verde</span> para notas ≥ 4.0.",
        unsafe_allow_html=True
    )
    
    # Construcción de la matriz formateada
    matrix_data = []
    for s in filtered_subjects:
        row = {"Asignatura": s["subject_name"], "Media Global": s["global_mean"]}
        for i in range(1, 24):
            item_obj = next((it for it in s["items"] if it["item_id"] == i), None)
            row[f"IT{i:02d}"] = item_obj["mean"] if item_obj else np.nan
        matrix_data.append(row)
        
    df_matrix_display = pd.DataFrame(matrix_data)
    
    def highlight_score(val):
        if pd.isna(val) or not isinstance(val, (int, float)):
            return ''
        if val < threshold:
            return 'background-color: #FEE2E2; color: #991B1B; font-weight: bold;'
        elif val < 4.0:
            return 'background-color: #FEF3C7; color: #92400E;'
        else:
            return 'background-color: #DCFCE7; color: #166534;'
            
    styled_df = df_matrix_display.style.format(
        {col: "{:.2f}" for col in df_matrix_display.columns if col != "Asignatura"}
    ).map(
        highlight_score,
        subset=[col for col in df_matrix_display.columns if col != "Asignatura"]
    )
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📥 Exportación de Informes Ejecutivos")
    
    col_exp1, col_exp2 = st.columns([6, 4])
    with col_exp1:
        st.markdown(
            "Descargue el informe consolidado completo en formato **Excel (.xlsx)**. "
            "El archivo contiene cuatro pestañas estructuradas con formato institucional:\n"
            "1. **Resumen Titulación:** KPIs, ranking de asignaturas y valoración por dimensiones.\n"
            "2. **Plan de Mejora (< 3.5):** Detalle de asignaturas, ítems críticos, acciones correctivas, responsables y KPIs.\n"
            "3. **Matriz de Ítems:** Matriz completa de notas con formato condicional de colores.\n"
            "4. **Detalle por Asignatura:** Registro de las 23 preguntas."
        )
    with col_exp2:
        excel_bytes = generate_degree_excel_report(degree_data, filtered_subjects)
        file_clean_deg = selected_degree.replace(' ', '_').replace('/', '_')
        st.download_button(
            label="📊 Descargar Informe de Calidad en Excel (.xlsx)",
            data=excel_bytes,
            file_name=f"Informe_Encuestas_Docentes_{file_clean_deg}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# Pie de página
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6B7280; font-size: 0.85rem;'>"
    "Sistema de Explotación de Encuestas Docentes & Planes de Mejora | Desarrollado con Antigravity & Streamlit"
    "</div>",
    unsafe_allow_html=True
)
