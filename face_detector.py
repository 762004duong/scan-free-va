import cv2
import multiprocessing

from assistant import assistant_process

video = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
is_va_running = False
th = None

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    frame_h, frame_w, frame_c = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = detector.detectMultiScale(gray, 1.1, minNeighbors=10, minSize=(100, 100))

    if th is not None:
        is_va_running = th.is_alive()

    is_turn_va = False

    for xmin, ymin, w, h in face:
        cv2.rectangle(frame, (xmin, ymin), (xmin + w, ymin + h), (0, 255, 0), 3)
        if w / frame_w > 0.2:
            is_turn_va = True

    # Run assistant
    if (not is_va_running) and is_turn_va:
        is_va_running = True
        th = multiprocessing.Process(target=assistant_process)
        th.start()

    cv2.imshow('frame', frame)
    key = cv2.waitKey(2)
    if key & 0xFF == ord('q'):
        th.terminate()
        break

cv2.destroyAllWindows()
