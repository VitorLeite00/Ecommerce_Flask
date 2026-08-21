"""
Autenticação e gestão de sessão.

Implementa o padrão clássico do Flask para proteger rotas: a sessão guarda apenas
o id do usuário autenticado (session["user_id"]); a partir dele, get_current_user()
busca o registro completo no banco. O decorator login_required() bloqueia o acesso
a views que exigem login, redirecionando para a tela de login e preservando a URL
de destino original (?next=...), para retomar a navegação após autenticar.
"""

from functools import wraps

from flask import flash, redirect, request, session, url_for

from app.models import Usuario


def get_current_user():
    """Retorna o objeto Usuario da sessão atual, ou None se ninguém estiver logado."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    return Usuario.query.get(user_id)


def login_required(view_func):
    """Decorator: exige usuário autenticado para acessar a rota decorada."""

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get("user_id"):
            flash("Você precisa entrar na sua conta para acessar esta página.")
            return redirect(url_for("usuarios.login", next=request.path))
        return view_func(*args, **kwargs)

    return wrapped_view
