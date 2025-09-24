<?php
/**
 * MONITOR PROGRESSTRACKER EM TEMPO REAL
 * Acompanha passo a passo o progresso do RPA
 */

class MonitorProgressoTempoReal {
    
    private $arquivo_progresso = "temp/progress_status.json";
    private $arquivo_config = "monitor_progress.json";
    private $timeout = 300; // 5 minutos
    
    public function __construct() {
        echo "MONITOR PROGRESSTRACKER EM TEMPO REAL\n";
        echo "====================================\n\n";
    }
    
    /**
     * Criar configuração para monitoramento
     */
    public function criarConfiguracao() {
        echo "Criando configuração de monitoramento...\n";
        
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
        echo "OK - Arquivo criado: {$this->arquivo_config}\n\n";
    }
    
    /**
     * Executar RPA em background
     */
    public function executarRPABackground() {
        echo "Executando RPA em background...\n";
        echo "Inicio: " . date("H:i:s") . "\n\n";
        
        $comando = "python executar_rpa_imediato_playwright.py --config {$this->arquivo_config}";
        
        // Executar em background
        if (strtoupper(substr(PHP_OS, 0, 3)) === "WIN") {
            $processo = popen("start /B $comando", "r");
        } else {
            $processo = popen("$comando &", "r");
        }
        
        if ($processo) {
            pclose($processo);
            echo "OK - RPA iniciado em background\n";
            return true;
        } else {
            echo "ERRO - Falha ao iniciar RPA\n";
            return false;
        }
    }
    
    /**
     * Monitorar progresso em tempo real
     */
    public function monitorarProgresso() {
        echo "MONITORAMENTO EM TEMPO REAL\n";
        echo "===========================\n\n";
        
        $etapas_anteriores = [];
        $start_time = time();
        $ultima_etapa = 0;
        
        while ((time() - $start_time) < $this->timeout) {
            $progresso_atual = $this->lerProgressoAtual();
            
            if ($progresso_atual) {
                $etapa_atual = $progresso_atual["etapa_atual"] ?? 0;
                $status = $progresso_atual["status"] ?? "N/A";
                $percentual = round($progresso_atual["percentual"] ?? 0, 1);
                $tempo_decorrido = round($progresso_atual["tempo_decorrido"] ?? 0, 1);
                
                // Verificar se é uma nova etapa
                if ($etapa_atual > $ultima_etapa) {
                    echo "ETAPA $etapa_atual: $status\n";
                    echo "   Progresso: $percentual%\n";
                    echo "   Tempo: {$tempo_decorrido}s\n";
                    echo "   " . date("H:i:s") . "\n\n";
                    
                    $ultima_etapa = $etapa_atual;
                    
                    // Capturar estimativas (Etapa 5)
                    if ($etapa_atual == 5) {
                        $this->capturarEstimativas($progresso_atual);
                    }
                }
                
                // Verificar se terminou
                if ($etapa_atual >= 15) {
                    echo "EXECUCAO CONCLUIDA!\n";
                    echo "Fim: " . date("H:i:s") . "\n\n";
                    break;
                }
            }
            
            sleep(2); // Verificar a cada 2 segundos
        }
        
        // Capturar resultado final
        $this->capturarResultadoFinal();
    }
    
    /**
     * Ler progresso atual do arquivo
     */
    private function lerProgressoAtual() {
        if (file_exists($this->arquivo_progresso)) {
            $conteudo = file_get_contents($this->arquivo_progresso);
            if ($conteudo) {
                $progresso = json_decode($conteudo, true);
                if ($progresso) {
                    return $progresso;
                }
            }
        }
        return null;
    }
    
    /**
     * Capturar e exibir estimativas (Etapa 5)
     */
    private function capturarEstimativas($progresso) {
        echo "CAPTURANDO ESTIMATIVAS (ETAPA 5)\n";
        echo "================================\n";
        
        if (isset($progresso["json_retorno"])) {
            echo "OK - Estimativas disponíveis!\n";
            echo "Dados das estimativas:\n";
            echo $progresso["json_retorno"] . "\n\n";
        } else {
            echo "AVISO - Estimativas não encontradas no progresso\n\n";
        }
    }
    
    /**
     * Capturar e exibir resultado final
     */
    private function capturarResultadoFinal() {
        echo "CAPTURANDO RESULTADO FINAL\n";
        echo "=========================\n";
        
        // Buscar arquivo de resultado mais recente
        $arquivos_resultado = glob("dados_planos_seguro_*.json");
        if (!empty($arquivos_resultado)) {
            $arquivo_mais_recente = max($arquivos_resultado);
            echo "Arquivo mais recente: $arquivo_mais_recente\n";
            
            $resultado = json_decode(file_get_contents($arquivo_mais_recente), true);
            if ($resultado) {
                echo "OK - Resultado final capturado!\n\n";
                
                // Informações gerais
                echo "INFORMACOES GERAIS:\n";
                echo "Plano recomendado: " . $resultado["plano_recomendado"]["valor"] . "\n";
                echo "Plano alternativo: " . $resultado["plano_alternativo"]["valor"] . "\n";
                echo "Franquia recomendada: " . $resultado["plano_recomendado"]["valor_franquia"] . "\n";
                echo "Franquia alternativa: " . $resultado["plano_alternativo"]["valor_franquia"] . "\n\n";
                
                // JSON completo
                echo "JSON COMPLETO DO RESULTADO:\n";
                echo "===========================\n";
                echo json_encode($resultado, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";
                
            } else {
                echo "ERRO - JSON inválido no resultado final\n\n";
            }
        } else {
            echo "ERRO - Nenhum arquivo de resultado encontrado\n\n";
        }
    }
    
    /**
     * Limpar arquivos temporários
     */
    public function limpar() {
        echo "Limpando arquivos...\n";
        if (file_exists($this->arquivo_config)) {
            unlink($this->arquivo_config);
            echo "Removido: {$this->arquivo_config}\n";
        }
        echo "Limpeza concluida!\n";
    }
    
    /**
     * Executar monitoramento completo
     */
    public function executarMonitoramento() {
        try {
            $this->criarConfiguracao();
            
            if ($this->executarRPABackground()) {
                $this->monitorarProgresso();
            }
            
            $this->limpar();
            
            echo "\nMONITORAMENTO CONCLUIDO!\n";
            echo "ProgressTracker monitorado em tempo real OK\n";
            
        } catch (Exception $e) {
            echo "ERRO: " . $e->getMessage() . "\n";
        }
    }
}

// Executar se chamado diretamente
if (basename(__FILE__) == basename($_SERVER["SCRIPT_NAME"])) {
    $monitor = new MonitorProgressoTempoReal();
    $monitor->executarMonitoramento();
}
?>
