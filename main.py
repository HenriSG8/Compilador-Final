from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo-fonte>")
        return 1

    source_path = Path(sys.argv[1])

    if not source_path.exists():
        print(f"Arquivo nao encontrado: {source_path}")
        return 1

    source_code = source_path.read_text(encoding="utf-8")

    print("Compilador iniciado.")
    print(f"Arquivo: {source_path}")
    print(f"Tamanho: {len(source_code)} caracteres")
    print()
    print("As fases do compilador ainda serao implementadas.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
