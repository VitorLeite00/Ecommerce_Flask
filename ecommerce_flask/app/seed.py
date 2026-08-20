"""Popula o banco de dados com dados de demonstração na primeira execução,
apenas se as tabelas ainda estiverem vazias (idempotente)."""

from datetime import date

from app import db
from app.models import (
    Anuncio,
    Categoria,
    Compra,
    ItemFavorito,
    ListaFavoritos,
    Pergunta,
    Usuario,
)


def seed_data():
    if Usuario.query.first():
        return  # banco ja populado, nao faz nada

    u1 = Usuario(nome="Vitor Leite", email="vitor@email.com", senha="123456", data_cadastro=date(2026, 1, 10))
    u2 = Usuario(nome="Ana Souza", email="ana@email.com", senha="123456", data_cadastro=date(2026, 2, 5))
    u3 = Usuario(nome="Carlos Lima", email="carlos@email.com", senha="123456", data_cadastro=date(2026, 3, 1))
    db.session.add_all([u1, u2, u3])
    db.session.flush()  # garante que u1.id, u2.id, u3.id ja existam

    c1 = Categoria(nome="Eletrônicos", descricao="Celulares, computadores e acessórios")
    c2 = Categoria(nome="Móveis", descricao="Móveis para casa e escritório")
    c3 = Categoria(nome="Livros", descricao="Livros novos e usados")
    db.session.add_all([c1, c2, c3])
    db.session.flush()

    a1 = Anuncio(titulo="Notebook Dell i5", descricao="8GB RAM, 256GB SSD, seminovo", preco=2500.00,
                 data_publicacao=date(2026, 6, 1), status="disponivel", id_usuario=u1.id, id_categoria=c1.id)
    a2 = Anuncio(titulo="Mesa de escritório", descricao="Mesa em MDF, 120x60cm", preco=350.00,
                 data_publicacao=date(2026, 6, 10), status="disponivel", id_usuario=u2.id, id_categoria=c2.id)
    a3 = Anuncio(titulo="Coleção Senhor dos Anéis", descricao="3 livros, capa dura", preco=150.00,
                 data_publicacao=date(2026, 7, 2), status="vendido", id_usuario=u1.id, id_categoria=c3.id)
    a4 = Anuncio(titulo="Smartphone Galaxy", descricao="128GB, usado, funcionando perfeitamente", preco=900.00,
                 data_publicacao=date(2026, 7, 20), status="disponivel", id_usuario=u3.id, id_categoria=c1.id)
    db.session.add_all([a1, a2, a3, a4])
    db.session.flush()

    p1 = Pergunta(texto_pergunta="O notebook aceita upgrade de memória?", data_pergunta=date(2026, 6, 2),
                  texto_resposta="Sim, aceita até 16GB.", data_resposta=date(2026, 6, 3),
                  id_anuncio=a1.id, id_usuario=u2.id)
    p2 = Pergunta(texto_pergunta="Tem nota fiscal?", data_pergunta=date(2026, 6, 3),
                  id_anuncio=a1.id, id_usuario=u3.id)
    db.session.add_all([p1, p2])

    compra1 = Compra(data_compra=date(2026, 7, 5), valor_pago=150.00, id_anuncio=a3.id, id_comprador=u2.id)
    db.session.add(compra1)

    lista1 = ListaFavoritos(nome_lista="Quero comprar", id_usuario=u2.id)
    lista2 = ListaFavoritos(nome_lista="Favoritos", id_usuario=u1.id)
    db.session.add_all([lista1, lista2])
    db.session.flush()

    item1 = ItemFavorito(id_lista=lista1.id, id_anuncio=a1.id, data_adicao=date(2026, 6, 5))
    item2 = ItemFavorito(id_lista=lista2.id, id_anuncio=a4.id, data_adicao=date(2026, 7, 21))
    db.session.add_all([item1, item2])

    db.session.commit()
