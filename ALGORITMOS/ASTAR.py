from base import lista_abierta, lista_cerrada, manhattan, tamano
from nodo import Nodo


def definir_origen(x: int, y: int, destino: Nodo, cuadricula: list) -> Nodo:
    cuadricula[y][x] = Nodo(x, y, heuristica=manhattan(x, y, destino.x, destino.y))
    return cuadricula[y][x]


def definir_destino(x: int, y: int, cuadricula: list) -> Nodo:
    cuadricula[y][x] = Nodo(x, y)
    return cuadricula[y][x]


def definir_obstaculo(x: int, y: int, cuadricula: list):
    cuadricula[y][x] = Nodo(x, y, obstaculo=True)


def main():

    cuadricula = [[Nodo(x, y) for x in range(tamano)] for y in range(tamano)]

    nodo_destino = definir_destino(3, 0, cuadricula)

    nodo_origen = definir_origen(0, 0, nodo_destino, cuadricula)

    definir_obstaculo(1, 0, cuadricula)
    definir_obstaculo(1, 1, cuadricula)
    definir_obstaculo(1, 3, cuadricula)

    lista_abierta.append(nodo_origen)

    while True:
        if lista_abierta == []:
            break

        lista_abierta.sort(key=lambda x: x.costo_estimado)

        nodo_actual = lista_abierta.pop(0)

        if nodo_actual == nodo_destino:
            print("Busqueda finalizada")
            print("Nodo origen: ", nodo_origen)
            print("Nodo destino: ", nodo_destino)
            print("Ruta: ")
            print(nodo_origen)
            ruta = []

            while not nodo_actual == lista_cerrada[0]:
                ruta.append(nodo_actual)
                nodo_actual = nodo_actual.padre

            ruta.reverse()

            for i in ruta:
                print(i)
            break

        nodo_actual.descubrir(cuadricula, lista_abierta, nodo_destino)

        lista_cerrada.append(nodo_actual)


if __name__ == "__main__":
    main()
