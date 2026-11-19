"""Conexão e esquema do banco de dados SQLite.

Usamos o driver `sqlite3` da biblioteca padrão para manter o projeto
leve: nenhum servidor de banco é necessário para rodar ou testar.
"""

import sqlite3

from flask import current_app, g

ESQUEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT    NOT NULL,
    email       TEXT    NOT NULL UNIQUE,
    senha_hash  TEXT    NOT NULL,
    criado_em   TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tarefas (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id    INTEGER NOT NULL REFERENCES usuarios (id) ON DELETE CASCADE,
    titulo        TEXT    NOT NULL,
    descricao     TEXT    NOT NULL DEFAULT '',
    status        TEXT    NOT NULL DEFAULT 'a_fazer',
    prioridade    TEXT    NOT NULL DEFAULT 'media',
    prazo         TEXT,
    criado_em     TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    concluido_em  TEXT
);

CREATE INDEX IF NOT EXISTS idx_tarefas_usuario ON tarefas (usuario_id);
"""


def get_db() -> sqlite3.Connection:
    """Retorna (e reaproveita) a conexão da requisição atual."""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def fechar_db(_erro=None) -> None:
    """Fecha a conexão ao final da requisição."""
    conexao = g.pop("db", None)
    if conexao is not None:
        conexao.close()


def criar_esquema() -> None:
    """Cria as tabelas se ainda não existirem."""
    db = get_db()
    db.executescript(ESQUEMA)
    db.commit()


def init_app(app) -> None:
    """Registra o fechamento de conexão e cria o esquema na inicialização."""
    app.teardown_appcontext(fechar_db)
    with app.app_context():
        criar_esquema()
