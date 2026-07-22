from flask import Flask, render_template, Response, send_file
import cv2

from detection.face_detection import detect_faces
from detection.head_pose import detect_head_pose
from detection.phone_detection import detect_phone
from detection.risk_score import get_risk
from detection.status import (
    get_persons,
    get_head_pose,
    get_phone,
    get_alerts
)

app = Flask(__name__)

# ---------------- CAMERA ----------------

camera = cv2.VideoCapture(0)

# If camera 0 fails, try camera 1
if not camera.isOpened():
    print("Camera 0 Failed... Trying Camera 1")
    camera = cv2.VideoCapture(1)

if not camera.isOpened():
    print("Camera Open Failed")
else:
    print("Camera Opened Successfully")

# ---------------- VIDEO GENERATOR ----------------

def generate_frames():

    while True:

        success, frame = camera.read()

        if not success:
            print("❌ Camera Read Failed")
            break

        print("✅ Frame Captured")

        ret, buffer = cv2.imencode(".jpg", frame)

        if not ret:
            print("❌ JPEG Encode Failed")
            break

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )
# ---------------- ROUTES ----------------

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


@app.route("/face")
def face():
    return render_template("face.html")


@app.route("/headpose")
def headpose():
    return render_template("headpose.html")


@app.route("/phone")
def phone():
    return render_template("phone.html")


@app.route("/alerts")
def alerts():
    return render_template("alerts.html")


@app.route("/report")
def report():
    return send_file(
        "logs/violations.csv",
        as_attachment=True
    )

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)