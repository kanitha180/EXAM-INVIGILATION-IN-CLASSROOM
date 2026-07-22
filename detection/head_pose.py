import cv2
import mediapipe as mp

from detection.status import set_head_pose
from detection.logger import log_violation
from detection.risk_score import add_risk

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=5,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE = 33
RIGHT_EYE = 263
NOSE = 1

def detect_head_pose(frame):

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        h, w, _ = frame.shape

        for face in results.multi_face_landmarks:

            nose = face.landmark[NOSE]
            left = face.landmark[LEFT_EYE]
            right = face.landmark[RIGHT_EYE]

            nose_x = int(nose.x * w)
            nose_y = int(nose.y * h)

            left_x = int(left.x * w)
            right_x = int(right.x * w)

            center = (left_x + right_x) // 2

            text = "Looking Forward"
            color = (0,255,0)

            if nose_x < center - 25:

                text = "Looking Left"
                color = (0,0,255)

                add_risk(2)
                log_violation("Looking Left","MEDIUM")

            elif nose_x > center + 25:

                text = "Looking Right"
                color = (0,0,255)

                add_risk(2)
                log_violation("Looking Right","MEDIUM")

            elif nose_y > int(h * 0.60):

                text = "Looking Down"
                color = (0,140,255)

                add_risk(3)
                log_violation("Looking Down","MEDIUM")

            set_head_pose(text)

            cv2.putText(
                frame,
                text,
                (20,120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

    return frame