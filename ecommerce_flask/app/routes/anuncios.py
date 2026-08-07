from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.data import ANUNCIOS, CATEGORIAS, CURRENT_USER_ID, LISTAS_FAVORITOS, PERGUNTAS, USUARIOS

anuncios_bp = Blueprint("anuncios", __name__)


def get_anuncio(id_anuncio):
    return next((a for a in ANUNCIOS if a["id"] == id_anuncio), None)


@anuncios_bp.route("/")
def listar():
    """Vitrine geral de anuncios, com filtro opcional ?categoria=<id>."""
    id_categoria = request.args.get("categoria", type=int)
    anuncios = [a for a in ANUNCIOS if a["status"] == "disponivel"]
    if id_categoria:
        anuncios = [a for a in anuncios if a["id_categoria"] == id_categoria]
    return render_template(
        "anuncios/list.html", anuncios=anuncios, categorias=CATEGORIAS, id_categoria=id_categoria
    )


@anuncios_bp.route("/meus")
def meus_anuncios():
    anuncios = [a for a in ANUNCIOS if a["id_usuario"] == CURRENT_USER_ID]
    return render_template("anuncios/meus.html", anuncios=anuncios)


@anuncios_bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        novo_id = max((a["id"] for a in ANUNCIOS), default=0) + 1
        ANUNCIOS.append(
            {
                "id": novo_id,
                "titulo": request.form.get("titulo"),
                "descricao": request.form.get("descricao"),
                "preco": float(request.form.get("preco") or 0),
                "data_publicacao": None,
                "status": "disponivel",
                "id_usuario": CURRENT_USER_ID,
                "id_categoria": int(request.form.get("id_categoria")),
            }
        )
        flash("Anúncio publicado com sucesso!")
        return redirect(url_for("anuncios.meus_anuncios"))
    return render_template("anuncios/form.html", categorias=CATEGORIAS, anuncio=None)


@anuncios_bp.route("/<int:id_anuncio>/editar", methods=["GET", "POST"])
def editar(id_anuncio):
    anuncio = get_anuncio(id_anuncio)
    if request.method == "POST":
        anuncio["titulo"] = request.form.get("titulo")
        anuncio["descricao"] = request.form.get("descricao")
        anuncio["preco"] = float(request.form.get("preco") or 0)
        anuncio["id_categoria"] = int(request.form.get("id_categoria"))
        flash("Anúncio atualizado!")
        return redirect(url_for("anuncios.meus_anuncios"))
    return render_template("anuncios/form.html", categorias=CATEGORIAS, anuncio=anuncio)


@anuncios_bp.route("/<int:id_anuncio>")
def detalhe(id_anuncio):
    anuncio = get_anuncio(id_anuncio)
    vendedor = next((u for u in USUARIOS if u["id"] == anuncio["id_usuario"]), None)
    perguntas = [p for p in PERGUNTAS if p["id_anuncio"] == id_anuncio]
    minhas_listas = [l for l in LISTAS_FAVORITOS if l["id_usuario"] == CURRENT_USER_ID]
    return render_template(
        "anuncios/detail.html",
        anuncio=anuncio,
        vendedor=vendedor,
        perguntas=perguntas,
        minhas_listas=minhas_listas,
    )
