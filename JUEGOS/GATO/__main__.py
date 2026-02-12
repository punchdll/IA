import time

from Tablero import Tablero


def main():
    orden = None
    tablero = Tablero()

    while orden is None or (orden != "H" and orden != "M"):
        orden = input("¿Quién empieza?: (H/M): ")

    print(f"Empieza {'Humano' if orden == 'H' else 'Maquina'}.")

    while True:
        tablero.comprobar_tablero()

        tablero.imprimir_tablero()

        if orden == "H":
            while True:
                eleccion = input("Elige una de las casillas disponibles (x, y): ")
                eleccion = eleccion.split(",")

                try:
                    # Ajustamos la cuadricula para iniciar en 1,1
                    x = int(eleccion[0]) - 1
                    y = int(eleccion[1]) - 1

                    tablero.change(x, y, "H")
                except IndexError as e:
                    print(e)
                except ValueError:
                    print("Introduce valores validos de acuerdo al formato")
                except Exception as e:
                    print(e)
                else:
                    print("Operacion realizada")

                if tablero.comprobar_ganador("H"):
                    tablero.imprimir_tablero()
                    print("El humano gana")
                    return

                if tablero.comprobar_ganador("M"):
                    tablero.imprimir_tablero()
                    print("La maquina gana")
                    return

                tablero.imprimir_tablero()
                time.sleep(0.5)


if __name__ == "__main__":
    main()
