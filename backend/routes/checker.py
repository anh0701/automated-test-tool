import json
from flask import Blueprint, request, jsonify

from services.test_service import TestService
from loggers.csv_logger import CsvLogger

checker_bp = Blueprint("checker", __name__)


@checker_bp.route("/check", methods=["POST"])
def check_vectors():
    if "spec" not in request.files or "vectors" not in request.files:
        return jsonify({
            "error": "spec.json and test_vectors.json are required"
        }), 400

    logger = CsvLogger()
    service = TestService(logger)

    try:
        spec = json.load(request.files["spec"])
        vectors = json.load(request.files["vectors"])
    except Exception as e:
        return jsonify({
            "error": f"Invalid JSON: {str(e)}"
        }), 400

    try:
        results = service.run_tests(spec, vectors)
    finally:
        logger.close()

    summary = {
        "total": results["total"],
        "passed": results["pass"],
        "failed": results["fail"]
    }

    return jsonify({
        "summary": summary,
        "log_file": logger.file_path
    })
