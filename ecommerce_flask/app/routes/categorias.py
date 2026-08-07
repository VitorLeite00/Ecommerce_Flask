from flask import Blueprint, render_template

from app.data import ANUNCIOS, CATEGORIAS

categorias_bp = Blueprint("categorias", __name__)


@categorias_bp.route("/")
def listar():
    return render_template("categorias/list.html", categorias=CATEGORIAS)


@categorias_bp.route("/<int:id_categoria>")
def anuncios_da_categoria(id_categoria):
    categoria = next((c for c in CATEGORIAS if c["id"] == id_categoria), None)
    anuncios = [
        a for a in ANUNCIOS if a["id_categoria"] == id_categoria and a["status"] == "disponivel"
    ]
    return render_template("categorias/anuncios.html", categoria=categoria, anuncios=anuncios)
