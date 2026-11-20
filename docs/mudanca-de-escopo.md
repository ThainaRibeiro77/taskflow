# Registro de mudança de escopo — Sprint 3

## Contexto

Ao final da Sprint 2, o quadro Kanban já funcionava: criar, editar, mover e
excluir tarefas. Na revisão da sprint, a *product owner* da startup de logística
apresentou dois problemas do dia a dia da operação:

1. **"Tudo parece urgente."** Sem prioridade explícita, a equipe escolhia o que
   fazer primeiro por memória ou por quem reclamava mais alto.
2. **"Não sei se estamos melhorando."** Havia visibilidade do *agora*, mas não do
   *desempenho*: quantas tarefas são concluídas por semana, quantas estão atrasadas.

## Solicitação do cliente

> "Precisamos saber o que atacar primeiro e como estamos performando ao longo das
> semanas." — *Product Owner, reunião de revisão da Sprint 2*

## Decisão

A solicitação foi aceita como **mudança de escopo da Sprint 3**, porque:

- é **incremental**: usa a mesma tabela `tarefas`, sem reescrever o que existe;
- é **pequena**: dois campos e uma tela;
- gera **valor direto** para os dois problemas relatados;
- não compromete o prazo (cabia em uma sprint de uma semana).

A decisão foi registrada na retro da Sprint 2 e comunicada no quadro com três
novos cards (`TF-15`, `TF-16`, `TF-17`), mantendo os cards anteriores intactos.

## O que entrou no escopo

| Item | Antes | Depois |
| --- | --- | --- |
| Prioridade da tarefa | não existia | `baixa`, `media`, `alta`, `critica`, com ordenação automática no quadro |
| Data de conclusão | não existia | campo `concluido_em`, preenchido ao mover para "Concluído" e limpo ao reabrir |
| Indicadores | só o quadro | página `/painel`: total, taxa de conclusão, atrasos e throughput dos últimos 7 dias |

## O que **não** entrou (e por quê)

- **Comentários nas tarefas**: exigiria nova tabela e tela; ficou para o backlog.
- **Notificações por e-mail**: dependeria de serviço externo e credenciais.
- **Multiusuário no mesmo quadro**: mudaria o modelo de permissões (escopo grande,
  risco alto para o prazo).
- **Relatórios exportáveis (CSV/PDF)**: valor secundário nesta fase.

Essas recusas foram registradas para mostrar que nem toda solicitação entra no
sprint — o backlog é priorizado, não acumulado.

## Impacto técnico

- Banco: duas colunas novas (`prioridade`, `concluido_em`) e índices mantidos.
- Regras: `validar_prioridade()` em `src/validacao.py`.
- Consultas: ordenação por criticidade e prazo em `listar_tarefas()`; cálculo dos
  indicadores em `metricas()`.
- Interface: novo `<select>` de prioridade no formulário, etiqueta no card e uma
  página de painel.
- Testes: casos novos para prioridade inválida e para o cálculo da taxa de
  conclusão (o pipeline continua verde).
- Documentação: esta página, seção "Mudança de escopo" no `README.md` e três
  cards novos no Kanban.

## Impacto no processo

- **Kanban**: 3 cards criados em `To Do`, movidos para `In Progress` e depois
  `Done`; os cards da Sprint 1/2 não foram reabertos.
- **Commits**: `feat(escopo)...` (2 commits de código) + `docs(escopo)...`
  (1 commit de documentação).
- **Prazo**: absorvido na Sprint 3; a entrega do núcleo do sistema não atrasou.

## Lição aprendida (retrospectiva)

Mudanças pequenas e bem justificadas fortalecem o produto; o perigo está em
mudanças sem critério e sem registro. O combinado do time passou a ser: **toda
mudança de escopo entra como card, com justificativa escrita e análise de impacto**
— exatamente o que este documento faz.
