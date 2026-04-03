from dataclasses import dataclass
from typing import Optional

from model import ResultStatus


@dataclass
class TestResult:
    case_id: str
    signal: str
    measured_value: float
    expected_low: Optional[float]
    expected_high: Optional[float]
    result: ResultStatus
    fail_reason: str
    detail: str