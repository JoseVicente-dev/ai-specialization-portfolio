# ============================================================
# procesar.py
# Pipeline de procesamiento de datos con PySpark
# Lee el CSV crudo de Kaggle y genera 5 tablas agregadas
#
# Requiere: data/flights.csv (dataset de Kaggle)
# Ejecucion: python procesar.py
# Salida: 5 archivos CSV en data/
# ============================================================

import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# ------------------------------------------------------------
# VERIFICAR QUE EL ARCHIVO DE DATOS EXISTE
# ------------------------------------------------------------

RUTA_DATASET = "data/flights.csv"

if not os.path.exists(RUTA_DATASET):
    print("ERROR: No se encontro el archivo de datos.")
    print("Descarga el dataset con:")
    print("  kaggle datasets download -d usdot/flight-delays --unzip -p data/")
    print("El archivo debe quedar en: " + RUTA_DATASET)
    sys.exit(1)

# Verificamos que la carpeta de salida existe
os.makedirs("data", exist_ok=True)
# os.makedirs con exist_ok=True crea la carpeta solo si no existe

# ------------------------------------------------------------
# CREAR LA SESION DE SPARK
# ------------------------------------------------------------

def crear_sesion_spark():
    # Configuramos Spark para correr en la maquina local
    # local[*] usa todos los nucleos del procesador disponibles
    spark = (
        SparkSession.builder
        .appName("FlightDelayAnalysis")
        .master("local[*]")
        .config("spark.driver.memory", "4g")
        # 4g → reservamos 4 GB de RAM para el driver de Spark
        .config("spark.sql.shuffle.partitions", "8")
        # 8 particiones es suficiente para modo local; el default de 200 es excesivo
        .config("spark.ui.showConsoleProgress", "false")
        # Silenciamos la barra de progreso de consola de Spark
        .getOrCreate()
    )
    # Reducimos el nivel de logs para que no inunden la consola
    spark.sparkContext.setLogLevel("ERROR")
    return spark


# ------------------------------------------------------------
# CARGAR Y NORMALIZAR EL DATASET
# ------------------------------------------------------------

def cargar_dataset(spark, ruta):
    print("Cargando dataset desde " + ruta + " ...")

    df = spark.read.csv(
        ruta,
        header=True,
        # header=True indica que la primera fila tiene los nombres de columnas
        inferSchema=True,
        # inferSchema=True detecta automaticamente el tipo de cada columna
    )

    # Normalizamos los nombres de columna a MAYUSCULAS sin espacios
    # Esto hace el codigo mas robusto ante variaciones del CSV
    df = df.toDF(*[c.upper().strip().replace(" ", "_") for c in df.columns])
    # * desempaqueta la lista como argumentos individuales

    # Verificamos que las columnas esenciales existen
    columnas_requeridas = [
        "AIRLINE", "ORIGIN_AIRPORT", "DESTINATION_AIRPORT",
        "DEPARTURE_DELAY", "ARRIVAL_DELAY", "CANCELLED",
        "SCHEDULED_DEPARTURE", "MONTH", "DISTANCE"
    ]
    columnas_presentes = df.columns
    faltantes = [c for c in columnas_requeridas if c not in columnas_presentes]

    if faltantes:
        print("ERROR: Faltan columnas en el CSV: " + str(faltantes))
        print("Columnas encontradas: " + str(columnas_presentes))
        sys.exit(1)

    total = df.count()
    print("Registros cargados: " + str(total))
    return df


# ------------------------------------------------------------
# LIMPIAR Y ENRIQUECER LOS DATOS
# ------------------------------------------------------------

def limpiar_datos(df):
    print("Limpiando y enriqueciendo datos...")

    # Casteamos las columnas numericas al tipo correcto
    # Algunos CSV traen estos valores como string
    df = df.withColumn("DEPARTURE_DELAY", F.col("DEPARTURE_DELAY").cast("double"))
    df = df.withColumn("ARRIVAL_DELAY",   F.col("ARRIVAL_DELAY").cast("double"))
    df = df.withColumn("CANCELLED",       F.col("CANCELLED").cast("integer"))
    df = df.withColumn("DISTANCE",        F.col("DISTANCE").cast("double"))
    df = df.withColumn("MONTH",           F.col("MONTH").cast("integer"))
    df = df.withColumn("SCHEDULED_DEPARTURE", F.col("SCHEDULED_DEPARTURE").cast("integer"))

    # Eliminamos filas donde AIRLINE o los aeropuertos son nulos
    # Estos registros no aportan informacion util
    df = df.filter(
        F.col("AIRLINE").isNotNull() &
        F.col("ORIGIN_AIRPORT").isNotNull() &
        F.col("DESTINATION_AIRPORT").isNotNull()
    )

    # Extraemos la hora de salida desde SCHEDULED_DEPARTURE
    # SCHEDULED_DEPARTURE es un entero HHMM: 1430 = 14:30 (2:30 PM)
    # floor(1430 / 100) = 14 → hora correcta
    df = df.withColumn(
        "HORA_SALIDA",
        F.floor(F.col("SCHEDULED_DEPARTURE") / 100).cast("integer")
    )

    # Clasificamos la hora en franjas del dia
    df = df.withColumn(
        "FRANJA_DIA",
        F.when(F.col("HORA_SALIDA").between(0, 5),   "Madrugada")
         .when(F.col("HORA_SALIDA").between(6, 11),  "Manana")
         .when(F.col("HORA_SALIDA").between(12, 17), "Tarde")
         .otherwise("Noche")
        # .between(a, b) → True si el valor esta entre a y b (inclusive)
    )

    # Marcamos cada vuelo como puntual o no (estandar FAA: <= 15 minutos)
    df = df.withColumn(
        "ES_PUNTUAL",
        F.when(
            F.col("CANCELLED") == 1, 0
            # Un vuelo cancelado nunca es puntual
        ).when(
            F.col("DEPARTURE_DELAY").isNull(), None
            # Si no hay dato de retraso, dejamos nulo
        ).when(
            F.col("DEPARTURE_DELAY") <= 15, 1
            # <= 15 minutos → vuelo puntual
        ).otherwise(0)
    )

    # Guardamos el DataFrame en memoria para que no se recalcule
    df = df.cache()
    # .cache() guarda el DF en RAM despues del primer calculo

    registros_limpios = df.count()
    print("Registros despues de limpieza: " + str(registros_limpios))
    return df


# ------------------------------------------------------------
# AGREGACION 1: ESTADISTICAS POR AEROLINEA
# ------------------------------------------------------------

def agregar_por_aerolinea(df):
    print("Calculando estadisticas por aerolinea...")

    # Separamos vuelos cancelados de los que despegaron
    # Para retrasos solo usamos vuelos que si volaron
    df_volados = df.filter(F.col("CANCELLED") == 0)

    agg = df.groupBy("AIRLINE").agg(
        F.count("*").alias("total_vuelos"),
        # count("*") cuenta todas las filas del grupo
        F.sum("CANCELLED").alias("vuelos_cancelados"),
        F.round(
            F.sum("CANCELLED") / F.count("*") * 100, 1
        ).alias("pct_cancelaciones"),
    )

    agg_retrasos = df_volados.groupBy("AIRLINE").agg(
        F.round(F.mean("DEPARTURE_DELAY"), 1).alias("retraso_salida_promedio"),
        # mean() calcula el promedio, ignorando valores nulos
        F.round(F.mean("ARRIVAL_DELAY"), 1).alias("retraso_llegada_promedio"),
        F.round(F.mean("ES_PUNTUAL") * 100, 1).alias("pct_puntual"),
        F.round(F.mean("DISTANCE"), 0).alias("distancia_promedio"),
    )

    # Unimos las dos agregaciones por AIRLINE
    resultado = agg.join(agg_retrasos, on="AIRLINE", how="left")
    # how="left" mantiene todas las aerolineas aunque no tengan vuelos registrados

    resultado = resultado.orderBy("total_vuelos", ascending=False)
    # Ordenamos por total de vuelos de mayor a menor

    # Renombramos la columna para el dashboard
    resultado = resultado.withColumnRenamed("AIRLINE", "aerolinea")

    return resultado


# ------------------------------------------------------------
# AGREGACION 2: ESTADISTICAS POR RUTA
# ------------------------------------------------------------

def agregar_por_ruta(df):
    print("Calculando estadisticas por ruta...")

    df_volados = df.filter(F.col("CANCELLED") == 0)

    resultado = df_volados.groupBy("ORIGIN_AIRPORT", "DESTINATION_AIRPORT").agg(
        F.count("*").alias("total_vuelos"),
        F.round(F.mean("DEPARTURE_DELAY"), 1).alias("retraso_promedio"),
        F.round(F.mean("ES_PUNTUAL") * 100, 1).alias("pct_puntual"),
        F.round(F.first("DISTANCE"), 0).alias("distancia"),
        # first() toma el primer valor de DISTANCE (es constante por ruta)
    )

    # Filtramos rutas con menos de 50 vuelos para evitar ruido estadistico
    resultado = resultado.filter(F.col("total_vuelos") >= 50)

    # Creamos la columna "ruta" concatenando origen y destino
    resultado = resultado.withColumn(
        "ruta",
        F.concat(
            F.col("ORIGIN_AIRPORT"),
            F.lit(" -> "),
            # F.lit() crea una columna con un valor constante
            F.col("DESTINATION_AIRPORT")
        )
    )

    resultado = resultado.orderBy("total_vuelos", ascending=False)

    # Renombramos para consistencia
    resultado = resultado.withColumnRenamed("ORIGIN_AIRPORT", "origen")
    resultado = resultado.withColumnRenamed("DESTINATION_AIRPORT", "destino")

    return resultado


# ------------------------------------------------------------
# AGREGACION 3: ESTADISTICAS POR HORA DEL DIA
# ------------------------------------------------------------

def agregar_por_hora(df):
    print("Calculando estadisticas por hora...")

    df_volados = df.filter(
        (F.col("CANCELLED") == 0) &
        F.col("HORA_SALIDA").isNotNull() &
        F.col("HORA_SALIDA").between(0, 23)
        # Filtramos horas validas (algunas filas tienen valores erroneos)
    )

    resultado = df_volados.groupBy("HORA_SALIDA", "FRANJA_DIA").agg(
        F.count("*").alias("vuelos"),
        F.round(F.mean("DEPARTURE_DELAY"), 1).alias("retraso_promedio"),
        F.round(F.mean("ES_PUNTUAL") * 100, 1).alias("pct_puntual"),
    )

    resultado = resultado.orderBy("HORA_SALIDA")

    resultado = resultado.withColumnRenamed("HORA_SALIDA", "hora")
    resultado = resultado.withColumnRenamed("FRANJA_DIA", "franja_dia")

    return resultado


# ------------------------------------------------------------
# AGREGACION 4: EVOLUCION MENSUAL
# ------------------------------------------------------------

def agregar_mensual(df):
    print("Calculando estadisticas mensuales...")

    agg = df.groupBy("MONTH").agg(
        F.count("*").alias("vuelos"),
        F.sum("CANCELLED").alias("cancelaciones"),
        F.round(
            F.sum("CANCELLED") / F.count("*") * 100, 1
        ).alias("pct_cancelaciones"),
        F.round(
            F.mean(F.when(F.col("CANCELLED") == 0, F.col("DEPARTURE_DELAY"))), 1
        ).alias("retraso_promedio"),
        # mean() con condicion: solo promediamos retrasos de vuelos que despegaron
    )

    # Calculamos la variacion porcentual respecto al mes anterior
    ventana = Window.orderBy("MONTH")
    # Window define el orden para funciones de ventana (como lag)

    agg = agg.withColumn(
        "vuelos_mes_anterior",
        F.lag("vuelos", 1).over(ventana)
        # lag(col, n) trae el valor de n filas atras
    )

    agg = agg.withColumn(
        "variacion_pct",
        F.round(
            (F.col("vuelos") - F.col("vuelos_mes_anterior")) /
            F.col("vuelos_mes_anterior") * 100,
            1
        )
    )

    agg = agg.drop("vuelos_mes_anterior")
    # Eliminamos la columna auxiliar

    # Creamos la columna nombre_mes con F.when para legibilidad
    agg = agg.withColumn(
        "nombre_mes",
        F.when(F.col("MONTH") == 1,  "Enero")
         .when(F.col("MONTH") == 2,  "Febrero")
         .when(F.col("MONTH") == 3,  "Marzo")
         .when(F.col("MONTH") == 4,  "Abril")
         .when(F.col("MONTH") == 5,  "Mayo")
         .when(F.col("MONTH") == 6,  "Junio")
         .when(F.col("MONTH") == 7,  "Julio")
         .when(F.col("MONTH") == 8,  "Agosto")
         .when(F.col("MONTH") == 9,  "Septiembre")
         .when(F.col("MONTH") == 10, "Octubre")
         .when(F.col("MONTH") == 11, "Noviembre")
         .otherwise("Diciembre")
    )

    agg = agg.orderBy("MONTH")
    agg = agg.withColumnRenamed("MONTH", "mes")

    return agg


# ------------------------------------------------------------
# AGREGACION 5: TOP AEROPUERTOS DE ORIGEN
# ------------------------------------------------------------

def agregar_por_aeropuerto(df):
    print("Calculando estadisticas por aeropuerto de origen...")

    df_volados = df.filter(F.col("CANCELLED") == 0)

    resultado = df_volados.groupBy("ORIGIN_AIRPORT").agg(
        F.count("*").alias("total_vuelos"),
        F.round(F.mean("DEPARTURE_DELAY"), 1).alias("retraso_promedio"),
        F.round(F.mean("ES_PUNTUAL") * 100, 1).alias("pct_puntual"),
    )

    # Nos quedamos con los 30 aeropuertos con mas vuelos
    resultado = resultado.orderBy("total_vuelos", ascending=False).limit(30)
    # .limit(30) equivale a LIMIT 30 en SQL

    resultado = resultado.withColumnRenamed("ORIGIN_AIRPORT", "origen")

    return resultado


# ------------------------------------------------------------
# GUARDAR COMO CSV
# ------------------------------------------------------------

def guardar_csv(df_spark, ruta_salida):
    # Convertimos el DataFrame de Spark a pandas para guardarlo
    # Las agregaciones son pequenas (<1000 filas), esto es seguro y eficiente
    df_pandas = df_spark.toPandas()
    df_pandas.to_csv(ruta_salida, index=False)
    # index=False → no guarda el indice de fila como columna extra
    print("  Guardado: " + ruta_salida + " (" + str(len(df_pandas)) + " filas)")


# ------------------------------------------------------------
# FUNCION PRINCIPAL
# ------------------------------------------------------------

def main():
    print("=" * 55)
    print("  Pipeline PySpark — Analisis de Retrasos de Vuelos")
    print("=" * 55)
    print()

    # Creamos la sesion de Spark
    spark = crear_sesion_spark()
    print("Spark iniciado correctamente")
    print()

    # Cargamos y limpiamos el dataset
    df_crudo  = cargar_dataset(spark, RUTA_DATASET)
    df_limpio = limpiar_datos(df_crudo)
    print()

    # Calculamos las 5 agregaciones
    print("Generando agregaciones...")
    agg_aerolineas = agregar_por_aerolinea(df_limpio)
    agg_rutas      = agregar_por_ruta(df_limpio)
    agg_horario    = agregar_por_hora(df_limpio)
    agg_mensual    = agregar_mensual(df_limpio)
    agg_estado     = agregar_por_aeropuerto(df_limpio)
    print()

    # Guardamos los resultados como CSV
    print("Guardando archivos CSV...")
    guardar_csv(agg_aerolineas, "data/agg_aerolineas.csv")
    guardar_csv(agg_rutas,      "data/agg_rutas.csv")
    guardar_csv(agg_horario,    "data/agg_horario.csv")
    guardar_csv(agg_mensual,    "data/agg_mensual.csv")
    guardar_csv(agg_estado,     "data/agg_estado.csv")

    print()
    print("Procesamiento completado.")
    print("Ya puedes ejecutar:")
    print("  python reporte.py      (genera el reporte analitico con GPT-4)")
    print("  python agente.py       (chatbot interactivo)")
    print("  streamlit run app.py   (dashboard web)")

    spark.stop()
    # Cerramos la sesion de Spark al finalizar


# ------------------------------------------------------------
# PUNTO DE ENTRADA
# ------------------------------------------------------------

if __name__ == "__main__":
    # Este bloque solo se ejecuta cuando corres el archivo directamente
    # No se ejecuta si otro archivo importa este modulo
    main()
