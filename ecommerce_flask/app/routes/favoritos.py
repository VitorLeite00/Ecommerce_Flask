from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.data import ANUNCIOS, CURRENT_USER_ID, ITENS_FAVORITOS, LISTAS_FAVORITOS

favoritos_bp = Blueprint("favoritos", __name__)


@favoritos_bp.route("/")
def minhas_listas():
    listas = [l for l in LISTAS_FAVORITOS if l["id_usuario"] == CURRENT_USER_ID]
    return render_template("favoritos/list.html", listas=listas)


@favoritos_bp.route("/nova", methods=["GET", "POST"])
def nova_lista():
    if request.method == "POST":
        novo_id = max((l["id"] for l in LISTAS_FAVORITOS), default=0) + 1
        LISTAS_FAVORITOS.append(
            {"id": novo_id, "nome_lista": request.form.get("nome_lista"), "id_usuario": CURRENT_USER_ID}
        )
        flash("Lista de favoritos criada!")
        return redirect(url_for("favoritos.minhas_listas"))
    return render_template("favoritos/form.html")


@favoritos_bp.route("/<int:id_lista>")
def detalhe(id_lista):
    lista = next((l for l in LISTAS_FAVORITOS if l["id"] == id_lista), None)
    itens = [i for i in ITENS_FAVORITOS if i["id_lista"] == id_lista]
    anuncios_por_id = {a["id"]: a for a in ANUNCIOS}
    return render_template(
        "favoritos/detail.html", lista=lista, itens=itens, anuncios_por_id=anuncios_por_id
    )


@favoritos_bp.route("/<int:id_lista>/adicionar", methods=["POST"])
def adicionar_item(id_lista):
    """Adiciona um anuncio a uma lista de favoritos (ItemFavorito)."""
    id_anuncio = int(request.form.get("id_anuncio"))
    novo_id = max((i["id"] for i in ITENS_FAVORITOS), default=0) + 1
    ITENS_FAVORITOS.append(
        {"id": novo_id, "id_lista": id_lista, "id_anuncio": id_anuncio, "data_adicao": None}
    )
    flash("Anúncio adicionado aos favoritos!")
    return redirect(url_for("anuncios.detalhe", id_anuncio=id_anuncio))
