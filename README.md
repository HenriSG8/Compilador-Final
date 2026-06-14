# Compilador Didatico

Projeto de um compilador simples feito em Python para uma linguagem parecida com C.

O compilador sera dividido nas seguintes etapas:

1. Analise lexica. Feita.
2. Analise sintatica e AST. Feita.
3. Analise semantica. Feita.
4. Geracao de codigo intermediario. Feita.
5. Geracao de Assembly MIPS. Feita.
6. Otimizacao simples. Feita.

## Como Executar

```bash
python main.py exemplos/exemplo_basico.hc
```

No momento o projeto executa as analises lexica, sintatica e semantica, aplica otimizacoes simples, gera codigo intermediario e traduz para Assembly MIPS.

## Estrutura

```text
compiler/
  lexer.py       analise lexica
  parser.py      analise sintatica
  ast_nodes.py   nos da AST
  semantic.py    analise semantica
  optimizer.py   otimizacao simples da AST
  ir.py          codigo intermediario
  mips.py        geracao de Assembly MIPS
  errors.py      erros do compilador
exemplos/
  exemplo_basico.hc
docs/
  linguagem.md
  semantica.md
  codigo-intermediario.md
  mips.md
  otimizacao.md
```
