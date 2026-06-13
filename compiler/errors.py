class CompilerError(Exception):
    """Erro base usado pelas fases do compilador."""


class LexicalError(CompilerError):
    def __init__(self, message: str, line: int, column: int) -> None:
        super().__init__(f"Erro lexico na linha {line}, coluna {column}: {message}")
        self.line = line
        self.column = column


class ParserError(CompilerError):
    def __init__(self, message: str, line: int, column: int) -> None:
        super().__init__(f"Erro sintatico na linha {line}, coluna {column}: {message}")
        self.line = line
        self.column = column


class SemanticError(CompilerError):
    def __init__(self, message: str) -> None:
        super().__init__(f"Erro semantico: {message}")
