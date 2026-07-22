risk_score = 0

def add_risk(points):
    global risk_score
    risk_score += points

    if risk_score > 100:
        risk_score = 100


def get_risk():
    return risk_score