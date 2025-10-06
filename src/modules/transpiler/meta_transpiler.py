# meta_transpiler.py — orchestrates adapters (placeholder)
from .adapters import python_adapter
def to_target(ast, target):
    if target == "python":
        return python_adapter.transpile(ast)
    raise NotImplementedError("Target not supported")
