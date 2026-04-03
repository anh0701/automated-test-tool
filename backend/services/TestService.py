from services.evaluator import evaluate_signal

class TestService:

    def __init__(self, logger):
        self.logger = logger

    def run_tests(self, spec, test_vectors):
        rules = spec.get("fields", {})
        results = []

        for case in test_vectors:
            case_id = case.get("id")

            for signal, measured in case.items():
                if signal == "id":
                    continue

                result = evaluate_signal(
                    case_id,
                    signal,
                    measured,
                    rules.get(signal)
                )

                results.append(result)

                self.logger.log(**result.__dict__)

        return results