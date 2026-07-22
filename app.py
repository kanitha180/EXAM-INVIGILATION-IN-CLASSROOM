from flask import Flask, render_template, Response, jsonify, send_file
import cv2

from detection.face_detection import detect_faces
from detection.head_pose import detect_head_pose
from detection.phone_detection import detect_phone
from detection.evidence import start_recording, update_recording

from detection.status import (
    get_persons,
    get_head_pose,
    get_phone,
    get_alerts
)

from detection.risk_score import get_risk

app = Flask(__name__)

# ---------------- CAMERA ---------------- #

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print("Camera 0 Failed... Trying Camera 1")

    camera = cv2.VideoCapture(1)

if not camera.isOpened():

    print("Camera Open Failed")

else:

    print("Camera Opened Successfully")


# ---------------- VIDEO STREAM ---------------- #

def generate_frames():

    while True:

        success, frame = camera.read()

        if not success:
            break

        # Face Detection
        frame = detect_faces(frame)

        # Head Pose
        frame = detect_head_pose(frame)

        # Phone Detection
        frame = detect_phone(frame)

        update_recording(frame)


        # Risk Score
        risk = get_risk()

        if risk < 30:
            risk_text = "LOW"
            color = (0,255,0)

        elif risk < 70:
            risk_text = "MEDIUM"
            color = (0,255,255)

        else:
            risk_text = "HIGH"
            color = (0,0,255)

        cv2.putText(
            frame,
            f"Risk : {risk}% ({risk_text})",
            (20,160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        ret, buffer = cv2.imencode(".jpg", frame)

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )
        # ---------------- ROUTES ---------------- #

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


# ---------- LIVE DASHBOARD STATUS ---------- #

@app.route("/status")
def status():

    risk = get_risk()

    if risk < 30:
        risk_level = "LOW"

    elif risk < 70:
        risk_level = "MEDIUM"

    else:
        risk_level = "HIGH"

    return jsonify({

        "persons": get_persons(),

        "head_pose": get_head_pose(),

        "phone": get_phone(),

        "alerts": get_alerts(),

        "risk_score": risk,

        "risk_level": risk_level

    })


# ---------- REPORT DOWNLOAD ---------- #

@app.route("/report")
def report():

    return send_file(
        "logs/violations.csv",
        as_attachment=True
    )


# ---------- RUN ---------- #

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )