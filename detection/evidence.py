import cv2
import os
from datetime import datetime

os.makedirs("evidence", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)

writer = None
recording = False
start_time = None


def start_recording(frame):

    global writer, recording, start_time

    if recording:
        return

    filename = datetime.now().strftime("%Y%m%d_%H%M%S")

    video_path = f"evidence/video_{filename}.mp4"
    image_path = f"screenshots/img_{filename}.jpg"

    cv2.imwrite(image_path, frame)

    h, w = frame.shape[:2]

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(video_path, fourcc, 20, (w, h))

    recording = True

    start_time = datetime.now()


def update_recording(frame):

    global writer, recording, start_time

    if not recording:
        return

    writer.write(frame)

    elapsed = (datetime.now() - start_time).total_seconds()

    if elapsed >= 10:

        writer.release()

        writer = None

        recording = False