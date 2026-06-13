from __future__ import annotations

from compiler.ast_nodes import (
    Assignment,
    BinaryExpression,
    Block,
    IfStatement,
    Literal,
    PrintStatement,
    Program,
    ReadExpression,
    UnaryExpression,
    VarDeclaration,
    Variable,
    WhileStatement,
)
from compiler.errors import ParserError
from compiler.lexer import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        declarations = []

        while not self._is_at_end():
            declarations.append(self._declaration())

        return Program(declarations)

    def _declaration(self):
        if self._match(TokenType.INT, TokenType.BOOL):
            return self._var_declaration(self._previous())

        return self._statement()

    def _var_declaration(self, type_token: Token) -> VarDeclaration:
        name = self._consume(TokenType.IDENTIFIER, "esperado nome da variavel")
        self._consume(TokenType.SEMICOLON, "esperado ';' depois da declaracao")
        return VarDeclaration(type_token.lexeme, name.lexeme)

    def _statement(self):
        if self._match(TokenType.IF):
            return self._if_statement()

        if self._match(TokenType.WHILE):
            return self._while_statement()

        if self._match(TokenType.PRINT):
            return self._print_statement()

        if self._match(TokenType.LEFT_BRACE):
            return Block(self._block())

        if self._check(TokenType.IDENTIFIER):
            statement = self._assignment()
            self._consume(TokenType.SEMICOLON, "esperado ';' depois da atribuicao")
            return statement

        token = self._peek()
        raise ParserError("esperado comando ou declaracao", token.line, token.column)

    def _if_statement(self) -> IfStatement:
        self._consume(TokenType.LEFT_PAREN, "esperado '(' depois de if")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "esperado ')' depois da condicao")

        then_branch = self._statement()
        else_branch = None

        if self._match(TokenType.ELSE):
            else_branch = self._statement()

        return IfStatement(condition, then_branch, else_branch)

    def _while_statement(self) -> WhileStatement:
        self._consume(TokenType.LEFT_PAREN, "esperado '(' depois de while")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "esperado ')' depois da condicao")
        body = self._statement()
        return WhileStatement(condition, body)

    def _print_statement(self) -> PrintStatement:
        self._consume(TokenType.LEFT_PAREN, "esperado '(' depois de print")
        value = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "esperado ')' depois do valor")
        self._consume(TokenType.SEMICOLON, "esperado ';' depois de print")
        return PrintStatement(value)

    def _block(self) -> list:
        declarations = []

        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            declarations.append(self._declaration())

        self._consume(TokenType.RIGHT_BRACE, "esperado '}' no final do bloco")
        return declarations

    def _assignment(self) -> Assignment:
        name = self._consume(TokenType.IDENTIFIER, "esperado nome da variavel")
        self._consume(TokenType.ASSIGN, "esperado '=' na atribuicao")
        value = self._expression()
        return Assignment(name.lexeme, value)

    def _expression(self):
        return self._or()

    def _or(self):
        expression = self._and()

        while self._match(TokenType.OR):
            operator = self._previous().lexeme
            right = self._and()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _and(self):
        expression = self._equality()

        while self._match(TokenType.AND):
            operator = self._previous().lexeme
            right = self._equality()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _equality(self):
        expression = self._comparison()

        while self._match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            operator = self._previous().lexeme
            right = self._comparison()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _comparison(self):
        expression = self._term()

        while self._match(
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
        ):
            operator = self._previous().lexeme
            right = self._term()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _term(self):
        expression = self._factor()

        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous().lexeme
            right = self._factor()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _factor(self):
        expression = self._unary()

        while self._match(TokenType.STAR, TokenType.SLASH):
            operator = self._previous().lexeme
            right = self._unary()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _unary(self):
        if self._match(TokenType.NOT, TokenType.MINUS):
            operator = self._previous().lexeme
            operand = self._unary()
            return UnaryExpression(operator, operand)

        return self._primary()

    def _primary(self):
        if self._match(TokenType.NUMBER):
            return Literal(int(self._previous().lexeme), "int")

        if self._match(TokenType.STRING):
            return Literal(self._previous().lexeme, "string")

        if self._match(TokenType.TRUE):
            return Literal(True, "bool")

        if self._match(TokenType.FALSE):
            return Literal(False, "bool")

        if self._match(TokenType.IDENTIFIER):
            return Variable(self._previous().lexeme)

        if self._match(TokenType.READ):
            self._consume(TokenType.LEFT_PAREN, "esperado '(' depois de read")
            self._consume(TokenType.RIGHT_PAREN, "esperado ')' depois de read")
            return ReadExpression()

        if self._match(TokenType.LEFT_PAREN):
            expression = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "esperado ')' depois da expressao")
            return expression

        token = self._peek()
        raise ParserError("esperada expressao", token.line, token.column)

    def _match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True

        return False

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()

        token = self._peek()
        raise ParserError(message, token.line, token.column)

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return token_type == TokenType.EOF

        return self._peek().type == token_type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1

        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]


def parse(tokens: list[Token]) -> Program:
    return Parser(tokens).parse()
