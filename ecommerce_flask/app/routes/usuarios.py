from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.constants import CURRENT_USER_ID
from app.models import Anuncio, Usuario

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/")
def listar():
    """Lista todos os usuarios cadastrados (Read)."""
    usuarios = Usuario.query.order_by(Usuario.nome).all()
    return render_template("usuarios/list.html", usuarios=usuarios)


@usuarios_bp.route("/perfil")
def perfil():
    """Perfil do usuario logado (simulado)."""
    usuario = Usuario.query.get_or_404(CURRENT_USER_ID)
    anuncios_usuario = Anuncio.query.filter_by(id_usuario=CURRENT_USER_ID).all()
    return render_template("usuarios/perfil.html", usuario=usuario, anuncios=anuncios_usuario)


@usuarios_bp.route("/<int:id_usuario>")
def detalhe(id_usuario):
    """Perfil publico de um usuario (Read)."""
    usuario = Usuario.query.get_or_404(id_usuario)
    anuncios_usuario = [a for a in usuario.anuncios if a.status == "disponivel"]
    return render_template("usuarios/detail.html", usuario=usuario, anuncios=anuncios_usuario)


@usuarios_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    """Create."""
    if request.method == "POST":
        usuario = Usuario(
            nome=request.form.get("nome"),
            email=request.form.get("email"),
            senha=request.form.get("senha"),
            data_cadastro=date.today(),
        )
        db.session.add(usuario)
        db.session.commit()
        flash("Cadastro realizado com sucesso!")
        return redirect(url_for("usuarios.login"))
    return render_template("usuarios/cadastro.html")


@usuarios_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        flash("Login simulado - autenticação real será implementada em etapa futura.")
        return redirect(url_for("main.index"))
    return render_template("usuarios/login.html")


@usuarios_bp.route("/<int:id_usuario>/editar", methods=["GET", "POST"])
def editar(id_usuario):
    """Update."""
    usuario = Usuario.query.get_or_404(id_usuario)
    if request.method == "POST":
        usuario.nome = request.form.get("nome")
        usuario.email = request.form.get("email")
        nova_senha = request.form.get("senha")
        if nova_senha:
            usuario.senha = nova_senha
        db.session.commit()
        flash("Usuário atualizado com sucesso!")
        return redirect(url_for("usuarios.listar"))
    return render_template("usuarios/form.html", usuario=usuario)


@usuarios_bp.route("/<int:id_usuario>/excluir", methods=["GET", "POST"])
def excluir(id_usuario):
    """Delete, com tela de confirmação."""
    usuario = Usuario.query.get_or_404(id_usuario)
    if request.method == "POST":
        db.session.delete(usuario)
        db.session.commit()
        flash("Usuário excluído com sucesso!")
        return redirect(url_for("usuarios.listar"))
    return render_template(
        "confirm_delete.html",
        titulo="Excluir usuário",
        mensagem=f'Tem certeza que deseja excluir o usuário "{usuario.nome}"? '
        "Todos os anúncios, perguntas, compras e listas de favoritos dele também serão removidos.",
        voltar_url=url_for("usuarios.listar"),
    )
