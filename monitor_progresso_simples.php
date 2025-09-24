<?php
/**
 * MONITOR DE PROGRESSO EM TEMPO REAL - FASE 3 (CORRIGIDO)
 * Executa RPA e monitora progresso passo a passo
 */

class MonitorProgressoTempoReal {
    
    private $arquivo_config = "monitor_progress.json";
    private $arquivo_resultado = "monitor_resultado.json";
    private $arquivo_progresso = "temp/progress_status.json";
    private $timeout = 300; // 5 minutos
    
    public function __construct() {
        echo "🔍 MONITOR DE PROGRESSO EM TEMPO REAL - FASE 3\n";
        echo "==============================================\n\n";
    }
    
    /**
     * Criar configuração para monitoramento
     */
    public function criarConfiguracao() {
        echo "📁 Criando configuração de monitoramento...\n";
        
        $config = [
            "configuracao" => [
                "log" => true,
                "display" => true,
                "log_rotacao_dias" => 90,
                "log_nivel" => "INFO",
                "tempo_estabilizacao" => 0.5,
                "tempo_carregamento" => 0.5,
                "tempo_estabilizacao_tela5" => 2,
                "tempo_carregamento_tela5" => 5,
                "tempo_estabilizacao_tela15" => 3,
                "tempo_carregamento_tela15" => 5,
                "inserir_log" => true,
                "visualizar_mensagens" => false, // Modo silencioso
                "eliminar_tentativas_inuteis" => true
            ],
            "autenticacao" => [
                "email_login" => "aleximediatoseguros@gmail.com",
                "senha_login" => "Lrotero1$",
                "manter_login_atual" => true
            ],
            "url" => "https://www.app.tosegurado.com.br/imediatosolucoes",
            "tipo_veiculo" => "carro",
            "placa" => "EYQ4J41",
            "marca" => "TOYOTA",
            "modelo" => "COROLLA XEI 1.8/1.8 FLEX 16V MEC",
            "ano" => "2009",
            "zero_km" => false,
            "combustivel" => "Flex",
            "veiculo_segurado" => "Não",
            "cep" => "03317-000",
            "endereco_completo" => "Rua Serra de Botucatu, 410 APTO 11 - São Paulo, SP",
            "uso_veiculo" => "Pessoal",
            "nome" => "ALEX KAMINSKI",
            "cpf" => "97137189768",
            "data_nascimento" => "25/04/1970",
            "sexo" => "Masculino",
            "estado_civil" => "Casado ou Uniao Estavel",
            "email" => "alex.kaminski@imediatoseguros.com.br",
            "celular" => "11953288466",
            "endereco" => "Rua Serra de Botucatu, Tatuapé - São Paulo/SP",
            "condutor_principal" => true,
            "nome_condutor" => "SANDRA LOUREIRO",
            "cpf_condutor" => "25151787829",
            "data_nascimento_condutor" => "28/08/1975",
            "sexo_condutor" => "Feminino",
            "estado_civil_condutor" => "Casado ou Uniao Estavel",
            "local_de_trabalho" => false,
            "estacionamento_proprio_local_de_trabalho" => false,
            "local_de_estudo" => false,
            "estacionamento_proprio_local_de_estudo" => false,
            "garagem_residencia" => true,
            "portao_eletronico" => "Eletronico",
            "reside_18_26" => "Não",
            "sexo_do_menor" => "N/A",
            "faixa_etaria_menor_mais_novo" => "N/A",
            "kit_gas" => false,
            "blindado" => false,
            "financiado" => false,
            "continuar_com_corretor_anterior" => true
        ];
        
        file_put_contents($this->arquivo_config, json_encode($config, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        echo "✅ Arquivo criado: {$this->arquivo_config}\n\n";
    }
    
    /**
     * Executar RPA e capturar resultado diretamente
     */
    public function executarRPADireto() {
        echo "🚀 Executando RPA diretamente...\n";
        echo "⏰ Início: " . date("H:i:s") . "\n\n";
        
        $comando = "python executar_rpa_imediato_playwright.py --config {$this->arquivo_config}";
        
        echo "📋 Comando: $comando\n";
        echo "⏳ Executando...\n\n";
        
        // Executar e capturar resultado
        $resultado_json = shell_exec($comando);
        
        echo "⏰ Fim: " . date("H:i:s") . "\n";
        echo "📊 Resultado capturado!\n\n";
        
        return $resultado_json;
    }
    
    /**
     * Analisar resultado completo
     */
    public function analisarResultado($resultado_json) {
        echo "🔍 ANÁLISE COMPLETA DO RESULTADO\n";
        echo "================================\n\n";
        
        if (empty($resultado_json)) {
            echo "❌ Resultado vazio!\n";
            return;
        }
        
        $resultado = json_decode($resultado_json, true);
        
        if (!$resultado) {
            echo "❌ JSON inválido!\n";
            echo "📄 Conteúdo bruto:\n";
            echo $resultado_json . "\n";
            return;
        }
        
        // Informações gerais
        echo "📊 INFORMAÇÕES GERAIS:\n";
        echo "Status: " . ($resultado["status"] ?? "N/A") . "\n";
        echo "Tempo de execução: " . ($resultado["tempo_execucao"] ?? "N/A") . "s\n";
        echo "Erros: " . ($resultado["erros"]["total_erros"] ?? "N/A") . "\n";
        echo "Warnings: " . ($resultado["erros"]["total_warnings"] ?? "N/A") . "\n\n";
        
        // ProgressTracker (Fase 3)
        if (isset($resultado["progresso"])) {
            $progresso = $resultado["progresso"];
            
            echo "🎯 PROGRESSTRACKER (FASE 3):\n";
            echo "===========================\n";
            echo "Etapa final: " . ($progresso["etapa_atual"] ?? "N/A") . "\n";
            echo "Total de etapas: " . ($progresso["total_etapas"] ?? "N/A") . "\n";
            echo "Percentual final: " . round($progresso["percentual"] ?? 0, 2) . "%\n";
            echo "Status final: " . ($progresso["status"] ?? "N/A") . "\n";
            echo "Tempo total: " . round($progresso["tempo_decorrido"] ?? 0, 2) . "s\n";
            echo "Timestamp: " . ($progresso["timestamp"] ?? "N/A") . "\n\n";
            
            // Histórico de etapas
            if (isset($progresso["etapas_historico"]) && is_array($progresso["etapas_historico"])) {
                echo "📋 HISTÓRICO DE ETAPAS:\n";
                echo "======================\n";
                
                foreach ($progresso["etapas_historico"] as $index => $etapa) {
                    $num = $index + 1;
                    $etapa_num = $etapa["etapa"] ?? "N/A";
                    $status = $etapa["status"] ?? "N/A";
                    $timestamp = $etapa["timestamp"] ?? "N/A";
                    $tempo = round($etapa["tempo_etapa"] ?? 0, 2);
                    
                    echo "Etapa $etapa_num: $status\n";
                    echo "  ⏰ Timestamp: $timestamp\n";
                    echo "  ⏱️ Tempo acumulado: {$tempo}s\n\n";
                }
                
                echo "📊 Total de etapas no histórico: " . count($progresso["etapas_historico"]) . "\n\n";
            } else {
                echo "⚠️ Histórico de etapas não encontrado\n\n";
            }
            
            // JSON completo do progresso
            echo "📄 JSON COMPLETO DO PROGRESSO:\n";
            echo "==============================\n";
            echo json_encode($progresso, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";
            
        } else {
            echo "❌ PROGRESSTRACKER NÃO ENCONTRADO!\n";
            echo "⚠️ Problema na implementação da Fase 3\n\n";
        }
        
        // JSON completo do resultado
        echo "📄 JSON COMPLETO DO RESULTADO:\n";
        echo "==============================\n";
        echo json_encode($resultado, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";
    }
    
    /**
     * Limpar arquivos temporários
     */
    public function limpar() {
        echo "🧹 Limpando arquivos...\n";
        $arquivos = [$this->arquivo_config];
        
        foreach ($arquivos as $arquivo) {
            if (file_exists($arquivo)) {
                unlink($arquivo);
                echo "🗑️ Removido: $arquivo\n";
            }
        }
        echo "✅ Limpeza concluída!\n";
    }
    
    /**
     * Executar monitoramento completo
     */
    public function executarMonitoramento() {
        try {
            $this->criarConfiguracao();
            $resultado = $this->executarRPADireto();
            $this->analisarResultado($resultado);
            $this->limpar();
            
            echo "\n🎯 MONITORAMENTO CONCLUÍDO!\n";
            echo "Fase 3: ProgressTracker analisado ✅\n";
            
        } catch (Exception $e) {
            echo "❌ ERRO: " . $e->getMessage() . "\n";
        }
    }
}

// Executar se chamado diretamente
if (basename(__FILE__) == basename($_SERVER["SCRIPT_NAME"])) {
    $monitor = new MonitorProgressoTempoReal();
    $monitor->executarMonitoramento();
}
?>
