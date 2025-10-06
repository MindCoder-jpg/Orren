# ORREN META-TRANSPILER DESIGN (Prototype)

A minimal, runnable prototype of the Orren meta-transpiler. This package demonstrates:
- a simple Orren parser (universal AST)
- multi-target emitter (Python / HTML / JSON)
- CLI usage to transpile `.orren` files into multiple targets

## Quick start
1. Unzip the package and open a terminal in the directory.
2. Run examples:
   ```bash
   python core/orren.py tests/demo.orren --target=python
   python core/orren.py tests/demo.orren --target=html
   python core/orren.py tests/demo.orren --target=json
   ```
3. Inspect generated files `tests/demo.python`, `tests/demo.html`, `tests/demo.json`

## Structure
- core/orren.py        : main meta-transpiler CLI
- tests/demo.orren     : sample Orren source
- SPEC.md              : short spec excerpt
- .gitignore           : recommended patterns
