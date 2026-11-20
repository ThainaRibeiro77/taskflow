"""Fábrica da aplicação Flask (`create_app`).

O padrão *application factory* permite criar instâncias isoladas para os
testes automatizados, cada uma com seu próprio banco temporário.
"""

import os

from flask import Flask

from . import db
from .auth import bp as auth_bp
from .tarefas import bp as tarefas_bp


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "chave-de-desenvolvimento"),
        DATABASE=os.environ.get("TASKFLOW_DB", os.path.join(os.getcwd(), "taskflow.sqlite3")),
    )

    if config is not None:
        app.config.update(config)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(tarefas_bp)

    return app
