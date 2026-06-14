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


class Optimizer:
    def optimize(self, program: Program) -> Program:
        declarations = []

        for declaration in program.declarations:
            optimized = self._optimize_declaration(declaration)

            if optimized is None:
                continue

            if isinstance(optimized, list):
                declarations.extend(optimized)
            else:
                declarations.append(optimized)

        return Program(declarations)

    def _optimize_declaration(self, declaration):
        if isinstance(declaration, VarDeclaration):
            return declaration

        return self._optimize_statement(declaration)

    def _optimize_statement(self, statement):
        if isinstance(statement, Assignment):
            return Assignment(statement.name, self._optimize_expression(statement.value))

        if isinstance(statement, PrintStatement):
            return PrintStatement(self._optimize_expression(statement.value))

        if isinstance(statement, Block):
            declarations = []

            for declaration in statement.declarations:
                optimized = self._optimize_declaration(declaration)

                if optimized is None:
                    continue

                if isinstance(optimized, list):
                    declarations.extend(optimized)
                else:
                    declarations.append(optimized)

            return Block(declarations)

        if isinstance(statement, IfStatement):
            condition = self._optimize_expression(statement.condition)
            then_branch = self._optimize_statement(statement.then_branch)
            else_branch = None

            if statement.else_branch is not None:
                else_branch = self._optimize_statement(statement.else_branch)

            if self._is_bool_literal(condition):
                return then_branch if condition.value else else_branch

            return IfStatement(condition, then_branch, else_branch)

        if isinstance(statement, WhileStatement):
            condition = self._optimize_expression(statement.condition)
            body = self._optimize_statement(statement.body)

            if self._is_bool_literal(condition) and condition.value is False:
                return None

            return WhileStatement(condition, body)

        return statement

    def _optimize_expression(self, expression):
        if isinstance(expression, BinaryExpression):
            left = self._optimize_expression(expression.left)
            right = self._optimize_expression(expression.right)

            if isinstance(left, Literal) and isinstance(right, Literal):
                folded = self._fold_binary(left, expression.operator, right)

                if folded is not None:
                    return folded

            return BinaryExpression(left, expression.operator, right)

        if isinstance(expression, UnaryExpression):
            operand = self._optimize_expression(expression.operand)

            if isinstance(operand, Literal):
                folded = self._fold_unary(expression.operator, operand)

                if folded is not None:
                    return folded

            return UnaryExpression(expression.operator, operand)

        if isinstance(expression, (Literal, Variable, ReadExpression)):
            return expression

        return expression

    def _fold_binary(
        self, left: Literal, operator: str, right: Literal
    ) -> Literal | None:
        if left.literal_type == "int" and right.literal_type == "int":
            if operator == "+":
                return Literal(left.value + right.value, "int")
            if operator == "-":
                return Literal(left.value - right.value, "int")
            if operator == "*":
                return Literal(left.value * right.value, "int")
            if operator == "/" and right.value != 0:
                return Literal(left.value // right.value, "int")
            if operator == "<":
                return Literal(left.value < right.value, "bool")
            if operator == ">":
                return Literal(left.value > right.value, "bool")
            if operator == "<=":
                return Literal(left.value <= right.value, "bool")
            if operator == ">=":
                return Literal(left.value >= right.value, "bool")
            if operator == "==":
                return Literal(left.value == right.value, "bool")
            if operator == "!=":
                return Literal(left.value != right.value, "bool")

        if left.literal_type == "bool" and right.literal_type == "bool":
            if operator == "&&":
                return Literal(left.value and right.value, "bool")
            if operator == "||":
                return Literal(left.value or right.value, "bool")
            if operator == "==":
                return Literal(left.value == right.value, "bool")
            if operator == "!=":
                return Literal(left.value != right.value, "bool")

        return None

    def _fold_unary(self, operator: str, operand: Literal) -> Literal | None:
        if operator == "-" and operand.literal_type == "int":
            return Literal(-operand.value, "int")

        if operator == "!" and operand.literal_type == "bool":
            return Literal(not operand.value, "bool")

        return None

    def _is_bool_literal(self, expression) -> bool:
        return isinstance(expression, Literal) and expression.literal_type == "bool"


def optimize(program: Program) -> Program:
    return Optimizer().optimize(program)
