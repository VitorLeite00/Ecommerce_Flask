from flask import Blueprint, render_template

from app.data import ANUNCIOS, COMPRAS, CURRENT_USER_ID

relatorios_bp = Blueprint("relatorios", __name__)


@relatorios_bp.route("/vendas")
def vendas():
    """Relatorio de vendas: compras associadas aos anuncios do usuario logado."""
    meus_anuncios_ids = [a["id"] for a in ANUNCIOS if a["id_usuario"] == CURRENT_USER_ID]
    minhas_vendas = [c for c in COMPRAS if c["id_anuncio"] in meus_anuncios_ids]
    anuncios_por_id = {a["id"]: a for a in ANUNCIOS}
    total = sum(v["valor_pago"] for v in minhas_vendas)
    return render_template(
        "relatorios/vendas.html", vendas=minhas_vendas, anuncios_por_id=anuncios_por_id, total=total
    )


@relatorios_bp.route("/compras")
def compras():
    """Relatorio de compras: compras feitas pelo usuario logado."""
    minhas_compras = [c for c in COMPRAS if c["id_comprador"] == CURRENT_USER_ID]
    anuncios_por_id = {a["id"]: a for a in ANUNCIOS}
    total = sum(c["valor_pago"] for c in minhas_compras)
    return render_template(
        "relatorios/compras.html", compras=minhas_compras, anuncios_por_id=anuncios_por_id, total=total
    )
