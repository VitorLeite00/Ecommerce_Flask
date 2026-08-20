from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.constants import CURRENT_USER_ID
from app.models import Anuncio, Compra

compras_bp = Blueprint("compras", __name__)


@compras_bp.route("/")
def listar():
    """Read (lista geral de todas as compras do sistema)."""
    compras = Compra.query.order_by(Compra.id.desc()).all()
    return render_template("compras/list.html", compras=compras)


@compras_bp.route("/<int:id_compra>")
def detalhe(id_compra):
    """Read (detalhe)."""
    compra = Compra.query.get_or_404(id_compra)
    return render_template("compras/detail.html", compra=compra)


@compras_bp.route("/novo", methods=["POST"])
def nova():
    """Create: usuario compra um anuncio (sem carrinho de compras)."""
    id_anuncio = int(request.form.get("id_anuncio"))
    anuncio = Anuncio.query.get_or_404(id_anuncio)
    if anuncio.status == "disponivel":
        compra = Compra(
            data_compra=date.today(),
            valor_pago=anuncio.preco,
            id_anuncio=id_anuncio,
            id_comprador=CURRENT_USER_ID,
        )
        anuncio.status = "vendido"
        db.session.add(compra)
        db.session.commit()
        flash("Compra realizada com sucesso!")
    else:
        flash("Este anúncio não está mais disponível.")
    return redirect(url_for("relatorios.compras"))


@compras_bp.route("/<int:id_compra>/editar", methods=["GET", "POST"])
def editar(id_compra):
    """Update (corrigir valor pago ou data de uma compra já registrada)."""
    compra = Compra.query.get_or_404(id_compra)
    if request.method == "POST":
        compra.valor_pago = float(request.form.get("valor_pago") or 0)
        db.session.commit()
        flash("Compra atualizada com sucesso!")
        return redirect(url_for("compras.listar"))
    return render_template("compras/form.html", compra=compra)


@compras_bp.route("/<int:id_compra>/excluir", methods=["GET", "POST"])
def excluir(id_compra):
    """Delete, com tela de confirmação. Ao excluir, o anúncio volta a ficar disponível."""
    compra = Compra.query.get_or_404(id_compra)
    if request.method == "POST":
        anuncio = compra.anuncio
        if anuncio:
            anuncio.status = "disponivel"
        db.session.delete(compra)
        db.session.commit()
        flash("Compra excluída! O anúncio voltou a ficar disponível.")
        return redirect(url_for("compras.listar"))
    return render_template(
        "confirm_delete.html",
        titulo="Excluir compra",
        mensagem=f'Tem certeza que deseja excluir a compra do anúncio '
        f'"{compra.anuncio.titulo if compra.anuncio else compra.id}"?',
        voltar_url=url_for("compras.listar"),
    )
