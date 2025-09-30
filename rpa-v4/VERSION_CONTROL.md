# Controle de Versão - RPA V4

## Versão Atual: 4.0.1

### Data: 30/09/2025

## Modificações Implementadas

### ✅ Correção de Compatibilidade com V3
- **Problema**: V4 não utilizava `parametros.json` como a V3
- **Solução**: Modificado `SessionService.php` para usar `--config /opt/imediatoseguros-rpa/parametros.json`
- **Status**: Implementado

### ✅ Validação Temporariamente Desabilitada
- **Problema**: Validação de entrada estava causando erros na V3
- **Solução**: Comentada validação no `RPAController.php`
- **Status**: Implementado

## TODO - Próximas Versões

### 🔄 Versão 4.1.0 - Chamada Robusta do RPA Modular
- **Objetivo**: Implementar chamada robusta do RPA modular/principal usando dados via linha de comando
- **Estratégia**: 
  1. Modificar script Python para aceitar parâmetros via linha de comando
  2. Implementar validação robusta de entrada na V4
  3. Criar sistema de mapeamento de dados da API para parâmetros do RPA
  4. Manter compatibilidade com `parametros.json` como fallback

### 📋 Tarefas para V4.1.0
- [ ] Analisar estrutura atual do `executar_rpa_modular_telas_1_a_5.py`
- [ ] Implementar suporte a parâmetros via linha de comando no script Python
- [ ] Criar sistema de validação robusta na V4
- [ ] Implementar mapeamento de dados da API para parâmetros do RPA
- [ ] Criar testes de compatibilidade V3 vs V4
- [ ] Documentar nova API de parâmetros

### 🎯 Estratégia de Migração
1. **Fase 1**: V4.0.1 (atual) - Compatibilidade total com V3
2. **Fase 2**: V4.1.0 - Chamada robusta com dados dinâmicos
3. **Fase 3**: V4.2.0 - Otimizações e melhorias
4. **Fase 4**: V5.0.0 - Nova arquitetura completa

## Notas Técnicas

### Arquivo de Configuração Atual
- **Localização**: `/opt/imediatoseguros-rpa/parametros.json`
- **Uso**: V3 e V4 (temporariamente)
- **Conteúdo**: Dados estáticos de configuração do RPA

### Comando Atual V4
```bash
python3 executar_rpa_modular_telas_1_a_5.py --config /opt/imediatoseguros-rpa/parametros.json --session-id $SESSION_ID
```

### Comando Futuro V4.1.0
```bash
python3 executar_rpa_modular_telas_1_a_5.py --session-id $SESSION_ID --cpf "$CPF" --nome "$NOME" --email "$EMAIL" --placa "$PLACA" --marca "$MARCA" --modelo "$MODELO" --ano "$ANO" --cep "$CEP"
```

## Histórico de Versões

### v4.0.0 (30/09/2025)
- Implementação inicial da arquitetura modular
- Dashboard web responsivo
- API REST completa
- Logs estruturados
- Health checks

### v4.0.1 (30/09/2025)
- Correção de compatibilidade com V3
- Uso de `parametros.json` como V3
- Validação temporariamente desabilitada
- Preparação para chamada robusta futura

## Próximos Passos

1. **Testar V4.0.1** com `parametros.json`
2. **Validar funcionamento** comparado com V3
3. **Planejar V4.1.0** com chamada robusta
4. **Implementar sistema de parâmetros dinâmicos**
5. **Migrar gradualmente** da V3 para V4

---

**Responsável**: Equipe de Desenvolvimento  
**Última Atualização**: 30/09/2025  
**Próxima Revisão**: 07/10/2025
