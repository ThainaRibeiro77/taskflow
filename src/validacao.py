"""Regras de validação de entrada do TaskFlow.

Este módulo concentra validações *puras* (sem acesso a banco ou a HTTP),
o que torna as regras de negócio simples de testar com PyTest.
"""

from datetime import datetime

# Constantes de domínio usadas pela aplicação e pelos testes.
STATUS_VALIDOS = ("a_fazer", "em_progresso", "concluido")
PRIORIDADES_VALIDAS = ("baixa", "media", "alta", "critica")

TAMANHO_MAX_TITULO = 120
TAMANHO_MAX_DESCRICAO = 2000
TAMANHO_MIN_SENHA = 8


class ErroDeValidacao(ValueError):
    """Erro de regra de negócio (mensagem exibida ao usuário)."""


def validar_titulo(titulo: str | None) -> str:
    """Valida o título de uma tarefa: obrigatório e com tamanho limitado."""
    titulo = (titulo or "").strip()
    if not titulo:
        raise ErroDeValidacao("O título da tarefa é obrigatório.")
    if len(titulo) > TAMANHO_MAX_TITULO:
        raise ErroDeValidacao(
            f"O título deve ter no máximo {TAMANHO_MAX_TITULO} caracteres."
        )
    return titulo


def validar_descricao(descricao: str | None) -> str:
    """Normaliza a descrição (opcional), limitando o tamanho máximo."""
    descricao = (descricao or "").strip()
    if len(descricao) > TAMANHO_MAX_DESCRICAO:
        raise ErroDeValidacao(
            f"A descrição deve ter no máximo {TAMANHO_MAX_DESCRICAO} caracteres."
        )
    return descricao


def validar_status(status: str | None) -> str:
    """Garante que o status pertence ao fluxo Kanban."""
    status = (status or "").strip().lower()
    if status not in STATUS_VALIDOS:
        raise ErroDeValidacao(f"Status inválido: '{status}'.")
    return status


def validar_prioridade(prioridade: str | None) -> str:
    """Garante que a prioridade é uma das previstas (padrão: media)."""
    prioridade = (prioridade or "media").strip().lower()
    if prioridade not in PRIORIDADES_VALIDAS:
        raise ErroDeValidacao(f"Prioridade inválida: '{prioridade}'.")
    return prioridade


def validar_prazo(prazo: str | None) -> str | None:
    """Valida a data limite opcional no formato AAAA-MM-DD."""
    prazo = (prazo or "").strip()
    if not prazo:
        return None
    try:
        datetime.strptime(prazo, "%Y-%m-%d")
    except ValueError as exc:
        raise ErroDeValidacao(
            "O prazo deve estar no formato AAAA-MM-DD."
        ) from exc
    return prazo


def validar_nome(nome: str | None) -> str:
    """Valida o nome do usuário."""
    nome = (nome or "").strip()
    if len(nome) < 2:
        raise ErroDeValidacao("Informe um nome com pelo menos 2 caracteres.")
    return nome


def validar_email(email: str | None) -> str:
    """Validação simplificada de e-mail (formato básico)."""
    email = (email or "").strip().lower()
    if "@" not in email or "." not in email.split("@")[-1] or " " in email:
        raise ErroDeValidacao("Informe um endereço de e-mail válido.")
    return email


def validar_senha(senha: str | None) -> str:
    """Valida a senha: mínimo de 8 caracteres."""
    senha = senha or ""
    if len(senha) < TAMANHO_MIN_SENHA:
        raise ErroDeValidacao(
            f"A senha deve ter no mínimo {TAMANHO_MIN_SENHA} caracteres."
        )
    return senha
