"""
slides.py — 9 funciones render_slide_N(data, container) para el dashboard ARCOR.
Cada función recibe el dict de DataFrames y un contenedor de Streamlit.
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import os
from data import COLORS, FOOTNOTE


# ── Helpers compartidos ──────────────────────────────────────────────────────

def _normalize_year_label(y):
    """Muestra '2025*' para cualquier label que contenga 2025."""
    s = str(y).strip()
    if "2025" in s:
        return "2025*"
    return s


def _apply_chart_layout(fig, title="", hovermode="x unified"):
    """Estilo claro consistente para todos los charts."""
    fig.update_layout(
        title=dict(text=title, font=dict(color=COLORS["white"], size=16), x=0.5),
        plot_bgcolor=COLORS["bg"],
        paper_bgcolor=COLORS["bg"],
        font=dict(color=COLORS["white"], size=12),
        hovermode=hovermode,
        xaxis=dict(
            gridcolor="#e2e8f0",
            zerolinecolor="#cbd5e1",
            tickfont=dict(color=COLORS["white"]),
            title_font=dict(color=COLORS["white"]),
        ),
        yaxis=dict(
            gridcolor="#e2e8f0",
            zerolinecolor="#cbd5e1",
            tickfont=dict(color=COLORS["white"]),
            title_font=dict(color=COLORS["white"]),
        ),
        legend=dict(font=dict(color=COLORS["white"]), orientation="h", y=1.12),
        margin=dict(l=60, r=40, t=60, b=60),
    )
    return fig


def _render_footer(container):
    """Append footnote + separator al final de un slide."""
    with container:
        st.divider()
        st.caption(FOOTNOTE)


def _metric_card_html(label, value, delta=None, color=COLORS["gold"]):
    """Tarjeta HTML compacta para métricas destacadas."""
    delta_html = f"<span style='color:#22c55e; font-size:0.8rem;'>▲ {delta}</span>" if delta else ""
    return f"""
    <div style="background:#f1f5f9; padding:0.6rem; border-radius:6px;
                border-left:3px solid {color}; margin:0.3rem 0;">
        <p style="color:#64748b; font-size:0.7rem; margin:0;">{label}</p>
        <p style="color:{color}; font-size:1.2rem; font-weight:700; margin:0;">{value}</p>
        {delta_html}
    </div>
    """


def _formula_card_html(label, formula, color=COLORS["navy"]):
    """Tarjeta HTML compacta para fórmulas LaTeX."""
    return f"""
    <div style="background:#f8fafc; padding:0.5rem; border-radius:6px;
                border:1px solid #e2e8f0; margin:0.3rem 0;">
        <p style="color:#64748b; font-size:0.65rem; margin:0 0 0.2rem 0;">{label}</p>
        <p style="color:{color}; font-size:0.8rem; font-weight:600; margin:0;
                   font-family: 'Courier New', monospace;">{formula}</p>
    </div>
    """


def _tooltip_html(text, color="#64748b"):
    """Tooltip informativo con icono de ayuda."""
    return f"""
    <span style="color:{color}; font-size:0.65rem; cursor:help;
                 border-bottom:1px dotted {color};">
        {text}
    </span>
    """


def _explanation_row(items, help_text=None):
    """Row horizontal con explicaciones simples de cada indicador."""
    cols = st.columns(len(items))
    for col, (label, desc) in zip(cols, items):
        with col:
            st.markdown(
                f'<p style="color:#0f0f0f; font-size:0.85rem; font-weight:500; '
                f'margin:0.2rem 0; line-height:1.4;">'
                f'<strong>{label}</strong>: {desc}</p>',
                unsafe_allow_html=True,
            )
    if help_text:
        st.caption(help_text)


def _status_indicator(value, thresholds, labels=("Bueno", "Regular", "Malo")):
    """Indicador visual de estado basado en umbrales."""
    if value >= thresholds[0]:
        return f'<span style="color:#22c55e; font-weight:600;">{labels[0]}</span>'
    elif value >= thresholds[1]:
        return f'<span style="color:#f97316; font-weight:600;">{labels[1]}</span>'
    else:
        return f'<span style="color:#ef4444; font-weight:600;">{labels[2]}</span>'


# ── Slide 1: Portada Institucional ───────────────────────────────────────────

def render_slide_1(data, container):
    with container:
        # Logo + boton de descarga
        if os.path.isfile("logo-grupo-arcor.png"):
            col_logo, col_btn = st.columns([3, 1])
            with col_logo:
                st.image("logo-grupo-arcor.png", width=80)
            with col_btn:
                tp_path = "GRUPO 9 - TP EECC ARCOR.pdf"
                if os.path.isfile(tp_path):
                    with open(tp_path, "rb") as f:
                        st.download_button(
                            label="Descargar TP",
                            data=f,
                            file_name="GRUPO 9 - TP EECC ARCOR.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )
        else:
            # Sin logo, mostrar boton solo
            col_btn, _ = st.columns([1, 4])
            with col_btn:
                tp_path = "GRUPO 9 - TP EECC ARCOR.pdf"
                if os.path.isfile(tp_path):
                    with open(tp_path, "rb") as f:
                        st.download_button(
                            label="Descargar TP",
                            data=f,
                            file_name="GRUPO 9 - TP EECC ARCOR.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )

        st.markdown("## Análisis de Estados Contables — ARCOR S.A.I.C.")
        st.markdown(
            "**Evaluación de Riesgo Crediticio e Inversión en "
            "Obligaciones Negociables (Clases 5 y 6)**"
        )

        st.markdown(
            f"<div style='text-align:center; background:{COLORS['navy']}; "
            f"padding:0.6rem; border-radius:8px; margin:0.6rem 0;'>"
            f"<h3 style='color:white; margin:0; font-size:1.3rem;'>"
            f"Período 2019 — 2025*</h3>"
            f"<p style='color:#e2e8f0; margin:0; font-size:0.8rem;'>"
            f"enero-septiembre · valores en moneda homogénea (RT6)</p>"
            f"</div>",
            unsafe_allow_html=True,
        )

        # Metadata secundaria (chico, no roba atención)
        st.caption(
            "CUIT 30-50279317-5 · Destinatario: Acreedores Financieros · "
            "Analistas: Arpires Anael, Galván Ariadna, Godoy Karla, "
            "Lopez Natalia, Quiroga Gabriel"
        )

    _render_footer(container)


# ── Slide 1b: Sobre la Empresa ────────────────────────────────────────────────

def render_slide_empresa(data, container):
    with container:
        st.subheader("Grupo Arcor")
        st.markdown("""
- **Rubro:** Alimentación — alimentos de consumo masivo, agronegocios y packaging
- **Fundación:** 1951 en Arroyito, Córdoba (conjunción de *Ar*royito + *Cór*doba)
- **Presencia global:** 49 plantas industriales, oficinas en 4 continentes, +20.000 empleados
- **Líder mundial en caramelos duros** — produce +2 millones de kilos al año, exporta a más de 120 países
- **Principal exportador de golosinas** de Argentina, Chile y Perú
- **~30% de ventas en USD** — subsidiarias en el exterior + exportación directa cubren holgadamente la deuda internacional (Fix SCR)
- **Marcas principales:** Águila, Noel, La Campagnola, Arcor, Bagley (51% Danone)
- **Calificación:** Fix SCR AAA(arg) — máxima calidad crediticia en Argentina
        """)

        st.markdown("**Integración vertical** — Cartocor (envases), Bagley (galletitas), "
                    "La Campagnola (conservas), Mastellone 43% (lácteos), "
                    "agronegocios propios. Controla toda la cadena de valor.")

        st.info("**¿Por qué analizamos ARCOR?**  \n"
                "Emisión de Obligaciones Negociables Clases 5 y 6. "
                "Evaluamos su capacidad de pago y riesgo crediticio "
                "mediante el análisis de Estados Contables 2019–2025*.")

    _render_footer(container)


# ── Slide 1c: Integración Vertical ─────────────────────────────────────────────

def render_slide_integracion(data, container):
    with container:
        st.subheader("Integración Vertical")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("""
- **Cartocor, Zucamor, Converflex** — producen sus propios envases, cartón y packaging (~22% ventas)
- **Bagley** (51% Arcor + Danone) — galletitas y cereales, líder en Latinoamérica (~23% ventas)
- **La Campagnola** — conservas, dulces, salsas y puré de tomates
- **Mastellone Hnos.** (43%) — lácteos (La Serenísima)
- **Agronegocios propios** — materia prima desde el campo hasta el producto final (~14% ventas)
- **Golosinas y Chocolates** — caramelos duros, chicles, chocolates (~32% ventas, líder mundial)
            """)

        with col2:
            # Donut chart de distribución por segmento (Moody's Local Argentina 2024)
            segments = ["Golosinas y\nChocolates", "Galletas\n(Bagley)", "Packaging\n(Cartocor)", "Agronegocios"]
            values = [32, 23, 22, 14]
            colors = [COLORS["navy"], COLORS["gold"], COLORS["green"], "#94a3b8"]

            fig = go.Figure(data=[go.Pie(
                labels=segments, values=values,
                hole=0.5,
                marker=dict(colors=colors, line=dict(color=COLORS["bg"], width=2)),
                textinfo="label+percent",
                textfont=dict(color="white", size=10),
                hovertemplate="%{label}<br>%{percent} de ventas<extra></extra>",
            )])
            fig.update_layout(
                title=dict(
                    text="Ventas por Segmento (2024)",
                    font=dict(color=COLORS["white"], size=14),
                    x=0.5,
                ),
                paper_bgcolor=COLORS["bg"],
                plot_bgcolor=COLORS["bg"],
                height=260,
                margin=dict(l=10, r=10, t=40, b=10),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

        st.success(
            "**¿Por qué importa?**  \n"
            "Arcor no solo fabrica alimentos: fabrica el envase, el cartón, "
            "procesa la materia prima y distribuye. Eso la protege de "
            "proveedores externos, reduce costos y le da control total "
            "sobre la cadena de valor."
        )

    _render_footer(container)


# ── Slide 2: Síntesis + RT6 ──────────────────────────────────────────────────

def render_slide_2(data, container):
    with container:
        st.subheader("Metodología RT6")
        st.info(
            "Reexpresión a moneda homogénea de septiembre 2025* "
            "mediante RT6 (FACPCE).\n\n"
            "**Importe Homogéneo = Importe Histórico × Índice de Reexpresión**\n\n"
            "Coeficientes AXI al 30/09/2025:\n"
            "- 2019: **33,11** — 2024: **1,22**\n\n"
            "**Nota**: Todos los importes monetarios están "
            "expresados en millones de pesos ($M)."
        )

        st.warning(
            "**Limitación:** 2025* corresponde solo a los primeros 9 meses "
            "(enero-septiembre), según balance intermedio acumulado al 30/09/2025."
        )

    _render_footer(container)


# ── Slide 3: Rentabilidad ────────────────────────────────────────────────────

def render_slide_3(data, container):
    with container:
        # ── Preparar datos ──
        df = data["tabla_rentabilidad"]
        df["Anio_label"] = df["Anio"].apply(_normalize_year_label)
        years = df["Anio_label"]
        roa = df["ROA"] * 100
        roe = df["ROE"] * 100
        ebitda = df["Margen_EBITDA"] * 100

        # Contexto ROE (respaldado por TP p.28-30)
        roe_ctx = [
            "2019: -0.48%, resultado neto negativo (TP p.28)",
            "2020: 12.45% (TP p.28)",
            "2021: 27.34%, pico por resultados de tenencia (TP p.28-29)",
            "2022: 22.52% (TP p.29)",
            "2023: 4.63% (TP p.29)",
            "2024: 26.99%, ganancias financieras por inflacion (TP p.29)",
            "2025*: 10.21% acumulado 9 meses (TP p.30)",
        ]
        # Contexto ROA (respaldado por TP p.24-27)
        roa_ctx = [
            "2019: -0.13%, reorganizacion industrial (TP p.24-25)",
            "2020: 3.61% (TP p.25)",
            "2021: 8.36%, pico por efectos de tenencia (TP p.25-26)",
            "2022: 7.82% (TP p.26)",
            "2023: 1.54% (TP p.26)",
            "2024: 10.01% inflado, EBIT/Activo real fue 6.78% (TP p.26)",
            "2025*: 3.71% acumulado 9 meses (TP p.27)",
        ]
        # Contexto EBITDA (respaldado por TP p.31-36)
        ebitda_ctx = [
            "2019: 8.20% (TP p.31, 119)",
            "2020: 13.12%, pico del periodo (TP p.31, 35)",
            "2021: 10.01% (TP p.31)",
            "2022: 9.44% (TP p.31)",
            "2023: 8.78% (TP p.31)",
            "2024: 8.08%, minimo del periodo (TP p.31)",
            "2025*: 8.73% acumulado 9 meses (TP p.36)",
        ]

        # ── LINEA 1: Grafico + KPIs ──
        col_chart, col_kpis = st.columns([2, 1])

        with col_chart:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=years, y=ebitda,
                name="Margen EBITDA",
                mode="lines+markers",
                line=dict(color=COLORS["green"], width=3, dash="dot"),
                marker=dict(size=8, color=COLORS["green"]),
                fill="tozeroy",
                customdata=ebitda_ctx,
                hovertemplate="EBITDA: %{y:.2f}%<br>%{customdata}<extra></extra>",
            ))
            fig.add_trace(go.Scatter(
                x=years, y=roe, mode="lines+markers",
                name="ROE",
                line=dict(color=COLORS["gold"], width=3),
                marker=dict(size=8, color=COLORS["gold"]),
                customdata=roe_ctx,
                hovertemplate="ROE: %{y:.2f}%<br>%{customdata}<extra></extra>",
            ))
            fig.add_trace(go.Scatter(
                x=years, y=roa, mode="lines+markers",
                name="ROA", line=dict(color=COLORS["navy"], width=3),
                marker=dict(size=8, color=COLORS["navy"]),
                customdata=roa_ctx,
                hovertemplate="ROA: %{y:.2f}%<br>%{customdata}<extra></extra>",
            ))

            fig = _apply_chart_layout(fig, title="ROA, ROE y Margen EBITDA (%)")
            fig.update_yaxes(title_text="Porcentaje", tickformat=".1f")
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)

        with col_kpis:
            ebitda_margins = df["Margen_EBITDA"] * 100
            last_ebitda = ebitda_margins.iloc[-1]
            min_ebitda = ebitda_margins.min()
            max_ebitda = ebitda_margins.max()

            st.markdown(
                _metric_card_html("Margen EBITDA 2025*", f"{last_ebitda:.2f}%"),
                unsafe_allow_html=True,
            )
            st.markdown(
                _metric_card_html("Minimo Historico", f"{min_ebitda:.2f}%"),
                unsafe_allow_html=True,
            )
            st.markdown(
                _metric_card_html("Maximo Historico", f"{max_ebitda:.2f}%"),
                unsafe_allow_html=True,
            )

        # ── LINEA 2: Texto + Formulas ──
        col_text, col_formulas = st.columns([2, 1])

        with col_text:
            st.markdown(
                "*A pesar de la volatilidad del ROA y ROE por efectos financieros "
                "extraordinarios, el Margen EBITDA demuestra una estabilidad "
                "operativa excepcional. La verdadera fortaleza de ARCOR esta en "
                "su operacion, no en los resultados financieros.* (TP)"
            )

        with col_formulas:
            st.markdown(
                _formula_card_html("ROA", "Resultado Neto / Activo Total"),
                unsafe_allow_html=True,
            )
            st.markdown(
                _formula_card_html("ROE", "Resultado Neto / Patrimonio Neto"),
                unsafe_allow_html=True,
            )
            st.markdown(
                _formula_card_html("EBITDA", "EBITDA / Ventas"),
                unsafe_allow_html=True,
            )# ── Slide 4: Liquidez ────────────────────────────────────────────────────────

def render_slide_4(data, container):
    with container:
        col_chart, col_metric = st.columns([2, 1])

        with col_chart:
            df = data["liquidez"].copy()
            df["Anio_label"] = df["Anio"].apply(_normalize_year_label)
            years = df["Anio_label"]

            # Contexto por punto (respaldado por TP p.36-40)
            liq_ctx = [
                "2019: 1.42x, dentro del rango adecuado (TP p.37)",
                "2020: 1.56x, pico por bajo nivel de pasivos corrientes",
                "2021: 1.55x, estable en rango adecuado (TP p.37)",
                "2022: 1.28x, caída por acumulación planificada de pasivos (TP p.38)",
                "2023: 1.40x, recuperación parcial",
                "2024: 1.24x, mínimo por pasivos financieros acumulados (TP p.38)",
                "2025*: 1.51x, recuperada con emisión de ONs Clases 5 y 6 (TP p.39)",
            ]
            pa_ctx = [
                "2019: 0.87x, aceptable",
                "2020: 0.94x, pico del período (TP p.40)",
                "2021: 0.90x, estable",
                "2022: 0.65x, mínimo: dependencia de vender stock (TP p.40)",
                "2023: 0.80x, recuperación parcial",
                "2024: 0.69x, caída por pasivos acumulados (TP p.40)",
                "2025*: 0.89x, recuperada por reclasificación deuda cte a no cte (TP p.39-40)",
            ]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=years, y=df["Liquidez"],
                name="Liquidez Corriente",
                marker_color=COLORS["navy"],
                customdata=liq_ctx,
                hovertemplate="Liquidez: %{y:.2f}x<br>%{customdata}<extra></extra>",
            ))
            fig.add_trace(go.Bar(
                x=years, y=df["Prueba_Acida"],
                name="Prueba Ácida",
                marker_color=COLORS["gold"],
                customdata=pa_ctx,
                hovertemplate="Prueba Ácida: %{y:.2f}x<br>%{customdata}<extra></extra>",
            ))
            fig.add_hline(y=1.50, line_color=COLORS["green"], line_dash="dash",
                          annotation_text="Mínimo recomendado (1.50x)")
            fig.add_hline(y=0.80, line_color=COLORS["red"], line_dash="dot",
                          annotation_text="Zona de riesgo (0.80x)")

            fig = _apply_chart_layout(
                fig,
                title="Liquidez Corriente vs Prueba Ácida",
            )
            fig.update_yaxes(title_text="Veces")
            fig.update_layout(barmode="group", bargap=0.25, height=250)
            st.plotly_chart(fig, use_container_width=True)

        with col_metric:
            last_liq = df["Liquidez"].iloc[-1]
            last_pa = df["Prueba_Acida"].iloc[-1]

            st.markdown(
                _metric_card_html("Liquidez Corriente 2025*", f"{last_liq:.2f}x"),
                unsafe_allow_html=True,
            )
            st.markdown(
                _metric_card_html("Prueba Ácida 2025*", f"{last_pa:.2f}x"),
                unsafe_allow_html=True,
            )

            st.markdown(
                _formula_card_html("Liquidez Corriente", "Act. Corriente / Pas. Corriente"),
                unsafe_allow_html=True,
            )
            st.markdown(
                _formula_card_html("Prueba Ácida", "(Act. Cte. - Inventarios) / Pas. Corriente"),
                unsafe_allow_html=True,
            )

        _explanation_row([
            ("Liquidez Corriente", "Por cada $1 que debe a corto plazo, tiene $1.51. Minimo sano: 1.5x"),
            ("Prueba Acida", "Igual pero sin inventario. Minimo: 0.8x"),
        ], help_text="La Prueba Acida excluye inventarios porque no se pueden convertir en efectivo rapido.")

    _render_footer(container)


# ── Slide 5: OCF + Capital de Trabajo ────────────────────────────────────────

def render_slide_5(data, container):
    with container:
        col_chart, col_metric = st.columns([2, 1])

        # OCF chart
        with col_chart:
            df_ocf = data["ocf"].copy()
            df_ocf["Anio_label"] = df_ocf["Anio"].apply(_normalize_year_label)
            
            df_ct = data["capital_trabajo"].copy()
            df_ct["Anio_label"] = df_ct["Anio"].apply(_normalize_year_label)

            # Contexto por punto (respaldado por TP p.45-48, 120)
            ocf_ctx = [
                "2019: 0.34x (TP p.45)",
                "2020: 0.43x, pico por bajo nivel de inversiones (TP p.46, 120)",
                "2021: 0.20x, caída por reinversión (TP p.46)",
                "2022: 0.25x (TP p.46)",
                "2023: 0.29x (TP p.46)",
                "2024: 0.15x, mínimo: utilidades contables no se convirtieron en caja (TP p.46-47, 120)",
                "2025*: 0.20x, recuperación parcial (TP p.48, 120)",
            ]
            ct_ctx = [
                "2019: $548.401M (TP p.41, 117)",
                "2020: $685.197M (TP p.41, 117)",
                "2021: $754.067M (TP p.41, 117)",
                "2022: $460.777M, caída (TP p.41, 117)",
                "2023: $758.012M, recuperación (TP p.41, 117)",
                "2024: $433.366M, mínimo del período (TP p.41, 117)",
                "2025*: $857.035M, récord por emisión de ONs Clases 5 y 6 (TP p.42-43, 117)",
            ]

            fig = go.Figure()

            # Capital de Trabajo (eje Y secundario)
            fig.add_trace(go.Scatter(
                x=df_ct["Anio_label"], y=df_ct["Capital_Trabajo"],
                mode="lines+markers",
                name="Capital de Trabajo ($M)",
                line=dict(color=COLORS["gold"], width=3),
                marker=dict(size=10, color=COLORS["gold"]),
                yaxis="y2",
                customdata=ct_ctx,
                hovertemplate="$%{y:,.0f}M<br>%{customdata}<extra></extra>",
            ))

            # OCF Ratio (eje Y principal)
            fig.add_trace(go.Scatter(
                x=df_ocf["Anio_label"], y=df_ocf["OCF_Ratio"],
                mode="lines+markers",
                name="OCF Ratio",
                line=dict(color=COLORS["navy"], width=4),
                marker=dict(size=12, color=COLORS["navy"],
                           line=dict(color="white", width=2)),
                fill="tozeroy",
                customdata=ocf_ctx,
                hovertemplate="%{y:.2f}x<br>%{customdata}<extra></extra>",
            ))

            fig.add_hline(y=0.20, line_color=COLORS["red"], line_dash="dash",
                          annotation_text="Referencia 2025*")
            
            fig = _apply_chart_layout(fig, title="OCF Ratio y Capital de Trabajo")
            fig.update_layout(
                height=250,
                yaxis=dict(title_text="OCF Ratio (veces)", side="left"),
                yaxis2=dict(
                    title_text="Capital de Trabajo ($M)",
                    side="right",
                    overlaying="y",
                    gridcolor="rgba(0,0,0,0)",
                ),
                legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.8)"),
            )
            st.plotly_chart(fig, use_container_width=True)

        # Capital de Trabajo metric
        with col_metric:
            cap_t = data["capital_trabajo"]
            last_ct = cap_t["Capital_Trabajo"].iloc[-1]
            prev_ct = cap_t["Capital_Trabajo"].iloc[-2]
            delta = f"+$ {last_ct - prev_ct:,.0f}M"

            st.metric(
                "Capital de Trabajo 2025*",
                f"$ {last_ct:,.0f}M",
                delta=delta,
            )

            st.markdown(
                _formula_card_html(
                    "OCF Ratio",
                    "Flujo Op. / Pas. Corriente",
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                _formula_card_html("Capital de Trabajo", "Act. Corriente - Pas. Corriente"),
                unsafe_allow_html=True,
            )

        _explanation_row([
            ("OCF Ratio", "Si las ganancias contables se convierten en efectivo. 0.15x en 2024 = alerta"),
            ("Capital de Trabajo", "Colchón de seguridad. Siempre positivo, récord $857.035M en 2025*"),
        ])

    _render_footer(container)


# ── Slide 6: Endeudamiento ───────────────────────────────────────────────────

def render_slide_6(data, container):
    with container:
        col_chart, col_metric = st.columns([2, 1])

        with col_chart:
            df = data["tabla_endeudamiento"].copy()
            df["Anio_label"] = df["Anio"].apply(_normalize_year_label)
            years = df["Anio_label"]

            # Contexto por punto (respaldado por TP p.51-55)
            end_ctx = [
                "2019: 2.71x, pico del período (TP p.51, 115)",
                "2020: 2.45x, inicio de tendencia decreciente (TP p.51)",
                "2021: 2.27x, reducción sostenida (TP p.51)",
                "2022: 1.88x, efecto inflación licuó pasivos comerciales (TP p.52-53)",
                "2023: 2.01x, aumento por devaluación dic-2023",
                "2024: 1.70x, mínimo: inflación licuó pasivos no indexados (TP p.52-53)",
                "2025*: 1.75x, leve aumento por nuevos pasivos (TP p.53)",
            ]
            sol_ctx = [
                "2019: 0.37x, mínimo del período (TP p.53, 114)",
                "2020: 0.41x (TP p.54)",
                "2021: 0.44x (TP p.54)",
                "2022: 0.53x, mejora por inflación sobre pasivos (TP p.55)",
                "2023: 0.50x (TP p.55)",
                "2024: 0.59x, pico: paradoja inflacionaria (TP p.54-55)",
                "2025*: 0.57x, sólido (TP p.55)",
            ]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=years,
                y=df["Endeudamiento"],
                name="Nivel de Endeudamiento",
                marker_color=COLORS["navy"],
                marker_line_color=COLORS["navy"],
                marker_line_width=1.5,
                customdata=end_ctx,
                hovertemplate="Endeudamiento: %{y:.2f}x<br>%{customdata}<extra></extra>",
            ))
            fig.add_trace(go.Scatter(
                x=years,
                y=df["Solvencia"],
                name="Solvencia",
                mode="lines+markers",
                line=dict(color=COLORS["gold"], width=4),
                marker=dict(size=12, color=COLORS["gold"],
                           line=dict(color="white", width=2)),
                customdata=sol_ctx,
                hovertemplate="Solvencia: %{y:.2f}x<br>%{customdata}<extra></extra>",
            ))

            fig = _apply_chart_layout(fig, title="Endeudamiento y Solvencia")
            fig.update_yaxes(title_text="Veces")
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)

        with col_metric:
            last_end = df["Endeudamiento"].iloc[-1]
            last_sol = df["Solvencia"].iloc[-1]

            st.markdown(
                _metric_card_html("Endeudamiento 2025*", f"{last_end:.2f}x"),
                unsafe_allow_html=True,
            )
            st.markdown(
                _metric_card_html("Solvencia 2025*", f"{last_sol:.2f}x", color=COLORS["green"]),
                unsafe_allow_html=True,
            )

            st.markdown(
                _formula_card_html("Endeudamiento", "Pasivo Total / Patrimonio Neto"),
                unsafe_allow_html=True,
            )
            st.markdown(
                _formula_card_html("Solvencia", "Patrimonio Neto / Pasivo Total"),
                unsafe_allow_html=True,
            )

        _explanation_row([
            ("Endeudamiento", "$1.75 de deuda por cada $1 de patrimonio. Menos de 2x es saludable"),
            ("Solvencia", "57% del activo financiado por patrimonio propio"),
        ], help_text="La inflacion 2024 licuo pasivos comerciales no indexados. Parte de la mejora es coyuntural (TP p.52-53).")

    _render_footer(container)


# ── Slide 7: Apalancamiento ──────────────────────────────────────────────────

def render_slide_7(data, container):
    with container:
        col1, col2 = st.columns([2, 1])

        with col1:
            df_lev = data["leverage"].copy()
            df_lev["Anio_label"] = df_lev["Anio"].apply(_normalize_year_label)
            
            df_de = data["tabla_endeudamiento"].copy()
            df_de["Anio_label"] = df_de["Anio"].apply(_normalize_year_label)

            # Contexto por punto (respaldado por TP p.55-58, 115)
            de_ctx = [
                "2019: 4.91x, pico del período (TP p.60, 116)",
                "2020: 2.75x, mejora significativa (TP p.60)",
                "2021: 2.83x (TP p.60)",
                "2022: 2.18x, mínimo del período (TP p.60)",
                "2023: 3.09x, aumento por devaluación (TP p.60)",
                "2024: 2.90x (TP p.60)",
                "2025*: 2.79x, nivel seguro (<3x) (TP p.60)",
            ]
            lev_ctx = [
                "2019: -0.02x, retorno activos inferior al costo deuda (TP p.56, 115)",
                "2020: 0.70x (TP p.56)",
                "2021: 5.40x (TP p.56)",
                "2022: 97.31x, apreciación real TC: inflación > devaluación (TP p.56-57, 115)",
                "2023: -0.24x, devaluación brusca dic-2023 (TP p.57, 115)",
                "2024: 2.58x, recuperación (TP p.58)",
                "2025*: 0.61x, normalización (TP p.58)",
            ]

            fig = go.Figure()

            # Deuda/EBITDA (eje Y secundario)
            fig.add_trace(go.Scatter(
                x=df_de["Anio_label"], y=df_de["Deuda_EBITDA"],
                mode="lines+markers",
                name="Deuda/EBITDA",
                line=dict(color=COLORS["navy"], width=4),
                marker=dict(size=12, color=COLORS["navy"],
                           line=dict(color="white", width=2)),
                yaxis="y2",
                customdata=de_ctx,
                hovertemplate="%{y:.2f}x<br>%{customdata}<extra></extra>",
            ))

            # Leverage (eje Y principal)
            fig.add_trace(go.Scatter(
                x=df_lev["Anio_label"], y=df_lev["Leverage"],
                mode="lines+markers",
                name="Leverage (Apalancamiento)",
                line=dict(color=COLORS["gold"], width=4),
                marker=dict(size=12, color=COLORS["gold"],
                           line=dict(color="white", width=2)),
                customdata=lev_ctx,
                hovertemplate="%{y:.2f}x<br>%{customdata}<extra></extra>",
            ))

            fig = _apply_chart_layout(fig, title="Apalancamiento y Deuda/EBITDA")
            fig.update_layout(
                height=250,
                yaxis=dict(title_text="Leverage (ROA / Costo Fin.)", side="left"),
                yaxis2=dict(
                    title_text="Deuda/EBITDA",
                    side="right",
                    overlaying="y",
                    gridcolor="rgba(0,0,0,0)",
                ),
                legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.8)"),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            last_lev = df_lev["Leverage"].iloc[-1]
            last_de = df_de["Deuda_EBITDA"].iloc[-1]
            min_de = df_de["Deuda_EBITDA"].min()

            st.markdown(
                _metric_card_html(
                    "Leverage 2025*",
                    f"{last_lev:.2f}x",
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                _metric_card_html(
                    "Deuda/EBITDA 2025*",
                    f"{last_de:.2f}x",
                    color=COLORS["green"],
                ),
                unsafe_allow_html=True,
            )

            st.markdown(
                _formula_card_html(
                    "Leverage",
                    "ROA / Costo Financiero del Pasivo",
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                _formula_card_html("Deuda/EBITDA", "Deuda Financiera / EBITDA"),
                unsafe_allow_html=True,
            )

        _explanation_row([
            ("Leverage", "ROA / costo deuda. Volatil por TC e inflacion (97.31x en 2022 no es error)"),
            ("Deuda/EBITDA", "Anios de EBITDA para pagar deuda. <3x es seguro. ARCOR: 2.79x"),
        ])

    _render_footer(container)


# ── Slide 8: Variaciones Patrimoniales ───────────────────────────────────────

def render_slide_8(data, container):
    with container:
        tab1, tab2, tab3 = st.tabs([
            "Var Ventas y Utilidad Bruta",
            "Flujo de Efectivo",
            "ARCOR vs INDEC",
        ])

        # ── Tab 1: Var Ventas + Var UB ──
        with tab1:
            col_chart, col_metric = st.columns([2, 1])

            with col_chart:
                df = data["var_ventas"].copy()
                df["Anio_label"] = df["Anio"].apply(_normalize_year_label)
                # Excluir 2019 (no hay datos de variación)
                df = df[df["Anio_label"] != "2019"].copy()

                # Contexto por punto (respaldado por TP p.61-66, 112-113)
                vv_ctx = [
                    "2020: -3.48%, restricciones pandemia (TP p.62, 81, 112)",
                    "2021: +12.73%, recuperación por consumo refugio y exportaciones (TP p.62-63, 81)",
                    "2022: +6.54%, terreno positivo (TP p.63, 81)",
                    "2023: -1.61%, inicio recesión (TP p.64, 81)",
                    "2024: -5.54%, recesión severa (TP p.64, 81)",
                    "2025*: -7.80% acumulado 9 meses (TP p.65)",
                ]
                ub_ctx = [
                    "2020: +9.61%, pese a caída ventas, ajuste costos, margen bruto 32.88% (TP p.66-67, 81)",
                    "2021: +0.24% (TP p.66)",
                    "2022: +6.99% (TP p.66)",
                    "2023: -5.70% (TP p.66)",
                    "2024: -2.78%, mitiga caída ventas -5.54% por integración vertical (TP p.65-66, 81)",
                ]

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=df["Anio_label"], y=df["Var_Ventas"] * 100,
                    name="Var % Ventas Reales",
                    marker_color=COLORS["navy"],
                    marker_line_color=COLORS["navy"],
                    marker_line_width=1.5,
                    customdata=vv_ctx,
                    hovertemplate="%{y:.2f}%<br>%{customdata}<extra></extra>",
                ))
                fig.add_trace(go.Scatter(
                    x=df["Anio_label"], y=df["Var_UB"] * 100,
                    name="Var % Utilidad Bruta",
                    mode="lines+markers",
                    line=dict(color=COLORS["gold"], width=4),
                    marker=dict(size=12, color=COLORS["gold"],
                               line=dict(color="white", width=2)),
                    customdata=ub_ctx,
                    hovertemplate="%{y:.2f}%<br>%{customdata}<extra></extra>",
                ))
                fig.add_hline(y=0, line_color="#cbd5e1", line_dash="dash")
                fig = _apply_chart_layout(fig, title="Variación % de Ventas Reales y Utilidad Bruta")
                fig.update_yaxes(title_text="Variación %")
                fig.update_layout(height=250)
                st.plotly_chart(fig, use_container_width=True)

            with col_metric:
                last_vv = df["Var_Ventas"].iloc[-1] * 100
                last_ub = df["Var_UB"].dropna().iloc[-1] * 100

                st.markdown(
                    _metric_card_html(
                        "Var % Ventas 2025*",
                        f"{last_vv:.2f}%",
                        color=COLORS["red"],
                    ),
                    unsafe_allow_html=True,
                )
                st.markdown(
                    _metric_card_html(
                        "Var % UB 2024",
                        f"{last_ub:.2f}%",
                        color=COLORS["red"],
                    ),
                    unsafe_allow_html=True,
                )

                st.markdown(
                    _formula_card_html(
                        "Var % Ventas",
                        "(Ventast / Ventast-1) - 1",
                    ),
                    unsafe_allow_html=True,
                )
                st.markdown(
                    _formula_card_html(
                        "Var % UB",
                        "(UBt / UBt-1) - 1",
                    ),
                    unsafe_allow_html=True,
                )

                st.caption(
                    "2020: shock pandemia (-3,48%). "
                    "2021: recuperacion (+12,73%). "
                    "2023-2025*: erosion recesion en ventas."
                )

        # ── Tab 3: ARCOR vs INDEC ──
        with tab3:
            col_chart, col_metric = st.columns([2, 1])

            with col_chart:
                df = data["arcor_indec"].copy()
                df["Anio_label"] = df["Anio"].apply(_normalize_year_label)

                # Excluir 2025 porque INDEC no está disponible
                df_plot = df[~df["Anio_label"].str.contains(r"\*", na=False)].copy()

                # Contexto por punto (respaldado por TP p.76-79, 119)
                arcor_ctx = [
                    "2019: dato base",
                    "2020: -3.48%, golosinas son productos discrecionales (TP p.76)",
                    "2021: +12.73%, recuperación fuerte (TP p.62-63)",
                    "2022: +6.54% (TP p.63)",
                    "2023: -1.61% (TP p.64)",
                    "2024: -5.54%, consumidores priorizan marcas líderes (TP p.78-79)",
                ]
                indec_ctx = [
                    "2019: -9.80% (TP p.76, 119)",
                    "2020: +0.80%, consumo concentrado en básicos (TP p.76)",
                    "2021: +1.50% (TP p.76, 119)",
                    "2022: +1.60% (TP p.76, 119)",
                    "2023: +0.90% (TP p.76, 119)",
                    "2024: -11.00%, caída del mercado general (TP p.78-79)",
                ]

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=df_plot["Anio_label"],
                    y=df_plot["ARCOR"] * 100,
                    name="ARCOR Var % Ventas",
                    marker_color=COLORS["navy"],
                    marker_line_color=COLORS["navy"],
                    marker_line_width=1.5,
                    customdata=arcor_ctx,
                    hovertemplate="ARCOR: %{y:.2f}%<br>%{customdata}<extra></extra>",
                ))
                fig.add_trace(go.Bar(
                    x=df_plot["Anio_label"],
                    y=df_plot["INDEC"] * 100,
                    name="INDEC Supermercados",
                    marker_color=COLORS["gold"],
                    marker_line_color=COLORS["gold"],
                    marker_line_width=1.5,
                    customdata=indec_ctx,
                    hovertemplate="INDEC: %{y:.2f}%<br>%{customdata}<extra></extra>",
                ))
                fig.add_hline(y=0, line_color="#cbd5e1", line_dash="dash")
                fig = _apply_chart_layout(
                    fig,
                    title="ARCOR vs INDEC — Variación % Ventas (2019-2024)",
                )
                fig.update_yaxes(title_text="Variación %")
                fig.update_layout(barmode="group", bargap=0.3, height=250)
                st.plotly_chart(fig, use_container_width=True)

            with col_metric:
                # Calcular diferenciales clave
                df_2020 = df_plot[df_plot["Anio_label"] == "2020"]
                df_2024 = df_plot[df_plot["Anio_label"] == "2024"]
                
                if not df_2020.empty and not df_2024.empty:
                    diff_2020 = (df_2020["ARCOR"].iloc[0] - df_2020["INDEC"].iloc[0]) * 100
                    diff_2024 = (df_2024["ARCOR"].iloc[0] - df_2024["INDEC"].iloc[0]) * 100
                else:
                    diff_2020 = 0
                    diff_2024 = 0

                st.markdown(
                    _metric_card_html(
                        "Diferencial 2020 (Pandemia)",
                        f"{diff_2020:.2f}%",
                        color=COLORS["red"],
                    ),
                    unsafe_allow_html=True,
                )
                st.markdown(
                    _metric_card_html(
                        "Diferencial 2024 (Recesión)",
                        f"+{diff_2024:.2f}%",
                        color=COLORS["green"],
                    ),
                    unsafe_allow_html=True,
                )

                st.markdown(
                    _formula_card_html("Diferencial", "Var% ARCOR - Var% INDEC"),
                    unsafe_allow_html=True,
                )

                _explanation_row([
                    ("2020 Pandemia", "ARCOR -4.28% vs mercado. Golosinas son discrecionales (TP p.76)"),
                    ("2024 Recesion", "ARCOR +5.46% vs mercado. Consumidores priorizan marcas lideres (TP p.78-79)"),
                ])

        # ── Tab 2: Flujo de Efectivo ──
        with tab2:
            cf = data["cashflow"].copy()
            cf["Anio_label"] = cf["Anio"].apply(_normalize_year_label)

            rows_data = [
                ("Act. Operativa", "Act_Operativa"),
                ("Act. Inversión", "Act_Inversion"),
                ("Act. Financiación", "Act_Financiacion"),
                ("Variación Total", "Var_Efectivo"),
            ]

            html = """<div style="overflow-x:auto;">
            <table style="width:100%; border-collapse:collapse; font-size:0.85rem;">
                <thead><tr style="background:#1e3a5f; color:white;">
                    <th style="padding:8px; text-align:left;">Actividad</th>"""
            for label in cf["Anio_label"]:
                html += f'<th style="padding:8px; text-align:center;">{label}</th>'
            html += "</tr></thead><tbody>"

            for row_name, col_key in rows_data:
                html += f'<tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px; font-weight:600;">{row_name}</td>'
                for _, r in cf.iterrows():
                    val = r[col_key]
                    color = "#22c55e" if val >= 0 else "#ef4444"
                    html += f'<td style="padding:8px; text-align:center; color:{color}; font-weight:600;">${val:,.0f}M</td>'
                html += "</tr>"

            html += "</tbody></table></div>"
            st.markdown(html, unsafe_allow_html=True)

            insight = []
            last = cf["Var_Efectivo"].iloc[-1]
            insight.append(f"**2025\\*:** Variación total **${last:,.0f}M**")
            worst_idx = cf["Var_Efectivo"].idxmin()
            insight.append(f"**Peor año:** {cf.loc[worst_idx, 'Anio_label']} ({cf.loc[worst_idx, 'Var_Efectivo']:,.0f}M)")
            best_idx = cf["Var_Efectivo"].idxmax()
            insight.append(f"**Mejor año:** {cf.loc[best_idx, 'Anio_label']} ({cf.loc[best_idx, 'Var_Efectivo']:,.0f}M)")
            st.info(" | ".join(insight))

    _render_footer(container)


# ── Slide 9: Dictamen ────────────────────────────────────────────────────────

def render_slide_9(data, container):
    with container:
        col_hits, col_seal = st.columns([1, 1])

        with col_hits:
            st.subheader("Síntesis del Análisis")
            st.markdown("""
- **Margen EBITDA estable 8%–13%** — pilar operativo inquebrantable
- **Endeudamiento en descenso** — de 2,71x a 1,75x (-35%)
- **Deuda/EBITDA 2,79x** — nivel seguro
- **Liquidez recuperada** — 1,51x con Capital de Trabajo récord
- **Fix SCR AAA(arg)** — respaldo de calificadora
            """)

        with col_seal:
            st.markdown(
                f"<div style='text-align:center; background:#f8fafc; "
                f"padding:1rem; border-radius:8px; "
                f"border:3px solid {COLORS['gold']}; margin:0.5rem 0;'>"
                f"<h2 style='color:{COLORS['gold']}; margin:0; font-size:1.3rem;'>"
                f"RECOMENDACIÓN FAVORABLE<br>BAJO RIESGO CREDITICIO</h2>"
                f"<p style='color:#475569; font-size:0.8rem; margin:0.3rem 0;'>"
                f"Obligaciones Negociables Clases 5 y 6</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

            c1, c2 = st.columns(2)
            with c1:
                st.caption("**Fix SCR** — AAA(arg)")
            with c2:
                st.caption("**Moody's** — EBITDA 8-10%")

    _render_footer(container)


# ── Slide 10: Rotación y Eficiencia Operativa ──────────────────────────────

def render_slide_10(data, container):
    with container:
        col_chart, col_metric = st.columns([2, 1])

        with col_chart:
            df_ra = data["rotacion"].copy()
            df_ra["Anio_label"] = df_ra["Anio"].apply(_normalize_year_label)

            # Contexto por punto (respaldado por TP p.69-71, 117-118)
            rp_ctx = [
                "2019: 1.66x (TP p.69, 113)",
                "2020: 1.65x (TP p.69)",
                "2021: 1.82x (TP p.69)",
                "2022: 2.11x, pico del período (TP p.70-71, 113)",
                "2023: 1.69x (TP p.69)",
                "2024: 2.03x (TP p.69)",
                "2025*: 2.11x, facturación cubre 2.11x las obligaciones totales (TP p.69)",
            ]
            ra_ctx = [
                "2019: 1.21x (TP p.69, 117)",
                "2020: 1.17x (TP p.69)",
                "2021: 1.26x (TP p.69)",
                "2022: 1.38x, pico del período (TP p.69)",
                "2023: 1.13x, mínimo: impacto recesión (TP p.69)",
                "2024: 1.28x (TP p.69)",
                "2025*: 1.34x, eficiencia recuperada (TP p.69)",
            ]

            fig = go.Figure()

            # Rotación de Pasivos (eje Y secundario)
            fig.add_trace(go.Scatter(
                x=df_ra["Anio_label"], y=df_ra["Rot_Pasivos"],
                mode="lines+markers",
                name="Rotación de Pasivos",
                line=dict(color=COLORS["navy"], width=4),
                marker=dict(size=12, color=COLORS["navy"],
                           line=dict(color="white", width=2)),
                yaxis="y2",
                customdata=rp_ctx,
                hovertemplate="%{y:.2f}x<br>%{customdata}<extra></extra>",
            ))

            # Rotación de Activos (eje Y principal)
            fig.add_trace(go.Scatter(
                x=df_ra["Anio_label"], y=df_ra["Rot_Activos"],
                mode="lines+markers",
                name="Rotación de Activos",
                line=dict(color=COLORS["gold"], width=4),
                marker=dict(size=12, color=COLORS["gold"],
                           line=dict(color="white", width=2)),
                customdata=ra_ctx,
                hovertemplate="%{y:.2f}x<br>%{customdata}<extra></extra>",
            ))

            fig = _apply_chart_layout(fig, title="Rotación de Activos y Pasivos")
            fig.update_layout(
                height=250,
                yaxis=dict(title_text="Rot. Activos (veces)", side="left"),
                yaxis2=dict(
                    title_text="Rot. Pasivos (veces)",
                    side="right",
                    overlaying="y",
                    gridcolor="rgba(0,0,0,0)",
                ),
                legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.8)"),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_metric:
            last_ra = df_ra["Rot_Activos"].iloc[-1]
            last_rp = df_ra["Rot_Pasivos"].iloc[-1]

            st.markdown(
                _metric_card_html(
                    "Rot. Activos 2025*",
                    f"{last_ra:.2f}x",
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                _metric_card_html(
                    "Rot. Pasivos 2025*",
                    f"{last_rp:.2f}x",
                    color=COLORS["green"],
                ),
                unsafe_allow_html=True,
            )

            st.markdown(
                _formula_card_html(
                    "Rot. Activos",
                    "Ventas / Activo Total",
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                _formula_card_html("Rot. Pasivos", "Ventas / Pasivo Total"),
                unsafe_allow_html=True,
            )

        _explanation_row([
            ("Rot. Activos", "1.34x = cada $1 en activos genera $1.34 en ventas. Estable 1.13-1.38x"),
            ("Rot. Pasivos", "2.11x = facturacion cubre 2x las deudas. Indica eficiencia operativa"),
        ])

    _render_footer(container)
