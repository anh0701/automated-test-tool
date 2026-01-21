class TestService:
    def __init__(self, logger):
        self.logger = logger

    def run_tests(self, spec: dict, test_vectors: list) -> dict:
        rules = spec.get("fields", {})

        summary = {
            "total": 0,
            "pass": 0,
            "fail": 0
        }

        for case in test_vectors:
            case_id = case.get("id")

            for signal, measured in case.items():
                if signal == "id":
                    continue

                summary["total"] += 1
                rule = rules.get(signal)

                if rule is None:
                    self._fail(
                        case_id=case_id,
                        signal=signal,
                        measured=measured,
                        expected_low=None,
                        expected_high=None,
                        fail_reason="SIGNAL_NOT_IN_SPEC",
                        detail="Signal not defined in spec",
                        summary=summary
                    )
                    continue

                min_v = rule["min"]
                max_v = rule["max"]

                if min_v <= measured <= max_v:
                    self._pass(
                        case_id, signal, measured, min_v, max_v, summary
                    )
                else:
                    if measured < min_v:
                        reason = "OUT_OF_RANGE_LOW"
                    else:
                        reason = "OUT_OF_RANGE_HIGH"

                    detail = (
                        f"measured={measured}, "
                        f"expected=[{min_v}, {max_v}]"
                    )

                    self._fail(
                        case_id=case_id,
                        signal=signal,
                        measured=measured,
                        expected_low=min_v,
                        expected_high=max_v,
                        fail_reason=reason,
                        detail=detail,
                        summary=summary
                    )

        return summary

    def _pass(self, case_id, signal, measured, low, high, summary):
        self.logger.log(
            case_id=case_id,
            signal=signal,
            measured_value=measured,
            expected_low=low,
            expected_high=high,
            result="PASS",
            fail_reason="",
            detail=""
        )
        summary["pass"] += 1

    def _fail(
        self,
        case_id,
        signal,
        measured,
        expected_low,
        expected_high,
        fail_reason,
        detail,
        summary
    ):
        self.logger.log(
            case_id=case_id,
            signal=signal,
            measured_value=measured,
            expected_low=expected_low,
            expected_high=expected_high,
            result="FAIL",
            fail_reason=fail_reason,
            detail=detail
        )
        summary["fail"] += 1
