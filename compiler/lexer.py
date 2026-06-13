from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from compiler.errors import LexicalError


class TokenType(Enum):
    INT = "INT"
    BOOL = "BOOL"
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    PRINT = "PRINT"
    READ = "READ"

    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"

    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"

    ASSIGN = "ASSIGN"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"

    AND = "AND"
    OR = "OR"
    NOT = "NOT"

    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    SEMICOLON = "SEMICOLON"

    EOF = "EOF"


@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int


KEYWORDS = {
    "int": TokenType.INT,
    "bool": TokenType.BOOL,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "print": TokenType.PRINT,
    "read": TokenType.READ,
}


SINGLE_CHAR_TOKENS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
    "{": TokenType.LEFT_BRACE,
    "}": TokenType.RIGHT_BRACE,
    ";": TokenType.SEMICOLON,
}


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []
        self.current = 0
        self.line = 1
        self.column = 1

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens

    def _scan_token(self) -> None:
        char = self._advance()
        start_line = self.line
        start_column = self.column - 1

        if char in (" ", "\r", "\t"):
            return

        if char == "\n":
            self.line += 1
            self.column = 1
            return

        if char == "/" and self._match("/"):
            self._skip_comment()
            return

        if char in SINGLE_CHAR_TOKENS:
            self._add_token(SINGLE_CHAR_TOKENS[char], char, start_line, start_column)
            return

        if char == "/":
            self._add_token(TokenType.SLASH, char, start_line, start_column)
            return

        if char == "=":
            token_type = TokenType.EQUAL if self._match("=") else TokenType.ASSIGN
            lexeme = "==" if token_type == TokenType.EQUAL else "="
            self._add_token(token_type, lexeme, start_line, start_column)
            return

        if char == "!":
            token_type = TokenType.NOT_EQUAL if self._match("=") else TokenType.NOT
            lexeme = "!=" if token_type == TokenType.NOT_EQUAL else "!"
            self._add_token(token_type, lexeme, start_line, start_column)
            return

        if char == "<":
            token_type = TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
            lexeme = "<=" if token_type == TokenType.LESS_EQUAL else "<"
            self._add_token(token_type, lexeme, start_line, start_column)
            return

        if char == ">":
            token_type = TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
            lexeme = ">=" if token_type == TokenType.GREATER_EQUAL else ">"
            self._add_token(token_type, lexeme, start_line, start_column)
            return

        if char == "&":
            if self._match("&"):
                self._add_token(TokenType.AND, "&&", start_line, start_column)
                return
            raise LexicalError("operador '&' incompleto, use '&&'", start_line, start_column)

        if char == "|":
            if self._match("|"):
                self._add_token(TokenType.OR, "||", start_line, start_column)
                return
            raise LexicalError("operador '|' incompleto, use '||'", start_line, start_column)

        if char.isdigit():
            self._number(char, start_line, start_column)
            return

        if char == '"':
            self._string(start_line, start_column)
            return

        if char.isalpha() or char == "_":
            self._identifier(char, start_line, start_column)
            return

        raise LexicalError(f"caractere inesperado '{char}'", start_line, start_column)

    def _number(self, first_char: str, line: int, column: int) -> None:
        lexeme = first_char

        while self._peek().isdigit():
            lexeme += self._advance()

        self._add_token(TokenType.NUMBER, lexeme, line, column)

    def _string(self, line: int, column: int) -> None:
        lexeme = ""

        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                raise LexicalError("string nao finalizada", line, column)

            lexeme += self._advance()

        if self._is_at_end():
            raise LexicalError("string nao finalizada", line, column)

        self._advance()
        self._add_token(TokenType.STRING, lexeme, line, column)

    def _identifier(self, first_char: str, line: int, column: int) -> None:
        lexeme = first_char

        while self._peek().isalnum() or self._peek() == "_":
            lexeme += self._advance()

        token_type = KEYWORDS.get(lexeme, TokenType.IDENTIFIER)
        self._add_token(token_type, lexeme, line, column)

    def _skip_comment(self) -> None:
        while self._peek() != "\n" and not self._is_at_end():
            self._advance()

    def _add_token(self, token_type: TokenType, lexeme: str, line: int, column: int) -> None:
        self.tokens.append(Token(token_type, lexeme, line, column))

    def _advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        self.column += 1
        return char

    def _match(self, expected: str) -> bool:
        if self._is_at_end() or self.source[self.current] != expected:
            return False

        self.current += 1
        self.column += 1
        return True

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)


def tokenize(source: str) -> list[Token]:
    return Lexer(source).scan_tokens()
