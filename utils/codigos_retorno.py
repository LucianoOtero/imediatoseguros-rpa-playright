# ========================================
# CÓDIGOS DE RETORNO ESTRUTURADO
# ========================================
# Sistema de códigos padronizados para retorno estruturado
# Versão: 3.0.0
# Data: 2025-09-02

# ========================================
# CÓDIGOS DE SUCESSO (9000-9099)
# ========================================

CODIGOS_SUCESSO = {
    9001: "RPA iniciado com sucesso",
    9002: "RPA executado com sucesso - Todas as telas",
    9003: "RPA executado com sucesso - Telas parciais",
    9004: "Dados capturados com sucesso",
    9005: "Arquivo salvo com sucesso",
    9006: "Navegação concluída com sucesso",
    9007: "Autenticação realizada com sucesso",
    9008: "Configuração carregada com sucesso",
    9009: "Validação de parâmetros concluída",
    9010: "Processamento finalizado com sucesso"
}

# ========================================
# CÓDIGOS DE ERRO (9100-9199)
# ========================================

CODIGOS_ERRO = {
    9101: "Erro na inicialização do RPA",
    9102: "Erro na navegação - Tela específica falhou",
    9103: "Erro na captura de dados",
    9104: "Erro na validação de parâmetros",
    9105: "Erro de timeout",
    9106: "Erro de conexão",
    9107: "Erro de autenticação",
    9108: "Erro genérico",
    9109: "Erro de elemento não encontrado",
    9110: "Erro de carregamento de página",
    9111: "Erro de JavaScript",
    9112: "Erro de rede",
    9113: "Erro de permissão",
    9114: "Erro de arquivo não encontrado",
    9115: "Erro de formato inválido"
}

# ========================================
# CÓDIGOS DE WARNING (9200-9299)
# ========================================

CODIGOS_WARNING = {
    9201: "Parâmetros incompletos",
    9202: "Tela condicional não apareceu",
    9203: "Dados parciais capturados",
    9204: "Timeout menor que o esperado",
    9205: "Elemento encontrado mas não clicável",
    9206: "Dados opcionais não disponíveis",
    9207: "Performance abaixo do esperado",
    9208: "Configuração não padrão detectada",
    9209: "Logs de debug ativados",
    9210: "Modo de teste detectado"
}

# ========================================
# FUNÇÕES AUXILIARES
# ========================================

def obter_mensagem_codigo(codigo: int) -> str:
    """
    Retorna a mensagem associada a um código de status
    
    PARÂMETROS:
        codigo: int - Código de status
        
    RETORNO:
        str: Mensagem associada ao código
    """
    if codigo in CODIGOS_SUCESSO:
        return CODIGOS_SUCESSO[codigo]
    elif codigo in CODIGOS_ERRO:
        return CODIGOS_ERRO[codigo]
    elif codigo in CODIGOS_WARNING:
        return CODIGOS_WARNING[codigo]
    else:
        return f"Código {codigo} não reconhecido"


def validar_codigo(codigo: int) -> bool:
    """
    Valida se um código de status é válido
    
    PARÂMETROS:
        codigo: int - Código de status
        
    RETORNO:
        bool: True se válido, False caso contrário
    """
    return (codigo in CODIGOS_SUCESSO or 
            codigo in CODIGOS_ERRO or 
            codigo in CODIGOS_WARNING)


def obter_tipo_codigo(codigo: int) -> str:
    """
    Retorna o tipo do código (success, error, warning)
    
    PARÂMETROS:
        codigo: int - Código de status
        
    RETORNO:
        str: Tipo do código
    """
    if codigo in CODIGOS_SUCESSO:
        return "success"
    elif codigo in CODIGOS_ERRO:
        return "error"
    elif codigo in CODIGOS_WARNING:
        return "warning"
    else:
        return "unknown"


def listar_codigos_disponiveis() -> dict:
    """
    Lista todos os códigos disponíveis organizados por tipo
    
    RETORNO:
        dict: Dicionário com todos os códigos organizados
    """
    return {
        "sucesso": CODIGOS_SUCESSO,
        "erro": CODIGOS_ERRO,
        "warning": CODIGOS_WARNING
    }
