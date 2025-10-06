# 📋 ESPECIFICAÇÃO TÉCNICA COMPLETA - MODAL SEPARADO V6.2.0

## 🎯 DOCUMENTO PARA ENGENHEIRO DE SOFTWARE

**Data**: 04 de Outubro de 2025  
**Versão**: 6.2.0  
**Status**: Em Análise  
**Autor**: Desenvolvedor Frontend  
**Revisor**: Engenheiro de Software  

---

## 📌 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Problema Identificado](#problema-identificado)
4. [Especificações Técnicas](#especificações-técnicas)
5. [Estrutura de Arquivos](#estrutura-de-arquivos)
6. [Códigos-Fonte](#códigos-fonte)
7. [Fluxo de Execução](#fluxo-de-execução)
8. [Testes e Validação](#testes-e-validação)
9. [Problemas e Soluções](#problemas-e-soluções)
10. [Recomendações](#recomendações)

---

## 📖 1. VISÃO GERAL

### 1.1 OBJETIVO
Criar uma interface de usuário com **modal separado** para exibir o progresso de execução do RPA (Robotic Process Automation) de cálculo de seguros da Imediato Seguros.

### 1.2 REQUISITOS FUNCIONAIS
- **RF01**: Formulário simplificado com 8 campos essenciais
- **RF02**: Modal overlay que abre após clicar "Efetuar Cálculo"
- **RF03**: Barra de progresso em tempo real no topo do modal
- **RF04**: 3 divs para exibir resultados (Estimativa, Recomendado, Alternativo)
- **RF05**: Integração com API RPA V4
- **RF06**: Atualização em tempo real via polling
- **RF07**: Design responsivo para desktop, tablet e mobile

### 1.3 REQUISITOS NÃO FUNCIONAIS
- **RNF01**: Identidade visual Imediato Seguros (cores, logotipo, fonte Titillium Web)
- **RNF02**: Performance: polling a cada 2 segundos
- **RNF03**: Compatibilidade: navegadores modernos (Chrome, Firefox, Edge, Safari)
- **RNF04**: Acessibilidade: WCAG 2.1 nível AA
- **RNF05**: UX: animações suaves, feedback visual

---

## 🏗️ 2. ARQUITETURA DO SISTEMA

### 2.1 DIAGRAMA DE COMPONENTES

```
┌─────────────────────────────────────────────────────────┐
│                     INDEX.HTML                          │
│                  (Página Principal)                     │
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │           FORMULÁRIO (8 campos)                │   │
│  │  - CPF, Nome, Data Nasc., Sexo, Estado Civil  │   │
│  │  - Placa, Marca, CEP                          │   │
│  │                                                │   │
│  │  [Botão: Efetuar Cálculo]                     │   │
│  └────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼ (onClick)
┌─────────────────────────────────────────────────────────┐
│              MAIN-PAGE.JS (Controller)                  │
│                                                         │
│  1. Coletar dados do formulário                        │
│  2. Mesclar com dados fixos (parametros.json)          │
│  3. Criar modal dinamicamente                          │
│  4. Chamar API /api/rpa/start                          │
│  5. Inicializar ProgressModalRPA                       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│         MODAL DE PROGRESSO (Overlay Fixo)              │
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │  BARRA DE PROGRESSO (Fixa no Topo)            │   │
│  │  - Logo, Porcentagem, Fase Atual, Estágio     │   │
│  │  - Barra visual de progresso                   │   │
│  └────────────────────────────────────────────────┘   │
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │  3 DIVS DE RESULTADOS                          │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐      │   │
│  │  │Estimativa│ │Recomend. │ │Alternativ│      │   │
│  │  │ Inicial  │ │  (Tela   │ │  (Tela   │      │   │
│  │  │(Tela 5)  │ │   15)    │ │   15)    │      │   │
│  │  └──────────┘ └──────────┘ └──────────┘      │   │
│  └────────────────────────────────────────────────┘   │
│                                                         │
│  [Nova Cotação]  [Falar com Corretor]                 │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼ (polling a cada 2s)
┌─────────────────────────────────────────────────────────┐
│           MODAL-PROGRESS.JS (Controller)                │
│                                                         │
│  1. Polling: GET /api/rpa/progress/{session_id}        │
│  2. Atualizar barra de progresso                       │
│  3. Atualizar fase atual                               │
│  4. Preencher valores nos 3 divs                       │
│  5. Detectar conclusão (success/failed)                │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              RPA-INTEGRATION.JS (Service)               │
│                                                         │
│  - Métodos auxiliares para API                         │
│  - Formatação de dados                                 │
│  - Geração de Session ID                               │
│  - Processamento de progresso                          │
└─────────────────────────────────────────────────────────┘
```

### 2.2 FLUXO DE DADOS

```
USUÁRIO → Formulário → MainPageRPA.collectFormData()
                              ↓
                       MainPageRPA.mergeWithFixedData()
                              ↓
                       MainPageRPA.openProgressModal()
                              ↓
                       API POST /api/rpa/start
                              ↓
                       ProgressModalRPA.setSessionId()
                              ↓
                       ProgressModalRPA.startProgressPolling()
                              ↓
              API GET /api/rpa/progress/{session_id} (a cada 2s)
                              ↓
                       ProgressModalRPA.updateProgress()
                              ↓
                       ProgressModalRPA.updateResults()
                              ↓
                       CONCLUSÃO (success/failed)
```

### 2.3 TECNOLOGIAS UTILIZADAS

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| HTML5 | - | Estrutura semântica |
| CSS3 | - | Estilização (Grid, Flexbox, Animações) |
| JavaScript | ES6+ | Lógica de negócio (Classes, Async/Await) |
| Font Awesome | 6.4.0 | Ícones |
| Google Fonts | - | Titillium Web |
| API RPA | V4 | Backend de processamento |

---

## 🚨 3. PROBLEMA IDENTIFICADO

### 3.1 DESCRIÇÃO DO PROBLEMA
O modal **NÃO está abrindo como overlay fixo** sobre a página principal. Em vez disso, está sendo renderizado como uma div integrada na página, logo abaixo do formulário.

### 3.2 EVIDÊNCIAS
- **Funcionalidade**: ✅ RPA executou com sucesso
- **API**: ✅ Dados enviados e recebidos corretamente
- **Progresso**: ✅ Polling funcionando
- **Visual**: ❌ Modal não é um overlay fixo

### 3.3 COMPORTAMENTO ESPERADO
```
┌─────────────────────────────────────────────┐
│        OVERLAY ESCURO (rgba(0,0,0,0.8))     │
│                                             │
│   ┌───────────────────────────────────┐   │
│   │                                   │   │
│   │         MODAL DE PROGRESSO        │   │
│   │                                   │   │
│   │  [Barra de Progresso]             │   │
│   │  [3 Divs de Resultados]           │   │
│   │                                   │   │
│   └───────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

### 3.4 COMPORTAMENTO ATUAL
```
┌─────────────────────────────────────────────┐
│          PÁGINA PRINCIPAL                   │
│                                             │
│  [Formulário]                               │
│                                             │
│  [Botão: Efetuar Cálculo]                   │
│                                             │
│  ┌───────────────────────────────────┐     │
│  │    MODAL (como div integrada)     │     │
│  │                                   │     │
│  │  [Barra de Progresso]             │     │
│  │  [3 Divs de Resultados]           │     │
│  └───────────────────────────────────┘     │
│                                             │
└─────────────────────────────────────────────┘
```

### 3.5 HIPÓTESES DA CAUSA RAIZ
1. **CSS não está sendo aplicado corretamente**
   - `position: fixed` sendo sobrescrito por outro CSS
   - Conflito de z-index com elementos da página principal
   - Estilos inline não estão funcionando

2. **Modal sendo criado no lugar errado do DOM**
   - `insertAdjacentHTML('beforeend')` pode estar colocando dentro de um container restrito
   - Container pai com `position: relative` interferindo

3. **CSS da página principal interferindo**
   - Reset CSS global sobrescrevendo estilos do modal
   - Herança de estilos indesejada

---

## 📐 4. ESPECIFICAÇÕES TÉCNICAS

### 4.1 ESPECIFICAÇÃO DO MODAL

#### 4.1.1 Layout Desktop (>1200px)
```
Largura: 100vw
Altura: 100vh
Position: fixed
Top: 0
Left: 0
Z-index: 999999
Background: rgba(0, 0, 0, 0.8)
Display: flex
Flex-direction: column
```

#### 4.1.2 Barra de Progresso
```
Position: sticky (dentro do modal)
Top: 0
Z-index: 10001 (relativo ao modal)
Background: linear-gradient(135deg, #003366, #0099CC)
Height: auto (conteúdo + padding)
```

#### 4.1.3 Divs de Resultados
```
Layout: Grid (3 colunas)
Grid-template-columns: 1fr 1fr 1fr
Gap: 2rem
Padding: 2rem
```

### 4.2 CORES OFICIAIS IMEDIATO SEGUROS
```css
--imediato-dark-blue: #003366    /* Azul Escuro Principal */
--imediato-light-blue: #0099CC   /* Azul Claro Secundário */
--imediato-white: #FFFFFF        /* Branco Neutro */
--imediato-gray: #F8F9FA         /* Cinza Claro */
--imediato-text: #333333         /* Texto Principal */
--imediato-text-light: #666666   /* Texto Secundário */
```

### 4.3 TIPOGRAFIA
```
Família: 'Titillium Web', sans-serif
Pesos: 300 (Light), 400 (Regular), 600 (SemiBold), 700 (Bold)
Fonte do logotipo: Extraída de https://www.segurosimediato.com.br
```

### 4.4 ANIMAÇÕES
```css
@keyframes modalSlideIn {
    from { opacity: 0; transform: scale(0.9) translateY(-50px); }
    to { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes progressShimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

@keyframes cardSlideIn {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
```

---

## 📁 5. ESTRUTURA DE ARQUIVOS

```
modal-rpa-separado-v6.2.0/
├── index.html                           # Página principal com formulário
├── modal-progress.html                  # Referência (não usado dinamicamente)
├── css/
│   ├── imediato-brand.css              # Variáveis CSS e identidade visual
│   ├── main-page.css                   # Estilos da página principal
│   └── modal-progress.css              # Estilos do modal de progresso
├── js/
│   ├── main-page.js                    # Controller da página principal
│   ├── modal-progress.js               # Controller do modal de progresso
│   └── rpa-integration.js              # Service de integração com API
├── PROJETO_MODAL_SEPARADO_V6.2.0.md    # Projeto original
├── IMPLEMENTACAO_MODAL_SEPARADO_V6.2.0.md  # Documentação de implementação
└── ESPECIFICACAO_TECNICA_MODAL_V6.2.0.md   # Este documento
```

---

## 💻 6. CÓDIGOS-FONTE

Ver arquivos separados para cada componente:
- `CODIGO_INDEX_HTML.md` - HTML da página principal
- `CODIGO_CSS_COMPLETO.md` - Todos os arquivos CSS
- `CODIGO_JAVASCRIPT_COMPLETO.md` - Todos os arquivos JavaScript

---

## 🔄 7. FLUXO DE EXECUÇÃO

### 7.1 INICIALIZAÇÃO
```
1. Página carrega index.html
2. CSS carregados (imediato-brand.css, main-page.css)
3. JavaScript carregados na ordem:
   a) rpa-integration.js
   b) modal-progress.js
   c) main-page.js
4. MainPageRPA inicializa:
   - Configura event listeners
   - Configura validação em tempo real
```

### 7.2 SUBMISSÃO DO FORMULÁRIO
```
1. Usuário preenche formulário
2. Clica "Efetuar Cálculo"
3. MainPageRPA.handleFormSubmit():
   a) Valida formulário
   b) Coleta dados (8 campos)
   c) Mescla com dados fixos
   d) Abre modal de progresso
   e) Inicia RPA
```

### 7.3 ABERTURA DO MODAL
```
1. MainPageRPA.openProgressModal():
   a) Cria HTML do modal dinamicamente
   b) Injeta no body (document.body.insertAdjacentHTML)
   c) Aguarda 100ms
   d) Inicializa ProgressModalRPA (sem sessionId)
```

### 7.4 INÍCIO DO RPA
```
1. MainPageRPA.startRPA():
   a) Chama API POST /api/rpa/start
   b) Recebe sessionId
   c) Atualiza ProgressModalRPA.setSessionId()
   d) Inicia polling
```

### 7.5 POLLING DE PROGRESSO
```
1. ProgressModalRPA.startProgressPolling():
   a) setInterval a cada 2000ms
   b) Chama API GET /api/rpa/progress/{session_id}
   c) Processa resposta
   d) Atualiza interface
   e) Verifica conclusão
```

### 7.6 ATUALIZAÇÃO DA INTERFACE
```
1. ProgressModalRPA.updateProgress():
   a) Extrai dados (status, mensagem, percentual, fase)
   b) Atualiza barra de progresso
   c) Atualiza fase atual
   d) Atualiza estágio (X de 15)
   e) Verifica falhas
   f) Verifica conclusão
```

### 7.7 CONCLUSÃO
```
1. RPA concluído (status: 'success'):
   a) Para polling
   b) Atualiza header para sucesso
   c) Extrai valores dos resultados
   d) Preenche 3 divs
   e) Anima valores

2. RPA falhou (status: 'failed'):
   a) Para polling
   b) Atualiza header para erro
   c) Exibe mensagem de erro
```

---

## 🧪 8. TESTES E VALIDAÇÃO

### 8.1 TESTES FUNCIONAIS
- [ ] Formulário valida campos em tempo real
- [ ] Modal abre como overlay fixo
- [ ] Barra de progresso atualiza corretamente
- [ ] 3 divs são preenchidos com valores corretos
- [ ] Polling funciona sem erros
- [ ] Conclusão é detectada corretamente

### 8.2 TESTES DE INTEGRAÇÃO
- [ ] API /api/rpa/start responde corretamente
- [ ] API /api/rpa/progress retorna dados completos
- [ ] SessionId é gerado e usado corretamente
- [ ] Dados fixos são mesclados corretamente

### 8.3 TESTES DE UI/UX
- [ ] Modal é visualmente correto
- [ ] Animações são suaves
- [ ] Cores seguem identidade visual
- [ ] Tipografia é consistente
- [ ] Responsividade funciona em todos os dispositivos

---

## 🔧 9. PROBLEMAS E SOLUÇÕES

### 9.1 PROBLEMA: ProgressModalRPA is not defined
**Causa**: Classe não carregada antes de ser usada  
**Solução**: Carregar scripts na ordem correta e usar `window.ProgressModalRPA`

### 9.2 PROBLEMA: Session ID não encontrado
**Causa**: Modal inicializado com sessionId antes da API responder  
**Solução**: Criar método `setSessionId()` e chamar após API responder

### 9.3 PROBLEMA: Modal não é overlay fixo
**Causa**: CSS não está sendo aplicado corretamente  
**Solução Implementada**:
- CSS com `!important` para forçar estilos
- CSS inline no HTML do modal
- Z-index muito alto (999999)

**Solução Recomendada pelo Engenheiro**:
- ??? (aguardando análise)

---

## 💡 10. RECOMENDAÇÕES PARA O ENGENHEIRO

### 10.1 QUESTÕES TÉCNICAS
1. **Por que o modal não está sendo renderizado como overlay fixo?**
   - Há algum CSS global interferindo?
   - O `insertAdjacentHTML` está no lugar correto?
   - Devemos usar `createPortal` (React) ou equivalente em JavaScript puro?

2. **Qual a melhor abordagem para garantir o overlay?**
   - Criar o modal no body (atual)
   - Criar o modal em um container dedicado
   - Usar Shadow DOM
   - Usar iframe

3. **Como evitar conflitos de CSS?**
   - CSS Modules
   - CSS-in-JS
   - Aumentar especificidade
   - Usar `!important` (atual)

### 10.2 ARQUITETURA
1. **A arquitetura atual está adequada?**
   - Separação de responsabilidades está correta?
   - Classes JavaScript estão bem estruturadas?
   - Há acoplamento excessivo?

2. **Melhorias sugeridas**
   - Implementar padrão Observer para comunicação entre componentes
   - Criar um Store centralizado para estado
   - Usar Web Components

### 10.3 PERFORMANCE
1. **O polling a cada 2s é adequado?**
   - Devemos usar WebSockets?
   - Server-Sent Events (SSE)?
   - Long Polling?

2. **Animações estão otimizadas?**
   - Usar `will-change`
   - Usar `transform` em vez de `top/left`
   - Reduzir repaints/reflows

### 10.4 SEGURANÇA
1. **Validação de dados**
   - Frontend está validando corretamente?
   - Backend deve revalidar?

2. **XSS Protection**
   - HTML dinâmico é seguro?
   - Devemos sanitizar inputs?

---

## 📞 11. CONTATO E SUPORTE

**Desenvolvedor**: Desenvolvedor Frontend  
**Engenheiro de Software**: [Nome]  
**Data de Análise**: [Data]  
**Status**: **AGUARDANDO ANÁLISE DO ENGENHEIRO**

---

**Fim do Documento**

*Este documento contém todas as especificações técnicas necessárias para análise do engenheiro de software. Códigos-fonte completos disponíveis nos arquivos do projeto.*



