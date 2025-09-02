# 🚀 RPA Tô Segurado - Migração Playwright

## 📋 Descrição

Migração completa do projeto RPA "Tô Segurado" de Selenium para Playwright, implementando automação de cotações de seguro automotivo com captura estruturada de dados.

## 🎯 Status do Projeto

### ✅ **Telas Implementadas (1-5):**
- **Tela 1**: Seleção do tipo de seguro (Carro)
- **Tela 2**: Inserção da placa do veículo
- **Tela 3**: Confirmação das informações do veículo
- **Tela 4**: Verificação se o veículo já está segurado
- **Tela 5**: Estimativa inicial com captura de dados dos cards de cobertura

### 🔄 **Próximas Telas (6-13):**
- Em desenvolvimento

## 🛠️ Tecnologias

- **Python 3.8+**
- **Playwright** (substituindo Selenium)
- **JSON** para estruturação de dados
- **Regex** para parsing de valores monetários

## 📊 Funcionalidades Implementadas

### 🎯 **Captura de Dados - Tela 5**
- ✅ **3 Coberturas Capturadas**:
  - Cobertura Compreensiva (R$ 1.600,00 - R$ 2.200,00)
  - Cobertura Roubo e Furto (R$ 1.400,00 - R$ 1.700,00)
  - Cobertura RCF (R$ 1.000,00 - R$ 1.500,00)

- ✅ **Benefícios Estruturados**:
  - Colisão e Acidentes, Roubo e Furto, Incêndio
  - Danos a terceiros, Assistência 24h, Carro Reserva, Vidros
  - Danos parciais, Danos materiais/corporais

- ✅ **JSON Estruturado**:
  - Valores "de" e "até" parseados
  - Benefícios com status "incluido"
  - Metadados completos (timestamp, URL, elementos detectados)

## 🚀 Como Executar

### 📋 **Pré-requisitos**
```bash
pip install playwright
playwright install chromium
```

### ⚙️ **Configuração**
1. Edite `config/parametros.json` com sua placa:
```json
{
  "placa": "EED-3D56",
  "veiculo_segurado": "Não"
}
```

### 🎯 **Execução**
```bash
# Executar Telas 1-5 sequencialmente
python src/teste_tela_1_a_5_sequencial_final.py
```

## 📁 Estrutura do Projeto

```
imediatoseguros-rpa-playwright/
├── src/
│   ├── teste_tela_1_a_5_sequencial_final.py  # Script principal
│   └── executar_rpa_playwright.py            # Versão completa
├── config/
│   └── parametros.json                       # Configurações
├── docs/
│   ├── exemplo_json_retorno_completo.json    # JSON de referência
│   └── DOCUMENTACAO_JSON_RETORNO.md          # Documentação
├── temp/
│   └── captura_carrossel/                    # Dados capturados
└── README.md
```

## 📊 Exemplo de Saída JSON

```json
{
  "status": "sucesso",
  "timestamp": "2025-09-02T03:45:30.523994",
  "sistema": "RPA Tô Segurado - Playwright",
  "dados": {
    "capturas_intermediarias": {
      "carrossel": {
        "coberturas_detalhadas": [
          {
            "cobertura": "Cobertura Compreensiva",
            "valores": {
              "de": "R$ 1.600,00",
              "ate": "R$ 2.200,00"
            },
            "beneficios": [
              {"nome": "Colisão e Acidentes", "status": "incluido"},
              {"nome": "Roubo e Furto", "status": "incluido"}
            ]
          }
        ]
      }
    }
  }
}
```

## 🔧 Melhorias Implementadas

### ✅ **Playwright vs Selenium:**
- **Auto-waiting** para elementos dinâmicos
- **Melhor performance** e estabilidade
- **Captura mais precisa** de dados estruturados
- **Tratamento robusto** de timeouts

### ✅ **Captura de Dados:**
- **Seletores específicos** identificados (`div.bg-primary`, `p.text-primary.underline`)
- **Regex patterns** para parsing de valores monetários
- **Estrutura JSON** alinhada com padrão esperado
- **Logs detalhados** de execução

## 📈 Próximos Passos

1. **Implementar Telas 6-13**
2. **Captura completa de dados finais**
3. **Tratamento de modais e popups**
4. **Otimização de performance**
5. **Testes automatizados**

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é privado e pertence à Imediato Soluções em Seguros.

## 👨‍💻 Autor

**Luciano Otero** - [LucianoOtero](https://github.com/LucianoOtero)

---

**Versão**: 2.11.0  
**Última atualização**: 2025-09-02  
**Status**: Em desenvolvimento ativo
