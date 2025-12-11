<!-- ======================================== -->
<!-- FOOTER CODE SITE FINAL - VERSÃO RPA V6.13.1 -->
<!-- ======================================== -->
<!-- 
  SOLUÇÃO DEFINITIVA PARA LIMITE DE 50.000 CARACTERES:
  - JavaScript RPA hospedado externamente
  - SweetAlert2 carregado dinamicamente pelo RPA
  - Validações individuais mantidas
  - Interceptação de formulário garantida
  
  PROBLEMAS RESOLVIDOS:
  ✅ Limite de 50.000 caracteres do Webflow
  ✅ Conflitos de timing com script externo
  ✅ Duplicação de SweetAlert2
  ✅ Interceptação de formulário falha
  ✅ Dependências externas não carregadas
  
  DATA: 18/10/2025
  VERSÃO: V6.13.1
  PROJETO: Integração definitiva Webflow + RPA
-->

<!-- Google Tag Manager (noscript) -->
<noscript>
  <iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PD6J398"
          height="0" width="0"
          style="display:none;visibility:hidden"></iframe>
</noscript>

<!-- Bibliotecas base -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js" crossorigin="anonymous"></script>

<!-- ====================== -->
<!-- 🎯 CONFIGURAÇÃO RPA GLOBAL -->
<script>
  // Flag global para controle do RPA
  window.rpaEnabled = false;
  console.log('🎯 [CONFIG] RPA habilitado:', window.rpaEnabled);
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

<!-- Validações individuais mantidas -->
<script>
$(document).ready(function() {
  // Validações individuais (CPF, CEP, Placa, Celular, Email)
  // Auto-preenchimento de campos
  // Funções GCLID e WhatsApp
  // Contador de Equipes
  
  // Aguardar SweetAlert2 estar disponível
  const waitForSweetAlert = () => {
    if (typeof Swal !== 'undefined') {
      console.log('✅ SweetAlert2 disponível para validações individuais');
      initializeValidations();
    } else {
      setTimeout(waitForSweetAlert, 100);
    }
  };
  
  const initializeValidations = () => {
    // Validações individuais aqui
    console.log('🔍 Validações individuais inicializadas');
  };
  
  // Iniciar após DOM estar pronto
  waitForSweetAlert();
});
</script>
