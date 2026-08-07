from flask import Blueprint, flash, redirect, request, url_for

from app.data import ANUNCIOS, COMPRAS, CURRENT_USER_ID

compras_bp = Blueprint("compras", __name__)


@compras_bp.route("/novo", methods=["POST"])
def nova():
    """Usuario compra um anuncio (sem carrinho de compras)."""
    id_anuncio = int(request.form.get("id_anuncio"))
    anuncio = next((a for a in ANUNCIOS if a["id"] == id_anuncio), None)
    if anuncio and anuncio["status"] == "disponivel":
        novo_id = max((c["id"] for c in COMPRAS), default=0) + 1
        COMPRAS.append(
            {
                "id": novo_id,
                "data_compra": None,
                "valor_pago": anuncio["preco"],
                "id_anuncio": id_anuncio,
                "id_comprador": CURRENT_USER_ID,
            }
        )
        anuncio["status"] = "vendido"
        flash("Compra realizada com sucesso!")
    return redirect(url_for("relatorios.compras"))
