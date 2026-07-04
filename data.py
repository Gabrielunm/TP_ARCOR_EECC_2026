"""
data.py — Carga de datos y constantes para el dashboard ARCOR.
"""
import pandas as pd
import numpy as np
import streamlit as st

# ── Constantes ───────────────────────────────────────────────────────────────

COLORS = {
    "navy": "#267dc4",      # Azul ARCOR (oficial)
    "gold": "#f97316",      # Naranja (mantenido para contraste)
    "white": "#0f0f0f",     # Texto negro puro para legibilidad
    "bg": "#f8fafc",        # Fondo claro
    "red": "#ef4444",       # Rojo para alertas
    "green": "#5bbe45",     # Verde ARCOR (oficial)
    "blue_light": "#dbeafe", # Azul claro
}

FOOTNOTE = (
    "Ajustado por inflación bajo RT6. "
    "*2025: enero-septiembre (balance intermedio). "
    "Importes en millones de $ homogéneos sep2025."
)

SLIDE_TITLES = {
    1: "Portada Institucional",
    2: "Sobre la Empresa",
    3: "Metodología RT6",
    4: "Análisis de Rentabilidad Operativa y Comercial",
    5: "Indicadores de Liquidez",
    6: "Capital de Trabajo y Brecha Operativa (OCF)",
    7: "Estructura de Capital y Paradoja Inflacionaria",
    8: "Apalancamiento y Coberturas Financieras",
    9: "Variaciones Patrimoniales, Actividad y Comparativa de Mercado",
    10: "Limitaciones y Dictamen de Inversión",
    11: "Rotación y Eficiencia Operativa",
}

EXCEL_PATH = "balances_ARCOR.xlsx"
SHEET_NAME = "cuadros"

# ── Row ranges for each block in the Excel sheet ─────────────────────────────
# fmt: (start, end_exclusive, col_names, has_header)
BLOCK_DEFS = {
    "activo_resultado":    (0, 11,   ["Anio", "Total_Activo", "Resultado_Ejercicio", "_c3", "_c4"], True),
    "endeudamiento":       (22, 30,  ["Anio", "Endeudamiento", "Solvencia"], True),
    "liquidez":            (36, 44,  ["Anio", "Liquidez", "Prueba_Acida"], True),
    "capital_trabajo":     (52, 60,  ["Anio", "Capital_Trabajo"], False),
    "ocf":                 (66, 74,  ["Anio", "OCF_Ratio"], False),
    "roa_roe":             (79, 87,  ["Anio", "ROA", "ROE"], True),
    "var_ventas":          (95, 103, ["Anio", "Var_Ventas", "Var_UB"], True),
    "rotacion":            (120, 128, ["Anio", "Rot_Activos", "Rot_Pasivos"], True),
    "arcor_indec":         (136, 144,["Anio", "ARCOR", "INDEC"], True),
    "cashflow":            (151, 159,["Anio", "Act_Operativa", "Act_Inversion", "Act_Financiacion", "Var_Efectivo"], True),
    "leverage":            (182, 189,["Anio", "Leverage"], False),
    # "Tablas maestras" — cleaner, with "2025 (ENE-SEP)" labels
    # Note: +1 start to skip section-title row (e.g. "Tabla de Rentabilidad")
    "tabla_rentabilidad":   (199, 207,["Anio", "ROA", "ROE", "Margen_EBITDA"], True),
    "tabla_liquidez":       (209, 217,["Anio", "Liquidez", "Prueba_Acida", "Cap_Trabajo"], True),
    "tabla_endeudamiento":  (219, 227,["Anio", "Endeudamiento", "Solvencia", "Deuda_EBITDA"], True),
    "tabla_variaciones":    (229, 237,["Anio", "Var_Ventas", "Var_UB", "Rot_Activos", "INDEC_Ventas"], True),
}


def _parse_block(df, start, end, col_names, has_header=True):
    """Parse a fixed-range block into a clean DataFrame."""
    block = df.iloc[start:end].copy()
    ncols = min(len(col_names), block.shape[1])
    block.columns = col_names[:ncols] + [f"_extra_{i}" for i in range(ncols, block.shape[1])]
    if has_header:
        block = block.iloc[1:]  # skip header row
    # Keep only the named columns (drop auxiliary extras)
    use_cols = [c for c in col_names if not c.startswith("_")]
    block = block[use_cols].copy()
    # Drop rows that are entirely empty in the named columns
    block = block.dropna(how="all", subset=use_cols[1:]).reset_index(drop=True)
    # Convert numeric columns
    for c in use_cols[1:]:
        block[c] = pd.to_numeric(block[c], errors="coerce")
    # Filter out rows with "Q" or "H" in year (quarterly / half-year data)
    yr_col = use_cols[0]
    block[yr_col] = block[yr_col].astype(str).str.strip()
    block = block[~block[yr_col].str.contains(r"[QH]", na=False, regex=True)].reset_index(drop=True)
    # Preserve original year label (e.g. "2025 (ENE-SEP)")
    return block


@st.cache_data(ttl=3600)
def load_data():
    """
    Carga el Excel, parsea todos los bloques y devuelve un dict[str, DataFrame].

    Overrides conocidos:
    - Var% Ventas 2025 → -7.8% (valor del TP, no 0.61 del Excel raw)
    - ARCOR vs INDEC 2025 → -7.8% (misma corrección)
    """
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME, header=None)
    except FileNotFoundError:
        st.error(
            "Error: No se encontró el archivo balances_ARCOR.xlsx. "
            "Verificar que esté en el directorio de la aplicación."
        )
        st.stop()
    except Exception as e:
        st.error(f"Error al leer el archivo Excel: {e}")
        st.stop()

    data = {}
    for key, (start, end, col_names, has_header) in BLOCK_DEFS.items():
        data[key] = _parse_block(df, start, end, col_names, has_header)

    # ── Correcciones post-parseo ─────────────────────────────────────────

    # 1) Var% Ventas 2025: override TP value -7.8%
    vv = data["var_ventas"]
    mask_vv2025 = vv["Anio"].str.contains("2025", na=False)
    vv.loc[mask_vv2025, "Var_Ventas"] = -0.078
    # Var_UB 2025 no disponible para 9 meses
    vv.loc[mask_vv2025, "Var_UB"] = np.nan

    # 2) ARCOR vs INDEC 2025: override ARCOR, leave INDEC
    ai = data["arcor_indec"]
    mask_ai2025 = ai["Anio"].str.contains("2025", na=False)
    ai.loc[mask_ai2025, "ARCOR"] = -0.078
    # INDEC 2025: no disponible, queda NaN

    # 3) tabla_variaciones: 2025 Var_Ventas también override
    tv = data["tabla_variaciones"]
    mask_tv2025 = tv["Anio"].str.contains("2025", na=False)
    tv.loc[mask_tv2025, "Var_Ventas"] = -0.078
    tv.loc[mask_tv2025, "Var_UB"] = np.nan

    return data
