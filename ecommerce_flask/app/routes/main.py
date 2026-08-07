from flask import Blueprint, render_template

from app.data import ANUNCIOS, CATEGORIAS

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    destaques = [a for a in ANUNCIOS if a["status"] == "disponivel"][:4]
    return render_template("index.html", destaques=destaques, categorias=CATEGORIAS)
