<!-- ====================== -->
<!-- Google Tag Manager (noscript) - manter -->
<noscript>
  <iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PD6J398"
          height="0" width="0"
          style="display:none;visibility:hidden"></iframe>
</noscript>
<!-- ====================== -->

<!-- ====================== -->
<!-- Submissão especial: abre WhatsApp e depois envia o form -->
<script>
  document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('form-wp');
    if (!form) return;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var whatsappUrl = "https://api.whatsapp.com/send?phone=551141718837&text=Ola.%20Quero%20fazer%20uma%20cotacao%20de%20seguro.";
      window.open(whatsappUrl, '_blank');
      form.submit();
    });
  });
</script>
<!-- ====================== -->

<!-- ====================== -->
<!-- Bibliotecas base -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js" crossorigin="anonymous"></script>

<!-- SweetAlert2 v11.14.0 -->
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11.14.0/dist/sweetalert2.all.min.js" defer></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11.14.0/dist/sweetalert2.min.css"/>
<!-- ====================== -->

<!-- ====================== -->
<!-- 🔧 CONFIGURAÇÕES E CONSTANTES - Deve estar ANTES do Utils.js -->
<script>
/* ========= CONFIG ========= */
const USE_PHONE_API = true;  // usa Apilayer além da regra local
const APILAYER_KEY  = 'dce92fa84152098a3b5b7b8db24debbc';
const SAFETY_TICKET = '9bab7f0c2711c5accfb83588c859dc1103844a94';
const SAFETY_API_KEY = '20a7a1c297e39180bd80428ac13c363e882a531f';

// Flag para controlar validação PH3A
const VALIDAR_PH3A = false; // true = consulta API PH3A, false = apenas validação local

// ✅ EXPOR CONSTANTES GLOBALMENTE (OBRIGATÓRIO - antes de Utils.js carregar)
window.USE_PHONE_API = USE_PHONE_API;
window.APILAYER_KEY = APILAYER_KEY;
window.SAFETY_TICKET = SAFETY_TICKET;
window.SAFETY_API_KEY = SAFETY_API_KEY;
window.VALIDAR_PH3A = VALIDAR_PH3A;

console.log('✅ [FOOTER] Constantes expostas globalmente');
</script>
<!-- ====================== -->

<!-- ====================== -->
<!-- 🛠️ Footer Code Utils - Carregar funções utilitárias -->
<script>
(function() {
  // Carregar Utils.js dinamicamente antes de tudo
  const utilsScript = document.createElement('script');
  utilsScript.src = 'https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoUtils.js?v=3&nocache=' + Date.now();
  utilsScript.async = false; // Carregar de forma síncrona para garantir ordem
  
  console.log('🔄 [FOOTER] Tentando carregar Utils.js da URL:', utilsScript.src);
  
  // Função para verificar se todas as funções foram carregadas
  function verificarFuncoesUtils() {
    const requiredFunctions = [
      'onlyDigits', 'toUpperNospace', 'setFieldValue', 'readCookie',
      'generateSessionId', 'nativeSubmit', 'validarEmailLocal',
      'validarCPFFormato', 'validarCPFAlgoritmo', 'validarPlacaFormato',
      'validarCelularLocal', 'aplicarMascaraPlaca', 'sha1', 'hmacSHA256',
      'extractDataFromPH3A', 'extractVehicleFromPlacaFipe',
      'preencherEnderecoViaCEP', 'validarCPFApi', 'validarCepViaCep',
      'validarPlacaApi', 'validarCelularApi', 'validarTelefoneAsync',
      'validarEmailSafetyMails', 'initLoading', 'showLoading', 'hideLoading'
    ];
    
    // ✅ Verificar constantes também (recomendação do engenheiro)
    const requiredConstants = ['USE_PHONE_API', 'APILAYER_KEY', 'SAFETY_TICKET', 'SAFETY_API_KEY', 'VALIDAR_PH3A'];
    const missingConstants = requiredConstants.filter(c => typeof window[c] === 'undefined');
    if (missingConstants.length > 0) {
      console.error('❌ [FOOTER] Constantes faltando:', missingConstants);
    }
    
    const missing = requiredFunctions.filter(fn => typeof window[fn] !== 'function');
    if (missing.length > 0) {
      console.error('❌ [FOOTER] Funções faltando:', missing);
      return false;
    } else {
      console.log('✅ [FOOTER] Todas as funções utilitárias disponíveis');
      return true;
    }
  }
  
  utilsScript.onload = function() {
    console.log('✅ [FOOTER] Utils.js carregado com sucesso');
    verificarFuncoesUtils();
    
    // Disparar evento customizado para indicar que Utils está pronto
    window.dispatchEvent(new CustomEvent('footerUtilsLoaded'));
  };
  
  utilsScript.onerror = function(error) {
    console.error('❌ [FOOTER] Erro ao carregar Utils.js');
    console.error('❌ [FOOTER] Detalhes do erro:', error);
    console.error('❌ [FOOTER] URL tentada:', utilsScript.src);
    console.error('❌ [FOOTER] Script element:', utilsScript);
    
    // Tentar diagnosticar o problema
    fetch(utilsScript.src, { method: 'HEAD' })
      .then(response => {
        console.log('✅ [FOOTER] HEAD request OK - Status:', response.status);
        console.log('✅ [FOOTER] Content-Type:', response.headers.get('content-type'));
      })
      .catch(err => {
        console.error('❌ [FOOTER] HEAD request falhou:', err);
      });
    
    console.warn('⚠️ [FOOTER] Algumas funcionalidades podem não funcionar corretamente');
  };
  
  document.head.appendChild(utilsScript);
})();
</script>
<!-- ====================== -->

<!-- ====================== -->
<!-- 🎯 CONFIGURAÇÃO RPA GLOBAL -->
<script>
  // Flag global para controle do RPA
  window.rpaEnabled = false;
  console.log('🎯 [CONFIG] RPA habilitado:', window.rpaEnabled);
  
  // FASE 0: Função básica de logging para teste
  function logDebug(level, message, data = null) {
    const logData = {
      level: level,
      message: message,
      data: data,
      timestamp: new Date().toISOString(),
      sessionId: window.sessionId || 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
      url: window.location.href,
      userAgent: navigator.userAgent
    };
    
    // Enviar para sistema PHP de logging com tratamento completo de resposta
    fetch('https://bpsegurosimediato.com.br/logging_system/debug_logger_db.php', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(logData),
      mode: 'cors',
      credentials: 'omit'
    })
    .then(response => {
      console.log(`[LOG DEBUG] Status: ${response.status} ${response.statusText}`);
      console.log(`[LOG DEBUG] Headers:`, Object.fromEntries(response.headers.entries()));
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return response.text(); // Usar text() primeiro para ver se há conteúdo
    })
    .then(text => {
      console.log(`[LOG DEBUG] Resposta bruta:`, text);
      
      try {
        const result = JSON.parse(text);
        console.log(`[LOG DEBUG] Sucesso:`, result);
        
        if (result.success) {
          console.log(`[LOG DEBUG] Log enviado com sucesso! ID: ${result.logged?.log_id || 'N/A'}`);
        } else {
          console.error(`[LOG DEBUG] Erro no servidor:`, result.error);
        }
      } catch (parseError) {
        console.error(`[LOG DEBUG] Erro ao fazer parse da resposta:`, parseError);
        console.error(`[LOG DEBUG] Resposta que causou erro:`, text);
      }
    })
    .catch(error => {
      console.error(`[LOG DEBUG] Erro na requisição:`, error);
      console.error(`[LOG DEBUG] Tipo do erro:`, error.constructor.name);
      console.error(`[LOG DEBUG] Mensagem:`, error.message);
      
      // Log adicional para debugging
      if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
        console.error(`[LOG DEBUG] Possível problema de CORS ou rede`);
      }
    });
    
    // Manter console.log para desenvolvimento local
    console.log(`[${level}] ${message}`, data);
  }
  
  // Expor funções globalmente
  window.logDebug = logDebug;
  
  // generateSessionId agora está no Utils.js
  
  // FASE 0: Teste da funcionalidade de logging
  logDebug('INFO', '[CONFIG] RPA habilitado via PHP Log', {rpaEnabled: window.rpaEnabled});
</script>
<!-- ====================== -->

<!-- ====================== -->
<!-- 🎯 CARREGAMENTO DINÂMICO RPA -->
<script>
// Função para carregar script RPA dinamicamente
function loadRPAScript() {
  return new Promise((resolve, reject) => {
    // Verificar se já foi carregado
    if (window.MainPage && window.ProgressModalRPA) {
      console.log('🎯 Script RPA já carregado');
      resolve();
      return;
    }

    console.log('🎯 Carregando script RPA...');
    
    const script = document.createElement('script');
    script.src = 'https://mdmidia.com.br/webflow_injection_limpo.js';
    script.onload = () => {
      console.log('✅ Script RPA carregado com sucesso');
      resolve();
    };
    script.onerror = () => {
      console.error('❌ Erro ao carregar script RPA');
      reject(new Error('Falha ao carregar script RPA'));
    };
    document.head.appendChild(script);
  });
}

// Expor função globalmente
window.loadRPAScript = loadRPAScript;
</script>
<!-- ====================== -->

<!-- ====================== -->
<!-- WhatsApp links com GCLID -->
<script>
  // readCookie agora está no Utils.js
  // Aguardar Utils.js carregar antes de usar
  var gclid = null;
  
  function initGCLID() {
    if (typeof window.readCookie === 'function') {
      gclid = window.readCookie('gclid');
    } else {
      // Fallback se Utils.js não carregou
      console.warn('⚠️ [FOOTER] readCookie não disponível, tentando novamente...');
      setTimeout(initGCLID, 100);
    }
  }
  
  // Tentar inicializar imediatamente ou aguardar carregamento do Utils
  if (typeof window.readCookie === 'function') {
    gclid = window.readCookie('gclid');
  } else {
    window.addEventListener('footerUtilsLoaded', initGCLID);
    setTimeout(initGCLID, 500); // Fallback após 500ms
  }

  // Função para carregar modal dinamicamente
  function loadWhatsAppModal() {
    if (window.whatsappModalLoaded) {
      console.log('✅ [MODAL] Modal já carregado');
      return;
    }
    
    console.log('🔄 [MODAL] Carregando modal de dev.bpsegurosimediato.com.br...');
    const script = document.createElement('script');
    script.src = 'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=23&force=' + Math.random();
    script.onload = function() {
      window.whatsappModalLoaded = true;
      console.log('✅ [MODAL] Modal carregado com sucesso');
    };
    script.onerror = function() {
      console.error('❌ [MODAL] Erro ao carregar modal');
    };
    document.head.appendChild(script);
  }
  
  $(function () {
    // Interceptar clicks (MANTÉM ESTRUTURA ORIGINAL)
    ['whatsapplink', 'whatsapplinksucesso', 'whatsappfone1', 'whatsappfone2'].forEach(function (id) {
      var $el = $('#' + id);
      if ($el.length) {
        $el.on('click', function (e) {
          e.preventDefault(); // ✅ NOVO: Bloqueia window.open direto
          
          // Se modal já existe, apenas abrir
          if ($('#whatsapp-modal').length) {
            $('#whatsapp-modal').fadeIn(300);
          } else {
            // Modal não existe, carregar
            loadWhatsAppModal();
            
            // Aguardar modal ser criado pelo script
            const checkModal = setInterval(function() {
              if ($('#whatsapp-modal').length) {
                clearInterval(checkModal);
                $('#whatsapp-modal').fadeIn(300);
              }
            }, 100);
            
            // Timeout de 3 segundos
            setTimeout(function() {
              clearInterval(checkModal);
              if ($('#whatsapp-modal').length) {
                $('#whatsapp-modal').fadeIn(300);
              }
            }, 3000);
          }
        });
      }
    });
  });
</script>
<!-- ====================== -->

<!-- ====================== -->
<!-- 🎨 Tema SweetAlert2 (Imediato) + centralização + ícone warning azul -->
<style id="swal2-brand-theme">
  :root {
    --brand-primary: #004A8D; /* azul escuro */
    --brand-accent:  #009FE3; /* azul claro  */
    --brand-text:    #004A8D;
  }

  /* Overlay com leve tint azul e sempre centralizado */
  .swal2-container {
    background-color: rgba(0, 74, 141, 0.35) !important;
    z-index: 99999 !important;
  }
  .swal2-popup {
    border-radius: 14px !important;
    box-shadow: 0 16px 50px rgba(0, 74, 141, 0.25) !important;
    padding-top: 22px !important;
  }
  .swal2-title {
    color: var(--brand-text) !important;
    font-weight: 700 !important;
  }
  .swal2-html-container {
    color: #2b3a4a !important;
    line-height: 1.45 !important;
    text-align: center !important;
    white-space: pre-wrap; /* permite \n */
  }

  /* ========= ÍCONES ========= */
  /* WARNING → círculo azul escuro, borda igual, ponto de exclamação branco */
  .swal2-icon.swal2-warning {
    border-color: var(--brand-primary) !important;
    background-color: var(--brand-primary) !important;
    color: #fff !important; /* fallback */
  }
  .swal2-icon.swal2-warning .swal2-icon-content {
    color: #fff !important;  /* ponto de exclamação */
    font-weight: 800 !important;
  }

  /* INFO / SUCCESS (mantêm paleta da marca) */
  .swal2-icon.swal2-info {
    border-color: var(--brand-accent) !important;
    color: var(--brand-accent) !important;
  }
  .swal2-icon.swal2-success {
    border-color: rgba(0,159,227,.35) !important;
    color: var(--brand-accent) !important;
  }

  /* ========= BOTÕES ========= */
  .swal2-actions { gap: 10px !important; }
  .swal2-styled.swal2-cancel {
    color: var(--brand-primary) !important;
    background: #fff !important;
    border: 2px solid var(--brand-primary) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    min-width: 170px !important;
    padding: 10px 16px !important;
  }
  .swal2-styled.swal2-confirm {
    color: #fff !important;
    background: linear-gradient(180deg, var(--brand-accent) 0%, var(--brand-primary) 100%) !important;
    border: 0 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    min-width: 170px !important;
    padding: 10px 16px !important;
  }
</style>
<!-- ====================== -->

<!-- ====================== -->
<!-- Validações unificadas: CPF, CEP, PLACA, CELULAR, E-MAIL -->
<script>
/* ========= CONFIG ========= */
// Constantes agora estão definidas ANTES do Utils.js (linha ~38)
// Valores expostos globalmente via window.USE_PHONE_API, window.APILAYER_KEY, etc.

/* ========= VALIDAÇÃO API ========= */
// validarCPFApi, validarCepViaCep, validarPlacaApi, validarCelularApi, 
// validarTelefoneAsync, validarEmailSafetyMails agora estão no Utils.js

/* ========= LOADING ========= */
// initLoading, showLoading, hideLoading agora estão no Utils.js

/* ========= HELPERS ========= */
// onlyDigits, toUpperNospace, nativeSubmit e setFieldValue agora estão no Utils.js

/* ========= CPF + API PH3A ========= */
// validarCPFFormato, validarCPFAlgoritmo e extractDataFromPH3A agora estão no Utils.js
// validarCPFApi agora está no Utils.js

// Função de compatibilidade para código existente
function validarCPF(cpf){
  return typeof window.validarCPFAlgoritmo === 'function' ? window.validarCPFAlgoritmo(cpf) : false;
}

/* ========= CEP (ViaCEP) ========= */
// preencherEnderecoViaCEP agora está no Utils.js
// validarCepViaCep agora está no Utils.js

/* ========= PLACA ========= */
// toUpperNospace, onlyDigits (duplicação removida), validarPlacaFormato e extractVehicleFromPlacaFipe agora estão no Utils.js
// validarPlacaApi agora está no Utils.js

// Função de compatibilidade para código existente
function validarPlaca(placa) {
  return typeof window.validarPlacaApi === 'function' ? window.validarPlacaApi(placa) : Promise.resolve({ok: false});
}

/* ========= CELULAR ========= */
/* Máscara jQuery Mask (sem limpar incompletos). Valida apenas no blur do CELULAR. */
// validarCelularLocal agora está no Utils.js
// validarCelularApi e validarTelefoneAsync agora estão no Utils.js

/* ========= E-MAIL ========= */
/* Bloqueio: apenas regex. SafetyMails: aviso não bloqueante. */
// validarEmailLocal agora está no Utils.js

/* ========= MÁSCARAS ========= */
// aplicarMascaraPlaca agora está no Utils.js

/* ========= BOOT ========= */
// ✅ Função de inicialização que aguarda Utils.js carregar
function initValidacoes() {
  // Campos
  const $CPF   = $('#CPF, [name="CPF"]');
  const $CEP   = $('#CEP, [name="CEP"]');
  const $PLACA = $('#PLACA, [name="PLACA"]');
  const $MARCA = $('#MARCA, [name="MARCA"]');
  const $ANO   = $('#ANO, [name="ANO"]');
  const $DDD   = $('#DDD-CELULAR, [name="DDD-CELULAR"]');
  const $CEL   = $('#CELULAR, [name="CELULAR"]');
  const $EMAIL = $('#email, [name="email"], #EMAIL, [name="EMAIL"]');

  // Máscaras
  if ($CPF.length)   $CPF.mask('000.000.000-00');
  if ($CEP.length)   $CEP.mask('00000-000');
  // PLACA: Aplicar máscara quando Utils.js carregar ou imediatamente se já disponível
  function aplicarMascaraPlacaSeDisponivel() {
    if ($PLACA.length && typeof window.aplicarMascaraPlaca === 'function') {
      window.aplicarMascaraPlaca($PLACA);
    } else if ($PLACA.length) {
      // Se campo existe mas função não está disponível, tentar novamente quando Utils carregar
      console.log('⏳ [FOOTER] Aguardando Utils.js para aplicar máscara de placa...');
      window.addEventListener('footerUtilsLoaded', function aplicarAposUtilsCarregar() {
        if ($PLACA.length && typeof window.aplicarMascaraPlaca === 'function') {
          window.aplicarMascaraPlaca($PLACA);
          window.removeEventListener('footerUtilsLoaded', aplicarAposUtilsCarregar);
          console.log('✅ [FOOTER] Máscara de placa aplicada após Utils.js carregar');
        }
      }, { once: true });
      // Fallback: tentar após delay se evento não disparar
      setTimeout(function() {
        if ($PLACA.length && typeof window.aplicarMascaraPlaca === 'function' && !$PLACA.data('mask')) {
          window.aplicarMascaraPlaca($PLACA);
          console.log('✅ [FOOTER] Máscara de placa aplicada via fallback timeout');
        }
      }, 1000);
    }
  }
  aplicarMascaraPlacaSeDisponivel();
  if ($DDD.length)   $DDD.off('.siPhone').mask('00', { clearIfNotMatch:false });
  if ($CEL.length)   $CEL.off('.siPhone').mask('00000-0000', { clearIfNotMatch:false });

  // ============ Helpers de Alert (SweetAlert2) ============
  function saWarnConfirmCancel(opts) {
    return Swal.fire(Object.assign({
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Corrigir',
      cancelButtonText: 'Não',
      reverseButtons: true,
      allowOutsideClick: false,
      allowEscapeKey: true
    }, opts));
  }
  function saInfoConfirmCancel(opts) {
    return Swal.fire(Object.assign({
      icon: 'info',
      showCancelButton: true,
      confirmButtonText: 'Prosseguir assim mesmo',
      cancelButtonText: 'Corrigir',
      reverseButtons: true,
      allowOutsideClick: false,
      allowEscapeKey: true
    }, opts));
  }

  // CPF → change (com/sem API PH3A)
  $CPF.on('change', function(){
    const cpfValue = $(this).val();
    
    // Validação local primeiro
    if (typeof window.validarCPFAlgoritmo !== 'function') {
      console.error('❌ [FOOTER] validarCPFAlgoritmo não disponível');
      return;
    }
    if (!window.validarCPFAlgoritmo(cpfValue)) {
      saWarnConfirmCancel({
        title: 'CPF inválido',
        html: 'Deseja corrigir?'
      }).then(r => { 
        if (r.isConfirmed) $CPF.focus(); 
      });
      return;
    }
    
    // Se flag VALIDAR_PH3A estiver desabilitada, apenas validar formato
    if (typeof window.VALIDAR_PH3A !== 'undefined' && !window.VALIDAR_PH3A) {
      // CPF válido, mas sem consulta à API - limpar campos para preenchimento manual
      if (typeof window.setFieldValue === 'function') {
        window.setFieldValue('SEXO', '');
        window.setFieldValue('DATA-DE-NASCIMENTO', '');
        window.setFieldValue('ESTADO-CIVIL', '');
      }
      return;
    }
    
    // Se CPF válido e flag ativa, consultar API PH3A
    if (typeof window.showLoading === 'function') window.showLoading('Consultando dados do CPF…');
    if (typeof window.validarCPFApi === 'function') {
      window.validarCPFApi(cpfValue).then(res => {
        if (typeof window.hideLoading === 'function') window.hideLoading();
      
      if (res.ok && res.parsed && typeof window.setFieldValue === 'function') {
        // Preencher campos automaticamente
        if (res.parsed.sexo) window.setFieldValue('SEXO', res.parsed.sexo);
        if (res.parsed.dataNascimento) window.setFieldValue('DATA-DE-NASCIMENTO', res.parsed.dataNascimento);
        if (res.parsed.estadoCivil) window.setFieldValue('ESTADO-CIVIL', res.parsed.estadoCivil);
      } else if (res.reason === 'nao_encontrado') {
        // CPF válido mas não encontrado na base
        saInfoConfirmCancel({
          title: 'CPF não encontrado',
          html: 'O CPF é válido, mas não foi encontrado na nossa base de dados.<br><br>Deseja preencher os dados manualmente?'
        }).then(r => {
          if (r.isConfirmed) {
            // Limpar campos e permitir preenchimento manual
            if (typeof window.setFieldValue === 'function') {
              window.setFieldValue('SEXO', '');
              window.setFieldValue('DATA-DE-NASCIMENTO', '');
              window.setFieldValue('ESTADO-CIVIL', '');
            }
          }
        });
      }
      }).catch(_ => {
        if (typeof window.hideLoading === 'function') window.hideLoading();
        // Em caso de erro na API, não bloquear o usuário
        console.log('Erro na consulta da API PH3A');
      });
    } else {
      if (typeof window.hideLoading === 'function') window.hideLoading();
    }
  });

  // CEP → change (ViaCEP)
  $CEP.on('change', function(){
    const val = $(this).val();
    if (typeof window.showLoading === 'function') window.showLoading('Validando CEP…');
    if (typeof window.validarCepViaCep === 'function') {
      window.validarCepViaCep(val).then(res=>{
        if (typeof window.hideLoading === 'function') window.hideLoading();
      if (!res.ok){
        saWarnConfirmCancel({
          title: 'CEP inválido',
          html: 'Deseja corrigir?'
        }).then(r=>{ if (r.isConfirmed) $CEP.focus(); });
      } else if (res.viacep && typeof window.preencherEnderecoViaCEP === 'function'){
        window.preencherEnderecoViaCEP(res.viacep);
      }
      });
    } else {
      if (typeof window.hideLoading === 'function') window.hideLoading();
    }
    }).catch(_=>{
      if (typeof window.hideLoading === 'function') window.hideLoading();
    });
  });

  // PLACA → change (preenche MARCA/ANO/TIPO se ok)
  $PLACA.on('change', function(){
    if (typeof window.showLoading === 'function') window.showLoading('Validando placa…');
    if (typeof window.validarPlacaApi === 'function') {
      window.validarPlacaApi($(this).val()).then(res=>{
        if (typeof window.hideLoading === 'function') window.hideLoading();
      if (!res.ok){
        saWarnConfirmCancel({
          title: 'Placa inválida',
          html: 'Deseja corrigir?'
        }).then(r=>{ if (r.isConfirmed) $PLACA.focus(); });
        if (typeof window.setFieldValue === 'function') {
          window.setFieldValue('MARCA',''); 
          window.setFieldValue('ANO',''); 
          window.setFieldValue('TIPO-DE-VEICULO','');
        }
      } else {
        if (typeof window.setFieldValue === 'function' && res.parsed) {
          if (res.parsed.marcaTxt) window.setFieldValue('MARCA', res.parsed.marcaTxt);
          if (res.parsed.anoModelo) window.setFieldValue('ANO', res.parsed.anoModelo);
          if (res.parsed.tipoVeiculo) window.setFieldValue('TIPO-DE-VEICULO', res.parsed.tipoVeiculo);
        }
      }
      });
    } else {
      if (typeof window.hideLoading === 'function') window.hideLoading();
    }
    }).catch(_=>{
      if (typeof window.hideLoading === 'function') window.hideLoading();
    });
  });

  // CELULAR → valida SÓ no BLUR do CELULAR
  $DDD.off('change'); $CEL.off('change'); // remove handlers antigos
  
  // DDD → valida no BLUR do DDD
  $DDD.on('blur.siPhone', function(){
    if (typeof window.onlyDigits !== 'function') {
      console.error('❌ [FOOTER] onlyDigits não disponível');
      return;
    }
    const dddDigits = window.onlyDigits($DDD.val()).length;
    
    // Se DDD incompleto (não tem 2 dígitos)
    if (dddDigits > 0 && dddDigits < 2) {
      saWarnConfirmCancel({
        title: 'DDD incompleto',
        html: 'O DDD precisa ter 2 dígitos.<br><br>Deseja corrigir?'
      }).then(r=>{ if (r.isConfirmed) $DDD.focus(); });
      return;
    }
    
    // Se DDD inválido (mais de 2 dígitos)
    if (dddDigits > 2) {
      saWarnConfirmCancel({
        title: 'DDD inválido',
        html: 'O DDD deve ter exatamente 2 dígitos.<br><br>Deseja corrigir?'
      }).then(r=>{ if (r.isConfirmed) $DDD.focus(); });
      return;
    }
  });
  
  $CEL.on('blur.siPhone', function(){
    if (typeof window.onlyDigits !== 'function') {
      console.error('❌ [FOOTER] onlyDigits não disponível');
      return;
    }
    const dddDigits = window.onlyDigits($DDD.val()).length;
    const celDigits = window.onlyDigits($CEL.val()).length;

    // Validação DDD: deve ter exatamente 2 dígitos
    if (dddDigits !== 2) {
      saWarnConfirmCancel({
        title: 'DDD inválido',
        html: 'O DDD precisa ter 2 dígitos.<br><br>Deseja corrigir?'
      }).then(r=>{ if (r.isConfirmed) $DDD.focus(); });
      return;
    }

    // Validação Celular: deve ter exatamente 9 dígitos
    if (celDigits > 0 && celDigits < 9) {
      saWarnConfirmCancel({
        title: 'Celular incompleto',
        html: 'O celular precisa ter 9 dígitos.<br><br>Deseja corrigir?'
      }).then(r=>{ if (r.isConfirmed) $CEL.focus(); });
      return;
    }

    // Se DDD=2 e celular=9 → valida via API
    if (dddDigits === 2 && celDigits === 9){
      if (typeof window.showLoading === 'function') window.showLoading('Validando celular…');
      if (typeof window.validarTelefoneAsync === 'function') {
        window.validarTelefoneAsync($DDD,$CEL).then(res=>{
          if (typeof window.hideLoading === 'function') window.hideLoading();
        if (!res.ok){
          const numero = `${($DDD.val()||'').trim()}-${($CEL.val()||'').trim()}`;
          saWarnConfirmCancel({
            title: 'Celular inválido',
            html: `Parece que o celular informado<br><br><b>${numero}</b><br><br>não é válido.<br><br>Deseja corrigir?`
          }).then(r=>{ if (r.isConfirmed) $CEL.focus(); });
        }
        });
      } else {
        if (typeof window.hideLoading === 'function') window.hideLoading();
      }
      }).catch(_=>{
        if (typeof window.hideLoading === 'function') window.hideLoading();
      });
    }
    // Se DDD incompleto ou celular vazio → não valida agora (submit cuida)
  });

  // E-MAIL → change (regex bloqueia; SafetyMails só avisa)
  $EMAIL.on('change.siMail', function(){
    const v = ($(this).val()||'').trim();
    if (!v) return;
    if (typeof window.validarEmailLocal !== 'function') {
      console.error('❌ [FOOTER] validarEmailLocal não disponível');
      return;
    }
    if (!window.validarEmailLocal(v)){
      saWarnConfirmCancel({
        title: 'E-mail inválido',
        html: `O e-mail informado:<br><br><b>${v}</b><br><br>não parece válido.<br><br>Deseja corrigir?`,
        cancelButtonText: 'Não Corrigir',
        confirmButtonText: 'Corrigir'
      }).then(r=>{ if (r.isConfirmed) $EMAIL.focus(); });
      return;
    }
    // Aviso opcional via SafetyMails (não bloqueia)
    if (typeof window.validarEmailSafetyMails === 'function') {
      window.validarEmailSafetyMails(v).then(resp=>{
        if (resp && resp.StatusEmail && resp.StatusEmail !== 'VALIDO'){
          saWarnConfirmCancel({
            title: 'Atenção',
            html: `O e-mail informado:<br><br><b>${v}</b><br><br>pode não ser válido segundo verificador externo.<br><br>Deseja corrigir?`,
            cancelButtonText: 'Manter',
            confirmButtonText: 'Corrigir'
          }).then(r=>{ if (r.isConfirmed) $EMAIL.focus(); });
        }
      }).catch(()=>{ /* silêncio em erro externo */ });
    }
  });


  // CONTROLE MANUAL DO BOTÃO SUBMIT
  $('#submit_button_auto').on('click', function(e) {
    console.log('🎯 [DEBUG] Botão CALCULE AGORA! clicado');
    e.preventDefault(); // Bloquear submit natural para validação
    e.stopPropagation();
    
    // Encontrar o formulário e disparar validação
    const $form = $(this).closest('form');
    if ($form.length) {
      console.log('🔍 [DEBUG] Disparando validação manual do formulário');
      $form.trigger('submit');
    }
  });

  // SUBMIT — revalida tudo e oferece Corrigir / Prosseguir
  $('form').each(function(){
    const $form=$(this);
    
    $form.on('submit', function(ev){
      if ($form.data('validated-ok') === true) { $form.removeData('validated-ok'); return true; }
      if ($form.data('skip-validate') === true){ $form.removeData('skip-validate');  return true; }

      console.log('🔍 [DEBUG] Submit do formulário interceptado');
      ev.preventDefault();
      ev.stopPropagation();
      if (typeof window.showLoading === 'function') window.showLoading('Validando seus dados…');

      Promise.all([
        $CPF.length ? (typeof window.VALIDAR_PH3A !== 'undefined' && window.VALIDAR_PH3A && typeof window.validarCPFApi === 'function' ? window.validarCPFApi($CPF.val()) : Promise.resolve({ok: typeof window.validarCPFAlgoritmo === 'function' ? window.validarCPFAlgoritmo($CPF.val()) : false})) : Promise.resolve({ok: true}),
        $CEP.length   ? (typeof window.validarCepViaCep === 'function' ? window.validarCepViaCep($CEP.val()) : Promise.resolve({ok:true}))  : Promise.resolve({ok:true}),
        $PLACA.length ? (typeof window.validarPlacaApi === 'function' ? window.validarPlacaApi($PLACA.val()) : Promise.resolve({ok:true})) : Promise.resolve({ok:true}),
        // TELEFONE no submit — considera incompleto como inválido
        ($DDD.length && $CEL.length && typeof window.onlyDigits === 'function')
          ? (function(){
              const d = window.onlyDigits($DDD.val()).length;
              const n = window.onlyDigits($CEL.val()).length;
              if (d === 2 && n === 9) return typeof window.validarTelefoneAsync === 'function' ? window.validarTelefoneAsync($DDD,$CEL) : Promise.resolve({ok:true});    // completo → valida API
              if (d === 2 && n > 0 && n < 9) return Promise.resolve({ok:false});  // incompleto → inválido
              return Promise.resolve({ok:false}); // ddd incompleto ou vazio → inválido
            })()
          : Promise.resolve({ok:false}),
        // E-mail: regex (bloqueante)
        $EMAIL.length ? Promise.resolve({ok: typeof window.validarEmailLocal === 'function' ? window.validarEmailLocal(($EMAIL.val()||'').trim()) : false}) : Promise.resolve({ok:true})
      ])
      .then(([cpfRes, cepRes, placaRes, telRes, mailRes])=>{
        if (typeof window.hideLoading === 'function') window.hideLoading();

        // autopreenche MARCA/ANO/TIPO de novo se validou placa
        if (placaRes.ok && placaRes.parsed && typeof window.setFieldValue === 'function'){
          if (placaRes.parsed.marcaTxt) window.setFieldValue('MARCA', placaRes.parsed.marcaTxt);
          if (placaRes.parsed.anoModelo) window.setFieldValue('ANO', placaRes.parsed.anoModelo);
          if (placaRes.parsed.tipoVeiculo) window.setFieldValue('TIPO-DE-VEICULO', placaRes.parsed.tipoVeiculo);
        }

        // autopreenche SEXO/DATA/ESTADO-CIVIL se validou CPF com API
        if (cpfRes.ok && cpfRes.parsed && typeof window.VALIDAR_PH3A !== 'undefined' && window.VALIDAR_PH3A && typeof window.setFieldValue === 'function') {
          if (cpfRes.parsed.sexo) window.setFieldValue('SEXO', cpfRes.parsed.sexo);
          if (cpfRes.parsed.dataNascimento) window.setFieldValue('DATA-DE-NASCIMENTO', cpfRes.parsed.dataNascimento);
          if (cpfRes.parsed.estadoCivil) window.setFieldValue('ESTADO-CIVIL', cpfRes.parsed.estadoCivil);
        }

        const invalido = (!cpfRes.ok) || (!cepRes.ok) || (!placaRes.ok) || (!telRes.ok) || (!mailRes.ok);
        console.log('🔍 [DEBUG] Dados inválidos?', invalido);

        if (!invalido){
          console.log('✅ [DEBUG] Dados válidos - verificando RPA');
          
          // 🎯 CAPTURAR CONVERSÃO GTM - DADOS VÁLIDOS
          console.log('🎯 [GTM] Registrando conversão - dados válidos');
          if (typeof window.dataLayer !== 'undefined') {
            window.dataLayer.push({
              'event': 'form_submit_valid',
              'form_type': 'cotacao_seguro',
              'validation_status': 'valid'
            });
          }
          
          if (window.rpaEnabled === true) {
            console.log('🎯 [RPA] RPA habilitado - iniciando processo RPA');
            window.loadRPAScript()
              .then(() => {
                console.log('🎯 [RPA] Script RPA carregado - executando processo');
                if (window.MainPage && typeof window.MainPage.prototype.handleFormSubmit === 'function') {
                  const mainPageInstance = new window.MainPage();
                  mainPageInstance.handleFormSubmit($form[0]);
                } else {
                  console.warn('🎯 [RPA] Função handleFormSubmit não encontrada - usando fallback');
                  $form.data('validated-ok', true);
                  if (typeof window.nativeSubmit === 'function') {
                    window.nativeSubmit($form);
                  } else {
                    $form[0].submit();
                  }
                }
              })
              .catch((error) => {
                console.error('🎯 [RPA] Erro ao carregar script RPA:', error);
                console.log('🎯 [RPA] Fallback para processamento Webflow');
                $form.data('validated-ok', true);
                if (typeof window.nativeSubmit === 'function') {
                  window.nativeSubmit($form);
                } else {
                  $form[0].submit();
                }
              });
          } else {
            console.log('🎯 [RPA] RPA desabilitado - processando apenas com Webflow');
            $form.data('validated-ok', true);
            if (typeof window.nativeSubmit === 'function') {
              window.nativeSubmit($form);
            } else {
              $form[0].submit();
            }
          }
        } else {
          console.log('❌ [DEBUG] Dados inválidos - mostrando SweetAlert');
          let linhas = "";
          if (!cpfRes.ok)       linhas += "• CPF inválido\n";
          if (!cepRes.ok)   linhas += "• CEP inválido\n";
          if (!placaRes.ok) linhas += "• Placa inválida\n";
          if (!telRes.ok)   linhas += "• Celular inválido\n";
          if (!mailRes.ok)  linhas += "• E-mail inválido\n";

          Swal.fire({
            icon: 'info',
            title: 'Atenção!',
            html:
              "⚠️ Os campos CPF, CEP, PLACA, CELULAR e E-MAIL corretamente preenchidos são necessários para efetuar o cálculo do seguro.\n\n" +
              "Campos com problema:\n\n" + linhas + "\n" +
              "Caso decida prosseguir assim mesmo, um especialista entrará em contato para coletar esses dados.",
            showCancelButton: true,
            confirmButtonText: 'Prosseguir assim mesmo',
            cancelButtonText: 'Corrigir',
            reverseButtons: true,
            allowOutsideClick: false,
            allowEscapeKey: true
          }).then(r=>{
            if (r.isConfirmed){
              console.log('🎯 [RPA] Usuário escolheu prosseguir com dados inválidos');
              
              // 🎯 CAPTURAR CONVERSÃO GTM - USUÁRIO PROSSEGUIU COM DADOS INVÁLIDOS
              console.log('🎯 [GTM] Registrando conversão - usuário prosseguiu com dados inválidos');
              if (typeof window.dataLayer !== 'undefined') {
                window.dataLayer.push({
                  'event': 'form_submit_invalid_proceed',
                  'form_type': 'cotacao_seguro',
                  'validation_status': 'invalid_proceed'
                });
              }
              
              if (window.rpaEnabled === true) {
                console.log('🎯 [RPA] RPA habilitado - iniciando processo RPA com dados inválidos');
                window.loadRPAScript()
                  .then(() => {
                    console.log('🎯 [RPA] Script RPA carregado - executando processo com dados inválidos');
                    if (window.MainPage && typeof window.MainPage.prototype.handleFormSubmit === 'function') {
                      const mainPageInstance = new window.MainPage();
                      mainPageInstance.handleFormSubmit($form[0]);
                    } else {
                      console.warn('🎯 [RPA] Função handleFormSubmit não encontrada - usando fallback');
                      $form.data('skip-validate', true);
                      if (typeof window.nativeSubmit === 'function') {
                        window.nativeSubmit($form);
                      } else {
                        $form[0].submit();
                      }
                    }
                  })
                  .catch((error) => {
                    console.error('🎯 [RPA] Erro ao carregar script RPA:', error);
                    console.log('🎯 [RPA] Fallback para processamento Webflow');
                    $form.data('skip-validate', true);
                    if (typeof window.nativeSubmit === 'function') {
                      window.nativeSubmit($form);
                    } else {
                      $form[0].submit();
                    }
                  });
              } else {
                console.log('🎯 [RPA] RPA desabilitado - processando apenas com Webflow');
                $form.data('skip-validate', true);
                if (typeof window.nativeSubmit === 'function') {
                  window.nativeSubmit($form);
                } else {
                  $form[0].submit();
                }
              }
            } else {
              if (!cpfRes.ok && $CPF.length)        { $CPF.focus(); return; }
              if (!cepRes.ok && $CEP.length)    { $CEP.focus(); return; }
              if (!placaRes.ok && $PLACA.length){ $PLACA.focus(); return; }
              if (!telRes.ok && ($DDD.length && $CEL.length)) { $CEL.focus(); return; }
              if (!mailRes.ok && $EMAIL.length) { $EMAIL.focus(); return; }
            }
          });
        }
      })
      .catch(_=>{
        if (typeof window.hideLoading === 'function') window.hideLoading();
        Swal.fire({
          icon: 'info',
          title: 'Não foi possível validar agora',
          html:  'Deseja prosseguir assim mesmo?',
          showCancelButton: true,
          confirmButtonText: 'Prosseguir assim mesmo',
          cancelButtonText: 'Corrigir',
          reverseButtons: true,
          allowOutsideClick: false,
          allowEscapeKey: true
        }).then(r=>{
          if (r.isConfirmed) { 
            console.log('🎯 [RPA] Usuário escolheu prosseguir após erro de rede');
            
            // 🎯 CAPTURAR CONVERSÃO GTM - USUÁRIO PROSSEGUIU APÓS ERRO DE REDE
            console.log('🎯 [GTM] Registrando conversão - usuário prosseguiu após erro de rede');
            if (typeof window.dataLayer !== 'undefined') {
              window.dataLayer.push({
                'event': 'form_submit_network_error_proceed',
                'form_type': 'cotacao_seguro',
                'validation_status': 'network_error_proceed'
              });
            }
            
            if (window.rpaEnabled === true) {
              console.log('🎯 [RPA] RPA habilitado - iniciando processo RPA após erro de rede');
              window.loadRPAScript()
                .then(() => {
                  console.log('🎯 [RPA] Script RPA carregado - executando processo após erro de rede');
                  if (window.MainPage && typeof window.MainPage.prototype.handleFormSubmit === 'function') {
                    const mainPageInstance = new window.MainPage();
                    mainPageInstance.handleFormSubmit($form[0]);
                  } else {
                    console.warn('🎯 [RPA] Função handleFormSubmit não encontrada - usando fallback');
                    $form.data('skip-validate', true);
                    if (typeof window.nativeSubmit === 'function') {
                      window.nativeSubmit($form);
                    } else {
                      $form[0].submit();
                    }
                  }
                })
                .catch((error) => {
                  console.error('🎯 [RPA] Erro ao carregar script RPA:', error);
                  console.log('🎯 [RPA] Fallback para processamento Webflow');
                  $form.data('skip-validate', true);
                  if (typeof window.nativeSubmit === 'function') {
                    window.nativeSubmit($form);
                  } else {
                    $form[0].submit();
                  }
                });
            } else {
              console.log('🎯 [RPA] RPA desabilitado - processando apenas com Webflow');
              $form.data('skip-validate', true);
              if (typeof window.nativeSubmit === 'function') {
                window.nativeSubmit($form);
              } else {
                $form[0].submit();
              }
            }
          }
        });
      });
    });
  });
}

// ✅ Aguardar Utils.js carregar antes de inicializar validações
// IMPORTANTE: Executar DEPOIS que tudo carregar, incluindo Utils.js
function waitForUtilsAndInit() {
  // Verificar se Utils já carregou com múltiplas funções críticas
  if (typeof window.showLoading === 'function' && 
      typeof window.validarEmailLocal === 'function' && 
      typeof window.validarCPFAlgoritmo === 'function' &&
      typeof window.onlyDigits === 'function') {
    console.log('✅ [FOOTER] Utils.js já carregado, inicializando validações imediatamente');
    initValidacoes();
    return true;
  }
  return false;
}

// Tentar inicializar quando DOM estiver pronto
$(function () {
  // Verificar imediatamente se já carregou
  if (waitForUtilsAndInit()) {
    return; // Já inicializou, sair
  }
  
  console.log('⏳ [FOOTER] Aguardando Utils.js carregar antes de inicializar validações...');
  
  // Aguardar evento de carregamento (disparado quando Utils.js carrega)
  const initOnUtilsLoad = function() {
    console.log('✅ [FOOTER] Utils.js carregado (evento footerUtilsLoaded), inicializando validações');
    if (!waitForUtilsAndInit()) {
      console.warn('⚠️ [FOOTER] Utils.js evento disparado mas funções ainda não disponíveis');
      console.warn('⚠️ [FOOTER] Disponíveis:', {
        showLoading: typeof window.showLoading,
        validarEmailLocal: typeof window.validarEmailLocal,
        validarCPFAlgoritmo: typeof window.validarCPFAlgoritmo,
        onlyDigits: typeof window.onlyDigits
      });
    }
  };
  window.addEventListener('footerUtilsLoaded', initOnUtilsLoad, { once: true });
  
  // Fallback 1: Verificar após 100ms (pode já ter carregado)
  setTimeout(function() {
    if (waitForUtilsAndInit()) {
      window.removeEventListener('footerUtilsLoaded', initOnUtilsLoad);
    }
  }, 100);
  
  // Fallback 2: Verificar após 500ms
  setTimeout(function() {
    if (waitForUtilsAndInit()) {
      window.removeEventListener('footerUtilsLoaded', initOnUtilsLoad);
    }
  }, 500);
  
  // Fallback 3: Tentar após delay maior se evento não disparar
  setTimeout(function() {
    if (!waitForUtilsAndInit()) {
      console.error('❌ [FOOTER] Utils.js não carregou após timeout - validações podem não funcionar');
      console.error('❌ [FOOTER] Funções disponíveis:', {
        showLoading: typeof window.showLoading,
        validarEmailLocal: typeof window.validarEmailLocal,
        validarCPFAlgoritmo: typeof window.validarCPFAlgoritmo,
        onlyDigits: typeof window.onlyDigits,
        validarCPFApi: typeof window.validarCPFApi,
        validarCepViaCep: typeof window.validarCepViaCep
      });
    }
  }, 3000);
});
</script>
<!-- ====================== -->

<script>
window.Webflow ||= [];
window.Webflow.push(() => {
  const LIST = document.querySelector('#Equipes-list');        // ID da Collection List (Equipes)
  const OUT  = document.getElementById('qtde_colaboradores');  // seu elemento de texto

  const isVisible = (el) => {
    const st = getComputedStyle(el);
    return el.offsetParent !== null && st.display !== 'none' && st.visibility !== 'hidden' && st.opacity !== '0';
  };

  const recalc = () => {
    const n = LIST ? [...LIST.querySelectorAll('.w-dyn-item')].filter(isVisible).length : 0;
    if (OUT) OUT.textContent = String(n);
  };

  recalc(); // na carga

  // Atualiza em mudanças (filtros/paginação/dinâmicas)
  if (LIST) new MutationObserver(recalc).observe(LIST, {
    childList: true, subtree: true, attributes: true, attributeFilter: ['style','class']
  });
  document.addEventListener('fs-cmsfilter-update', recalc);       // Finsweet
  document.addEventListener('jetboost:filter:applied', recalc);    // Jetboost
  document.addEventListener('jetboost:pagination:loaded', recalc); // Jetboost
});
</script>
<!-- ====================== -->
<!-- 🔍 DEBUG: VERIFICAÇÃO DE INJEÇÃO RPA -->
<script>
console.log('🔍 [DEBUG] Iniciando verificação de injeção RPA...');

// Função para verificar se a injeção foi bem-sucedida
function debugRPAModule() {
  console.log('🔍 [DEBUG] === VERIFICAÇÃO DE INJEÇÃO RPA ===');
  
  // 1. Verificar se window.rpaEnabled existe
  if (typeof window.rpaEnabled !== 'undefined') {
    console.log('✅ [DEBUG] window.rpaEnabled encontrado:', window.rpaEnabled);
  } else {
    console.error('❌ [DEBUG] window.rpaEnabled NÃO encontrado!');
  }
  
  // 2. Verificar se loadRPAScript existe
  if (typeof window.loadRPAScript === 'function') {
    console.log('✅ [DEBUG] window.loadRPAScript encontrado');
  } else {
    console.error('❌ [DEBUG] window.loadRPAScript NÃO encontrado!');
  }
  
  // 3. Verificar se jQuery está disponível
  if (typeof $ !== 'undefined') {
    console.log('✅ [DEBUG] jQuery disponível:', $.fn.jquery);
  } else {
    console.error('❌ [DEBUG] jQuery NÃO disponível!');
  }
  
  // 4. Verificar se SweetAlert2 está disponível
  if (typeof Swal !== 'undefined') {
    console.log('✅ [DEBUG] SweetAlert2 disponível');
  } else {
    console.warn('⚠️ [DEBUG] SweetAlert2 NÃO disponível (pode ser carregado dinamicamente)');
  }
  
  // 5. Verificar conflitos de nomes de função
  const globalFunctions = Object.keys(window).filter(key => typeof window[key] === 'function');
  const rpaFunctions = globalFunctions.filter(func => func.toLowerCase().includes('rpa') || func.toLowerCase().includes('load'));
  console.log('🔍 [DEBUG] Funções globais relacionadas ao RPA:', rpaFunctions);
  
  // 6. Verificar se há elementos de formulário
  const forms = document.querySelectorAll('form');
  console.log('🔍 [DEBUG] Formulários encontrados:', forms.length);
  
  // 7. Verificar se há botões de submit
  const submitButtons = document.querySelectorAll('button[type="submit"], input[type="submit"]');
  console.log('🔍 [DEBUG] Botões de submit encontrados:', submitButtons.length);
  
  console.log('🔍 [DEBUG] === FIM DA VERIFICAÇÃO ===');
}

// Função para testar carregamento dinâmico
function testDynamicLoading() {
  console.log('🔍 [DEBUG] Testando carregamento dinâmico...');
  
  if (typeof window.loadRPAScript === 'function') {
    console.log('🔍 [DEBUG] Tentando carregar script RPA...');
    
    window.loadRPAScript()
      .then(() => {
        console.log('✅ [DEBUG] Script RPA carregado com sucesso!');
        
        // Verificar se as classes RPA foram carregadas
        if (typeof window.MainPage !== 'undefined') {
          console.log('✅ [DEBUG] window.MainPage disponível');
        } else {
          console.error('❌ [DEBUG] window.MainPage NÃO disponível após carregamento');
        }
        
        if (typeof window.ProgressModalRPA !== 'undefined') {
          console.log('✅ [DEBUG] window.ProgressModalRPA disponível');
        } else {
          console.error('❌ [DEBUG] window.ProgressModalRPA NÃO disponível após carregamento');
        }
        
        if (typeof window.SpinnerTimer !== 'undefined') {
          console.log('✅ [DEBUG] window.SpinnerTimer disponível');
        } else {
          console.error('❌ [DEBUG] window.SpinnerTimer NÃO disponível após carregamento');
        }
        
      })
      .catch(error => {
        console.error('❌ [DEBUG] Erro ao carregar script RPA:', error);
      });
  } else {
    console.error('❌ [DEBUG] window.loadRPAScript não está disponível para teste');
  }
}

// Função para detectar conflitos
function detectConflicts() {
  console.log('🔍 [DEBUG] === DETECÇÃO DE CONFLITOS ===');
  
  // Verificar se há múltiplas definições de funções
  const functionNames = [];
  const scripts = document.querySelectorAll('script');
  
  scripts.forEach((script, index) => {
    if (script.textContent) {
      const content = script.textContent;
      
      // Pular scripts que contêm apenas código de debug (evitar detectar a si mesmo)
      if (content.includes('detectConflicts') && content.includes('DEBUG] === DETECÇÃO DE CONFLITOS ===')) {
        return; // Pular este script
      }
      
      // Verificar se há DEFINIÇÕES reais de loadRPAScript (não apenas menções)
      if (content.includes('window.loadRPAScript =') || content.includes('function loadRPAScript(')) {
        functionNames.push(`Script ${index + 1}: loadRPAScript`);
      }
      
      // Verificar se há DEFINIÇÕES reais de rpaEnabled (não apenas menções)
      if (content.includes('window.rpaEnabled =') || content.includes('var rpaEnabled') || content.includes('let rpaEnabled') || content.includes('const rpaEnabled')) {
        functionNames.push(`Script ${index + 1}: rpaEnabled`);
      }
    }
  });
  
  if (functionNames.length > 1) {
    console.warn('⚠️ [DEBUG] Possível conflito detectado - múltiplas definições:', functionNames);
  } else {
    console.log('✅ [DEBUG] Nenhum conflito de múltiplas definições detectado');
  }
  
  // Verificar se há erros no console
  const originalError = console.error;
  const errors = [];
  console.error = function(...args) {
    errors.push(args.join(' '));
    originalError.apply(console, args);
  };
  
  setTimeout(() => {
    console.error = originalError;
    if (errors.length > 0) {
      console.warn('⚠️ [DEBUG] Erros detectados durante inicialização:', errors);
    } else {
      console.log('✅ [DEBUG] Nenhum erro detectado durante inicialização');
    }
  }, 2000);
  
  console.log('🔍 [DEBUG] === FIM DA DETECÇÃO DE CONFLITOS ===');
}

// Executar verificações após DOM estar pronto
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    setTimeout(debugRPAModule, 100);
    setTimeout(detectConflicts, 200);
  });
} else {
  setTimeout(debugRPAModule, 100);
  setTimeout(detectConflicts, 200);
}

// Expor funções de debug globalmente para teste manual
window.debugRPAModule = debugRPAModule;
window.testDynamicLoading = testDynamicLoading;
window.detectConflicts = detectConflicts;

console.log('🔍 [DEBUG] Funções de debug disponíveis:');
console.log('  - window.debugRPAModule()');
console.log('  - window.testDynamicLoading()');
console.log('  - window.detectConflicts()');
</script>
<!-- ====================== -->
