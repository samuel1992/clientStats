# -*- coding: utf-8 -*-
from app import db, Base

class Clients(Base, db.Model):
    """
    Classe do model dos clientes onde colocaremos o nome, descricao e range de ramais
    """
    __tablename__ =  'clients'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.String(200))
    server = db.Column(db.String(30))
    extensions = db.Column(db.String(10))

    def __init__(self, title, description, server, extensions):
        self.title = title
        self.description = description
        self.server = server
        self.extensions = extensions

    def __repr__(self):
        return '<Title %r>' % self.title

class StatusExtens(Base, db.Model):
    """
    Classe para consulmir a tabela que contem os status dos ramais
    """
    __tablename__ = 'statusExtens'

    id = db.Column(db.Integer, primary_key=True)
    exten = db.Column(db.String(20))
    status = db.Column(db.String(50))

    def __init__(self, exten, status):
        self.exten = exten
        self. status = status

    def __repr__(self):
        return '<Exten %s>' % self.exten


