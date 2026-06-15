from __future__ import annotations

import sys
from pathlib import Path

from compiler.errors import CompilerError
from compiler.ir import generate_ir
from compiler.lexer import tokenize
from compiler.mips import generate_mips
from compiler.optimizer import optimize
from compiler.parser import parse
from compiler.semantic import analyze


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("Uso: python main.py <arquivo-fonte> [saida.asm]")
        return 1

    source_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) == 3 else None

    if not source_path.exists():
        print(f"Arquivo nao encontrado: {source_path}")
        return 1

    source_code = source_path.read_text(encoding="utf-8")

    try:
        # Pipeline principal: texto fonte -> tokens -> AST -> verificacao -> IR -> MIPS.
        tokens = tokenize(source_code)
        program = parse(tokens)
        analyze(program)
        program = optimize(program)
        instructions = generate_ir(program)
        mips_code = generate_mips(instructions)
    except CompilerError as error:
        print(error)
        return 1

    print("Analises lexica, sintatica e semantica concluidas com sucesso.")
    print(f"Declaracoes encontradas: {len(program.declarations)}")
    print()
    print("Codigo intermediario:")

    for instruction in instructions:
        print(instruction)

    print()
    print("Assembly MIPS:")
    print(mips_code)

    if output_path is not None:
        try:
            # A geracao sempre acontece antes; salvar em arquivo e uma etapa opcional.
            output_path.write_text(mips_code, encoding="utf-8")
        except OSError as error:
            print()
            print(f"Nao foi possivel salvar o Assembly: {error}")
            return 1

        print()
        print(f"Assembly salvo em: {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
