# Global counters

left_count = 0
right_count = 0
multiple_face_count = 0
no_face_count = 0


def get_counts():
    return {
        "left": left_count,
        "right": right_count,
        "multiple": multiple_face_count,
        "no_face": no_face_count
    }


def increase_left():
    global left_count
    left_count += 1


def increase_right():
    global right_count
    right_count += 1


def increase_multiple():
    global multiple_face_count
    multiple_face_count += 1


def increase_no_face():
    global no_face_count
    no_face_count += 1