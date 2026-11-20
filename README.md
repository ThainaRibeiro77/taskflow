# TaskFlow — Sistema Ágil de Gerenciamento de Tarefas

Sistema web de gerenciamento de tarefas com quadro Kanban, desenvolvido como
projeto final da disciplina de **Engenharia de Software**.

O projeto simula o trabalho da **TechFlow Solutions**, contratada por uma startup
de logística para entregar uma ferramenta capaz de (1) acompanhar o fluxo de
trabalho em tempo real, (2) priorizar tarefas críticas e (3) monitorar o
desempenho da equipe.

---

## Sumário

- [Objetivo e escopo](#objetivo-e-escopo)
- [Funcionalidades](#funcionalidades)
- [Metodologia ágil adotada](#metodologia-ágil-adotada)
- [Tecnologias](#tecnologias)
- [Estrutura de diretórios](#estrutura-de-diretórios)
- [Como executar o projeto](#como-executar-o-projeto)
- [Testes automatizados](#testes-automatizados)
- [Integração contínua (GitHub Actions)](#integração-contínua-github-actions)
- [Kanban (GitHub Projects)](#kanban-github-projects)
- [Histórico de commits](#histórico-de-commits)
- [Mudança de escopo](#mudança-de-escopo)
- [Decisões de arquitetura](#decisões-de-arquitetura)
- [Autores](#autores)

---

## Objetivo e escopo

O **TaskFlow** permite que uma pessoa da equipe crie tarefas, organize-as em um
fluxo Kanban e acompanhe indicadores de produtividade. O objetivo é reduzir dois
problemas clássicos de projetos ágeis: **falta de visibilidade** do andamento e
**priorização informal** (o famoso "tudo é urgente").

**Escopo inicial (Sprint 1 e 2)**

- Cadastro e login de usuários com senha protegida por hash.
- CRUD completo de tarefas (criar, listar, editar, mover e excluir).
- Quadro com as colunas **A Fazer**, **Em Progresso** e **Concluído**.
- Isolamento de dados: cada usuário enxerga apenas as próprias tarefas.

**Fora de escopo**

- Multiusuário colaborativo em um mesmo quadro (equipes compartilhadas).
- Notificações por e-mail, anexos e aplicativo mobile.
- Integrações externas (ERP, transportadoras).

## Funcionalidades

| Requisito | Descrição | Onde está no código |
| --- | --- | --- |
| RF01 | Cadastro de usuário com validação de nome, e-mail e senha (mín. 8 caracteres) | `src/auth.py`, `src/validacao.py` |
| RF02 | Login/logout com sessão e senha em hash (`werkzeug`) | `src/auth.py` |
| RF03 | Criar tarefa com título, descrição, prioridade e prazo | `src/tarefas.py` |
| RF04 | Listar tarefas no quadro Kanban por coluna | `src/tarefas.py`, `templates/tarefas/quadro.html` |
| RF05 | Editar tarefa | `src/tarefas.py` |
| RF06 | Mover tarefa entre colunas | `src/tarefas.py` |
| RF07 | Excluir tarefa | `src/tarefas.py` |
| RF08 | Prioridade: baixa, média, alta e crítica | `src/validacao.py` |
| RF09 | Painel de métricas (taxa de conclusão, atrasos, throughput de 7 dias) | `src/repositorio.py`, `templates/tarefas/painel.html` |
| RF10 | Controle de acesso: rotas privadas exigem login | `src/auth.py` |

## Metodologia ágil adotada

Modelo **híbrido Scrum + Kanban**, adequado a um time pequeno:

- **Sprints de 1 semana**, com planejamento na segunda e revisão na sexta.
- **Kanban** no GitHub Projects como fonte única de verdade: cada card é um item
  de trabalho com critério de aceite, etiqueta de prioridade e vínculo com o
  commit/PR que o implementa.
- **Definition of Done**: código revisado, teste automatizado cobrindo o
  comportamento e pipeline verde no GitHub Actions.
- **Commits semânticos** (`feat:`, `fix:`, `test:`, `docs:`, `ci:`), um assunto por
  commit, referenciando o card correspondente.

Cerimônias registradas no repositório: planejamento (issues), *daily* assíncrona
(comentários nos cards) e retrospectiva (seção de mudança de escopo abaixo).

## Tecnologias

- **Python 3.10+** e **Flask 3** (rotas, sessão, templates Jinja).
- **SQLite** (biblioteca padrão `sqlite3`) — zero configuração para rodar/avaliar.
- **PyTest** + **pytest-cov** para testes automatizados e cobertura.
- **Ruff** para análise estática (estilo e erros comuns).
- **GitHub Actions** para integração contínua.
- **HTML + CSS** puro (sem build de front-end), layout responsivo.

## Estrutura de diretórios

```
taskflow/
├── .github/
│   └── workflows/
│       └── ci.yml              # pipeline de CI (ruff + pytest)
├── docs/
│   ├── kanban.md               # cards e colunas do GitHub Projects
│   ├── commits.md              # plano de commits semânticos
│   ├── mudanca-de-escopo.md    # análise da mudança de escopo
│   ├── prints-github.md        # roteiro das evidências (prints)
│   └── uml/                    # diagramas de casos de uso e de classes
├── src/
│   ├── __init__.py
│   ├── app.py                  # application factory
│   ├── auth.py                 # cadastro, login, logout, decorators
│   ├── db.py                   # conexão e esquema SQLite
│   ├── repositorio.py          # consultas SQL e métricas
│   ├── tarefas.py              # quadro Kanban, CRUD e painel
│   ├── validacao.py            # regras de validação (testáveis isoladamente)
│   ├── static/style.css
│   └── templates/              # Jinja2 (base, auth, tarefas)
├── tests/
│   ├── conftest.py             # fixtures (app isolada + helpers)
│   ├── test_auth.py
│   ├── test_tarefas.py
│   └── test_validacao.py
├── pyproject.toml              # configuração de pytest, coverage e ruff
├── requirements.txt
├── requirements-dev.txt
└── run.py
```

## Como executar o projeto

Pré-requisitos: Python 3.10 ou superior e Git.

```bash
# 1. Clone o repositório
git clone https://github.com/SEU-USUARIO/taskflow.git
cd taskflow

# 2. Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements-dev.txt

# 4. Rode a aplicação
python run.py
```

Acesse <http://127.0.0.1:5000>, crie uma conta em **Criar conta** e comece a
cadastrar tarefas. O banco `taskflow.sqlite3` é criado automaticamente na primeira
execução (ele está no `.gitignore`).

> **Aviso:** a `SECRET_KEY` padrão serve apenas para desenvolvimento. Em produção,
> defina a variável de ambiente `SECRET_KEY` com um valor aleatório.

## Testes automatizados

```bash
pytest                                          # suíte completa
pytest --cov=src --cov-report=term-missing      # com cobertura
ruff check .                                    # análise estática
```

A suíte cobre três níveis:

1. **Unitário** (`tests/test_validacao.py`) — regras de entrada: título
   obrigatório/limite de tamanho, status e prioridade do domínio, formato de prazo,
   e-mail e senha.
2. **Integração HTTP** (`tests/test_auth.py`) — cadastro, e-mail duplicado, senha
   curta, login válido/inválido, logout e bloqueio de rotas privadas.
3. **Integração de negócio** (`tests/test_tarefas.py`) — CRUD, movimentação no
   quadro, exclusão, **isolamento entre usuários** (usuário B recebe 404 ao tentar
   acessar tarefa do usuário A) e cálculo das métricas do painel.

Cada teste roda contra um banco SQLite temporário próprio, criado pela fixture
`app` (`tests/conftest.py`), então nada é compartilhado entre execuções.

## Integração contínua (GitHub Actions)

O workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) dispara em todo
`push` e `pull_request` para a branch `main` e executa, em um runner Ubuntu com
Python 3.12:

1. Instalação das dependências (`requirements-dev.txt`).
2. `ruff check .` — análise estática.
3. `pytest --cov=src --cov-fail-under=80` — testes com cobertura mínima de 80%.

Se qualquer etapa falhar, o merge é bloqueado pela regra de proteção da branch
`main` (*Require status checks to pass before merging*).


## Mudança de escopo

Durante a Sprint 3, o cliente (startup de logística) solicitou **priorização de
tarefas críticas e acompanhamento de desempenho**, alegando que o quadro sozinho
não respondia "o que atacar primeiro" nem "como estamos performando".

A mudança foi aceita porque era **pequena, incremental e não quebrava o que já
existia**. Ela adicionou:

- campo `prioridade` (baixa, média, alta, crítica) com ordenação automática no quadro;
- campo `concluido_em` para medir throughput;
- página **/painel** com taxa de conclusão, tarefas em atraso e concluídas nos
  últimos 7 dias;
- 3 novos cards no Kanban e 4 novos commits.

Justificativa completa, análise de impacto e registro da decisão:
[`docs/mudanca-de-escopo.md`](docs/mudanca-de-escopo.md).

## Decisões de arquitetura

- **Application factory** (`create_app`): permite instanciar a aplicação com
  configurações diferentes — essencial para os testes usarem banco temporário.
- **Validação isolada** (`validacao.py`): regras de negócio puras, sem Flask,
  testáveis em milissegundos e reutilizáveis por qualquer camada.
- **SQLite**: elimina dependência de servidor externo e garante que o avaliador
  consiga rodar o projeto com um único comando.
- **Sem ORM**: o SQL explícito deixa visível o filtro por `usuario_id`, que é o
  mecanismo de isolamento de dados entre contas.
- **HTML/Jinja sem framework JS**: menos peças móveis, mais fácil de explicar no
  vídeo pitch.

## Autores

- **Thaina Fernandes Ribeiro** — desenvolvimento, testes e documentação, kanban, revisão e vídeo pitch

Disciplina: Engenharia de Software
