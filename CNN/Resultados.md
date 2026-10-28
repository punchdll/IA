
# Resulados

> Las pruebas son incrementales.

## Prueba 1

Usando arquitectura original, `learning rate de 0.001` y `20 épocas`.

```
precision    recall  f1-score   support

     Class 0       0.83      0.40      0.54      1039
     Class 1       0.98      1.00      0.99      1842
     Class 2       0.65      0.64      0.65      1901
     Class 3       0.74      0.84      0.78      1954
     Class 4       0.93      0.93      0.93      1007
     Class 5       0.75      0.83      0.79      1777
     Class 6       0.82      0.92      0.86      1418
     Class 7       0.77      0.77      0.77      1544
     Class 8       0.90      0.82      0.85      1459
     Class 9       0.96      0.99      0.97      1485

    accuracy                           0.82     15426
   macro avg       0.83      0.81      0.81     15426
weighted avg       0.82      0.82      0.82     15426


```

## Prueba 2

Usando arquitectura original, `learning rate de 0.004` y `50 épocas`.

```
precision    recall  f1-score   support

     Class 0       0.94      0.94      0.94      1027
     Class 1       1.00      1.00      1.00      1791
     Class 2       0.95      0.88      0.91      1889
     Class 3       0.92      0.98      0.95      1969
     Class 4       0.99      1.00      0.99      1055
     Class 5       0.96      0.96      0.96      1738
     Class 6       0.96      0.99      0.98      1417
     Class 7       0.95      0.97      0.96      1516
     Class 8       0.99      0.96      0.97      1477
     Class 9       0.99      1.00      1.00      1547

    accuracy                           0.96     15426
   macro avg       0.97      0.97      0.97     15426
weighted avg       0.96      0.96      0.96     15426

```

## Prueba 3

Usando arquitectura original, `learning rate de 0.004`, `50 épocas` y `optimizador adam`.

```
precision    recall  f1-score   support

     Class 0       1.00      0.98      0.99      1047
     Class 1       1.00      1.00      1.00      1744
     Class 2       0.97      0.97      0.97      1886
     Class 3       0.97      0.99      0.98      1976
     Class 4       1.00      1.00      1.00      1051
     Class 5       1.00      0.99      0.99      1715
     Class 6       0.99      1.00      0.99      1353
     Class 7       0.99      0.99      0.99      1581
     Class 8       1.00      0.99      0.99      1531
     Class 9       1.00      1.00      1.00      1542

    accuracy                           0.99     15426
   macro avg       0.99      0.99      0.99     15426
weighted avg       0.99      0.99      0.99     15426

```

## Prueba 4

Usando arquitectura original, `learning rate de 0.004`, `50 épocas`, `optimizador SGD` y `dropout reducido a 0.2`.

```
precision    recall  f1-score   support

     Class 0       0.96      0.95      0.96      1027
     Class 1       1.00      1.00      1.00      1777
     Class 2       0.96      0.95      0.95      1820
     Class 3       0.97      0.99      0.98      2002
     Class 4       1.00      1.00      1.00      1072
     Class 5       0.99      0.97      0.98      1808
     Class 6       0.99      0.99      0.99      1379
     Class 7       0.96      0.98      0.97      1558
     Class 8       0.99      0.98      0.99      1513
     Class 9       1.00      1.00      1.00      1470

    accuracy                           0.98     15426
   macro avg       0.98      0.98      0.98     15426
weighted avg       0.98      0.98      0.98     15426

```

## Prueba 5

Usando arquitectura original, `learning rate de 0.004`, `50 épocas`, `optimizador SGD` y `dropout reducido a 0.2`con capa de convolución extra.

```
precision    recall  f1-score   support

     Class 0       0.97      0.91      0.94      1097
     Class 1       1.00      1.00      1.00      1732
     Class 2       0.94      0.92      0.93      1831
     Class 3       0.95      0.98      0.97      1987
     Class 4       1.00      1.00      1.00      1066
     Class 5       0.99      0.98      0.98      1763
     Class 6       0.98      1.00      0.99      1378
     Class 7       0.95      0.98      0.96      1530
     Class 8       0.99      0.98      0.99      1539
     Class 9       1.00      1.00      1.00      1503

    accuracy                           0.97     15426
   macro avg       0.98      0.97      0.98     15426
weighted avg       0.97      0.97      0.97     15426

```