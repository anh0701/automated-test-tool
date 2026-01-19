import json
from logger import CsvLogger

with open("test_vectors.json", "r") as f:
    test_vectors = json.load(f)["test_cases"]

with open("spec.json", "r") as f:
    spec = json.load(f)


def check_against_spec(signal_name, measured_value):
    """
    Compare measured value against specification
    """
    signal_spec = spec.get(signal_name)

    if signal_spec is None:
        return False, f"No spec defined for {signal_name}"

    if "min" in signal_spec or "max" in signal_spec:
        min_v = signal_spec.get("min", float("-inf"))
        max_v = signal_spec.get("max", float("inf"))

        if min_v <= measured_value <= max_v:
            return True, "PASS"
        else:
            return False, f"Out of range ({min_v} ~ {max_v})"

    if "expected" in signal_spec:
        if measured_value == signal_spec["expected"]:
            return True, "PASS"
        else:
            return False, "Unexpected response"

    return False, "Invalid spec format"


def run_tests():
    total = len(test_vectors)
    passed = 0
    logger = CsvLogger()

    print("=== TEST START ===\n")

    for tc in test_vectors:
        case_id = tc["case_id"]
        description = tc["description"]
        stimulus = tc["stimulus"]

        print(f"[TEST] {case_id}")
        print(f"       {description}")

        case_pass = True

        for signal_name, measured_value in stimulus.items():
            result, message = check_against_spec(signal_name, measured_value)

            print(
                f"       {signal_name} = {measured_value} -> {message}"
            )

            logger.log(
                case_id=case_id,
                signal=signal_name,
                measured_value=measured_value,
                result="PASS" if result else "FAIL",
                fail_reason="" if result else message
            )

            if not result:
                case_pass = False

        if case_pass:
            print("       RESULT: PASS\n")
            passed += 1
        else:
            print("       RESULT: FAIL\n")

    yield_rate = (passed / total) * 100

    print("=== TEST SUMMARY ===")
    print(f"Total cases : {total}")
    print(f"Passed      : {passed}")
    print(f"Yield       : {yield_rate:.2f}%")

    print("\n=== TEST END ===")

    logger.close()


if __name__ == "__main__":
    run_tests()
