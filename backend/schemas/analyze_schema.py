import pandas as pd
from flask import jsonify

REQUIRED_COLUMNS = {"case_id", "result", "fail_reason"}
MAX_FILE_SIZE_MB = 20

def validate_analyze_request(request):
    if "log" not in request.files:
        return None, (jsonify({"error": "log CSV file is required"}), 400)
    
    file = request.files["log"]

    if not file.filename:
        return None, (jsonify({"error": "No file selected"}), 400)
    
    file.stream.seek(0, 2)
    size_mb = file.stream.tell() / (1024 * 1024)
    file.stream.seek(0)

    if size_mb > MAX_FILE_SIZE_MB:
        return None, (
            jsonify({"error": f"File too large (> {MAX_FILE_SIZE_MB} MB)"}),
            400
        )
    
    try:
        df = pd.read_csv(
            file.stream,
            encoding="utf-8",
            on_bad_lines="skip"
        )
    except Exception as e:
        return None, (jsonify({"error": f"Invalid CSV: {str(e)}"}), 400)
    
    if df.empty:
        return None, (jsonify({"error": "Empty log file"}), 400)
    
    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        return None, (
            jsonify(
                {
                    "error": "Missing required columns",
                    "missing": list(missing)
                }
            ),
            400
        )
    
    return df, None
