import cv2
import mediapipe as mp
from detection.violation_counter import increase_left, increase_right

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
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
            left_x = int(left.x * w)
            right_x = int(right.x * w)

            center = (left_x + right_x) // 2

            if nose_x < center - 20:
                text = "Looking Left"
                color = (0, 0, 255)
                increase_left()

            elif nose_x > center + 20:
                text = "Looking Right"
                color = (0, 0, 255)
                increase_right()

            else:
                text = "Looking Forward"
                color = (0, 255, 0)

            cv2.putText(
                frame,
                text,
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                2
            )

    return frame