# AI Specialization · Portfolio

[🇪🇸 Español](README.md) · 🇬🇧 English

Notebooks and projects I built during the **Specialization in Artificial Intelligence** (a postgraduate program) at **Universidad Autónoma de Manizales (UAM)**, Colombia, between 2025 and 2026. The path goes from data analytics with Python and SQL to LLM agents, through classical machine learning, deep learning, NLP and distributed processing with Spark.

The notebooks are written in Spanish, the language of the program. This page summarizes what each one covers.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?logo=jupyter&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?logo=tensorflow&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?logo=apachespark&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-EA4B71?logo=n8n&logoColor=white)

## Featured projects

| Project | What it does | Stack |
|---|---|---|
| [Flight analytics agent](05-visualizacion-big-data/agente-analitica-vuelos/) | Processes 5.8 million flights with PySpark and exposes them to a GPT-4o agent with seven tools, a report generator and an interactive dashboard. | PySpark, OpenAI function calling, Streamlit, Plotly |
| [HR agent with RAG](04-procesamiento-lenguaje-natural/proyecto-final-agente-rrhh/) | Telegram assistant that answers internal policy questions with RAG, manages vacation requests in Google Sheets, asks for human approval by email and books meetings. | n8n, OpenAI, RAG, Google Workspace |
| [CO and NOx emission prediction](02-aprendizaje-automatico/05_proyecto_final_emisiones_turbinas_gas.ipynb) | Regularized regression models that estimate gas turbine emissions, compared against published results. | scikit-learn, GridSearchCV |
| [Attention mechanisms in vision](03-aprendizaje-profundo/05_mecanismos_de_atencion_se_cnn.ipynb) | Compares a baseline CNN with attention-based variants on a flower image dataset. | TensorFlow/Keras |
| [RNN vs LSTM for emotion in text](03-aprendizaje-profundo/04_rnn_vs_lstm_emociones.ipynb) | Classifies six emotions and analyzes why long-term memory changes the outcome. | TensorFlow/Keras, Hugging Face Datasets |

## Contents by course

| # | Course | Topics | Notebooks |
|---|---|---|---|
| 01 | [Programming for Data Analytics](01-analitica-de-datos/) | Python, Pandas, SQL/SQLite, data cleaning, EDA | 5 + 3 study notes |
| 02 | [Machine Learning](02-aprendizaje-automatico/) | Regression, classification, neural networks, clustering, PCA | 5 |
| 03 | [Deep Learning](03-aprendizaje-profundo/) | MLP, CNN, transfer learning, RNN/LSTM, attention, GANs | 5 + 3 on GANs |
| 04 | [Natural Language Processing](04-procesamiento-lenguaje-natural/) | Embeddings, WordNet, sentiment analysis, POS tagging, RAG and agents | 2 + project + class material |
| 05 | [Visualization and Big Data](05-visualizacion-big-data/) | Business EDA, Apache Spark, Power BI, analytics agents | 2 + dashboard + project |
| 06 | [Mathematics for AI](06-matematicas-para-ia/) | Linear algebra, probability, random variables | 4 |

Each folder has its own README describing every notebook, the tools used, and a button to open it in Google Colab.

### Other courses in the program

- **Cloud Computing.** The work lives in separate repositories: an inventory system ([backend](https://github.com/JoseVicente-dev/inventory-be), [frontend](https://github.com/JoseVicente-dev/inventory-fe)) and a coworking system ([backend](https://github.com/JoseVicente-dev/coworking-system-be), [frontend](https://github.com/JoseVicente-dev/coworking-system-fe)), deployed with containers in the cloud.
- **AI Project Management.** CRISP-DM, ML Canvas and MLOps; the deliverables were documents and boards, not code.

## Running the notebooks

Most were written in Google Colab, so the quickest way is the **Open in Colab** button in each README.

To run them locally:

```bash
git clone https://github.com/JoseVicente-dev/ai-specialization-portfolio.git
cd ai-specialization-portfolio
python -m venv .venv
.venv\Scripts\activate          # Windows; on Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Some notebooks mount Google Drive or read files from `/content/`; locally, point that path to wherever the dataset is.

## About the data

Only small datasets are included. Large ones (Airbnb, GloVe, US flights, e-commerce logs) are left out because of their size; each course README says where to get them. Several notebooks download their data directly from UCI, scikit-learn or Hugging Face.

## About authorship

The notebooks are my solutions to the program's assignments. The assignment statements, which appear as text inside several of them, belong to the UAM instructors. Two items are not mine and are labeled as such, with attribution inside each notebook: the three GAN notebooks, adapted from third-party tutorials, and the NLP course guide notebook. In some assignments I used AI assistants (Gemini in Colab, Claude Code) for support; where that shaped the result, the notebook says so.

## Contact

**José Vicente Velasco López** · [GitHub](https://github.com/JoseVicente-dev)

## License

Code is released under the [MIT](LICENSE) license. Datasets belong to their respective authors.
