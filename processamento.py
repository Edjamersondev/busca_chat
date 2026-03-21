import json
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ARQUIVO = "dados.json"

def carregar():
    try:
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    except:
        return []

def salvar(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f)

def adicionar_documento(texto):
    dados = carregar()
    dados.append(texto)
    salvar(dados)

def buscar(query):
    dados = carregar()

    if not dados:
        return []

    vetor = TfidfVectorizer(stop_words=stopwords.words('portuguese'))
    matriz = vetor.fit_transform(dados + [query])

    similaridade = cosine_similarity(matriz[-1], matriz[:-1])

    resultados = sorted(
        zip(dados, similaridade[0]),
        key=lambda x: x[1],
        reverse=True
    )

    return resultados[:3]

def responder(pergunta):
    resultados = buscar(pergunta)

    if not resultados:
        return "Não encontrei nada relevante."

    melhor_texto, score = resultados[0]

    if score < 0.1:
        return "Não tenho certeza, mas talvez isso ajude: " + melhor_texto

    return "Encontrei isso: " + melhor_texto