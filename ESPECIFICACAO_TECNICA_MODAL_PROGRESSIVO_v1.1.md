# 📋 ESPECIFICAÇÃO TÉCNICA: MODAL WHATSAPP PROGRESSIVO V1.1

**Projeto:** Modal WhatsApp com Campos Progressivos  
**Versão:** 1.1  
**Data:** 28/01/2025  
**Autor:** Equipe de Desenvolvimento  
**Status:** Aprovado para Desenvolvimento

---

## 🎯 OBJETIVO

Desenvolver modal WhatsApp com **campos que aparecem progressivamente** conforme o preenchimento, reduzindo atrito inicial e mantendo flexibilidade para usuário.

---

## 📊 ESTRUTURA DE DIVISÕES

### DIV 1: DADOS ESSENCIAIS (Sempre Visível)
**Ordem de aparecimento:** Imediato  
**Campos:**
1. Telefone com DDD (integrado ou separado)
2. Placa do Veículo

**Validações:**
- Telefone: Formato brasileiro válido
- Placa: Formato antigo (ABC-1234) ou Mercosul (ABC1D23)

**Botões:**
- "📱 IR PARA O WHATSAPP" (habilitado após validar ambos)
- Opcionalmente: "Pular e ir direto" (se decidir ir só com telefone)

---

### DIV 2: DADOS COMPLEMENTARES (Aparece após DIV 1)
**Ordem de aparecimento:** Após telefone + placa validados  
**Campos:**
1. CPF *
2. Nome Completo (opcional)

**Validações:**
- CPF: Algoritmo + API PH3A (opcional)

**Mensagem:**
> ℹ️ *"O CPF ajuda a calcular uma cotação mais precisa. Caso deseje, pode informá-lo agora ou depois no WhatsApp."*

**Botões:**
- "📱 IR PARA O WHATSAPP"
- "Pular CPF e ir direto"

---

### DIV 3: DADOS EXTRAS (Aparece após DIV 2 - Opcional)
**Ordem de aparecimento:** Após CPF validado  
**Campos:**
1. CEP
2. Endereço completo (preenchido automaticamente via ViaCEP)

**Validações:**
- CEP: ViaCEP

**Mensagem:**
> ℹ️ *"CEP e endereço ajudam a personalizar ainda mais sua cotação."*

**Botões:**
- "📱 IR PARA O WHATSAPP"
- "Pular e ir direto"

---

## 🎨 WIREFRAMES DETALHADOS

### WIREFRAME 1: ESTADO INICIAL
```
┌───────────────────────────────────────────────┐
│  [X] Fechar                                  │
│                                               │
│  ╔═══════════════════════════════════════╗   │
│  ║  Solicitar Cotação                    ║   │
│  ║  Passo 1 de 3                         ║   │
│  ╚═══════════════════════════════════════╝   │
│                                               │
│  ┌─────────────────────────────────────┐     │
│  │ Telefone *                           │     │
│  │ ┌───────────────────────────────┐   │     │
│  │ │ (11) 99999-9999                 │   │     │
│  │ └───────────────────────────────┘   │     │
│  └─────────────────────────────────────┘     │
│                                               │
│  ┌─────────────────────────────────────┐     │
│  │ Placa *                              │     │
│  │ ┌───────────────────────────────┐   │     │
│  │ │ ABC-1234                        │   │     │
│  │ └───────────────────────────────┘   │     │
│  └─────────────────────────────────────┘     │
│                                               │
│  ┌─────────────────────────────────────┐     │
│  │ [📱 IR PARA O WHATSAPP] (disabled)  │     │
│  └─────────────────────────────────────┘     │
│                                               │
│  ○○○ Indicador de progresso                  │
│                                               │
└───────────────────────────────────────────────┘
```

### WIREFRAME 2: APÓS VALIDAR TELEFONE + PLACA
```
┌───────────────────────────────────────────────┐
│  [X]                                         │
│                                               │
│  ╔═══════════════════════════════════════╗   │
│  ║  ✅ Telefone: (11) 99999-9999        ║   │
│  ║  ✅ Placa: ABC-1234                   ║   │
│  ║                                       ║   │
│  ║  Passo 2 de 3                        ║   │
│  ╚═══════════════════════════════════════╝   │
│  ───────────────────────────────────────     │
│                                               │
│  ┌─────────────────────────────────────┐     │
│  │ CPF * (opcional mas recomendado)     │     │
│  │ ┌───────────────────────────────┐   │     │
│  │ │ 000.000.000-00                  │   │     │
│  │ └───────────────────────────────┘   │     │
│  └─────────────────────────────────────┘     │
│  ℹ️ CPF ajuda a calcular uma cotação mais   │
│     precisa. Pode informar agora ou depois. │
│                                               │
│  ┌─────────────────────────────────────┐     │
│  │ Nome Completo                       │     │
│  │ ┌───────────────────────────────┐   │     │
│  │ │ João da Silva                   │   │     │
│  │ └───────────────────────────────┘   │     │
│  └─────────────────────────────────────┘     │
│                                               │
│  ┌─────────────────────────────────────┐     │
│  │ [📱 IR PARA O WHATSAPP] (enabled)   │     │
│  └─────────────────────────────────────┘     │
│                                               │
│  ┌─────────────────────────────────────┐     │
│  │ Pular CPF e ir direto               │     │
│  └─────────────────────────────────────┘     │
│                                               │
│  ○●○ Indicador de progresso                  │
│                                               │
└───────────────────────────────────────────────┘
```

### WIREFRAME 3: APÓS VALIDAR CPF (Opcional)
```
┌───────────────────────────────────────────────┐
│  [X]                                         │
│                                               │
│  ╔═══════════════════════════════════════╗   │
│  ║  ✅ Telefone: (11) 99999-9999        ║   │
│  ║  ✅ Placa: ABC-1234                   ║   │
│  ║  ✅ CPF: 123.456.789-00              ║   │
│  ║  ✅ Nome: João da Silva              ║   │
│  ║                                       ║   │
│  ║  Passo 3 de 3                        ║   │
│  ╚═══════════════════════════════════════╝   │
│  ───────────────────────────────────────     │
│                                               │
│  ┌─────────────────────────────────────┐     │
│  │ CEP * (opcional)                     │     │
│  │ ┌───────────────────────────────┐   │     │
│  │ │ 01234-567                       │   │     │
│  │ └───────────────────────────────┘   │     │
│  │ (busca endereço via ViaCEP)          │     │
│  └─────────────────────────────────────┘     │
│                                               │
│  ┌─────────────────────────────────────┐     │
│  │ Endereço Completo                   │     │
│  │ ┌───────────────────────────────┐   │     │
│  │ │ Rua X, 123 - Centro - SP       │   │     │
│  │ │ (preenchido automaticamente)   │   │     │
│  │ └───────────────────────────────┘   │     │
│  └─────────────────────────────────────┘     │
│  ℹ️ CEP e endereço ajudam a personalizar    │
│     ainda mais sua cotação.                  │
│                                               │
│  ┌─────────────────────────────────────┐     │
│  │ [📱 IR PARA O WHATSAPP] (enabled)   │     │
│  └─────────────────────────────────────┘     │
│                                               │
│  ┌─────────────────────────────────────┐     │
│  │ Pular e ir direto                   │     │
│  └─────────────────────────────────────┘     │
│                                               │
│  ○●● Indicador de progresso                  │
│                                               │
└───────────────────────────────────────────────┘
```

---

## 💻 ESTRUTURA DE CÓDIGO

### HTML Estrutura

```html
<!-- Modal Container -->
<div id="whatsapp-modal" style="display: none;">
  
  <!-- Overlay -->
  <div class="whatsapp-modal-overlay"></div>
  
  <!-- Modal Content -->
  <div class="whatsapp-modal-content">
    
    <!-- Header -->
    <div class="modal-header">
      <button class="modal-close">×</button>
      <h2>Solicitar Cotação</h2>
      <div class="progress-indicator">
        <span class="step active">1</span>
        <span class="step-divider"></span>
        <span class="step">2</span>
        <span class="step-divider"></span>
        <span class="step">3</span>
        <span class="progress-text">Passo <span id="current-step">1</span> de 3</span>
      </div>
    </div>
    
    <!-- Form Container -->
    <form id="whatsapp-form-modal">
      
      <!-- DIV 1: Dados Essenciais -->
      <div id="div-etapa-1" class="modal-div active">
        
        <!-- Telefone -->
        <div class="field-group">
          <label for="telefone-modal">Telefone com DDD *</label>
          <input type="tel" id="telefone-modal" name="TELEFONE" />
          <small id="telefone-help" class="help-message"></small>
        </div>
        
        <!-- Placa -->
        <div class="field-group">
          <label for="placa-modal">Placa do Veículo *</label>
          <input type="text" id="placa-modal" name="PLACA" maxlength="8" />
          <small id="placa-help" class="help-message"></small>
        </div>
        
        <!-- Botão Principal -->
        <button type="submit" id="btn-prosseguir" class="btn-primary" disabled>
          📱 IR PARA O WHATSAPP
        </button>
        
      </div>
      
      <!-- DIV 2: Dados Complementares -->
      <div id="div-etapa-2" class="modal-div hidden">
        
        <!-- Divider visual -->
        <div class="divider">
          ✅ <span id="telefone-display"></span>
          ✅ <span id="placa-display"></span>
        </div>
        
        <!-- CPF -->
        <div class="field-group">
          <label for="cpf-modal">CPF * <small>(opcional mas recomendado)</small></label>
          <input type="text" id="cpf-modal" name="CPF" />
          <small id="cpf-help" class="help-message"></small>
        </div>
        
        <!-- Mensagem -->
        <div class="info-box">
          ℹ️ CPF ajuda a calcular uma cotação mais precisa. 
          Pode informar agora ou depois no WhatsApp.
        </div>
        
        <!-- Botão Principal -->
        <button type="submit" id="btn-prosseguir-2" class="btn-primary">
          📱 IR PARA O WHATSAPP
        </button>
        
        <!-- Botão Pular -->
        <button type="button" id="btn-pular-cpf" class="btn-secondary">
          Pular CPF e ir direto
        </button>
        
      </div>
      
      <!-- DIV 3: Dados Extras -->
      <div id="div-etapa-3" class="modal-div hidden">
        
        <!-- Divider visual -->
        <div class="divider">
          ✅ <span id="telefone-display-2"></span>
          ✅ <span id="cpf-display"></span>
          ✅ <span id="nome-display"></span>
        </div>
        
        <!-- CEP -->
        <div class="field-group">
          <label for="cep-modal">CEP * <small>(opcional)</small></label>
          <input type="text" id="cep-modal" name="CEP" />
          <small id="cep-help" class="help-message"></small>
        </div>
        
        <!-- Endereço -->
        <div class="field-group">
          <label for="endereco-modal">Endereço Completo</label>
          <input type="text" id="endereco-modal" name="ENDERECO" readonly />
        </div>
        
        <!-- Mensagem -->
        <div class="info-box">
          ℹ️ CEP e endereço ajudam a personalizar ainda mais sua cotação.
        </div>
        
        <!-- Botão Principal -->
        <button type="submit" id="btn-prosseguir-3" class="btn-primary">
          📱 IR PARA O WHATSAPP
        </button>
        
        <!-- Botão Pular -->
        <button type="button" id="btn-pular-endereco" class="btn-secondary">
          Pular e ir direto
        </button>
        
      </div>
      
    </form>
    
  </div>
  
</div>
```

---

## ⚙️ LÓGICA DE CONTROLE

### JavaScript - Estados e Transições

```javascript
const ModalStates = {
  ETAPA_1: {
    id: 'div-etapa-1',
    ativo: true,
    proximo: 'ETAPA_2',
    campos: ['telefone-modal', 'placa-modal'],
    botao: 'btn-prosseguir'
  },
  ETAPA_2: {
    id: 'div-etapa-2',
    ativo: false,
    proximo: 'ETAPA_3',
    campos: ['cpf-modal', 'nome-modal'],
    botao: 'btn-prosseguir-2',
    botaoPular: 'btn-pular-cpf'
  },
  ETAPA_3: {
    id: 'div-etapa-3',
    ativo: false,
    proximo: null,
    campos: ['cep-modal', 'endereco-modal'],
    botao: 'btn-prosseguir-3',
    botaoPular: 'btn-pular-endereco'
  }
};

let estadoAtual = 'ETAPA_1';
let dadosColetados = {};
```

### Função de Validação e Transição

```javascript
function validarEContinuar(campos, proximaEtapa) {
  let todosValidos = true;
  const dados = {};
  
  // Validar campos
  campos.forEach(campoId => {
    const $campo = $(`#${campoId}`);
    const valor = $campo.val();
    const nome = $campo.attr('name');
    
    if (!validarCampo(campoId, valor)) {
      todosValidos = false;
      mostrarErro($campo, `Campo ${campoId} inválido`);
    } else {
      dados[nome] = valor;
      mostrarSucesso($campo);
    }
  });
  
  // Se válidos, transicionar
  if (todosValidos) {
    dadosColetados = { ...dadosColetados, ...dados };
    
    if (proximaEtapa) {
      transicionarParaEtapa(proximaEtapa);
    } else {
      abrirWhatsApp(dadosColetados);
    }
  }
}

function transicionarParaEtapa(etapa) {
  const etapaAtual = ModalStates[estadoAtual];
  const etapaProxima = ModalStates[etapa];
  
  // Fade out etapa atual
  $(`#${etapaAtual.id}`).fadeOut(200, function() {
    // Atualizar estado
    estadoAtual = etapa;
    
    // Atualizar dados visuais anteriores
    atualizarDividerVisual(etapa);
    
    // Fade in próxima etapa
    $(`#${etapaProxima.id}`).fadeIn(200);
    
    // Atualizar indicador de progresso
    atualizarIndicadorProgresso(etapa);
  });
}
```

---

## 🎨 CSS - Animações e Transições

```css
/* Estados das DIVs */
.modal-div {
  display: none;
  animation: slideIn 0.3s ease;
}

.modal-div.active {
  display: block;
}

.modal-div.hidden {
  display: none;
}

/* Animação de entrada */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Indicador de Progresso */
.progress-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 15px 30px;
  background: rgba(255, 255, 255, 0.1);
}

.step {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
  transition: all 0.3s ease;
}

.step.active {
  background: #25D366;
  transform: scale(1.1);
}

.step-divider {
  width: 30px;
  height: 2px;
  background: rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.step.active ~ .step-divider {
  background: rgba(255, 255, 255, 0.5);
}

/* Divider Visual */
.divider {
  padding: 15px;
  background: #f0f7ff;
  border-left: 4px solid #25D366;
  margin: 20px 0;
  font-size: 14px;
  color: #666;
}

.divider span {
  color: #25D366;
  font-weight: bold;
}

/* Info Box */
.info-box {
  padding: 15px;
  background: #f8f9fa;
  border-left: 4px solid #0099CC;
  margin: 20px 0;
  font-size: 14px;
  color: #666;
}

/* Botões */
.btn-primary {
  width: 100%;
  padding: 16px 24px;
  background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  width: 100%;
  padding: 12px 24px;
  background: transparent;
  color: #0099CC;
  border: 2px solid #0099CC;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: #f0f7ff;
}
```

---

## 🔧 FUNÇÕES PRINCIPAIS

### 1. Validação de Campos

```javascript
function validarCampo(campoId, valor) {
  switch (campoId) {
    case 'telefone-modal':
      return validarTelefone(valor);
    
    case 'placa-modal':
      return validarPlaca(valor);
    
    case 'cpf-modal':
      return validarCPF(valor);
    
    case 'cep-modal':
      return validarCEP(valor);
    
    default:
      return true;
  }
}
```

### 2. Coleta de Dados

```javascript
function coletarTodosDados() {
  const dados = {};
  
  // Etapa 1: Sempre presente
  dados.TELEFONE = $('#telefone-modal').val();
  dados.PLACA = $('#placa-modal').val();
  
  // Etapa 2: Se validado
  if (estadoAtual === 'ETAPA_2' || estadoAtual === 'ETAPA_3') {
    dados.CPF = $('#cpf-modal').val();
    dados.NOME = $('#nome-modal').val();
  }
  
  // Etapa 3: Se validado
  if (estadoAtual === 'ETAPA_3') {
    dados.CEP = $('#cep-modal').val();
    dados.ENDERECO = $('#endereco-modal').val();
  }
  
  // Sempre adicionar GCLID
  dados.GCLID = getGCLID();
  
  return dados;
}
```

### 3. Abertura do WhatsApp

```javascript
function abrirWhatsApp(dados) {
  const telefone = dados.TELEFONE.replace(/\D/g, '');
  const gclid = dados.GCLID || '';
  
  // Construir mensagem
  let mensagem = 'Olá! Quero uma cotação de seguro.';
  
  if (dados.PLACA) {
    mensagem += `%0APlaca: ${dados.PLACA}`;
  }
  
  if (dados.CPF) {
    mensagem += `%0ACPF: ${dados.CPF}`;
  }
  
  if (dados.CEP) {
    mensagem += `%0ACEP: ${dados.CEP}`;
  }
  
  if (gclid) {
    mensagem += `%0ACódigo: ${gclid}`;
  }
  
  const whatsappUrl = `https://api.whatsapp.com/send?phone=551132301422&text=${mensagem}`;
  
  // Fechar modal
  $('#whatsapp-modal').fadeOut(300, function() {
    window.open(whatsappUrl, '_blank');
  });
}
```

---

## 📝 CHECKLIST DE IMPLEMENTAÇÃO

### Fase 1: Estrutura Base ✅
- [ ] Criar HTML do modal com 3 DIVs
- [ ] Implementar CSS de animações
- [ ] Adicionar indicador de progresso
- [ ] Configurar estado inicial (ETAPA_1 ativa)

### Fase 2: Lógica de Transição ✅
- [ ] Implementar função `validarEContinuar()`
- [ ] Implementar função `transicionarParaEtapa()`
- [ ] Implementar função `coletarTodosDados()`
- [ ] Implementar função `atualizarIndicadorProgresso()`

### Fase 3: Validações ✅
- [ ] Validar telefone (formato brasileiro)
- [ ] Validar placa (antigo + Mercosul)
- [ ] Validar CPF (algoritmo)
- [ ] Validar CEP (ViaCEP)
- [ ] Auto-preenchimento de endereço via ViaCEP

### Fase 4: Botões e Navegação ✅
- [ ] Botão principal desabilitado até validar telefone + placa
- [ ] Botão "Pular CPF" -> Ir direto para WhatsApp
- [ ] Botão "Pular Endereço" -> Ir direto para WhatsApp
- [ ] Botão principal -> Coletar todos os dados

### Fase 5: Integração GCLID ✅
- [ ] Capturar GCLID dos cookies
- [ ] Incluir GCLID na mensagem do WhatsApp
- [ ] Validar funcionamento offline

### Fase 6: Testes ✅
- [ ] Testar todas as transições
- [ ] Testar validações
- [ ] Testar em mobile
- [ ] Testar em diferentes browsers
- [ ] Validar mensagem do WhatsApp

### Fase 7: Analytics ✅
- [ ] Medir taxa de conversão por etapa
- [ ] Rastrear quantos usuários vão até etapa 3
- [ ] Monitorar taxa de "Pular"

---

## 🎯 ESPECIFICAÇÕES DE COMPORTAMENTO

### Regra 1: DIV 2 SÓ aparece se DIV 1 validado
```javascript
// Ao validar telefone + placa
$('#div-etapa-1').on('submit', function(e) {
  e.preventDefault();
  
  if (validarTelefone() && validarPlaca()) {
    transicionarParaEtapa('ETAPA_2');
  }
});
```

### Regra 2: DIV 3 SÓ aparece se DIV 2 validado
```javascript
// Ao validar CPF
$('#div-etapa-2').on('submit', function(e) {
  e.preventDefault();
  
  if (validarCPF()) {
    transicionarParaEtapa('ETAPA_3');
  }
});
```

### Regra 3: Botão "Pular" sempre disponível
```javascript
// Pular CPF
$('#btn-pular-cpf').on('click', function() {
  abrirWhatsApp(coletarTodosDados());
});

// Pular Endereço
$('#btn-pular-endereco').on('click', function() {
  abrirWhatsApp(coletarTodosDados());
});
```

---

## 📊 MÉTRICAS DE SUCESSO

| Métrica | Valor Esperado | Como Medir |
|---------|---------------|------------|
| **Taxa de abandono inicial** | < 15% | Analytics - cliques em #whatsapplink vs. submits |
| **Conversão DIV 1 → DIV 2** | > 60% | Analisar transições |
| **Conversão DIV 2 → DIV 3** | > 30% | Analisar transições |
| **Taxa de "Pular"** | < 40% | Contador de botões |
| **Tempo médio preenchimento** | < 40s | Timer em cada etapa |
| **Taxa de erro de validação** | < 10% | Log de erros |

---

## 🚀 ORDEM DE EXECUÇÃO

### Sprint 1 (1 semana)
1. Criar estrutura HTML com 3 DIVs
2. Implementar CSS de animações
3. Criar lógica de transição entre etapas
4. Implementar validações básicas (telefone, placa)

### Sprint 2 (1 semana)
1. Adicionar validações completas (CPF, CEP)
2. Implementar auto-preenchimento de endereço
3. Criar botões de "Pular"
4. Implementar coleta de GCLID

### Sprint 3 (1 semana)
1. Testes completos em diferentes browsers
2. Testes em mobile responsivo
3. Ajustes de UX baseados em feedback
4. Implementação de analytics

---

**Versão:** 1.1  
**Status:** Aprovado para Desenvolvimento  
**Data:** 28/01/2025





















