<?php
/**
 * TESTE AWS SES - Produção
 * Testar envio de email para administradores
 */

require_once __DIR__ . '/send_admin_notification_ses.php';

echo "=== TESTE AWS SES ===\n\n";

$dados_teste = [
    'ddd' => '11',
    'celular' => '987654321',
    'cpf' => '123.456.789-00',
    'nome' => 'Teste Sistema SES',
    'email' => 'teste@email.com',
    'cep' => '01234-567',
    'placa' => 'TEST1234',
    'gclid' => 'test-gclid-123',
];

echo "Dados de teste:\n";
print_r($dados_teste);
echo "\n";

echo "Enviando email...\n";
$resultado = enviarNotificacaoAdministradores($dados_teste);

echo "\n=== RESULTADO ===\n";
print_r($resultado);

if ($resultado['success']) {
    echo "\n✅ SUCESSO! Email enviado para {$resultado['total_sent']} administrador(es)\n";
    echo "Verifique a caixa de entrada de " . implode(', ', ADMIN_EMAILS) . "\n";
} else {
    echo "\n❌ ERRO ao enviar email:\n";
    echo "Erro: " . ($resultado['error'] ?? 'Desconhecido') . "\n";
    if (isset($resultado['code'])) {
        echo "Código: " . $resultado['code'] . "\n";
    }
}


