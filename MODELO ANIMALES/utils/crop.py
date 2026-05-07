import os
from PIL import Image, UnidentifiedImageError
from tqdm import tqdm

INPUT_DIR = "changos_raw"
OUTPUT_DIR = "changos_128_crop"
SIZE = (128, 128)

os.makedirs(OUTPUT_DIR, exist_ok=True)

def center_crop(img, size):
    width, height = img.size
    new_width, new_height = size

    scale = max(new_width / width, new_height / height)

    img = img.resize(
        (int(width * scale), int(height * scale)),
        Image.Resampling.LANCZOS
    )

    left = (img.width - new_width) // 2
    top = (img.height - new_height) // 2
    right = left + new_width
    bottom = top + new_height

    return img.crop((left, top, right, bottom))


print("🔄 Aplicando crop centrado (con validación)...")

valid = 0
skipped = 0

for file in tqdm(os.listdir(INPUT_DIR)):
    path = os.path.join(INPUT_DIR, file)
    out_path = os.path.join(OUTPUT_DIR, file)

    try:
        # 🔥 validación fuerte de imagen
        with Image.open(path) as img:
            img.verify()

        # reabrir (verify deja el archivo inutilizable)
        img = Image.open(path).convert("RGB")

        img = center_crop(img, SIZE)

        img.save(out_path, quality=95)
        valid += 1

    except (UnidentifiedImageError, OSError, ValueError) as e:
        skipped += 1
        # opcional: borrar corruptas
        try:
            os.remove(path)
        except:
            pass

    except Exception:
        skipped += 1

print("\n✅ Terminado")
print(f"✔ Procesadas: {valid}")
print(f"❌ Ignoradas/eliminadas: {skipped}")
