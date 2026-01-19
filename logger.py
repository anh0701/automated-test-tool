import csv
from datetime import datetime
import os


class CsvLogger:
    def __init__(self, log_dir="logs"):
        os.makedirs(log_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.file_path = os.path.join(
            log_dir, f"test_log_{timestamp}.csv"
        )

        self.file = open(self.file_path, mode="w", newline="")
        self.writer = csv.writer(self.file)

        self.writer.writerow([
            "timestamp",
            "case_id",
            "signal",
            "measured_value",
            "result",
            "fail_reason"
        ])

    def log(self, case_id, signal, measured_value, result, fail_reason=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.writer.writerow([
            timestamp,
            case_id,
            signal,
            measured_value,
            result,
            fail_reason
        ])

    def close(self):
        self.file.close()
