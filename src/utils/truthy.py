def is_truthy(obj: object) -> bool:
    """
    Plox follows Ruby's truthiness: `False` and `None` are falsey, and
    everything else is truthy.
    """
    if obj == None:
        return False
    if isinstance(obj, bool):
        return obj
    return True
