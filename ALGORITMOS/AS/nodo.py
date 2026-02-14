from base import (
    calcular_costo_de_movimiento,
    lista_abierta,
    lista_cerrada,
    manhattan,
    tamano,
)


class Nodo:
    def __init__(self, x: int, y: int, heuristica=0, obstaculo=False) -> None:
        self.x = x
        self.y = y
        self.costo_de_ruta = 0
        self.heuristica = heuristica
        self.costo_estimado = 0
        self.padre = None
        self.obstaculo = obstaculo

    def __str__(self) -> str:
        return f"POS: ({self.x}, {self.y}) CE: (({self.costo_de_ruta}, {self.heuristica}) --> {self.costo_estimado})"

    def _descubrir(
        self,
        x: int,
        y: int,
        cuadricula: list,
        nodo_destino: "Nodo",
    ) -> object:

        indice_x = self.x + x
        indice_y = self.y + y

        # Verificamos no salirnos de la rejilla
        if (indice_x < 0 or indice_y < 0) or (indice_x > tamano or indice_y > tamano):
            return None

        nodo = cuadricula[indice_y][indice_x]

        if nodo.obstaculo:
            return None

        if nodo in lista_cerrada:
            return None

        costo_de_movimiento = calcular_costo_de_movimiento(indice_x, indice_y)

        costo_de_ruta = self.costo_de_ruta + costo_de_movimiento

        # Si no tiene padre el que lo descubrio se hace su padre
        if nodo not in lista_abierta:
            nodo.padre = self
            nodo.heuristica = manhattan(nodo.x, nodo.y, nodo_destino.x, nodo_destino.y)
            nodo.costo_de_ruta = costo_de_ruta
            nodo.costo_estimado = nodo.costo_de_ruta + nodo.heuristica
            lista_abierta.append(nodo)
            return nodo

        # Si no verificamos si podemos mejorar el costo del camino
        else:
            if costo_de_ruta < nodo.costo_de_ruta:
                nodo.costo_de_ruta = self.costo_de_ruta + costo_de_movimiento
                nodo.padre = self
                nodo.costo_estimado = nodo.costo_de_ruta + nodo.heuristica
                return nodo

    def descubrir(self, cuadricula: list, lista_abierta: list, nodo_destino: "Nodo"):
        indices_de_movimientos = [
            [-1, -1],
            [-1, 0],
            [-1, 1],
            [0, -1],
            [0, 1],
            [1, -1],
            [1, 0],
            [1, 1],
        ]
        for par in indices_de_movimientos:
            self._descubrir(par[0], par[1], cuadricula, nodo_destino)
