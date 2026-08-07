from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.data import ANUNCIOS, CURRENT_USER_ID, USUARIOS

usuarios_bp = Blueprint("usuarios", __name__)


def get_usuario(id_usuario):
    return next((u for u in USUARIOS if u["id"] == id_usuario), None)


@usuarios_bp.route("/")
def listar():
    """Lista todos os usuarios cadastrados (rota da entidade Usuario)."""
    return render_template("usuarios/list.html", usuarios=USUARIOS)


@usuarios_bp.route("/perfil")
def perfil():
    """Perfil do usuario logado (simulado via CURRENT_USER_ID)."""
    usuario = get_usuario(CURRENT_USER_ID)
    anuncios_usuario = [a for a in ANUNCIOS if a["id_usuario"] == CURRENT_USER_ID]
    return render_template("usuarios/perfil.html", usuario=usuario, anuncios=anuncios_usuario)


@usuarios_bp.route("/<int:id_usuario>")
def detalhe(id_usuario):
    """Perfil publico de um usuario (vitrine dos anuncios dele)."""
    usuario = get_usuario(id_usuario)
    anuncios_usuario = [
        a for a in ANUNCIOS if a["id_usuario"] == id_usuario and a["status"] == "disponivel"
    ]
    return render_template("usuarios/detail.html", usuario=usuario, anuncios=anuncios_usuario)


@usuarios_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        novo_id = max(u["id"] for u in USUARIOS) + 1
        USUARIOS.append(
            {
                "id": novo_id,
                "nome": request.form.get("nome"),
                "email": request.form.get("email"),
                "senha": request.form.get("senha"),
                "data_cadastro": None,
            }
        )
        flash("Cadastro realizado com sucesso!")
        return redirect(url_for("usuarios.login"))
    return render_template("usuarios/cadastro.html")


@usuarios_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        flash("Login simulado - autenticação real será implementada em etapa futura.")
        return redirect(url_for("main.index"))
    return render_template("usuarios/login.html")
