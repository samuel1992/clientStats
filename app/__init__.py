# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
# BAse para criar os models
Base = declarative_base()

# Criando a aplicacao
app = Flask('app', static_folder='static', static_url_path="/statics_v1")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:my19901992@localhost/clientsConsult'
app.secret_key = '1q2w3e'
db = SQLAlchemy(app)

# Importando os arquivos necessários da aplicacao
from app import views, models
