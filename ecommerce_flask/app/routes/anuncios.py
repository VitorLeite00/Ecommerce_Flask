from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.constants import CURRENT_USER_ID
from app.models import Anuncio, Categoria, ListaFavoritos, Pergunta

anuncios_bp = Blueprint("anuncios", __name__)


@anuncios_bp.route("/")
def listar():
    """Read (vitrine geral), com filtro opcional ?categoria=<id>."""
    id_categoria = request.args.get("categoria", type=int)
    query = Anuncio.query.filter_by(status="disponivel")
    if id_categoria:
        query = query.filter_by(id_categoria=id_categoria)
    anuncios = query.order_by(Anuncio.data_publicacao.desc()).all()
    categorias = Categoria.query.order_by(Categoria.nome).all()
    return render_template(
        "anuncios/list.html", anuncios=anuncios, categorias=categorias, id_categoria=id_categoria
    )


@anuncios_bp.route("/meus")
def meus_anuncios():
    """Read (lista) apenas dos anuncios do usuario logado."""
    anuncios = Anuncio.query.filter_by(id_usuario=CURRENT_USER_ID).order_by(Anuncio.id.desc()).all()
    return render_template("anuncios/meus.html", anuncios=anuncios)


@anuncios_bp.route("/novo", methods=["GET", "POST"])
def novo():
    """Create."""
    categorias = Categoria.query.order_by(Categoria.nome).all()
    if request.method == "POST":
        anuncio = Anuncio(
            titulo=request.form.get("titulo"),
            descricao=request.form.get("descricao"),
            preco=float(request.form.get("preco") or 0),
            data_publicacao=date.today(),
            status="disponivel",
            id_usuario=CURRENT_USER_ID,
            id_categoria=int(request.form.get("id_categoria")),
        )
        db.session.add(anuncio)
        db.session.commit()
        flash("Anúncio publicado com sucesso!")
        return redirect(url_for("anuncios.meus_anuncios"))
    return render_template("anuncios/form.html", categorias=categorias, anuncio=None)


@anuncios_bp.route("/<int:id_anuncio>/editar", methods=["GET", "POST"])
def editar(id_anuncio):
    """Update."""
    anuncio = Anuncio.query.get_or_404(id_anuncio)
    categorias = Categoria.query.order_by(Categoria.nome).all()
    if request.method == "POST":
        anuncio.titulo = request.form.get("titulo")
        anuncio.descricao = request.form.get("descricao")
        anuncio.preco = float(request.form.get("preco") or 0)
        anuncio.id_categoria = int(request.form.get("id_categoria"))
        db.session.commit()
        flash("Anúncio atualizado com sucesso!")
        return redirect(url_for("anuncios.meus_anuncios"))
    return render_template("anuncios/form.html", categorias=categorias, anuncio=anuncio)


@anuncios_bp.route("/<int:id_anuncio>/excluir", methods=["GET", "POST"])
def excluir(id_anuncio):
    """Delete, com tela de confirmação. Também remove perguntas, compras e
    favoritos associados a este anúncio (cascade definido no modelo)."""
    anuncio = Anuncio.query.get_or_404(id_anuncio)
    if request.method == "POST":
        db.session.delete(anuncio)
        db.session.commit()
        flash("Anúncio excluído com sucesso!")
        return redirect(url_for("anuncios.meus_anuncios"))
    return render_template(
        "confirm_delete.html",
        titulo="Excluir anúncio",
        mensagem=f'Tem certeza que deseja excluir o anúncio "{anuncio.titulo}"? '
        "Perguntas, compras e favoritos ligados a ele também serão removidos.",
        voltar_url=url_for("anuncios.meus_anuncios"),
    )


@anuncios_bp.route("/<int:id_anuncio>")
def detalhe(id_anuncio):
    """Read (detalhe)."""
    anuncio = Anuncio.query.get_or_404(id_anuncio)
    perguntas = Pergunta.query.filter_by(id_anuncio=id_anuncio).order_by(Pergunta.id.desc()).all()
    minhas_listas = ListaFavoritos.query.filter_by(id_usuario=CURRENT_USER_ID).all()
    return render_template(
        "anuncios/detail.html",
        anuncio=anuncio,
        vendedor=anuncio.usuario,
        perguntas=perguntas,
        minhas_listas=minhas_listas,
        is_owner=(anuncio.id_usuario == CURRENT_USER_ID),
    )
