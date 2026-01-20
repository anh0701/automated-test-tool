from schemas.analyze_schema import validate_analyze_request

@analyze_bp.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    valid, error = validate_analyze_request(data)
    if not valid:
        return jsonify({"error": error}), 400

    result = analyze_log_content(data["content"])
    return jsonify(result), 200
