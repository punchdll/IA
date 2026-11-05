**Paso 1: Inicialización (t=0)**

$$
h_0 = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}
$$

**Paso 2: Primer paso temporal (t=1)**

**Entrada:**

$$
x_1 = \begin{bmatrix} 1 \\ 2 \end{bmatrix}
$$

**Pesos (ejemplo):**

$$
W_{xh} = \begin{bmatrix} 0.1 & 0.3 \\ 0.2 & 0.4 \\ 0.3 & 0.5 \end{bmatrix}, \quad W_{hh} = \begin{bmatrix} 0.6 & 0.1 & 0.2 \\ 0.1 & 0.7 & 0.3 \\ 0.2 & 0.3 & 0.8 \end{bmatrix}, \quad b_h = \begin{bmatrix} 0.1 \\ 0.2 \\ 0.3 \end{bmatrix}
$$

**Cálculo del estado oculto:**

1.

$$
W_{xh} \cdot x_1
$$

$$
\begin{bmatrix} 0.1 & 0.3 \\ 0.2 & 0.4 \\ 0.3 & 0.5 \end{bmatrix} \begin{bmatrix} 1 \\ 2 \end{bmatrix} = \begin{bmatrix} 0.1(1) + 0.3(2) \\ 0.2(1) + 0.4(2) \\ 0.3(1) + 0.5(2) \end{bmatrix} = \begin{bmatrix} 0.7 \\ 1.0 \\ 1.3 \end{bmatrix}
$$

2.

$$
W_{hh} \cdot h_0 :
$$

$$
\begin{bmatrix} 0.6 & 0.1 & 0.2 \\ 0.1 & 0.7 & 0.3 \\ 0.2 & 0.3 & 0.8 \end{bmatrix} \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}
$$

1. Suma con bias:

$$
\begin{bmatrix} 0.7 \\ 1.0 \\ 1.3 \end{bmatrix} + \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix} + \begin{bmatrix} 0.1 \\ 0.2 \\ 0.3 \end{bmatrix} = \begin{bmatrix} 0.8 \\ 1.2 \\ 1.6 \end{bmatrix}
$$



2. Aplicar tanh:

$$
h_1 = \tanh \left( \begin{bmatrix} 0.8 \\ 1.2 \\ 1.6 \end{bmatrix} \right) \approx \begin{bmatrix} 0.664 \\ 0.834 \\ 0.922 \end{bmatrix}
$$

**Cálculo de la salida:**

$$
W_{hy} = \begin{bmatrix} 0.5 & 0.3 & 0.2 \end{bmatrix}, \quad b_y = 0.1
$$

$$
y_1 = W_{hy} \cdot h_1 + b_y = \begin{bmatrix} 0.5 & 0.3 & 0.2 \end{bmatrix} \begin{bmatrix} 0.664 \\ 0.834 \\ 0.922 \end{bmatrix} + 0.1
$$

$$
= 0.5(0.664) + 0.3(0.834) + 0.2(0.922) + 0.1 = 0.332 + 0.250 + 0.184 + 0.1 = 0.866
$$

**Paso 3: Segundo paso temporal (t=2)**

**Entrada:**

$$
x_2 = \begin{bmatrix} 3 \\ 4 \end{bmatrix}
$$

**Cálculo:**

1.

$$
W_{xh} \cdot x_2 :
$$

$$
\begin{bmatrix} 0.1 & 0.3 \\ 0.2 & 0.4 \\ 0.3 & 0.5 \end{bmatrix} \begin{bmatrix} 3 \\ 4 \end{bmatrix} = \begin{bmatrix} 1.5 \\ 2.2 \\ 2.9 \end{bmatrix}
$$

2.

$$
W_{hh} \cdot h_1
$$

(¡Ahora usamos la memoria!):

$$
\begin{bmatrix} 0.6 & 0.1 & 0.2 \\ 0.1 & 0.7 & 0.3 \\ 0.2 & 0.3 & 0.8 \end{bmatrix} \begin{bmatrix} 0.664 \\ 0.834 \\ 0.922 \end{bmatrix} = \begin{bmatrix} 0.6(0.664) + 0.1(0.834) + 0.2(0.922) \\ 0.1(0.664) + 0.7(0.834) + 0.3(0.922) \\ 0.2(0.664) + 0.3(0.834) + 0.8(0.922) \end{bmatrix} = \begin{bmatrix} 0.398 + 0.083 + 0.184 \\ 0.066 + 0.584 + 0.277 \\ 0.133 + 0.250 + 0.738 \end{bmatrix} = \begin{bmatrix} 0.665 \\ 0.927 \\ 1.121 \end{bmatrix}
$$

3. Suma:

$$
\begin{bmatrix} 1.5 \\ 2.2 \\ 2.9 \end{bmatrix} + \begin{bmatrix} 0.665 \\ 0.927 \\ 1.121 \end{bmatrix} + \begin{bmatrix} 0.1 \\ 0.2 \\ 0.3 \end{bmatrix} = \begin{bmatrix} 2.265 \\ 3.327 \\ 4.321 \end{bmatrix}
$$

4. Aplicar tanh:

$$
h_2 = \tanh \left( \begin{bmatrix} 2.265 \\ 3.327 \\ 4.321 \end{bmatrix} \right) \approx \begin{bmatrix} 0.978 \\ 0.997 \\ 0.999 \end{bmatrix}
$$

**Cálculo de la salida:**

$$
W_{hy} = \begin{bmatrix} 0.5 & 0.3 & 0.2 \end{bmatrix}, \quad b_y = 0.1
$$

$$
y_2 = W_{hy} \cdot h_2 + b_y = \begin{bmatrix} 0.5 & 0.3 & 0.2 \end{bmatrix} \begin{bmatrix} 0.978 \\ 0.997 \\ 0.999 \end{bmatrix} + 0.1
$$

$$
= 0.5(0.978) + 0.3(0.997) + 0.2(0.999) + 0.1 = 0.489 + 0.2991 + 0.1998 + 0.1 = 1.0879
$$

**Paso 4: Tercer paso temporal (t=3)**

**Entrada:**

$$
x_3 = \begin{bmatrix} 5 \\ 6 \end{bmatrix}
$$

**Cálculo:**

1.

$$
W_{xh} \cdot x_3 :
$$

$$
\begin{bmatrix} 0.1 & 0.3 \\ 0.2 & 0.4 \\ 0.3 & 0.5 \end{bmatrix} \begin{bmatrix} 5 \\ 6 \end{bmatrix} = \begin{bmatrix} 0.1(5) + 0.3(6) \\ 0.2(5) + 0.4(6) \\ 0.3(5) + 0.5(6) \end{bmatrix} = \begin{bmatrix} 2.3 \\ 3.4 \\ 4.5 \end{bmatrix}
$$

2.

$$
W_{hh} \cdot h_2
$$

(¡Ahora usamos la memoria!):

$$
\begin{bmatrix} 0.6 & 0.1 & 0.2 \\ 0.1 & 0.7 & 0.3 \\ 0.2 & 0.3 & 0.8 \end{bmatrix} \begin{bmatrix} 0.978 \\ 0.997 \\ 0.999 \end{bmatrix} = \begin{bmatrix} 0.6(0.978) + 0.1(0.997) + 0.2(0.999) \\ 0.1(0.978) + 0.7(0.997) + 0.3(0.999) \\ 0.2(0.978) + 0.3(0.997) + 0.8(0.999) \end{bmatrix} = \begin{bmatrix} 0.5868 + 0.0997 + 0.1998 \\ 0.0978 + 0.6979 + 0.2997 \\ 0.1956 + 0.2991 + 0.7992 \end{bmatrix} = \begin{bmatrix} 0.8863 \\ 1.0954 \\ 1.2939 \end{bmatrix}
$$

3. Suma con bias:

$$
\begin{bmatrix} 2.3 \\ 3.4 \\ 4.5 \end{bmatrix} + \begin{bmatrix} 0.8863 \\ 1.0954 \\ 1.2939 \end{bmatrix} + \begin{bmatrix} 0.1 \\ 0.2 \\ 0.3 \end{bmatrix} = \begin{bmatrix} 3.2863 \\ 4.6954 \\ 6.0939 \end{bmatrix}
$$

4. Aplicar tanh:

$$
h_3 = \tanh \left( \begin{bmatrix} 3.2863 \\ 4.6954 \\ 6.0939 \end{bmatrix} \right) \approx \begin{bmatrix} 0.9972 \\ 0.9998 \\ 1.0000 \end{bmatrix}
$$

**Cálculo de la salida:**

$$
y_3 = W_{hy} \cdot h_3 + b_y = \begin{bmatrix} 0.5 & 0.3 & 0.2 \end{bmatrix} \begin{bmatrix} 0.9972 \\ 0.9998 \\ 1.0000 \end{bmatrix} + 0.1
$$

$$
= 0.5(0.9972) + 0.3(0.9998) + 0.2(1.0000) + 0.1 = 0.4986 + 0.29994 + 0.2 + 0.1 = 1.09854
$$

$$
\boxed{y_3 \approx 1.0985}
$$

**Paso 5: Cuarto paso temporal (t=4)**

**Entrada:**

$$
x_4 = \begin{bmatrix} 7 \\ 8 \end{bmatrix}
$$

**Cálculo:**

1.

$$
W_{xh} \cdot x_4 :
$$

$$
\begin{bmatrix} 0.1 & 0.3 \\ 0.2 & 0.4 \\ 0.3 & 0.5 \end{bmatrix} \begin{bmatrix} 7 \\ 8 \end{bmatrix} = \begin{bmatrix} 0.1(7) + 0.3(8) \\ 0.2(7) + 0.4(8) \\ 0.3(7) + 0.5(8) \end{bmatrix} = \begin{bmatrix} 3.1 \\ 4.6 \\ 6.1 \end{bmatrix}
$$

2.

$$
W_{hh} \cdot h_3
$$

(¡Ahora usamos la memoria!):

$$
\begin{bmatrix} 0.6 & 0.1 & 0.2 \\ 0.1 & 0.7 & 0.3 \\ 0.2 & 0.3 & 0.8 \end{bmatrix} \begin{bmatrix} 0.9972 \\ 0.9998 \\ 1.0000 \end{bmatrix} = \begin{bmatrix} 0.6(0.9972) + 0.1(0.9998) + 0.2(1.0000) \\ 0.1(0.9972) + 0.7(0.9998) + 0.3(1.0000) \\ 0.2(0.9972) + 0.3(0.9998) + 0.8(1.0000) \end{bmatrix} = \begin{bmatrix} 0.59832 + 0.09998 + 0.20000 \\ 0.09972 + 0.69986 + 0.30000 \\ 0.19944 + 0.29994 + 0.80000 \end{bmatrix} = \begin{bmatrix} 0.89830 \\ 1.09958 \\ 1.29938 \end{bmatrix}
$$

3. Suma con bias:

$$
\begin{bmatrix} 3.1 \\ 4.6 \\ 6.1 \end{bmatrix} + \begin{bmatrix} 0.89830 \\ 1.09958 \\ 1.29938 \end{bmatrix} + \begin{bmatrix} 0.1 \\ 0.2 \\ 0.3 \end{bmatrix} = \begin{bmatrix} 4.09830 \\ 5.89958 \\ 7.69938 \end{bmatrix}
$$

4. Aplicar tanh:

$$
h_4 = \tanh \left( \begin{bmatrix} 4.09830 \\ 5.89958 \\ 7.69938 \end{bmatrix} \right) \approx \begin{bmatrix} 0.99945 \\ 0.999985 \\ 0.9999996 \end{bmatrix}
$$

**Cálculo de la salida:**

$$
W_{hy} = \begin{bmatrix} 0.5 & 0.3 & 0.2 \end{bmatrix}, \quad b_y = 0.1
$$

$$
y_4 = W_{hy} \cdot h_4 + b_y = \begin{bmatrix} 0.5 & 0.3 & 0.2 \end{bmatrix} \begin{bmatrix} 0.99945 \\ 0.999985 \\ 0.9999996 \end{bmatrix} + 0.1
$$

$$
= 0.5(0.99945) + 0.3(0.999985) + 0.2(0.9999996) + 0.1
$$

$$
= 0.499725 + 0.2999955 + 0.19999992 + 0.1 = 1.09972042
$$

$$
\boxed{y_4 \approx 1.0997}
$$