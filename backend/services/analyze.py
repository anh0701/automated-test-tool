from collections import defaultdict
from typing import Counter


def normalize(logs):
    for l in logs:
        for k in ("measured_value", "expected_low", "expected_high"):
            if k in l and l[k] not in ("", None):
                l[k] = float(l[k])
        l["result"] = l["result"].upper()
        l["fail_reason"] = (l.get("fail_reason") or "").upper()
    return logs

def summary_stats(logs):
    total = len(logs)
    fail = sum(1 for l in logs if l["result"] == "FAIL")
    return {
        "total": total,
        "pass": total - fail,
        "fail": fail,
        "fail_rate": round(fail / total, 4) if total else 0
    }

def error_distribution(logs):
    return dict(Counter(
        l["fail_reason"] for l in logs
        if l["result"] == "FAIL" and l["fail_reason"]
    ))

def signal_health(logs):
    stats = defaultdict(lambda: {"total": 0, "fail": 0})
    for l in logs:
        s = l["signal"]
        stats[s]["total"] += 1
        if l["result"] == "FAIL":
            stats[s]["fail"] += 1

    out = []
    for s, v in stats.items():
        rate = v["fail"] / v["total"]
        out.append({
            "signal": s,
            "total": v["total"],
            "fail": v["fail"],
            "fail_rate": round(rate, 4),
            "health_score": round(100 * (1 - rate), 1)
        })
    return sorted(out, key=lambda x: x["fail_rate"], reverse=True)

def detect_flaky(logs):
    hist = defaultdict(set)
    for l in logs:
        key = (l["case_id"], l["signal"])
        hist[key].add(l["result"])
    return [
        {"case_id": k[0], "signal": k[1]}
        for k, v in hist.items() if len(v) > 1
    ]

def root_cause_summary(logs):
    rules = {
        "OUT_OF_RANGE_LOW": "Possible undervoltage or calibration drift",
        "OUT_OF_RANGE_HIGH": "Possible overvoltage or reference error",
        "UNSTABLE": "Noise or timing issue",
        "TIMEOUT": "Communication or response latency issue",
        "NO_SIGNAL": "Connection or enable sequence issue"
    }
    cnt = Counter(l["fail_reason"] for l in logs if l["result"] == "FAIL")
    return [
        {
            "fail_reason": r,
            "count": c,
            "suspected_cause": rules.get(r, "Manual investigation needed")
        }
        for r, c in cnt.items()
    ]

def recommendations(signals, error_dist):
    rec = []
    if signals and signals[0]["fail_rate"] > 0.3:
        rec.append(f"Review spec/tolerance for signal {signals[0]['signal']}")
    if error_dist.get("UNSTABLE"):
        rec.append("Check noise, settling time, or averaging")
    if error_dist.get("TIMEOUT"):
        rec.append("Review timeout thresholds and communication latency")
    return rec
