from fastapi import FastAPI #importei a biblioteca fastapi
from processamento import adicionar_documento, buscar #importei as funçoes que criei no arquivo processamento
from processamento import responder #importei a funçao que criei no arquivo processamento

app = FastAPI() #criei uma aplicação chamada app com a classe principal FastAPI

@app.get("/") #criei uma rota  chamada por padrão
def home():
    return {"mensagem": "API funcionando 🚀"}

@app.post("/documento") #criei uma rota chamada documento para adicionar textos
def add_doc(texto: str):
    adicionar_documento(texto)
    return {"status": "Texto adicionado"}

@app.get("/buscar") #criei uma rota para buscar textos
def busca(q: str):
    resultados = buscar(q)
    return {"resultados": resultados}

@app.get("/pergunta") #criei uma rota para perguntar sobre os textos 
def perguntar(q: str):
    resposta = responder(q)
    return {"resposta": resposta}