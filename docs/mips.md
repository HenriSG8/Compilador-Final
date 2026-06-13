# Geracao de Assembly MIPS

A ultima etapa do compilador traduz o Codigo de Tres Enderecos para Assembly MIPS.

O codigo gerado usa uma estrutura simples:

- secao `.data` para variaveis, temporarios e strings;
- secao `.text` para as instrucoes executaveis;
- `syscall 5` para leitura de inteiro;
- `syscall 1` para impressao de inteiro;
- `syscall 4` para impressao de string;
- `syscall 10` para encerrar o programa.

## Exemplo

Codigo fonte:

```c
int x;
x = read();
print(x);
```

Trecho de Assembly gerado:

```asm
.data
newline: .asciiz "\n"
t1: .word 0
x: .word 0

.text
.globl main
main:
    li $v0, 5
    syscall
    sw $v0, t1
    lw $t0, t1
    sw $t0, x
    lw $a0, x
    li $v0, 1
    syscall
    la $a0, newline
    li $v0, 4
    syscall
    li $v0, 10
    syscall
```

## Observacoes

Algumas instrucoes usadas, como `seq`, `sne`, `sle` e `sge`, sao pseudo-instrucoes aceitas por simuladores didaticos como MARS e SPIM. Elas deixam a traducao mais direta para um projeto academico introdutorio.
