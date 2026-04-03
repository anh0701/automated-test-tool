from enum import Enum


class FailReason(str, Enum):
    SIGNAL_NOT_IN_SPEC = "SIGNAL_NOT_IN_SPEC"
    OUT_OF_RANGE_LOW = "OUT_OF_RANGE_LOW"
    OUT_OF_RANGE_HIGH = "OUT_OF_RANGE_HIGH"