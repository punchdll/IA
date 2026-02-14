tamano = 4
costo_lado = 10
costo_diagonal = 14

lista_abierta = []
lista_cerrada = []


def calcular_costo_de_movimiento(x: int, y: int) -> int:
    return costo_lado if x == 0 or y == 0 else costo_diagonal


def manhattan(origen_x: int, origen_y: int, destino_x: int, destino_y: int) -> int:
    componente_x = abs(origen_x - destino_x)
    componente_y = abs(origen_y - destino_y)
    return costo_lado * (componente_x + componente_y)
