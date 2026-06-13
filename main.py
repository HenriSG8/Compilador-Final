from __future__ import annotations

import sys
from pathlib import Path

from compiler.errors import CompilerError
from compiler.lexer import tokenize


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo-fonte>")
        return 1

    source_path = Path(sys.argv[1])

    if not source_path.exists():
        print(f"Arquivo nao encontrado: {source_path}")
        return 1

    source_code = source_path.read_text(encoding="utf-8")

    try:
        tokens = tokenize(source_code)
    except CompilerError as error:
        print(error)
        return 1

    for token in tokens:
        print(f"{token.line}:{token.column} {token.type.value} {token.lexeme}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
