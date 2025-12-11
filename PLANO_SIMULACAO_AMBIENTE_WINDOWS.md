# 🖥️ PLANO DE SIMULAÇÃO - AMBIENTE WINDOWS
## Teste de Comunicação entre Ambientes

**Data:** 29 de Setembro de 2025  
**Projeto:** Simulação de Comunicação RPA  
**Status:** PLANO DE CONFIGURAÇÃO  
**Objetivo:** Simular comunicação entre frontend e backend no Windows  

---

## 🎯 ESTRUTURA DE SIMULAÇÃO

### **Ambiente 1: Frontend (Webflow Simulado)**
- **Local:** Windows local
- **Função:** Interface web com JavaScript
- **Porta:** 3000 (localhost:3000)
- **Tecnologia:** HTML + CSS + JavaScript

### **Ambiente 2: Backend (Hetzner Simulado)**
- **Local:** Windows local
- **Função:** API PHP + RPA Python
- **Porta:** 8000 (localhost:8000)
- **Tecnologia:** PHP + Python + Redis

---

## 🚀 CONFIGURAÇÃO DO AMBIENTE

### **1. Estrutura de Diretórios**
```
C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\imediatoseguros-rpa-playwright\
├── simulacao\
│   ├── frontend\          # Simula Webflow
│   │   ├── index.html
│   │   ├── css\
│   │   ├── js\
│   │   └── assets\
│   ├── backend\           # Simula Hetzner
│   │   ├── api\
│   │   │   ├── executar_rpa.php
│   │   │   └── get_progress.php
│   │   ├── rpa\
│   │   │   ├── executar_rpa_imediato_playwright.py
│   │   │   └── parametros.json
│   │   └── logs\
│   └── scripts\
│       ├── start_frontend.bat
│       ├── start_backend.bat
│       └── start_all.bat
```

### **2. Frontend Simulado (Webflow)**

#### **index.html**
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulação Webflow - Imediato Seguros</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="css/style.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h3 class="mb-0">
                            <i class="fas fa-car"></i>
                            Simulação Webflow - Calculadora de Seguro
                        </h3>
                    </div>
                    <div class="card-body">
                        <form id="seguro-form">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="placa" class="form-label">Placa do Veículo</label>
                                        <input type="text" class="form-control" id="placa" name="placa" 
                                               placeholder="ABC1234" value="EYQ4J41">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="marca" class="form-label">Marca</label>
                                        <select class="form-select" id="marca" name="marca">
                                            <option value="TOYOTA">TOYOTA</option>
                                            <option value="HONDA">HONDA</option>
                                            <option value="VOLKSWAGEN">VOLKSWAGEN</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="modelo" class="form-label">Modelo</label>
                                        <input type="text" class="form-control" id="modelo" name="modelo" 
                                               placeholder="COROLLA" value="COROLLA">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="ano" class="form-label">Ano</label>
                                        <input type="number" class="form-control" id="ano" name="ano" 
                                               placeholder="2009" value="2009">
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="nome" class="form-label">Nome do Segurado</label>
                                        <input type="text" class="form-control" id="nome" name="nome" 
                                               placeholder="João Silva" value="João Silva">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="cpf" class="form-label">CPF</label>
                                        <input type="text" class="form-control" id="cpf" name="cpf" 
                                               placeholder="123.456.789-00" value="123.456.789-00">
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="email" class="form-label">Email</label>
                                        <input type="email" class="form-control" id="email" name="email" 
                                               placeholder="joao@email.com" value="joao@email.com">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="celular" class="form-label">Celular</label>
                                        <input type="text" class="form-control" id="celular" name="celular" 
                                               placeholder="(11) 99999-9999" value="(11) 99999-9999">
                                    </div>
                                </div>
                            </div>
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary btn-lg">
                                    <i class="fas fa-calculator"></i>
                                    Calcular Seguro
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal de Progresso -->
    <div id="rpa-modal" class="rpa-modal-overlay" style="display: none;">
        <div class="rpa-modal-container">
            <div class="rpa-modal-header">
                <div class="rpa-modal-logo">
                    <i class="fas fa-shield-alt" style="font-size: 40px;"></i>
                </div>
                <div class="rpa-modal-title">
                    <h3>⏳ Calculando seu Seguro...</h3>
                    <p>Aguarde um momento, estamos processando seus dados</p>
                </div>
                <button class="rpa-modal-close" onclick="window.rpaModal.hide()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            
            <div class="rpa-modal-body">
                <!-- Progresso Geral -->
                <div class="rpa-progress-container">
                    <div class="rpa-progress-header">
                        <span class="rpa-progress-label">Progresso Geral</span>
                        <span class="rpa-progress-percentage">0%</span>
                    </div>
                    <div class="rpa-progress-bar">
                        <div class="rpa-progress-fill" style="width: 0%"></div>
                    </div>
                    <div class="rpa-progress-steps">0 de 15 telas processadas</div>
                </div>

                <!-- Tela Atual -->
                <div class="rpa-current-step">
                    <div class="rpa-step-header">
                        <div class="rpa-step-icon">🚗</div>
                        <div class="rpa-step-info">
                            <h4>Aguardando início...</h4>
                            <small>Preparando processamento</small>
                        </div>
                    </div>
                    <div class="rpa-step-progress">
                        <div class="rpa-progress-bar small">
                            <div class="rpa-progress-fill" style="width: 0%"></div>
                        </div>
                        <span class="rpa-step-time">⏱️ Tempo estimado: --</span>
                    </div>
                </div>

                <!-- Estimativas -->
                <div class="rpa-estimates">
                    <h5>📊 Estimativas Iniciais (Tela 5)</h5>
                    <div class="rpa-estimates-grid">
                        <div class="rpa-estimate-card">
                            <div class="rpa-estimate-header">
                                <i class="fas fa-shield-alt"></i>
                                <h6>Compreensiva</h6>
                            </div>
                            <div class="rpa-estimate-value">--</div>
                        </div>
                        <div class="rpa-estimate-card">
                            <div class="rpa-estimate-header">
                                <i class="fas fa-lock"></i>
                                <h6>Roubo e Furto</h6>
                            </div>
                            <div class="rpa-estimate-value">--</div>
                        </div>
                        <div class="rpa-estimate-card">
                            <div class="rpa-estimate-header">
                                <i class="fas fa-car-crash"></i>
                                <h6>RCF</h6>
                            </div>
                            <div class="rpa-estimate-value">--</div>
                        </div>
                    </div>
                </div>

                <!-- Timeline -->
                <div class="rpa-timeline">
                    <h5>📋 Timeline de Execução</h5>
                    <div class="rpa-timeline-container" id="rpa-timeline">
                        <!-- Timeline items will be populated dynamically -->
                    </div>
                </div>
            </div>

            <div class="rpa-modal-footer">
                <div class="rpa-last-update">
                    <i class="fas fa-sync-alt"></i>
                    Última atualização: <span id="rpa-last-update">--</span>
                </div>
            </div>
        </div>
    </div>

    <script src="js/rpa-modal.js"></script>
    <script src="js/app.js"></script>
</body>
</html>
```

#### **css/style.css**
```css
/* Estilos do modal RPA */
.rpa-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.rpa-modal-container {
    background: white;
    border-radius: 16px;
    max-width: 600px;
    width: 100%;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    animation: rpa-modal-slide-in 0.3s ease-out;
}

@keyframes rpa-modal-slide-in {
    from {
        opacity: 0;
        transform: translateY(-20px) scale(0.95);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.rpa-modal-header {
    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
    color: white;
    padding: 24px;
    border-radius: 16px 16px 0 0;
    display: flex;
    align-items: center;
    gap: 16px;
    position: relative;
}

.rpa-modal-title h3 {
    margin: 0;
    font-size: 20px;
    font-weight: 700;
}

.rpa-modal-title p {
    margin: 4px 0 0 0;
    opacity: 0.9;
    font-size: 14px;
}

.rpa-modal-close {
    position: absolute;
    top: 16px;
    right: 16px;
    background: none;
    border: none;
    color: white;
    font-size: 18px;
    padding: 8px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.3s ease;
}

.rpa-modal-close:hover {
    background: rgba(255, 255, 255, 0.1);
}

.rpa-modal-body {
    padding: 24px;
}

.rpa-progress-container {
    margin-bottom: 24px;
}

.rpa-progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.rpa-progress-label {
    font-weight: 600;
    color: #374151;
}

.rpa-progress-percentage {
    font-weight: 700;
    color: #1e40af;
    font-size: 18px;
}

.rpa-progress-bar {
    height: 8px;
    background: #e5e7eb;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 8px;
}

.rpa-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
    border-radius: 4px;
    transition: width 0.5s ease;
    position: relative;
}

.rpa-progress-fill::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%);
    animation: rpa-progress-shine 2s infinite;
}

@keyframes rpa-progress-shine {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.rpa-progress-steps {
    font-size: 14px;
    color: #6b7280;
    text-align: center;
}

.rpa-current-step {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 24px;
}

.rpa-step-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}

.rpa-step-icon {
    font-size: 24px;
}

.rpa-step-info h4 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
    color: #374151;
}

.rpa-step-info small {
    color: #6b7280;
    font-size: 12px;
}

.rpa-step-progress {
    display: flex;
    align-items: center;
    gap: 12px;
}

.rpa-progress-bar.small {
    flex: 1;
    height: 6px;
}

.rpa-step-time {
    font-size: 12px;
    color: #6b7280;
    white-space: nowrap;
}

.rpa-estimates {
    margin-bottom: 24px;
}

.rpa-estimates h5 {
    margin: 0 0 16px 0;
    font-size: 16px;
    font-weight: 600;
    color: #374151;
}

.rpa-estimates-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px;
}

.rpa-estimate-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 12px;
    text-align: center;
}

.rpa-estimate-header {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    margin-bottom: 8px;
}

.rpa-estimate-header i {
    color: #1e40af;
}

.rpa-estimate-header h6 {
    margin: 0;
    font-size: 12px;
    font-weight: 600;
    color: #374151;
}

.rpa-estimate-value {
    font-size: 14px;
    font-weight: 700;
    color: #059669;
}

.rpa-timeline h5 {
    margin: 0 0 16px 0;
    font-size: 16px;
    font-weight: 600;
    color: #374151;
}

.rpa-timeline-container {
    max-height: 200px;
    overflow-y: auto;
}

.rpa-timeline-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0;
    border-bottom: 1px solid #f3f4f6;
}

.rpa-timeline-item:last-child {
    border-bottom: none;
}

.rpa-timeline-icon {
    font-size: 16px;
    width: 24px;
    text-align: center;
}

.rpa-timeline-content h6 {
    margin: 0;
    font-size: 14px;
    font-weight: 600;
    color: #374151;
}

.rpa-timeline-content small {
    color: #6b7280;
    font-size: 12px;
}

.rpa-timeline-item.completed .rpa-timeline-icon {
    color: #059669;
}

.rpa-timeline-item.active .rpa-timeline-icon {
    color: #1e40af;
}

.rpa-timeline-item.pending .rpa-timeline-icon {
    color: #9ca3af;
}

.rpa-modal-footer {
    padding: 16px 24px;
    border-top: 1px solid #e5e7eb;
    background: #f9fafb;
    border-radius: 0 0 16px 16px;
}

.rpa-last-update {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    font-size: 12px;
    color: #6b7280;
}

.rpa-last-update i {
    animation: rpa-spin 2s linear infinite;
}

@keyframes rpa-spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
    .rpa-modal-container {
        margin: 10px;
        max-width: calc(100% - 20px);
    }
    
    .rpa-modal-header {
        padding: 16px;
        flex-direction: column;
        text-align: center;
        gap: 12px;
    }
    
    .rpa-modal-close {
        position: static;
        align-self: flex-end;
    }
    
    .rpa-modal-body {
        padding: 16px;
    }
    
    .rpa-estimates-grid {
        grid-template-columns: 1fr;
    }
}
```

#### **js/rpa-modal.js**
```javascript
/**
 * RPA Modal para Simulação - Imediato Seguros
 * Versão: 1.0.0
 */

(function() {
  'use strict';

  // Configurações
  const CONFIG = {
    apiUrl: 'http://localhost:8000', // Backend local
    pollingInterval: 1500, // 1.5 segundos
    timeout: 30000, // 30 segundos
    sessionPrefix: 'seguro_simulacao_'
  };

  // Classe principal do modal
  class RPAModal {
    constructor() {
      this.modal = null;
      this.isActive = false;
      this.sessionId = null;
      this.pollingInterval = null;
      this.init();
    }

    init() {
      this.modal = document.getElementById('rpa-modal');
      this.setupEventListeners();
    }

    // Configurar event listeners
    setupEventListeners() {
      // Fechar modal ao clicar no overlay
      this.modal.addEventListener('click', (e) => {
        if (e.target.classList.contains('rpa-modal-overlay')) {
          this.hide();
        }
      });

      // Fechar modal com ESC
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && this.isActive) {
          this.hide();
        }
      });
    }

    // Mostrar modal
    show(sessionId) {
      this.sessionId = sessionId;
      this.isActive = true;
      this.modal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
      this.startPolling();
    }

    // Esconder modal
    hide() {
      this.isActive = false;
      this.modal.style.display = 'none';
      document.body.style.overflow = '';
      this.stopPolling();
    }

    // Iniciar polling
    startPolling() {
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval);
      }

      this.pollingInterval = setInterval(() => {
        this.updateProgress();
      }, CONFIG.pollingInterval);
    }

    // Parar polling
    stopPolling() {
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval);
        this.pollingInterval = null;
      }
    }

    // Atualizar progresso
    async updateProgress() {
      try {
        const response = await fetch(`${CONFIG.apiUrl}/get_progress.php?session=${this.sessionId}`);
        const data = await response.json();

        if (data.success) {
          this.updateProgressBar(data.progress);
          this.updateCurrentStep(data.current_step);
          this.updateEstimates(data.estimates);
          this.updateTimeline(data.timeline);
          this.updateLastUpdate();

          // Verificar se concluído
          if (data.progress >= 100) {
            this.handleCompletion(data);
          }
        }
      } catch (error) {
        console.error('Erro ao atualizar progresso:', error);
      }
    }

    // Atualizar barra de progresso
    updateProgressBar(progress) {
      const progressFill = document.querySelector('.rpa-progress-fill');
      const progressPercentage = document.querySelector('.rpa-progress-percentage');
      const progressSteps = document.querySelector('.rpa-progress-steps');

      if (progressFill) {
        progressFill.style.width = `${progress}%`;
      }
      if (progressPercentage) {
        progressPercentage.textContent = `${progress}%`;
      }
      if (progressSteps) {
        const currentStep = Math.floor((progress / 100) * 15);
        progressSteps.textContent = `${currentStep} de 15 telas processadas`;
      }
    }

    // Atualizar etapa atual
    updateCurrentStep(stepData) {
      const stepIcon = document.querySelector('.rpa-step-icon');
      const stepTitle = document.querySelector('.rpa-step-info h4');
      const stepDescription = document.querySelector('.rpa-step-info small');
      const stepProgress = document.querySelector('.rpa-step-progress .rpa-progress-fill');
      const stepTime = document.querySelector('.rpa-step-time');

      if (stepIcon) stepIcon.textContent = stepData.icon || '🚗';
      if (stepTitle) stepTitle.textContent = stepData.title || 'Processando...';
      if (stepDescription) stepDescription.textContent = stepData.description || 'Aguarde...';
      if (stepProgress) stepProgress.style.width = `${stepData.progress || 0}%`;
      if (stepTime) stepTime.textContent = `⏱️ Tempo estimado: ${stepData.estimated_time || '--'}`;
    }

    // Atualizar estimativas
    updateEstimates(estimates) {
      if (!estimates) return;

      const estimateCards = document.querySelectorAll('.rpa-estimate-card');
      const estimateTypes = ['compreensiva', 'roubo_furto', 'rcf'];

      estimateTypes.forEach((type, index) => {
        const card = estimateCards[index];
        if (card && estimates[type]) {
          const valueElement = card.querySelector('.rpa-estimate-value');
          if (valueElement) {
            valueElement.textContent = estimates[type];
          }
        }
      });
    }

    // Atualizar timeline
    updateTimeline(timeline) {
      if (!timeline) return;

      const timelineContainer = document.getElementById('rpa-timeline');
      if (!timelineContainer) return;

      timelineContainer.innerHTML = timeline.map(step => `
        <div class="rpa-timeline-item ${step.status}">
          <div class="rpa-timeline-icon">${step.icon}</div>
          <div class="rpa-timeline-content">
            <h6>${step.title}</h6>
            <small>${step.description}</small>
          </div>
        </div>
      `).join('');
    }

    // Atualizar última atualização
    updateLastUpdate() {
      const lastUpdateElement = document.getElementById('rpa-last-update');
      if (lastUpdateElement) {
        lastUpdateElement.textContent = new Date().toLocaleTimeString();
      }
    }

    // Tratar conclusão
    handleCompletion(data) {
      this.stopPolling();
      
      // Mostrar resultado final
      setTimeout(() => {
        this.hide();
        this.showResults(data.final_result);
      }, 2000);
    }

    // Mostrar resultados
    showResults(result) {
      alert('RPA concluído com sucesso!\n\nResultado: ' + JSON.stringify(result, null, 2));
    }
  }

  // Função para executar RPA
  async function executeRPA(formData) {
    try {
      const sessionId = CONFIG.sessionPrefix + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      
      const response = await fetch(`${CONFIG.apiUrl}/executar_rpa.php`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session: sessionId,
          dados: formData
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        // Mostrar modal de progresso
        window.rpaModal.show(sessionId);
        return { success: true, sessionId };
      } else {
        throw new Error(data.message || 'Erro ao executar RPA');
      }
    } catch (error) {
      console.error('Erro ao executar RPA:', error);
      return { success: false, error: error.message };
    }
  }

  // Inicializar quando DOM estiver pronto
  function init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        window.rpaModal = new RPAModal();
        window.executeRPA = executeRPA;
      });
    } else {
      window.rpaModal = new RPAModal();
      window.executeRPA = executeRPA;
    }
  }

  // Inicializar
  init();

})();
```

#### **js/app.js**
```javascript
// Aplicação principal
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('seguro-form');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Coletar dados do formulário
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Executar RPA
        const result = await executeRPA(data);
        
        if (result.success) {
            console.log('RPA iniciado com sucesso!');
        } else {
            alert('Erro ao iniciar cálculo: ' + result.error);
        }
    });
});
```

### **3. Backend Simulado (Hetzner)**

#### **api/executar_rpa.php**
```php
<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Tratar preflight OPTIONS
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Verificar método
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Método não permitido']);
    exit();
}

// Obter dados JSON
$input = file_get_contents('php://input');
$data = json_decode($input, true);

if (!$data) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Dados JSON inválidos']);
    exit();
}

// Validar dados obrigatórios
$required_fields = ['session', 'dados'];
foreach ($required_fields as $field) {
    if (!isset($data[$field])) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => "Campo obrigatório: $field"]);
        exit();
    }
}

$session_id = $data['session'];
$dados = $data['dados'];

// Criar arquivo de parâmetros temporário
$parametros_file = "temp/parametros_{$session_id}.json";
$parametros_dir = dirname($parametros_file);

if (!is_dir($parametros_dir)) {
    mkdir($parametros_dir, 0755, true);
}

// Mapear dados do formulário para parâmetros do RPA
$parametros = [
    'placa' => $dados['placa'] ?? 'EYQ4J41',
    'marca' => $dados['marca'] ?? 'TOYOTA',
    'modelo' => $dados['modelo'] ?? 'COROLLA',
    'ano' => intval($dados['ano'] ?? 2009),
    'combustivel' => 'flex',
    'zero_km' => false,
    'kit_gas' => false,
    'blindado' => false,
    'financiado' => false,
    'nome' => $dados['nome'] ?? 'João Silva',
    'cpf' => $dados['cpf'] ?? '123.456.789-00',
    'email' => $dados['email'] ?? 'joao@email.com',
    'celular' => $dados['celular'] ?? '(11) 99999-9999',
    'cep' => '01234-567',
    'endereco' => 'Rua das Flores, 123',
    'cidade' => 'São Paulo',
    'estado' => 'SP',
    'garagem_residencia' => true,
    'garagem_trabalho' => false,
    'garagem_outros' => false,
    'uso_veiculo' => 'particular'
];

// Salvar arquivo de parâmetros
file_put_contents($parametros_file, json_encode($parametros, JSON_PRETTY_PRINT));

// Executar RPA em background
$rpa_script = '../rpa/executar_rpa_imediato_playwright.py';
$command = "python \"$rpa_script\" --config \"$parametros_file\" --session \"$session_id\" --progress-tracker json --modo-silencioso > logs/rpa_{$session_id}.log 2>&1 &";

// Executar comando
$pid = shell_exec($command);

// Resposta de sucesso
echo json_encode([
    'success' => true,
    'session_id' => $session_id,
    'pid' => trim($pid),
    'message' => 'RPA iniciado com sucesso'
]);
?>
```

#### **api/get_progress.php**
```php
<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Tratar preflight OPTIONS
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Verificar método
if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Método não permitido']);
    exit();
}

// Obter session ID
$session_id = $_GET['session'] ?? '';

if (empty($session_id)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Session ID obrigatório']);
    exit();
}

// Procurar arquivo de progresso
$progress_file = "../rpa_data/progress_{$session_id}.json";

if (!file_exists($progress_file)) {
    echo json_encode([
        'success' => true,
        'progress' => 0,
        'current_step' => [
            'icon' => '🚗',
            'title' => 'Aguardando início...',
            'description' => 'Preparando processamento',
            'progress' => 0,
            'estimated_time' => '--'
        ],
        'estimates' => null,
        'timeline' => []
    ]);
    exit();
}

// Ler arquivo de progresso
$progress_data = json_decode(file_get_contents($progress_file), true);

if (!$progress_data) {
    echo json_encode([
        'success' => false,
        'message' => 'Erro ao ler arquivo de progresso'
    ]);
    exit();
}

// Preparar resposta
$response = [
    'success' => true,
    'progress' => $progress_data['progresso_geral'] ?? 0,
    'current_step' => [
        'icon' => $progress_data['etapa_atual']['icon'] ?? '🚗',
        'title' => $progress_data['etapa_atual']['titulo'] ?? 'Processando...',
        'description' => $progress_data['etapa_atual']['descricao'] ?? 'Aguarde...',
        'progress' => $progress_data['etapa_atual']['progresso'] ?? 0,
        'estimated_time' => $progress_data['etapa_atual']['tempo_estimado'] ?? '--'
    ],
    'estimates' => $progress_data['estimativas'] ?? null,
    'timeline' => $progress_data['timeline'] ?? []
];

echo json_encode($response);
?>
```

### **4. Scripts de Inicialização**

#### **scripts/start_frontend.bat**
```batch
@echo off
echo Iniciando Frontend (Simulação Webflow)...
cd /d "%~dp0..\frontend"
python -m http.server 3000
pause
```

#### **scripts/start_backend.bat**
```batch
@echo off
echo Iniciando Backend (Simulação Hetzner)...
cd /d "%~dp0..\backend"
php -S localhost:8000
pause
```

#### **scripts/start_all.bat**
```batch
@echo off
echo Iniciando Simulação Completa...
echo.
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
echo.
start "Frontend" cmd /k "cd /d "%~dp0..\frontend" && python -m http.server 3000"
timeout /t 2
start "Backend" cmd /k "cd /d "%~dp0..\backend" && php -S localhost:8000"
echo.
echo Ambientes iniciados!
echo Pressione qualquer tecla para fechar...
pause > nul
```

---

## 🚀 COMO EXECUTAR

### **1. Preparar Ambiente**
```bash
# Criar estrutura de diretórios
mkdir simulacao
cd simulacao
mkdir frontend backend scripts
mkdir frontend\css frontend\js frontend\assets
mkdir backend\api backend\rpa backend\logs backend\temp
mkdir backend\rpa_data
```

### **2. Copiar Arquivos**
- Copiar arquivos HTML, CSS, JS para `frontend/`
- Copiar arquivos PHP para `backend/api/`
- Copiar RPA Python para `backend/rpa/`
- Copiar scripts .bat para `scripts/`

### **3. Executar Simulação**
```bash
# Opção 1: Executar tudo de uma vez
scripts\start_all.bat

# Opção 2: Executar separadamente
scripts\start_frontend.bat  # Terminal 1
scripts\start_backend.bat   # Terminal 2
```

### **4. Testar Comunicação**
1. Abrir navegador em `http://localhost:3000`
2. Preencher formulário
3. Clicar em "Calcular Seguro"
4. Observar modal de progresso
5. Verificar logs em `backend/logs/`

---

## 🎯 RESULTADO ESPERADO

### **Simulação Completa**
- **Frontend:** Interface web simulando Webflow
- **Backend:** API PHP simulando Hetzner
- **Comunicação:** HTTP entre localhost:3000 e localhost:8000
- **RPA:** Execução real do Python RPA
- **Progresso:** Modal em tempo real

### **Testes Possíveis**
- ✅ Formulário → API → RPA
- ✅ Polling de progresso
- ✅ Modal de progresso
- ✅ Timeline de execução
- ✅ Estimativas em tempo real
- ✅ Responsividade mobile

---

**📋 Plano gerado em:** 29 de Setembro de 2025  
**🖥️ Ambiente:** Windows Local  
**⏱️ Setup:** 30 minutos  
**👥 Complexidade:** Baixa  
**💰 Investimento:** Zero  
**🏆 Resultado:** Simulação completa funcional



























