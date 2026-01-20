def validate_analyze_request(data: dict):
    if not data:
        return False, "Request body is empty"

    if "content" not in data:
        return False, "Missing 'content' field"

    if not isinstance(data["content"], str):
        return False, "'content' must be string"

    return True, None
