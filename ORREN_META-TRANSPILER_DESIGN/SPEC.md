# ORREN SPEC (Prototype excerpt)

This file is a short excerpt for the Orren meta-transpiler prototype.

## Purpose
Orren is a meta-language that expresses intent and compiles to multiple targets.

## Minimal Syntax (prototype)
- `function NAME ARG:` starts a function definition (single arg supported)
- `if CONDITION:` begins an if block
- `else:` begins else
- `return VALUE` returns a value
- other lines treated as expressions / actions

Example:
```
function greet name:
    if time < 12:
        return "Good morning, " + name
    else:
        return "Hello, " + name
```
