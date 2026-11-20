"""Rotas do sistema: quadro Kanban, CRUD de tarefas e painel de métricas."""

from flask import (
    Blueprint,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)

from . import repositorio
from .auth import login_obrigatorio
from .db import get_db
from .validacao import (
    PRIORIDADES_VALIDAS,
    STATUS_VALIDOS,
    ErroDeValidacao,
    validar_descricao,
    validar_prazo,
    validar_prioridade,
    validar_status,
    validar_titulo,
)

bp = Blueprint("tarefas", __name__)

COLUNAS = (
    ("a_fazer", "A Fazer", "To Do"),
    ("em_progresso", "Em Progresso", "In Progress"),
    ("concluido", "Concluído", "Done"),
)

ROTULOS_PRIORIDADE = {
    "baixa": "Baixa",
    "media": "Média",
    "alta": "Alta",
    "critica": "Crítica",
}


@bp.get("/")
@login_obrigatorio
def quadro():
    """Exibe as tarefas do usuário agrupadas nas colunas do Kanban."""
    db = get_db()
    tarefas = repositorio.listar_tarefas(db, g.usuario["id"])

    colunas = []
    for status, rotulo, rotulo_github in COLUNAS:
        colunas.append(
            {
                "status": status,
                "rotulo": rotulo,
                "rotulo_github": rotulo_github,
                "tarefas": [t for t in tarefas if t["status"] == status],
            }
        )

    return render_template(
        "tarefas/quadro.html",
        colunas=colunas,
        prioridades=ROTULOS_PRIORIDADE,
        total=len(tarefas),
    )


@bp.route("/tarefas/nova", methods=("GET", "POST"))
@login_obrigatorio
def nova_tarefa():
    if request.method == "POST":
        try:
            titulo = validar_titulo(request.form.get("titulo"))
            descricao = validar_descricao(request.form.get("descricao"))
            prioridade = validar_prioridade(request.form.get("prioridade"))
            prazo = validar_prazo(request.form.get("prazo"))
        except ErroDeValidacao as erro:
            flash(str(erro), "erro")
        else:
            repositorio.criar_tarefa(
                get_db(), g.usuario["id"], titulo, descricao, prioridade, prazo
            )
            flash("Tarefa criada com sucesso.", "sucesso")
            return redirect(url_for("tarefas.quadro"))

    return render_template(
        "tarefas/formulario.html",
        tarefa=None,
        prioridades=ROTULOS_PRIORIDADE,
        acao="Nova tarefa",
    )


@bp.route("/tarefas/<int:tarefa_id>/editar", methods=("GET", "POST"))
@login_obrigatorio
def editar_tarefa(tarefa_id: int):
    db = get_db()
    tarefa = repositorio.obter_tarefa(db, tarefa_id, g.usuario["id"])
    if tarefa is None:
        abort(404)

    if request.method == "POST":
        try:
            titulo = validar_titulo(request.form.get("titulo"))
            descricao = validar_descricao(request.form.get("descricao"))
            prioridade = validar_prioridade(request.form.get("prioridade"))
            prazo = validar_prazo(request.form.get("prazo"))
        except ErroDeValidacao as erro:
            flash(str(erro), "erro")
        else:
            repositorio.atualizar_tarefa(
                db, tarefa_id, g.usuario["id"], titulo, descricao, prioridade, prazo
            )
            flash("Tarefa atualizada.", "sucesso")
            return redirect(url_for("tarefas.quadro"))

    return render_template(
        "tarefas/formulario.html",
        tarefa=tarefa,
        prioridades=ROTULOS_PRIORIDADE,
        acao="Editar tarefa",
    )


@bp.post("/tarefas/<int:tarefa_id>/status")
@login_obrigatorio
def mover_tarefa(tarefa_id: int):
    """Move a tarefa entre as colunas do Kanban."""
    db = get_db()
    if repositorio.obter_tarefa(db, tarefa_id, g.usuario["id"]) is None:
        abort(404)

    try:
        status = validar_status(request.form.get("status"))
    except ErroDeValidacao as erro:
        flash(str(erro), "erro")
    else:
        repositorio.atualizar_status(db, tarefa_id, g.usuario["id"], status)
        flash("Tarefa movida no quadro.", "sucesso")

    return redirect(url_for("tarefas.quadro"))


@bp.post("/tarefas/<int:tarefa_id>/excluir")
@login_obrigatorio
def excluir_tarefa(tarefa_id: int):
    db = get_db()
    if repositorio.obter_tarefa(db, tarefa_id, g.usuario["id"]) is None:
        abort(404)

    repositorio.excluir_tarefa(db, tarefa_id, g.usuario["id"])
    flash("Tarefa excluída.", "sucesso")
    return redirect(url_for("tarefas.quadro"))


@bp.get("/painel")
@login_obrigatorio
def painel():
    """Painel de desempenho da equipe (funcionalidade da mudança de escopo)."""
    dados = repositorio.metricas(get_db(), g.usuario["id"])
    return render_template(
        "tarefas/painel.html",
        metricas=dados,
        rotulos_prioridade=ROTULOS_PRIORIDADE,
        colunas=COLUNAS,
    )


@bp.get("/sobre")
def sobre():
    """Página pública com o objetivo do projeto e a metodologia adotada."""
    return render_template(
        "sobre.html",
        status_validos=STATUS_VALIDOS,
        prioridades_validas=PRIORIDADES_VALIDAS,
    )
