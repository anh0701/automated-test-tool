import csv
import io
from services.analyze import detect_flaky, error_distribution, normalize, recommendations, root_cause_summary, signal_health, summary_stats
from flask import Blueprint, request, jsonify

analyst_bp = Blueprint("analyze", __name__)

@analyst_bp.route("/api/analyze", methods=["POST"])
def analyze():
    if "log" not in request.files:
        return jsonify({"error": "log CSV file is required"}), 400

    file = request.files["log"]
    stream = io.StringIO(file.stream.read().decode("utf-8"))
    logs = list(csv.DictReader(stream))

    if not logs:
        return jsonify({"error": "Empty log file"}), 400

    logs = normalize(logs)

    signals = signal_health(logs)
    err_dist = error_distribution(logs)

    report = {
        "summary": summary_stats(logs),
        "signals": signals,
        "error_distribution": err_dist,
        "flaky_cases": detect_flaky(logs),
        "root_causes": root_cause_summary(logs),
        "recommendations": recommendations(signals, err_dist)
    }

    return jsonify(report)
