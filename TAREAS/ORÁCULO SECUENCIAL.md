

# ACTIVIDAD 2: EL ENIGMA DEL ORÁCULO SECUENCIAL

## ANATOMÍA DE UNA VANILLA RNN

**Profesor:Eduardo Alcaraz**

---

## Table of Contents

```
1. El Acertijo: El Guardián del Tiempo
2. Actividades de Comprensión (Para el Alumno)
3. Actividad 2.1: Mapeo de Variables
4. Actividad 2.2: El Análisis de Dimensionalidad (El tamaño de los peajes)
5. Actividad 2.3: La Estrofa Perdida (Pensamiento Lateral)
6. Actividad 2.4: El Límite del Muro Curvo (Análisis de Saturación)
7. Actividad 2.5: El Eco del Castigo (Trazo del Gradiente)
8. Actividad 2.6: Depuración del Oráculo (Inspección de Código NumPy)
```

---

## 1 1. El Acertijo: El Guardián del Tiempo

Lee atentamente las siguientes líneas. Cada estrofa describe un
componente matemático exacto de una celda recurrente básica. ¿Puedes
identificar a qué variable, matriz o función se refiere cada una antes
de leer la disección?

> Soy la novedad pura, el pulso del instante, la matriz de
> características que el mundo me da en este segundo.
>
> Pero soy ciego sin mi compañero, el fantasma del pasado,
> que trae consigo el resumen de todo lo que hemos vivido
> hasta ayer.
>
> Para unirnos, cruzamos por peajes inmutables, barreras que
> multiplican nuestra importancia y deciden qué tanto
> valemos.
>
> Juntos, sumados a un pequeño desvío inevitable, chocamos
> contra un muro curvo que nos comprime entre el -1 y el 1,
> evitando que nuestra energía explote hacia el infinito.
>
> Al salir de esa curva, nazco yo, una nueva identidad. Soy
> tu estado actual, la respuesta de hoy, y estoy listo para
> ser el fantasma de tu mañana.

---

## 2. Actividades de Comprensión (Para el Alumno)

Antes de avanzar a la disección analítica, resuelve los siguientes
retos para poner a prueba tu intuición matemática sobre la
arquitectura del modelo.

---

## 2.1 Actividad 2.1: Mapeo de Variables

Dada la ecuación fundamental de la Vanilla RNN:

$$
h_t = \tanh(W_{hx} x_t + W_{hh} h_{t-1} + b)
$$

Identifica y escribe la frase exacta del poema que hace referencia a
cada uno de los siguientes componentes matemáticos:

**$x_t$**
"Soy la novedad pura, el pulso del instante, la matriz de características que el mundo me da en este segundo."

---

**$h_{t-1}$**
"Pero soy ciego sin mi compañero, el fantasma del pasado, que trae consigo el resumen de todo lo que hemos vivido hasta ayer."

---

**$W_{hx}, W_{hh}$**
"Para unirnos, cruzamos por peajes inmutables, barreras que multiplican nuestra importancia y deciden qué tanto valemos."

---

**$b$**
"sumados a un pequeño desvío inevitable"

---

**$\tanh$**
"chocamos contra un muro curvo que nos comprime entre el -1 y el 1, evitando que nuestra energía explote hacia el infinito."

---

**$h_t$**
"Al salir de esa curva, nazco yo, una nueva identidad. Soy tu estado actual, la respuesta de hoy, y estoy listo para ser el fantasma de tu mañana."

---


## 2.2 Actividad 2.2: El Análisis de Dimensionalidad (El tamaño de los peajes)

Supón que estás diseñando esta red para procesar secuencias de
datos. Si la "novedad pura" ($x_t$) es un vector de entrada con
características de dimensión $\mathbb{R}^{20}$ y decides que el
"fantasma del pasado" ($h_{t-1}$) requiere una capacidad de memoria
representada en un espacio oculto de dimensión $\mathbb{R}^{64}$.

Calcula y justifica matemáticamente:

1. Las dimensiones exactas requeridas para la matriz $W_{hx}$.
   Para que $W_{hx} x_t$ sea válido:
   $W_{hx} \in \mathbb{R}^{64 \times 20}$

2. Las dimensiones exactas requeridas para la matriz recurrente $W_{hh}$.
   Para que $W_{hh} h_{t-1}$ sea válido:
   $W_{hh} \in \mathbb{R}^{64 \times 64}$

3. La dimensión final del vector resultante $h_t$.
   La suma produce un vector en $\mathbb{R}^{64}$, y $\tanh$ no cambia la dimensión:
   $h_t \in \mathbb{R}^{64}$

---

## 2.3 Actividad 2.3: La Estrofa Perdida (Pensamiento Lateral)

En el poema original, el vector de sesgo (bias) $b$ apenas se menciona
como "un pequeño desvío inevitable". Sabiendo que en álgebra lineal el
sesgo permite desplazar la función de activación para evitar que pase
rígidamente por el origen, **redacta una estrofa corta** (manteniendo
el tono literario del acertijo) que describa de manera exclusiva la
función y utilidad del parámetro $b$.

> Soy el leve susurro que inclina la balanza,
> el ajuste invisible que rompe la simetría,
> sin mí, todo nacería atado al frío origen,
> conmigo, cada respuesta encuentra su propio camino.

---

## 2.4 Actividad 2.4: El Límite del Muro Curvo (Análisis de Saturación)

El acertijo menciona que el muro curvo ($\tanh$) evita que "nuestra
energía explote hacia el infinito".

1. Grafica mentalmente o en papel la función $f(z) = \tanh(z)$ y su
   derivada $f'(z) = 1 - \tanh^2(z)$.
   La función $\tanh$ tiene forma sigmoide centrada en 0, saturando en -1 y 1. Su derivada es máxima en 0 y tiende a 0 en los extremos.

2. Si los valores de entrada y los pesos crecen descontroladamente y
   el resultado de la suma lineal es $z = 500$, la salida del muro
   curvo será casi exactamente $1$. ¿Qué le sucede a la derivada
   $f'(500)$ en ese punto?
   $f'(500) \approx 0$

3. Explica brevemente por qué este fenómeno (conocido como saturación)
   es catastrófico para el aprendizaje de la red.
   Porque el gradiente se vuelve prácticamente cero, impidiendo que el error se propague hacia atrás. Esto causa el problema de desvanecimiento del gradiente, bloqueando el aprendizaje.

---

## 2.5 Actividad 2.5: El Eco del Castigo (Trazo del Gradiente)

El aprendizaje en una RNN se realiza propagando el error hacia atrás
en el tiempo (BPTT). Supón que la red cometió un error en su
"respuesta de hoy" ($h_t$). Para corregirlo, la red debe enviar una
señal de castigo hacia atrás para ajustar los pesos.

Siguiendo la narrativa del acertijo: Describe qué "peajes" y "muros"
debe atravesar el error en reversa para llegar desde $h_t$ y poder
modificar la percepción del "fantasma del pasado" ($h_{t-1}$). ¿Qué
operación matemática del cálculo diferencial representa este viaje en
reversa?

El error debe atravesar primero el "muro curvo" ($\tanh$), pasando por su derivada. Luego cruza los "peajes" ($W_{hh}$) en sentido inverso mediante su transpuesta. Este proceso se repite a través del tiempo. Matemáticamente, este viaje corresponde a la aplicación de la **regla de la cadena** del cálculo diferencial.

---

## 2.6 Actividad 2.6: Depuración del Oráculo (Inspección de Código NumPy)

A continuación se presenta un intento de programar el oráculo en
Python. Sin embargo, el programador junior cometió **un grave error
algorítmico y matemático** en la línea 4 que provocará un colapso en
la dimensionalidad o un cálculo erróneo.

```python
def paso_rnn_erroneo(x_t, h_prev, W_hx, W_hh, b):
    # Línea con error oculto
    combinacion = (W_hx * x_t) + (W_hh * h_prev) + b
    return np.tanh(combinacion)
```

1. Identifica cuál es el error matemático exacto al usar el operador `*` en NumPy para este contexto matricial.
   El operador `*` realiza multiplicación elemento a elemento, pero aquí se requiere multiplicación matricial (producto punto).

2. Reescribe la línea de código utilizando la operación correcta dictada por el álgebra lineal para transformaciones afines.

```python
combinacion = (W_hx @ x_t) + (W_hh @ h_prev) + b
```

