"""
app.py — Entry point del dashboard ARCOR.
Navegación por sidebar + tabs por sección.
"""
import os
import streamlit as st
from data import load_data, SLIDE_TITLES
from slides import (
    render_slide_1,
    render_slide_empresa,
    render_slide_2,
    render_slide_3,
    render_slide_4,
    render_slide_5,
    render_slide_6,
    render_slide_7,
    render_slide_8,
    render_slide_9,
    render_slide_10,
)

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    layout="wide",
    page_title="ARCOR - Análisis Financiero",
    page_icon=None,
)

# ── CSS para modo diapositiva (sin scroll, viewport fijo) ────────────────────

SLIDE_CSS = """
<style>
    /* Ocultar scrollbar global */
    ::-webkit-scrollbar {
        display: none;
    }
    
    /* Forzar viewport completo en el contenido principal */
    .main .block-container {
        height: 100vh;
        max-height: 100vh;
        overflow: hidden;
        padding-top: 1rem;
        padding-bottom: 0;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        gap: 0;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label {
        padding: 0.5rem 1rem;
        border-radius: 6px;
        margin: 0.2rem 0;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background-color: #e2e8f0;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
        background-color: #267dc4;
        color: white;
    }
    
    /* Tabs como diapositivas fijas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: #f1f5f9;
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 0.5rem 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #267dc4;
        color: white;
        border-radius: 6px 6px 0 0;
    }
    
    /* Contenido del tab como diapositiva */
    .stTabs [data-baseweb="tab-panel"] {
        height: calc(100vh - 180px);
        max-height: calc(100vh - 180px);
        overflow-y: auto;
        padding: 1rem;
        background-color: white;
        border: 1px solid #e2e8f0;
        border-top: none;
        border-radius: 0 0 8px 8px;
    }
    
    /* Compactar headers */
    .stTabs h2, .stTabs h3 {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
        color: #0f0f0f;
    }
    
    /* Compactar graficos */
    .stPlotlyChart {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Compactar metricas */
    .stMetric {
        padding: 0.5rem;
    }
    
    /* Compactar info boxes */
    .stAlert {
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    
    /* Hacer caption mas legible */
    .stCaption {
        font-size: 0.9rem !important;
        color: #0f0f0f !important;
        font-weight: 500 !important;
    }
    
    /* Todo el texto general mas oscuro y legible */
    .stMarkdown p, .stMarkdown li, .stText {
        color: #0f0f0f;
        font-weight: 500;
    }
    
    /* Ocultar footer de Streamlit */
    footer { display: none; }
    
    /* Ocultar elementos decorativos (no el boton sidebar) */
    [data-testid="stDecoration"] { display: none; }
    #MainMenu { display: none; }
    .stDeployButton { display: none; }
    
    /* Logo mas compacto */
    .stImage {
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    
    /* Warning/alert boxes con mejor contraste */
    .stAlert p {
        font-weight: 500 !important;
    }
</style>
"""

st.markdown(SLIDE_CSS, unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    if os.path.isfile("logo-grupo-arcor.png"):
        st.image("logo-grupo-arcor.png", width=120)
    
    st.markdown("## ARCOR - Análisis Financiero")
    st.caption("Obligaciones Negociables Clases 5 y 6")
    
    st.divider()
    
    section = st.radio(
        "Navegación",
        [
            "Presentación",
            "Rentabilidad",
            "Liquidez",
            "Endeudamiento",
            "Variaciones",
            "Conclusión",
        ],
        label_visibility="collapsed",
    )

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    data = load_data()

    if section == "Presentación":
        tabs = st.tabs(["Carátula", "Sobre la Empresa", "Metodología RT6"])
        with tabs[0]:
            render_slide_1(data, st.container())
        with tabs[1]:
            render_slide_empresa(data, st.container())
        with tabs[2]:
            render_slide_2(data, st.container())

    elif section == "Rentabilidad":
        tabs = st.tabs(["Rentabilidad", "Rotación"])
        with tabs[0]:
            render_slide_3(data, st.container())
        with tabs[1]:
            render_slide_10(data, st.container())

    elif section == "Liquidez":
        tabs = st.tabs(["Liquidez", "Cap. Trabajo + OCF"])
        with tabs[0]:
            render_slide_4(data, st.container())
        with tabs[1]:
            render_slide_5(data, st.container())

    elif section == "Endeudamiento":
        tabs = st.tabs(["Endeudamiento", "Apalancamiento"])
        with tabs[0]:
            render_slide_6(data, st.container())
        with tabs[1]:
            render_slide_7(data, st.container())

    elif section == "Variaciones":
        render_slide_8(data, st.container())

    elif section == "Conclusión":
        render_slide_9(data, st.container())


if __name__ == "__main__":
    main()
