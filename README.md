# Compilador Didatico

Projeto de um compilador simples feito em Python para uma linguagem parecida com C.

O compilador sera dividido nas seguintes etapas:

1. Analise lexica.
2. Analise sintatica e AST.
3. Analise semantica.
4. Geracao de codigo intermediario.
5. Geracao de Assembly MIPS.

## Como Executar

```bash
python main.py exemplos/exemplo_basico.hc
```

No momento o projeto esta apenas com a estrutura inicial. As fases do compilador serao implementadas aos poucos.

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
```
