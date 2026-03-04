## **¿Qué es el Análisis Exploratorio de Datos (EDA) en Inteligencia Artificial (IA)?**

## El Análisis Exploratorio de Datos (EDA, por sus siglas en inglés, *Exploratory Data Analysis*) es un paso crítico y fundamental en el flujo de trabajo de la IA y el Machine Learning. Consiste en la aplicación de técnicas estadísticas y visuales para resumir, caracterizar y comprender las principales propiedades de un conjunto de datos.

## **Objetivo Principal**

## El objetivo del EDA no es probar hipótesis, sino descubrir patrones, detectar anomalías (outliers), probar supuestos y verificar las relaciones entre las variables *antes* de aplicar modelos predictivos. Esto asegura que el científico de datos o ingeniero de Machine Learning tenga una comprensión profunda de los datos con los que está trabajando, lo que lleva a una mejor selección de modelos, mejor ingeniería de características (*feature engineering*) y, en última instancia, modelos de IA más robustos y precisos.

## **Proceso del EDA**

| Etapa del EDA | Descripción | Ejemplo en el Contexto del Esquive |
| ----- | ----- | ----- |
| **Resumen Descriptivo** | Obtener estadísticas básicas (media, mediana, desviación estándar, distribución). | Verificar el rango de **velocidad\_proyectil** o la distribución de **distancia\_x**. |
| **Identificación de Calidad** | Detectar valores faltantes, formatos incorrectos o duplicados. | Asegurar que no haya registros donde **velocidad\_proyectil** sea cero o nulo, lo cual distorsionaba el TTI. |
| **Análisis de Distribución** | Visualizar la forma en que se distribuyen las variables (histogramas, box plots). | Observar si la **distancia\_x** para los saltos exitosos sigue una distribución normal o está sesgada. |
| **Detección de Outliers** | Identificar puntos de datos que se desvían significativamente del resto. | Encontrar proyectiles con una **velocidad\_proyectil** extremadamente alta que el motor de física no puede manejar. |
| **Análisis de Correlación** | Medir la relación estadística entre pares de variables. | Confirmar la correlación negativa entre **velocidad\_proyectil** y la **distancia\_x** necesaria para el salto. |

## 

## **1\. Identificación de Variables (Features)**

Para que la IA esquive con éxito, los datos deben capturar la relación espacio-temporal entre el proyectil y el personaje.

| Variable | Descripción | Relevancia |
| :---- | :---- | :---- |
| **distancia\_x** | Distancia horizontal entre el proyectil y el personaje. | Principal indicador de proximidad. |
| **velocidad\_proyectil** | Píxeles por frame del ataque alienígena. | Determina el "Tiempo de Impacto" (TTI). |
| **altura\_personaje** | Posición en el eje Y del personaje. | Verifica si el personaje ya está en el aire o en el suelo. |
| **ancho\_proyectil** | Tamaño horizontal del objeto atacante. | Define la ventana de error para el salto. |
| **estado\_salto** | Booleano (0: Suelo, 1: Aire). | Evita comandos de salto redundantes. |

## **2\. Análisis de Distribución y Correlación**

### **Ventana de Salto Crítica**

El análisis de los datos históricos muestra que el éxito del esquive no depende solo de la distancia, sino del **Tiempo al Impacto (TTI)**:

TTI \= **distancia\_x****velocidad\_proyectil**

* **Zona de Éxito:** TTI entre 0.15s y 0.30s.  
* **Zona de Fallo (Tarde):** TTI\<0.10s (el colisionador golpea antes de alcanzar la altura máxima).  
* **Zona de Fallo (Temprano):** TTI\>0.40s (el personaje cae antes de que pase el proyectil).

### **Correlación de Variables**

* **velocidad\_proyectil vs distancia\_x:** Existe una correlación negativa fuerte. A mayor velocidad, la IA debe reaccionar a una distancia\_x mayor para mantener el TTI constante.

## **3\. Visualización de Datos Relevantes**

* **Outliers:** Proyectiles con velocidad excesiva que superan la capacidad de respuesta del motor de física (frames de salto \< frames de colisión).  
* **Balance de Clases:** En los datos de entrenamiento, se debe asegurar una proporción 50/50 entre "Salto Exitoso" y "Colisión" para evitar sesgos de pasividad en la IA.