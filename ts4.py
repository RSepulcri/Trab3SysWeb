from flask import Flask, render_template, request
import random
import json

app = Flask(__name__)

template = "grid6.html"

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
