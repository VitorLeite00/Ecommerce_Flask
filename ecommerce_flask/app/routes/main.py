from flask import Blueprint, render_template

from app.models import Anuncio, Categoria

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    destaques = (
        Anuncio.query.filter_by(status="disponivel")
        .order_by(Anuncio.data_publicacao.desc())
        .limit(4)
        .all()
    )
    categorias = Categoria.query.order_by(Categoria.nome).all()
    return render_template("index.html", destaques=destaques, categorias=categorias)
