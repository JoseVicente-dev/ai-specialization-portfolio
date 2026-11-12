# Agente de analítica de vuelos

Sistema de analítica de retrasos de vuelos domésticos de EE. UU. Un pipeline en PySpark resume 5,8 millones de vuelos en tablas agregadas, y un agente con GPT-4o responde preguntas sobre ellas usando herramientas (function calling). Incluye un chatbot de consola, un generador de reportes y un dashboard web.

> 🇬🇧 Flight delay analytics system. A PySpark pipeline condenses 5.8 million US domestic flights into aggregate tables, and a GPT-4o agent answers questions about them through function calling. Ships with a CLI chatbot, an automated report generator and a Streamlit dashboard.

## Cómo funciona

```
flights.csv (Kaggle, 565 MB)
      │  procesar.py  (PySpark)
      ▼
data/agg_*.csv  ──►  tools.py  (7 herramientas sobre pandas)
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   agente.py         reporte.py         app.py
   chatbot CLI       reporte en         dashboard Streamlit
                     Markdown           + chat con el agente
```

| Archivo | Función |
|---|---|
| `procesar.py` | Lee el CSV crudo con PySpark y genera cinco tablas agregadas: aerolíneas, estados, franjas horarias, meses y rutas. |
| `tools.py` | Define las siete herramientas del agente: estadísticas por aerolínea, comparación de aerolíneas, top de rutas, análisis horario, evolución mensual, resumen general y análisis por aeropuerto. |
| `agente.py` | Chatbot de consola: GPT-4o decide qué herramienta llamar y redacta la respuesta con los datos devueltos. |
| `reporte.py` | Envía las tablas a GPT-4o y guarda un reporte analítico en `data/reporte_final.md`. |
| `app.py` | Dashboard con gráficos Plotly y chat integrado con el agente. |

Las tablas agregadas y un [reporte de ejemplo](data/reporte_final.md) están incluidos, así que el agente y el dashboard funcionan sin descargar el dataset completo.

## Ejecución

```bash
python -m venv venv
venv\Scripts\activate            # Windows; en Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env           # y agrega tu OPENAI_API_KEY

python agente.py                 # chatbot en consola
streamlit run app.py             # dashboard
python reporte.py                # regenerar el reporte
```

Para regenerar las tablas desde cero, descarga [2015 Flight Delays and Cancellations](https://www.kaggle.com/datasets/usdot/flight-delays) de Kaggle, coloca `flights.csv` en `data/` y ejecuta `python procesar.py` (requiere Java para Spark).

[← Volver a Visualización y Big Data](../README.md)
