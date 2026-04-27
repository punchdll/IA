import os
import shutil
from PIL import Image
import numpy as np

def es_imagen_mala(ruta_imagen, umbral_pixel=50, porcentaje=0.7, umbral_contraste=20):
    try:
        with Image.open(ruta_imagen) as img:
            img = img.convert("L")
            arr = np.array(img)

            # % de píxeles oscuros
            pixeles_oscuros = np.sum(arr < umbral_pixel)
            ratio_oscuros = pixeles_oscuros / arr.size

            # contraste
            contraste = arr.std()

            if ratio_oscuros > porcentaje or contraste < umbral_contraste:
                return True
            return False

    except Exception as e:
        print(f"Error con {ruta_imagen}: {e}")
        return False


def mover_seguro(origen, destino):
    base = os.path.basename(origen)
    nombre, ext = os.path.splitext(base)
    contador = 1

    ruta_final = os.path.join(destino, base)

    # evitar sobrescribir
    while os.path.exists(ruta_final):
        ruta_final = os.path.join(destino, f"{nombre}_{contador}{ext}")
        contador += 1

    shutil.move(origen, ruta_final)


def limpiar_dataset(carpeta_origen, carpeta_destino):
    extensiones = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
    os.makedirs(carpeta_destino, exist_ok=True)

    total = 0
    movidas = 0

    for archivo in os.listdir(carpeta_origen):
        ruta = os.path.join(carpeta_origen, archivo)

        if archivo.lower().endswith(extensiones):
            total += 1

            if es_imagen_mala(ruta):
                mover_seguro(ruta, carpeta_destino)
                movidas += 1
                print(f"Movida: {archivo}")
            else:
                print(f"OK: {archivo}")

    print("\n--- RESUMEN ---")
    print(f"Total analizadas: {total}")
    print(f"Movidas: {movidas}")
    print(f"Conservadas: {total - movidas}")


if __name__ == "__main__":
    carpeta_imagenes = "ballenas"
    carpeta_descartes = "ballenas/recicle"

    limpiar_dataset(carpeta_imagenes, carpeta_descartes)