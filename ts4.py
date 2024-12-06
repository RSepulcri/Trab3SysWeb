from flask import Flask, render_template, request
import random
import json
import math
import heapq

app = Flask(__name__)

template = "grid6.html"

matriz = []
matrizColunas = 0
inicioTupla = ()
destinotupla = ()

#funcao para calcular a distancia entre os pontos
#parametros serão as variaveis globais origem e destino
#retorno será a soma de deslocamentos em pixels nos eixos x e y
def calculardistancia(origem,destino):
    return abs(origem[0] - destino[0]) + abs(origem[1] - destino[1])

def a_star(matriz,origem,destino):
    linhas, colunas = len(matriz), len(matriz[0])

    #criando lista de prioridades
    open_list = []
    heapq.heappush(open_list,(0,origem))

    #mapeando quantidade de pixels deslocados
    #passos_inicio guarda custo real da origem até uma posicao especifica
    #passos_final armazena o custo total estimado para chegar no objetivo
    #   será a soma, do deslocamento da origem até destino, em x e y
    passos_inicio = {origem:0}
    passos_final = {origem: calculardistancia(origem,destino)}

    #dicionario para armazenar as coordenadas ja visitadas
    #servirá para reconstruir o caminho mais curto no final
    rotas_realizadas = {}

    #estrutura para rodar e explorar enquanto existir posicoes na open_list
    while open_list:
        _, atual = heapq.heappop(open_list)

        #se chegamos ao destino, reconstruir o caminho:
        #se a posicao atual é o objetivo, entao o caminho foi encontrado
        if atual == destino:
            caminho = []
            while atual in rotas_realizadas:
                caminho.append(atual)
                atual = rotas_realizadas[atual]
            caminho.append(origem)

            for x , y in caminho[1:]:
                if matriz[x][y] != "b" and matriz[x][y] != "i":
                    matriz[x][y] = "c"
                    
            return caminho[::-1] #retorna o caminho na ordem correta(invertida)
        
        #verificar os vizinhos
        vizinhos = [(0,1),(1,0),(0,-1),(-1,0)] #as possibilidades a partir de um ponto
        #dx = deslocamento em x, dy = deslocamento em y
        for dx, dy in vizinhos:
            x , y = atual[0] + dx , atual[1] + dy
            vizinho = (x , y)

            #verificacao se o vizinho esta dentro dos limites e se nao é um obstaculo
            if 0 <= x < linhas and 0 <= y < colunas and matriz[x][y] != "b":
                custo_tentativa = passos_inicio[atual] + 1

                #por algum motivo matemático pica, abaixo, devemos trabalhar com float invés de int
                #por favor nao pergunte :D
                if custo_tentativa < passos_inicio.get(vizinho , float("inf")):
                    #atualiza o mapa de custos:
                    rotas_realizadas[vizinho] = atual
                    passos_inicio[vizinho] = custo_tentativa
                    passos_final[vizinho] = custo_tentativa + calculardistancia(vizinho,destino)

                    #adiciona o vizinho a lista aberta
                    if vizinho not in [n[1] for n in open_list]:
                        heapq.heappush(open_list,(passos_final[vizinho], vizinho))
    
    return None #retorna none se nao existir caminho possivel

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
    global inicioTupla
    global destinotupla
    #Se grid n for None(null), ou seja, se existir, voltamos ela a uma lista vazia
    #matriz is not None x not matriz ?
    if matriz is not None:
        matriz = []
        inicioTupla = ()
        destinotupla = ()

    return render_template(template, matriz=matriz)

@app.route('/enviaPos', methods=['POST'])
def atualizaPosicoes():
    global matrizColunas
    global matriz
    global inicioTupla
    global destinotupla

    #Objeto com posição vinda do frontend (ou 0)
    posicao = request.json.get('position', 0)
    #A coluna na qual a posição que veio do frontend está localizada (sim, esse operador ternário retorna o mesmo valor pra ambas possibilidadeskkkk)
    colunaPosicao = math.ceil(posicao / matrizColunas) - 1 if posicao % matrizColunas != 0 else math.ceil(posicao / matrizColunas) - 1
    print(colunaPosicao)

    #Se inicio ainda n estiver definido
    if not inicioTupla:
        fimMatrizIndex = (colunaPosicao + 1) * matrizColunas #x
        inicioMatrizIndex = fimMatrizIndex - (matrizColunas - 1) #y

        #[y, ..., x], lista q vai de y(numero do inicio do grid) até x(fim do grid)
        #Isso facilita a busca da posição escolhida
        listaNova = list(range(inicioMatrizIndex, fimMatrizIndex + 1));

        #Posição do número dentro de um vetor do mesmo tamanho das colunas (posição tratada)
        posicaoDentroDaLista = listaNova.index(posicao)

        #Setando tupla com os valores
        inicioTupla  = (colunaPosicao, posicaoDentroDaLista)
        print(inicioTupla)

        print(posicaoDentroDaLista)
        definePontos(posicaoDentroDaLista, colunaPosicao)
    #Se inicio já estievr definido, definimos então o destino
    else:
        fimMatrizIndex = (colunaPosicao + 1) * matrizColunas #x
        inicioMatrizIndex = fimMatrizIndex - (matrizColunas - 1) #y

        #[y, ..., x], lista q vai de y(numero do inicio do grid) até x(fim do grid)
        listaNova = list(range(inicioMatrizIndex, fimMatrizIndex + 1));
        
        #Posição do número dentro de um vetor do mesmo tamanho das colunas (posição tratada)
        posicaoDentroDaLista = listaNova.index(posicao)

        #Tupla de destino
        destinotupla = (colunaPosicao, posicaoDentroDaLista)
        print(destinotupla)

        a_star(matriz=matriz, origem=inicioTupla, destino= destinotupla)
        print(matriz)

        print(posicaoDentroDaLista)
        definePontos(posicaoDentroDaLista, colunaPosicao, 'destino')
    
    #Envia dados pro front end (apenas p debug)
    return json.dumps({'currentInicio': inicioTupla, 'currentDestino': destinotupla, 'matrizAtual': matriz})
    #return render_template(template,matriz=matriz)
    

if __name__ == "__main__":
    app.run(debug=True, port=8000)
