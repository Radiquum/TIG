import argparse
from typing import Literal


def opacity_type(s: str) -> float:
    try:
        value = float(s)
    except TypeError as e:
        raise argparse.ArgumentTypeError(f"{s!r} is not a valid numeric value") from e

    if not (0 <= value <= 1):
        raise argparse.ArgumentTypeError(f"{s} must be in the range 0-1")

    return value


def accent_type(s: str) -> int | Literal["off"] |  Literal["all"] |  Literal["gradient"]:
    if s in ["off", "all", "gradient"]:
        return s
    try:
        value = int(s)
        return value
    except TypeError as e:
        raise argparse.ArgumentTypeError(f"{s!r} should be one of number|off|all|gradient") from e
