import cv2
import mediapipe as mp

mp_face = mp.solutions.face_detection

face_detection = mp_face.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.5
)

def detect_faces(frame):

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb)

    face_count = 0

    if results.detections:

        face_count = len(results.detections)

        h, w, _ = frame.shape

        for detection in results.detections:

            bbox = detection.location_data.relative_bounding_box

            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            bw = int(bbox.width * w)
            bh = int(bbox.height * h)

            cv2.rectangle(frame, (x, y), (x + bw, y + bh), (0, 255, 0), 2)

    # Face Count
    cv2.putText(
        frame,
        f"Faces : {face_count}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2
    )

    # Status
    if face_count == 0:

        cv2.putText(
            frame,
            "STATUS : No Student",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    elif face_count > 1:

        cv2.putText(
            frame,
            "STATUS : Multiple Students",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    else:

        cv2.putText(
            frame,
            "STATUS : Normal",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    return frame