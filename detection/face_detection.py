import cv2
import mediapipe as mp

from detection.status import set_persons
from detection.logger import log_violation
from detection.risk_score import add_risk


mp_face = mp.solutions.face_detection

face_detection = mp_face.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.6
)

def detect_faces(frame):

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb)

    face_count = 0

    h, w, _ = frame.shape

    if results.detections:

        face_count = len(results.detections)

        for detection in results.detections:

            bbox = detection.location_data.relative_bounding_box

            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            bw = int(bbox.width * w)
            bh = int(bbox.height * h)

            # Green Rectangle
            color = (0,255,0)

            # Multiple Students -> Red Rectangle
            if face_count > 1:
                color = (0,0,255)

            cv2.rectangle(
                frame,
                (x,y),
                (x+bw,y+bh),
                color,
                3
            )

    set_persons(face_count)

    # Face Count
    cv2.putText(
        frame,
        f"Faces : {face_count}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255,255,0),
        2
    )

    # Status
    if face_count == 0:

        cv2.putText(
            frame,
            "STATUS : NO STUDENT",
            (20,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,0,255),
            2
        )

    elif face_count == 1:

        cv2.putText(
            frame,
            "STATUS : NORMAL",
            (20,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

    else:

        cv2.putText(
            frame,
            "WARNING : MULTIPLE STUDENTS",
            (20,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,0,255),
            2
        )

        log_violation(
            "Multiple Students Detected",
            "HIGH"
        )

        add_risk(25)
    return frame