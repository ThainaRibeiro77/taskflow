"""Consultas SQL da aplicação (usuários, tarefas e métricas).

Manter o SQL isolado aqui deixa as rotas Flask curtas e os testes
independentes da camada web.
"""

from datetime import date, datetime, timedelta

from .validacao import PRIORIDADES_VALIDAS, STATUS_VALIDOS

# ---------------------------------------------------------------- usuários


def criar_usuario(db, nome, email, senha_hash) -> int:
    cursor = db.execute(
        "INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
        (nome, email, senha_hash),
    )
    db.commit()
    return cursor.lastrowid


def buscar_usuario_por_email(db, email):
    return db.execute(
        "SELECT * FROM usuarios WHERE email = ?", (email,)
    ).fetchone()


def buscar_usuario_por_id(db, usuario_id):
    return db.execute(
        "SELECT * FROM usuarios WHERE id = ?", (usuario_id,)
    ).fetchone()


# ---------------------------------------------------------------- tarefas


def criar_tarefa(db, usuario_id, titulo, descricao="", prioridade="media", prazo=None):
    cursor = db.execute(
        """
        INSERT INTO tarefas (usuario_id, titulo, descricao, prioridade, prazo)
        VALUES (?, ?, ?, ?, ?)
        """,
        (usuario_id, titulo, descricao, prioridade, prazo),
    )
    db.commit()
    return cursor.lastrowid


def listar_tarefas(db, usuario_id, status=None, prioridade=None):
    """Lista as tarefas do usuário, opcionalmente filtradas."""
    sql = "SELECT * FROM tarefas WHERE usuario_id = ?"
    parametros = [usuario_id]
    if status:
        sql += " AND status = ?"
        parametros.append(status)
    if prioridade:
        sql += " AND prioridade = ?"
        parametros.append(prioridade)
    # Prioridade crítica sobe no quadro, seguida do prazo mais próximo.
    sql += """
        ORDER BY CASE prioridade
                    WHEN 'critica' THEN 1
                    WHEN 'alta'    THEN 2
                    WHEN 'media'   THEN 3
                    ELSE 4
                 END,
                 CASE WHEN prazo IS NULL THEN 1 ELSE 0 END,
                 prazo,
                 id DESC
    """
    return db.execute(sql, parametros).fetchall()


def obter_tarefa(db, tarefa_id, usuario_id):
    """Busca uma tarefa garantindo que pertence ao usuário logado."""
    return db.execute(
        "SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?",
        (tarefa_id, usuario_id),
    ).fetchone()


def atualizar_tarefa(db, tarefa_id, usuario_id, titulo, descricao, prioridade, prazo):
    db.execute(
        """
        UPDATE tarefas
           SET titulo = ?, descricao = ?, prioridade = ?, prazo = ?,
               atualizado_em = CURRENT_TIMESTAMP
         WHERE id = ? AND usuario_id = ?
        """,
        (titulo, descricao, prioridade, prazo, tarefa_id, usuario_id),
    )
    db.commit()


def atualizar_status(db, tarefa_id, usuario_id, status):
    """Move a tarefa no Kanban e registra a data de conclusão."""
    agora = datetime.now().isoformat(timespec="seconds")
    if status == "concluido":
        db.execute(
            """
            UPDATE tarefas
               SET status = ?, atualizado_em = CURRENT_TIMESTAMP, concluido_em = ?
             WHERE id = ? AND usuario_id = ?
            """,
            (status, agora, tarefa_id, usuario_id),
        )
    else:
        db.execute(
            """
            UPDATE tarefas
               SET status = ?, atualizado_em = CURRENT_TIMESTAMP, concluido_em = NULL
             WHERE id = ? AND usuario_id = ?
            """,
            (status, tarefa_id, usuario_id),
        )
    db.commit()


def excluir_tarefa(db, tarefa_id, usuario_id) -> None:
    db.execute(
        "DELETE FROM tarefas WHERE id = ? AND usuario_id = ?",
        (tarefa_id, usuario_id),
    )
    db.commit()


# ---------------------------------------------------------------- métricas


def metricas(db, usuario_id) -> dict:
    """Indicadores do painel de desempenho (funcionalidade do escopo novo)."""
    contagem = db.execute(
        "SELECT COUNT(*) AS total FROM tarefas WHERE usuario_id = ?", (usuario_id,)
    ).fetchone()["total"]

    por_status = {status: 0 for status in STATUS_VALIDOS}
    for linha in db.execute(
        "SELECT status, COUNT(*) AS qtd FROM tarefas WHERE usuario_id = ? GROUP BY status",
        (usuario_id,),
    ):
        if linha["status"] in por_status:
            por_status[linha["status"]] = linha["qtd"]

    por_prioridade = {prioridade: 0 for prioridade in PRIORIDADES_VALIDAS}
    for linha in db.execute(
        """
        SELECT prioridade, COUNT(*) AS qtd
          FROM tarefas
         WHERE usuario_id = ? AND status != 'concluido'
      GROUP BY prioridade
        """,
        (usuario_id,),
    ):
        if linha["prioridade"] in por_prioridade:
            por_prioridade[linha["prioridade"]] = linha["qtd"]

    hoje = date.today().isoformat()
    atrasadas = db.execute(
        """
        SELECT COUNT(*) AS qtd
          FROM tarefas
         WHERE usuario_id = ? AND status != 'concluido'
           AND prazo IS NOT NULL AND prazo < ?
        """,
        (usuario_id, hoje),
    ).fetchone()["qtd"]

    limite = (datetime.now() - timedelta(days=7)).isoformat(timespec="seconds")
    concluidas_7_dias = db.execute(
        """
        SELECT COUNT(*) AS qtd
          FROM tarefas
         WHERE usuario_id = ? AND status = 'concluido' AND concluido_em >= ?
        """,
        (usuario_id, limite),
    ).fetchone()["qtd"]

    taxa_conclusao = round(por_status["concluido"] / contagem * 100) if contagem else 0

    return {
        "total": contagem,
        "por_status": por_status,
        "por_prioridade": por_prioridade,
        "atrasadas": atrasadas,
        "concluidas_7_dias": concluidas_7_dias,
        "taxa_conclusao": taxa_conclusao,
    }
