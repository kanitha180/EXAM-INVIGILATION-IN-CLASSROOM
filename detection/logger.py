import csv
import os
from datetime import datetime

LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "violations.csv")

# Create logs folder if not exists
os.makedirs(LOG_FOLDER, exist_ok=True)

# Create CSV with header if first time
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Time",
            "Violation",
            "Risk"
        ])


def log_violation(message, risk="LOW"):

    with open(LOG_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            message,
            risk
        ])