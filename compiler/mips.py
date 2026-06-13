from __future__ import annotations

from compiler.ir import TACInstruction


class MIPSGenerator:
    def __init__(self, instructions: list[TACInstruction]) -> None:
        self.instructions = instructions
        self.lines: list[str] = []
        self.variables: set[str] = set()
        self.string_literals: dict[str, str] = {}
        self.string_count = 0

    def generate(self) -> str:
        self._collect_storage()
        self._emit_data_section()
        self._emit_text_section()
        return "\n".join(self.lines)

    def _collect_storage(self) -> None:
        for instruction in self.instructions:
            if instruction.operation == "declare" and instruction.result is not None:
                self.variables.add(instruction.result)

            if instruction.result is not None and self._is_temp(instruction.result):
                self.variables.add(instruction.result)

            if instruction.operation == "print" and self._is_string(instruction.arg1):
                self._string_label(instruction.arg1)

    def _emit_data_section(self) -> None:
        self.lines.append(".data")
        self.lines.append('newline: .asciiz "\\n"')

        for name in sorted(self.variables):
            self.lines.append(f"{name}: .word 0")

        for value, label in self.string_literals.items():
            text = value[1:-1]
            self.lines.append(f'{label}: .asciiz "{text}"')

    def _emit_text_section(self) -> None:
        self.lines.append("")
        self.lines.append(".text")
        self.lines.append(".globl main")
        self.lines.append("main:")

        for instruction in self.instructions:
            self._emit_instruction(instruction)

        self.lines.append("    li $v0, 10")
        self.lines.append("    syscall")

    def _emit_instruction(self, instruction: TACInstruction) -> None:
        if instruction.operation == "declare":
            return

        if instruction.operation == "label":
            self.lines.append(f"{instruction.result}:")
            return

        if instruction.operation == "goto":
            self.lines.append(f"    j {instruction.result}")
            return

        if instruction.operation == "if_false":
            self._load_value(instruction.arg1, "$t0")
            self.lines.append(f"    beq $t0, $zero, {instruction.result}")
            return

        if instruction.operation == "assign":
            self._load_value(instruction.arg1, "$t0")
            self._store_value("$t0", instruction.result)
            return

        if instruction.operation == "read":
            self.lines.append("    li $v0, 5")
            self.lines.append("    syscall")
            self._store_value("$v0", instruction.result)
            return

        if instruction.operation == "print":
            self._emit_print(instruction.arg1)
            return

        if instruction.operation == "unary":
            self._emit_unary(instruction)
            return

        if instruction.operation == "binary":
            self._emit_binary(instruction)
            return

    def _emit_print(self, value: str | None) -> None:
        if self._is_string(value):
            label = self._string_label(value)
            self.lines.append(f"    la $a0, {label}")
            self.lines.append("    li $v0, 4")
            self.lines.append("    syscall")
        else:
            self._load_value(value, "$a0")
            self.lines.append("    li $v0, 1")
            self.lines.append("    syscall")

        self.lines.append("    la $a0, newline")
        self.lines.append("    li $v0, 4")
        self.lines.append("    syscall")

    def _emit_unary(self, instruction: TACInstruction) -> None:
        expression = instruction.arg1 or ""
        operator = expression[0]
        value = expression[1:]

        self._load_value(value, "$t0")

        if operator == "-":
            self.lines.append("    neg $t2, $t0")
        elif operator == "!":
            self.lines.append("    seq $t2, $t0, $zero")

        self._store_value("$t2", instruction.result)

    def _emit_binary(self, instruction: TACInstruction) -> None:
        operator, right = self._split_binary_operation(instruction.arg2)

        self._load_value(instruction.arg1, "$t0")
        self._load_value(right, "$t1")

        if operator == "+":
            self.lines.append("    add $t2, $t0, $t1")
        elif operator == "-":
            self.lines.append("    sub $t2, $t0, $t1")
        elif operator == "*":
            self.lines.append("    mul $t2, $t0, $t1")
        elif operator == "/":
            self.lines.append("    div $t0, $t1")
            self.lines.append("    mflo $t2")
        elif operator == "<":
            self.lines.append("    slt $t2, $t0, $t1")
        elif operator == ">":
            self.lines.append("    sgt $t2, $t0, $t1")
        elif operator == "<=":
            self.lines.append("    sle $t2, $t0, $t1")
        elif operator == ">=":
            self.lines.append("    sge $t2, $t0, $t1")
        elif operator == "==":
            self.lines.append("    seq $t2, $t0, $t1")
        elif operator == "!=":
            self.lines.append("    sne $t2, $t0, $t1")
        elif operator == "&&":
            self.lines.append("    and $t2, $t0, $t1")
        elif operator == "||":
            self.lines.append("    or $t2, $t0, $t1")

        self._store_value("$t2", instruction.result)

    def _load_value(self, value: str | None, register: str) -> None:
        if value is None:
            return

        if value == "true":
            self.lines.append(f"    li {register}, 1")
            return

        if value == "false":
            self.lines.append(f"    li {register}, 0")
            return

        if self._is_integer(value):
            self.lines.append(f"    li {register}, {value}")
            return

        self.lines.append(f"    lw {register}, {value}")

    def _store_value(self, register: str, name: str | None) -> None:
        if name is not None:
            self.lines.append(f"    sw {register}, {name}")

    def _split_binary_operation(self, operation: str | None) -> tuple[str, str]:
        if operation is None:
            raise ValueError("operacao binaria incompleta")

        operator, right = operation.split(" ", 1)
        return operator, right

    def _string_label(self, value: str | None) -> str:
        if value is None:
            raise ValueError("string sem valor")

        if value not in self.string_literals:
            self.string_count += 1
            self.string_literals[value] = f"str_{self.string_count}"

        return self.string_literals[value]

    def _is_string(self, value: str | None) -> bool:
        return value is not None and len(value) >= 2 and value[0] == '"' and value[-1] == '"'

    def _is_integer(self, value: str) -> bool:
        if value.startswith("-"):
            return value[1:].isdigit()

        return value.isdigit()

    def _is_temp(self, value: str) -> bool:
        return value.startswith("t") and value[1:].isdigit()


def generate_mips(instructions: list[TACInstruction]) -> str:
    return MIPSGenerator(instructions).generate()
