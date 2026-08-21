import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """Application factory: cria e configura a aplicacao Flask, inicializa o
    banco de dados (SQLite via SQLAlchemy) e registra um Blueprint para cada
    entidade do MER."""
    app = Flask(__name__)

    # SECRET_KEY vem de variavel de ambiente em producao (configurada na aba
    # Web do PythonAnywhere); em desenvolvimento local, usa um valor padrao.
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-troque-em-producao")

    # Banco de dados: SQLite, com o arquivo .db criado dentro da própria pasta
    # do projeto (nada de MySQL nem de configuração externa de banco).
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # importa os modelos para que fiquem registrados no SQLAlchemy
    from app import models  # noqa: F401

    from app.routes.main import main_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.categorias import categorias_bp
    from app.routes.anuncios import anuncios_bp
    from app.routes.perguntas import perguntas_bp
    from app.routes.compras import compras_bp
    from app.routes.favoritos import favoritos_bp
    from app.routes.relatorios import relatorios_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(categorias_bp, url_prefix="/categorias")
    app.register_blueprint(anuncios_bp, url_prefix="/anuncios")
    app.register_blueprint(perguntas_bp, url_prefix="/perguntas")
    app.register_blueprint(compras_bp, url_prefix="/compras")
    app.register_blueprint(favoritos_bp, url_prefix="/favoritos")
    app.register_blueprint(relatorios_bp, url_prefix="/relatorios")

    from app.auth import get_current_user

    @app.context_processor
    def inject_current_user():
        return {"current_user": get_current_user()}

    with app.app_context():
        db.create_all()
        from app.seed import seed_data

        seed_data()

    return app
