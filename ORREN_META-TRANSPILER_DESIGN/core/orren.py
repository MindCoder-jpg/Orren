#!/usr/bin/env python3
# ORREN META-TRANSPILER (prototype)
# Author: AZURA DAEMON
# Organization: MindCoder (HAEL Initiative)
#
# Usage:
#   python orren.py <source.orren> --target=python|html|json
#
import sys, re, json
from pathlib import Path

INDENT = '    '

# ---- Simple tokenizer by line (keeps indentation semantics minimal)
def tokenize_lines(source):
    lines = []
    for raw in source.splitlines():
        line = raw.rstrip('\n')
        if not line.strip():
            continue
        # leading spaces count as indent level (multiple of 4 assumed)
        indent = len(line) - len(line.lstrip(' '))
        lines.append((indent, line.strip()))
    return lines

# ---- Parser -> simple AST
def parse(source):
    lines = tokenize_lines(source)
    ast = []
    stack = []  # (node, indent)
    current_block = None

    def push_node(node, indent):
        nonlocal stack, ast
        if not stack:
            ast.append(node)
            stack.append((node, indent))
        else:
            # find parent by indent
            while stack and indent <= stack[-1][1]:
                stack.pop()
            if stack:
                parent = stack[-1][0]
                parent.setdefault('body', []).append(node)
                stack.append((node, indent))
            else:
                ast.append(node)
                stack.append((node, indent))

    for indent, text in lines:
        # function: function name arg:
        m = re.match(r'^function\s+(\w+)(?:\s+([\w"\' ]+))?:$', text)
        if m:
            name = m.group(1)
            arg_raw = m.group(2)
            args = []
            if arg_raw:
                # handle simple quoted arg or single word
                args = [arg_raw.strip().strip('"\'') ]
            node = {'type':'function', 'name':name, 'args': args, 'body': []}
            push_node(node, indent)
            continue

        # if condition
        m = re.match(r'^if\s+(.+):$', text)
        if m:
            cond = m.group(1).strip()
            node = {'type':'if', 'condition': cond, 'then': []}
            # attach to current container (top of stack)
            if stack:
                parent = stack[-1][0]
                parent.setdefault('body', []).append(node)
            else:
                ast.append(node)
            # push if container with synthetic indent
            stack.append((node, indent))
            continue

        # else
        if text.startswith('else:'):
            node = {'type':'else', 'body': []}
            if stack:
                parent = stack[-1][0]
                parent.setdefault('body', []).append(node)
            else:
                ast.append(node)
            stack.append((node, indent))
            continue

        # return
        m = re.match(r'^return\s+(.+)$', text)
        if m:
            val = m.group(1).strip()
            node = {'type':'return', 'value': val}
            if stack:
                parent = stack[-1][0]
                parent.setdefault('body', []).append(node)
            else:
                ast.append(node)
            continue

        # generic expression
        node = {'type':'expr', 'value': text}
        if stack:
            parent = stack[-1][0]
            parent.setdefault('body', []).append(node)
        else:
            ast.append(node)

    # normalize if/else then/else bodies
    # convert 'if' nodes whose then is empty but body contains return/expr into then list
    def normalize(node):
        if isinstance(node, dict):
            if node.get('type') == 'if':
                if 'then' in node and not node['then']:
                    # move any children in node['body'] to node['then']
                    node['then'] = node.pop('body', []) if 'body' in node else []
            for k,v in list(node.items()):
                if isinstance(v, list):
                    for child in v:
                        normalize(child)
    for n in ast:
        normalize(n)

    return ast

# ---- Emitters ----
def emit_python(ast):
    lines = []
    def emit_node(node, indent_level=0):
        pad = INDENT * indent_level
        t = node.get('type')
        if t == 'function':
            args = ', '.join(node.get('args', []))
            lines.append(f"{pad}def {node['name']}({args}):")
            body = node.get('body', [])
            if not body:
                lines.append(pad + INDENT + 'pass')
            else:
                for child in body:
                    emit_node(child, indent_level+1)
        elif t == 'if':
            lines.append(f"{pad}if {node['condition']}:")
            then = node.get('then', []) or node.get('body', [])
            if not then:
                lines.append(pad + INDENT + 'pass')
            else:
                for child in then:
                    emit_node(child, indent_level+1)
            # check for else sibling
            for sibling in node.get('body', []):
                if sibling.get('type') == 'else':
                    lines.append(pad + 'else:')
                    for child in sibling.get('body', []):
                        emit_node(child, indent_level+1)
        elif t == 'else':
            # handled by if emitter
            pass
        elif t == 'return':
            lines.append(f"{pad}return {node['value']}")
        elif t == 'expr':
            lines.append(f"{pad}# expr: {node['value']}")
        else:
            lines.append(f"{pad}# unknown node: {node}")
    for n in ast:
        emit_node(n, 0)
    return "\n".join(lines)

def emit_html(ast):
    parts = ["<html>", "<body>", "<script>"]
    for node in ast:
        if node.get('type') == 'function':
            parts.append(f"// Function {node['name']}")
            parts.append("// (Generated from Orren)")
    parts.append("</script>")
    parts.append("</body>")
    parts.append("</html>")
    return '\n'.join(parts)

# ---- Public transpile API
def transpile(source, target='python'):
    ast = parse(source)
    if target == 'python':
        return emit_python(ast)
    elif target == 'html':
        return emit_html(ast)
    elif target == 'json':
        return json.dumps(ast, indent=2)
    else:
        return json.dumps({'error':'unknown target', 'ast': ast}, indent=2)

# ---- CLI
def main():
    if len(sys.argv) < 2:
        print('Usage: python orren.py <source.orren> [--target=python|html|json]')
        sys.exit(1)
    src = Path(sys.argv[1])
    if not src.exists():
        print('Source file not found:', src)
        sys.exit(1)
    target = 'python'
    for arg in sys.argv[2:]:
        if arg.startswith('--target='):
            target = arg.split('=',1)[1]
    source = src.read_text()
    out = transpile(source, target)
    out_path = src.with_suffix('.' + target)
    out_path.write_text(out)
    print(f'✅ Transpiled {src.name} → {out_path.name}')

if __name__ == '__main__':
    main()
