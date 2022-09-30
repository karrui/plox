from typing import Any


def is_alpha(val: str) -> bool:
    return val.isalpha() or val == '_'


def is_alnum(val: str) -> bool:
    return is_alpha(val) or val.isdigit()


def stringify(val: Any) -> str:
    if val == None:
        return 'nil'

    if isinstance(val, float):
        text = str(val)
        if text.endswith(".0"):
            text = text[:-2]
        return text

    return str(val)
