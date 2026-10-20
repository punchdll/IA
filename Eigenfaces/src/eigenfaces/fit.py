"""Entrena un reconocedor de rostros Eigenfaces con el dataset de images/."""

import json
import sys
from pathlib import Path

import cv2 as cv
import numpy as np

IMAGE_SIZE = (64, 64)
TEST_SIZE = 0.2
SEED = 42
NUM_COMPONENTS = 150
MAX_IMAGES_PER_PERSON = 150

PROJECT_DIR = Path(__file__).resolve().parents[2]
IMAGES_PATH = PROJECT_DIR / "images"
MODELS_PATH = PROJECT_DIR / "models"
MODEL_PATH = MODELS_PATH / "eigenface.xml"
LABELS_PATH = MODELS_PATH / "eigenface_labels.json"


def main() -> None:
    faces, labels, names = load_dataset(IMAGES_PATH)

    if not faces:
        sys.exit(f'No se encontraron imágenes en "{IMAGES_PATH}".')

    train_faces, train_labels, test_faces, test_labels = split_dataset(
        faces, labels
    )

    print(f"Entrenando con {len(train_faces)} imágenes...")

    recognizer = cv.face.EigenFaceRecognizer_create(NUM_COMPONENTS)
    recognizer.train(train_faces, train_labels)

    accuracy = evaluate(recognizer, test_faces, test_labels, names)
    print(f"Precisión en prueba: {accuracy:.2%}")

    MODELS_PATH.mkdir(exist_ok=True)
    recognizer.write(str(MODEL_PATH))

    LABELS_PATH.write_text(
        json.dumps(
            {"names": names, "image_size": list(IMAGE_SIZE)},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"Modelo guardado en {MODEL_PATH}")
    print(f"Etiquetas guardadas en {LABELS_PATH}")


def load_dataset(
    images_path: Path,
) -> tuple[list[np.ndarray], np.ndarray, list[str]]:
    person_dirs = sorted(path for path in images_path.iterdir() if path.is_dir())

    if not person_dirs:
        return [], np.array([], dtype=np.int32), []

    faces: list[np.ndarray] = []
    labels: list[int] = []
    names: list[str] = []

    for label, person_dir in enumerate(person_dirs):
        names.append(person_dir.name)
        person_faces = 0

        for image_path in sorted(person_dir.iterdir()):
            image = cv.imread(str(image_path), cv.IMREAD_GRAYSCALE)

            if image is None:
                print(f"Advertencia: no se pudo leer {image_path}", file=sys.stderr)
                continue

            if image.shape[::-1] != IMAGE_SIZE:
                image = cv.resize(image, IMAGE_SIZE, interpolation=cv.INTER_AREA)

            faces.append(image)
            labels.append(label)
            person_faces += 1

        print(f"{person_dir.name}: {person_faces} imágenes")

    return faces, np.array(labels, dtype=np.int32), names


def split_dataset(
    faces: list[np.ndarray],
    labels: np.ndarray,
) -> tuple[list[np.ndarray], np.ndarray, list[np.ndarray], np.ndarray]:
    """Divide por persona y limita las muestras de entrenamiento por clase."""
    rng = np.random.default_rng(SEED)
    train_indices: list[int] = []
    test_indices: list[int] = []

    for label in np.unique(labels):
        indices = np.flatnonzero(labels == label)
        rng.shuffle(indices)

        test_count = max(1, int(round(len(indices) * TEST_SIZE)))
        test_indices.extend(indices[:test_count])
        train_indices.extend(
            indices[test_count:test_count + MAX_IMAGES_PER_PERSON]
        )

    rng.shuffle(train_indices)
    rng.shuffle(test_indices)

    train_faces = [faces[i] for i in train_indices]
    test_faces = [faces[i] for i in test_indices]

    return (
        train_faces,
        labels[train_indices],
        test_faces,
        labels[test_indices],
    )


def evaluate(
    recognizer: cv.face.BasicFaceRecognizer,
    faces: list[np.ndarray],
    labels: np.ndarray,
    names: list[str],
) -> float:
    if not faces:
        return 0.0

    correct = 0
    per_person_correct = np.zeros(len(names), dtype=int)
    per_person_total = np.zeros(len(names), dtype=int)

    for face, expected in zip(faces, labels):
        predicted, _confidence = recognizer.predict(face)
        per_person_total[expected] += 1

        if predicted == expected:
            correct += 1
            per_person_correct[expected] += 1

    print("\nPrecisión por persona:")
    for label, name in enumerate(names):
        total = per_person_total[label]
        accuracy = per_person_correct[label] / total if total else 0.0
        print(f"  {name}: {accuracy:.2%} ({per_person_correct[label]}/{total})")

    return correct / len(faces)


if __name__ == "__main__":
    main()
