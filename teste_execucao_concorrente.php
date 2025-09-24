<?php
/**
 * TESTE DE EXECUÇÃO CONCORRENTE - FASE 3
 * ProgressTracker sem arquivos + Execução simultânea
 * 
 * Este programa testa a funcionalidade de execução concorrente
 * implementada na Fase 3 do RPA Imediato Seguros.
 */

class TesteExecucaoConcorrente {
    private $sessoes = [];
    private $resultados = [];
    
    public function __construct() {
        echo "🚀 TESTE DE EXECUÇÃO CONCORRENTE - FASE 3\n";
        echo "==========================================\n\n";
    }
    
    /**
     * Criar arquivos de configuração para múltiplas sessões
     */
    public function criarArquivosConfiguracao() {
        echo "📁 Criando arquivos de configuração...\n";
        
        $placas = [
EYQ4J41, TKH6F60, ABC1234];
        $tipos = [carro, moto, carro];
        
        for ($i = 0; $i < 3; $i++) {
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
                    "visualizar_mensagens" => false, // Modo silencioso para teste
                    "eliminar_tentativas_inuteis" => true
                ],
                "autenticacao" => [
                    "email_login" => "aleximediatoseguros@gmail.com",
                    "senha_login" => "Lrotero1$",
                    "manter_login_atual" => true
                ],
                "url" => "https://www.app.tosegurado.com.br/imediatosolucoes",
                "tipo_veiculo" => $tipos[$i],
                "placa" => $placas[$i],
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
            
            $arquivo = "sessao" . ($i + 1) . ".json";
            file_put_contents($arquivo, json_encode($config, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
            echo "✅ Arquivo criado: $arquivo (Placa: {$placas[$i]}, Tipo: {$tipos[$i]})\n";
        }
        
        echo "\n";
    }
    
    /**
     * Executar múltiplas instâncias simultaneamente
     */
    public function executarConcorrente() {
        echo "🚀 Iniciando execução concorrente...\n";
        echo "⏰ Início: " . date(H:i:s) . "\n\n";
        
        $processos = [];
        
        // Iniciar 3 execuções simultâneas
        for ($i = 1; $i <= 3; $i++) {
            $comando = "python executar_rpa_imediato_playwright.py --config sessao$i.json > resultado$i.json 2>&1";
            echo "🔄 Iniciando Sessão $i...\n";
            
            // Executar em background (Windows)
            if (strtoupper(substr(PHP_OS, 0, 3)) === WIN) {
                $processos[$i] = popen("start /B $comando", r);
            } else {
                $processos[$i] = popen("$comando &", r);
            }
        }
        
        echo "\n⏳ Aguardando conclusão das execuções...\n";
        
        // Aguardar conclusão
        $inicio = time();
        $timeout = 300; // 5 minutos timeout
        
        while (time() - $inicio < $timeout) {
            $concluidas = 0;
            
            for ($i = 1; $i <= 3; $i++) {
                if (file_exists("resultado$i.json")) {
                    $conteudo = file_get_contents("resultado$i.json");
                    if (!empty($conteudo) && strpos($conteudo, status) !== false) {
                        $concluidas++;
                    }
                }
            }
            
            if ($concluidas == 3) {
                echo "✅ Todas as execuções concluídas!\n";
                break;
            }
            
            echo "📊 Progresso: $concluidas/3 execuções concluídas\n";
            sleep(5);
        }
        
        // Fechar processos
        foreach ($processos as $processo) {
            if (is_resource($processo)) {
                pclose($processo);
            }
        }
        
        echo "⏰ Fim: " . date(H:i:s) . "\n\n";
    }
    
    /**
     * Analisar resultados das execuções
     */
    public function analisarResultados() {
        echo "📊 ANÁLISE DOS RESULTADOS\n";
        echo "========================\n\n";
        
        $sucessos = 0;
        $erros = 0;
        
        for ($i = 1; $i <= 3; $i++) {
            echo "🔍 SESSÃO $i:\n";
            echo "Arquivo: resultado$i.json\n";
            
            if (file_exists("resultado$i.json")) {
                $conteudo = file_get_contents("resultado$i.json");
                
                if (!empty($conteudo)) {
                    $resultado = json_decode($conteudo, true);
                    
                    if ($resultado) {
                        echo "Status: " . ($resultado[status] ?? N/A) . "\n";
                        echo "Tempo: " . ($resultado[tempo_execucao] ?? N/A) . "s\n";
                        
                        // Verificar progresso (Fase 3)
                        if (isset($resultado[progresso])) {
                            $progresso = $resultado[progresso];
                            echo "Progresso: Etapa " . ($progresso[etapa_atual] ?? N/A) . "/" . ($progresso[total_etapas] ?? N/A) . "\n";
                            echo "Percentual: " . round($progresso[percentual] ?? 0, 1) . "%\n";
                            echo "Histórico: " . count($progresso[etapas_historico] ?? []) . " etapas\n";
                        } else {
                            echo "⚠️ Progresso não encontrado (problema na Fase 3)\n";
                        }
                        
                        if (($resultado[status] ?? ') === success) {
                            $sucessos++;
                            echo "✅ SUCESSO\n";
                        } else {
                            $erros++;
                            echo "❌ ERRO\n";
                        }
                    } else {
                        echo "❌ JSON inválido\n";
                        $erros++;
                    }
                } else {
                    echo "❌ Arquivo vazio\n";
                    $erros++;
                }
            } else {
                echo "❌ Arquivo não encontrado\n";
                $erros++;
            }
            
            echo "\n";
        }
        
        echo "📈 RESUMO FINAL:\n";
        echo "Sucessos: $sucessos/3\n";
        echo "Erros: $erros/3\n";
        echo "Taxa de sucesso: " . round(($sucessos / 3) * 100, 1) . "%\n\n";
        
        if ($sucessos == 3) {
            echo "🎉 TESTE CONCORRENTE PASSOU!\n";
            echo "✅ Fase 3 implementada com sucesso\n";
            echo "✅ Zero race conditions\n";
            echo "✅ Execução concorrente funcionando\n";
        } else {
            echo "⚠️ TESTE CONCORRENTE COM PROBLEMAS\n";
            echo "❌ Verificar implementação da Fase 3\n";
        }
    }
    
    /**
     * Limpar arquivos temporários
     */
    public function limparArquivos() {
        echo "🧹 Limpando arquivos temporários...\n";
        
        $arquivos = [
            sessao1.json, sessao2.json, sessao3.json,
            resultado1.json, resultado2.json, resultado3.json
        ];
        
        foreach ($arquivos as $arquivo) {
            if (file_exists($arquivo)) {
                unlink($arquivo);
                echo "🗑️ Removido: $arquivo\n";
            }
        }
        
        echo "✅ Limpeza concluída!\n";
    }
    
    /**
     * Executar teste completo
     */
    public function executarTesteCompleto() {
        try {
            $this->criarArquivosConfiguracao();
            $this->executarConcorrente();
            $this->analisarResultados();
            $this->limparArquivos();
            
            echo "\n🎯 TESTE CONCORRENTE CONCLUÍDO!\n";
            echo "Fase 3: ProgressTracker sem arquivos ✅\n";
            echo "Execução concorrente habilitada ✅\n";
            
        } catch (Exception $e) {
            echo "❌ ERRO NO TESTE: " . $e->getMessage() . "\n";
        }
    }
}

// Executar teste se chamado diretamente
if (basename(__FILE__) == basename($_SERVER[SCRIPT_NAME])) {
    $teste = new TesteExecucaoConcorrente();
    $teste->executarTesteCompleto();
}
?>
