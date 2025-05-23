import random
import string
from shared.log import log

def check_int(s: str) -> bool:
    if not isinstance(s, str) or len(s) < 1:
        return False
    if s[0] in ("-", "+"):
        return s[1:].isdigit()
    return s.isdigit()


def check_hex(s: str) -> bool:
    if len(s) < 6:
        return False
    return True


def str_to_hex(s: str) -> str:
    return f"#{s}"


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


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


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(
        (
            (img_width - crop_width) // 2,
            (img_height - crop_height) // 2,
            (img_width + crop_width) // 2,
            (img_height + crop_height) // 2,
        )
    )

def check_color(string: str):
    if string.startswith("hex["):
            allowed_symbols = [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
            ]
            string = string.removeprefix("hex[").removesuffix("]").lower()
            if len(string) < 6:
                log.error(
                    f"invalid hex value, it should be in full format (6 symbols), got {string} ({len(string)} symbols)",
                    extra={"highlighter": None},
                )
                exit(0)
            for index, char in enumerate(string, start=1):
                if char not in allowed_symbols:
                    log.error(
                        f"unexpected symbol `{char}` at index `{index}`, allowed only 0-9 a-f",
                        extra={"highlighter": None},
                    )
                    exit(0)
            string = str_to_hex(string)
    elif string.startswith("rgb["):
        allowed_symbols = [str(i) for i in range(256)]
        string = string.removeprefix("rgb[").removesuffix("]").split(",")
        if len(string) < 3:
            log.error(
                "invalid rgb value, it should be [[red]red[/red],[green]green[/green],[blue]blue[/blue]] in range 0-255",
                extra={"highlighter": None, "markup": True},
            )
            exit(0)
        for index, char in enumerate(string, start=1):
            if char not in allowed_symbols:
                log.error(
                    f"unexpected symbol `{char}` at index `{index}`, allowed only 0-255",
                    extra={"highlighter": None},
                )
                exit(0)
        string = rgb_to_hex(
            int(string[0]), int(string[1]), int(string[2])
        )
    else:
        log.error(
            "invalid key value type, expected: hex[value] | rgb[0-255,0-255,0-255]",
            extra={"highlighter": None},
        )
        exit(0)
    return string