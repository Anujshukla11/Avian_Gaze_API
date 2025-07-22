import cv2
import datetime
import time

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open video capture
video = cv2.VideoCapture(0)
if not video.isOpened():
    print("Cannot open the camera")
    exit()

video_width = int(video.get(3))
video_height = int(video.get(4))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = None  # We'll create this later only if recording starts

face_detected_start = None
recording = False

print("Monitoring... Press 'q' to quit")

while True:
    ret, frame = video.read()
    if not ret:
        print("Cannot grab the frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=7, minSize=(80, 80), flags=cv2.CASCADE_SCALE_IMAGE
    )

    current_time = time.time()

    if len(faces) > 0:
        if face_detected_start is None:
            face_detected_start = current_time
        elif current_time - face_detected_start >= 5 and not recording:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            out = cv2.VideoWriter(f"recording_{timestamp}.avi", fourcc, 20.0, (video_width, video_height))
            recording = True
            print("🎥 Started recording...")

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        if recording:
            out.write(frame)

    else:
        face_detected_start = None
        if recording:
            print("🛑 Face lost. Stopping recording.")
            recording = False
            out.release()
            out = None

    cv2.imshow("Face Detection (Press 'q' to quit)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Program exited.")
        break

# Cleanup
if out is not None:
    out.release()
video.release()
cv2.destroyAllWindows()
