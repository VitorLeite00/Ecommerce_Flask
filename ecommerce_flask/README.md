# Marketplace — Sistema de E-commerce (Flask)

Projeto acadêmico: estrutura inicial de um sistema de e-commerce desenvolvido com o
framework Flask, como parte da disciplina de Desenvolvimento de Software.

## Requisitos atendidos

- Usuários que anunciam e compram produtos
- Anúncios organizados em categorias
- Perguntas em anúncios, respondidas pelo dono do anúncio
- Compra direta de um anúncio (sem carrinho)
- Listas de anúncios favoritos
- Relatório de vendas e relatório de compras do usuário

## Estrutura do projeto

```
ecommerce_flask/
├── run.py                  # ponto de entrada da aplicação
├── requirements.txt
└── app/
    ├── __init__.py         # application factory + registro dos blueprints
    ├── data.py              # dados em memória (mock) representando as tabelas do MER
    ├── routes/               # um blueprint por entidade do MER
    │   ├── main.py
    │   ├── usuarios.py
    │   ├── categorias.py
    │   ├── anuncios.py
    │   ├── perguntas.py
    │   ├── compras.py
    │   ├── favoritos.py
    │   └── relatorios.py
    ├── templates/            # HTML (Jinja2), incluindo o menu de navegação em base.html
    └── static/css/style.css
```

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Acesse http://127.0.0.1:5000

## Observações sobre este estágio do projeto

- Os dados ficam em listas Python em memória (`app/data.py`), simulando as tabelas do MER.
  Isso evita a complexidade de configurar um banco de dados nesta primeira entrega, mas
  mantém os mesmos nomes de entidades/atributos definidos no MER, facilitando a migração
  futura para modelos SQLAlchemy.
- Não há sistema de autenticação real: um usuário fixo (`CURRENT_USER_ID`) simula o
  usuário logado, para permitir navegar por "Meus Anúncios", "Favoritos" e "Relatórios".
  As telas de Login e Cadastro já existem e serão conectadas à autenticação real na
  próxima etapa (ex.: Flask-Login + hashing de senha).
- O menu de navegação (`app/templates/base.html`) segue o diagrama de navegação entregue
  junto com este projeto.

## Entidades e rotas (MER)

| Entidade | Blueprint | Rotas principais |
|---|---|---|
| Usuario | `usuarios` | `/usuarios`, `/usuarios/<id>`, `/usuarios/perfil`, `/usuarios/cadastro`, `/usuarios/login` |
| Categoria | `categorias` | `/categorias`, `/categorias/<id>` |
| Anuncio | `anuncios` | `/anuncios`, `/anuncios/<id>`, `/anuncios/novo`, `/anuncios/<id>/editar`, `/anuncios/meus` |
| Pergunta | `perguntas` | `/perguntas/novo`, `/perguntas/recebidas`, `/perguntas/<id>/responder` |
| Compra | `compras` | `/compras/novo` |
| ListaFavoritos / ItemFavorito | `favoritos` | `/favoritos`, `/favoritos/nova`, `/favoritos/<id>`, `/favoritos/<id>/adicionar` |
| Relatórios (consulta) | `relatorios` | `/relatorios/vendas`, `/relatorios/compras` |
