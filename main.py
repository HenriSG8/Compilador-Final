from __future__ import annotations

import sys
from pathlib import Path

from compiler.errors import CompilerError
from compiler.ir import generate_ir
from compiler.lexer import tokenize
from compiler.parser import parse
from compiler.semantic import analyze


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
        program = parse(tokens)
        analyze(program)
        instructions = generate_ir(program)
    except CompilerError as error:
        print(error)
        return 1

    print("Analises lexica, sintatica e semantica concluidas com sucesso.")
    print(f"Declaracoes encontradas: {len(program.declarations)}")
    print()
    print("Codigo intermediario:")

    for instruction in instructions:
        print(instruction)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
