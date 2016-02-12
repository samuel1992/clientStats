# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, jsonify,abort
from app import app, db, Base
from app.models import Clients, StatusExtens

@app.route('/', methods=['GET'])
def home():
    clients = Clients.query.all()
    arrRanges = []
    # Fazendo uma iteracao no campo que tem os ranges de ramais
    for i in clients:
        arrRanges.append(i.extensions) # Aqui jogo cada range dentro de uma lista
    # Fazendo uma query que filtra o que esta dentro da lista
    #  a lista contem todos os ramais da central, ela eh o resultado de uma funcao que une todos
    extens = StatusExtens.query.filter(StatusExtens.exten.in_(makeArrExtens(arrRanges))) #exemplo filtrando por range de ramais
    return render_template('list_clients.html', extens=extens)

@app.route('/add_client', methods=['POST', 'GET'])
def add_client():
    """
    Funcao que recebe um post e adiciona no banco os campos, tambem retorna todos os clientes adicionados
    """
    if request.method == 'POST':
        # Caputrando as variavels via POST, usando request.form
        title = request.form['title']
        description = request.form['description']
        server = request.form['server']
        extensions = request.form['extensions']
        # Arqui passo os parametros para instanciar meu Objeto do tipo Clients
        client = Clients(title, description, server, extensions)
        params = [title, description, server, extensions]
        # validando se existe algum campo em branco
        if (validaBlank(params) == False):
            abort(403)
        else:
            db.session.add(client) # adiciona na sessao do SQLAlchemy
        try:
            db.session.commit() # Insere no banco de dados
        except: # Se meu commit tiver problemas significa que o banco nao existe
            setupBd()
            db.session.commit()
        clientParam = Clients.query.all() 
        return render_template('add_client.html', clientParam=clientParam)
    try:
        clientParam = Clients.query.all()
    except:
        setupBd()
        clientParam = Clients.query.all()
    return render_template('add_client.html', clientParam=clientParam)

@app.route('/del_client/', methods=['GET'])
def del_client():
    """
    Funcao para deletar cliente quando requisitado
    """
    # Pegando o parametro via get
    client_id = request.args.get('client_id', 0, type=int)
    # Filtrando a query pelo id recebido via get
    client = Clients.query.filter_by(id=client_id).first()
    db.session.delete(client)
    db.session.commit()
    b = [dict(id=i.id, title=i.title, description=i.description, server=i.server, extensions=i.extensions)
         for i in Clients.query.all()]
    return jsonify(ret_data=b)

@app.route('/client/<int:client_id>')
def view_client(client_id):
    """
    Funcao para visualizar os detalhes desse cliente
    """
    pass

@app.route('/echo/', methods=['GET'])
def ajaxResponse():
    """
    Funcao para retornar dados em json sob um get via ajax
    """
    b = [dict(id=i.id, title=i.title, description=i.description, server=i.server, extensions=i.extensions)
         for i in Clients.query.all()]
    return jsonify(ret_data=b)

def setupBd():
    """
    Criando as tabelas caso nao existam
    """
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)

def validaBlank(params):
    """
    Funcao para validar se ha algum campo em branco
    """
    for i in params : 
        if i != "":
            pass
        else : 
            return False

def makeRange(data):
    """
    Essa funcao recebe uma string no formato 1000-2000 e cria uma lista com o range desse intervalo
    """
    data = data.split('-')
    dataRange = range(int(data[0]), int(data[1])) # Preciso transformar em inteiro para poder usar a funcao range
    dataArr = []
    for i in dataRange:
        dataArr.append(i)
    return dataArr

def makeArrExtens(params):
    """
    Essa funcao pega todos os ranges de ramais e adiciona tudo em apenas uma lista
    funcao recebe uma lista com todos os ranges, onde cada item eh uma string no formato '1000-2000'
    """
    arr = []
    for i in params:
        for e in (makeRange(i)):
            arr.append(e)
    return arr
