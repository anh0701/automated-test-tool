def analyze_log_content(content: str) -> dict:
    lines = content.splitlines()

    error_count = 0
    warning_count = 0

    for line in lines:
        line_lower = line.lower()
        if "error" in line_lower:
            error_count += 1
        if "warning" in line_lower:
            warning_count += 1

    return {
        "total_lines": len(lines),
        "errors": error_count,
        "warnings": warning_count
    }
