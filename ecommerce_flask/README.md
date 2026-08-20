# Marketplace — Sistema de E-commerce (Flask)

Projeto acadêmico desenvolvido em duas trilhas:

- **Trilha 1** — estrutura inicial em Flask: MER, menu de navegação e rotas básicas
  (dados mantidos em memória).
- **Trilha 2** (esta versão) — persistência real em banco de dados (SQLite via
  SQLAlchemy) e **CRUD completo** (criar, ler, atualizar, excluir com confirmação)
  para todas as entidades do MER.

## Requisitos atendidos

- Usuários que anunciam e compram produtos
- Anúncios organizados em categorias
- Perguntas em anúncios, respondidas pelo dono do anúncio
- Compra direta de um anúncio (sem carrinho)
- Listas de anúncios favoritos
- Relatório de vendas e relatório de compras do usuário
- **CRUD completo (Create, Read, Update, Delete) para todas as entidades do MER,
  com persistência em banco de dados e exclusão com tela de confirmação**

## Estrutura do projeto

```
ecommerce_flask/
├── run.py                  # ponto de entrada da aplicação
├── requirements.txt
└── app/
    ├── __init__.py         # application factory + SQLAlchemy + registro dos blueprints
    ├── models.py            # modelos SQLAlchemy (7 entidades do MER)
    ├── seed.py               # dados iniciais de demonstração (roda 1x, se o banco estiver vazio)
    ├── constants.py           # CURRENT_USER_ID (usuário logado simulado)
    ├── data.py                 # [obsoleto] dados em memória usados na Trilha 1
    ├── routes/                  # um blueprint por entidade do MER, com CRUD completo
    │   ├── main.py
    │   ├── usuarios.py            # C/R/U/D de Usuario
    │   ├── categorias.py          # C/R/U/D de Categoria
    │   ├── anuncios.py            # C/R/U/D de Anuncio
    │   ├── perguntas.py           # C/R/U/D de Pergunta
    │   ├── compras.py             # C/R/U/D de Compra
    │   ├── favoritos.py           # C/R/U/D de ListaFavoritos e ItemFavorito
    │   └── relatorios.py          # consultas (somente leitura)
    ├── templates/                 # HTML (Jinja2): listas, formulários e confirm_delete.html
    └── static/css/style.css

instance/
└── ecommerce.db             # banco SQLite (criado automaticamente, não vai para o Git)
```

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Acesse http://127.0.0.1:5000

Na primeira execução, o Flask cria o arquivo `instance/ecommerce.db` (SQLite) e popula
automaticamente algumas linhas de exemplo (`app/seed.py`), para facilitar os testes.
Para começar do zero, basta apagar o arquivo `instance/ecommerce.db` e rodar novamente.

## CRUD implementado por entidade

| Entidade | Create | Read | Update | Delete (com confirmação) |
|---|---|---|---|---|
| Usuario | `/usuarios/cadastro` | `/usuarios/`, `/usuarios/<id>` | `/usuarios/<id>/editar` | `/usuarios/<id>/excluir` |
| Categoria | `/categorias/nova` | `/categorias/`, `/categorias/<id>` | `/categorias/<id>/editar` | `/categorias/<id>/excluir` |
| Anuncio | `/anuncios/novo` | `/anuncios/`, `/anuncios/<id>`, `/anuncios/meus` | `/anuncios/<id>/editar` | `/anuncios/<id>/excluir` |
| Pergunta | `/perguntas/novo` | `/perguntas/`, `/perguntas/recebidas` | `/perguntas/<id>/editar` | `/perguntas/<id>/excluir` |
| Compra | `/compras/novo` | `/compras/`, `/compras/<id>` | `/compras/<id>/editar` | `/compras/<id>/excluir` |
| ListaFavoritos | `/favoritos/nova` | `/favoritos/`, `/favoritos/<id>` | `/favoritos/<id>/editar` | `/favoritos/<id>/excluir` |
| ItemFavorito | `/favoritos/<id>/adicionar` | (dentro de `/favoritos/<id>`) | — | `/favoritos/item/<id>/excluir` |

Todas as rotas de exclusão exibem uma tela de confirmação (`confirm_delete.html`) antes
de remover o registro do banco de dados.

## Observações

- Ainda não há sistema de autenticação real: um usuário fixo (`CURRENT_USER_ID`, em
  `app/constants.py`) simula o usuário logado. As telas de Login e Cadastro já existem
  e serão conectadas à autenticação real (ex.: Flask-Login + hash de senha) em uma
  próxima etapa.
- Exclusões em cascata: excluir um Usuario remove seus anúncios, perguntas, compras e
  listas de favoritos; excluir um Anuncio remove suas perguntas, compras e favoritos
  associados; excluir uma ListaFavoritos remove seus itens. Isso é feito via
  `cascade="all, delete-orphan"` nos relacionamentos do SQLAlchemy (`app/models.py`),
  refletindo as cardinalidades definidas no MER da Trilha 1.
