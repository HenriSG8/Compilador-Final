from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from compiler.errors import CompilerError
from compiler.ir import generate_ir
from compiler.lexer import tokenize
from compiler.mips import generate_mips
from compiler.optimizer import optimize
from compiler.parser import parse
from compiler.semantic import analyze


ROOT = Path(__file__).resolve().parents[1]


def compile_source(source: str):
    tokens = tokenize(source)
    program = parse(tokens)
    analyze(program)
    program = optimize(program)
    instructions = generate_ir(program)
    mips_code = generate_mips(instructions)
    return instructions, mips_code


def read_example(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_valid(path: str) -> None:
    instructions, mips_code = compile_source(read_example(path))

    assert instructions, f"{path} nao gerou codigo intermediario"
    assert ".text" in mips_code, f"{path} nao gerou secao .text"
    assert "main:" in mips_code, f"{path} nao gerou label main"


def assert_invalid(path: str, expected: str) -> None:
    try:
        compile_source(read_example(path))
    except CompilerError as error:
        assert expected in str(error), f"{path} gerou erro diferente: {error}"
        return

    raise AssertionError(f"{path} deveria falhar")


def test_constant_folding() -> None:
    source = read_example("exemplos/otimizacao.hc")
    instructions, _ = compile_source(source)
    text = "\n".join(str(instruction) for instruction in instructions)

    assert "x = 14" in text
    assert "ifFalse" not in text
    assert "goto" not in text
    assert "print 1" not in text


def test_output_file() -> None:
    output_path = ROOT / "saida_teste.asm"

    if output_path.exists():
        output_path.unlink()

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "main.py"),
            str(ROOT / "exemplos" / "strings.hc"),
            str(output_path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert output_path.exists()
    assert ".text" in output_path.read_text(encoding="utf-8")

    output_path.unlink()


def test_invalid_output_file() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "main.py"),
            str(ROOT / "exemplos" / "strings.hc"),
            str(ROOT / "pasta_inexistente" / "saida.asm"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "Nao foi possivel salvar" in result.stdout


def main() -> int:
    assert_valid("exemplos/exemplo_basico.hc")
    assert_valid("exemplos/strings.hc")
    assert_valid("exemplos/otimizacao.hc")

    assert_invalid("exemplos/erros/variavel_nao_declarada.hc", "nao foi declarada")
    assert_invalid("exemplos/erros/tipo_incorreto.hc", "recebeu bool")
    assert_invalid("exemplos/erros/sintaxe_sem_ponto_virgula.hc", "esperado ';'")
    assert_invalid("exemplos/erros/variavel_redeclarada_bloco.hc", "ja foi declarada")
    assert_invalid("exemplos/erros/nome_reservado_interno.hc", "reservado")

    test_constant_folding()
    test_output_file()
    test_invalid_output_file()

    print("Todos os testes passaram.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
