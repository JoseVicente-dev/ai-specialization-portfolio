# ============================================================
# app.py
# Dashboard interactivo con graficos y chat con el agente
#
# Ejecucion: streamlit run app.py
# ============================================================

import os
import sys
import json
import pandas as pd
import plotly.express as px
import streamlit as st

# ------------------------------------------------------------
# CONFIGURACION DE LA PAGINA
# ------------------------------------------------------------
# Esta instruccion debe ser la primera llamada a Streamlit en el archivo

st.set_page_config(
    page_title="Analisis de Vuelos EE.UU.",
    page_icon="✈",
    layout="wide",
    # layout="wide" usa todo el ancho de la pantalla
)

# ------------------------------------------------------------
# CARGAR LOS DATOS
# ------------------------------------------------------------
# @st.cache_data guarda el resultado en memoria
# La proxima vez que el usuario recarga la pagina, no relee los archivos

@st.cache_data
def cargar_todos_los_datos():
    datos = {}

    archivos = {
        "aerolineas": "data/agg_aerolineas.csv",
        "rutas":      "data/agg_rutas.csv",
        "horario":    "data/agg_horario.csv",
        "mensual":    "data/agg_mensual.csv",
        "estado":     "data/agg_estado.csv",
    }

    for nombre, ruta in archivos.items():
        if os.path.exists(ruta):
            datos[nombre] = pd.read_csv(ruta)
        else:
            datos[nombre] = pd.DataFrame()
            # Si el archivo no existe, guardamos una tabla vacia

    return datos


datos = cargar_todos_los_datos()

# ------------------------------------------------------------
# VERIFICAR QUE LOS DATOS EXISTEN
# ------------------------------------------------------------

if datos["aerolineas"].empty:
    # .empty → True si la tabla no tiene filas
    st.error(
        "No se encontraron los datos. Ejecuta primero:\n\n"
        "```\npython procesar.py\n```"
    )
    st.stop()
    # st.stop() detiene la ejecucion de la app aqui

# ------------------------------------------------------------
# MENU LATERAL
# ------------------------------------------------------------

with st.sidebar:
    st.title("Vuelos EE.UU.")
    st.caption("PySpark + GPT-4 Analytics")
    st.divider()

    seccion = st.radio(
        "Seccion",
        ["Dashboard", "Chat con IA"],
    )
    # st.radio crea botones de seleccion unica

    st.divider()

    # Boton para ver el reporte generado por GPT-4
    st.subheader("Reporte IA")
    if os.path.exists("data/reporte_final.md"):
        with open("data/reporte_final.md", encoding="utf-8") as f:
            contenido_reporte = f.read()
        with st.expander("Ver reporte analitico"):
            st.markdown(contenido_reporte)
            # st.markdown renderiza el Markdown como HTML formateado
    else:
        st.info(
            "Ejecuta `python reporte.py` para generar el reporte automatico con GPT-4."
        )

    st.divider()
    total_vuelos_sidebar = int(datos["aerolineas"]["total_vuelos"].sum())
    st.caption("Dataset: " + f"{total_vuelos_sidebar:,}" + " vuelos")


# ============================================================
# SECCION 1: DASHBOARD
# ============================================================

if seccion == "Dashboard":

    st.title("Dashboard — Retrasos de Vuelos EE.UU.")

    ae = datos["aerolineas"]
    rt = datos["rutas"]
    hr = datos["horario"]
    mn = datos["mensual"]

    # --------------------------------------------------------
    # INDICADORES PRINCIPALES (KPIs)
    # --------------------------------------------------------

    st.subheader("Resumen Global")

    col1, col2, col3, col4 = st.columns(4)
    # st.columns(4) crea 4 columnas de igual ancho

    with col1:
        total_vuelos = int(ae["total_vuelos"].sum())
        st.metric("Total Vuelos", f"{total_vuelos:,}")
        # f"{valor:,}" agrega separador de miles: 5000000 → 5,000,000

    with col2:
        total_cancelados = int(ae["vuelos_cancelados"].sum()) if "vuelos_cancelados" in ae.columns else 0
        pct_canc = round(total_cancelados / total_vuelos * 100, 1) if total_vuelos > 0 else 0
        st.metric("Tasa Cancelacion", f"{pct_canc}%")

    with col3:
        retraso_global = round(float(ae["retraso_salida_promedio"].mean()), 1)
        st.metric("Retraso Prom. Salida", f"{retraso_global} min")

    with col4:
        puntualidad_global = round(float(ae["pct_puntual"].mean()), 1)
        st.metric("% Vuelos Puntuales", f"{puntualidad_global}%")

    st.divider()

    # --------------------------------------------------------
    # FILA 1: PUNTUALIDAD Y CUOTA DE MERCADO
    # --------------------------------------------------------

    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("Puntualidad por Aerolinea")

        ae_ordenada = ae.sort_values("pct_puntual", ascending=True)

        fig_puntualidad = px.bar(
            ae_ordenada,
            x="pct_puntual",
            y="aerolinea",
            orientation="h",
            # orientation="h" crea barras horizontales
            color="pct_puntual",
            color_continuous_scale="RdYlGn",
            # RdYlGn: Rojo (bajo) → Amarillo (medio) → Verde (alto)
            text="pct_puntual",
            labels={"pct_puntual": "% Puntualidad", "aerolinea": ""},
        )
        fig_puntualidad.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_puntualidad.update_layout(height=350, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_puntualidad, use_container_width=True)
        # use_container_width=True hace que el grafico ocupe todo el ancho

    with col_der:
        st.subheader("Cuota de Mercado (por vuelos)")

        fig_torta = px.pie(
            ae,
            values="total_vuelos",
            names="aerolinea",
            hole=0.4,
            # hole=0.4 crea un agujero en el centro (grafico dona)
        )
        fig_torta.update_layout(height=350)
        st.plotly_chart(fig_torta, use_container_width=True)

    st.divider()

    # --------------------------------------------------------
    # FILA 2: PATRON HORARIO Y EVOLUCION MENSUAL
    # --------------------------------------------------------

    col_izq2, col_der2 = st.columns(2)

    with col_izq2:
        st.subheader("Retraso Promedio por Hora de Salida")

        hr_ordenado = hr.sort_values("hora")

        fig_horario = px.line(
            hr_ordenado,
            x="hora",
            y="retraso_promedio",
            color="franja_dia",
            # color diferencia las franjas del dia con distintos colores
            markers=True,
            # markers=True agrega un punto en cada hora
            labels={
                "hora": "Hora de salida",
                "retraso_promedio": "Retraso prom. (min)",
                "franja_dia": "Franja"
            },
        )
        fig_horario.update_layout(height=350)
        st.plotly_chart(fig_horario, use_container_width=True)

    with col_der2:
        st.subheader("Evolucion Mensual de Vuelos")

        mn_ordenado = mn.sort_values("mes").copy()

        # Creamos una columna con el nombre del mes para el eje X
        if "nombre_mes" in mn_ordenado.columns:
            eje_x = "nombre_mes"
        else:
            eje_x = "mes"

        fig_mensual = px.bar(
            mn_ordenado,
            x=eje_x,
            y="vuelos",
            color="pct_cancelaciones",
            # color representa la tasa de cancelacion de ese mes
            color_continuous_scale="RdYlGn_r",
            # _r invierte la escala: rojo = mas cancelaciones
            labels={
                eje_x: "Mes",
                "vuelos": "Total vuelos",
                "pct_cancelaciones": "% Cancelaciones"
            },
        )
        fig_mensual.update_layout(height=350, xaxis_tickangle=-45)
        # xaxis_tickangle inclina las etiquetas del eje X
        st.plotly_chart(fig_mensual, use_container_width=True)

    st.divider()

    # --------------------------------------------------------
    # FILA 3: TOP RUTAS Y SCATTER DISTANCIA VS RETRASO
    # --------------------------------------------------------

    col_izq3, col_der3 = st.columns(2)

    with col_izq3:
        st.subheader("Top 20 Rutas por Frecuencia")

        rt_top = rt.sort_values("total_vuelos", ascending=False).head(20)

        fig_rutas = px.bar(
            rt_top,
            x="ruta",
            y="total_vuelos",
            color="retraso_promedio",
            color_continuous_scale="RdYlGn_r",
            # rojo = rutas con mas retraso
            labels={
                "ruta": "Ruta",
                "total_vuelos": "Total vuelos",
                "retraso_promedio": "Retraso prom. (min)"
            },
        )
        fig_rutas.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_rutas, use_container_width=True)

    with col_der3:
        st.subheader("Distancia vs Retraso por Ruta")
        st.caption("Cada punto es una ruta. Revela si las rutas largas tienen mas retrasos.")

        fig_scatter = px.scatter(
            rt,
            x="distancia",
            y="retraso_promedio",
            size="total_vuelos",
            # size hace que los puntos mas grandes representen mas vuelos
            color="pct_puntual",
            color_continuous_scale="RdYlGn",
            hover_data=["ruta"],
            # hover_data muestra el nombre de la ruta al pasar el mouse
            labels={
                "distancia": "Distancia (millas)",
                "retraso_promedio": "Retraso prom. (min)",
                "pct_puntual": "% Puntual",
                "total_vuelos": "Total vuelos"
            },
        )
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()

    # --------------------------------------------------------
    # TABLA DETALLADA DE AEROLINEAS
    # --------------------------------------------------------

    st.subheader("Tabla Detallada por Aerolinea")
    st.dataframe(ae, use_container_width=True, hide_index=True)
    # st.dataframe muestra una tabla interactiva (se puede ordenar, buscar)


# ============================================================
# SECCION 2: CHAT CON EL AGENTE
# ============================================================

elif seccion == "Chat con IA":

    st.title("Chat con el Agente de Analisis")
    st.caption("Pregunta cualquier cosa sobre el dataset de retrasos de vuelos de EE.UU.")

    # --------------------------------------------------------
    # VERIFICAR API KEY
    # --------------------------------------------------------

    api_key = os.environ.get("OPENAI_API_KEY", "")
    # os.environ.get devuelve "" si la variable no existe

    if not api_key:
        # Si no hay API key cargada del .env, pedimos que la escriban
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            # type="password" oculta el texto con asteriscos
            placeholder="sk-...",
        )

        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        else:
            st.info("Escribe tu API Key de OpenAI para activar el chat.")
            st.stop()

    # --------------------------------------------------------
    # IMPORTAR EL CLIENTE Y LAS HERRAMIENTAS
    # --------------------------------------------------------
    # Importamos aqui (no al inicio) para que solo cargue cuando hay API key

    from dotenv import load_dotenv
    load_dotenv()

    from openai import OpenAI
    from tools import HERRAMIENTAS, DESCRIPCION_HERRAMIENTAS

    cliente_chat = OpenAI()

    INSTRUCCIONES_CHAT = (
        "Eres un analista de datos experto en aviacion de EE.UU. "
        "Tienes acceso a estadisticas reales del dataset de retrasos de vuelos de Kaggle. "
        "Usa siempre las herramientas para dar datos concretos. "
        "Responde en espanol."
    )

    # --------------------------------------------------------
    # ESTADO DE LA CONVERSACION
    # --------------------------------------------------------
    # st.session_state guarda variables entre interacciones del usuario
    # Sin esto, cada clic reinicia la pagina y perdemos el historial

    if "mensajes_pantalla" not in st.session_state:
        st.session_state.mensajes_pantalla = []
        # mensajes_pantalla: lo que mostramos en el chat al usuario

    if "historial_agente" not in st.session_state:
        st.session_state.historial_agente = []
        # historial_agente: lo que enviamos al modelo (incluye tool results)

    # --------------------------------------------------------
    # BOTON PARA LIMPIAR EL CHAT
    # --------------------------------------------------------

    if st.button("Nueva conversacion"):
        st.session_state.mensajes_pantalla = []
        st.session_state.historial_agente  = []
        st.rerun()
        # st.rerun() vuelve a ejecutar la app desde el principio

    # --------------------------------------------------------
    # SUGERENCIAS DE PREGUNTAS
    # --------------------------------------------------------

    if len(st.session_state.mensajes_pantalla) == 0:
        st.markdown("**Preguntas sugeridas:**")

        sugerencias = [
            "Dame un resumen general del dataset",
            "Que aerolinea tiene mas puntualidad?",
            "Top 5 rutas con mas retrasos",
            "A que hora hay mas retrasos?",
            "Como varia el retraso por mes?",
        ]

        columnas = st.columns(len(sugerencias))

        for i in range(len(sugerencias)):
            with columnas[i]:
                if st.button(sugerencias[i], key="sug_" + str(i)):
                    # Si el usuario hace clic en una sugerencia la procesamos
                    st.session_state.mensajes_pantalla.append(
                        {"role": "user", "content": sugerencias[i]}
                    )
                    st.session_state._pregunta_sugerida = sugerencias[i]
                    st.rerun()

    # --------------------------------------------------------
    # MOSTRAR EL HISTORIAL DEL CHAT
    # --------------------------------------------------------

    for mensaje in st.session_state.mensajes_pantalla:
        with st.chat_message(mensaje["role"]):
            # st.chat_message("user") → burbuja azul del usuario
            # st.chat_message("assistant") → burbuja gris del agente
            st.markdown(mensaje["content"])

    # --------------------------------------------------------
    # PROCESAR PREGUNTA NUEVA
    # --------------------------------------------------------

    pregunta_nueva = st.chat_input("Escribe tu pregunta aqui...")
    # st.chat_input es el campo de texto fijo en la parte inferior de la pagina

    # Verificamos si viene una pregunta de las sugerencias
    if not pregunta_nueva and hasattr(st.session_state, "_pregunta_sugerida"):
        pregunta_nueva = st.session_state._pregunta_sugerida
        del st.session_state._pregunta_sugerida

    if pregunta_nueva:
        # Mostramos la pregunta del usuario en el chat
        with st.chat_message("user"):
            st.markdown(pregunta_nueva)

        # Guardamos en los dos historiales
        st.session_state.mensajes_pantalla.append(
            {"role": "user", "content": pregunta_nueva}
        )
        st.session_state.historial_agente.append(
            {"role": "user", "content": pregunta_nueva}
        )

        # Procesamos con el agente
        with st.chat_message("assistant"):
            with st.spinner("Consultando datos..."):
                # st.spinner muestra un indicador de carga

                # Loop del agente (identico al de agente.py)
                for paso in range(10):

                    mensajes_api = (
                        [{"role": "system", "content": INSTRUCCIONES_CHAT}] +
                        st.session_state.historial_agente
                    )

                    respuesta_api = cliente_chat.chat.completions.create(
                        model="gpt-4o",
                        messages=mensajes_api,
                        tools=DESCRIPCION_HERRAMIENTAS,
                        tool_choice="auto",
                        temperature=0,
                    )

                    mensaje_modelo = respuesta_api.choices[0].message
                    st.session_state.historial_agente.append(mensaje_modelo)

                    if mensaje_modelo.tool_calls:
                        # El modelo quiere usar herramientas
                        for llamada in mensaje_modelo.tool_calls:
                            nombre = llamada.function.name
                            args   = json.loads(llamada.function.arguments)

                            herramienta = HERRAMIENTAS[nombre]
                            try:
                                resultado = herramienta(**args)
                            except Exception as e:
                                resultado = "Error: " + str(e)

                            st.session_state.historial_agente.append({
                                "role":         "tool",
                                "tool_call_id": llamada.id,
                                "content":      str(resultado)
                            })
                    else:
                        # El modelo tiene la respuesta final
                        respuesta_texto = mensaje_modelo.content
                        st.markdown(respuesta_texto)

                        # Guardamos la respuesta para mostrarla en recargas futuras
                        st.session_state.mensajes_pantalla.append(
                            {"role": "assistant", "content": respuesta_texto}
                        )
                        break
