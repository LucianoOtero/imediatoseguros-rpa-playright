# 📋 GUIA PASSO-A-PASSO: CONFIGURAÇÃO GTM + GOOGLE ADS
## Conversão Modal WhatsApp - Ação Separada

**Data de Criação:** 02/11/2025  
**Objetivo:** Configurar registro de conversões do Modal WhatsApp como ação separada no Google Ads  
**Evento GTM:** `whatsapp_modal_initial_contact`

---

## 📊 INFORMAÇÕES DO EVENTO

### **Evento Disparado pelo Modal:**
- **Nome do Evento:** `whatsapp_modal_initial_contact`
- **Quando Dispara:** Usuário preenche DDD + Celular no modal WhatsApp
- **Arquivo:** `MODAL_WHATSAPP_DEFINITIVO.js`
- **Função:** `registrarConversaoInicialGTM()` (linha 1093)
- **Container GTM:** `GTM-PD6J398`

### **Dados Disponíveis no Evento:**
```javascript
{
  'event': 'whatsapp_modal_initial_contact',
  'form_type': 'whatsapp_modal',
  'contact_stage': 'initial',
  'phone_ddd': '11',
  'phone_number': '***',
  'has_phone': true,
  'gclid': 'Teste_Luciano_202511021424',
  'utm_source': '',
  'utm_campaign': '',
  'utm_medium': '',
  'utm_term': '',
  'utm_content': '',
  'page_url': 'https://www.segurosimediato.com.br/',
  'page_title': 'Seguro Imediato',
  'user_agent': '...',
  'timestamp': '2025-11-02T17:25:56.670Z',
  'environment': 'prod'
}
```

---

## 🎯 PASSO 1: CRIAR AÇÃO DE CONVERSÃO NO GOOGLE ADS

### **1.1. Acessar Google Ads**

1. Acesse: https://ads.google.com/
2. Faça login na sua conta Google
3. Selecione a conta/agência correta

### **1.2. Acessar Metas → Conversões**

1. No menu lateral esquerdo, clique em **Metas**
2. No submenu, clique em **Conversões**

### **1.3. Criar Nova Ação de Conversão**

1. Clique no botão **+ Nova ação de conversão** (botão azul no canto superior)
2. Selecione **Site** como origem da conversão

### **1.4. Configurar Detalhes da Conversão**

#### **Categoria:**
- Selecione: **Lead** (ou outra categoria conforme sua estratégia)

#### **Nome:**
- **Nome:** `Modal WhatsApp - Primeiro Contato`
- **Descrição:** `Conversão quando usuário preenche DDD + Celular no modal WhatsApp` (opcional)

#### **Valor:**
- **Como você deseja medir o valor?**
  - Opção 1: **Não usar valor** (apenas contar conversões) - ✅ **Recomendado para leads**
  - Opção 2: **Usar o mesmo valor para cada conversão** (ex: R$ 10,00)
  - Opção 3: **Usar diferentes valores para cada conversão** (se tiver valor variável)

#### **Contagem:**
- **Quantas conversões você deseja contar?**
  - **Uma** (recomendado para leads) - ✅ **Recomendado**
  - Ou **Todas** (se quiser contar múltiplos contatos do mesmo usuário)

#### **Janela de Conversão:**
- **Período de clique:** `30 dias` (ou conforme sua estratégia)
- **Período de visualização:** `1 dia` (ou conforme sua estratégia)

#### **Modelo de Atribuição:**
- Escolha o modelo que melhor se adequa à sua análise (ex: Último clique, Primeiro clique, etc.)

#### **Incluir em Conversões:**
- ⚠️ **NÃO marque** ainda (vamos configurar depois de testar)
- Você pode incluir depois se esta for uma conversão importante

### **1.5. Salvar e Obter ID de Conversão**

1. Clique em **Criar e continuar** (ou **Salvar**)
2. Na próxima tela, escolha **"Usar o Gerenciador de tags do Google"** (Google Tag Manager)
   - ⚠️ **NÃO escolha** "Instalar o código de rastreamento"
3. Você verá o **ID de Conversão** e o **Rótulo de Conversão**:
   - Formato do ID: `AW-1234567890`
   - Formato do Rótulo: `abc123def456` ou similar
   - **Combinação completa:** `AW-1234567890/abc123def456`
4. **⚠️ COPIE E GUARDE ESTAS INFORMAÇÕES!** Você precisará delas nos próximos passos.

---

## 🎯 PASSO 2: CONFIGURAR VARIÁVEIS NO GTM

### **2.1. Criar Variável para Nome do Evento**

1. Acesse: https://tagmanager.google.com/
2. Selecione o container: **GTM-PD6J398**
3. No menu lateral esquerdo, clique em **Variáveis**
4. Clique em **Novo** (botão no canto superior direito)
5. **Nome:** `Event - Modal WhatsApp Contact`
6. Clique em **Configuração da variável** → Selecione **Nome do evento**
7. **Salvar**

### **2.2. Criar Variável para GCLID**

1. No mesmo container GTM, **Variáveis → Novo**
2. **Nome:** `GCLID - Modal WhatsApp`
3. Clique em **Configuração da variável** → Selecione **Variável de camada de dados**
4. **Nome da variável da camada de dados:** `gclid`
5. **Versão da camada de dados:** `2`
6. **Salvar**

### **2.3. Criar Variável para Page URL**

1. **Variáveis → Novo**
2. **Nome:** `Page URL - Modal WhatsApp`
3. **Configuração da variável** → **Variável de camada de dados**
4. **Nome da variável da camada de dados:** `page_url`
5. **Versão da camada de dados:** `2`
6. **Salvar**

### **2.4. Criar Variável para UTM Source**

1. **Variáveis → Novo**
2. **Nome:** `UTM Source - Modal WhatsApp`
3. **Configuração da variável** → **Variável de camada de dados**
4. **Nome da variável da camada de dados:** `utm_source`
5. **Versão da camada de dados:** `2`
6. **Salvar**

### **2.5. Criar Variável para UTM Campaign**

1. **Variáveis → Novo**
2. **Nome:** `UTM Campaign - Modal WhatsApp`
3. **Configuração da variável** → **Variável de camada de dados**
4. **Nome da variável da camada de dados:** `utm_campaign`
5. **Versão da camada de dados:** `2`
6. **Salvar**

---

## 🎯 PASSO 3: CRIAR TRIGGER NO GTM

### **3.1. Criar Trigger para Modal WhatsApp**

1. No container GTM, clique em **Acionadores** (ou **Triggers**) no menu lateral
2. Clique em **Novo**
3. **Nome:** `Modal WhatsApp - Initial Contact`
4. Clique em **Configuração do acionador** → Selecione **Evento personalizado**
5. **Nome do evento:** `whatsapp_modal_initial_contact`
   - ⚠️ **DEVE SER EXATAMENTE:** `whatsapp_modal_initial_contact`
   - ⚠️ **Case-sensitive** (maiúsculas/minúsculas importam)
6. **Este acionador é acionado em:** Deixe como "Todos os eventos" (padrão)
7. **Salvar**

### **3.2. Verificar Trigger (Opcional mas Recomendado)**

1. No GTM, clique em **Visualizar** (botão no canto superior direito)
2. Insira a URL: `https://www.segurosimediato.com.br/`
3. Clique em **Conectar**
4. No navegador que abrir:
   - Abra o modal WhatsApp
   - Preencha DDD + Celular
5. **Verificar no painel de visualização do GTM:**
   - ✅ Evento `whatsapp_modal_initial_contact` deve aparecer na lista
   - ✅ Deve mostrar os dados do evento

---

## 🎯 PASSO 4: CRIAR TAG DE CONVERSÃO NO GTM

### **4.1. Criar Tag Google Ads: Conversão**

1. No container GTM, clique em **Tags** no menu lateral
2. Clique em **Novo**
3. **Nome da Tag:** `Google Ads - Conversão Modal WhatsApp`
4. Clique em **Configuração da tag** → Selecione **Google Ads: Conversão**
5. **ID de Conversão:** Cole o ID completo que você copiou no Passo 1
   - Formato: `AW-1234567890/abc123def456`
   - Ou cole separadamente: ID `AW-1234567890` e Rótulo `abc123def456`
6. **Valor de Conversão:**
   - **Usar valor fixo:** `1`
   - Ou deixe vazio se não usar valor (conforme configurado no Google Ads)
7. **Moeda da conversão:** `BRL` (ou deixe vazio se não usar valor)
8. Clique em **Acionamento** → Selecione o trigger `Modal WhatsApp - Initial Contact`
9. **Salvar**

### **4.2. Adicionar Variáveis à Tag (Opcional - Recomendado)**

**Parâmetros de Conversão Adicionais:**

1. Na tag criada, clique em **Mais configurações**
2. Expanda **Parâmetros de conversão**
3. Clique em **Adicionar linha**
4. Adicione os seguintes parâmetros (um por linha):
   - **Nome do parâmetro:** `gclid`
   - **Valor:** `{{GCLID - Modal WhatsApp}}`
   
   - **Nome do parâmetro:** `page_url`
   - **Valor:** `{{Page URL - Modal WhatsApp}}`
   
   - **Nome do parâmetro:** `utm_source`
   - **Valor:** `{{UTM Source - Modal WhatsApp}}`
   
   - **Nome do parâmetro:** `utm_campaign`
   - **Valor:** `{{UTM Campaign - Modal WhatsApp}}`

**Importante:** Esses parâmetros são opcionais mas ajudam no rastreamento e análise.

---

## 🎯 PASSO 5: PUBLICAR CONTAINER NO GTM

### **5.1. Revisar Configuração Antes de Publicar**

Verifique se está tudo correto:
- ✅ Tag criada com ID de conversão correto
- ✅ Trigger configurado corretamente
- ✅ Variáveis criadas (se for usar parâmetros adicionais)

### **5.2. Publicar Container**

1. No GTM, clique em **Enviar** (botão no canto superior direito)
2. Na tela de resumo, verifique:
   - Tags que serão publicadas
   - Acionadores que serão publicados
   - Variáveis que serão publicadas
3. **Nome da versão:** `Conversão Modal WhatsApp - Configuração Inicial`
4. **Descrição:** `Adicionada tag de conversão para Modal WhatsApp com evento whatsapp_modal_initial_contact`
5. Clique em **Publicar**
6. ✅ Container publicado com sucesso!

---

## 🎯 PASSO 6: VERIFICAR CONFIGURAÇÃO NO GOOGLE ADS

### **6.1. Confirmar Configuração da Ação de Conversão**

1. **Google Ads → Metas → Conversões**
2. Abra a ação **`Modal WhatsApp - Primeiro Contato`**
3. Verifique:
   - ✅ **Método de instalação:** "Gerenciador de tags do Google" ou "Google Tag Manager"
   - ✅ **Status:** Deve aparecer como "Ativo" ou "Verificando" (pode demorar alguns minutos)
   - ✅ **ID de conversão** está correto

---

## 🧪 PASSO 7: TESTAR A CONFIGURAÇÃO

### **7.1. Teste 1: Modo de Visualização do GTM**

1. No GTM, clique em **Visualizar** (botão no canto superior direito)
2. Insira a URL: `https://www.segurosimediato.com.br/`
3. Clique em **Conectar**
4. No navegador que abrir:
   - Abra o modal WhatsApp
   - Preencha DDD + Celular (ex: DDD: 11, Celular: 976687668)
5. **Verificar no painel de visualização do GTM:**
   - ✅ Evento `whatsapp_modal_initial_contact` deve aparecer
   - ✅ Tag `Google Ads - Conversão Modal WhatsApp` deve estar marcada como "Disparada"
   - ✅ Verifique os dados do evento enviados

### **7.2. Teste 2: Verificar DataLayer no Console**

1. Abra o Console do navegador (F12)
2. Abra o modal WhatsApp
3. Preencha DDD + Celular
4. No console, digite:
   ```javascript
   window.dataLayer.filter(item => item.event === 'whatsapp_modal_initial_contact')
   ```
5. **Verificar:**
   - ✅ Deve retornar objeto com `event: 'whatsapp_modal_initial_contact'`
   - ✅ Deve conter `gclid`, `utm_source`, etc.

### **7.3. Teste 3: Verificar no Google Ads (24-48h após teste)**

1. **Google Ads → Metas → Conversões**
2. Abra **`Modal WhatsApp - Primeiro Contato`**
3. **Verificar:**
   - ✅ Conversões devem aparecer (pode levar até 48h para aparecer)
   - ✅ Dados devem estar corretos (se configurou parâmetros adicionais)
   - ✅ Status deve mudar de "Verificando" para "Ativo" após algumas horas

---

## 🔍 PASSO 8: VERIFICAÇÃO E MONITORAMENTO

### **8.1. Verificar Disparos em Tempo Real**

**Google Ads:**
1. **Google Ads → Metas → Conversões**
2. Clique na ação de conversão `Modal WhatsApp - Primeiro Contato`
3. **Ver "Conversões"** (pode demorar algumas horas para aparecer)
4. Na aba **"Resumo"**, você verá as conversões registradas

**GTM:**
1. **GTM → Tags**
2. Verificar **"Disparos"** na tag criada

### **8.2. Verificar Dados no Google Ads (Relatórios)**

1. **Google Ads → Relatórios → Conversões**
2. Filtrar por **`Modal WhatsApp - Primeiro Contato`**
3. Analisar:
   - Quantidade de conversões
   - Custo por conversão
   - Taxa de conversão

---

## ⚙️ CONFIGURAÇÕES AVANÇADAS (OPCIONAL)

### **A. Valor Dinâmico de Conversão**

Se quiser usar valores diferentes para cada conversão:

1. **GTM → Variáveis → Nova**
2. **Nome:** `Conversion Value - Modal WhatsApp`
3. **Tipo:** Variável de Camada de Dados
4. **Nome da Variável:** `conversion_value`
5. **Na Tag:** Configure **"Usar valor fixo"** como `{{Conversion Value - Modal WhatsApp}}`

**No código (MODAL_WHATSAPP_DEFINITIVO.js):**
```javascript
// Adicionar na linha ~1145 do objeto gtmEventData:
'conversion_value': valorCalculado || 1
```

### **B. Múltiplas Conversões com Diferentes Valores**

Se tiver diferentes tipos de leads (ex: seguro-auto vs seguro-residencial):

1. Criar trigger adicional com condição no `form_type` ou `contact_stage`
2. Criar tag adicional com valor específico
3. Conectar ao mesmo ID de conversão (Google Ads conta tudo junto)
   - Ou criar ações de conversão separadas no Google Ads

---

## 🐛 TROUBLESHOOTING

### **Problema 1: Tag não dispara**

**Verificar:**
- ✅ Trigger está correto? (`whatsapp_modal_initial_contact`)
- ✅ Evento está sendo enviado ao dataLayer?
  ```javascript
  // Console do navegador:
  window.dataLayer.filter(item => item.event === 'whatsapp_modal_initial_contact')
  ```
- ✅ Container GTM está carregado?
- ✅ Modo de pré-visualização mostra o trigger disparando?

**Solução:**
- Verificar nome exato do evento no código vs. trigger
- Verificar se dataLayer existe: `typeof window.dataLayer !== 'undefined'`

### **Problema 2: Conversões não aparecem no Google Ads**

**Verificar:**
- ✅ ID de conversão está correto na tag?
- ✅ Tag está publicada no GTM?
- ✅ Container GTM está instalado no site?
- ⏰ Aguardar 24-48h (conversões podem demorar para aparecer)

**Solução:**
- Revisar configuração da tag
- Verificar disparos da tag no GTM
- Confirmar que evento está sendo enviado

### **Problema 3: GCLID não está sendo capturado**

**Verificar:**
- ✅ URL tem `?gclid=...` ou `&gclid=...`?
- ✅ Código está capturando GCLID corretamente?
  ```javascript
  // Console do navegador:
  console.log(window.dataLayer.filter(item => item.gclid))
  ```

**Solução:**
- Verificar captura de GCLID no `FooterCodeSiteDefinitivoCompleto_prod.js`
- Testar com URL contendo GCLID

---

## 📋 CHECKLIST DE CONFIGURAÇÃO

### **GTM:**
- [ ] Variáveis criadas (Event, GCLID, Page URL, UTM Source, UTM Campaign)
- [ ] Trigger `Modal WhatsApp - Initial Contact` criado e testado
- [ ] Tag `Google Ads - Conversão Modal WhatsApp` criada
- [ ] ID de Conversão do Google Ads configurado na tag
- [ ] Container publicado no GTM

### **Google Ads:**
- [ ] Ação de conversão `Modal WhatsApp - Primeiro Contato` criada
- [ ] ID de Conversão copiado e configurado no GTM
- [ ] Configurações de atribuição ajustadas
- [ ] Categoria e tipo configurados

### **Testes:**
- [ ] Modo de pré-visualização do GTM testado
- [ ] Evento verificado no dataLayer (console)
- [ ] Tag dispara corretamente no teste
- [ ] Conversões aparecem no Google Ads (24-48h após)

---

## 📊 ESTRUTURA FINAL

```
GTM (GTM-PD6J398)
├── Variáveis
│   ├── Event - Modal WhatsApp Contact
│   ├── GCLID - Modal WhatsApp
│   ├── Page URL - Modal WhatsApp
│   ├── UTM Source - Modal WhatsApp
│   └── UTM Campaign - Modal WhatsApp
├── Triggers
│   └── Modal WhatsApp - Initial Contact
│       └── Evento: whatsapp_modal_initial_contact
└── Tags
    └── Google Ads - Conversão Modal WhatsApp
        ├── ID de Conversão: AW-XXXXXXXXX/XXXXXXXXX
        ├── Valor: 1
        ├── Moeda: BRL
        └── Trigger: Modal WhatsApp - Initial Contact

Google Ads
└── Conversões
    └── Modal WhatsApp - Primeiro Contato
        ├── Tipo: Website
        ├── Método: Google Tag Manager
        └── ID: AW-XXXXXXXXX/XXXXXXXXX
```

---

## 📞 SUPORTE

Se encontrar problemas:

1. **Verificar logs do console:**
   - Procurar por `[GTM]` nos logs
   - Verificar erros no console

2. **Verificar dataLayer:**
   ```javascript
   // Console:
   console.log(window.dataLayer)
   ```

3. **Testar em modo de pré-visualização do GTM:**
   - Mais confiável para debugar
   - ⚠️ **IMPORTANTE:** Se a tag não disparar no Preview Mode, verifique se a opção "Dispare essa tag apenas em contêineres publicados" está marcada nas "Configurações avançadas" da tag. Se estiver marcada, desmarque para testar, ou publique o contêiner para funcionar em produção.

4. **Tag não dispara no Preview Mode:**
   - Verifique se "Dispare essa tag apenas em contêineres publicados" está desmarcada nas Configurações avançadas
   - Verifique se o trigger está disparando corretamente
   - Verifique se o evento está sendo enviado ao dataLayer: `window.dataLayer.filter(item => item.event === 'whatsapp_modal_initial_contact')`

5. **Verificar documentação:**
   - [GTM Help](https://support.google.com/tagmanager)
   - [Google Ads Conversões](https://support.google.com/google-ads/answer/1727054)

---

**Data de Criação:** 02/11/2025  
**Última Atualização:** 02/11/2025 19:30  
**Status:** ✅ Guia atualizado com interface atual do Google Ads e GTM (2025)  
**Nota:** Incluído troubleshooting sobre "Dispare essa tag apenas em contêineres publicados"

