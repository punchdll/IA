from Casilla import Casilla


class Tablero:
    def __init__(self, espacios=3) -> None:
        self.espacios = espacios

        self._tablero = [
            [Casilla() for _ in range(self.espacios)] for _ in range(self.espacios)
        ]

    def get(self) -> list:
        return self._tablero

    def change(self, x: int, y: int, propietario: str) -> None:
        if not (0 <= x < self.espacios and 0 <= y < self.espacios):
            raise IndexError("El valor sale de los limites del tablero")
        if not self.comprobar_casilla(x, y):
            raise Exception("Casilla ocupada")

        self._tablero[x][y].propietario = propietario

    def comprobar_tablero(self) -> bool:
        for filas in self.get():
            for casilla in filas:
                if casilla.propietario == "#":
                    return True
        return False

    def imprimir_tablero(self) -> None:
        print("Tablero actual: ")
        for fila in self.get():
            for casilla in fila:
                print(f"{casilla.propietario}\t", end="")
            print("\n")

    def comprobar_casilla(self, x: int, y: int) -> bool:
        if self.get()[x][y].propietario == "#":
            return True
        else:
            return False

    def comprobar_ganador(self, jugador: str) -> bool:
        self.get()

        # Filas
        for i in range(self.espacios):
            if all(
                self.get()[i][j].propietario == jugador for j in range(self.espacios)
            ):
                return True

        # Columnas
        for j in range(self.espacios):
            if all(
                self.get()[i][j].propietario == jugador for i in range(self.espacios)
            ):
                return True

        # Diagonal principal
        if all(self.get()[i][i].propietario == jugador for i in range(self.espacios)):
            return True

        # Diagonal secundaria
        if all(
            self.get()[i][self.espacios - 1 - i].propietario == jugador
            for i in range(self.espacios)
        ):
            return True
        return False
