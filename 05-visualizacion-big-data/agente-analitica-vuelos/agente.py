# ============================================================
# agente.py
# Chatbot CLI de analisis de retrasos de vuelos EE.UU.
# Usa GPT-4o para razonar y las herramientas de tools.py para obtener datos
#
# Requiere: archivos CSV en data/ (ejecutar procesar.py primero)
#           archivo .env con OPENAI_API_KEY=sk-...
# Ejecucion: python agente.py
# ============================================================

import os
import sys
import json

# Cargamos las variables del archivo .env (donde esta la API key)
from dotenv import load_dotenv
load_dotenv()
# load_dotenv() busca un archivo llamado .env en el directorio actual
# y carga sus variables como variables de entorno del sistema

from openai import OpenAI

# Importamos las herramientas y sus descripciones desde tools.py
from tools import HERRAMIENTAS, DESCRIPCION_HERRAMIENTAS

# ------------------------------------------------------------
# CONFIGURACION
# ------------------------------------------------------------

MODELO = "gpt-4o"
# gpt-4o es el modelo GPT-4 mas reciente y eficiente de OpenAI
# Cambiar a "gpt-4o-mini" para reducir costos durante desarrollo

MAX_PASOS = 10
# Limite de iteraciones del agente por pregunta
# Evita loops infinitos si el modelo entra en un ciclo de herramientas

INSTRUCCIONES = (
    "Eres un analista de datos experto en aviacion de EE.UU. "
    "Tienes acceso a estadisticas reales del dataset de retrasos de vuelos de Kaggle "
    "(fuente: Bureau of Transportation Statistics). "
    "Usa siempre las herramientas disponibles para dar datos concretos y precisos. "
    "Cuando el usuario pregunte por aerolineas, usa sus codigos IATA (AA, DL, WN, UA, etc.). "
    "Responde en espanol, de forma clara, organizada y con numeros especificos."
)

# Creamos el cliente de OpenAI
# Lee automaticamente OPENAI_API_KEY del entorno cargado por load_dotenv()
cliente = OpenAI()

# ------------------------------------------------------------
# VERIFICAR QUE LOS DATOS EXISTEN
# ------------------------------------------------------------

if not os.path.exists("data/agg_aerolineas.csv"):
    print("ERROR: No se encontraron los datos procesados.")
    print("Ejecuta primero: python procesar.py")
    sys.exit(1)
    # sys.exit(1) cierra el programa con codigo de error

# ------------------------------------------------------------
# INICIO DEL PROGRAMA
# ------------------------------------------------------------

print("=" * 55)
print("  Agente de Analisis de Vuelos — EE.UU.")
print("  Modelo: " + MODELO)
print("  Escribe 'salir' para terminar")
print("=" * 55)
print()
print("Comandos utiles:")
print("  'resumen'  → estadisticas generales del dataset")
print("  'ranking'  → ranking de aerolineas por puntualidad")
print("  'salir'    → termina el programa")
print()

# Lista que guarda todo el historial de la conversacion
# El agente necesita el historial para recordar lo que se dijo antes
historial = []

# ------------------------------------------------------------
# LOOP PRINCIPAL: CONVERSACION CON EL USUARIO
# ------------------------------------------------------------

while True:
    print()
    pregunta = input("Tu: ").strip()
    # .strip() elimina espacios al inicio y al final

    if pregunta.lower() in ["salir", "exit", "quit", ""]:
        print("Hasta luego!")
        break
    # break → sale del while True y termina el programa

    # Guardamos la pregunta en el historial
    historial.append({
        "role":    "user",
        "content": pregunta
    })

    print("Agente pensando...", end=" ", flush=True)
    # end=" " evita el salto de linea
    # flush=True muestra el texto inmediatamente

    # --------------------------------------------------------
    # LOOP DEL AGENTE: RAZONAR Y USAR HERRAMIENTAS
    # --------------------------------------------------------
    # El agente puede necesitar varios pasos para responder
    # Ejemplo: primero obtiene datos generales, luego compara aerolineas

    for paso in range(MAX_PASOS):

        # Construimos los mensajes para enviar a OpenAI
        # Incluye el system prompt mas todo el historial
        mensajes = [{"role": "system", "content": INSTRUCCIONES}] + historial

        # Llamamos a la API de OpenAI
        respuesta_api = cliente.chat.completions.create(
            model=MODELO,
            messages=mensajes,
            tools=DESCRIPCION_HERRAMIENTAS,
            # tools le dice al modelo que herramientas puede llamar
            tool_choice="auto",
            # auto → el modelo decide si usar herramienta o responder directamente
            temperature=0,
            # 0 → respuestas consistentes y precisas (sin aleatoriedad)
        )

        # Extraemos el mensaje del modelo
        mensaje_modelo = respuesta_api.choices[0].message
        # .choices[0] → primer (y unico) candidato de respuesta

        # Agregamos la respuesta al historial
        historial.append(mensaje_modelo)

        # ---- El modelo quiere usar una herramienta ----
        if mensaje_modelo.tool_calls:
            # tool_calls es una lista: el modelo puede pedir varias herramientas a la vez

            for llamada in mensaje_modelo.tool_calls:
                nombre = llamada.function.name
                # Nombre de la herramienta que el modelo quiere ejecutar

                argumentos = json.loads(llamada.function.arguments)
                # Los argumentos vienen como JSON en texto; json.loads los convierte a dict

                print(f"\n  [Usando: {nombre}]", end=" ", flush=True)

                # Ejecutamos la herramienta
                herramienta = HERRAMIENTAS[nombre]
                # Buscamos la funcion en el diccionario HERRAMIENTAS de tools.py

                try:
                    resultado = herramienta(**argumentos)
                    # **argumentos desempaqueta el dict como argumentos de la funcion
                except Exception as error:
                    resultado = "Error al ejecutar la herramienta: " + str(error)

                # Devolvemos el resultado al modelo para que continue su razonamiento
                historial.append({
                    "role":         "tool",
                    # role="tool" indica que este mensaje es el resultado de una herramienta
                    "tool_call_id": llamada.id,
                    # tool_call_id vincula este resultado con la herramienta que lo genero
                    "content":      str(resultado)
                })

        # ---- El modelo tiene la respuesta final ----
        else:
            # Si no hay tool_calls, el modelo ya tiene suficiente informacion
            respuesta_final = mensaje_modelo.content

            print()  # salto de linea
            print()
            print("Agente:", respuesta_final)
            break
            # Salimos del for y esperamos la siguiente pregunta del usuario

    else:
        # Este else del for se ejecuta si el for termino sin break
        # Es decir, se agotaron los MAX_PASOS sin llegar a una respuesta final
        print()
        print("Agente: Alcance el limite de pasos. Por favor reformula tu pregunta.")
