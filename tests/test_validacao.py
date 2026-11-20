"""Testes unitários das regras de validação (sem banco e sem HTTP)."""

import pytest

from src.validacao import (
    ErroDeValidacao,
    validar_descricao,
    validar_email,
    validar_nome,
    validar_prazo,
    validar_prioridade,
    validar_senha,
    validar_status,
    validar_titulo,
)


class TestTitulo:
    def test_titulo_valido_e_normalizado(self):
        assert validar_titulo("  Revisar cargas  ") == "Revisar cargas"

    @pytest.mark.parametrize("entrada", ["", "   ", None])
    def test_titulo_obrigatorio(self, entrada):
        with pytest.raises(ErroDeValidacao, match="obrigatório"):
            validar_titulo(entrada)

    def test_titulo_muito_longo(self):
        with pytest.raises(ErroDeValidacao, match="120"):
            validar_titulo("x" * 121)


class TestStatusEPrioridade:
    @pytest.mark.parametrize("status", ["a_fazer", "em_progresso", "concluido"])
    def test_status_validos(self, status):
        assert validar_status(status) == status

    def test_status_invalido(self):
        with pytest.raises(ErroDeValidacao, match="Status inválido"):
            validar_status("arquivado")

    @pytest.mark.parametrize("prioridade", ["baixa", "media", "alta", "critica"])
    def test_prioridades_validas(self, prioridade):
        assert validar_prioridade(prioridade) == prioridade

    def test_prioridade_padrao(self):
        assert validar_prioridade(None) == "media"

    def test_prioridade_invalida(self):
        with pytest.raises(ErroDeValidacao, match="Prioridade inválida"):
            validar_prioridade("urgentissima")


class TestPrazo:
    def test_prazo_vazio_vira_none(self):
        assert validar_prazo("") is None

    def test_prazo_valido(self):
        assert validar_prazo("2026-12-01") == "2026-12-01"

    def test_prazo_em_formato_errado(self):
        with pytest.raises(ErroDeValidacao, match="AAAA-MM-DD"):
            validar_prazo("01/12/2026")


class TestDadosDeConta:
    def test_email_normalizado(self):
        assert validar_email("  Ana@Exemplo.COM ") == "ana@exemplo.com"

    @pytest.mark.parametrize("email", ["ana", "ana@exemplo", "ana exemplo@x.com"])
    def test_email_invalido(self, email):
        with pytest.raises(ErroDeValidacao, match="e-mail válido"):
            validar_email(email)

    def test_senha_curta(self):
        with pytest.raises(ErroDeValidacao, match="8 caracteres"):
            validar_senha("1234567")

    def test_senha_valida(self):
        assert validar_senha("senha1234") == "senha1234"

    def test_nome_curto(self):
        with pytest.raises(ErroDeValidacao, match="2 caracteres"):
            validar_nome("A")


class TestDescricao:
    def test_descricao_opcional(self):
        assert validar_descricao(None) == ""

    def test_descricao_muito_longa(self):
        with pytest.raises(ErroDeValidacao, match="2000"):
            validar_descricao("d" * 2001)
