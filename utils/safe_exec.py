import builtins

_ALLOWED = {"abs", "min", "max", "sum", "len", "range"}


def safe_exec(code: str, local_ns: dict):
    """Execute code in a restricted environment."""
    safe_builtins = {k: getattr(builtins, k) for k in _ALLOWED}
    exec(code, {"__builtins__": safe_builtins}, local_ns)