"""Testes de integração do CRUD de tarefas e do painel de métricas."""

from conftest import cadastrar, criar_tarefa, entrar


def _preparar_sessao(client):
    cadastrar(client)
    entrar(client)


def test_criar_tarefa_e_ver_no_quadro(client):
    _preparar_sessao(client)
    resposta = criar_tarefa(client, titulo="Despachar pedido 1042")
    assert b"Tarefa criada com sucesso" in resposta.data
    assert b"Despachar pedido 1042" in resposta.data


def test_criar_tarefa_sem_titulo_e_recusado(client):
    _preparar_sessao(client)
    resposta = criar_tarefa(client, titulo="   ")
    assert b"obrigat" in resposta.data


def test_criar_tarefa_com_prioridade_invalida(client):
    _preparar_sessao(client)
    resposta = criar_tarefa(client, prioridade="urgentissima")
    assert b"Prioridade inv" in resposta.data


def test_criar_tarefa_com_prazo_invalido(client):
    _preparar_sessao(client)
    resposta = criar_tarefa(client, prazo="31/12/2026")
    assert b"AAAA-MM-DD" in resposta.data


def test_mover_tarefa_no_quadro(client):
    _preparar_sessao(client)
    criar_tarefa(client, titulo="Conferir estoque")

    resposta = client.post(
        "/tarefas/1/status", data={"status": "concluido"}, follow_redirects=True
    )
    assert b"Tarefa movida no quadro" in resposta.data

    resposta = client.post(
        "/tarefas/1/status", data={"status": "arquivado"}, follow_redirects=True
    )
    assert b"Status inv" in resposta.data


def test_editar_tarefa(client):
    _preparar_sessao(client)
    criar_tarefa(client, titulo="Rota antiga")

    resposta = client.post(
        "/tarefas/1/editar",
        data={
            "titulo": "Rota nova",
            "descricao": "Atualizada",
            "prioridade": "critica",
            "prazo": "2026-12-20",
        },
        follow_redirects=True,
    )
    assert b"Tarefa atualizada" in resposta.data
    assert b"Rota nova" in resposta.data
    assert b"prioridade-critica" in resposta.data


def test_excluir_tarefa(client):
    _preparar_sessao(client)
    criar_tarefa(client, titulo="Tarefa descartavel")

    resposta = client.post("/tarefas/1/excluir", follow_redirects=True)
    assert b"Tarefa exclu" in resposta.data
    assert b"Tarefa descartavel" not in resposta.data


def test_tarefa_inexistente_retorna_404(client):
    _preparar_sessao(client)
    assert client.get("/tarefas/999/editar").status_code == 404


def test_usuario_nao_acessa_tarefa_de_outro(client):
    # Usuária A cria uma tarefa.
    _preparar_sessao(client)
    criar_tarefa(client, titulo="Tarefa privada da Ana")

    # Usuário B se cadastra e entra.
    client.post("/logout")
    cadastrar(client, nome="Bruno Lima", email="bruno@exemplo.com", senha="senha1234")
    entrar(client, email="bruno@exemplo.com")

    assert client.get("/tarefas/1/editar").status_code == 404
    assert client.post("/tarefas/1/excluir").status_code == 404
    assert client.post("/tarefas/1/status", data={"status": "concluido"}).status_code == 404

    resposta = client.get("/")
    assert b"Tarefa privada da Ana" not in resposta.data


def test_painel_mostra_metricas(client):
    _preparar_sessao(client)
    criar_tarefa(client, titulo="Tarefa 1", prioridade="critica")
    criar_tarefa(client, titulo="Tarefa 2", prioridade="baixa")
    criar_tarefa(client, titulo="Tarefa 3", prioridade="media")

    client.post("/tarefas/1/status", data={"status": "concluido"})

    resposta = client.get("/painel")
    assert resposta.status_code == 200
    assert "Taxa de conclusão".encode() in resposta.data
    assert b"33%" in resposta.data
