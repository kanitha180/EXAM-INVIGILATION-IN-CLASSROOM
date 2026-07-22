import cv2
from ultralytics import YOLO

from detection.risk_score import add_risk
from detection.logger import log_violation
from detection.status import set_phone, increase_alert

# Load YOLOv8 Nano model
model = YOLO("yolov8n.pt")


def detect_phone(frame):

    # Default Status
    set_phone("Not Detected")

    results = model.predict(
        source=frame,
        conf=0.45,
        verbose=False
    )

    for result in results:

        boxes = result.boxes

        for box in boxes:

            cls = int(box.cls[0])
            label = model.names[cls]

            if label == "cell phone":

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 255),
                    3
                )

                cv2.putText(
                    frame,
                    "🚨 MOBILE PHONE DETECTED",
                    (30, 160),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

                # Dashboard Update
                set_phone("Detected")

                # Log Violation
                log_violation("Mobile Phone Detected")

                # Increase Risk Score
                add_risk(40)

                # Increase Alert Count
                increase_alert()

    return frame