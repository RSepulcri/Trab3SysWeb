from flask import Flask, render_template, request
import random
import json
import heapq

app = Flask(__name__)

template = "grid7.html"

matriz = []

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

#funcao para calcular a distancia entre os pontos
#parametros serão as variaveis globais origem e destino
#retorno será a soma de deslocamentos em pixels nos eixos x e y
def calculardistancia(origem,destino):
    return abs(origem[0] - destino[0]) + abs(origem[1] - origem[1])

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

            for x , y in caminho:
                if matriz[x][y] != "b":
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


@app.route("/", methods=["GET","POST"])
def geragridpost():
    global matriz


    if request.method == "POST":
        linhas = int(request.form["linhas"])
        colunas = int(request.form["colunas"])
        obstaculos = int(request.form["obstaculos"])
        #if (!matriz)? pq não if matriz is None
        if not matriz:
            criamatriz(linhas,colunas,obstaculos,matriz)

        #return render_template(template, matriz)
    
    return render_template(template,matriz=matriz)

@app.route('/delete', methods=['POST'])
def apagarGridAtual():
    global matriz
    #Se grid n for None(null), ou seja, se existir, voltamos ela a uma lista vazia
    #matriz is not None x not matriz ?
    if matriz is not None:
        matriz = []
    return render_template(template, matriz=matriz)
    
    

if __name__ == "__main__":
    app.run(debug=True)
