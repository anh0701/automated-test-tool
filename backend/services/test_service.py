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
                        case_id,
                        signal,
                        measured,
                        "Signal not found in spec",
                        summary
                    )
                    continue

                if rule["min"] <= measured <= rule["max"]:
                    self._pass(case_id, signal, measured, summary)
                else:
                    self._fail(
                        case_id,
                        signal,
                        measured,
                        f"Out of range [{rule['min']}, {rule['max']}]",
                        summary
                    )

        return summary

    def _pass(self, case_id, signal, measured, summary):
        self.logger.log(case_id, signal, measured, "PASS")
        summary["pass"] += 1

    def _fail(self, case_id, signal, measured, reason, summary):
        self.logger.log(
            case_id,
            signal,
            measured,
            "FAIL",
            reason
        )
        summary["fail"] += 1
