def is_alpha(val: str) -> bool:
    return val.isalpha() or val == '_'


def is_alnum(val: str) -> bool:
    return is_alpha(val) or val.isdigit()
