# 📋 Documentação Completa do JSON de Retorno - RPA Tô Segurado

## 📖 **Visão Geral**

Este documento descreve detalhadamente a estrutura e todos os campos do JSON de retorno do RPA Tô Segurado. O sistema retorna informações estruturadas sobre a execução do processo de cotação, incluindo dados capturados em diferentes etapas.

## 🎯 **Versão Atual**

- **Versão do RPA**: 2.11.0
- **Data da Documentação**: 31/08/2025
- **Última Atualização**: Implementação da estrutura simplificada de planos

## 📊 **Estrutura Geral do JSON**

### **1. Retorno de Sucesso Completo**

```json
{
  "status": "sucesso",
  "timestamp": "2025-08-31T17:45:00.199712",
  "versao": "2.11.0",
  "sistema": "RPA Tô Segurado",
  "codigo": 9002,
  "mensagem": "RPA executado com sucesso",
  "dados": {
    "telas_executadas": 8,
    "tempo_execucao": "85.2s",
    "placa_processada": "FPG-8D63",
    "url_final": "https://www.app.tosegurado.com.br/cotacao/carro",
    "capturas_intermediarias": {
      "carrossel": { /* dados do carrossel */ },
      "tela_final": { /* dados da tela final */ }
    }
  },
  "logs": [
    "2025-08-31 17:44:07 | INFO | RPA executado com sucesso",
    "2025-08-31 17:44:09 | INFO | Chrome fechado"
  ]
}
```

### **2. Retorno de Erro**

```json
{
  "status": "erro",
  "timestamp": "2025-08-31T17:45:00.199712",
  "versao": "2.11.0",
  "sistema": "RPA Tô Segurado",
  "codigo": 2002,
  "mensagem": "Elemento não encontrado na página",
  "dados": {
    "tela_falhou": 6,
    "elemento_nao_encontrado": "//button[contains(., 'Continuar')]",
    "tentativas_realizadas": 3,
    "ultimo_url": "https://www.app.tosegurado.com.br/cotacao/tela5"
  }
}
```

## 🔍 **Detalhamento de Cada Campo**

### **Campos Principais do Retorno**

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|-------|------|-------------|-----------|---------|
| `status` | string | ✅ | Status da execução | `"sucesso"` ou `"erro"` |
| `timestamp` | string | ✅ | Data/hora da execução em ISO 8601 | `"2025-08-31T17:45:00.199712"` |
| `versao` | string | ✅ | Versão do RPA | `"2.11.0"` |
| `sistema` | string | ✅ | Nome do sistema | `"RPA Tô Segurado"` |
| `codigo` | integer | ✅ | Código de retorno | `9002` (sucesso) ou `2002` (erro) |
| `mensagem` | string | ✅ | Mensagem descritiva | `"RPA executado com sucesso"` |
| `dados` | object | ✅ | Dados da execução | Objeto com informações detalhadas |
| `logs` | array | ❌ | Logs da execução | Array de strings com logs |

### **Campos do Objeto `dados`**

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|-------|------|-------------|-----------|---------|
| `telas_executadas` | integer | ✅ | Número de telas processadas | `8` |
| `tempo_execucao` | string | ✅ | Tempo total de execução | `"85.2s"` |
| `placa_processada` | string | ✅ | Placa do veículo processado | `"FPG-8D63"` |
| `url_final` | string | ✅ | URL da página final | `"https://www.app.tosegurado.com.br/cotacao/carro"` |
| `capturas_intermediarias` | object | ❌ | Dados capturados durante a execução | Objeto com carrossel e tela final |

## 🎠 **Captura do Carrossel (`capturas_intermediarias.carrossel`)**

### **Estrutura Completa**

```json
{
  "timestamp": "2025-08-31T17:44:30.123456",
  "tela": "carrossel",
  "nome_tela": "Estimativas de Cobertura",
  "url": "https://www.app.tosegurado.com.br/cotacao/carro",
  "titulo": "Faça agora sua cotação de Seguro Auto",
  "estimativas": [
    {
      "cobertura": "Cobertura Compreensiva",
      "valores": {
        "de": "R$ 1.200,00",
        "ate": "R$ 1.700,00"
      },
      "beneficios": [
        {
          "nome": "Colisão e Acidentes",
          "status": "incluido"
        },
        {
          "nome": "Roubo e Furto",
          "status": "incluido"
        }
      ]
    }
  ]
}
```

### **Campos do Carrossel**

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|-------|------|-------------|-----------|---------|
| `timestamp` | string | ✅ | Data/hora da captura | `"2025-08-31T17:44:30.123456"` |
| `tela` | string | ✅ | Identificador da tela | `"carrossel"` |
| `nome_tela` | string | ✅ | Nome descritivo da tela | `"Estimativas de Cobertura"` |
| `url` | string | ✅ | URL da página | `"https://www.app.tosegurado.com.br/cotacao/carro"` |
| `titulo` | string | ✅ | Título da página | `"Faça agora sua cotação de Seguro Auto"` |
| `estimativas` | array | ✅ | Lista de estimativas capturadas | Array de objetos de estimativa |

### **Campos das Estimativas (`estimativas[]`)**

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|-------|------|-------------|-----------|---------|
| `cobertura` | string | ✅ | Nome da cobertura | `"Cobertura Compreensiva"` |
| `valores.de` | string | ✅ | Valor mínimo | `"R$ 1.200,00"` |
| `valores.ate` | string | ✅ | Valor máximo | `"R$ 1.700,00"` |
| `beneficios` | array | ✅ | Lista de benefícios | Array de objetos de benefício |

### **Campos dos Benefícios (`beneficios[]`)**

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|-------|------|-------------|-----------|---------|
| `nome` | string | ✅ | Nome do benefício | `"Colisão e Acidentes"` |
| `status` | string | ✅ | Status do benefício | `"incluido"` |

**Valores possíveis para `status`:**
- `"incluido"`: Benefício incluído no plano
- `"nao_incluido"`: Benefício não incluído
- `"opcional"`: Benefício opcional

## 🎯 **Captura da Tela Final (`capturas_intermediarias.tela_final`)**

### **Estrutura Completa**

```json
{
  "timestamp": "2025-08-31T17:45:00.199712",
  "tela": "final",
  "nome_tela": "Resultado Final",
  "url": "https://www.app.tosegurado.com.br/cotacao/carro",
  "titulo": "Faça agora sua cotação de Seguro Auto",
  "titulo_pagina": "Parabéns, chegamos ao resultado final",
  "planos": [
    {
      "titulo": "Plano Recomendado",
      "franquia": {
        "valor": "R$ 2.500,00",
        "tipo": "Reduzida"
      },
      "valor_mercado": "100% da tabela FIPE",
      "assistencia": true,
      "vidros": true,
      "carro_reserva": true,
      "danos_materiais": "R$ 50.000,00",
      "danos_corporais": "R$ 50.000,00",
      "danos_morais": "R$ 10.000,00",
      "morte_invalidez": "R$ 5.000,00",
      "precos": {
        "anual": "R$ 100,00",
        "parcelado": {
          "valor": "R$ 218,17",
          "parcelas": "1x sem juros"
        }
      },
      "score_qualidade": 100,
      "texto_completo": "Texto completo do plano...",
      "categoria": "premium"
    }
  ],
  "modal_login": {
    "detectado": true,
    "titulo": "Modal de envio de cotação por email",
    "campos": ["email"]
  },
  "elementos_detectados": [
    "palavra_chave: Parabéns",
    "palavra_chave: resultado final"
  ],
  "resumo": {
    "total_planos": 2,
    "plano_recomendado": "Plano Recomendado",
    "valores_encontrados": 22,
    "qualidade_captura": "boa"
  }
}
```

### **Campos da Tela Final**

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|-------|------|-------------|-----------|---------|
| `timestamp` | string | ✅ | Data/hora da captura | `"2025-08-31T17:45:00.199712"` |
| `tela` | string | ✅ | Identificador da tela | `"final"` |
| `nome_tela` | string | ✅ | Nome descritivo da tela | `"Resultado Final"` |
| `url` | string | ✅ | URL da página | `"https://www.app.tosegurado.com.br/cotacao/carro"` |
| `titulo` | string | ✅ | Título da página | `"Faça agora sua cotação de Seguro Auto"` |
| `titulo_pagina` | string | ✅ | Título específico da página | `"Parabéns, chegamos ao resultado final"` |
| `planos` | array | ✅ | Lista de planos capturados | Array de objetos de plano |
| `modal_login` | object | ✅ | Informações sobre modal de login | Objeto com dados do modal |
| `elementos_detectados` | array | ✅ | Elementos detectados na página | Array de strings |
| `resumo` | object | ✅ | Resumo da captura | Objeto com estatísticas |

### **Campos dos Planos (`planos[]`)**

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|-------|------|-------------|-----------|---------|
| `titulo` | string | ✅ | Título do plano | `"Plano Recomendado"` |
| `franquia.valor` | string | ✅ | Valor da franquia | `"R$ 2.500,00"` |
| `franquia.tipo` | string | ✅ | Tipo da franquia | `"Reduzida"` |
| `valor_mercado` | string | ✅ | Valor de mercado | `"100% da tabela FIPE"` |
| `assistencia` | boolean | ✅ | Inclui assistência | `true` |
| `vidros` | boolean | ✅ | Inclui cobertura de vidros | `true` |
| `carro_reserva` | boolean | ✅ | Inclui carro reserva | `true` |
| `danos_materiais` | string | ✅ | Cobertura de danos materiais | `"R$ 50.000,00"` |
| `danos_corporais` | string | ✅ | Cobertura de danos corporais | `"R$ 50.000,00"` |
| `danos_morais` | string | ✅ | Cobertura de danos morais | `"R$ 10.000,00"` |
| `morte_invalidez` | string | ✅ | Cobertura de morte/invalidez | `"R$ 5.000,00"` |
| `precos.anual` | string | ✅ | Preço anual | `"R$ 100,00"` |
| `precos.parcelado.valor` | string | ✅ | Valor da parcela | `"R$ 218,17"` |
| `precos.parcelado.parcelas` | string | ✅ | Condições de parcelamento | `"1x sem juros"` |
| `score_qualidade` | integer | ✅ | Score de qualidade (0-100) | `100` |
| `texto_completo` | string | ✅ | Texto completo do plano | `"Texto completo..."` |
| `categoria` | string | ✅ | Categoria do plano | `"premium"` |

**Valores possíveis para `categoria`:**
- `"premium"`: Plano com mais coberturas e benefícios
- `"intermediario"`: Plano com coberturas moderadas
- `"basico"`: Plano com coberturas básicas

### **Campos do Modal de Login (`modal_login`)**

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|-------|------|-------------|-----------|---------|
| `detectado` | boolean | ✅ | Se o modal foi detectado | `true` |
| `titulo` | string | ✅ | Título do modal | `"Modal de envio de cotação por email"` |
| `campos` | array | ✅ | Campos do modal | `["email"]` |

### **Campos do Resumo (`resumo`)**

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|-------|------|-------------|-----------|---------|
| `total_planos` | integer | ✅ | Total de planos capturados | `2` |
| `plano_recomendado` | string | ✅ | Nome do plano recomendado | `"Plano Recomendado"` |
| `valores_encontrados` | integer | ✅ | Total de valores capturados | `22` |
| `qualidade_captura` | string | ✅ | Qualidade da captura | `"boa"` |

## 📊 **Códigos de Retorno**

### **Códigos de Sucesso (9001-9999)**

| Código | Mensagem | Descrição |
|--------|----------|-----------|
| 9001 | Tela executada com sucesso | Sucesso em tela específica |
| 9002 | RPA executado com sucesso | Sucesso completo do RPA |
| 9003 | Elemento encontrado e processado | Sucesso em elemento específico |
| 9004 | Ação realizada com sucesso | Sucesso em ação específica |

### **Códigos de Erro (1000-8999)**

#### **Configuração (1000-1999)**
| Código | Mensagem | Solução |
|--------|----------|---------|
| 1001 | Erro ao carregar arquivo de configuração | Verifique se parametros.json existe e está válido |
| 1002 | Configuração inválida ou incompleta | Verifique a estrutura do arquivo de configuração |
| 1003 | Erro no ChromeDriver | Verifique se o ChromeDriver está instalado e acessível |
| 1004 | Erro ao inicializar navegador | Verifique as configurações do Chrome e permissões |

#### **Navegação (2000-2999)**
| Código | Mensagem | Solução |
|--------|----------|---------|
| 2001 | Timeout na navegação | A página demorou muito para carregar, verifique a conexão |
| 2002 | Elemento não encontrado na página | A estrutura da página pode ter mudado |
| 2003 | Elemento não está clicável | O elemento existe mas não pode ser interagido |
| 2004 | Página não carregou completamente | Aguarde mais tempo ou verifique a conexão |
| 2005 | Erro no redirecionamento | Problema na navegação entre páginas |

#### **Automação (3000-3999)**
| Código | Mensagem | Solução |
|--------|----------|---------|
| 3001 | Falha ao clicar no elemento | Elemento pode estar sobreposto ou não visível |
| 3002 | Falha ao inserir dados no campo | Campo pode estar desabilitado ou inválido |
| 3003 | Timeout aguardando elemento | Elemento não apareceu no tempo esperado |
| 3004 | Elemento obsoleto (stale) | A página foi recarregada, tente novamente |
| 3005 | Erro na execução de JavaScript | Problema na interação com a página |

#### **Sistema (4000-4999)**
| Código | Mensagem | Solução |
|--------|----------|---------|
| 4001 | Erro de conexão de rede | Verifique sua conexão com a internet |
| 4002 | Erro de memória insuficiente | Feche outros programas e tente novamente |
| 4003 | Erro de disco/arquivo | Verifique o espaço em disco e permissões |
| 4004 | Erro de permissão | Execute como administrador se necessário |

#### **Validação (5000-5999)**
| Código | Mensagem | Solução |
|--------|----------|---------|
| 5001 | Dados inválidos fornecidos | Verifique os dados de entrada |
| 5002 | Formato de dados incorreto | Verifique o formato dos dados |
| 5003 | Validação falhou | Dados não passaram na validação |

## 📈 **Qualidade da Captura**

O campo `qualidade_captura` é calculado com base no `score_qualidade` médio dos planos capturados:

| Qualidade | Score | Descrição |
|-----------|-------|-----------|
| `"excelente"` | 90-100 | Captura muito precisa, todos os dados importantes |
| `"boa"` | 70-89 | Captura precisa, maioria dos dados importantes |
| `"regular"` | 50-69 | Captura parcial, alguns dados podem estar faltando |
| `"ruim"` | 0-49 | Captura incompleta, muitos dados faltando |

### **Cálculo do Score de Qualidade**

O `score_qualidade` de cada plano é calculado com base na presença e qualidade dos seguintes campos:

- **Preços (30 pontos)**: `precos.anual` e `precos.parcelado.valor`
- **Franquia (20 pontos)**: `franquia.valor` e `franquia.tipo`
- **Coberturas (30 pontos)**: `assistencia`, `vidros`, `carro_reserva`
- **Valores de Cobertura (20 pontos)**: `danos_materiais`, `danos_corporais`, `danos_morais`, `morte_invalidez`

## 💻 **Exemplos de Uso**

### **JavaScript/TypeScript**

```javascript
async function processarRetornoRPA(jsonRetorno) {
    if (jsonRetorno.status === 'sucesso') {
        console.log('✅ RPA executado com sucesso!');
        
        // Acessar dados do carrossel
        const carrossel = jsonRetorno.dados.capturas_intermediarias.carrossel;
        console.log('Estimativas encontradas:', carrossel.estimativas.length);
        
        // Acessar dados da tela final
        const telaFinal = jsonRetorno.dados.capturas_intermediarias.tela_final;
        console.log('Planos encontrados:', telaFinal.planos.length);
        
        // Processar planos
        telaFinal.planos.forEach(plano => {
            console.log(`Plano: ${plano.titulo}`);
            console.log(`Preço anual: ${plano.precos.anual}`);
            console.log(`Franquia: ${plano.franquia.valor}`);
            console.log(`Assistência: ${plano.assistencia ? 'Sim' : 'Não'}`);
        });
        
    } else {
        console.error('❌ Erro no RPA:', jsonRetorno.codigo, jsonRetorno.mensagem);
    }
}
```

### **Python**

```python
def processar_retorno_rpa(json_retorno):
    if json_retorno['status'] == 'sucesso':
        print('✅ RPA executado com sucesso!')
        
        # Acessar dados do carrossel
        carrossel = json_retorno['dados']['capturas_intermediarias']['carrossel']
        print(f'Estimativas encontradas: {len(carrossel["estimativas"])}')
        
        # Acessar dados da tela final
        tela_final = json_retorno['dados']['capturas_intermediarias']['tela_final']
        print(f'Planos encontrados: {len(tela_final["planos"])}')
        
        # Processar planos
        for plano in tela_final['planos']:
            print(f'Plano: {plano["titulo"]}')
            print(f'Preço anual: {plano["precos"]["anual"]}')
            print(f'Franquia: {plano["franquia"]["valor"]}')
            print(f'Assistência: {"Sim" if plano["assistencia"] else "Não"}')
            
    else:
        print(f'❌ Erro no RPA: {json_retorno["codigo"]} - {json_retorno["mensagem"]}')
```

## 🔧 **Tratamento de Erros**

### **Exemplo de Tratamento Robusto**

```javascript
function tratarRetornoRPA(jsonRetorno) {
    try {
        // Verificar estrutura básica
        if (!jsonRetorno || typeof jsonRetorno !== 'object') {
            throw new Error('Retorno inválido');
        }
        
        // Verificar campos obrigatórios
        const camposObrigatorios = ['status', 'timestamp', 'codigo', 'mensagem'];
        for (const campo of camposObrigatorios) {
            if (!(campo in jsonRetorno)) {
                throw new Error(`Campo obrigatório ausente: ${campo}`);
            }
        }
        
        // Processar conforme status
        if (jsonRetorno.status === 'sucesso') {
            return processarSucesso(jsonRetorno);
        } else {
            return processarErro(jsonRetorno);
        }
        
    } catch (error) {
        console.error('Erro ao processar retorno:', error);
        return {
            status: 'erro',
            codigo: 9999,
            mensagem: 'Erro interno no processamento do retorno'
        };
    }
}

function processarSucesso(jsonRetorno) {
    const dados = jsonRetorno.dados;
    
    // Verificar se há capturas intermediárias
    if (!dados.capturas_intermediarias) {
        console.warn('⚠️ Nenhuma captura intermediária encontrada');
        return jsonRetorno;
    }
    
    // Processar carrossel
    if (dados.capturas_intermediarias.carrossel) {
        console.log('🎠 Carrossel processado:', dados.capturas_intermediarias.carrossel.estimativas.length, 'estimativas');
    }
    
    // Processar tela final
    if (dados.capturas_intermediarias.tela_final) {
        const telaFinal = dados.capturas_intermediarias.tela_final;
        console.log('🎯 Tela final processada:', telaFinal.planos.length, 'planos');
        
        // Verificar qualidade da captura
        if (telaFinal.resumo.qualidade_captura === 'ruim') {
            console.warn('⚠️ Qualidade da captura baixa');
        }
    }
    
    return jsonRetorno;
}

function processarErro(jsonRetorno) {
    console.error(`❌ Erro ${jsonRetorno.codigo}: ${jsonRetorno.mensagem}`);
    
    // Sugerir soluções baseadas no código de erro
    const sugestoes = {
        2002: 'Verifique se o site não mudou sua estrutura',
        3001: 'Tente executar novamente',
        4001: 'Verifique sua conexão com a internet'
    };
    
    if (sugestoes[jsonRetorno.codigo]) {
        console.log(`💡 Sugestão: ${sugestoes[jsonRetorno.codigo]}`);
    }
    
    return jsonRetorno;
}
```

## 📝 **Notas Importantes**

### **Campos Opcionais**
- Alguns campos podem estar vazios (`""`) quando não conseguimos capturar a informação
- Campos booleanos sempre retornam `true` ou `false`
- Arrays vazios são retornados como `[]`

### **Formato de Valores Monetários**
- Valores monetários são retornados como strings no formato brasileiro
- Exemplo: `"R$ 1.200,00"` (com vírgula como separador decimal)
- Valores podem incluir texto adicional (ex: `"100% da tabela FIPE"`)

### **Timestamps**
- Todos os timestamps seguem o padrão ISO 8601
- Fuso horário: UTC
- Formato: `"YYYY-MM-DDTHH:MM:SS.microseconds"`

### **URLs**
- URLs são retornadas exatamente como capturadas
- Podem incluir parâmetros de query string
- Sempre começam com `https://`

## 🔄 **Evolução da Documentação**

Esta documentação será atualizada conforme novas versões do RPA são lançadas. Mudanças significativas na estrutura do JSON serão documentadas aqui.

---

**Última Atualização**: 31/08/2025  
**Versão da Documentação**: 1.0.0  
**Autor**: Sistema RPA Tô Segurado
