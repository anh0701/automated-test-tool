from flask import Blueprint, request, jsonify
from config.settings import ROOT_CAUSE_RULES
from services.analyzer import LogAnalyzer
from utils.converter import to_test_results
from schemas.analyze_schema import validate_analyze_request

analyst_bp = Blueprint("analyze", __name__)

@analyst_bp.route("/api/analyze", methods=["POST"])
def analyze():
    df, error = validate_analyze_request(request)

    if error:
        return error

    results = to_test_results(df)

    analyzer = LogAnalyzer(results, ROOT_CAUSE_RULES)

    report = {
        "summary": analyzer.summary(),
        "signals": analyzer.signal_health(),
        "error_distribution": analyzer.error_distribution(),
        "root_causes": analyzer.root_cause_summary()
    }

    return jsonify(report)