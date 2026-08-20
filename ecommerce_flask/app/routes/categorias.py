from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.models import Anuncio, Categoria

categorias_bp = Blueprint("categorias", __name__)


@categorias_bp.route("/")
def listar():
    """Read (lista)."""
    categorias = Categoria.query.order_by(Categoria.nome).all()
    return render_template("categorias/list.html", categorias=categorias)


@categorias_bp.route("/<int:id_categoria>")
def anuncios_da_categoria(id_categoria):
    """Read (detalhe): anuncios disponiveis dentro da categoria."""
    categoria = Categoria.query.get_or_404(id_categoria)
    anuncios = Anuncio.query.filter_by(id_categoria=id_categoria, status="disponivel").all()
    return render_template("categorias/anuncios.html", categoria=categoria, anuncios=anuncios)


@categorias_bp.route("/nova", methods=["GET", "POST"])
def nova():
    """Create."""
    if request.method == "POST":
        categoria = Categoria(nome=request.form.get("nome"), descricao=request.form.get("descricao"))
        db.session.add(categoria)
        db.session.commit()
        flash("Categoria criada com sucesso!")
        return redirect(url_for("categorias.listar"))
    return render_template("categorias/form.html", categoria=None)


@categorias_bp.route("/<int:id_categoria>/editar", methods=["GET", "POST"])
def editar(id_categoria):
    """Update."""
    categoria = Categoria.query.get_or_404(id_categoria)
    if request.method == "POST":
        categoria.nome = request.form.get("nome")
        categoria.descricao = request.form.get("descricao")
        db.session.commit()
        flash("Categoria atualizada com sucesso!")
        return redirect(url_for("categorias.listar"))
    return render_template("categorias/form.html", categoria=categoria)


@categorias_bp.route("/<int:id_categoria>/excluir", methods=["GET", "POST"])
def excluir(id_categoria):
    """Delete, com tela de confirmação. Bloqueia exclusão se houver anúncios vinculados."""
    categoria = Categoria.query.get_or_404(id_categoria)
    if request.method == "POST":
        if categoria.anuncios:
            flash("Não é possível excluir: existem anúncios cadastrados nesta categoria.")
            return redirect(url_for("categorias.listar"))
        db.session.delete(categoria)
        db.session.commit()
        flash("Categoria excluída com sucesso!")
        return redirect(url_for("categorias.listar"))
    return render_template(
        "confirm_delete.html",
        titulo="Excluir categoria",
        mensagem=f'Tem certeza que deseja excluir a categoria "{categoria.nome}"?',
        voltar_url=url_for("categorias.listar"),
    )
