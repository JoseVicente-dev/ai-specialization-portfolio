# ============================================================
# reporte.py
# Generador automatico de reportes analiticos con GPT-4
#
# Lee las 5 tablas agregadas generadas por procesar.py,
# las envia a GPT-4o como contexto estructurado y guarda
# el reporte analitico resultante en data/reporte_final.md
#
# Requiere: archivos CSV en data/ (ejecutar procesar.py primero)
#           archivo .env con OPENAI_API_KEY=sk-...
# Ejecucion: python reporte.py
# Salida: data/reporte_final.md
# ============================================================

import os
import sys
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Cargamos las variables del archivo .env
load_dotenv()

# ------------------------------------------------------------
# CONFIGURACION
# ------------------------------------------------------------

MODELO_REPORTE = "gpt-4o"
# Cambiar a "gpt-4o-mini" para reducir costos (~10x mas barato)
# gpt-4o tiene contexto de 128K tokens, mas que suficiente para este reporte

TEMPERATURA = 0.3
# 0.3 permite prosa analitica fluida manteniendo consistencia con los datos

MAX_TOKENS_RESPUESTA = 2500
# Suficiente para un reporte de ~1500 palabras con todas las secciones

RUTA_SALIDA = "data/reporte_final.md"

# ------------------------------------------------------------
# VERIFICACIONES INICIALES
# ------------------------------------------------------------

# Verificamos que los datos procesados existen
archivos_requeridos = [
    "data/agg_aerolineas.csv",
    "data/agg_rutas.csv",
    "data/agg_horario.csv",
    "data/agg_mensual.csv",
    "data/agg_estado.csv",
]

for archivo in archivos_requeridos:
    if not os.path.exists(archivo):
        print("ERROR: No se encontro el archivo " + archivo)
        print("Ejecuta primero: python procesar.py")
        sys.exit(1)

# Verificamos que la API key existe
if not os.environ.get("OPENAI_API_KEY"):
    print("ERROR: No se encontro OPENAI_API_KEY.")
    print("Crea un archivo .env con: OPENAI_API_KEY=sk-tu-clave")
    sys.exit(1)

# ------------------------------------------------------------
# CARGAR LAS AGREGACIONES
# ------------------------------------------------------------

def cargar_agregaciones():
    # Leemos los 5 CSVs generados por procesar.py
    datos = {
        "aerolineas": pd.read_csv("data/agg_aerolineas.csv"),
        "rutas":      pd.read_csv("data/agg_rutas.csv"),
        "horario":    pd.read_csv("data/agg_horario.csv"),
        "mensual":    pd.read_csv("data/agg_mensual.csv"),
        "estado":     pd.read_csv("data/agg_estado.csv"),
    }
    return datos


# ------------------------------------------------------------
# FORMATEAR TABLAS PARA EL PROMPT
# ------------------------------------------------------------

def formatear_tabla(df, max_filas=20):
    # Limitamos el numero de filas para controlar el uso de tokens
    df_limitado = df.head(max_filas)

    # to_string() produce una tabla de texto bien alineada
    return df_limitado.to_string(index=False)


# ------------------------------------------------------------
# CONSTRUIR EL SYSTEM PROMPT
# ------------------------------------------------------------

def construir_prompt_sistema():
    return (
        "Eres un analista senior de operaciones aereas con 15 anos de experiencia "
        "en la industria de aviacion de EE.UU. Tu tarea es generar reportes analiticos "
        "profesionales en espanol basados exclusivamente en los datos que se te proporcionan.\n\n"
        "REGLAS ESTRICTAS:\n"
        "- No inventes datos ni cifras que no aparezcan en las tablas.\n"
        "- Basa cada observacion en numeros concretos de las tablas.\n"
        "- Usa un tono ejecutivo, formal y directo.\n"
        "- Redacta en espanol con tildes y enies correctos.\n\n"
        "FORMATO OBLIGATORIO DEL REPORTE (usa exactamente estas secciones en Markdown):\n\n"
        "# Reporte de Analisis de Retrasos de Vuelos — EE.UU.\n\n"
        "## 1. Resumen Ejecutivo\n"
        "(3-4 oraciones: hallazgo principal, magnitud del problema, recomendacion clave)\n\n"
        "## 2. Estadisticas Descriptivas Generales\n"
        "(tabla o lista con: total vuelos, tasa cancelacion global, retraso promedio, "
        "% vuelos puntuales, aerolinea con mejor y peor desempeno)\n\n"
        "## 3. Analisis por Aerolinea\n"
        "(observaciones sobre las 3 mejores y 3 peores en puntualidad con datos concretos)\n\n"
        "## 4. Patrones Temporales\n"
        "### 4.1 Patron Horario\n"
        "(que horas concentran mas retrasos y posible causa operacional)\n"
        "### 4.2 Estacionalidad Mensual\n"
        "(meses criticos, posibles causas: clima, demanda vacacional)\n\n"
        "## 5. Analisis de Rutas\n"
        "(rutas con mayor congestion vs rutas con mejor operacion; anomalias destacables)\n\n"
        "## 6. Recomendaciones Operacionales\n"
        "(5 recomendaciones concretas numeradas, basadas exclusivamente en los datos)\n\n"
        "## 7. Sugerencias de Visualizacion\n"
        "(5 graficos especificos con tipo de grafico y variables recomendadas)\n\n"
        "---\n"
        "*Reporte generado automaticamente con " + MODELO_REPORTE + "*"
    )


# ------------------------------------------------------------
# CONSTRUIR EL USER PROMPT CON LOS DATOS
# ------------------------------------------------------------

def construir_prompt_usuario(datos):
    # Calculamos estadisticas globales para incluir en el contexto
    ae = datos["aerolineas"]
    total_vuelos = int(ae["total_vuelos"].sum()) if "total_vuelos" in ae.columns else "N/D"

    # Ordenamos las tablas para el prompt
    rutas_top = datos["rutas"].sort_values("total_vuelos", ascending=False).head(20)
    horario_ordenado = datos["horario"].sort_values("hora")
    mensual_ordenado = datos["mensual"].sort_values("mes")
    estado_top = datos["estado"].sort_values("total_vuelos", ascending=False).head(15)

    prompt = (
        "Analiza el siguiente dataset de retrasos de vuelos de EE.UU. "
        "y genera el reporte completo siguiendo el formato indicado.\n\n"

        "=== CONTEXTO DEL DATASET ===\n"
        "Fuente: Kaggle — Flight Delay Analysis (dataset usdot/flight-delays)\n"
        "Cobertura: Vuelos domesticos de EE.UU.\n"
        "Total registros procesados: " + str(total_vuelos) + " vuelos\n"
        "Umbral de puntualidad: retraso de salida <= 15 minutos (estandar FAA)\n\n"

        "=== ESTADISTICAS POR AEROLINEA ===\n"
        + formatear_tabla(ae) + "\n\n"

        "=== TOP 20 RUTAS POR FRECUENCIA ===\n"
        + formatear_tabla(rutas_top) + "\n\n"

        "=== PATRON HORARIO ===\n"
        + formatear_tabla(horario_ordenado) + "\n\n"

        "=== EVOLUCION MENSUAL ===\n"
        + formatear_tabla(mensual_ordenado) + "\n\n"

        "=== TOP 15 AEROPUERTOS DE ORIGEN ===\n"
        + formatear_tabla(estado_top) + "\n\n"

        "Genera ahora el reporte completo en Markdown siguiendo exactamente "
        "el formato de 7 secciones especificado en las instrucciones del sistema."
    )

    return prompt


# ------------------------------------------------------------
# LLAMAR A GPT-4
# ------------------------------------------------------------

def llamar_gpt4(prompt_sistema, prompt_usuario, cliente):
    print("Enviando datos a " + MODELO_REPORTE + " ...")
    print("(Esto puede tardar 15-30 segundos)")

    try:
        respuesta = cliente.chat.completions.create(
            model=MODELO_REPORTE,
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user",   "content": prompt_usuario},
            ],
            temperature=TEMPERATURA,
            max_tokens=MAX_TOKENS_RESPUESTA,
        )

        # Mostramos informacion sobre el uso de tokens
        uso = respuesta.usage
        print("Tokens usados — entrada: " + str(uso.prompt_tokens) +
              " | salida: " + str(uso.completion_tokens) +
              " | total: " + str(uso.total_tokens))

        # Extraemos el texto del reporte
        contenido = respuesta.choices[0].message.content
        return contenido

    except Exception as e:
        # Capturamos el tipo de error para dar instrucciones utiles
        tipo_error = type(e).__name__

        if "PermissionDenied" in tipo_error or "AuthenticationError" in tipo_error:
            print("ERROR de autenticacion: verifica tu OPENAI_API_KEY en el archivo .env")
            print("Si tu cuenta no tiene acceso a " + MODELO_REPORTE + ",")
            print("cambia MODELO_REPORTE = 'gpt-4o-mini' al inicio de este archivo.")
        elif "RateLimit" in tipo_error:
            print("ERROR de rate limit: demasiadas solicitudes.")
            print("Espera 1 minuto y vuelve a ejecutar el script.")
        elif "Connection" in tipo_error:
            print("ERROR de conexion: verifica tu conexion a internet.")
        else:
            print("ERROR al llamar a la API: " + str(e))

        sys.exit(1)


# ------------------------------------------------------------
# GUARDAR EL REPORTE
# ------------------------------------------------------------

def guardar_reporte(contenido_llm, datos, ruta_salida):
    # Generamos una cabecera con metadatos automaticos
    ae = datos["aerolineas"]
    total_vuelos = int(ae["total_vuelos"].sum()) if "total_vuelos" in ae.columns else "N/D"
    fecha_generacion = datetime.now().strftime("%Y-%m-%d %H:%M")

    cabecera = (
        "<!-- Reporte generado automaticamente — no editar esta cabecera -->\n"
        "<!-- Fecha: " + fecha_generacion + " | Modelo: " + MODELO_REPORTE + " -->\n"
        "<!-- Vuelos analizados: " + str(total_vuelos) + " -->\n\n"
    )

    # Pie de pagina para el reporte academico
    pie = (
        "\n\n---\n\n"
        "## Nota Metodologica\n\n"
        "Este reporte fue generado automaticamente utilizando el modelo " + MODELO_REPORTE + " "
        "de OpenAI, a partir de estadisticas agregadas calculadas con PySpark sobre el "
        "dataset *Flight Delay Analysis* de Kaggle (fuente: Bureau of Transportation Statistics, "
        "U.S. Department of Transportation).\n\n"
        "**Proceso:**\n"
        "1. Los datos crudos fueron procesados con PySpark (`procesar.py`) para calcular "
        "estadisticas por aerolinea, ruta, hora y mes.\n"
        "2. Las tablas agregadas fueron enviadas como contexto estructurado al modelo LLM.\n"
        "3. El modelo genero las observaciones, conclusiones y recomendaciones.\n\n"
        "**Complemento humano:** [Espacio para que el analista agregue sus propias "
        "observaciones, correcciones o analisis adicional]\n"
    )

    contenido_final = cabecera + contenido_llm + pie

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(contenido_final)
    # encoding="utf-8" asegura que los caracteres especiales (tildes, enies) se guarden bien

    print("Reporte guardado en: " + ruta_salida)


# ------------------------------------------------------------
# FUNCION PRINCIPAL
# ------------------------------------------------------------

def generar_reporte_completo():
    print("=" * 55)
    print("  Generador de Reporte Analitico con GPT-4")
    print("=" * 55)
    print()

    # Creamos el cliente de OpenAI
    # Lee automaticamente OPENAI_API_KEY del entorno
    cliente = OpenAI()

    # Cargamos los datos agregados
    print("Cargando datos agregados...")
    datos = cargar_agregaciones()
    print("Datos cargados: " + str(len(datos)) + " tablas")
    print()

    # Construimos los prompts
    prompt_sistema = construir_prompt_sistema()
    prompt_usuario = construir_prompt_usuario(datos)

    # Estimamos el tamano del prompt
    chars_total = len(prompt_sistema) + len(prompt_usuario)
    tokens_estimados = chars_total // 4
    # Aproximacion: ~4 caracteres por token en texto en espanol
    print("Tamano del prompt: ~" + str(tokens_estimados) + " tokens estimados")
    print()

    # Llamamos a GPT-4
    contenido_reporte = llamar_gpt4(prompt_sistema, prompt_usuario, cliente)
    print()

    # Guardamos el reporte
    guardar_reporte(contenido_reporte, datos, RUTA_SALIDA)
    print()
    print("Listo. Para ver el reporte:")
    print("  - Abre el archivo: " + RUTA_SALIDA)
    print("  - O ejecuta: streamlit run app.py  (disponible en el sidebar)")
    print()
    print("Recuerda complementar el reporte con tus propias observaciones")
    print("en la seccion 'Complemento humano' al final del archivo.")


# ------------------------------------------------------------
# PUNTO DE ENTRADA
# ------------------------------------------------------------

if __name__ == "__main__":
    generar_reporte_completo()
