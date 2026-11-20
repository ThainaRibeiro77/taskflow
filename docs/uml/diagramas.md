# Diagramas UML do TaskFlow

Versões em imagem (para o documento teórico):
[`casos-de-uso.png`](casos-de-uso.png) e [`classes.png`](classes.png).


## 1. Diagrama de Casos de Uso

```mermaid
flowchart LR
    Visitante(("Visitante"))
    Usuario(("Usuário"))
    CI(("GitHub Actions"))

    subgraph SISTEMA["TaskFlow — Sistema de Gerenciamento de Tarefas"]
        UC1(["Criar conta"])
        UC2(["Autenticar-se (login/logout)"])
        UC3(["Consultar página Sobre"])
        UC4(["Consultar quadro Kanban"])
        UC5(["Criar tarefa"])
        UC6(["Editar tarefa"])
        UC7(["Mover tarefa no quadro"])
        UC8(["Excluir tarefa"])
        UC9(["Consultar painel de métricas"])
        UC10(["Validar dados de entrada"])
        UC11(["Executar testes automatizados"])
        UC12(["Análise estática do código"])
    end

    Visitante --> UC1
    Visitante --> UC2
    Visitante --> UC3
    Usuario --> UC4
    Usuario --> UC5
    Usuario --> UC6
    Usuario --> UC7
    Usuario --> UC8
    Usuario --> UC9
    CI --> UC11
    CI --> UC12

    UC1 -. "<<include>>" .-> UC10
    UC5 -. "<<include>>" .-> UC10
    UC6 -. "<<include>>" .-> UC10
```

## 2. Diagrama de Classes

```mermaid
classDiagram
    class Usuario {
        -int id
        -String nome
        -String email
        -String senha_hash
        -DateTime criado_em
        +autenticar(senha) bool
    }

    class Tarefa {
        -int id
        -int usuario_id
        -String titulo
        -String descricao
        -StatusTarefa status
        -Prioridade prioridade
        -Date prazo
        -DateTime criado_em
        -DateTime atualizado_em
        -DateTime concluido_em
        +moverPara(status) void
    }

    class StatusTarefa {
        <<enumeration>>
        A_FAZER
        EM_PROGRESSO
        CONCLUIDO
    }

    class Prioridade {
        <<enumeration>>
        BAIXA
        MEDIA
        ALTA
        CRITICA
    }

    class RepositorioTarefas {
        <<utility>>
        +criar_tarefa()
        +listar_tarefas()
        +obter_tarefa()
        +atualizar_tarefa()
        +atualizar_status()
        +excluir_tarefa()
        +metricas()
    }

    class Validacao {
        <<utility>>
        +validar_titulo()
        +validar_status()
        +validar_prioridade()
        +validar_prazo()
        +validar_email()
        +validar_senha()
    }

    class ErroDeValidacao {
        <<exception>>
        +String mensagem
    }

    Usuario "1" --> "0..*" Tarefa : possui
    Tarefa --> StatusTarefa
    Tarefa --> Prioridade
    RepositorioTarefas ..> Tarefa : persiste
    RepositorioTarefas ..> Validacao : usa
    Validacao ..> ErroDeValidacao : lança
```
