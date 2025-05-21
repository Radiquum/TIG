def check_int(s: str) -> bool:
    if s[0] in ("-", "+"):
        return s[1:].isdigit()
    return s.isdigit()

def check_hex(s: str) -> bool:
    if len(s) < 6:
        return False
    return True
