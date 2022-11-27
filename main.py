from flask import Flask, jsonify
from unidecode import unidecode as uni #retirar acentuação
import csv

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


#Padrão
@app.route('/')
def ajuda_api():
    return '''<h3>Como utilizar: pesquisar 
    por dia_mes_ano (12_12_2021) retornado todos os casos do municipio.
    Cosultar por ID ou Municipio acresentar /covid/ID ou Municipio<BR>
    Exemplos:<br>
    ID:<br>
    12_12_2021/covid/1<br>
    12_12_2021/covid/campo largo
    </h3>'''

# ler arquivo e adicionar na lista [[item]]
lista = []


@app.route('/<int:dia>_<int:mes>_<int:ano>')
def obter_dados_csv(dia: int, mes: int, ano: int):
    with open(f'2021/{dia:02d}_{mes}_{ano}.csv', 'r') as arquivo:
        arquivo_lido = csv.reader(arquivo, delimiter=';')
        for casos in arquivo_lido:
            lista.append(casos)

        return retorno_casos()


# deixar os casos somente em uma lista e acrescentar o ID. lista [[]] > [id=1]
def retorno_casos():
    casos = []
    for linha, casos_lido in enumerate(lista):
        if linha != 0:
            casos.append({
                'id': linha,
                'IBGE': casos_lido[0],
                'RS': casos_lido[1],
                'MACRO': casos_lido[2],
                'Municipio': uni(casos_lido[3].lower()),
                'Casos': casos_lido[4],
                'Obitos': casos_lido[5],
                'Recuperado': casos_lido[6],
                'Em_investigacao': casos_lido[7]
            })
        else:
            pass
    return casos


@app.route('/<int:dia>_<int:mes>_<int:ano>/covid/<int:id>', methods=['GET'])
def obter_casos_id(dia: int, mes: int, ano: int, id: int):
    # Lista com dicionarios, retornar o dicionario depois o ID
    lista.clear()
    obter_dados = obter_dados_csv(dia, mes, ano)
    if id > 0 and id <= len(obter_dados):
        for contador in range(len(obter_dados)):
            if obter_dados[contador]['id'] == id:
                return jsonify(obter_dados[contador])
    else:
        return f'<h3>ID não localizado. ID min 1 ID Max {len(obter_dados)}</h3>'


@app.route('/<int:dia>_<int:mes>_<int:ano>/covid/<string:municipio>')
def obter_casos_municipio(dia: int, mes: int, ano: int, municipio: str, methods=['GET']):
    validar = False
    lista.clear()
    obter_dados = obter_dados_csv(dia, mes, ano)
    for contador in range(len(obter_dados)):
        if obter_dados[contador]['Municipio'] == municipio:
            return jsonify(obter_dados[contador])
        else:
            validar = True  # verdadeiro caso não exista o municipio

    if validar:
        return f'<h3>Municipio não localizado "{municipio}"</h3>'


app.run(port=5000, host='localhost', debug=True)
