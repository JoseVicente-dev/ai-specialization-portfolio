# ============================================================
# tools.py
# Define las herramientas que puede usar el agente
# Cada herramienta lee los CSVs generados por procesar.py
# ============================================================

import os
import pandas as pd

# ------------------------------------------------------------
# CARGAR LOS DATOS EN MEMORIA
# ------------------------------------------------------------
# Leemos los CSVs una sola vez cuando el programa arranca
# Asi no tenemos que releerlos cada vez que el agente usa una herramienta

if not os.path.exists("data/agg_aerolineas.csv"):
    print("ERROR: No se encontraron los datos procesados.")
    print("Ejecuta primero: python procesar.py")

# Cargamos cada CSV como una tabla de pandas
datos_aerolineas = pd.read_csv("data/agg_aerolineas.csv")
# datos_aerolineas: estadisticas agregadas por aerolinea

datos_rutas = pd.read_csv("data/agg_rutas.csv")
# datos_rutas: estadisticas por par origen-destino

datos_horario = pd.read_csv("data/agg_horario.csv")
# datos_horario: estadisticas por hora del dia

datos_mensual = pd.read_csv("data/agg_mensual.csv")
# datos_mensual: estadisticas por mes del ano

datos_estado = pd.read_csv("data/agg_estado.csv")
# datos_estado: estadisticas por aeropuerto de origen (top 30)

print("Datos cargados correctamente")


# ------------------------------------------------------------
# HERRAMIENTA 1: ESTADISTICAS DE UNA AEROLINEA
# ------------------------------------------------------------

def estadisticas_aerolinea(aerolinea):
    # aerolinea → codigo IATA de la aerolinea, por ejemplo "AA", "DL", "WN"

    # Filtramos la tabla buscando el codigo de aerolinea (sin distinguir mayusculas)
    fila = datos_aerolineas[
        datos_aerolineas["aerolinea"].str.upper() == aerolinea.upper()
    ]

    if len(fila) == 0:
        opciones = datos_aerolineas["aerolinea"].tolist()
        return "Aerolinea no encontrada. Codigos disponibles: " + str(opciones)

    r = fila.iloc[0]
    # .iloc[0] → primera fila del resultado

    def fmt(valor, sufijo=""):
        # Funcion auxiliar para formatear valores que pueden ser nulos
        if pd.isna(valor):
            return "sin datos"
        if sufijo == "min":
            return str(round(float(valor), 1)) + " min"
        if sufijo == "%":
            return str(round(float(valor), 1)) + "%"
        return str(int(valor))

    respuesta = (
        "Estadisticas de " + str(r["aerolinea"]) + ":\n"
        "  Vuelos totales:          " + fmt(r["total_vuelos"]) + "\n"
        "  Vuelos cancelados:       " + fmt(r["vuelos_cancelados"]) + "\n"
        "  % Cancelaciones:         " + fmt(r["pct_cancelaciones"], "%") + "\n"
        "  Retraso salida prom.:    " + fmt(r["retraso_salida_promedio"], "min") + "\n"
        "  Retraso llegada prom.:   " + fmt(r["retraso_llegada_promedio"], "min") + "\n"
        "  % Vuelos puntuales:      " + fmt(r["pct_puntual"], "%") + "\n"
        "  Distancia prom. (millas):" + fmt(r["distancia_promedio"])
    )

    return respuesta


# ------------------------------------------------------------
# HERRAMIENTA 2: COMPARAR TODAS LAS AEROLINEAS
# ------------------------------------------------------------

def comparar_aerolineas(metrica):
    # metrica → columna por la que ordenar el ranking

    metricas_validas = [
        "pct_puntual", "total_vuelos", "distancia_promedio",
        "retraso_salida_promedio", "retraso_llegada_promedio", "pct_cancelaciones"
    ]

    if metrica not in metricas_validas:
        return "Metrica invalida. Usa una de: " + str(metricas_validas)

    # Para retraso y cancelaciones el mejor tiene el numero MAS BAJO
    # Para el resto el mejor tiene el numero MAS ALTO
    if metrica in ["retraso_salida_promedio", "retraso_llegada_promedio", "pct_cancelaciones"]:
        ordenado = datos_aerolineas.sort_values(metrica, ascending=True)
        # ascending=True → de menor a mayor (mejor primero)
    else:
        ordenado = datos_aerolineas.sort_values(metrica, ascending=False)
        # ascending=False → de mayor a menor (mejor primero)

    texto = "Ranking de aerolineas por " + metrica + ":\n"

    for pos in range(len(ordenado)):
        fila  = ordenado.iloc[pos]
        valor = fila[metrica]
        if pd.isna(valor):
            valor_texto = "sin datos"
        else:
            valor_texto = str(round(float(valor), 1))
        texto += "  " + str(pos + 1) + ". " + str(fila["aerolinea"]) + ": " + valor_texto + "\n"

    return texto


# ------------------------------------------------------------
# HERRAMIENTA 3: TOP RUTAS
# ------------------------------------------------------------

def top_rutas(n, criterio):
    # n → cuantas rutas mostrar (maximo 20)
    # criterio → columna por la que ordenar

    criterios_validos = [
        "total_vuelos", "retraso_promedio", "pct_puntual", "distancia"
    ]

    if criterio not in criterios_validos:
        return "Criterio invalido. Usa uno de: " + str(criterios_validos)

    n = min(int(n), 20)
    # Limitamos a 20 rutas para no saturar la respuesta del agente

    if criterio == "retraso_promedio":
        top = datos_rutas.sort_values(criterio, ascending=True).head(n)
        # ascending=True → rutas con MENOS retraso primero
    else:
        top = datos_rutas.sort_values(criterio, ascending=False).head(n)

    texto = "Top " + str(n) + " rutas por " + criterio + ":\n"

    for i in range(len(top)):
        fila = top.iloc[i]
        texto += (
            "  " + str(i + 1) + ". " + str(fila["ruta"]) +
            " | " + str(int(fila["total_vuelos"])) + " vuelos" +
            " | retraso: " + str(fila["retraso_promedio"]) + " min" +
            " | " + str(fila["pct_puntual"]) + "% puntual\n"
        )

    return texto


# ------------------------------------------------------------
# HERRAMIENTA 4: ANALISIS POR HORA
# ------------------------------------------------------------

def analisis_horario(franja):
    # franja → "Manana", "Tarde", "Noche", "Madrugada" o "todas"

    tabla = datos_horario.copy()
    # .copy() para no modificar el DataFrame original

    if franja.lower() != "todas":
        tabla = tabla[tabla["franja_dia"].str.lower() == franja.lower()]

        if len(tabla) == 0:
            return "Franja no encontrada. Opciones: Manana, Tarde, Noche, Madrugada, todas"

    tabla = tabla.sort_values("hora")

    texto = "Analisis horario (" + franja + "):\n"

    for i in range(len(tabla)):
        fila = tabla.iloc[i]
        hora_texto = str(int(fila["hora"])).zfill(2)
        # .zfill(2) rellena con cero: "9" → "09"

        retraso = fila["retraso_promedio"]
        retraso_texto = "sin datos" if pd.isna(retraso) else str(retraso) + " min"

        texto += (
            "  " + hora_texto + "h [" + str(fila["franja_dia"]) + "]"
            " | " + str(int(fila["vuelos"])) + " vuelos"
            " | " + str(fila["pct_puntual"]) + "% puntual"
            " | retraso prom: " + retraso_texto + "\n"
        )

    return texto


# ------------------------------------------------------------
# HERRAMIENTA 5: EVOLUCION MENSUAL
# ------------------------------------------------------------

def evolucion_mensual():
    # No recibe argumentos, muestra todos los meses disponibles

    tabla = datos_mensual.sort_values("mes")

    texto = "Evolucion mensual de vuelos:\n"

    for i in range(len(tabla)):
        fila = tabla.iloc[i]

        variacion = fila["variacion_pct"]
        if pd.isna(variacion):
            var_texto = "base"
        elif float(variacion) >= 0:
            var_texto = "+" + str(variacion) + "%"
        else:
            var_texto = str(variacion) + "%"

        nombre = fila["nombre_mes"] if "nombre_mes" in fila.index else "Mes " + str(int(fila["mes"]))

        texto += (
            "  " + nombre +
            ": " + str(int(fila["vuelos"])) + " vuelos" +
            " | cancelaciones: " + str(int(fila["cancelaciones"])) +
            " | retraso prom: " + str(fila["retraso_promedio"]) + " min" +
            " | variacion: " + var_texto + "\n"
        )

    return texto


# ------------------------------------------------------------
# HERRAMIENTA 6: RESUMEN GENERAL
# ------------------------------------------------------------

def resumen_general():
    # No recibe argumentos, devuelve un resumen ejecutivo del dataset completo

    ae = datos_aerolineas

    total_vuelos     = int(ae["total_vuelos"].sum())
    total_cancelados = int(ae["vuelos_cancelados"].sum()) if "vuelos_cancelados" in ae.columns else 0
    pct_cancelaciones = round(total_cancelados / total_vuelos * 100, 1) if total_vuelos > 0 else 0
    retraso_global   = round(float(ae["retraso_salida_promedio"].mean()), 1)
    puntualidad_global = round(float(ae["pct_puntual"].mean()), 1)

    # Aerolinea con mejor y peor puntualidad
    idx_mejor = ae["pct_puntual"].idxmax()
    # .idxmax() devuelve el indice de la fila con el valor mas alto
    idx_peor  = ae["pct_puntual"].idxmin()
    # .idxmin() devuelve el indice de la fila con el valor mas bajo

    mejor_aerolinea = ae.loc[idx_mejor, "aerolinea"]
    peor_aerolinea  = ae.loc[idx_peor, "aerolinea"]

    # Ruta mas frecuente
    idx_ruta_top = datos_rutas["total_vuelos"].idxmax()
    ruta_top = datos_rutas.loc[idx_ruta_top, "ruta"]

    # Hora con mas retrasos
    idx_hora_peor = datos_horario["retraso_promedio"].idxmax()
    hora_peor = int(datos_horario.loc[idx_hora_peor, "hora"])

    respuesta = (
        "Resumen general del dataset de vuelos EE.UU.:\n"
        "  Total de vuelos:           " + str(total_vuelos) + "\n"
        "  Vuelos cancelados:         " + str(total_cancelados) + " (" + str(pct_cancelaciones) + "%)\n"
        "  Retraso promedio salida:   " + str(retraso_global) + " min\n"
        "  Puntualidad global:        " + str(puntualidad_global) + "%\n"
        "  Aerolinea mas puntual:     " + mejor_aerolinea + "\n"
        "  Aerolinea menos puntual:   " + peor_aerolinea + "\n"
        "  Ruta mas frecuente:        " + ruta_top + "\n"
        "  Hora con mas retrasos:     " + str(hora_peor) + ":00h"
    )

    return respuesta


# ------------------------------------------------------------
# HERRAMIENTA 7: ANALISIS DE UN AEROPUERTO
# ------------------------------------------------------------

def analisis_aeropuerto(codigo):
    # codigo → codigo IATA del aeropuerto, por ejemplo "LAX", "JFK", "ATL"

    fila = datos_estado[
        datos_estado["origen"].str.upper() == codigo.upper()
    ]

    if len(fila) == 0:
        opciones = datos_estado["origen"].tolist()
        return "Aeropuerto no encontrado en el top 30. Disponibles: " + str(opciones)

    r = fila.iloc[0]

    respuesta = (
        "Estadisticas del aeropuerto " + str(r["origen"]) + " (como origen):\n"
        "  Total vuelos partiendo:  " + str(int(r["total_vuelos"])) + "\n"
        "  Retraso promedio salida: " + str(r["retraso_promedio"]) + " min\n"
        "  % Vuelos puntuales:      " + str(r["pct_puntual"]) + "%"
    )

    return respuesta


# ------------------------------------------------------------
# REGISTRO DE HERRAMIENTAS
# ------------------------------------------------------------
# Diccionario con todas las herramientas disponibles
# La clave es el nombre que el agente usara para llamarlas

HERRAMIENTAS = {
    "estadisticas_aerolinea": estadisticas_aerolinea,
    "comparar_aerolineas":    comparar_aerolineas,
    "top_rutas":              top_rutas,
    "analisis_horario":       analisis_horario,
    "evolucion_mensual":      evolucion_mensual,
    "resumen_general":        resumen_general,
    "analisis_aeropuerto":    analisis_aeropuerto,
}

# Describimos cada herramienta para que el agente sepa cuando usarlas
# Este texto lo lee el modelo de lenguaje para decidir cual herramienta invocar
DESCRIPCION_HERRAMIENTAS = [
    {
        "type": "function",
        "function": {
            "name": "estadisticas_aerolinea",
            "description": "Devuelve estadisticas completas de una aerolinea: vuelos, cancelaciones, retraso promedio y puntualidad.",
            "parameters": {
                "type": "object",
                "properties": {
                    "aerolinea": {
                        "type": "string",
                        "description": "Codigo IATA de la aerolinea, por ejemplo: AA (American), DL (Delta), WN (Southwest), UA (United)"
                    }
                },
                "required": ["aerolinea"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "comparar_aerolineas",
            "description": "Compara y rankea todas las aerolineas segun una metrica especifica.",
            "parameters": {
                "type": "object",
                "properties": {
                    "metrica": {
                        "type": "string",
                        "description": "Columna por la que ordenar: pct_puntual, total_vuelos, distancia_promedio, retraso_salida_promedio, retraso_llegada_promedio, pct_cancelaciones"
                    }
                },
                "required": ["metrica"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "top_rutas",
            "description": "Muestra las rutas mas destacadas segun un criterio (frecuencia, retraso o puntualidad).",
            "parameters": {
                "type": "object",
                "properties": {
                    "n": {
                        "type": "integer",
                        "description": "Cuantas rutas mostrar (maximo 20)"
                    },
                    "criterio": {
                        "type": "string",
                        "description": "Por que ordenar: total_vuelos, retraso_promedio, pct_puntual, distancia"
                    }
                },
                "required": ["n", "criterio"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analisis_horario",
            "description": "Analiza puntualidad y retraso por hora o franja del dia.",
            "parameters": {
                "type": "object",
                "properties": {
                    "franja": {
                        "type": "string",
                        "description": "Franja a analizar: Manana (6-11h), Tarde (12-17h), Noche (18-23h), Madrugada (0-5h) o todas"
                    }
                },
                "required": ["franja"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "evolucion_mensual",
            "description": "Muestra como evolucionaron los vuelos y retrasos mes a mes durante el ano.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "resumen_general",
            "description": "Devuelve un resumen ejecutivo completo del dataset sin necesitar argumentos.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analisis_aeropuerto",
            "description": "Estadisticas de un aeropuerto especifico como punto de origen de vuelos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo": {
                        "type": "string",
                        "description": "Codigo IATA del aeropuerto, por ejemplo: ATL, LAX, ORD, DFW, JFK"
                    }
                },
                "required": ["codigo"]
            }
        }
    },
]
