# Parte I. Conceptos y definiciones

## Pregunta 1

¿Qué es un árbol de decisión y cuál es su objetivo principal dentro de un problema de clasificación?

**Respuesta:**
Un árbol de decisión es un modelo predictivo que representa una serie de reglas del tipo `if`. Su objetivo principal en clasificación es **asignar a cada nuevo ejemplo la clase más probable**, siguiendo un camino desde la raíz hasta una hoja según sus valores.

## Pregunta 2

Explique con sus propias palabras los siguientes elementos de un árbol de decisión:

- **Nodo raíz.**
- **Nodo interno.**
- **Rama.**
- **Hoja.**

**Respuesta:**
- **Nodo raíz:** Es el primer nodo, en la parte superior. Representa la primera pregunta o división que se hace sobre todo el conjunto de datos.
- **Nodo interno:** Es un nodo intermedio. Representa una pregunta adicional sobre un subconjunto de datos que aún no es lo suficientemente puro para decidir.
- **Rama:** Es la conexión entre nodos. Representa el resultado de una prueba.
- **Hoja:** Es el nodo final, sin divisiones posteriores. Contiene la decisión.

## Pregunta 3

¿Qué es una red neuronal multicapa y qué función cumplen las siguientes capas?

- **Capa de entrada.**
- **Capa oculta.**
- **Capa de salida.**

**Respuesta:**
Una red neuronal multicapa o MLP (Multilayer Perceptron) es un modelo compuesto por neuronas artificiales organizadas en capas conectadas entre sí. Cada neurona calcula una suma ponderada de sus entradas y le aplica una función de activación no lineal. Al apilar capas puede aprender relaciones complejas y no lineales que un modelo lineal no puede representar.

- **Capa de entrada:** Recibe los datos. Tiene una neurona por variable.
- **Capa oculta:** Realiza la transformación intermedia. Puede haber una o varias. Cada capa combina las salidas anteriores y extrae características cada vez más abstractas.
- **Capa de salida:** Entrega el resultado final. Tiene tantas neuronas como clases o valores a predecir.

## Pregunta 4

¿Qué representan los pesos y los sesgos dentro de una red neuronal?

Explique también por qué sus valores cambian durante el entrenamiento.

**Respuesta:**
- **Pesos (w):** Representan la importancia o influencia de cada entrada sobre una neurona. Un peso grande positivo indica que esa entrada empuja fuertemente la activación; un peso cercano a cero indica que es irrelevante.
- **Sesgos (b):** Representan el umbral de activación de la neurona. Permiten desplazar la función de activación para que la neurona se active aunque todas las entradas sean cero.

Sus valores cambian durante el entrenamiento porque inicialmente son aleatorios y no representan el problema. Mediante **backpropagation y descenso de gradiente** la red calcula el error entre su predicción y el valor real (función de pérdida) y ajusta iterativamente pesos y sesgos en la dirección que reduce ese error.

## Pregunta 5

¿Cuál es la principal diferencia entre la forma en que aprende un árbol de decisión y la forma en que aprende una red neuronal multicapa?

Explique qué elementos aprende cada modelo.

**Respuesta:**

- **Árbol de decisión aprende reglas discretas:** elige qué atributo/umbral usar y cuándo detenerse mediante criterios como Entropía o Gini. Divide los datos de forma voraz y jerárquica, sin usar derivadas.
- **Red neuronal aprende parámetros continuos:** ajusta pesos y sesgos mediante optimización iterativa: propagación, pérdida, gradientes y actualización. Aprende una función matemática, no reglas explícitas.

# Parte II. Análisis y aplicación

## Pregunta 6

Una institución bancaria desea desarrollar un sistema que detecte posibles compras fraudulentas.

El sistema dispone de información como:

- **Monto de la compra.**
- **Hora de la operación.**
- **Ciudad donde se realizó.**
- **Tipo de establecimiento.**
- **Número de compras realizadas durante el día.**
- **Historial de compras del cliente.**

Analice las ventajas y desventajas de utilizar un árbol de decisión y una red neuronal multicapa.

**¿Cuál utilizaría y por qué?**

**Respuesta:**
**Árbol de decisión:**
Ventajas: interpretable; se puede explicar al cliente y al regulador por qué se bloqueó una compra; maneja bien variables mixtas numéricas/categóricas (monto, hora, ciudad, tipo de comercio); entrena rápido y funciona con menos datos.
Desventajas: tiende al sobreajuste; le cuesta capturar interacciones complejas y temporales del historial del cliente; el fraude es desbalanceado (<1% fraude) y cambiante, un árbol simple pierde precisión y genera muchos falsos positivos/negativos.

**Red neuronal multicapa:**
Ventajas: capta relaciones no lineales complejas entre monto, hora, frecuencia, historial y ciudad; con millones de transacciones suele lograr mayor  precisión; se adapta mejor a patrones sutiles de fraude.

Desventajas: difícil justificar un bloqueo; necesita gran volumen de datos etiquetados, más cómputo; sensible a desbalance si no se trata.

**¿Cuál utilizaría?** Para un banco en producción con gran volumen histórico, elegiría la **red neuronal como motor principal de detección**, porque el problema es complejo, no lineal, de alta dimensionalidad y el costo de no detectar fraude es alto. Si el banco tiene pocos datos o se exige por regulación explicar las decisiones, empezaría con el árbol.

## Pregunta 7

Una escuela quiere detectar estudiantes que presentan riesgo de reprobar una materia.

Se conocen variables como:

- **Asistencia.**
- **Calificaciones.**
- **Tareas entregadas.**
- **Participación.**
- **Número de materias reprobadas anteriormente.**

Suponga que un árbol de decisión y una red neuronal obtienen prácticamente la misma precisión.

**¿Qué otros factores tomaría en cuenta para elegir uno de los dos modelos?**

Justifique su respuesta.

**Respuesta:**:

1. **Interpretabilidad y aceptación:** la escuela necesita decirle al alumno/padre/docente *por qué* está en riesgo y qué hacer. El árbol lo da directamente; la red no.
2. **Cantidad de datos y cómputo:** una escuela tiene cientos o miles de registros, no millones, y pocas computadoras. El árbol entrena en segundos y requiere menos datos.
3. **Mantenimiento y confianza:** docentes pueden leer, validar y corregir un árbol. Una red genera desconfianza y dependencia técnica.

## Pregunta 8

Un hospital desarrolla un sistema para determinar qué pacientes necesitan atención prioritaria utilizando:

- **Edad.**
- **Temperatura.**
- **Presión arterial.**
- **Frecuencia cardiaca.**
- **Síntomas.**
- **Antecedentes médicos.**

Una red neuronal obtiene mejores resultados que un árbol de decisión, pero resulta más difícil explicar cómo obtuvo su respuesta.

**¿Considera que la mayor precisión es suficiente para elegir la red neuronal?**

Analice las consecuencias que podría tener esta decisión.

**Respuesta:**
No, la mayor precisión por sí sola **no es suficiente** para elegir la red.

Análisis de consecuencias:

- **Costo del error:** un falso negativo (no priorizar a un paciente grave) puede causar muerte o daño irreversible. Una precisión global alta puede ocultar mal desempeño en un subgrupo crítico.
- **Responsabilidad médica y legal:** el médico debe justificar el triage ante el paciente, la familia y una auditoría. Si el sistema no explica, el médico no puede validar ni asumir responsabilidad informada.
- **Confianza y adopción:** personal médico no usará un sistema opaco en decisiones vitales.

## Pregunta 9

Una empresa de reparto quiere predecir si un pedido llegará tarde considerando:

- **Distancia.**
- **Tráfico.**
- **Clima.**
- **Hora del día.**
- **Cantidad de pedidos.**
- **Experiencia del repartidor.**

Para determinado pedido, el árbol de decisión indica:

> **Llegará a tiempo.**

Mientras que la red neuronal indica:

> **Probablemente llegará tarde.**

**¿Cómo determinaría cuál de los dos modelos está realizando una mejor predicción?**

Explique qué información adicional debería analizar.

**Respuesta:**

1. **Evaluar en datos históricos con resultado conocido:**
2. **Calibración de probabilidad:** la red dice "probablemente tarde" (probabilidad). Verificar si sus probabilidades corresponden a frecuencias reales. El árbol solo da clase.
3. **Estabilidad:** probar cómo cambia la predicción ante pequeñas variaciones y revisar errores pasados de cada modelo en casos similares.

## Pregunta 10

Una empresa desarrolla dos sistemas para decidir si una persona puede recibir un crédito.

El primer sistema utiliza un árbol de decisión y permite explicar claramente por qué una solicitud fue rechazada.

El segundo utiliza una red neuronal multicapa y obtiene mejores resultados de predicción, pero es más difícil explicar sus decisiones.

Si usted fuera responsable del proyecto:

- **¿Cuál de los dos modelos utilizaría?**
- **¿Qué ventajas tendría su elección?**
- **¿Qué riesgos tendría?**
- **¿Consideraría posible utilizar ambos modelos dentro del mismo sistema?**

Justifique ampliamente su respuesta.

**Respuesta:**
**Usaría los dos**.

- **Si elijo el árbol:** Ventaja: puedo entregar al solicitante un motivo claro, cumplir con normativa financiera, auditar sesgos y generar confianza. Riesgo: al ser menos preciso, apruebo créditos que impagan (pérdida económica) o rechazo buenos clientes (pérdida comercial e injusticia).
- **Si elijo la red:** Ventaja: mejor predicción, menos morosidad, más rentabilidad. Riesgo: opacidad legal y ética —no puedo justificar un rechazo, puedo estar discriminando indirectamente por variables correlacionadas (código postal, edad), con riesgo de demanda, multa y daño reputacional.

**¿Usar ambos? Es la opción más responsable como una arquitectura híbrida** 

# Reflexión final

A partir de los ejercicios anteriores, explique brevemente la siguiente afirmación:

> **No existe un algoritmo de Inteligencia Artificial que sea el mejor para todos los problemas.**

Relacione su respuesta con los conceptos de:

- **Precisión.**
- **Interpretabilidad.**
- **Cantidad de datos.**
- **Complejidad del problema.**
- **Consecuencias de una decisión incorrecta.**

**Respuesta:**
Cada algoritmo hace supuestos distintos y paga un costo para ganar una ventaja.

- **Precisión:** la red suele ganar en problemas complejos no lineales (fraude, imágenes, triage con muchas interacciones), pero esa ventaja desaparece con pocos datos o problemas simples, como el ejemplo escolar donde iguala al árbol.
- **Interpretabilidad:** el árbol gana cuando hay que explicar, justificar legalmente o generar acciones (escuela, crédito, medicina). La mayor precisión de la red no compensa si no se puede auditar.
- **Cantidad de datos:** la red necesita miles/millones de ejemplos para estimar miles de pesos sin sobreajustar; el árbol funciona con cientos y es más robusto con datos tabulares pequeños.
- **Complejidad del problema:** a mayor interacción entre variables, más justificada la red; a reglas separables por umbrales, basta el árbol.
- **Consecuencias de un error:** si un error cuesta vidas, libertad o dinero regulado (hospital, crédito), se prioriza explicabilidad, control de falsos negativos y supervisión humana.

Por tanto, elegir modelo no es buscar "el mejor", sino el **más adecuado para las necesidades** que exige cada problema.
