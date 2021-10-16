import cv2

video = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.1, minNeighbors=10, minSize=(100, 100))
    # draw frame
    for xmin, ymin, w, h in faces:
        cv2.rectangle(frame, (xmin, ymin), (xmin+w, ymin+h), (0, 255, 0), 3)
    # show
    cv2.imshow('frame', frame)
    key = cv2.waitKey(2)
    if key & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
