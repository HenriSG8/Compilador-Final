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
from compiler.errors import SemanticError


class SymbolTable:
    def __init__(self) -> None:
        self.scopes: list[dict[str, str]] = [{}]

    def begin_scope(self) -> None:
        self.scopes.append({})

    def end_scope(self) -> None:
        self.scopes.pop()

    def define(self, name: str, var_type: str) -> None:
        current_scope = self.scopes[-1]

        if name in current_scope:
            raise SemanticError(f"variavel '{name}' ja foi declarada neste escopo")

        current_scope[name] = var_type

    def get(self, name: str) -> str:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]

        raise SemanticError(f"variavel '{name}' nao foi declarada")


class SemanticAnalyzer:
    def __init__(self) -> None:
        self.symbols = SymbolTable()

    def analyze(self, program: Program) -> None:
        for declaration in program.declarations:
            self._analyze_declaration(declaration)

    def _analyze_declaration(self, declaration) -> None:
        if isinstance(declaration, VarDeclaration):
            self.symbols.define(declaration.name, declaration.var_type)
            return

        self._analyze_statement(declaration)

    def _analyze_statement(self, statement) -> None:
        if isinstance(statement, Assignment):
            variable_type = self.symbols.get(statement.name)
            value_type = self._expression_type(statement.value)

            if variable_type != value_type:
                raise SemanticError(
                    f"variavel '{statement.name}' e do tipo {variable_type}, "
                    f"mas recebeu {value_type}"
                )
            return

        if isinstance(statement, PrintStatement):
            self._expression_type(statement.value)
            return

        if isinstance(statement, IfStatement):
            condition_type = self._expression_type(statement.condition)

            if condition_type != "bool":
                raise SemanticError("condicao do if deve ser bool")

            self._analyze_statement(statement.then_branch)

            if statement.else_branch is not None:
                self._analyze_statement(statement.else_branch)
            return

        if isinstance(statement, WhileStatement):
            condition_type = self._expression_type(statement.condition)

            if condition_type != "bool":
                raise SemanticError("condicao do while deve ser bool")

            self._analyze_statement(statement.body)
            return

        if isinstance(statement, Block):
            self.symbols.begin_scope()

            for declaration in statement.declarations:
                self._analyze_declaration(declaration)

            self.symbols.end_scope()
            return

        raise SemanticError("comando nao reconhecido na analise semantica")

    def _expression_type(self, expression) -> str:
        if isinstance(expression, Literal):
            return expression.literal_type

        if isinstance(expression, Variable):
            return self.symbols.get(expression.name)

        if isinstance(expression, ReadExpression):
            return "int"

        if isinstance(expression, UnaryExpression):
            operand_type = self._expression_type(expression.operand)

            if expression.operator == "-" and operand_type == "int":
                return "int"

            if expression.operator == "!" and operand_type == "bool":
                return "bool"

            raise SemanticError(
                f"operador unario '{expression.operator}' nao aceita {operand_type}"
            )

        if isinstance(expression, BinaryExpression):
            return self._binary_expression_type(expression)

        raise SemanticError("expressao nao reconhecida na analise semantica")

    def _binary_expression_type(self, expression: BinaryExpression) -> str:
        left_type = self._expression_type(expression.left)
        right_type = self._expression_type(expression.right)
        operator = expression.operator

        if operator in {"+", "-", "*", "/"}:
            if left_type == "int" and right_type == "int":
                return "int"

            raise SemanticError(
                f"operador '{operator}' exige int dos dois lados"
            )

        if operator in {"<", ">", "<=", ">="}:
            if left_type == "int" and right_type == "int":
                return "bool"

            raise SemanticError(
                f"operador '{operator}' compara apenas valores int"
            )

        if operator in {"==", "!="}:
            if left_type == right_type and left_type in {"int", "bool"}:
                return "bool"

            raise SemanticError(
                f"operador '{operator}' exige operandos do mesmo tipo"
            )

        if operator in {"&&", "||"}:
            if left_type == "bool" and right_type == "bool":
                return "bool"

            raise SemanticError(
                f"operador '{operator}' exige bool dos dois lados"
            )

        raise SemanticError(f"operador '{operator}' nao reconhecido")


def analyze(program: Program) -> None:
    SemanticAnalyzer().analyze(program)
