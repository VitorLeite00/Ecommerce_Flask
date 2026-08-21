from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.auth import get_current_user, login_required
from app.models import Usuario

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/")
@login_required
def listar():
    """Read (lista)."""
    usuarios = Usuario.query.order_by(Usuario.nome).all()
    return render_template("usuarios/list.html", usuarios=usuarios)


@usuarios_bp.route("/perfil")
@login_required
def perfil():
    """Perfil do usuario logado."""
    usuario = get_current_user()
    return render_template("usuarios/perfil.html", usuario=usuario, anuncios=usuario.anuncios)


@usuarios_bp.route("/<int:id_usuario>")
@login_required
def detalhe(id_usuario):
    """Read (detalhe): perfil publico de um usuario (dentro da area logada)."""
    usuario = Usuario.query.get_or_404(id_usuario)
    anuncios_usuario = [a for a in usuario.anuncios if a.status == "disponivel"]
    return render_template("usuarios/detail.html", usuario=usuario, anuncios=anuncios_usuario)


@usuarios_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    """Create: rota publica de auto-cadastro."""
    if request.method == "POST":
        email = request.form.get("email")
        if Usuario.query.filter_by(email=email).first():
            flash("Já existe uma conta com este email.")
            return render_template("usuarios/cadastro.html")
        usuario = Usuario(
            nome=request.form.get("nome"),
            email=email,
            senha_hash=generate_password_hash(request.form.get("senha")),
            data_cadastro=date.today(),
        )
        db.session.add(usuario)
        db.session.commit()
        flash("Cadastro realizado com sucesso! Faça login para continuar.")
        return redirect(url_for("usuarios.login"))
    return render_template("usuarios/cadastro.html")


@usuarios_bp.route("/login", methods=["GET", "POST"])
def login():
    """Autenticacao real: verifica email/senha e grava o id do usuario na sessao."""
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha_hash, senha):
            session["user_id"] = usuario.id
            flash(f"Bem-vindo(a), {usuario.nome}!")
            destino = request.args.get("next") or url_for("main.index")
            return redirect(destino)
        flash("Email ou senha inválidos.")
    return render_template("usuarios/login.html")


@usuarios_bp.route("/logout")
def logout():
    """Encerra a sessao do usuario."""
    session.pop("user_id", None)
    flash("Você saiu da sua conta.")
    return redirect(url_for("main.index"))


@usuarios_bp.route("/<int:id_usuario>/editar", methods=["GET", "POST"])
@login_required
def editar(id_usuario):
    """Update."""
    usuario = Usuario.query.get_or_404(id_usuario)
    if request.method == "POST":
        usuario.nome = request.form.get("nome")
        usuario.email = request.form.get("email")
        nova_senha = request.form.get("senha")
        if nova_senha:
            usuario.senha_hash = generate_password_hash(nova_senha)
        db.session.commit()
        flash("Usuário atualizado com sucesso!")
        return redirect(url_for("usuarios.listar"))
    return render_template("usuarios/form.html", usuario=usuario)


@usuarios_bp.route("/<int:id_usuario>/excluir", methods=["GET", "POST"])
@login_required
def excluir(id_usuario):
    """Delete, com tela de confirmação."""
    usuario = Usuario.query.get_or_404(id_usuario)
    if request.method == "POST":
        era_o_proprio_usuario = usuario.id == session.get("user_id")
        db.session.delete(usuario)
        db.session.commit()
        if era_o_proprio_usuario:
            session.pop("user_id", None)
        flash("Usuário excluído com sucesso!")
        return redirect(url_for("usuarios.listar"))
    return render_template(
        "confirm_delete.html",
        titulo="Excluir usuário",
        mensagem=f'Tem certeza que deseja excluir o usuário "{usuario.nome}"? '
        "Todos os anúncios, perguntas, compras e listas de favoritos dele também serão removidos.",
        voltar_url=url_for("usuarios.listar"),
    )
