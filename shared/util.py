import random
import string


def check_int(s: str) -> bool:
    if s[0] in ("-", "+"):
        return s[1:].isdigit()
    return s.isdigit()


def check_hex(s: str) -> bool:
    if len(s) < 6:
        return False
    return True


def hex_to_rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_rgba(value, alpha):
    return tuple([value[0], value[1], value[2], alpha])


def generate_random_symbols(length: int):
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string
