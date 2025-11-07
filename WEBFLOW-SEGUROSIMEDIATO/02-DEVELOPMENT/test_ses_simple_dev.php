<?php
require_once 'send_admin_notification_ses.php';
echo \ Testando SES...\n\;
\ = ['ddd' => '11', 'celular' => '987654321', 'nome' => 'Teste'];
\ = enviarNotificacaoAdministradores(\);
print_r(\);
