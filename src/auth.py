"""Autenticação simples baseada em sessão (cadastro, login e logout)."""

import sqlite3
from functools import wraps

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import repositorio
from .db import get_db
from .validacao import (
    ErroDeValidacao,
    validar_email,
    validar_nome,
    validar_senha,
)

bp = Blueprint("auth", __name__)


def carregar_usuario_logado() -> None:
    """Carrega o usuário da sessão em `g.usuario` antes de cada requisição."""
    usuario_id = session.get("usuario_id")
    g.usuario = (
        repositorio.buscar_usuario_por_id(get_db(), usuario_id)
        if usuario_id
        else None
    )


def login_obrigatorio(view):
    """Decorator que protege rotas privadas."""

    @wraps(view)
    def wrapper(*args, **kwargs):
        if g.get("usuario") is None:
            flash("Faça login para acessar o quadro de tarefas.", "aviso")
            return redirect(url_for("auth.login", proximo=request.path))
        return view(*args, **kwargs)

    return wrapper

def _caminho_interno(destino: str) -> bool:
    """True só para caminhos do próprio site (rejeita `//host` e `/\\host`)."""
    return (
        destino.startswith("/")
        and not destino.startswith("//")
        and "\\" not in destino
    )

@bp.before_app_request
def preparar_sessao() -> None:
    carregar_usuario_logado()


@bp.route("/cadastro", methods=("GET", "POST"))
def cadastro():
    if request.method == "POST":
        try:
            nome = validar_nome(request.form.get("nome"))
            email = validar_email(request.form.get("email"))
            senha = validar_senha(request.form.get("senha"))

            db = get_db()
            repositorio.criar_usuario(db, nome, email, generate_password_hash(senha))
        except ErroDeValidacao as erro:
            flash(str(erro), "erro")
        except sqlite3.IntegrityError:
            flash("Este e-mail já está cadastrado.", "erro")
        else:
            flash("Conta criada com sucesso. Faça login para começar.", "sucesso")
            return redirect(url_for("auth.login"))

    return render_template("auth/cadastro.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        senha = request.form.get("senha") or ""
        usuario = repositorio.buscar_usuario_por_email(get_db(), email)

        if usuario is None or not check_password_hash(usuario["senha_hash"], senha):
            flash("E-mail ou senha inválidos.", "erro")
        else:
            session.clear()
            session["usuario_id"] = usuario["id"]
            flash(f"Bem-vindo(a), {usuario['nome']}!", "sucesso")
            proximo = request.args.get("proximo") or url_for("tarefas.quadro")
            # Evita redirecionamento aberto: só aceitamos caminhos internos.
            if not _caminho_interno(proximo):
                proximo = url_for("tarefas.quadro")
            return redirect(proximo)

    return render_template("auth/login.html")


@bp.post("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada.", "sucesso")
    return redirect(url_for("auth.login"))
