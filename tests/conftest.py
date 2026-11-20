"""Fixtures compartilhadas pela suíte de testes."""

import pytest

from src import create_app


@pytest.fixture()
def app(tmp_path):
    """Cria uma instância isolada da aplicação com banco temporário."""
    aplicacao = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "chave-de-teste",
            "DATABASE": str(tmp_path / "teste.sqlite3"),
        }
    )
    yield aplicacao


@pytest.fixture()
def client(app):
    """Cliente HTTP de teste do Flask."""
    return app.test_client()


def cadastrar(client, nome="Ana Souza", email="ana@exemplo.com", senha="senha1234"):
    """Helper: cadastra um usuário pela rota real de cadastro."""
    return client.post(
        "/cadastro",
        data={"nome": nome, "email": email, "senha": senha},
        follow_redirects=True,
    )


def entrar(client, email="ana@exemplo.com", senha="senha1234"):
    """Helper: autentica o cliente de teste."""
    return client.post(
        "/login",
        data={"email": email, "senha": senha},
        follow_redirects=True,
    )


def criar_tarefa(
    client,
    titulo="Organizar entregas",
    descricao="Separar as rotas do dia",
    prioridade="alta",
    prazo="",
):
    """Helper: cria uma tarefa pela rota real de criação."""
    return client.post(
        "/tarefas/nova",
        data={
            "titulo": titulo,
            "descricao": descricao,
            "prioridade": prioridade,
            "prazo": prazo,
        },
        follow_redirects=True,
    )
