# Marketplace — Sistema de E-commerce (Flask)

Projeto acadêmico desenvolvido em três trilhas:

- Trilha 1 — estrutura inicial em Flask: MER, menu de navegação e rotas básicas
  (dados mantidos em memória).
- Trilha 2 — persistência real em banco de dados (SQLite via SQLAlchemy) e
  CRUD completo (criar, ler, atualizar, excluir com confirmação) para todas as
  entidades do MER.
- Trilha 3 — autenticação e sessão (login/logout/cadastro reais,
  com senha em hash e rotas protegidas), interface reformulada com Bootstrap 5 e
  implantação no PythonAnywhere usando SQLite.

## Requisitos atendidos

- Usuários que anunciam e compram produtos
- Anúncios organizados em categorias
- Perguntas em anúncios, respondidas pelo dono do anúncio
- Compra direta de um anúncio (sem carrinho)
- Listas de anúncios favoritos
- Relatório de vendas e relatório de compras do usuário
- CRUD completo (Create, Read, Update, Delete) para todas as entidades do MER
- Login/logout com sessão real e rotas protegidas (ver seção abaixo)
- Interface responsiva com Bootstrap 5 (navbar, tabelas, formulários, cards, alerts)
- Implantado no PythonAnywhere com SQLite

## Estrutura do projeto

```
ecommerce_flask/
├── run.py                  # ponto de entrada da aplicação
├── requirements.txt
└── app/
    ├── __init__.py         # application factory + SQLAlchemy + blueprints + current_user
    ├── auth.py              # login_required, get_current_user (sessão Flask)
    ├── models.py            # modelos SQLAlchemy (7 entidades do MER, senha em hash)
    ├── seed.py               # dados iniciais de demonstração (roda 1x, se o banco estiver vazio)
    ├── constants.py           # [obsoleto] usado até a Trilha 2
    ├── data.py                 # [obsoleto] dados em memória usados na Trilha 1
    ├── routes/                  # um blueprint por entidade do MER, com CRUD + login_required
    │   ├── main.py                 # pública
    │   ├── usuarios.py             # login, logout, cadastro (públicas) + CRUD (protegido)
    │   ├── categorias.py           # listagem pública + CRUD (protegido)
    │   ├── anuncios.py             # vitrine pública + CRUD/compra/detalhe (protegido)
    │   ├── perguntas.py            # protegido
    │   ├── compras.py              # protegido
    │   ├── favoritos.py            # protegido
    │   └── relatorios.py           # protegido
    ├── templates/                 # HTML (Jinja2 + Bootstrap 5 via CDN)
    └── static/css/style.css        # pequenos ajustes complementares ao Bootstrap

ecommerce.db                  # banco SQLite (criado automaticamente na raiz do projeto)
```

## Como executar localmente

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Acesse http://127.0.0.1:5000

Na primeira execução, o Flask cria o arquivo `ecommerce.db` (SQLite, na raiz do projeto)
e popula automaticamente algumas linhas de exemplo (`app/seed.py`). Três
usuários de teste (`vitor@email.com`, `ana@email.com`, `carlos@email.com`, todos com a
senha `123456`) para facilitar o login. 

## Autenticação e rotas protegidas

O login é feito por sessão Flask (`session["user_id"]`), com senha armazenada como hash
(`werkzeug.security.generate_password_hash`). O decorator `@login_required`
(`app/auth.py`) bloqueia o acesso de quem não estiver logado, redirecionando para a
tela de login e retomando a página original depois de autenticar.

Públicas (sem login): Início, listagem de Anúncios, listagem de Categorias
(e anúncios por categoria), Login e Cadastro.

Protegidas (exigem login): todo o restante perfil e gerenciamento de usuários,
detalhe/CRUD de anúncios, comprar, perguntar, responder perguntas, CRUD de perguntas e
compras, favoritos e relatórios de vendas/compras.

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


## Observações

- Exclusões em cascata: excluir um Usuario remove seus anúncios, perguntas, compras e
  listas de favoritos; excluir um Anuncio remove suas perguntas, compras e favoritos
  associados; excluir uma ListaFavoritos remove seus itens (`cascade="all, delete-orphan"`
  em `app/models.py`), refletindo as cardinalidades definidas no MER da Trilha 1.
- Este projeto usa uma tabela Usuario própria para autenticação (sem Flask-Login), o que
  é suficiente para o escopo da disciplina; em um sistema de produção real, o próximo
  passo natural seria adicionar Flask-Login (ou similar) para funcionalidades extras
  como "lembrar-me" e proteção contra fixação de sessão.
