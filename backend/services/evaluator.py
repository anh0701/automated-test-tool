from model.TestResult import TestResult
from model.ResultStatus import ResultStatus

def evaluate_signal(case_id, signal, measured, rule):
    if rule is None:
        return TestResult(
            case_id, signal, measured,
            None, None,
            ResultStatus.FAIL,
            "SIGNAL_NOT_IN_SPEC",
            "Signal not defined in spec"
        )

    min_v = rule["min"]
    max_v = rule["max"]

    if min_v <= measured <= max_v:
        return TestResult(
            case_id, signal, measured,
            min_v, max_v,
            ResultStatus.PASS,
            "", ""
        )

    reason = "OUT_OF_RANGE_LOW" if measured < min_v else "OUT_OF_RANGE_HIGH"

    return TestResult(
        case_id, signal, measured,
        min_v, max_v,
        ResultStatus.FAIL,
        reason,
        f"measured={measured}, expected=[{min_v}, {max_v}]"
    )