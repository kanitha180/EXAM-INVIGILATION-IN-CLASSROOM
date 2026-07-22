import cv2
from ultralytics import YOLO

from detection.status import set_phone, increase_alert
from detection.risk_score import add_risk
from detection.logger import log_violation
from detection.evidence import start_recording


# Load YOLO model only once
model = YOLO("yolov8n.pt")


def detect_phone(frame):

    phone_found = False

    results = model.predict(
        source=frame,
        conf=0.40,
        verbose=False
    )

    for result in results:

        for box in result.boxes:

            cls = int(box.cls[0])

            label = model.names[cls]

            if label == "cell phone":

                phone_found = True

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # RED Rectangle
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 255),
                    3
                )

                # Label
                cv2.putText(
                    frame,
                    "PHONE DETECTED",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

    if phone_found:

        set_phone("Detected")

        increase_alert()

        add_risk(40)

        log_violation(
            "Mobile Phone Detected",
            "HIGH"
        )
        start_recording(frame)
        

    else:

        set_phone("Not Detected")

    return frame