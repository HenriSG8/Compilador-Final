from __future__ import annotations

from dataclasses import dataclass

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


@dataclass(frozen=True)
class TACInstruction:
    operation: str
    arg1: str | None = None
    arg2: str | None = None
    result: str | None = None

    def __str__(self) -> str:
        if self.operation == "label":
            return f"{self.result}:"

        if self.operation == "goto":
            return f"goto {self.result}"

        if self.operation == "if_false":
            return f"ifFalse {self.arg1} goto {self.result}"

        if self.operation == "assign":
            return f"{self.result} = {self.arg1}"

        if self.operation == "binary":
            return f"{self.result} = {self.arg1} {self.arg2}"

        if self.operation == "unary":
            return f"{self.result} = {self.arg1}"

        if self.operation == "read":
            return f"{self.result} = read"

        if self.operation == "print":
            return f"print {self.arg1}"

        if self.operation == "declare":
            return f"declare {self.arg1} {self.result}"

        return self.operation


class IRGenerator:
    def __init__(self) -> None:
        self.instructions: list[TACInstruction] = []
        self.temp_count = 0
        self.label_count = 0

    def generate(self, program: Program) -> list[TACInstruction]:
        for declaration in program.declarations:
            self._generate_declaration(declaration)

        return self.instructions

    def _generate_declaration(self, declaration) -> None:
        if isinstance(declaration, VarDeclaration):
            self.instructions.append(
                TACInstruction("declare", declaration.var_type, result=declaration.name)
            )
            return

        self._generate_statement(declaration)

    def _generate_statement(self, statement) -> None:
        if isinstance(statement, Assignment):
            value = self._generate_expression(statement.value)
            self.instructions.append(TACInstruction("assign", value, result=statement.name))
            return

        if isinstance(statement, PrintStatement):
            value = self._generate_expression(statement.value)
            self.instructions.append(TACInstruction("print", value))
            return

        if isinstance(statement, Block):
            for declaration in statement.declarations:
                self._generate_declaration(declaration)
            return

        if isinstance(statement, IfStatement):
            self._generate_if(statement)
            return

        if isinstance(statement, WhileStatement):
            self._generate_while(statement)
            return

    def _generate_if(self, statement: IfStatement) -> None:
        else_label = self._new_label()
        end_label = self._new_label()
        condition = self._generate_expression(statement.condition)

        self.instructions.append(TACInstruction("if_false", condition, result=else_label))
        self._generate_statement(statement.then_branch)

        if statement.else_branch is None:
            self.instructions.append(TACInstruction("label", result=else_label))
            return

        self.instructions.append(TACInstruction("goto", result=end_label))
        self.instructions.append(TACInstruction("label", result=else_label))
        self._generate_statement(statement.else_branch)
        self.instructions.append(TACInstruction("label", result=end_label))

    def _generate_while(self, statement: WhileStatement) -> None:
        start_label = self._new_label()
        end_label = self._new_label()

        self.instructions.append(TACInstruction("label", result=start_label))
        condition = self._generate_expression(statement.condition)
        self.instructions.append(TACInstruction("if_false", condition, result=end_label))
        self._generate_statement(statement.body)
        self.instructions.append(TACInstruction("goto", result=start_label))
        self.instructions.append(TACInstruction("label", result=end_label))

    def _generate_expression(self, expression) -> str:
        if isinstance(expression, Literal):
            return self._literal_value(expression)

        if isinstance(expression, Variable):
            return expression.name

        if isinstance(expression, ReadExpression):
            temp = self._new_temp()
            self.instructions.append(TACInstruction("read", result=temp))
            return temp

        if isinstance(expression, UnaryExpression):
            value = self._generate_expression(expression.operand)
            temp = self._new_temp()
            self.instructions.append(
                TACInstruction("unary", f"{expression.operator}{value}", result=temp)
            )
            return temp

        if isinstance(expression, BinaryExpression):
            left = self._generate_expression(expression.left)
            right = self._generate_expression(expression.right)
            temp = self._new_temp()
            operation = f"{expression.operator} {right}"
            self.instructions.append(TACInstruction("binary", left, operation, temp))
            return temp

        raise ValueError("expressao nao reconhecida na geracao de IR")

    def _literal_value(self, literal: Literal) -> str:
        if literal.literal_type == "bool":
            return "true" if literal.value else "false"

        if literal.literal_type == "string":
            return f'"{literal.value}"'

        return str(literal.value)

    def _new_temp(self) -> str:
        self.temp_count += 1
        return f"t{self.temp_count}"

    def _new_label(self) -> str:
        self.label_count += 1
        return f"L{self.label_count}"


def generate_ir(program: Program) -> list[TACInstruction]:
    return IRGenerator().generate(program)
