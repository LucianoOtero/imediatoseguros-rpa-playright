import requests
import json
import time
from datetime import datetime

# --- CONFIGURAÇÕES ---
API_URL = "https://bpsegurosimediato.com.br/logging_system/debug_logger_db.php"
ANALYTICS_URL = "https://bpsegurosimediato.com.br/logging_system/viewer/api/analytics.php"
# --- FIM CONFIGURAÇÕES ---

def check_log_in_database(session_id=None, message_filter=None):
    """Verifica se o log está no banco de dados."""
    print("VERIFICANDO LOG NO BANCO DE DADOS")
    print("=" * 60)
    
    params = {'action': 'logs', 'limit': 50}
    if session_id:
        params['session_id'] = session_id
    if message_filter:
        params['message'] = message_filter
    
    try:
        response = requests.get(ANALYTICS_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                logs = result.get('logs', [])
                print(f"Total de logs encontrados: {len(logs)}")
                
                # Procurar pelo log específico do Footer Code
                footer_logs = []
                for log in logs:
                    if isinstance(log.get('message'), str):
                        try:
                            message_data = json.loads(log['message'])
                            if 'RPA habilitado via PHP Log' in str(message_data):
                                footer_logs.append(log)
                        except:
                            if 'RPA habilitado via PHP Log' in log.get('message', ''):
                                footer_logs.append(log)
                
                if footer_logs:
                    print(f"LOGS DO FOOTER CODE ENCONTRADOS: {len(footer_logs)}")
                    for i, log in enumerate(footer_logs):
                        print(f"   {i+1}. [{log['level']}] {log['timestamp']} | {log['session_id']}")
                        print(f"      Message: {log['message']}")
                        print(f"      URL: {log['url']}")
                    return True
                else:
                    print("NENHUM LOG DO FOOTER CODE ENCONTRADO")
                    print("Ultimos logs encontrados:")
                    for i, log in enumerate(logs[:5]):
                        print(f"   {i+1}. [{log['level']}] {log['timestamp']} | {log['session_id']}")
                        print(f"      Message: {log['message']}")
                    return False
            else:
                print(f"Erro na API: {result.get('message', 'Desconhecido')}")
                return False
        else:
            print(f"Erro HTTP: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisicao: {e}")
        return False

def test_direct_log_send():
    """Testa envio direto de log para verificar se o endpoint funciona."""
    print("\nTESTANDO ENVIO DIRETO DE LOG")
    print("=" * 60)
    
    log_data = {
        "level": "INFO",
        "message": "RPA habilitado via PHP Log",
        "data": {
            "rpaEnabled": False,
            "timestamp": datetime.now().isoformat(),
            "url": "https://www.segurosimediato.com.br",
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "sessionId": "test_" + str(int(time.time()))
        },
        "timestamp": datetime.now().isoformat(),
        "sessionId": "test_" + str(int(time.time())),
        "url": "https://www.segurosimediato.com.br",
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.post(API_URL, json=log_data, timeout=10)
        print(f"Enviando log de teste...")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Resposta: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if result.get('success'):
                print("LOG DE TESTE ENVIADO COM SUCESSO!")
                return True
            else:
                print(f"Erro no servidor: {result.get('error')}")
                return False
        else:
            print(f"Erro HTTP: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisicao: {e}")
        return False

def main():
    print("TESTE DE SENSIBILIZACAO DO LOG")
    print("=" * 60)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API URL: {API_URL}")
    print(f"Analytics URL: {ANALYTICS_URL}")
    
    # Teste 1: Verificar logs existentes
    print("\n" + "="*60)
    print("TESTE 1: VERIFICAR LOGS EXISTENTES")
    print("="*60)
    logs_exist = check_log_in_database(message_filter="RPA habilitado via PHP Log")
    
    # Teste 2: Enviar log de teste
    print("\n" + "="*60)
    print("TESTE 2: ENVIAR LOG DE TESTE")
    print("="*60)
    test_sent = test_direct_log_send()
    
    # Aguardar um pouco para o log ser processado
    if test_sent:
        print("\nAguardando 3 segundos para processamento...")
        time.sleep(3)
        
        # Teste 3: Verificar se o log de teste foi salvo
        print("\n" + "="*60)
        print("TESTE 3: VERIFICAR SE LOG DE TESTE FOI SALVO")
        print("="*60)
        test_log_saved = check_log_in_database(message_filter="RPA habilitado via PHP Log")
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    print(f"Logs existentes encontrados: {'SIM' if logs_exist else 'NAO'}")
    print(f"Log de teste enviado: {'SIM' if test_sent else 'NAO'}")
    if test_sent:
        print(f"Log de teste salvo no banco: {'SIM' if test_log_saved else 'NAO'}")
    
    if test_sent and test_log_saved:
        print("\nCONCLUSAO: Sistema de logging esta funcionando!")
        print("   O problema pode estar na execucao do JavaScript no website.")
    elif test_sent and not test_log_saved:
        print("\nCONCLUSAO: Log e enviado mas nao e salvo no banco!")
        print("   Problema no processamento do servidor PHP.")
    else:
        print("\nCONCLUSAO: Problema no envio do log!")
        print("   Verificar conectividade e configuracao do servidor.")

if __name__ == "__main__":
    main()