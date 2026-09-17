# Reporte EDA — Operación Dino Crash

**Analista:** Juan Vera
---

## 1. Problema y dataset (Misión 1)

### P1 — ¿Morirá en el siguiente frame?

- **Y:** `died_next_frame`, binaria 0/1. Hay que construirla a partir de `died` desplazada una posición dentro de cada sesión, porque `died` marca el frame en que ya murió, no el anterior.
- **X (mínimo 5):**
  1. `dist_obstacle` — distancia al obstáculo más próximo.
  2. `speed` — determina el tiempo de reacción disponible.
  3. `obstacle_type` — un cactus y un bird no exigen la misma respuesta.
  4. `jump` — si el dino ya está en el aire, no puede volver a saltar.
  5. `dino_y` — altura real del dino, sin la cual no se sabe si el salto está en curso o ya cayó.
  6. `ducking` — necesaria para los obstáculos tipo bird.
- **Granularidad:** un frame por observación (~16 ms).
- **Tamaño mínimo:** varias decenas de partidas, con al menos unos cientos de muertes reales para que la clase positiva sea aprendible.
- **Riesgo si está mal definido:** etiquetar con `died` del frame actual produce leakage y un modelo inservible en producción.

### P2 — ¿Cuántos puntos alcanzará esta partida al morir?

- **Y:** `final_score`, numérica entera ≥ 0. Una fila por partida.
- **X (mínimo 5):**
  1. `score_at_10s` — ritmo temprano.
  2. `frames_survived`.
  3. `max_speed_reached`.
  4. `n_jumps`, `n_ducks`.
  5. `avg_dist_obstacle`.
- **Granularidad:** resumen por partida.
- **Tamaño mínimo:** varios cientos de partidas para que un MLP no sobreajuste.
- **Riesgo:** usar `frames_survived` como X cuando Y es `final_score` es circular.

### P3 — ¿Qué tipo de obstáculo viene próximo?

- **Y:** `next_obstacle_type`, categórica de 4 valores.
- **X (mínimo 5):**
  1. `dist_obstacle` actual.
  2. `speed`.
  3. `obstacle_type` actual.
  4. `time_since_last_obstacle`.
  5. `score`.
- **Granularidad:** por evento de aparición, no por frame.
- **Tamaño mínimo:** bastantes eventos por clase; si `bird` ronda el 11%, hacen falta más de los que parecen.
- **Riesgo:** sin shift correcto, el modelo solo aprende a copiar el input.

---

## 2. Diccionario y muestra (Misión 2)

- **Patrón en `died=1` (frame 82):** `dist_obstacle=12`, `jump=0`, `cactus_small`, `speed=6.8`. Obstáculo inminente y sin salto activo → colisión. La señal ya está en el frame anterior (81: `dist=38`, `jump=1`).
- **¿Falta alguna columna crítica para P1?** Sí: `dino_y`, `ducking`, `obstacle_y` (un bird volando alto no mata) y `reaction_lag_ms`.
- **¿`died` sirve para P1?** No. Es post-hoc; hay que desplazarla por sesión.

---

## 3. Checklist EDA (Misión 3)

**Pregunta 3 — Balance de la clase objetivo (P1):**
~12 000 frames y 50 muertes → **0.42% positivos**. Ratio ≈ 1:240. Claramente desbalanceado.

**Pregunta 8 — i.i.d.:**
Los frames de una misma sesión están encadenados. Mezclarlos entre train y test hace que el modelo vea el futuro de la misma partida, así que el split correcto es por `session_id`.

**Pregunta 9 — Estacionariedad:**
No se cumple: las partidas empiezan lentas y con pocos obstáculos y terminan rápidas y densas. Conviene mirar el comportamiento por tramos de `speed`.

**Data leakage concreto (P1):** `score` o `time_ms` del frame actual como X. `score` crece con la supervivencia y `died_next_frame` solo ocurre al final; el modelo aprende "score alto → muerte inminente", que es un artefacto del muestreo. En el frame justo antes de morir, `score` todavía es normal y el modelo falla.

---

## 4. Interpretación de resúmenes (Misión 4)

- **¿P1 desbalanceado?** Sí, 50 / 12 000 ≈ **0.42%**.
- **Métricas:** `accuracy` no dice nada (decir siempre "no muere" acierta 99.58%). Usaría precision/recall/F1, PR-AUC y ponderación de clases.
- **`dist_obstacle` como predictor:** útil. Las muertes ocurren con `dist < 20` (mínimo 5). Una regla como `dist < 15 y jump=0` ya captura buena parte. La frontera se ve casi lineal en el espacio `(dist_obstacle, jump)`.
- **Distribución de `score`:** media 28, mediana 18, máx 120 → cola larga. Para P2 conviene trabajar sobre `log(1+score)`; sin transformación los valores grandes dominan el gradiente del perceptrón.

---

## 5. Elección de modelo (Misiones 5–6)

| Escenario | ¿Perceptrón alcanza? | Arquitectura | 2 condiciones del dataset |
|---|---|---|---|
| **P1** | Sí, la frontera es casi lineal. | **Perceptrón simple** con sigmoide y ponderación de clases; si el one-hot de `obstacle_type` lo exige, **MLP de 1 capa oculta (16–32 neuronas)**. | (1) `died_next_frame` construido por shift. (2) Split por `session_id` + features normalizadas. |
| **P2** | Parcialmente: la relación no es lineal. | **MLP de 1–2 capas ocultas (32–64)** sobre `log(1+score)`. Un perceptrón simple solo captura la tendencia. | (1) Agregados por partida. (2) Varios cientos de partidas. |
| **P3** | Sí, 4 clases en pocas dimensiones. | **MLP de 1 capa oculta (32) con softmax**. | (1) Etiquetado por evento. (2) Suficientes ejemplos de `bird`. |

### Dónde el perceptrón NO alcanza

- **P1 como secuencia temporal:** si se quieren ventanas de 10–15 frames para capturar la dinámica del salto y la caída, un perceptrón no basta. Bajo la restricción actual, P1 se resuelve frame a frame y la versión secuencial queda fuera.
- **P3 con pocos eventos:** con <1000 apariciones de obstáculos, ningún perceptrón generaliza y el problema se declara no resoluble con esta familia.

### Contraejemplos (Misión 6)

1. **Perceptrón profundo que parece buena idea pero el EDA desaconseja (P1):** un MLP de 3–4 capas ocultas sobre los frames. Con 0.42% positivos y frames de la misma sesión en train y test, memoriza y en test con partidas nuevas el recall se hunde. La solución pasa por 1 capa oculta, ponderación de clases y split por sesión.
2. **Perceptrón que sí tendría sentido:** P1 con features bien armadas y suficientes muertes reales. La frontera se ve casi lineal, así que incluso un perceptrón simple debería dar recall decente.
3. **Reglas fijas vs perceptrón (P1):**
   - Regla: `si dist_obstacle < 15 y jump=0 y not ducking → muerte`. Interpretable, sin datos, funciona ya. No cubre birds a media altura ni saltos tardíos que aún salvan.
   - Perceptrón simple: aprende pesos parecidos a esa regla y la refina con `speed` y `obstacle_type`. Necesita suficientes muertes y split por sesión.
   - Con pocas muertes, la regla gana. Con dataset completo, perceptrón simple o MLP de 1 capa oculta bastan.

---

## Síntesis (5 líneas)

1. Pediría el CSV con `session_id`, `frame`, `dist_obstacle`, `speed`, `obstacle_type`, `jump`, `dino_y` y `ducking`, una fila por frame, con varias decenas de partidas.
2. Antes de entrenar, construiría `died_next_frame` desplazando `died` por sesión.
3. Miraría el EDA para confirmar desbalance, split por sesión, leakage de `score`/`time_ms`, cola larga de `score` y zona letal cerca de `dist_obstacle < 20`.
4. Después elegiría modelo dentro de perceptrones: P1 → perceptrón simple o MLP de 1 capa oculta; P2 → MLP de 1–2 capas sobre `log(1+score)`; P3 → MLP de 1 capa oculta con softmax.
5. P1 secuencial y P3 con pocos eventos quedan fuera del alcance de un perceptrón.

---
