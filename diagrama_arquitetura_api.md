# 🏗️ DIAGRAMA DA ARQUITETURA API HETZNER

```mermaid
graph TB
    %% Frontend Layer
    subgraph "🌐 FRONTEND (Webflow)"
        A[Formulário de Cotação] --> B[JavaScript Injetado]
        B --> C[Coleta de Dados]
        C --> D[Validação Local]
    end
    
    %% API Layer
    subgraph "🖥️ API HETZNER (37.27.92.160)"
        E[start.php] --> F[Validação de Campos]
        F --> G[Geração Session ID]
        G --> H[Consulta PH3A]
        H --> I[Execução Webhooks]
        I --> J[Inicialização RPA]
        
        K[get_progress.php] --> L[Leitura Progress JSON]
        L --> M[Retorno Status]
    end
    
    %% RPA Layer
    subgraph "🤖 RPA PYTHON"
        N[executar_rpa_imediato_playwright.py] --> O[15 Telas Sequenciais]
        O --> P[Progress Tracker]
        P --> Q[Captura de Dados]
        Q --> R[Tratamento de Erros]
    end
    
    %% External Services
    subgraph "🌍 SERVIÇOS EXTERNOS"
        S[API PH3A] --> T[Validação CPF]
        U[Webhooks MDMIDIA] --> V[Integração CRM]
    end
    
    %% Data Storage
    subgraph "💾 ARMAZENAMENTO"
        W[Progress JSON Files] --> X[rpa_data/progress_*.json]
        Y[Session Files] --> Z[sessions/{id}/status.json]
        AA[Logs] --> BB[logs/rpa_*.log]
    end
    
    %% Connections
    D -->|POST /api/rpa/start| E
    E -->|GET /get_progress.php| K
    K -->|Polling 2s| B
    
    H -->|HTTP Request| S
    I -->|HTTP Request| U
    
    J -->|Background Process| N
    P -->|Write| W
    P -->|Write| Y
    R -->|Write| AA
    
    %% Styling
    classDef frontend fill:#e1f5fe
    classDef api fill:#f3e5f5
    classDef rpa fill:#e8f5e8
    classDef external fill:#fff3e0
    classDef storage fill:#fce4ec
    
    class A,B,C,D frontend
    class E,F,G,H,I,J,K,L,M api
    class N,O,P,Q,R rpa
    class S,T,U,V external
    class W,X,Y,Z,AA,BB storage
```

## 🔄 FLUXO DETALHADO DE EXECUÇÃO

```mermaid
sequenceDiagram
    participant U as 👤 Usuário
    participant F as 🌐 Frontend
    participant A as 🖥️ API Hetzner
    participant P as 📞 PH3A
    participant W as 🔗 Webhooks
    participant R as 🤖 RPA Python
    participant D as 💾 Dados
    
    U->>F: Preenche formulário
    F->>F: Valida dados localmente
    F->>A: POST /api/rpa/start
    
    A->>A: Valida campos obrigatórios
    A->>A: Gera session_id único
    
    alt Campos PH3A vazios
        A->>P: Consulta CPF
        P-->>A: Dados pessoais
        A->>A: Preenche campos
    end
    
    A->>W: Dispara webhooks
    W-->>A: Confirmação
    
    A->>R: Executa RPA em background
    A-->>F: Retorna session_id
    
    F->>F: Abre modal de progresso
    F->>A: GET /get_progress.php?session={id}
    
    loop A cada 2 segundos
        A->>D: Lê progress_{session_id}.json
        D-->>A: Dados de progresso
        A-->>F: Status atualizado
        F->>F: Atualiza modal
        
        alt RPA concluído
            F->>F: Exibe resultados finais
            F->>U: Mostra estimativas
        end
    end
```

## 📊 ESTRUTURA DE DADOS

```mermaid
graph LR
    subgraph "📥 INPUT"
        A[Formulário Webflow] --> B[JSON Request]
    end
    
    subgraph "🔄 PROCESSAMENTO"
        C[Validação PHP] --> D[Consulta PH3A]
        D --> E[Webhooks MDMIDIA]
        E --> F[Inicialização RPA]
    end
    
    subgraph "📤 OUTPUT"
        G[Session ID] --> H[Progress JSON]
        H --> I[Status Updates]
        I --> J[Resultados Finais]
    end
    
    B --> C
    F --> G
```

## 🚨 PONTOS CRÍTICOS

```mermaid
graph TD
    A[🚨 PROBLEMAS IDENTIFICADOS] --> B[⏱️ Timeout 3min → 10s]
    A --> C[❌ Lógica de Erro Incorreta]
    A --> D[🔧 Métodos Progress Tracker]
    A --> E[📁 Versão Desatualizada]
    
    B --> F[✅ CORREÇÕES APLICADAS]
    C --> F
    D --> F
    E --> G[📤 PRÓXIMO: Upload Hetzner]
    
    F --> H[🎯 SISTEMA FUNCIONANDO]
    G --> H
```
