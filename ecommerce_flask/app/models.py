"""
Modelos SQLAlchemy — mapeiam exatamente as entidades definidas no MER da Trilha 1
(Usuario, Categoria, Anuncio, Pergunta, Compra, ListaFavoritos, ItemFavorito) para
tabelas reais em um banco de dados SQLite, substituindo os dados em memória usados
na primeira entrega.
"""

from datetime import date

from app import db


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    data_cadastro = db.Column(db.Date, default=date.today)

    anuncios = db.relationship("Anuncio", backref="usuario", cascade="all, delete-orphan")
    perguntas = db.relationship("Pergunta", backref="usuario", cascade="all, delete-orphan")
    compras = db.relationship("Compra", backref="comprador", cascade="all, delete-orphan")
    listas = db.relationship("ListaFavoritos", backref="usuario", cascade="all, delete-orphan")


class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(255))

    anuncios = db.relationship("Anuncio", backref="categoria")


class Anuncio(db.Model):
    __tablename__ = "anuncio"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    data_publicacao = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(20), default="disponivel", nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)

    perguntas = db.relationship("Pergunta", backref="anuncio", cascade="all, delete-orphan")
    compras = db.relationship("Compra", backref="anuncio", cascade="all, delete-orphan")
    itens_favoritos = db.relationship("ItemFavorito", backref="anuncio", cascade="all, delete-orphan")


class Pergunta(db.Model):
    __tablename__ = "pergunta"

    id = db.Column(db.Integer, primary_key=True)
    texto_pergunta = db.Column(db.Text, nullable=False)
    data_pergunta = db.Column(db.Date, default=date.today)
    texto_resposta = db.Column(db.Text)
    data_resposta = db.Column(db.Date)
    id_anuncio = db.Column(db.Integer, db.ForeignKey("anuncio.id"), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)


class Compra(db.Model):
    __tablename__ = "compra"

    id = db.Column(db.Integer, primary_key=True)
    data_compra = db.Column(db.Date, default=date.today)
    valor_pago = db.Column(db.Float, nullable=False)
    id_anuncio = db.Column(db.Integer, db.ForeignKey("anuncio.id"), nullable=False)
    id_comprador = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)


class ListaFavoritos(db.Model):
    __tablename__ = "lista_favoritos"

    id = db.Column(db.Integer, primary_key=True)
    nome_lista = db.Column(db.String(120), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    itens = db.relationship("ItemFavorito", backref="lista", cascade="all, delete-orphan")


class ItemFavorito(db.Model):
    __tablename__ = "item_favorito"

    id = db.Column(db.Integer, primary_key=True)
    id_lista = db.Column(db.Integer, db.ForeignKey("lista_favoritos.id"), nullable=False)
    id_anuncio = db.Column(db.Integer, db.ForeignKey("anuncio.id"), nullable=False)
    data_adicao = db.Column(db.Date, default=date.today)
