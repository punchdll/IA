"""Reconoce rostros en un video (o cámara) con el modelo Eigenfaces entrenado."""

import argparse
import json
import sys
from pathlib import Path

import cv2 as cv

ESC_KEY = 27
SCALE = 0.5  # se procesa a media resolución para que la detección sea más rápida
# En Eigenfaces, menor confianza = mejor coincidencia. Calibrado con la
# precisión p99 del conjunto de prueba (~1280) y las detecciones del video (~1010).
CONFIDENCE_THRESHOLD = 2000.0
WINDOW_SIZE = (960, 540)

PROJECT_DIR = Path(__file__).resolve().parents[2]
VIDEO_PATH = PROJECT_DIR / "video" / "video.mp4"
MODEL_PATH = PROJECT_DIR / "models" / "eigenface.xml"
LABELS_PATH = PROJECT_DIR / "models" / "eigenface_labels.json"
CASCADE_PATH = Path(__file__).resolve().with_name(
    "haarcascade_frontalface_alt.xml"
)


def main() -> None:
    args = parse_args()

    if not MODEL_PATH.exists() or not LABELS_PATH.exists():
        sys.exit(
            f'No se encontró el modelo en "{MODEL_PATH}". '
            "Ejecuta primero: uv run fit"
        )

    labels = json.loads(LABELS_PATH.read_text(encoding="utf-8"))
    names: list[str] = labels["names"]
    image_size = tuple(labels.get("image_size", (64, 64)))

    recognizer = cv.face.EigenFaceRecognizer_create()
    recognizer.read(str(MODEL_PATH))

    cascade = cv.CascadeClassifier(str(CASCADE_PATH))

    if cascade.empty():
        sys.exit(f'No se pudo cargar el clasificador "{CASCADE_PATH.name}".')

    source = args.source
    capture = cv.VideoCapture(int(source) if source.isdigit() else source)

    if not capture.isOpened():
        sys.exit(f'No se pudo abrir la fuente "{source}".')

    window = "Reconocimiento de rostros"
    cv.namedWindow(window, cv.WINDOW_NORMAL)
    cv.resizeWindow(window, *WINDOW_SIZE)

    with capture:
        while True:
            ok, frame = capture.read()

            if not ok:
                break

            frame = cv.resize(
                frame, None, fx=SCALE, fy=SCALE, interpolation=cv.INTER_AREA
            )
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            faces = cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(40, 40),
            )

            for x, y, w, h in faces:
                face = cv.resize(
                    gray[y:y + h, x:x + w],
                    image_size,
                    interpolation=cv.INTER_AREA,
                )
                predicted, confidence = recognizer.predict(face)

                if predicted != -1 and confidence <= CONFIDENCE_THRESHOLD:
                    text = f"{names[predicted]} ({confidence:.0f})"
                    color = (0, 255, 0)
                else:
                    text = f"Desconocido ({confidence:.0f})"
                    color = (0, 0, 255)

                cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv.putText(
                    frame,
                    text,
                    (x, y - 10),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2,
                    cv.LINE_AA,
                )

            cv.imshow(window, frame)

            if cv.waitKey(1) & 0xFF == ESC_KEY:
                break

            if window_closed(window):
                break

    cv.destroyAllWindows()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reconoce rostros en un video o cámara con Eigenfaces."
    )
    parser.add_argument(
        "source",
        nargs="?",
        default=str(VIDEO_PATH),
        help="ruta del video, o el índice de la cámara (por ejemplo 0)",
    )
    return parser.parse_args()


def window_closed(window: str) -> bool:
    try:
        return cv.getWindowProperty(window, cv.WND_PROP_VISIBLE) < 1
    except cv.error:
        return True


if __name__ == "__main__":
    main()
