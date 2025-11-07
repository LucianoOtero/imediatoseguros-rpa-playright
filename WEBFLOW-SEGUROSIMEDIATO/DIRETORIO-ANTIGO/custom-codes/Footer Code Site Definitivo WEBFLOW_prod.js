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
<!-- Script Unificado - Footer Code Completo (PRODUÇÃO) -->
<!-- TEMPORÁRIO: Usando diretório dev enquanto corrigimos nginx de produção -->
<script src="https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js?v=1.3" defer></script>
<!-- ====================== -->




