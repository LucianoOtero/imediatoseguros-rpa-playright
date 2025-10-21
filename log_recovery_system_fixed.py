import requests
import json
import time
from datetime import datetime
import argparse
import sys

# --- CONFIGURAÇÕES ---
API_BASE_URL = "https://bpsegurosimediato.com.br/logging_system/viewer/api/analytics.php"
# --- FIM CONFIGURAÇÕES ---

def fetch_logs(action, params=None):
    """Faz uma requisição à API de logs."""
    url = f"{API_BASE_URL}?action={action}"
    if params:
        for key, value in params.items():
            url += f"&{key}={value}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERRO na requisicao a API: {e}")
        return None

def safe_print(text):
    """Imprime texto de forma segura, removendo caracteres problemáticos."""
    try:
        # Remover emojis e caracteres especiais que causam problemas no Windows
        safe_text = text.encode('ascii', 'ignore').decode('ascii')
        print(safe_text)
    except:
        print("ERRO ao exibir texto")

def get_latest_session_id():
    """Busca o ID da última sessão registrada."""
    response = fetch_logs('logs', {'limit': 1})
    if response and response.get('success') and response['logs']:
        return response['logs'][0]['session_id']
    return None

def display_session_logs(session_id, export_file=None):
    """Exibe e opcionalmente exporta os logs de uma sessão."""
    safe_print(f"\nANALISANDO SESSAO: {session_id}")
    safe_print("=" * 60)
    
    response = fetch_logs('sessions', {'session_id': session_id})
    
    if not response or not response.get('success'):
        safe_print(f"ERRO HTTP: {response.get('status_code', 'N/A')}")
        safe_print(response.get('message', 'Sessao nao encontrada ou sem logs'))
        return

    logs = response['logs']
    summary = response.get('summary', {})

    safe_print("\nRESUMO DA SESSAO:")
    safe_print("=" * 60)
    safe_print(f"Total de logs: {summary.get('total_logs', len(logs))}")
    
    if 'level_distribution' in summary:
        safe_print("Distribuicao por nivel:")
        for level, count in summary['level_distribution'].items():
            safe_print(f"   {level}: {count}")
    
    if 'first_log' in summary:
        safe_print(f"Primeiro log: {summary['first_log']}")
    if 'last_log' in summary:
        safe_print(f"Ultimo log: {summary['last_log']}")

    safe_print(f"\nLOGS DA SESSAO ({len(logs)} entradas):")
    safe_print("=" * 80)
    for i, log in enumerate(logs):
        # Processar mensagem de forma segura
        message_data = log['message']
        if isinstance(message_data, str):
            try:
                message_data = json.loads(message_data)
            except:
                pass
        
        # Processar dados de forma segura
        log_data = log['data']
        if isinstance(log_data, str):
            try:
                log_data = json.loads(log_data)
            except:
                pass
        
        safe_print(f"  {i+1}. [{log['level']}] {log['timestamp']} | {log['url']}")
        safe_print(f"     Mensagem: {str(message_data)}")
        if log_data:
            safe_print(f"     Dados: {json.dumps(log_data, indent=2, ensure_ascii=False)}")
    
    if export_file:
        try:
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(response, f, indent=2, ensure_ascii=False)
            safe_print(f"Logs exportados para: {export_file}")
        except IOError as e:
            safe_print(f"ERRO ao exportar logs para {export_file}: {e}")

def search_footer_code_logs():
    """Busca especificamente logs do Footer Code."""
    safe_print("\nBUSCANDO LOGS DO FOOTER CODE")
    safe_print("=" * 60)
    
    response = fetch_logs('logs', {'limit': 50, 'message': 'RPA habilitado via PHP Log'})
    
    if not response or not response.get('success'):
        safe_print("ERRO ao buscar logs do Footer Code")
        return
    
    logs = response['logs']
    
    if logs:
        safe_print(f"LOGS DO FOOTER CODE ENCONTRADOS: {len(logs)}")
        safe_print("=" * 60)
        
        for i, log in enumerate(logs):
            safe_print(f"  {i+1}. [{log['level']}] {log['timestamp']} | {log['session_id']}")
            safe_print(f"     URL: {log['url']}")
            safe_print(f"     IP: {log['ip_address']}")
        
        safe_print("\n✅ CONFIRMADO: Logs do Footer Code estao sendo salvos no banco!")
    else:
        safe_print("❌ ERRO: Nenhum log do Footer Code encontrado")

def get_database_stats():
    """Obtém estatísticas gerais do banco de dados."""
    safe_print("\nESTATISTICAS DO BANCO DE DADOS")
    safe_print("=" * 60)
    
    response = fetch_logs('stats')
    
    if response and response.get('success'):
        stats = response.get('stats', {})
        safe_print(f"Total de logs: {stats.get('total_logs', 'N/A')}")
        safe_print(f"Sessoes unicas: {stats.get('unique_sessions', 'N/A')}")
        safe_print(f"Log mais antigo: {stats.get('oldest_log', 'N/A')}")
        safe_print(f"Log mais recente: {stats.get('most_recent_log', 'N/A')}")
        
        level_counts = stats.get('level_distribution', {})
        if level_counts:
            safe_print("\nDistribuicao por nivel:")
            for level, count in level_counts.items():
                safe_print(f"   {level}: {count}")
    else:
        safe_print("ERRO ao obter estatisticas do banco")

def main():
    parser = argparse.ArgumentParser(description="Sistema de Recuperacao de Logs RPA")
    parser.add_argument('--latest', action='store_true', help='Recupera a ultima sessao registrada.')
    parser.add_argument('--session', type=str, help='Especifica um ID de sessao para recuperar.')
    parser.add_argument('--export', type=str, help='Nome do arquivo para exportar os logs (JSON).')
    parser.add_argument('--footer', action='store_true', help='Busca especificamente logs do Footer Code.')
    parser.add_argument('--stats', action='store_true', help='Mostra estatisticas gerais do banco.')
    args = parser.parse_args()

    safe_print("SISTEMA DE RECUPERACAO DE LOGS RPA")
    safe_print("=" * 60)
    safe_print(f"Servidor: {API_BASE_URL.replace('/viewer/api/analytics.php', '')}")
    safe_print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if args.footer:
        search_footer_code_logs()
    elif args.stats:
        get_database_stats()
    elif args.latest:
        safe_print("Buscando ultima sessao...")
        session_id_to_fetch = get_latest_session_id()
        if session_id_to_fetch:
            safe_print(f"Ultima sessao encontrada: {session_id_to_fetch}")
            export_filename = args.export if args.export else f"logs_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            display_session_logs(session_id_to_fetch, export_filename)
        else:
            safe_print("Nenhuma sessao encontrada")
    elif args.session:
        session_id_to_fetch = args.session
        safe_print(f"Sessao especificada: {session_id_to_fetch}")
        export_filename = args.export if args.export else f"logs_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        display_session_logs(session_id_to_fetch, export_filename)
    else:
        safe_print("Opcoes disponiveis:")
        safe_print("  --latest     : Recupera a ultima sessao")
        safe_print("  --session ID : Recupera sessao especifica")
        safe_print("  --footer     : Busca logs do Footer Code")
        safe_print("  --stats      : Mostra estatisticas do banco")
        safe_print("  --export FILE: Exporta logs para arquivo JSON")

if __name__ == "__main__":
    main()
