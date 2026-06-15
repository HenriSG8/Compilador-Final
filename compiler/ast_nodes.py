from __future__ import annotations

from dataclasses import dataclass
from typing import Any


# A AST guarda a estrutura do programa depois da analise sintatica.
@dataclass(frozen=True)
class Program:
    declarations: list[Any]


# Declaracoes e comandos aparecem no corpo principal ou dentro de blocos.
@dataclass(frozen=True)
class VarDeclaration:
    var_type: str
    name: str


@dataclass(frozen=True)
class Block:
    declarations: list[Any]


@dataclass(frozen=True)
class Assignment:
    name: str
    value: Any


@dataclass(frozen=True)
class IfStatement:
    condition: Any
    then_branch: Any
    else_branch: Any | None


@dataclass(frozen=True)
class WhileStatement:
    condition: Any
    body: Any


@dataclass(frozen=True)
class PrintStatement:
    value: Any


# Expressoes produzem valores e podem ser usadas em atribuicoes, condicoes e prints.
@dataclass(frozen=True)
class BinaryExpression:
    left: Any
    operator: str
    right: Any


@dataclass(frozen=True)
class UnaryExpression:
    operator: str
    operand: Any


@dataclass(frozen=True)
class Literal:
    value: Any
    literal_type: str


@dataclass(frozen=True)
class Variable:
    name: str


@dataclass(frozen=True)
class ReadExpression:
    pass
