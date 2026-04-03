from services.loggers.csv_logger import CsvLogger
from flask import Blueprint, request, jsonify

from services.TestService import TestService
from services.analyzer import LogAnalyzer
from config.settings import ROOT_CAUSE_RULES

from schemas.check_schema import validate_check_request


checker_bp = Blueprint("checker", __name__)


@checker_bp.route("/check", methods=["POST"])
def check_vectors():

    spec, test_vectors, error = validate_check_request(request)
    if error:
        return error


    logger = CsvLogger()
    service = TestService(logger=logger)  
    results = service.run_tests(spec, test_vectors)

    # print(type(results), results[:2])

    analyzer = LogAnalyzer(results, ROOT_CAUSE_RULES)

    summary = analyzer.summary()

    return jsonify({
        "log_file": logger.file_path,
        "summary": summary
    })