#!/usr/bin/env python3
# Orren CLI Runner v1 — dual-mode (REPL + subcommands)
import sys
import os
from pathlib import Path
from src.core.orren import ORNEngine

ROOT = Path(__file__).resolve().parents[2]

USAGE = """Orren CLI
Usage:
  orn                 # interactive REPL
  orn run <file>      # run a .orren file
  orn transpile <file> --to <target>  # transpile (placeholder)
  orn init <project>  # create project scaffold
  orn help
"""

def run_file(path):
    path = Path(path)
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(2)
    code = path.read_text(encoding='utf-8')
    engine = ORNEngine()
    engine.run(code)

def repl():
    print("Orren REPL — ORN v1.0 (type 'exit' or Ctrl-D to quit)")
    engine = ORNEngine()
    try:
        while True:
            try:
                line = input("ORN> ")
            except EOFError:
                print()
                break
            if not line:
                continue
            if line.strip() in ("exit", "quit"):
                break
            # support single-line execution
            engine.execute_line(line)
    except KeyboardInterrupt:
        print("\nExiting REPL.")

def transpile(path, target):
    # Placeholder: call the meta-transpiler module (to be implemented)
    # For now, just print intention and write a stub file.
    path = Path(path)
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(2)
    target = target.lower()
    out = Path.cwd() / (path.stem + f".{target}")
    print(f"[transpile] {path} -> {out} (target={target})")
    out.write_text(f"// Transpiled stub from {path.name} to {target}\n", encoding='utf-8')
    print("Wrote:", out)

def init_project(name):
    base = Path(name)
    if base.exists():
        print("Project already exists:", base)
        return
    base.mkdir(parents=True)
    (base / "main.orren").write_text('say "Hello from Orren project!"\n', encoding='utf-8')
    (base / "README.md").write_text(f"# {name}\n\nCreated by Orren.\n", encoding='utf-8')
    print("Initialized Orren project at", base)

def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        repl()
        return
    cmd = argv[0]
    if cmd in ("-h", "help", "--help"):
        print(USAGE); return
    if cmd == "run" and len(argv) >= 2:
        run_file(argv[1]); return
    if cmd == "transpile" and len(argv) >= 3:
        # expect: transpile <file> --to <target>
        target = None
        if "--to" in argv:
            idx = argv.index("--to")
            if idx + 1 < len(argv):
                target = argv[idx+1]
        if not target:
            print("Usage: orn transpile <file> --to <target>"); sys.exit(2)
        transpile(argv[1], target); return
    if cmd == "init" and len(argv) >= 2:
        init_project(argv[1]); return
    if cmd == "repl":
        repl(); return
    print("Unknown command.") ; print(USAGE)

if __name__ == "__main__":
    main()
