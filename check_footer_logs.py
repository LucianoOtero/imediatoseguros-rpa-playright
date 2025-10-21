import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime

# --- CONFIGURAÇÕES DO BANCO DE DADOS ---
DB_CONFIG = {
    'host': 'bpsegurosimediato.com.br',
    'port': 3306,
    'database': 'rpa_logs',
    'user': 'rpa_user',
    'password': 'RpaLogs2025!'
}
# --- FIM CONFIGURAÇÕES ---

def get_db_connection():
    """Estabelece e retorna uma conexão com o banco de dados."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"ERRO ao conectar: {e}")
        return None
    return None

def check_footer_code_logs(conn):
    """Busca logs específicos do Footer Code."""
    cursor = conn.cursor(dictionary=True)
    
    # Buscar logs que contenham a mensagem do Footer Code
    cursor.execute("""
        SELECT log_id, session_id, timestamp, level, message, data, url, ip_address 
        FROM debug_logs 
        WHERE message LIKE '%RPA habilitado via PHP Log%' 
        ORDER BY timestamp DESC 
        LIMIT 10
    """)
    
    logs = cursor.fetchall()
    cursor.close()
    return logs

def main():
    print("VERIFICACAO DE LOGS DO FOOTER CODE")
    print("=" * 60)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    conn = get_db_connection()
    if conn:
        print("OK - Conectado ao banco de dados MySQL")
        
        # Buscar logs do Footer Code
        footer_logs = check_footer_code_logs(conn)
        
        if footer_logs:
            print(f"\nLOGS DO FOOTER CODE ENCONTRADOS: {len(footer_logs)}")
            print("=" * 60)
            
            for i, log in enumerate(footer_logs):
                print(f"  {i+1}. [{log['level']}] {log['timestamp']} | {log['session_id']}")
                print(f"     Message: {log['message']}")
                print(f"     URL: {log['url']}")
                print(f"     IP: {log['ip_address']}")
                
                # Tentar decodificar os dados JSON
                try:
                    if log['data']:
                        data_obj = json.loads(log['data'])
                        print(f"     Dados: {json.dumps(data_obj, indent=2, ensure_ascii=False)}")
                except:
                    print(f"     Dados: {log['data']}")
                print()
            
            print("✅ CONFIRMADO: Logs do Footer Code estão sendo salvos no banco!")
        else:
            print("❌ ERRO: Nenhum log do Footer Code encontrado")
        
        conn.close()
        print("Desconectado do banco de dados")
    else:
        print("Não foi possível conectar ao banco de dados.")

if __name__ == "__main__":
    main()
