# EXAMEN TEÓRICO — PERCEPTRÓN, MLP Y CNN (GRUPO A)

**Eduardo Alcaraz**

## 1. Datos del alumno

| Campo  | Valor |
|---|----|
| Nombre | Juan Manuel Vera Miranda|
| Grupo  | A |
| Fecha  | 03 de Noviembre de 2026|

## Pregunta 1 — Idea del perceptrón

1. Explica qué recibe un perceptrón, qué hace con los pesos y el bias, y qué produce.
> Un perceptron recibe un vector con las caracteristicas y la etiqueta correspondiente a una entrada de datos, los pesos y el bias se ajustan durante el entrenamiento a través del backpropagation para conseguir los mejores valores que permitan clasificar y predecir futuras entradas.
2. ¿Qué quiere decir que dos clases sean *linealmente separables*?
>Significa que los datos estan separados de forma que con una linea recta se puede delimitar la frontera entre dos conjuntos de datos de dos distintas clases.
3. Señala *una* limitación fuerte del perceptrón de una sola capa.
>No pueden resolver problemas que no son linealmente separables. 

## Pregunta 2 — Por qué aparece el MLP

1. ¿En qué sentido un MLP es “más de una capa de neuronas”?
>Porque el nombre hace referencia a que es un perceptron que se compone de un conjunto de neuronas.
2. ¿Para qué sirve la capa oculta?
>Para ajustar los pesos y el bias del modelo.
3. Si quitas todas las activaciones no lineales, ¿qué tipo de comportamiento te queda y por qué importa?
>Queda un comportamiento en que todas las capas terminan sumandose como una tranformación linea. Se pierde la capacidad de resolver problemas con fronteras curvas.


## Pregunta 3 — XOR como lección histórica

1. ¿Qué enseña el ejemplo XOR sobre el perceptrón simple?
>El XOR no es linealmente separable, por lo que un solo perceptrón no puede resolverlo.
2. ¿Qué cambia al pasar a una red con capas ocultas y no linealidad?
> Se pueden separar correctamente dos datos de las dos clases.
3. ¿Eso significa que el perceptrón nunca sirve en problemas reales? Argumenta.
> No, sigue siendo util para resolver problemas donde los datos son linealmente separables.


## Pregunta 4 — Cómo “aprende” la red

1. Describe con palabras el ciclo: predicción → medir error → ajustar pesos.
> En la predicción se pasan las entradas a través de la red para obtener un valor final que correspode a la predicción del modelo. Se mide el error al comparar el valor que pudo predecir el modelo con el valor real con el que fueron etiquetadas esas caracteristicas. En este caso se pueden usar distintas funciones para calcular el loss que son optimas para distintos tipos de problemas. Despues utilizando el error el modelo ajusta sus propios pesos y bias para lograr que la predicción sea cercana a el valor esperado.
2. ¿Qué controla el *learning rate* (tasa de aprendizaje) a nivel conceptual?
> El learning rate es un valor que indica que tanto deben ajustarse los pesos. Es como una perilla que ajusta la sensibilidad del ajuste. Valores más altos mueven más los pesos en la dirección a donde se disminuye el error, valores más pequeños hacen saltos más cortos.
3. Diferencia *subajuste* y *sobreajuste* con un ejemplo escolar breve.
> El subajuste es cuando el modelo no es capaz de predecir correctamente entradas nuevas por falta de entrenamiento o carencia de valores de referencia. El sobreajuste es cuando el modelo aprende de los ejemplos proporcionados y se vuelve experto en predecirlos pero no en generalizar datos nuevos.


## Pregunta 5 — Salidas: sigmoide y softmax

1. ¿Cuándo usarías sigmoide y cuándo softmax?
> Sigmode en clasificaciones binarias y softmax en clasificaciones multiclase.
2. ¿Qué significa el vector que sale de un softmax en un problema de varias clases?
> Las probabilidades en escala de 0-1 de la clasificación en cada clase.
3. Pon un ejemplo del curso (juego, riesgo, imágenes, etc.) y di qué salida encajaría.
> Para el ejemplode la clasificación de imagenes con la CNN se utilizaría una capa de salida con activación softmax para permitirnos obtener las probabilidades de que la clasificación entre clases.

## Pregunta 6 — Motivación de la CNN

1. ¿Qué inconveniente conceptual tiene aplastar una imagen y meterla a un MLP denso?
2. ¿Qué aporta la idea de *filtro local* y *pesos compartidos*?
3. Menciona *dos* dominios (además de fotos cotidianas) donde una CNN tiene sentido.

### Respuesta

_Respuesta:_

## Pregunta 7 — Piezas de una CNN

Explica el *para qué* de:

1. Convolución
2. Pooling
3. Flatten + Dense al final
4. Dropout durante el entrenamiento

### Respuesta

_Respuesta:_

## Pregunta 8 — Capas bajas vs capas altas

1. ¿Qué suelen captar las primeras capas de una CNN frente a las más profundas?
2. Usa una analogía (lupas, detectores, “de simple a complejo”).
3. ¿Por qué “poner más capas” no garantiza mejor modelo?

### Respuesta

_Respuesta:_

## Pregunta 9 — Análisis: elige arquitectura

Elige **Perceptrón (o lineal simple) / MLP / CNN** y justifica en *una* frase:

1. Tabla de alumnos: promedio, faltas, horas de estudio → ¿aprueba?
2. Clasificar el color de un semáforo en una fotografía.
3. Clases en el plano que *no* se separan con una recta.
4. ¿Usarías CNN para autocompletar código o una secuencia larga de texto? ¿Sí/no y qué alternativa del curso mencionarías?

### Respuesta

_Respuesta:_

## Pregunta 10 — Análisis: mirada de proyecto

1. Train accuracy altísima y validation baja: ¿qué sospechas? ¿Qué dos preguntas le harías al equipo en la defensa?
2. ¿Por qué más neuronas o más capas no sustituyen un buen planteamiento del problema y buenos datos?
3. Escribe *tres* preguntas orales (tuyas) para verificar que distinguen perceptrón, MLP y CNN.

### Respuesta

_Respuesta:_