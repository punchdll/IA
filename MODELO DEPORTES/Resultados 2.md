# Resultados

El modelo identifica con éxito las clases 1 y 5, pero el bajo recall en la clase 3 indica que se omiten muchos casos reales.

```
R1:
               precision    recall  f1-score   support

     Class 0       0.65      0.90      0.76      1918
     Class 1       0.97      1.00      0.99      1794
     Class 2       0.74      0.75      0.75      1530
     Class 3       0.77      0.36      0.49      1051
     Class 4       0.92      0.82      0.87      1536
     Class 5       0.95      0.99      0.97      1493
     Class 6       0.67      0.53      0.59      1863
     Class 7       0.79      0.88      0.84      1764
     Class 8       0.89      0.92      0.91      1440
     Class 9       0.92      0.92      0.92      1037

    accuracy                           0.82     15426
   macro avg       0.83      0.81      0.81     15426
weighted avg       0.82      0.82      0.81     15426
```

Hay una mejora ligera en la exactitud global. El desempeño de la clase 6 es más consistente que en la prueba anterior.

```
R2:
               precision    recall  f1-score   support

     Class 0       0.66      0.89      0.76      1973
     Class 1       0.99      1.00      0.99      1726
     Class 2       0.81      0.69      0.74      1577
     Class 3       0.77      0.39      0.52      1015
     Class 4       0.91      0.83      0.87      1547
     Class 5       0.97      0.99      0.98      1543
     Class 6       0.68      0.63      0.66      1851
     Class 7       0.80      0.91      0.85      1759
     Class 8       0.89      0.90      0.89      1400
     Class 9       0.93      0.92      0.92      1035

    accuracy                           0.83     15426
   macro avg       0.84      0.82      0.82     15426
weighted avg       0.83      0.83      0.82     15426
```

La detección de la clase 3 mejora notablemente, aunque sigue siendo el punto más débil del sistema.

```
R3:
               precision    recall  f1-score   support

     Class 0       0.65      0.92      0.76      1968
     Class 1       0.99      1.00      0.99      1790
     Class 2       0.82      0.75      0.78      1538
     Class 3       0.78      0.44      0.56      1006
     Class 4       0.90      0.84      0.87      1504
     Class 5       0.98      0.99      0.99      1600
     Class 6       0.69      0.51      0.59      1820
     Class 7       0.79      0.86      0.82      1733
     Class 8       0.86      0.91      0.88      1439
     Class 9       0.92      0.93      0.93      1028

    accuracy                           0.83     15426
   macro avg       0.84      0.82      0.82     15426
weighted avg       0.83      0.83      0.82     15426
```

La clase 9 alcanza una precisión alta, pero el rigor con la clase 3 vuelve a disminuir.

```
R4:
               precision    recall  f1-score   support

     Class 0       0.69      0.88      0.78      1987
     Class 1       0.98      1.00      0.99      1783
     Class 2       0.78      0.77      0.78      1553
     Class 3       0.81      0.33      0.47       975
     Class 4       0.91      0.82      0.86      1494
     Class 5       0.97      0.99      0.98      1545
     Class 6       0.64      0.56      0.60      1907
     Class 7       0.75      0.90      0.82      1733
     Class 8       0.87      0.90      0.89      1419
     Class 9       0.95      0.92      0.94      1030

    accuracy                           0.82     15426
   macro avg       0.84      0.81      0.81     15426
weighted avg       0.82      0.82      0.81     15426
```

Resultados equilibrados en las clases con mayor soporte, manteniendo la dificultad en la detección de la clase 3.

```
R5:
               precision    recall  f1-score   support

     Class 0       0.70      0.91      0.79      2005
     Class 1       0.98      1.00      0.99      1755
     Class 2       0.80      0.70      0.75      1547
     Class 3       0.81      0.32      0.46       980
     Class 4       0.90      0.82      0.86      1474
     Class 5       0.96      0.99      0.97      1526
     Class 6       0.63      0.65      0.64      1843
     Class 7       0.81      0.87      0.84      1809
     Class 8       0.88      0.92      0.90      1437
     Class 9       0.94      0.94      0.94      1050

    accuracy                           0.83     15426
   macro avg       0.84      0.81      0.81     15426
weighted avg       0.83      0.83      0.82     15426

```

El modelo es muy conservador con la clase 3: tiene pocos errores cuando la predice, pero falla al detectar la mayoría de sus instancias.

```
R6:
               precision    recall  f1-score   support

     Class 0       0.73      0.90      0.80      1926
     Class 1       0.97      1.00      0.99      1814
     Class 2       0.75      0.73      0.74      1540
     Class 3       0.89      0.25      0.40      1031
     Class 4       0.88      0.83      0.86      1509
     Class 5       0.96      0.99      0.98      1506
     Class 6       0.67      0.64      0.66      1843
     Class 7       0.73      0.86      0.79      1827
     Class 8       0.89      0.90      0.89      1452
     Class 9       0.94      0.95      0.95       978

    accuracy                           0.82     15426
   macro avg       0.84      0.81      0.80     15426
weighted avg       0.83      0.82      0.81     15426

```

Es el mejor desempeño general. Logra el equilibrio más alto entre precisión y detección en todas las categorías.

```
R7:

               precision    recall  f1-score   support

     Class 0       0.73      0.85      0.78      1971
     Class 1       0.98      1.00      0.99      1793
     Class 2       0.76      0.79      0.77      1554
     Class 3       0.84      0.45      0.58      1009
     Class 4       0.94      0.84      0.88      1473
     Class 5       0.97      0.99      0.98      1517
     Class 6       0.69      0.67      0.68      1897
     Class 7       0.81      0.90      0.85      1750
     Class 8       0.91      0.91      0.91      1459
     Class 9       0.93      0.95      0.94      1003

    accuracy                           0.84     15426
   macro avg       0.85      0.83      0.84     15426
weighted avg       0.85      0.84      0.84     15426
```

Rendimiento estándar. La clase 6 presenta dificultades de reconocimiento comparables a la primera prueba.

```
R8:

               precision    recall  f1-score   support

     Class 0       0.68      0.89      0.77      1992
     Class 1       0.97      1.00      0.99      1781
     Class 2       0.78      0.74      0.76      1590
     Class 3       0.75      0.40      0.52       994
     Class 4       0.88      0.82      0.84      1511
     Class 5       0.97      0.99      0.98      1489
     Class 6       0.66      0.53      0.59      1849
     Class 7       0.81      0.89      0.85      1780
     Class 8       0.86      0.94      0.90      1445
     Class 9       0.91      0.93      0.92       995

    accuracy                           0.82     15426
   macro avg       0.83      0.81      0.81     15426
weighted avg       0.82      0.82      0.81     15426
```

Mantiene la consistencia en las clases de alto rendimiento (1, 5, 8 y 9) sin variaciones significativas.

```
R9:

               precision    recall  f1-score   support

     Class 0       0.67      0.90      0.77      1905
     Class 1       0.97      1.00      0.99      1843
     Class 2       0.80      0.74      0.76      1508
     Class 3       0.75      0.38      0.50      1044
     Class 4       0.90      0.80      0.85      1520
     Class 5       0.95      0.99      0.97      1481
     Class 6       0.66      0.60      0.63      1863
     Class 7       0.79      0.85      0.82      1757
     Class 8       0.84      0.90      0.87      1464
     Class 9       0.93      0.93      0.93      1041

    accuracy                           0.82     15426
   macro avg       0.83      0.81      0.81     15426
weighted avg       0.82      0.82      0.81     15426
```

Es el rendimiento más bajo registrado. La confusión en la clase 6 penaliza el promedio general de esta iteración.

```
R10:

               precision    recall  f1-score   support

     Class 0       0.65      0.89      0.75      1906
     Class 1       0.98      1.00      0.99      1848
     Class 2       0.74      0.76      0.75      1524
     Class 3       0.71      0.31      0.43      1028
     Class 4       0.94      0.81      0.87      1554
     Class 5       0.95      0.99      0.97      1481
     Class 6       0.60      0.55      0.57      1858
     Class 7       0.83      0.89      0.86      1736
     Class 8       0.89      0.90      0.89      1447
     Class 9       0.93      0.93      0.93      1044

    accuracy                           0.81     15426
   macro avg       0.82      0.80      0.80     15426
weighted avg       0.82      0.81      0.81     15426
```