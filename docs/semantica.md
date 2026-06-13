# Analise Semantica

A analise semantica verifica se o programa faz sentido depois de passar pela analise lexica e sintatica.

Nesta etapa foram implementadas as seguintes verificacoes:

- variavel precisa ser declarada antes do uso;
- nao pode haver duas variaveis com o mesmo nome no mesmo escopo;
- atribuicoes devem respeitar o tipo declarado da variavel;
- condicoes de `if` e `while` devem ser do tipo `bool`;
- operadores aritmeticos aceitam apenas valores `int`;
- operadores relacionais comparam valores `int` e retornam `bool`;
- operadores logicos aceitam apenas valores `bool`;
- `read()` retorna um valor `int`;
- `print` aceita expressoes validas.

## Tabela de Simbolos

A tabela de simbolos guarda o nome e o tipo de cada variavel declarada.

Como a linguagem permite blocos com `{` e `}`, a implementacao usa uma pilha de escopos. Quando o analisador entra em um bloco, um novo escopo e criado. Quando sai do bloco, esse escopo e removido.

Exemplo:

```c
int x;

if (x > 0) {
    int y;
    y = x + 1;
}
```

No exemplo acima, `x` pertence ao escopo global e `y` pertence apenas ao bloco do `if`.

## Exemplos de Erros Detectados

Variavel nao declarada:

```c
x = 10;
```

Atribuicao com tipo incorreto:

```c
int x;
x = true;
```

Condicao que nao retorna booleano:

```c
int x;

if (x) {
    print(x);
}
```
