# Plano de commits semânticos

Convenção: [Conventional Commits](https://www.conventionalcommits.org/pt-br/).
Cada commit tem **um assunto** e referencia o card do Kanban (`#número da issue`).

| # | Mensagem do commit | Card | Arquivos principais |
| --- | --- | --- | --- |
| 1 | `chore: estrutura inicial do projeto e dependências` | TF-01 | `requirements*.txt`, `pyproject.toml`, `run.py`, `.gitignore` |
| 2 | `feat(db): esquema SQLite de usuários e tarefas` | TF-02 | `src/db.py` |
| 3 | `feat(validacao): regras de validação de tarefas e contas` | TF-05 | `src/validacao.py` |
| 4 | `feat(auth): cadastro e login com sessão e senha em hash` | TF-03 | `src/auth.py`, `templates/auth/*` |
| 5 | `feat(tarefas): CRUD de tarefas com isolamento por usuário` | TF-05, TF-06 | `src/repositorio.py`, `src/tarefas.py` |
| 6 | `feat(ui): quadro Kanban com colunas e transições de status` | TF-07, TF-08 | `templates/tarefas/quadro.html`, `static/style.css` |
| 7 | `test(validacao): testes unitários das regras de entrada` | TF-09 | `tests/test_validacao.py` |
| 8 | `test(auth): testes de cadastro, login e proteção de rotas` | TF-09 | `tests/test_auth.py`, `tests/conftest.py` |
| 9 | `test(tarefas): CRUD, isolamento entre usuários e métricas` | TF-09 | `tests/test_tarefas.py` |
| 10 | `ci: pipeline do GitHub Actions com ruff e pytest` | TF-10 | `.github/workflows/ci.yml` |
| 11 | `docs: README com objetivo, escopo, metodologia e instruções` | TF-01 | `README.md` |
| 12 | `docs: Plano de commits e diagramas UML` | TF-13 | `docs/*` |
| 13 | `feat(escopo): prioridade nas tarefas e ordenação por criticidade` | TF-15 | `src/validacao.py`, `src/repositorio.py`, templates |
| 14 | `feat(escopo): registrar conclusão e exibir painel de métricas` | TF-16, TF-17 | `src/repositorio.py`, `src/tarefas.py`, `templates/tarefas/painel.html` |
| 15 | `docs(escopo): justificar mudança de escopo no README e no Kanban` | TF-11, TF-13 | `README.md`, `docs/mudanca-de-escopo.md`, `docs/kanban.md` |

