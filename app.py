from fastapi import FastAPI
from processamento import adicionar_documento, buscar
from processamento import responder

app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "API funcionando 🚀"}

@app.post("/documento")
def add_doc(texto: str):
    adicionar_documento(texto)
    return {"status": "Documento adicionado"}

@app.get("/buscar")
def busca(q: str):
    resultados = buscar(q)
    return {"resultados": resultados}

@app.get("/pergunta")
def perguntar(q: str):
    resposta = responder(q)
    return {"resposta": resposta}