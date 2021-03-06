import nltk
import heapq
nltk.download('punkt')
import string
nltk.download('stopwords')


stopwords = nltk.corpus.stopwords.words('portuguese')

def preprocessamento(texto):
  texto_formatado = texto.lower()
  tokens = []
  for token in nltk.word_tokenize(texto_formatado):
    tokens.append(token)

  tokens = [palavra for palavra in tokens if palavra not in stopwords and palavra not in string.punctuation]
  texto_formatado = ' '.join([str(elemento) for elemento in tokens if not elemento.isdigit()])

  return texto_formatado


def calcula_nota_sentenca(sentencas, palavras_importantes, distancia):
  notas = []
  indice_sentenca = 0

  for sentenca in [nltk.word_tokenize(sentenca.lower()) for sentenca in sentencas]:
    indice_palavra = []
    for palavra in palavras_importantes:
      try:
        indice_palavra.append(sentenca.index(palavra))
      except ValueError:
        pass
    
    indice_palavra.sort()

    if len(indice_palavra) == 0:
      continue

    lista_grupos = []
    grupo = [indice_palavra[0]]
    i = 1
    while i < len(indice_palavra):
      if indice_palavra[i] - indice_palavra[i - 1] < distancia:
        grupo.append(indice_palavra[i])

      else:
        lista_grupos.append(grupo[:])
        grupo = [indice_palavra[i]]

      i += 1
    lista_grupos.append(grupo)

    nota_maxima_grupo = 0
    for g in lista_grupos:

      palavras_importantes_no_grupo = len(g)
      total_palavras_no_grupo = g[-1] - g[0] + 1

      nota = 1.0 * palavras_importantes_no_grupo**2 / total_palavras_no_grupo

      if nota > nota_maxima_grupo:
        nota_maxima_grupo = nota

    notas.append((nota_maxima_grupo, indice_sentenca))
    indice_sentenca += 1

  return notas



def sumarizar(texto, top_n_palavras, distancia, quantidade_sentencas):
  sentencas_originais = [sentenca for sentenca in nltk.sent_tokenize(texto)]

  sentencas_formatadas = [preprocessamento(sentenca_original) for sentenca_original in sentencas_originais]

  palavras = [palavra for sentenca in sentencas_formatadas for palavra in nltk.word_tokenize(sentenca)]

  frequencia = nltk.FreqDist(palavras)

  top_n_palavras = [palavra[0] for palavra in frequencia.most_common(top_n_palavras)]

  notas_sentencas = calcula_nota_sentenca(sentencas_formatadas, top_n_palavras, distancia)

  melhores_sentencas = heapq.nlargest(quantidade_sentencas, notas_sentencas)

  melhores_sentencas = [sentencas_originais[i] for (nota, i) in melhores_sentencas]

  return sentencas_originais, melhores_sentencas, notas_sentencas