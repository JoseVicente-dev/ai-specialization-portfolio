# Procesamiento de Lenguaje Natural (Electiva 2)

NLP desde embeddings hasta un agente con LLM: recomendador de sinónimos con GloVe y WordNet, análisis de sentimientos y POS tagging, y un agente de RRHH con RAG construido en n8n.

> 🇬🇧 NLP from word embeddings to an LLM agent: synonym recommender with GloVe and WordNet, sentiment analysis and POS tagging, and a RAG-based HR agent built in n8n.

| Libreta | Contenido | Herramientas | |
|---|---|---|---|
| [`01_recomendador_sinonimos_glove_wordnet.ipynb`](01_recomendador_sinonimos_glove_wordnet.ipynb) | Recomendador de sinónimos y palabras relacionadas con vectores GloVe y con WordNet, y comparación de ambos enfoques. | gensim, NLTK | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JoseVicente-dev/ai-specialization-portfolio/blob/main/04-procesamiento-lenguaje-natural/01_recomendador_sinonimos_glove_wordnet.ipynb) |
| [`02_sentimientos_y_pos_tagging.ipynb`](02_sentimientos_y_pos_tagging.ipynb) | Analizador de sentimientos con TextBlob y etiquetado gramatical (POS) con spaCy. | TextBlob, spaCy, NLTK | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JoseVicente-dev/ai-specialization-portfolio/blob/main/04-procesamiento-lenguaje-natural/02_sentimientos_y_pos_tagging.ipynb) |

## Proyecto final

[`proyecto-final-agente-rrhh/`](proyecto-final-agente-rrhh/): agente conversacional de Recursos Humanos sobre Telegram, con RAG, herramientas de Google Sheets y Calendar, y aprobación humana por correo.

## Material de clase

[`material-de-clase/nlp_evolucion_de_tecnicas.ipynb`](material-de-clase/nlp_evolucion_de_tecnicas.ipynb) es la libreta guía del curso, elaborada por el equipo docente de la UAM; no es trabajo mío. La incluyo como referencia porque recorre en un solo lugar análisis de sentimientos, categorización de texto, POS tagging, NER, traducción, clasificación y generación de texto, desde métodos clásicos hasta Transformers.

## Datos

- La libreta 01 necesita [`glove.6B.100d.txt`](https://nlp.stanford.edu/projects/glove/) (331 MB, no incluido).

[← Volver al inicio](../README.md)
