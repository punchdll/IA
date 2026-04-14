import cv2
import os
import glob
import albumentations as A

def aumentar_datos(dir_entrada, dir_salida, multiplicador=5):
    """
    Lee imagenes, aplica transformaciones aleatorias y guarda 'multiplicador' 
    versiones nuevas por cada imagen original.
    """
    if not os.path.exists(dir_salida):
        os.makedirs(dir_salida)

    
    transformacion = A.Compose([
        A.HorizontalFlip(p=0.5),
        A.Rotate(limit=15, p=0.7),
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.6),
        A.GaussianBlur(blur_limit=(3, 5), p=0.2)
    ])

    patron_busqueda = os.path.join(dir_entrada, "*.jpg")
    rutas_img = glob.glob(patron_busqueda)

    if not rutas_img:
        print(f"Error: No se encontraron imagenes .jpg en {dir_entrada}")
        return

    imagenes_generadas = 0

    for ruta in rutas_img:
        nombre_base = os.path.basename(ruta).split('.')[0]
        
        imagen = cv2.imread(ruta)
        if imagen is None:
            continue
        
        cv2.imwrite(os.path.join(dir_salida, f"{nombre_base}_orig.jpg"), imagen)
        imagenes_generadas += 1

        for i in range(multiplicador):
            resultado = transformacion(image=imagen)
            img_aumentada = resultado['image']
            
            ruta_salida = os.path.join(dir_salida, f"{nombre_base}_aug_{i:02d}.jpg")
            cv2.imwrite(ruta_salida, img_aumentada)
            imagenes_generadas += 1

    print(f"Completado. Originales: {len(rutas_img)}. Generadas en total: {imagenes_generadas}.")

if __name__ == '__main__':
    aumentar_datos("animales/ranas", "animales/ranas_aumentadas", multiplicador=40)