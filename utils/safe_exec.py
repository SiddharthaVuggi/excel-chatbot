import builtins
from typing import Dict, Any, Optional


# Whitelisted built-in functions
ALLOWED_BUILTINS = {
    "abs",
    "min",
    "max",
    "sum",
    "len",
    "range",
    "enumerate",
    "zip",
    "sorted",
    "round",
    "all",
    "any",
}


def safe_exec(
    code: str,
    local_ns: Optional[Dict[str, Any]] = None,
    allowed_builtins: Optional[set] = None,
) -> Dict[str, Any]:
    """
    Execute Python code in a restricted environment.

    Args:
        code: Python code to execute.
        local_ns: Variables accessible during execution.
        allowed_builtins: Custom whitelist of built-in functions.

    Returns:
        Updated local namespace after execution.

    Raises:
        ValueError: If code is empty.
        RuntimeError: If execution fails.
    """

    if not code.strip():
        raise ValueError("Code cannot be empty.")

    if local_ns is None:
        local_ns = {}

    if allowed_builtins is None:
        allowed_builtins = ALLOWED_BUILTINS

    safe_builtins = {
        name: getattr(builtins, name)
        for name in allowed_builtins
        if hasattr(builtins, name)
    }

    try:
        exec(
            code,
            {"__builtins__": safe_builtins},
            local_ns,
        )

        return local_ns

    except Exception as e:
        raise RuntimeError(f"Execution failed: {e}") from e
