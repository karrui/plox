from typing import Any


def is_equal(a: Any, b: Any) -> bool:
    if a == None and b == None:
        return True
    if a == None:
        return False
    return a == b
