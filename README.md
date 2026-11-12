# Especialización en Inteligencia Artificial · Portafolio

🇪🇸 Español · [🇬🇧 English](README.en.md)

Libretas y proyectos que desarrollé durante la **Especialización en Inteligencia Artificial** de la **Universidad Autónoma de Manizales (UAM)**, Colombia, entre 2025 y 2026. El recorrido va desde analítica de datos con Python y SQL hasta agentes con LLM, pasando por machine learning clásico, deep learning, NLP y procesamiento distribuido con Spark.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?logo=jupyter&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?logo=tensorflow&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?logo=apachespark&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-EA4B71?logo=n8n&logoColor=white)

## Proyectos destacados

| Proyecto | Qué hace | Tecnologías |
|---|---|---|
| [Agente de analítica de vuelos](05-visualizacion-big-data/agente-analitica-vuelos/) | Procesa 5,8 millones de vuelos con PySpark y los expone a un agente GPT-4o con siete herramientas, un generador de reportes y un dashboard interactivo. | PySpark, OpenAI function calling, Streamlit, Plotly |
| [Agente de RRHH con RAG](04-procesamiento-lenguaje-natural/proyecto-final-agente-rrhh/) | Asistente en Telegram que responde políticas internas con RAG, gestiona vacaciones en Google Sheets, pide aprobación humana por correo y agenda citas. | n8n, OpenAI, RAG, Google Workspace |
| [Predicción de emisiones de CO y NOx](02-aprendizaje-automatico/05_proyecto_final_emisiones_turbinas_gas.ipynb) | Modelos de regresión regularizada para estimar emisiones de turbinas de gas, comparados con resultados publicados. | scikit-learn, GridSearchCV |
| [Mecanismos de atención en visión](03-aprendizaje-profundo/05_mecanismos_de_atencion_se_cnn.ipynb) | Compara una CNN base con variantes que incorporan atención sobre un dataset de flores. | TensorFlow/Keras |
| [RNN vs LSTM para emociones en texto](03-aprendizaje-profundo/04_rnn_vs_lstm_emociones.ipynb) | Clasifica seis emociones y analiza por qué la memoria de largo plazo cambia el resultado. | TensorFlow/Keras, Hugging Face Datasets |

## Contenido por curso

| # | Curso | Temas | Libretas |
|---|---|---|---|
| 01 | [Programación para Analítica de Datos](01-analitica-de-datos/) | Python, Pandas, SQL/SQLite, limpieza de datos, EDA | 5 + 3 de notas |
| 02 | [Aprendizaje Automático](02-aprendizaje-automatico/) | Regresión, clasificación, redes neuronales, clustering, PCA | 5 |
| 03 | [Aprendizaje Profundo](03-aprendizaje-profundo/) | MLP, CNN, transfer learning, RNN/LSTM, atención | 5 |
| 04 | [Procesamiento de Lenguaje Natural](04-procesamiento-lenguaje-natural/) | Embeddings, WordNet, sentimientos, POS tagging, RAG y agentes | 2 + proyecto |
| 05 | [Visualización y Big Data](05-visualizacion-big-data/) | EDA de negocio, Apache Spark, agentes de analítica, dashboards | 2 + proyecto |
| 06 | [Matemáticas para IA](06-matematicas-para-ia/) | Álgebra lineal, probabilidad, variables aleatorias | 4 |

Cada carpeta tiene su propio README con la descripción de cada libreta, las herramientas usadas y un botón para abrirla en Google Colab.

### Otros cursos del programa

- **Computación en la Nube.** El trabajo vive en repositorios aparte: sistema de inventarios ([backend](https://github.com/JoseVicente-dev/inventory-be), [frontend](https://github.com/JoseVicente-dev/inventory-fe)) y sistema de coworking ([backend](https://github.com/JoseVicente-dev/coworking-system-be), [frontend](https://github.com/JoseVicente-dev/coworking-system-fe)), desplegados con contenedores en la nube.
- **Gestión de Proyectos de IA.** CRISP-DM, ML Canvas y MLOps; los entregables fueron documentos y tableros, no código.

## Cómo ejecutar las libretas

La mayoría se escribió en Google Colab, así que la forma más rápida es el botón **Open in Colab** de cada README.

Para ejecutarlas en local:

```bash
git clone https://github.com/JoseVicente-dev/ai-specialization-portfolio.git
cd ai-specialization-portfolio
python -m venv .venv
.venv\Scripts\activate          # Windows; en Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Algunas libretas montan Google Drive o leen archivos de `/content/`; en local hay que ajustar esa ruta al lugar donde esté el dataset.

## Sobre los datos

El repositorio solo incluye datasets pequeños. Los grandes (Airbnb, GloVe, vuelos de EE. UU., logs de e-commerce) se omiten por tamaño; el README de cada curso indica de dónde obtenerlos. Varias libretas descargan sus datos directamente desde UCI, scikit-learn o Hugging Face.

## Sobre la autoría

Las libretas son mis soluciones a las actividades del programa. Los enunciados, que aparecen como texto dentro de varias de ellas, son de los docentes de la UAM. En algunos trabajos usé asistentes de IA (Gemini en Colab, Claude Code) como apoyo; donde influyó en el resultado, la libreta lo indica.

## Contacto

**Jose Vicente Velasco** · [GitHub](https://github.com/JoseVicente-dev)

## Licencia

El código se publica bajo licencia [MIT](LICENSE). Los datasets pertenecen a sus respectivos autores.
