from flask import Flask


def create_app():
    """Application factory: cria e configura a aplicacao Flask,
    registrando um Blueprint para cada entidade do MER."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key-troque-em-producao"

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

    return app
