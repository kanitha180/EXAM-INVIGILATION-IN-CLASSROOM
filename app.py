from flask import Flask, render_template, Response
import cv2

from detection.face_detection import detect_faces
from detection.head_pose import detect_head_pose
from detection.phone_detection import detect_phone

app = Flask(__name__)

camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()

        if not success:
            break

        # AI Face Detection
        frame = detect_faces(frame)

        # Head Pose Detection
        frame = detect_head_pose(frame)

        # Mobile Phone Detection
        #frame = detect_phone(frame)
        
        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/monitor")
def monitor():
    return render_template("monitor.html")


@app.route("/video")
def video():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(debug=True)