from collections import defaultdict, Counter
from model.ResultStatus import ResultStatus


class LogAnalyzer:

    def __init__(self, logs, root_cause_rules):
        self.logs = logs
        self.rules = root_cause_rules

    def aggregate(self):
        total = 0
        fail = 0
        error_counter = Counter()
        signal_stats = defaultdict(lambda: {"total": 0, "fail": 0})

        for l in self.logs:
            total += 1
            signal_stats[l.signal]["total"] += 1

            if l.result == ResultStatus.FAIL:
                fail += 1
                signal_stats[l.signal]["fail"] += 1

                if l.fail_reason:
                    error_counter[l.fail_reason] += 1

        return total, fail, error_counter, signal_stats

    def summary(self):
        total, fail, *_ = self.aggregate()
        return {
            "total": total,
            "pass": total - fail,
            "fail": fail,
            "fail_rate": round(fail / total, 4) if total else 0
        }

    def signal_health(self):
        _, _, _, stats = self.aggregate()
        return [
            {
                "signal": s,
                "fail_rate": v["fail"] / v["total"]
            }
            for s, v in stats.items()
        ]

    def error_distribution(self):
        _, _, errors, _ = self.aggregate()
        return dict(errors)

    def root_cause_summary(self):
        _, _, errors, _ = self.aggregate()

        result = defaultdict(lambda: {
            "count": 0,
            "cases": []
        })

        for l in self.logs:
            if l.result == ResultStatus.FAIL and l.fail_reason:
                result[l.fail_reason]["count"] += 1
                result[l.fail_reason]["cases"].append({
                    "case_id": l.case_id,
                    "signal": l.signal
                })

        return [
            {
                "fail_reason": r,
                "count": v["count"],
                "suspected_cause": self.rules.get(
                    r, "Manual investigation needed"
                ),
                "cases": v["cases"]
            }
            for r, v in result.items()
        ]