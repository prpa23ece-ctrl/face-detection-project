import cv2
import mediapipe as mp
import numpy as np
import face_recognition
import os

# ----------------------------------
# Load known faces
# ----------------------------------
known_encodings = []
known_names = []

for file in os.listdir("known_faces"):

    path = os.path.join("known_faces", file)

    image = face_recognition.load_image_file(path)
    encoding = face_recognition.face_encodings(image)

    if len(encoding) > 0:
        known_encodings.append(encoding[0])
        known_names.append(os.path.splitext(file)[0])

print("Loaded:", known_names)

# ----------------------------------
# MediaPipe Face Detection
# ----------------------------------
mp_face = mp.solutions.face_detection
face_detector = mp_face.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.6
)

# ----------------------------------
# Kalman Filter
# ----------------------------------
kalman = cv2.KalmanFilter(4,2)

kalman.measurementMatrix = np.array([
[1,0,0,0],
[0,1,0,0]
], np.float32)

kalman.transitionMatrix = np.array([
[1,0,1,0],
[0,1,0,1],
[0,0,1,0],
[0,0,0,1]
], np.float32)

kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03

# ----------------------------------
# Webcam
# ----------------------------------
cap = cv2.VideoCapture(0)

tracker = None
tracking = False
name = "Unknown"

# ----------------------------------
# Main Loop
# ----------------------------------
while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if not tracking:

        results = face_detector.process(frame_rgb)

        if results.detections:

            h, w, _ = frame.shape

            detection = results.detections[0]
            bboxC = detection.location_data.relative_bounding_box

            x = int(bboxC.xmin * w)
            y = int(bboxC.ymin * h)
            bw = int(bboxC.width * w)
            bh = int(bboxC.height * h)

            bbox = (x, y, bw, bh)

            face_locations = [(y, x+bw, y+bh, x)]
            encodings = face_recognition.face_encodings(frame_rgb, face_locations)

            name = "Unknown"

            if len(encodings) > 0:

                matches = face_recognition.compare_faces(
                    known_encodings,
                    encodings[0]
                )

                if True in matches:
                    index = matches.index(True)
                    name = known_names[index]

            tracker = cv2.TrackerCSRT_create()
            tracker.init(frame, bbox)

            tracking = True

    else:

        success, bbox = tracker.update(frame)

        if success:

            x, y, w_box, h_box = map(int, bbox)

            cx = x + w_box//2
            cy = y + h_box//2

            measurement = np.array([[np.float32(cx)],
                                    [np.float32(cy)]])

            kalman.correct(measurement)
            prediction = kalman.predict()

            smooth_x = int(prediction[0][0])
            smooth_y = int(prediction[1][0])

            cv2.rectangle(frame,
                          (smooth_x-w_box//2, smooth_y-h_box//2),
                          (smooth_x+w_box//2, smooth_y+h_box//2),
                          (0,255,0),2)

            cv2.putText(frame,
                        name,
                        (smooth_x-w_box//2, smooth_y-h_box//2-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0,255,0),
                        2)

        else:
            tracking = False

    cv2.imshow("Face Recognition Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()