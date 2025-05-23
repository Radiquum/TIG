import argparse
from typing import Literal


def opacity_type(s: str) -> float:
    try:
        value = float(s)
    except TypeError:
        raise argparse.ArgumentTypeError(f"{s!r} is not a valid numeric value")

    if not (0 <= value <= 1):
        raise argparse.ArgumentTypeError(f"{s} must be in the range 0-1")

    return value


def accent_type(s: str) -> int | Literal["off"] |  Literal["all"] |  Literal["gradient"]:
    if s not in ["off", "all", "gradient"]:
        try:
            value = int(s)
        except TypeError:
            raise argparse.ArgumentTypeError(f"{s!r} should be one of number|off|all|gradient")

    if isinstance(s, int):
        return int(value)
    return s
