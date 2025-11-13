import streamlit as st
from datetime import datetime
from calculator import calcular_tabletas, calcular_ampollas
from PIL import Image
import pytz
import os
import base64
# ======================================
# CONFIGURACIÓN GENERAL
# ======================================
st.set_page_config(
    page_title="Calculadora de Medicamentos 💊",
    layout="wide",
    page_icon="💉💊"
)
# ======================================
# ESTILO HOSPITALARIO AZUL + AVISO DESTACADO
# ======================================
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 0rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1300px;
        }
        h1 {
            color: #005b96;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }
        h2, h3 {
            color: #0074cc;
            margin-bottom: 0.4rem;
        }
        button[kind="primary"] {
            background-color: #0074cc !important;
            color: white !important;
            border-radius: 8px;
            border: none;
            padding: 0.35rem 0.8rem !important;
            font-size: 0.9rem !important;
            font-weight: 600 !important;
        }
        button[kind="primary"]:hover {
            background-color: #000000 !important;
        }
        [data-testid="stMetric"] {
            background-color: #e7f1fb;
            border-radius: 10px;
            padding: 0.4rem;
            border: 1px solid #b6d4f0;
        }
        div[data-testid="stMetricValue"] {
            color: #005b96;
            font-size: 1.3rem;
            font-weight: 700;
        }
        .logo-title-container {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .app-header img {
            height: 80px;
            width: auto;
            border-radius: 10px;
        }
        .app-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-bottom: 25px;
            background-color: #ffffff;
            padding: 15px 25px;
            border-radius: 15px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        .app-header h1 {
            font-size: 2.2em;
            font-weight: 700;
            color: #1E3A8A;
            margin: 0;
        }
    </style>
""", unsafe_allow_html=True)

# ======================================
# ENCABEZADO CON LOGO Y TÍTULO CENTRADO
# ======================================
logo_path = "logo/logo1.png"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode("utf-8")
    st.markdown(
        f"""
        <div class="app-header">
            <img src="data:image/png;base64,{logo_base64}" alt="Logo">
        </div>
        """,
        unsafe_allow_html=True
)
else:
    st.title("🖩 calculadora")
# ======================================
# LAYOUT PRINCIPAL
# ======================================
col_form, col_result = st.columns([1.1, 1])

# ======================================
# COLUMNA IZQUIERDA — FORMULARIO
# ======================================
with col_form:
    st.subheader("🔢 📌calculadora ")

    tipo = st.selectbox("Tipo:", ["Tableta 💊", "Ampolla 💉"])
    frecuencia = st.number_input("Frecuencia (horas):", min_value=1, max_value=24, value=8)
    duracion = st.number_input("Duración (días):", min_value=1, max_value=120, value=1)

    # ✅ Fecha local ajustada a zona horaria de Colombia
    zona_colombia = pytz.timezone("America/Bogota")
    fecha_local = datetime.now(zona_colombia).date()
    fecha_orden = st.date_input("Fecha de orden:", fecha_local)

    inicio_mismo_dia = st.checkbox("Inicia el mismo día", value=True)
    st.caption("Si no marca Check, inicia el día siguiente.")

    st.divider()

    if tipo == "Tableta 💊":
        dosis_toma = st.number_input("Dosis por toma (tabletas):", min_value=0.25, step=0.25, value=1.0)
        unidades_presentacion = st.number_input("Unidades por caja:", min_value=1, step=1, value=30)
        calcular = st.button("🧮 Calcular Tabletas", use_container_width=True)
    else:
        dosis_inyeccion = st.number_input("Dosis por inyección (ml):", min_value=0.1, step=0.1, value=1.0)
        volumen_ampolla = st.number_input("Presentacion por ampolla (ml):", min_value=0.5, step=0.5, value=1.0)
        calcular = st.button("🧮 Calcular Ampollas", use_container_width=True)

# ======================================
# COLUMNA DERECHA — RESULTADOS
# ======================================
with col_result:
    st.subheader("📊 Resultados")

    if tipo == "Tableta 💊" and 'calcular' in locals() and calcular:
        resultados = calcular_tabletas(frecuencia, duracion, dosis_toma, unidades_presentacion, fecha_orden, inicio_mismo_dia)

        st.success(f"**Tratamiento:** {resultados['Fecha de inicio']} → {resultados['Fecha de finalización']}")
        colA, colB, colC = st.columns(3)
        colA.metric("Tomas", resultados["Total de tomas"])
        colB.metric("Tabletas", resultados["Total de tabletas"])
        colC.metric("Presentaciones", resultados["Presentaciones necesarias"])

        st.caption("📆 Distribución mensual:")

        fecha_inicio = datetime.strptime(resultados["Fecha de inicio"], "%Y-%m-%d").date()
        if fecha_inicio.month != fecha_orden.month:
            st.warning(f"📌 Nota: La orden inicia en el mes siguiente ({fecha_inicio.strftime('%B')}). Todas las tabletas se asignan a ese mes.")

        st.markdown(f"""
            <div style='background-color:#fff3cd; border-left:6px solid #ffcc00; padding:0.8rem; border-radius:8px; margin-bottom:0.5rem;'>
                <strong>📌 Este mes:</strong> {resultados['Tabletas este mes']} tabletas
            </div>
            <div style='background-color:#fff3cd; border-left:6px solid #ffcc00; padding:0.8rem; border-radius:8px;'>
                <strong>📌 Próximo mes:</strong> {resultados['Tabletas próximo mes']} tabletas
            </div>
        """, unsafe_allow_html=True)

    elif tipo == "Ampolla 💉" and 'calcular' in locals() and calcular:
        resultados = calcular_ampollas(frecuencia, duracion, dosis_inyeccion, volumen_ampolla, fecha_orden, inicio_mismo_dia)

        st.success(f"**Tratamiento:** {resultados['Fecha de inicio']} → {resultados['Fecha de finalización']}")
        colA, colB, colC = st.columns(3)
        colA.metric("Inyecciones ", resultados["Total de inyecciones"])
        colB.metric("Ampollas utilizadas", resultados["Ampollas necesarias"])

        st.caption("📆 Distribución mensual:")

        fecha_inicio = datetime.strptime(resultados["Fecha de inicio"], "%Y-%m-%d").date()
        if fecha_inicio.month != fecha_orden.month:
            st.warning(f"📌 Nota: La orden inicia en el mes siguiente ({fecha_inicio.strftime('%B')}). Todas las ampollas se asignan a ese mes.")

        st.markdown(f"""
            <div style='background-color:#fff3cd; border-left:6px solid #ffcc00; padding:0.8rem; border-radius:8px; margin-bottom:0.5rem;'>
                <strong>📌 Este mes:</strong> {resultados['Ampollas este mes']} ampollas  
            </div>
            <div style='background-color:#fff3cd; border-left:6px solid #ffcc00; padding:0.8rem; border-radius:8px;'>
                <strong>📌 Próximo mes:</strong> {resultados['Ampollas próximo mes']} ampollas  
            </div>
        """, unsafe_allow_html=True)


# ======================================
# AVISO DE CONFIDENCIALIDAD AL FINAL
# ======================================
st.markdown("""
    <style>
        .aviso-container {
            margin-top: 3rem;
            padding: 1.5rem 2rem;
            background-color: #ffffff;
            border-top: 3px solid #d1d5db;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        }
        .mejora {
            color: #0074cc;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .confidencial {
            color: #c00000;
            font-weight: 700;
            margin-top: 10px;
            margin-bottom: 5px;
        }
        .texto {
            color: #c00000;
            margin: 0;
            font-size: 0.88rem;
            line-height: 1.3rem;
        }
    </style>

    <div class="aviso-container">
        <p class="mejora">ℹ️ Esta calculadora susceptible a mejoramiento, si usted encuentra alguna inconsitencia en el calculo  por favor notifíquelo al área responsable del diseño.</p>
        <p class="confidencial">⚠️ Aviso de uso confidencial:</p>
        <p class="texto">Está destinado exclusivamente para uso institucional y bajo las políticas de privacidad y seguridad de la compañia . Cualquier divulgación, copia o uso no autorizado está estrictamente prohibido.</p>
    </div>
""", unsafe_allow_html=True)













