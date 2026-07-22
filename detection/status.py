# -------------------------------
# AI Exam Invigilation Status
# -------------------------------

persons = 0
head_pose = "Looking Forward"
phone = "Not Detected"
alerts = 0
risk = "LOW"

# ---------------- Persons ----------------

def set_persons(value):
    global persons
    persons = value

def get_persons():
    return persons

# ---------------- Head Pose ----------------

def set_head_pose(value):
    global head_pose
    head_pose = value

def get_head_pose():
    return head_pose

# ---------------- Phone ----------------

def set_phone(value):
    global phone
    phone = value

def get_phone():
    return phone

# ---------------- Alerts ----------------

def increase_alert():
    global alerts
    alerts += 1

def reset_alerts():
    global alerts
    alerts = 0

def get_alerts():
    return alerts

# ---------------- Risk ----------------

def set_risk(value):
    global risk
    risk = value

def get_risk():
    return risk