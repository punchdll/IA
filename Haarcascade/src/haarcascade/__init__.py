import sys
from pathlib import Path

import cv2 as cv

ESC_KEY = 27
SKIP_FRAMES = 8
FACE_SIZE = (64, 64)
WINDOW_SIZE = (960, 540)

PROJECT_DIR = Path.cwd()
VIDEO_PATH = PROJECT_DIR / "video" / "lula0.mp4"
IMAGES_PATH = PROJECT_DIR / "images"
CLASSIFIER_PATH = Path(__file__).resolve().with_name(
    "haarcascade_frontalface_alt.xml"
)


def main() -> None:
    classifier = cv.CascadeClassifier(str(CLASSIFIER_PATH))

    if classifier.empty():
        sys.exit(f'No se pudo cargar el clasificador "{CLASSIFIER_PATH.name}".')

    capture = cv.VideoCapture(str(VIDEO_PATH))

    if not capture.isOpened():
        sys.exit(f'No se pudo abrir el video "{VIDEO_PATH.name}".')

    with capture:
        ok, frame = capture.read()

        if not ok:
            sys.exit("No se pudo leer el primer fotograma.")

        region = select_region(frame)

        if region[2] == 0 or region[3] == 0:
            sys.exit("No se seleccionó ninguna zona.")

        IMAGES_PATH.mkdir(exist_ok=True)
        saved = capture_faces(capture, classifier, region)

    print(f"Se guardaron {saved} rostros en {IMAGES_PATH}")


def select_region(frame) -> tuple[int, int, int, int]:
    window = "Seleccionar Zona"

    cv.namedWindow(window, cv.WINDOW_NORMAL)
    cv.resizeWindow(window, *WINDOW_SIZE)
    cv.imshow(window, frame)
    cv.waitKey(1)

    region = cv.selectROI(window, frame, showCrosshair=True, fromCenter=False)
    cv.destroyWindow(window)

    x, y, w, h = map(int, region)
    return x, y, w, h


def capture_faces(capture, classifier, region) -> int:
    x, y, w, h = region
    window = "Captura de rostros"

    cv.namedWindow(window, cv.WINDOW_NORMAL)
    cv.resizeWindow(window, *WINDOW_SIZE)

    saved = 0

    while True:
        for _ in range(SKIP_FRAMES):
            if not capture.grab():
                return saved

        ok, frame = capture.read()

        if not ok:
            return saved

        area = frame[y:y + h, x:x + w]
        gray = cv.cvtColor(area, cv.COLOR_BGR2GRAY)

        faces = classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
        )

        for fx, fy, fw, fh in faces:
            face = area[fy:fy + fh, fx:fx + fw]
            face = cv.resize(face, FACE_SIZE, interpolation=cv.INTER_AREA)

            cv.imwrite(str(IMAGES_PATH / f"rostro_{saved:05d}.png"), face)
            saved += 1

            cv.rectangle(
                frame,
                (x + fx, y + fy),
                (x + fx + fw, y + fy + fh),
                (0, 255, 0),
                2,
            )

        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv.imshow(window, frame)

        if cv.waitKey(1) & 0xFF == ESC_KEY:
            return saved

        if window_closed(window):
            return saved


def window_closed(window: str) -> bool:
    try:
        return cv.getWindowProperty(window, cv.WND_PROP_VISIBLE) < 1
    except cv.error:
        return True
