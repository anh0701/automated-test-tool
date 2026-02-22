import csv
import io
from services.analyze import detect_flaky, error_distribution, normalize, recommendations, root_cause_summary, signal_health, summary_stats
from flask import Blueprint, request, jsonify
from schemas.analyze_schema import validate_analyze_request

analyst_bp = Blueprint("analyze", __name__)

@analyst_bp.route("/api/analyze", methods=["POST"])
def analyze():
    df, error = validate_analyze_request(request)

    if error:
        return error
    
    logs = normalize(df.to_dict("records"))

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
