from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.constants import CURRENT_USER_ID
from app.models import ItemFavorito, ListaFavoritos

favoritos_bp = Blueprint("favoritos", __name__)


@favoritos_bp.route("/")
def minhas_listas():
    """Read (lista) das listas de favoritos do usuario logado."""
    listas = ListaFavoritos.query.filter_by(id_usuario=CURRENT_USER_ID).all()
    return render_template("favoritos/list.html", listas=listas)


@favoritos_bp.route("/nova", methods=["GET", "POST"])
def nova_lista():
    """Create."""
    if request.method == "POST":
        lista = ListaFavoritos(nome_lista=request.form.get("nome_lista"), id_usuario=CURRENT_USER_ID)
        db.session.add(lista)
        db.session.commit()
        flash("Lista de favoritos criada!")
        return redirect(url_for("favoritos.minhas_listas"))
    return render_template("favoritos/form.html", lista=None)


@favoritos_bp.route("/<int:id_lista>")
def detalhe(id_lista):
    """Read (detalhe): anuncios salvos na lista."""
    lista = ListaFavoritos.query.get_or_404(id_lista)
    return render_template("favoritos/detail.html", lista=lista)


@favoritos_bp.route("/<int:id_lista>/editar", methods=["GET", "POST"])
def editar(id_lista):
    """Update: renomear a lista."""
    lista = ListaFavoritos.query.get_or_404(id_lista)
    if request.method == "POST":
        lista.nome_lista = request.form.get("nome_lista")
        db.session.commit()
        flash("Lista atualizada com sucesso!")
        return redirect(url_for("favoritos.minhas_listas"))
    return render_template("favoritos/form.html", lista=lista)


@favoritos_bp.route("/<int:id_lista>/excluir", methods=["GET", "POST"])
def excluir(id_lista):
    """Delete da lista (e de todos os itens dentro dela), com confirmação."""
    lista = ListaFavoritos.query.get_or_404(id_lista)
    if request.method == "POST":
        db.session.delete(lista)
        db.session.commit()
        flash("Lista excluída com sucesso!")
        return redirect(url_for("favoritos.minhas_listas"))
    return render_template(
        "confirm_delete.html",
        titulo="Excluir lista de favoritos",
        mensagem=f'Tem certeza que deseja excluir a lista "{lista.nome_lista}" e todos os itens salvos nela?',
        voltar_url=url_for("favoritos.minhas_listas"),
    )


@favoritos_bp.route("/<int:id_lista>/adicionar", methods=["POST"])
def adicionar_item(id_lista):
    """Create: adiciona um anuncio a uma lista de favoritos (ItemFavorito)."""
    id_anuncio = int(request.form.get("id_anuncio"))
    item = ItemFavorito(id_lista=id_lista, id_anuncio=id_anuncio, data_adicao=date.today())
    db.session.add(item)
    db.session.commit()
    flash("Anúncio adicionado aos favoritos!")
    return redirect(url_for("anuncios.detalhe", id_anuncio=id_anuncio))


@favoritos_bp.route("/item/<int:id_item>/excluir", methods=["GET", "POST"])
def excluir_item(id_item):
    """Delete de um item de favorito especifico, com confirmação."""
    item = ItemFavorito.query.get_or_404(id_item)
    if request.method == "POST":
        id_lista = item.id_lista
        db.session.delete(item)
        db.session.commit()
        flash("Item removido da lista!")
        return redirect(url_for("favoritos.detalhe", id_lista=id_lista))
    return render_template(
        "confirm_delete.html",
        titulo="Remover item da lista",
        mensagem=f'Tem certeza que deseja remover "{item.anuncio.titulo}" desta lista de favoritos?',
        voltar_url=url_for("favoritos.detalhe", id_lista=item.id_lista),
    )
