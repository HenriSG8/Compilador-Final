# Especificacao da Linguagem

Este documento descreve a linguagem usada no compilador do projeto. A sintaxe foi pensada para ser parecida com C, mas reduzida para facilitar a implementacao das etapas do compilador.

## Caracteristicas Gerais

- Linguagem imperativa simples.
- Tipagem estatica.
- Tipos suportados: `int` e `bool`.
- Literais suportados: numeros inteiros, booleanos e strings.
- Comandos suportados: declaracao, atribuicao, `if/else`, `while`, `print` e `read`.
- Codigo final planejado: Assembly MIPS.

## Exemplo de Programa

```c
int x;
bool positivo;

x = read();
positivo = x > 0;

if (positivo) {
    print(x);
} else {
    print(0);
}

while (x > 0) {
    x = x - 1;
}
```

## Palavras Reservadas

```text
int
bool
true
false
if
else
while
print
read
```

## Tipos

### Inteiro

O tipo `int` representa numeros inteiros.

```c
int idade;
idade = 20;
```

### Booleano

O tipo `bool` representa valores logicos.

```c
bool ativo;
ativo = true;
```

### String

Strings podem aparecer como literais, principalmente no comando `print`. Elas nao sao usadas como tipo de variavel nesta versao da linguagem.

```c
print("resultado");
```

## Declaracao de Variaveis

Toda variavel deve ser declarada antes de ser usada.

```c
int x;
bool ok;
```

## Atribuicao

A atribuicao usa o operador `=`.

```c
x = 10;
ok = x > 5;
```

## Entrada e Saida

O comando `read()` le um numero inteiro.

```c
x = read();
```

O comando `print` imprime o valor de uma expressao.

```c
print(x);
print(10);
print("fim");
```

## Estruturas de Controle

### Condicional

```c
if (x > 0) {
    print(x);
} else {
    print(0);
}
```

### Repeticao

```c
while (x > 0) {
    x = x - 1;
}
```

## Operadores

### Aritmeticos

```text
+  soma
-  subtracao
*  multiplicacao
/  divisao inteira
```

Os operadores aritmeticos trabalham com valores `int` e retornam `int`.

### Relacionais

```text
==  igual
!=  diferente
<   menor
>   maior
<=  menor ou igual
>=  maior ou igual
```

Os operadores relacionais comparam valores `int` e retornam `bool`.

### Logicos

```text
&&  E logico
||  OU logico
!   NAO logico
```

Os operadores logicos trabalham com valores `bool` e retornam `bool`.

## Comentarios

A linguagem aceita comentarios de uma linha.

```c
// Isto e um comentario
int x;
```

## Gramatica Inicial

A gramatica abaixo sera usada como base para o parser descendente recursivo.

```text
programa      -> declaracao* EOF

declaracao    -> declaracao_var
              | comando

declaracao_var -> tipo IDENTIFICADOR ";"

tipo          -> "int"
              | "bool"

comando       -> atribuicao ";"
              | comando_if
              | comando_while
              | comando_print ";"
              | bloco

bloco         -> "{" declaracao* "}"

atribuicao    -> IDENTIFICADOR "=" expressao

comando_if    -> "if" "(" expressao ")" comando ("else" comando)?

comando_while -> "while" "(" expressao ")" comando

comando_print -> "print" "(" expressao ")"

expressao     -> ou_logico
ou_logico     -> e_logico ("||" e_logico)*
e_logico      -> igualdade ("&&" igualdade)*
igualdade     -> comparacao (("==" | "!=") comparacao)*
comparacao    -> termo (("<" | ">" | "<=" | ">=") termo)*
termo         -> fator (("+" | "-") fator)*
fator         -> unario (("*" | "/") unario)*
unario        -> ("!" | "-") unario
              | primario

primario      -> NUMERO
              | STRING
              | "true"
              | "false"
              | IDENTIFICADOR
              | "read" "(" ")"
              | "(" expressao ")"
```

## Observacoes Para Implementacao

- O scanner devera ignorar espacos, quebras de linha e comentarios.
- O parser devera montar uma AST simples.
- A analise semantica devera impedir uso de variaveis nao declaradas.
- A geracao final sera feita em Assembly MIPS.
