# assign1-RI

Information Retrieval

## Para executar o programa

```bash
$ python3 SPIMI.py [dataset] [flags]
```

Nenhuma das flags é obrigatória. O único parâmetro que é sempre necessário é o dataset para ser indexado.

Flags disponíveis:

  -s	-> Permite passar um ficheiro contendo uma lista com stopwords. Este ficheiro deve ter apenas uma palavra por linha. Caso não se passe nenhuma lista, será utilizada uma lista por default.

  -m	-> Permite definir o tamanho mínimo das palavras. O valor default são 3 caracteres.

As estatísticas pedidas estão anexadas no ficheiro Indexing_Statistics.csv 