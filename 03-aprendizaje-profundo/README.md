# Aprendizaje Profundo (Electiva 1)

Deep learning con TensorFlow/Keras: perceptrones y MLP, CNN y transfer learning, RNN vs LSTM para texto, y mecanismos de atención.

> 🇬🇧 Deep learning with TensorFlow/Keras: perceptrons and MLPs, CNNs and transfer learning, RNN vs LSTM for text, and attention mechanisms.

| Libreta | Contenido | Herramientas | |
|---|---|---|---|
| [`01_comparacion_clasificadores_pca_diabetes.ipynb`](01_comparacion_clasificadores_pca_diabetes.ipynb) | Línea base antes de las redes profundas: siete clasificadores (árbol, MLP, KNN, SGD, Extra Trees, Random Forest, Gradient Boosting) sobre diabetes, con y sin StandardScaler y PCA. | scikit-learn | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JoseVicente-dev/ai-specialization-portfolio/blob/main/03-aprendizaje-profundo/01_comparacion_clasificadores_pca_diabetes.ipynb) |
| [`02_perceptron_mlp_tensorflow.ipynb`](02_perceptron_mlp_tensorflow.ipynb) | Perceptrón para la función AND, MLP para MNIST, regularización L2 y Dropout, y clasificación de texto con IMDB. | TensorFlow/Keras | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JoseVicente-dev/ai-specialization-portfolio/blob/main/03-aprendizaje-profundo/02_perceptron_mlp_tensorflow.ipynb) |
| [`03_redes_convolucionales_cnn.ipynb`](03_redes_convolucionales_cnn.ipynb) | Operación de convolución y transfer learning con VGG16, InceptionV3 y MobileNetV2 para clasificar perros y gatos. | TensorFlow/Keras | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JoseVicente-dev/ai-specialization-portfolio/blob/main/03-aprendizaje-profundo/03_redes_convolucionales_cnn.ipynb) |
| [`04_rnn_vs_lstm_emociones.ipynb`](04_rnn_vs_lstm_emociones.ipynb) | SimpleRNN frente a LSTM para clasificar seis emociones en texto (`dair-ai/emotion`), con informe comparativo y limitaciones. | TensorFlow/Keras, Hugging Face Datasets | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JoseVicente-dev/ai-specialization-portfolio/blob/main/03-aprendizaje-profundo/04_rnn_vs_lstm_emociones.ipynb) |
| [`05_mecanismos_de_atencion_se_cnn.ipynb`](05_mecanismos_de_atencion_se_cnn.ipynb) | CNN base frente a variantes con atención (Squeeze-and-Excitation, MultiHeadAttention) sobre *Flower Photos*; reporte del impacto de la atención. | TensorFlow/Keras | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JoseVicente-dev/ai-specialization-portfolio/blob/main/03-aprendizaje-profundo/05_mecanismos_de_atencion_se_cnn.ipynb) |

## Redes generativas (material adaptado)

Las tres libretas de [`gan/`](gan/) son material del curso, adaptado al español a partir de los tutoriales de [Naoki Shibuya](https://github.com/naokishibuya/deep-learning) y de los ejemplos de Udacity que cada una cita en sus referencias. No son trabajo original mío; las incluyo por la experimentación que hice sobre ellas.

| Libreta | Contenido |
|---|---|
| [`gan_mnist.ipynb`](gan/gan_mnist.ipynb) | GAN con redes densas para generar dígitos de MNIST. |
| [`dcgan_mnist.ipynb`](gan/dcgan_mnist.ipynb) | DCGAN con la arquitectura original del tutorial. |
| [`dcgan_mnist_v2.ipynb`](gan/dcgan_mnist_v2.ipynb) | Mi variante: más filtros en generador y discriminador, Dropout en el discriminador y nuevos hiperparámetros de Adam y LeakyReLU. |

## Datos

- MNIST, IMDB, `dair-ai/emotion` y *Flower Photos* se descargan desde la propia libreta.
- La libreta 01 usa `diabetes.csv` y la 03 un conjunto pequeño de imágenes de perros y gatos; ninguno está incluido.

[← Volver al inicio](../README.md)
