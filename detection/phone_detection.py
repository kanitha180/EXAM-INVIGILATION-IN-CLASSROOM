import cv2
from ultralytics import YOLO

# Load YOLOv8 Nano model
model = YOLO("yolov8n.pt")


def detect_phone(frame):

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
                    (30, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

    return frame