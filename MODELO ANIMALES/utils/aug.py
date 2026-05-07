import os
import cv2
import albumentations as A
import random

# =========================
# CONFIG
# =========================
INPUT_DIR = "changos_128_crop"
OUTPUT_DIR = "changos_aug"
TARGET = 10000

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# PIPELINE DE AUGMENTACIÓN
# =========================
transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.Rotate(limit=25, p=0.5),
    A.RandomBrightnessContrast(p=0.5),
    A.HueSaturationValue(p=0.3),
])

files = os.listdir(INPUT_DIR)

print(f"\n🔄 Augmentando desde {len(files)} imágenes...")

count = 0

while count < TARGET:
    for f in files:
        try:
            path = os.path.join(INPUT_DIR, f)

            img = cv2.imread(path)

            if img is None:
                continue

            augmented = transform(image=img)["image"]

            cv2.imwrite(f"{OUTPUT_DIR}/{count}.jpg", augmented)

            count += 1

            if count >= TARGET:
                break

        except:
            pass

print(f"\n✅ Dataset aumentado listo: {count}")
