costo_lado = 10
costo_diagonal = 14


class Nodo:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.origen = False
        self.costo_de_ruta = 0
        self.heuristica = 0
        self.costo_estimado = 0
        self.padre = None

    def __str__(self) -> str:
        return f"POS: ({self.x}, {self.y}) CE: (({self.costo_de_ruta}, {self.heuristica}) --> {self.costo_estimado})"

    def manhattan(self, origen, destino) -> int:
        componente_x = abs(destino.x - origen.x)
        componente_y = abs(destino.y - origen.y)
        return costo_lado * (componente_x + componente_y)

    def _descubrir(
        self,
        x: int,
        y: int,
        cuadricula: list,
        lista_abierta: list,
        nodo_destino: object,
    ) -> object:

        indice_x = self.x + x
        indice_y = self.y + y

        # Verificamos no salirnos de la rejilla
        if indice_x < 0 or indice_y < 0:
            return None

        costo_de_movimiento = costo_lado if x == 0 or y == 0 else costo_diagonal

        try:
            nodo = cuadricula[indice_y][indice_x]
            nodo.heuristica = self.manhattan(nodo, nodo_destino)

            # Si no tiene padre el que lo descubrio se hace su padre
            if not nodo.padre and not nodo.origen:
                nodo.padre = self
                nodo.costo_de_ruta = self.costo_de_ruta + costo_de_movimiento
                nodo.costo_estimado = nodo.costo_de_ruta + nodo.heuristica
                lista_abierta.append(nodo)
                return nodo

            # Si no verificamos si podemos mejorar el costo del camino
            else:
                if (
                    self.costo_de_ruta + costo_de_movimiento < nodo.costo_de_ruta
                    and not nodo.origen
                ):
                    nodo.costo_de_ruta = self.costo_de_ruta + costo_de_movimiento
                    nodo.padre = self
                    nodo.costo_estimado = nodo.costo_de_ruta + nodo.heuristica
                    return nodo
        except IndexError:
            return None

    def descubrir(self, cuadricula: list, lista_abierta: list, nodo_destino: object):
        indices = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        for par in indices:
            self._descubrir(*par, cuadricula, lista_abierta, nodo_destino)


def main():
    tamano = 9

    cuadricula = [[Nodo(x, y) for x in range(tamano)] for y in range(tamano)]

    nodo_origen = cuadricula[0][0]
    nodo_destino = cuadricula[1][3]

    print("Nodo origen: ", nodo_origen)
    print("Nodo destino: ", nodo_destino)
    nodo_origen.origen = True

    lista_abierta = [nodo_origen]
    lista_cerrada = []

    while True:
        if lista_abierta == []:
            break

        lista_abierta.sort(key=lambda x: x.costo_estimado)

        nodo_actual = lista_abierta.pop(0)

        if nodo_actual == nodo_destino:
            print("Busqueda finalizada")
            print("Ruta: ")
            ruta = []

            while not nodo_actual.origen:
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
