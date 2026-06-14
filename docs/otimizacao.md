# Otimizacao

A etapa de otimizacao foi implementada de forma simples, antes da geracao de codigo intermediario.

O otimizador percorre a AST e aplica duas ideias principais:

- simplificacao de expressoes constantes;
- remocao de alguns comandos que nao precisam ser executados.

## Simplificacao de Expressoes

Quando uma expressao depende apenas de valores constantes, ela pode ser calculada durante a compilacao.

Exemplo:

```c
int x;
x = 2 + 3 * 4;
```

Depois da otimizacao, a expressao vira:

```c
x = 14;
```

Isso reduz a quantidade de temporarios e instrucoes no codigo intermediario.

## Condicionais Constantes

Quando a condicao de um `if` e conhecida durante a compilacao, apenas o bloco necessario e mantido.

```c
if (true) {
    print(1);
} else {
    print(0);
}
```

Nesse caso, o compilador mantem apenas:

```c
print(1);
```

## Lacos Sem Execucao

Um `while` com condicao constante falsa nao executa nenhuma vez.

```c
while (false) {
    print(1);
}
```

Esse comando e removido antes da geracao de TAC.
