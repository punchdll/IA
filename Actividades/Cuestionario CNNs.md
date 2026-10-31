# 10 PREGUNTAS REDES NEURONALES CONVOLUCIONALES (CNN)
---

## Índice

1. Instrucciones (alumnos)
2. Pregunta 1 — Convolución a mano (3×3)
3. Pregunta 2 — Contar pesos
4. Pregunta 3 — ¿Qué cambia si meto más capas?
5. Pregunta 4 — Formas: de volumen a vector
6. Pregunta 5 — Softmax y el error “casi seguro”
7. Pregunta 6 — Padding, stride y “se me achicó la imagen”
8. Pregunta 7 — Dropout: ¿dónde y para qué?
9. Pregunta 8 — Diseño: 5 clases de animales
10. Pregunta 9 — CNN vs MLP vs RNN (mismo problema, mala herramienta)
11. Pregunta 10 — Experimento mental: mover un gato
12. Autoevaluación rápida (opcional)
13. Notas al pie (fórmulas útiles — no sustituyen el razonamiento)

---

## 1. Instrucciones (alumnos)

- Responde **con lápiz y papel** (o en este mismo buffer de Org).
- No basta con definir de memoria: hay que **calcular**, **comparar** o **justificar**.

---

## 2. Pregunta 1 — Convolución a mano (3×3)

Tienes este trozo de imagen en escala de grises (un canal) y este kernel:

```text
Imagen 5×5               Kernel 3×3
0  0  1  0  0              1  0 -1
0  1  2  1  0              1  0 -1
1  2  3  2  1              1  0 -1
0  1  2  1  0
0  0  1  0  0
```




### Tareas

1. Con **stride = 1** y **padding valid** (sin relleno), ¿cuál es el tamaño del mapa de salida?
> 3 x 3
2. Calcula **solo** el valor de la esquina superior izquierda del mapa (la primera posición del filtro). Muestra la suma de productos.
```
(0)(1)+(0)(0)+(1)(−1)+(0)(1)+(1)(0)+(2)(−1)+(1)(1)+(2)(0)+(3)(−1)
​= -1-2+1-3 
```
> -5
3. ¿Este kernel parece detectar bordes **verticales** u **horizontales**? Justifica mirando los signos.
> Bordes verticales.
l kernel tiene valores positivos en la columna izquierda (1)(1), ceros en la columna central y valores negativos en la columna derecha (−1)
(−1). Por eso calcula la diferencia entre la intensidad del lado izquierdo y la del lado derecho, detectando cambios horizontales de intensidad que corresponden a bordes verticales.

---

## 3. Pregunta 2 — Contar pesos

Una imagen RGB de **28×28×3**. Compara dos modelos:

- **Modelo A (MLP ingenuo):** aplastas la imagen a un vector y conectas **todas** las entradas a una capa densa de **64 neuronas** (sin bias por ahora).
- **Modelo B (CNN):** una `Conv2D` con **16 filtros** de **3×3**, `padding='same'`, sobre la misma imagen (con bias: un bias por filtro).

### Tareas

1. ¿Cuántos pesos tiene la capa densa del Modelo A? (fórmula y número)
```
28×28×3=2352 entradas
Pesos=2352×64
```
> 150,528 pesos
2. ¿Cuántos parámetros tiene la Conv2D del Modelo B? (pesos de kernels + biases)
```
3×3×3=27 pesos por filtro
27×16=432 pesos
432+16=448 parametros
​
```
3. En **una frase**: ¿por qué la CNN suele generalizar mejor con el mismo número de imágenes de entrenamiento?
La CNN suele generalizar mejor porque tiene menos parámetros y reutiliza los mismos filtros.
---

## 4. Pregunta 3 — ¿Qué cambia si meto más capas?

Parte del notebook `CNNriesgo` (simplificado):

```text
Entrada (21×28×3)
  → Conv2D(32, 3×3, same) + LeakyReLU
  → MaxPool(2×2)
  → Flatten → Dense(32) → Dense(nClasses, softmax)
```

Quieres **apilar un segundo bloque** convolucional **antes** del `Flatten`:

```text
… → Conv2D(32) → Pool → Conv2D(64, 3×3, same) → Pool → Flatten → …
```

### Tareas

1. Tras el **primer** MaxPool(2×2) con padding same sobre 21×28, ¿qué tamaño aproximado (alto×ancho) esperas? (puedes redondear / usar la regla “casi la mitad”)
```
Con padding='same', la primera convolución mantiene el tamaño espacial en 21×28. Después, el MaxPool(2×2) reduce aproximadamente a la mitad cada dimensión
```
> 11x14
2. ¿Qué **significan** ahora los 64 filtros de la segunda Conv2D: detectan bordes “crudos” o patrones **más compuestos**? Explica con la analogía de la lupa / capas abstractas.
```
Detectan patrones más compuestos y abstractos, no solamente bordes crudos.

Analogía de la lupa: la primera convolución observa detalles sencillos, como bordes y líneas; la segunda combina esos detalles para reconocer formas más complejas, como esquinas, texturas o partes de objetos. Al tener 64 filtros, puede aprender 64 tipos distintos de patrones.
```
3. Riesgo: si añades **muchas** capas Conv+Pool con pocas imágenes, ¿qué falla típico verías en las curvas train vs validation? ¿Qué harías primero para mitigarlo (Dropout, más datos, menos filtros…)? Elige **una** medida y justifica.

```
Un fallo típico es el sobreajuste (overfitting): la curva de pérdida de entrenamiento (train loss) sigue bajando, mientras que la de validación (validation loss) deja de bajar o empieza a subir.
Con pocas imágenes, usar menos filtros reduce los parámetros y la capacidad del modelo para memorizar ejemplos, lo que puede mejorar la generalización y disminuir el sobreajuste.
```
---

## 5. Pregunta 4 — Formas: de volumen a vector

Supón que, justo antes del Flatten, el tensor tiene forma `(7, 7, 64)` (lote omitido: una sola imagen).

### Tareas

1. ¿Cuántos números salen del Flatten? (un solo entero)
> 3136
2. Si la siguiente Dense tiene **32 neuronas** (con bias), ¿cuántos parámetros tiene **esa** Dense?
```
3136×32+32=100,352+32
```
>=100,384
3. Si en vez de Flatten usas **Global Average Pooling** (un promedio por canal), ¿qué forma tendrías a la salida y cuántos valores serían? ¿Ventaja frente a Flatten cuando la imagen de entrada es más grande?
> Hace un promedio por cada canal. A la salida tendrías forma (64,)
```
Ventaja: reduce el número de parámetros antes de la Dense y disminuye el sobreajuste
```
---

## 6. Pregunta 5 — Softmax y el error “casi seguro”

Una CNN de 3 clases (inundación, incendio, tornado) saca logits que, tras softmax, dan:

```text
P = [0.10, 0.05, 0.85]
```

La etiqueta verdadera (one-hot) es `[0, 1, 0]` (incendio).

### Tareas

1. ¿Qué clase predice el modelo (`argmax`)?
> La clase 3, tornado, porque tiene probabilidad 0.85.
2. ¿Está “seguro” o “confundido”? Usa los números, no adjetivos vacíos.
```
Está muy seguro de la clase incorrecta. La clase verdadera, incendio, solo tiene probabilidad 0.05 (5 %), mientras que la predicción errónea tiene 85 %. Es un caso de alta confianza y baja precisión.
```
3. Sin calcular la fórmula exacta: argumenta si la **categorical crossentropy** de este ejemplo será **alta** o **baja**, y por qué (pista: castiga cuando la probabilidad de la clase correcta es pequeña).
```
Será alta, porque castiga que la probabilidad asignada a la clase correcta sea pequeña.
```
---

## 7. Pregunta 6 — Padding, stride y “se me achicó la imagen”

Entrada **32×32**, kernel **5×5**, **un** filtro, un canal.

### Tareas

Completa la tabla (escribe el alto×ancho de salida):

| padding | stride | salida (alto×ancho) |
|---------|--------|---------------------|
| valid   | 1      |28x2                 |
| valid   | 2      |14x14                |
| same    | 1      |32x32                |

Luego: si encadenas **tres** MaxPool(2×2) seguidos sobre una imagen 32×32 (sin cuidar bordes), ¿qué problema práctico aparece para clasificar objetos **pequeños** o detalles finos?
```
> 32→16→8→4
El problema práctico es que la resolución espacial se reduce demasiado: los objetos pequeños o detalles finos pueden desaparecer antes de llegar a la clasificación. También se pierde información de bordes si los tamaños son impares.
```
---

## 8. Pregunta 7 — Dropout: ¿dónde y para qué?

En `CNNriesgo` hay `Dropout(0.5)` después del pooling y otra vez antes de la salida.

### Tareas

1. Durante **entrenamiento**, ¿qué hace Dropout(0.5) en una capa densa de 32 neuronas (en promedio cuántas “sobreviven” por paso)?
```
Cada neurona se apaga aleatoriamente con probabilidad 0.5 en cada paso. En promedio sobreviven 16 neuronas por paso.
```
2. Durante **inferencia** (`predict`), ¿se apagan neuronas al azar? ¿Por qué sí o no?
> No se apagan neuronas al azar. Todas quedan activas y la red es determinista.
3. Un compañero pone Dropout **solo** en la última época “para que no se sobreajuste al final”. ¿Tiene sentido? Critica la idea en 3–5 líneas.
```
El Dropout es una regularización estocástica que debe aplicarse durante todo el entrenamiento para evitar que las neuronas se acostumbren a depender unas de otras. Aplicarlo solo al final no corrige el sobreajuste ya producido y puede impedir que el modelo termine de ajustar. Debe activarse desde el inicio y desactivarse en inferencia.
```
---

## 9. Pregunta 8 — Diseño: 5 clases de animales

Debes adaptar `CNNriesgo` a: ranas, arañas, monos, ballenas, pájaros.

### Tareas

1. ¿Cuántas neuronas debe tener la **última** Dense y qué activación? ¿Por qué?
```
5 neuronas con activación softmax, porque hay 5 clases mutuamente excluyentes y queremos una distribución de probabilidad sobre ellas.
```
2. Si todas las fotos entran a **224×224×3** pero el modelo tiene `input_shape=(21,28,3)`, ¿qué **debe** pasar antes del `fit`? (una frase operativa)
```
Hay que redimensionar todas las imágenes a 21×28×3, o bien modificar el input_shape
```
3. Propón **una** mejora de arquitectura (segundo Conv, BatchNorm, data augmentation…) y di **qué síntoma** en train/val te haría pensar que esa mejora era necesaria.
```
Usaría data augmentation (rotaciones, volteos, recortes, cambios de brillo).
Síntoma que la justificaría: que la accuracy de entrenamiento sea mucho más alta que la de validación, es decir, sobreajuste. Al augmentar los datos, el modelo ve variaciones realistas y generaliza mejor.
```
---

## 10. Pregunta 9 — CNN vs MLP vs RNN (mismo problema, mala herramienta)

Tres escenarios. Elige **CNN**, **MLP** o **RNN/Transformer** y justifica en **una** frase cada uno:

1. Predecir si un alumno aprueba con promedio, faltas y horas de estudio (tabla).
```
MLP. Son datos tabulares sin estructura espacial ni secuencial; una red densa puede combinar las variables.
```
2. Clasificar fotos de semáforo (rojo / amarillo / verde).
```
La imagen tiene estructura espacial y la CNN explota patrones locales y comparte pesos.
```
3. Autocompletar la siguiente línea de código dado el prefijo escrito.
```
El problema es secuencial y depende del contexto anterior; estos modelos están diseñados para secuencias.
```
Si aplastas la foto del semáforo y usas un MLP “grande”, ¿puede **aprender**? ¿Qué sacrificas respecto a una CNN? (parámetros, datos, invariancia…)
```
Podría aprenderlo pero se sacrificarian ciertas caracteristicas:
- Eficiencia de parámetros: el MLP necesita muchísimos más pesos.

- Invariancia a traslación: no la tiene incorporada; debe aprenderla con más datos.

- Conectividad local y pesos compartidos: la CNN reutiliza filtros; el MLP no.

- Generalización: suele necesitar más datos y tiende a sobreajustar más.
```
---

## 11. Pregunta 10 — Experimento mental: mover un gato

Entrenaste una CNN que detecta “hay un gato” en fotos 64×64. En el test, el mismo gato aparece **corrido 10 píxeles a la derecha**, mismo fondo, misma escala.

### Tareas

1. ¿Por qué una CNN tiene **más chance** de seguir acertando que un MLP que ve el vector aplastado? (pesos compartidos / detección local)
```
Porque usa pesos compartidos y campos receptivos locales: el mismo filtro busca el patrón “gato” en distintas posiciones de la imagen. Un MLP que ve el vector aplastado tiene pesos separados para cada píxel, así que un desplazamiento cambia las entradas y le cuesta más reconocer el mismo objeto.
```
2. Si en vez de correrlo lo **giraras 90°** y nunca viste gatos de lado en el train, ¿la CNN “mágica” garantiza acierto? ¿Qué haría falta (augmentation, más datos…)?
```
No hay garantía. La CNN no es mágicamente invariante a rotaciones; solo tiene cierta equivarianza a traslaciones. Para mejorar necesitaría data augmentation con rotaciones, más datos variados o un diseño que incluya invariancia a rotación.
```
3. Escribe **una** pregunta que tú le harías a un compañero para comprobar si entendió qué son los **pesos del kernel** (no copies las de arriba).
```
“Si un kernel 3×3 tiene todos sus pesos iguales a 1/9, ¿qué operación está haciendo sobre la imagen y qué esperarías ver en el mapa de salida?”
```
---

## 12. Autoevaluación rápida (opcional)

Marca 1–5 (1 = no entendí, 5 = lo explicaría en pizarrón):

| Tema                                | Nota |
|-------------------------------------|------|
| Producto punto del kernel           |4     |
| Conteo de parámetros Conv vs Dense  |3     |
| Efecto de apilar Conv+Pool          |2     |
| Softmax + pérdida                   |3     |
| Dropout train vs inferencia         |2     |

---

## 13. Notas al pie (fórmulas útiles — no sustituyen el razonamiento)

- Salida convolución (un eje), padding valid: \(\lfloor (N - K)/S \rfloor + 1\)
- Padding same + stride 1: salida ≈ mismo \(N\)
- Parámetros Conv2D: \(K_h \cdot K_w \cdot C_{in} \cdot C_{out} + C_{out}\) (si hay bias)
- Parámetros Dense: \(n_{in} \cdot n_{out} + n_{out}\) (si hay bias)