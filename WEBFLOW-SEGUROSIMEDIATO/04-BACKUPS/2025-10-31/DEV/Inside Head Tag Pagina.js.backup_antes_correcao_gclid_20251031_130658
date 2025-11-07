/**
 * PROJETO: CORREÇÃO NA DEFINIÇÃO DOS CAMPOS GCLID
 * INÍCIO: 31/10/2025 13:06
 * ÚLTIMA ALTERAÇÃO: 31/10/2025 13:06
 * 
 * VERSÃO: 1.1 - Correção na definição dos campos gclid
 * 
 * ALTERAÇÕES NESTA VERSÃO:
 * - Implementada verificação defensiva antes de acessar propriedade .value
 * - Adicionada validação de existência de elementos antes de ler valores
 * - Correção do erro "Cannot read properties of null (reading 'value')"
 * - Salvamento no localStorage apenas quando valores são válidos
 * 
 * ARQUIVOS RELACIONADOS:
 * - INVESTIGACAO_ERRO_CONSOLE_GCLID.md (documentação do problema)
 * 
 * LOCAIS DE USO:
 * - Webflow: Head Code (Inside <head> tag)
 * - Servidor DEV: https://dev.bpsegurosimediato.com.br/webhooks/InsideHeadTagPagina.js
 */
<script type="text/javascript">
  function setCookie(name, value, days) {
    var date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    var expires = "; expires=" + date.toUTCString(); // Atualizado para padrão moderno
    document.cookie = name + "=" + value + expires + ";path=/";
  }

  function getParam(p) {
    var params = new URLSearchParams(window.location.search);
    return params.get(p) ? decodeURIComponent(params.get(p)) : null;
  }

  // Captura gclid OU gbraid (qualquer um dos dois)
  var gclid = getParam("gclid") || getParam("GCLID") || getParam("gclId");
  var gbraid = getParam("gbraid") || getParam("GBRAID") || getParam("gBraid");

  // Define prioridade: se gclid existir, usa ele. Se não, usa gbraid.
  var trackingId = gclid || gbraid;

  if (trackingId) {
    var gclsrc = getParam("gclsrc");
    if (!gclsrc || gclsrc.indexOf("aw") !== -1) {
      setCookie("gclid", trackingId, 90);
    }
  }

  function readCookie(name) {
    var n = name + "=";
    var cookie = document.cookie.split(";");
    for (var i = 0; i < cookie.length; i++) {
      var c = cookie[i].trim();
      if (c.indexOf(n) == 0) {
        return c.substring(n.length, c.length);
      }
    }
    return null;
  }

  document.addEventListener("DOMContentLoaded", function () {
    const gclidFields = document.getElementsByName("GCLID_FLD");
    for (var i = 0; i < gclidFields.length; i++) {
      gclidFields[i].value = readCookie("gclid");
    }

    var anchors = document.querySelectorAll("[whenClicked='set']");
    for (var i = 0; i < anchors.length; i++) {
      anchors[i].onclick = function () {
        // ✅ Verificação defensiva: verificar se elemento existe antes de acessar .value
        var emailEl = document.getElementById("email");
        var gclidEl = document.getElementById("GCLID_FLD");
        var gclidWpEl = document.getElementById("GCLID_FLD_WP");
        
        var global_email = emailEl ? emailEl.value : null;
        var global_gclid = gclidEl ? gclidEl.value : null;
        var global_gclid_wp = gclidWpEl ? gclidWpEl.value : null;
        
        // Só salvar se houver valores válidos
        if (global_gclid) {
          window.localStorage.setItem("GCLID_FLD", global_gclid);
        }
        if (global_gclid_wp) {
          window.localStorage.setItem("GCLID_FLD_WP", global_gclid_wp);
        }
        if (global_email) {
          window.localStorage.setItem("EMAIL_FLD", global_email);
        }
      };
    }
  });
  
  document.addEventListener("DOMContentLoaded", function () {
  var gclidCookie = (document.cookie.match(/(^|;)\s*gclid=([^;]+)/) || [])[2];
  if (gclidCookie) {
    window.CollectChatAttributes = {
      gclid: decodeURIComponent(gclidCookie)
    };
    console.log("GCLID enviado ao Collect.chat:", decodeURIComponent(gclidCookie));
  }
});
  
</script>
