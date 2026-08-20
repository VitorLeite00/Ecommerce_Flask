from flask import Blueprint, render_template

from app.constants import CURRENT_USER_ID
from app.models import Anuncio, Compra

relatorios_bp = Blueprint("relatorios", __name__)


@relatorios_bp.route("/vendas")
def vendas():
    """Relatorio de vendas: compras associadas aos anuncios do usuario logado."""
    minhas_vendas = (
        Compra.query.join(Anuncio)
        .filter(Anuncio.id_usuario == CURRENT_USER_ID)
        .order_by(Compra.id.desc())
        .all()
    )
    total = sum(v.valor_pago for v in minhas_vendas)
    return render_template("relatorios/vendas.html", vendas=minhas_vendas, total=total)


@relatorios_bp.route("/compras")
def compras():
    """Relatorio de compras: compras feitas pelo usuario logado."""
    minhas_compras = (
        Compra.query.filter_by(id_comprador=CURRENT_USER_ID).order_by(Compra.id.desc()).all()
    )
    total = sum(c.valor_pago for c in minhas_compras)
    return render_template("relatorios/compras.html", compras=minhas_compras, total=total)
