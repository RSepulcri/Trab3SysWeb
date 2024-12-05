from flask import Flask, render_template, request
import random
import json
import math

app = Flask(__name__)

template = "grid6.html"

matriz = []
matrizColunas = 0
inicio = 0
destino = 0

#@app.route("/", methods=['POST'])
#def renderpage():
#    return render_template("grid5.html")

def criaobstaculos(qtd,linha,coluna, matriz):
    while(qtd > 0):
        random_linha = random.randint(0, linha - 1)
        random_coluna = random.randint(0, coluna - 1)
        #w = white
        #r = red
        #g = green
        #b = black
        matriz[random_linha][random_coluna] = "b"
        qtd -= 1
    return matriz


def criamatriz(linha,coluna,qtd,matriz):
    matriz.clear()
    for i in range (linha):
        linha_matriz = []
        for j in range (coluna):
            linha_matriz.append("w")
        matriz.append(linha_matriz)

    criaobstaculos(qtd, linha, coluna, matriz)

    return matriz

def definePontos(posicao, coluna, tipo = 'inicio'):
    if tipo == 'inicio':
        matriz[coluna][posicao] = 'i'
    else:
        matriz[coluna][posicao] = 'd'


@app.route("/", methods=["GET","POST"])
def geragridpost():
    global matriz
    global matrizColunas


    if request.method == "POST":
        linhas = int(request.form["linhas"])
        colunas = int(request.form["colunas"])
        obstaculos = int(request.form["obstaculos"])
        #if (!matriz)? pq não if matriz is None
        if not matriz:
            matrizColunas = colunas
            criamatriz(linhas,colunas,obstaculos,matriz)

        #return render_template(template, matriz)
    print(matriz)
    print(matrizColunas)
    return render_template(template,matriz=matriz)

@app.route('/delete', methods=['POST'])
def apagarGridAtual():
    global matriz
    global inicio
    global destino
    #Se grid n for None(null), ou seja, se existir, voltamos ela a uma lista vazia
    #matriz is not None x not matriz ?
    if matriz is not None:
        matriz = []
        inicio = 0
        destino = 0

    return render_template(template, matriz=matriz)

@app.route('/enviaPos', methods=['POST'])
def atualizaPosicoes():
    global inicio
    global destino
    global matrizColunas

    #Objeto com posição vinda do frontend (ou 0)
    posicao = request.json.get('position', 0)
    #A coluna na qual a posição que veio do frontend está localizada (sim, esse operador ternário retorna o mesmo valor pra ambas possibilidadeskkkk)
    colunaPosicao = math.ceil(posicao / matrizColunas) - 1 if posicao % matrizColunas != 0 else math.ceil(posicao / matrizColunas) - 1
    print(colunaPosicao)

    #Se inicio ainda n estiver definido
    if not inicio:
        #Seta inicio (posição não tratada)
        inicio = posicao

        fimMatrizIndex = (colunaPosicao + 1) * matrizColunas #x
        inicioMatrizIndex = fimMatrizIndex - (matrizColunas - 1) #y

        #[y, ..., x], lista q vai de y(numero do inicio do grid) até x(fim do grid)
        #Isso facilita a busca da posição escolhida
        listaNova = list(range(inicioMatrizIndex, fimMatrizIndex + 1));

        #Posição do número dentro de um vetor do mesmo tamanho das colunas (posição tratada)
        posicaoDentroDaLista = listaNova.index(posicao)
        print(posicaoDentroDaLista)
        definePontos(posicaoDentroDaLista, colunaPosicao)
    #Se inicio já estievr definido, definimos então o destino
    else:
        #Seta destino (posição não tratada)
        destino = posicao

        fimMatrizIndex = (colunaPosicao + 1) * matrizColunas #x
        inicioMatrizIndex = fimMatrizIndex - (matrizColunas - 1) #y

        #[y, ..., x], lista q vai de y(numero do inicio do grid) até x(fim do grid)
        listaNova = list(range(inicioMatrizIndex, fimMatrizIndex + 1));
        
        #Posição do número dentro de um vetor do mesmo tamanho das colunas (posição tratada)
        posicaoDentroDaLista = listaNova.index(posicao)
        print(posicaoDentroDaLista)
        definePontos(posicaoDentroDaLista, colunaPosicao, 'destino')
    
    #Envia dados pro front end (apenas p debug)
    return json.dumps({'currentInicio': inicio, 'currentDestino': destino, 'matrizAtual': matriz})
    #return render_template(template,matriz=matriz)
    

if __name__ == "__main__":
    app.run(debug=True, port=8000)
