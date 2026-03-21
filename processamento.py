import json
import nltk
import re
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
        return "Não encontrei nada sobre isso ainda."

    textos_relevantes = [texto for texto, score in resultados if score > 0.1]

    if not textos_relevantes:
        return "Não tenho informações suficientes sobre isso."

    if len(textos_relevantes) == 1:
        resposta = textos_relevantes[0]
    elif len(textos_relevantes) == 2:
        resposta = f"{textos_relevantes[0]} e {textos_relevantes[1]}"
    else:
        resposta = ", ".join(textos_relevantes[:-1])
        resposta += f" e {textos_relevantes[-1]}"
    #resposta = " e ".join(textos_relevantes)
    resposta = remover_repeticao(resposta)
    resposta = resumir_texto(resposta)
    tipo = tipo_pergunta(pergunta)

    if tipo == "definicao":
        return f"Pelo que encontrei, isso é o seguinte: {resposta}"
    elif tipo == "tempo":
        return f"Isso aconteceu em algum momento relacionado a: {resposta}"
    elif tipo == "local":
        return f"Isso ocorreu em um local como: {resposta}"
    elif tipo == "pessoa":
        return f"Está relacionado a alguém como: {resposta}"
    else:
        return f"Com base na minha base de dados,você mencionou que: {resposta}"


def tipo_pergunta(pergunta):
    pergunta = pergunta.lower()

    if "o que" in pergunta:
        return "definicao"
    elif "quando" in pergunta:
        return "tempo"
    elif "onde" in pergunta:
        return "local"
    elif "quem" in pergunta:
        return "pessoa"
    else:
        return "geral"


def limpar_texto(texto):
    
    texto = texto.lower()  # tudo minúsculo
    texto = re.sub(r'[^\w\s]', '', texto)  # remove pontuação
    return texto


def remover_repeticao(texto):
    palavras = texto.split()
    unicas = []

    for p in palavras:
        if p not in unicas:
            unicas.append(p)

    return " ".join(unicas)


def resumir_texto(texto, max_palavras=20):
    palavras = texto.split()
    return " ".join(palavras[:max_palavras])