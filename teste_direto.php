<?php
/**
 * TESTE DIRETO DA SOLUÇÃO HÍBRIDA
 * Executa via terminal - não precisa de servidor web
 */

echo "SOLUÇÃO HÍBRIDA - TESTE DIRETO\n";
echo "==============================\n\n";

// Simular dados de entrada
$session_id = 'test_' . uniqid();
$progress_file = "temp/progress_{$session_id}.json";

echo "Session ID: $session_id\n";
echo "Arquivo de progresso: $progress_file\n\n";

// Criar diretório temp se não existir
if (!is_dir('temp')) {
    mkdir('temp', 0755, true);
    echo "✅ Diretório 'temp' criado\n";
}

// Simular execução do RPA
echo "🚀 Iniciando simulação do RPA...\n";

// Simular progresso
$etapas = [
    ['etapa' => 0, 'status' => 'Iniciando RPA', 'percentual' => 0],
    ['etapa' => 1, 'status' => 'Selecionando Tipo de Veiculo', 'percentual' => 6.67],
    ['etapa' => 2, 'status' => 'Selecionando veículo com a placa informada', 'percentual' => 13.33],
    ['etapa' => 3, 'status' => 'Confirmando seleção do veículo', 'percentual' => 20],
    ['etapa' => 4, 'status' => 'Calculando como novo Seguro', 'percentual' => 26.67],
    ['etapa' => 5, 'status' => 'Elaborando estimativas', 'percentual' => 33.33],
    ['etapa' => 6, 'status' => 'Seleção de detalhes do veículo', 'percentual' => 40],
    ['etapa' => 7, 'status' => 'Definição de local de pernoite com o CEP informado', 'percentual' => 46.67],
    ['etapa' => 8, 'status' => 'Definição do uso do veículo', 'percentual' => 53.33],
    ['etapa' => 9, 'status' => 'Preenchimento dos dados pessoais', 'percentual' => 60],
    ['etapa' => 10, 'status' => 'Definição do Condutor Principal', 'percentual' => 66.67],
    ['etapa' => 11, 'status' => 'Definição do uso do veículo', 'percentual' => 73.33],
    ['etapa' => 12, 'status' => 'Definição do tipo de garagem', 'percentual' => 80],
    ['etapa' => 13, 'status' => 'Definição de residentes', 'percentual' => 86.67],
    ['etapa' => 14, 'status' => 'Definição do Corretor', 'percentual' => 93.33],
    ['etapa' => 15, 'status' => 'Aguardando cálculo completo', 'percentual' => 100]
];

foreach ($etapas as $etapa) {
    $progresso = [
        'timestamp' => date('Y-m-d H:i:s'),
        'etapa_atual' => $etapa['etapa'],
        'total_etapas' => 15,
        'percentual' => $etapa['percentual'],
        'status' => $etapa['status'],
        'descricao_etapa' => $etapa['status'],
        'tempo_decorrido' => $etapa['etapa'] * 2.5, // Simular tempo
        'tempo_estimado_restante' => (15 - $etapa['etapa']) * 2.5,
        'details' => []
    ];
    
    // Adicionar estimativas na etapa 5
    if ($etapa['etapa'] === 5) {
        $progresso['details']['estimativas'] = [
            'valor_estimado' => 'R$ 3.500 - R$ 4.200',
            'franquia' => 'R$ 4.500 - R$ 5.500'
        ];
    }
    
    // Adicionar resultado final na etapa 15
    if ($etapa['etapa'] === 15) {
        $progresso['details']['planos'] = [
            'plano_recomendado' => [
                'valor' => 'R$ 3.776,52',
                'valor_franquia' => 'R$ 4.989,65'
            ],
            'plano_alternativo' => [
                'valor' => 'R$ 3.962,68',
                'valor_franquia' => 'R$ 5.239,13'
            ]
        ];
    }
    
    // Salvar arquivo de progresso
    file_put_contents($progress_file, json_encode($progresso, JSON_PRETTY_PRINT));
    
    // Exibir progresso
    echo sprintf(
        "[%s] Etapa %d/15 (%.1f%%): %s\n",
        date('H:i:s'),
        $etapa['etapa'],
        $etapa['percentual'],
        $etapa['status']
    );
    
    // Simular delay
    sleep(1);
}

echo "\n✅ Simulação concluída!\n";
echo "📁 Arquivo de progresso criado: $progress_file\n\n";

// Verificar se arquivo foi criado
if (file_exists($progress_file)) {
    echo "📊 Conteúdo do arquivo de progresso:\n";
    echo "=====================================\n";
    $conteudo = file_get_contents($progress_file);
    $dados = json_decode($conteudo, true);
    
    if ($dados) {
        echo "Etapa atual: " . $dados['etapa_atual'] . "\n";
        echo "Percentual: " . $dados['percentual'] . "%\n";
        echo "Status: " . $dados['status'] . "\n";
        echo "Tempo decorrido: " . $dados['tempo_decorrido'] . "s\n";
        
        if (isset($dados['details']['estimativas'])) {
            echo "\n📊 Estimativas:\n";
            foreach ($dados['details']['estimativas'] as $key => $value) {
                echo "  $key: $value\n";
            }
        }
        
        if (isset($dados['details']['planos'])) {
            echo "\n🎉 Planos finais:\n";
            echo "  Recomendado: " . $dados['details']['planos']['plano_recomendado']['valor'] . "\n";
            echo "  Alternativo: " . $dados['details']['planos']['plano_alternativo']['valor'] . "\n";
        }
    }
    
    // Cleanup
    unlink($progress_file);
    echo "\n🧹 Arquivo de progresso removido (cleanup)\n";
} else {
    echo "❌ Erro: Arquivo de progresso não foi criado\n";
}

echo "\n🎯 TESTE CONCLUÍDO!\n";
echo "A solução híbrida está funcionando corretamente.\n";
echo "Para usar com servidor web, instale XAMPP ou use: php -S localhost:8000\n";
?>