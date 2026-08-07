"""
Dados "mockados" em memoria, representando as tabelas do MER.

Nesta primeira entrega o objetivo e demonstrar a estrutura de rotas e o
menu de navegacao do Flask. Por isso os dados vivem em listas de
dicionarios em memoria (perdidos a cada reinicio do servidor) em vez de
um banco de dados real. Numa proxima etapa estas listas serao
substituidas por modelos SQLAlchemy mapeados para as mesmas entidades
do MER (Usuario, Categoria, Anuncio, Pergunta, Compra, ListaFavoritos,
ItemFavorito).
"""

from datetime import date

# Simula o usuario autenticado no momento (sem sistema de login real ainda)
CURRENT_USER_ID = 1

USUARIOS = [
    {"id": 1, "nome": "Vitor Leite", "email": "vitor@email.com",
     "senha": "123456", "data_cadastro": date(2026, 1, 10)},
    {"id": 2, "nome": "Ana Souza", "email": "ana@email.com",
     "senha": "123456", "data_cadastro": date(2026, 2, 5)},
    {"id": 3, "nome": "Carlos Lima", "email": "carlos@email.com",
     "senha": "123456", "data_cadastro": date(2026, 3, 1)},
]

CATEGORIAS = [
    {"id": 1, "nome": "Eletrônicos", "descricao": "Celulares, computadores e acessórios"},
    {"id": 2, "nome": "Móveis", "descricao": "Móveis para casa e escritório"},
    {"id": 3, "nome": "Livros", "descricao": "Livros novos e usados"},
]

ANUNCIOS = [
    {"id": 1, "titulo": "Notebook Dell i5", "descricao": "8GB RAM, 256GB SSD, seminovo",
     "preco": 2500.00, "data_publicacao": date(2026, 6, 1), "status": "disponivel",
     "id_usuario": 1, "id_categoria": 1},
    {"id": 2, "titulo": "Mesa de escritório", "descricao": "Mesa em MDF, 120x60cm",
     "preco": 350.00, "data_publicacao": date(2026, 6, 10), "status": "disponivel",
     "id_usuario": 2, "id_categoria": 2},
    {"id": 3, "titulo": "Coleção Senhor dos Anéis", "descricao": "3 livros, capa dura",
     "preco": 150.00, "data_publicacao": date(2026, 7, 2), "status": "vendido",
     "id_usuario": 1, "id_categoria": 3},
    {"id": 4, "titulo": "Smartphone Galaxy", "descricao": "128GB, usado, funcionando perfeitamente",
     "preco": 900.00, "data_publicacao": date(2026, 7, 20), "status": "disponivel",
     "id_usuario": 3, "id_categoria": 1},
]

PERGUNTAS = [
    {"id": 1, "texto_pergunta": "O notebook aceita upgrade de memória?",
     "data_pergunta": date(2026, 6, 2), "texto_resposta": "Sim, aceita até 16GB.",
     "data_resposta": date(2026, 6, 3), "id_anuncio": 1, "id_usuario": 2},
    {"id": 2, "texto_pergunta": "Tem nota fiscal?", "data_pergunta": date(2026, 6, 3),
     "texto_resposta": None, "data_resposta": None, "id_anuncio": 1, "id_usuario": 3},
]

COMPRAS = [
    {"id": 1, "data_compra": date(2026, 7, 5), "valor_pago": 150.00,
     "id_anuncio": 3, "id_comprador": 2},
]

LISTAS_FAVORITOS = [
    {"id": 1, "nome_lista": "Quero comprar", "id_usuario": 2},
    {"id": 2, "nome_lista": "Favoritos", "id_usuario": 1},
]

ITENS_FAVORITOS = [
    {"id": 1, "id_lista": 1, "id_anuncio": 1, "data_adicao": date(2026, 6, 5)},
    {"id": 2, "id_lista": 2, "id_anuncio": 4, "data_adicao": date(2026, 7, 21)},
]
