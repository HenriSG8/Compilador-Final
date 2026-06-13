# Codigo Intermediario

Depois da analise semantica, o compilador gera uma representacao intermediaria em Codigo de Tres Enderecos, tambem chamado de TAC.

A ideia dessa etapa e transformar a AST em instrucoes mais simples, usando temporarios e rotulos. Isso facilita a proxima fase, que sera a traducao para Assembly MIPS.

## Temporarios

Expressoes compostas sao divididas em partes menores.

Codigo fonte:

```c
x = 2 + 3 * 4;
```

Codigo intermediario:

```text
t1 = 3 * 4
t2 = 2 + t1
x = t2
```

## Rotulos

Comandos de controle usam rotulos para representar saltos.

Codigo fonte:

```c
while (x > 0) {
    x = x - 1;
}
```

Codigo intermediario:

```text
L1:
t1 = x > 0
ifFalse t1 goto L2
t2 = x - 1
x = t2
goto L1
L2:
```

## Instrucoes Usadas

```text
declare tipo nome
variavel = valor
temporario = esquerda operador direita
temporario = operador valor
temporario = read
print valor
ifFalse condicao goto rotulo
goto rotulo
rotulo:
```
