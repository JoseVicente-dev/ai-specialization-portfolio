# Visualización y Big Data

Análisis exploratorio orientado a negocio, procesamiento distribuido con Apache Spark y un agente de analítica que combina PySpark, function calling con GPT-4o y un dashboard en Streamlit.

> 🇬🇧 Exploratory analysis for business insight, distributed processing with Apache Spark, and an analytics agent that combines PySpark, GPT-4o function calling and a Streamlit dashboard.

| Libreta | Contenido | Herramientas | |
|---|---|---|---|
| [`01_eda_comportamiento_consumidor.ipynb`](01_eda_comportamiento_consumidor.ipynb) | EDA de ventas y comportamiento del consumidor: limpieza, outliers, visualizaciones e insights de negocio. | Pandas, Seaborn | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JoseVicente-dev/ai-specialization-portfolio/blob/main/05-visualizacion-big-data/01_eda_comportamiento_consumidor.ipynb) |
| [`02_procesamiento_distribuido_spark.ipynb`](02_procesamiento_distribuido_spark.ipynb) | Calidad de datos, latencias y compras atípicas, y agregaciones de negocio sobre logs de e-commerce. | PySpark | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JoseVicente-dev/ai-specialization-portfolio/blob/main/05-visualizacion-big-data/02_procesamiento_distribuido_spark.ipynb) |
| [`03_dashboard_power_bi_online_retail.pbix`](03_dashboard_power_bi_online_retail.pbix) | Dashboard de ventas en Power BI sobre el dataset *Online Retail II*. GitHub no lo previsualiza: descárgalo y ábrelo con Power BI Desktop. | Power BI |  |

## Proyecto: agente de analítica de vuelos

[`agente-analitica-vuelos/`](agente-analitica-vuelos/): pipeline PySpark sobre 5,8 millones de vuelos, agente con GPT-4o y siete herramientas, reporte automático y dashboard en Streamlit.

## Datos

- `data/dataset_ventas.csv` viene incluido (libreta 01).
- La libreta 02 usa `big_data_ecommerce_logs.csv` (68 MB, material del curso, no incluido).

[← Volver al inicio](../README.md)
