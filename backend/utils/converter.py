from model.TestResult import TestResult
from model.ResultStatus import ResultStatus


def to_test_results(df):
    results = []

    for row in df.to_dict("records"):
        results.append(TestResult(
            case_id=row["case_id"],
            signal=row["signal"],
            measured_value=float(row["measured_value"]),
            expected_low=float(row["expected_low"]) if row["expected_low"] else None,
            expected_high=float(row["expected_high"]) if row["expected_high"] else None,
            result=ResultStatus(row["result"]),
            fail_reason=row.get("fail_reason", ""),
            detail=row.get("detail", "")
        ))

    return results