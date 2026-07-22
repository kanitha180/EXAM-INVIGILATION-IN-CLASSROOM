persons = 0
head_pose = "Looking Forward"
phone = "Not Detected"
alerts = 0

def set_persons(value):
    global persons
    persons = value

def get_persons():
    return persons

def set_head_pose(value):
    global head_pose
    head_pose = value

def get_head_pose():
    return head_pose

def set_phone(value):
    global phone
    phone = value

def get_phone():
    return phone

def increase_alert():
    global alerts
    alerts += 1

def get_alerts():
    return alerts