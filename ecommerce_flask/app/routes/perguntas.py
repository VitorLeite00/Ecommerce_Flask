from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.constants import CURRENT_USER_ID
from app.models import Anuncio, Pergunta

perguntas_bp = Blueprint("perguntas", __name__)


@perguntas_bp.route("/")
def listar():
    """Read (lista geral de todas as perguntas do sistema)."""
    perguntas = Pergunta.query.order_by(Pergunta.id.desc()).all()
    return render_template("perguntas/list.html", perguntas=perguntas)


@perguntas_bp.route("/novo", methods=["POST"])
def nova():
    """Create: usuario faz uma pergunta em um anuncio."""
    id_anuncio = int(request.form.get("id_anuncio"))
    pergunta = Pergunta(
        texto_pergunta=request.form.get("texto_pergunta"),
        data_pergunta=date.today(),
        id_anuncio=id_anuncio,
        id_usuario=CURRENT_USER_ID,
    )
    db.session.add(pergunta)
    db.session.commit()
    flash("Pergunta enviada!")
    return redirect(url_for("anuncios.detalhe", id_anuncio=id_anuncio))


@perguntas_bp.route("/recebidas")
def recebidas():
    """Read: perguntas feitas nos anuncios do usuario logado, para ele responder."""
    perguntas = (
        Pergunta.query.join(Anuncio)
        .filter(Anuncio.id_usuario == CURRENT_USER_ID)
        .order_by(Pergunta.id.desc())
        .all()
    )
    return render_template("perguntas/recebidas.html", perguntas=perguntas)


@perguntas_bp.route("/<int:id_pergunta>/responder", methods=["POST"])
def responder(id_pergunta):
    """Update rapido: o dono do anuncio responde a pergunta."""
    pergunta = Pergunta.query.get_or_404(id_pergunta)
    pergunta.texto_resposta = request.form.get("texto_resposta")
    pergunta.data_resposta = date.today()
    db.session.commit()
    flash("Resposta enviada!")
    return redirect(url_for("perguntas.recebidas"))


@perguntas_bp.route("/<int:id_pergunta>/editar", methods=["GET", "POST"])
def editar(id_pergunta):
    """Update completo (pergunta e resposta)."""
    pergunta = Pergunta.query.get_or_404(id_pergunta)
    if request.method == "POST":
        pergunta.texto_pergunta = request.form.get("texto_pergunta")
        resposta = request.form.get("texto_resposta")
        pergunta.texto_resposta = resposta or None
        if resposta and not pergunta.data_resposta:
            pergunta.data_resposta = date.today()
        db.session.commit()
        flash("Pergunta atualizada com sucesso!")
        return redirect(url_for("perguntas.listar"))
    return render_template("perguntas/form.html", pergunta=pergunta)


@perguntas_bp.route("/<int:id_pergunta>/excluir", methods=["GET", "POST"])
def excluir(id_pergunta):
    """Delete, com tela de confirmação."""
    pergunta = Pergunta.query.get_or_404(id_pergunta)
    if request.method == "POST":
        db.session.delete(pergunta)
        db.session.commit()
        flash("Pergunta excluída com sucesso!")
        return redirect(url_for("perguntas.listar"))
    return render_template(
        "confirm_delete.html",
        titulo="Excluir pergunta",
        mensagem=f'Tem certeza que deseja excluir a pergunta "{pergunta.texto_pergunta[:80]}"?',
        voltar_url=url_for("perguntas.listar"),
    )
