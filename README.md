# Compilador Didatico

Projeto de um compilador simples feito em Python para uma linguagem parecida com C.

O compilador sera dividido nas seguintes etapas:

1. Analise lexica. Feita.
2. Analise sintatica e AST. Feita.
3. Analise semantica. Feita.
4. Geracao de codigo intermediario.
5. Geracao de Assembly MIPS.

## Como Executar

```bash
python main.py exemplos/exemplo_basico.hc
```

No momento o projeto executa as analises lexica, sintatica e semantica.

## Estrutura

```text
compiler/
  lexer.py       analise lexica
  parser.py      analise sintatica
  ast_nodes.py   nos da AST
  semantic.py    analise semantica
  ir.py          codigo intermediario
  mips.py        geracao de Assembly MIPS
  errors.py      erros do compilador
exemplos/
  exemplo_basico.hc
docs/
  linguagem.md
  semantica.md
```
