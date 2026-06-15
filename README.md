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

Para salvar o Assembly MIPS em um arquivo:

```bash
python main.py exemplos/exemplo_basico.hc saida.asm
```

Para rodar os testes:

```bash
python tests/run_tests.py
```

O relatorio final esta em:

```text
docs/relatorio-final.md
docs/relatorio-final.pdf
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
  strings.hc
  otimizacao.hc
tests/
  run_tests.py
docs/
  testes.md
  relatorio-final.md
  relatorio-final.pdf
```
