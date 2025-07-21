import cv2
import dlib
import numpy as np
import time
from datetime import datetime 
import os

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(r"C:\Users\Jayendra\Downloads\shape_predictor_68_face_landmarks.dat\shape_predictor_68_face_landmarks.dat")

GAZE_TRIGGER_SECONDS = 3
FACE_AREA_TRESHOLD = 5000

def get_head_tilt(landmarks):
    left_point = (landmarks.part(36).x , landmarks.part(36).y)
    right_point = (landmarks.part(45).x , landmarks.part(45).y)

    delta_y = right_point[1] - left_point[1]
    delta_x = right_point[0] - left_point[0]

    angle = np.degrees(np.arctan2(delta_y , delta_x))
    return angle
def start_recording():
    video = cv2.VideoCapture(0)
    gaze_start_time = None
    recording = False
    out = None
    while True:
        ret, frame = video.read()

        if not ret:
            print("Unable to grab the frame\n")
            break

        gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray,face)
            face_area = face.width() * face.height()

            if face_area < FACE_AREA_TRESHOLD:
                tilt = get_head_tilt(landmarks)
                if abs(tilt) < 10:
                    status = "Staring (fallback)\n"
                else:
                    status = "Not Staring\n"

            else:
                left_eye = np.array([(landmarks.part(i).x , landmarks.part(i).y) for i in range(36,42)])
                right_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42 , 48)])

                def get_gaze_ratio(eye_points):
                    min_x = np.min(eye_points[:,0])
                    max_x = np.max(eye_points[:,0])
                    min_y = np.min(eye_points[:,1])
                    max_y = np.max(eye_points[:,1])

                    eye = gray[min_y:max_y , min_x:max_x]
                    _, tresh = cv2.threshold(eye,70,255,cv2.THRESH_BINARY)
                    h,w = tresh.shape
                    left = tresh[:, :w//2]
                    right = tresh[:, w//2: ]

                    if cv2.countNonZero(right) == 0:
                        return 5
                    if cv2.countNonZero(left) == 0:
                        return 1
                    return cv2.countNonZero(left) / cv2.countNonZero(right)
                
                left_ratio = get_gaze_ratio(left_eye)
                right_ratio = get_gaze_ratio(right_eye)
                avg_ratio = (left_ratio + right_ratio)/2

                if 0.9 < avg_ratio <1.2:
                    status = "Looking Forward\n"
                else:
                    status = "Not Looking Forward\n"

            if "Forward" in status or "Staring" in status:
                if gaze_start_time is None:
                    gaze_start_time = time.time()
                elif time.time() - gaze_start_time >= GAZE_TRIGGER_SECONDS:
                    if not recording:
                        recording = True
                        fourcc = cv2.VideoWriter_fourcc(*'XVID')
                        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        recording_folder = 'recordings'
                        if not os.path.exists(recording_folder):
                            os.makedirs(recording_folder)
                        filename = os.path.join(recording_folder , f'recording_{timestamp}.avi')
                        out = cv2.VideoWriter(filename,fourcc  ,20.0, (640,480))
                    cv2.putText(frame, "Recording Suspicious!", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),3)
            else:
                gaze_start_time = None
                if recording:
                    recording = False
                    out.release()
                    out = None
                
            if recording and out:
                out.write(frame)
            
            cv2.putText(frame, f"Status: {status}" , (50,50), cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,0),2)
        
        cv2.imshow("Safety Monitor",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if out:
        out.release()
    video.release()
    cv2.destroyAllWindows()