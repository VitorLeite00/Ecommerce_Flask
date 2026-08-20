import os
import sqlite3

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "marketplace.db")


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    data_cadastro TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS anuncios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    preco REAL NOT NULL,
    data_publicacao TEXT NOT NULL DEFAULT (date('now')),
    status TEXT NOT NULL DEFAULT 'disponivel',
    id_usuario INTEGER NOT NULL,
    id_categoria INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS perguntas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    texto_pergunta TEXT NOT NULL,
    data_pergunta TEXT NOT NULL DEFAULT (date('now')),
    texto_resposta TEXT,
    data_resposta TEXT,
    id_anuncio INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_anuncio) REFERENCES anuncios(id) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_compra TEXT NOT NULL DEFAULT (date('now')),
    valor_pago REAL NOT NULL,
    id_anuncio INTEGER NOT NULL,
    id_comprador INTEGER NOT NULL,
    FOREIGN KEY (id_anuncio) REFERENCES anuncios(id) ON DELETE CASCADE,
    FOREIGN KEY (id_comprador) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS listas_favoritos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_lista TEXT NOT NULL,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS itens_favoritos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_lista INTEGER NOT NULL,
    id_anuncio INTEGER NOT NULL,
    data_adicao TEXT NOT NULL DEFAULT (date('now')),
    FOREIGN KEY (id_lista) REFERENCES listas_favoritos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_anuncio) REFERENCES anuncios(id) ON DELETE CASCADE
);
"""


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db_connection()
    try:
        conn.executescript(SCHEMA)
        seed_database(conn)
        conn.commit()
    finally:
        conn.close()


def seed_database(conn):
    usuario_count = conn.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
    if usuario_count > 0:
        return

    usuarios = [
        (1, "Vitor Leite", "vitor@email.com", "123456", "2026-01-10"),
        (2, "Ana Souza", "ana@email.com", "123456", "2026-02-05"),
        (3, "Carlos Lima", "carlos@email.com", "123456", "2026-03-01"),
    ]
    conn.executemany(
        "INSERT INTO usuarios (id, nome, email, senha, data_cadastro) VALUES (?, ?, ?, ?, ?)",
        usuarios,
    )

    categorias = [
        (1, "Eletrônicos", "Celulares, computadores e acessórios"),
        (2, "Móveis", "Móveis para casa e escritório"),
        (3, "Livros", "Livros novos e usados"),
    ]
    conn.executemany(
        "INSERT INTO categorias (id, nome, descricao) VALUES (?, ?, ?)",
        categorias,
    )

    anuncios = [
        (1, "Notebook Dell i5", "8GB RAM, 256GB SSD, seminovo", 2500.00, "2026-06-01", "disponivel", 1, 1),
        (2, "Mesa de escritório", "Mesa em MDF, 120x60cm", 350.00, "2026-06-10", "disponivel", 2, 2),
        (3, "Coleção Senhor dos Anéis", "3 livros, capa dura", 150.00, "2026-07-02", "vendido", 1, 3),
        (4, "Smartphone Galaxy", "128GB, usado, funcionando perfeitamente", 900.00, "2026-07-20", "disponivel", 3, 1),
    ]
    conn.executemany(
        "INSERT INTO anuncios (id, titulo, descricao, preco, data_publicacao, status, id_usuario, id_categoria) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        anuncios,
    )

    perguntas = [
        (1, "O notebook aceita upgrade de memória?", "2026-06-02", "Sim, aceita até 16GB.", "2026-06-03", 1, 2),
        (2, "Tem nota fiscal?", "2026-06-03", None, None, 1, 3),
    ]
    conn.executemany(
        "INSERT INTO perguntas (id, texto_pergunta, data_pergunta, texto_resposta, data_resposta, id_anuncio, id_usuario) VALUES (?, ?, ?, ?, ?, ?, ?)",
        perguntas,
    )

    compras = [
        (1, "2026-07-05", 150.00, 3, 2),
    ]
    conn.executemany(
        "INSERT INTO compras (id, data_compra, valor_pago, id_anuncio, id_comprador) VALUES (?, ?, ?, ?, ?)",
        compras,
    )

    listas = [
        (1, "Quero comprar", 2),
        (2, "Favoritos", 1),
    ]
    conn.executemany(
        "INSERT INTO listas_favoritos (id, nome_lista, id_usuario) VALUES (?, ?, ?)",
        listas,
    )

    itens = [
        (1, 1, 1, "2026-06-05"),
        (2, 2, 4, "2026-07-21"),
    ]
    conn.executemany(
        "INSERT INTO itens_favoritos (id, id_lista, id_anuncio, data_adicao) VALUES (?, ?, ?, ?)",
        itens,
    )
