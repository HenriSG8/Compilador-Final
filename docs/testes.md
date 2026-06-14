# Testes

O projeto possui exemplos validos e invalidos para conferir as etapas principais do compilador.

## Exemplos validos

```text
exemplos/exemplo_basico.hc
exemplos/strings.hc
exemplos/otimizacao.hc
```

Esses arquivos devem passar pelas analises, gerar codigo intermediario e gerar Assembly MIPS.

## Exemplos invalidos

```text
exemplos/erros/variavel_nao_declarada.hc
exemplos/erros/tipo_incorreto.hc
exemplos/erros/sintaxe_sem_ponto_virgula.hc
```

Esses arquivos servem para verificar se o compilador rejeita programas incorretos.

## Como executar

```bash
python tests/run_tests.py
```

O script usa `assert` simples do Python e nao depende de bibliotecas externas.
