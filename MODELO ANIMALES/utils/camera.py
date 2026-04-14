import cv2
import os
import sys

def procesar_video_multiobjeto(ruta_video, dir_salida, ancho_out, alto_out, salto_frames=1):
    if not os.path.exists(dir_salida):
        os.makedirs(dir_salida)

    cap = cv2.VideoCapture(ruta_video)
    if not cap.isOpened():
        print(f"Error: No se pudo abrir {ruta_video}", file=sys.stderr)
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    cv2.namedWindow("Navegador de Video", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Navegador de Video", 800, 600)
    
    cv2.createTrackbar("Cuadro", "Navegador de Video", 0, total_frames - 1, lambda v: None)

    print("Busca el momento inicial.")
    print("Presiona ENTER para confirmar el cuadro. C para cancelar.")

    pos_actual = -1
    frame_inicio_img = None
    frame_idx = 0

    while True:
        pos_trackbar = cv2.getTrackbarPos("Cuadro", "Navegador de Video")
        
        if pos_trackbar != pos_actual:
            cap.set(cv2.CAP_PROP_POS_FRAMES, pos_trackbar)
            ret, frame = cap.read()
            if ret:
                frame_inicio_img = frame.copy()
                pos_actual = pos_trackbar
                
                display = frame_inicio_img.copy()
                cv2.putText(display, f"Cuadro: {pos_actual}/{total_frames}", (20, 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Navegador de Video", display)

        key = cv2.waitKey(30) & 0xFF
        if key in [13, 32]: 
            frame_idx = pos_actual
            break
        elif key in [ord('c'), ord('C')]:
            cap.release()
            cv2.destroyAllWindows()
            return

    cv2.destroyWindow("Navegador de Video")
    cv2.waitKey(1)

    cv2.namedWindow("Seleccion de objetivos", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Seleccion de objetivos", 800, 600)
    
    print("\n--- SELECCION MULTIPLE ---")
    bboxes = []
    frame_seleccion = frame_inicio_img.copy()

    while True:
        print(f"\nObjetivos guardados: {len(bboxes)}")
        print("1. Dibuja un recuadro y presiona ENTER para agregarlo.")
        print("2. Si ya terminaste, presiona ESC o ENTER sin dibujar nada para iniciar.")
        
        bbox = cv2.selectROI("Seleccion de objetivos", frame_seleccion, showCrosshair=True, fromCenter=False)
        
        if bbox[2] > 0 and bbox[3] > 0:
            bboxes.append(bbox)
            x, y, w, h = bbox
            cv2.rectangle(frame_seleccion, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame_seleccion, f"ID: {len(bboxes)-1}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        else:
            break

    cv2.destroyWindow("Seleccion de objetivos")
    cv2.waitKey(1)

    if len(bboxes) == 0:
        print("Error: Sin seleccion.", file=sys.stderr)
        cap.release()
        return
    trackers = []
    for bbox in bboxes:
        t = cv2.TrackerCSRT_create()
        t.init(frame_inicio_img, tuple(bbox))
        trackers.append(t)

    frames_guardados = 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx + 1)

    cv2.namedWindow("Rastreo y Guardado", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Rastreo y Guardado", 800, 600)
    print("\n--- CONTROLES ---")
    print("[p] : Pausar video y reajustar | [q] : Salir")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1
        frame_disp = frame.copy()
        alguna_perdida = False
        guardar_este_frame = (frame_idx % salto_frames == 0)

        for i, tracker in enumerate(trackers):
            ok, bbox = tracker.update(frame)

            if ok:
                x, y, w, h = [int(v) for v in bbox]
                cv2.rectangle(frame_disp, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame_disp, f"ID: {i}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                if guardar_este_frame:
                    x = max(0, x)
                    y = max(0, y)
                    w = min(frame.shape[1] - x, w)
                    h = min(frame.shape[0] - y, h)

                    if w > 0 and h > 0:
                        recorte = frame[y:y+h, x:x+w]
                        salida = cv2.resize(recorte, (ancho_out, alto_out))
                        ruta_img = os.path.join(dir_salida, f"id{i}_obj_{frames_guardados:05d}.jpg")
                        cv2.imwrite(ruta_img, salida)
            else:
                alguna_perdida = True

        if guardar_este_frame:
            frames_guardados += 1

        if alguna_perdida:
            cv2.putText(frame_disp, "PERDIDO - Presiona 'p'", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Rastreo y Guardado", frame_disp)

        key = cv2.waitKey(1) & 0xFF
        
        if key in [ord('q'), ord('Q'), 27]:
            break
        elif key in [ord('p'), ord('P')]:
            print(f"\nPAUSADO en cuadro {frame_idx}.")
            print("[a]: -5 cuadros | [d]: +5 cuadros | [s]: Seleccionar de nuevo")
            while True:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret_pausa, frame_pausa = cap.read()
                if not ret_pausa:
                    break

                display = frame_pausa.copy()
                cv2.putText(display, f"PAUSA - Cuadro: {frame_idx}", (20, 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.imshow("Rastreo y Guardado", display)

                k = cv2.waitKey(0) & 0xFF

                if k in [ord('c'), ord('C')]:
                    sys.exit(0)
                if k in [ord('a'), ord('A')]:
                    frame_idx = max(0, frame_idx - 5)
                elif k in [ord('d'), ord('D')]:
                    frame_idx = min(total_frames - 1, frame_idx + 5)
                elif k in [ord('s'), ord('S')]:
                    
                    print("\n--- REAJUSTE DE SELECCION ---")
                    nuevos_bboxes = []
                    frame_seleccion_pausa = frame_pausa.copy()
                    
                    while True:
                        print(f"Nuevos objetivos en cuadro {frame_idx}: {len(nuevos_bboxes)}")
                        nb = cv2.selectROI("Rastreo y Guardado", frame_seleccion_pausa, showCrosshair=True, fromCenter=False)
                        
                        if nb[2] > 0 and nb[3] > 0:
                            nuevos_bboxes.append(nb)
                            x, y, w, h = nb
                            cv2.rectangle(frame_seleccion_pausa, (x, y), (x+w, y+h), (255, 0, 0), 2)
                            cv2.putText(frame_seleccion_pausa, f"ID: {len(nuevos_bboxes)-1}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                        else:
                            break

                    if len(nuevos_bboxes) > 0:
                        trackers = []
                        for nb in nuevos_bboxes:
                            t = cv2.TrackerCSRT_create()
                            t.init(frame_pausa, tuple(nb))
                            trackers.append(t)
                        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx + 1)
                        print("Rastreo multiobjeto reanudado.")
                        break
                    else:
                        print("Seleccion vacia. Usa 'a'/'d' para cambiar cuadro o 's' para reintentar.")

    cap.release()
    cv2.destroyAllWindows()
    print(f"\nCompletado.")

if __name__ == '__main__':
    procesar_video_multiobjeto("frogs.mkv", "../animales/ranas", 128, 128, 5)