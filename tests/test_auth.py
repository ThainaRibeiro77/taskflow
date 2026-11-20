"""Testes de integração da autenticação (cadastro, login, sessão)."""

from conftest import cadastrar, entrar


def test_cadastro_com_sucesso(client):
    resposta = cadastrar(client)
    assert resposta.status_code == 200
    assert b"Conta criada com sucesso" in resposta.data


def test_cadastro_recusa_senha_curta(client):
    resposta = cadastrar(client, senha="123")
    assert b"8 caracteres" in resposta.data


def test_cadastro_recusa_email_duplicado(client):
    cadastrar(client)
    resposta = cadastrar(client, nome="Outra Pessoa", senha="outrasenha1")
    assert b"cadastrado" in resposta.data


def test_login_com_sucesso(client):
    cadastrar(client)
    resposta = entrar(client)
    assert b"Bem-vindo" in resposta.data
    assert b"Quadro de tarefas" in resposta.data


def test_login_com_senha_errada(client):
    cadastrar(client)
    resposta = entrar(client, senha="senhaerrada")
    assert b"senha inv" in resposta.data
    assert b"Quadro de tarefas" not in resposta.data


def test_login_com_email_inexistente(client):
    resposta = entrar(client, email="ninguem@exemplo.com")
    assert b"senha inv" in resposta.data


def test_rotas_privadas_exigem_login(client):
    resposta = client.get("/")
    assert resposta.status_code == 302
    assert "/login" in resposta.headers["Location"]

    assert client.get("/painel").status_code == 302
    assert client.get("/tarefas/nova").status_code == 302


def test_logout_encerra_a_sessao(client):
    cadastrar(client)
    entrar(client)
    resposta = client.post("/logout", follow_redirects=True)
    assert b"encerrada" in resposta.data
    assert client.get("/").status_code == 302


def test_sobre_e_publica(client):
    resposta = client.get("/sobre")
    assert resposta.status_code == 200
    assert b"TaskFlow" in resposta.data
