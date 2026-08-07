from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.data import ANUNCIOS, CURRENT_USER_ID, PERGUNTAS

perguntas_bp = Blueprint("perguntas", __name__)


@perguntas_bp.route("/novo", methods=["POST"])
def nova():
    """Usuario faz uma pergunta em um anuncio."""
    id_anuncio = int(request.form.get("id_anuncio"))
    novo_id = max((p["id"] for p in PERGUNTAS), default=0) + 1
    PERGUNTAS.append(
        {
            "id": novo_id,
            "texto_pergunta": request.form.get("texto_pergunta"),
            "data_pergunta": None,
            "texto_resposta": None,
            "data_resposta": None,
            "id_anuncio": id_anuncio,
            "id_usuario": CURRENT_USER_ID,
        }
    )
    flash("Pergunta enviada!")
    return redirect(url_for("anuncios.detalhe", id_anuncio=id_anuncio))


@perguntas_bp.route("/recebidas")
def recebidas():
    """Perguntas feitas nos anuncios do usuario logado, para ele responder."""
    meus_anuncios_ids = [a["id"] for a in ANUNCIOS if a["id_usuario"] == CURRENT_USER_ID]
    perguntas = [p for p in PERGUNTAS if p["id_anuncio"] in meus_anuncios_ids]
    anuncios_por_id = {a["id"]: a for a in ANUNCIOS}
    return render_template(
        "perguntas/recebidas.html", perguntas=perguntas, anuncios_por_id=anuncios_por_id
    )


@perguntas_bp.route("/<int:id_pergunta>/responder", methods=["POST"])
def responder(id_pergunta):
    """O dono do anuncio responde a pergunta."""
    pergunta = next((p for p in PERGUNTAS if p["id"] == id_pergunta), None)
    if pergunta:
        pergunta["texto_resposta"] = request.form.get("texto_resposta")
    flash("Resposta enviada!")
    return redirect(url_for("perguntas.recebidas"))
