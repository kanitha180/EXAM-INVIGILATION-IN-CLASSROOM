import csv
import os
from datetime import datetime

LOG_FILE = "logs/violations.csv"

def log_violation(message):

    os.makedirs("logs", exist_ok=True)

    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            message
        ])