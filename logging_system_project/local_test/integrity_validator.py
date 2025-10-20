#!/usr/bin/env python3
"""
🔒 INTEGRITY VALIDATOR - SISTEMA DE LOGGING PHP
Valida integridade do banco de dados e estrutura do sistema
"""

import mysql.connector
import json
import time
from datetime import datetime, timedelta

class IntegrityValidator:
    def __init__(self, config):
        """Inicializa validador de integridade"""
        self.config = config
        self.results = {
            'start_time': datetime.now(),
            'checks': {},
            'status': 'UNKNOWN'
        }
        self.connection = None
    
    def run_all_checks(self):
        """Executa todas as verificações de integridade"""
        print("🔒 Executando verificações de integridade...")
        
        try:
            # Conectar ao banco
            self.connect_to_database()
            
            # 1. Verificar estrutura das tabelas
            self.results['checks']['table_structure'] = self.check_table_structure()
            
            # 2. Verificar índices
            self.results['checks']['indexes'] = self.check_indexes()
            
            # 3. Verificar consistência de dados
            self.results['checks']['data_consistency'] = self.check_data_consistency()
            
            # 4. Verificar performance
            self.results['checks']['performance'] = self.check_performance()
            
            # 5. Verificar logs recentes
            self.results['checks']['recent_logs'] = self.check_recent_logs()
            
            # Determinar status geral
            self.determine_overall_status()
            
        except Exception as e:
            self.results['status'] = 'FAILED'
            self.results['error'] = str(e)
            print(f"❌ Erro crítico: {e}")
        finally:
            if self.connection:
                self.connection.close()
        
        self.results['duration'] = (datetime.now() - self.results['start_time']).total_seconds()
        return self.results
    
    def connect_to_database(self):
        """Conecta ao banco de dados"""
        try:
            db_config = self.config['database']
            self.connection = mysql.connector.connect(
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['database'],
                user=db_config['username'],
                password=db_config['password'],
                connection_timeout=10
            )
        except mysql.connector.Error as e:
            raise Exception(f"Erro de conexão com banco: {e}")
    
    def check_table_structure(self):
        """Verifica estrutura das tabelas"""
        print("  📋 Verificando estrutura das tabelas...")
        start_time = time.time()
        
        try:
            cursor = self.connection.cursor()
            
            # Verificar se tabela debug_logs existe
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = %s AND table_name = 'debug_logs'
            """, (self.config['database']['database'],))
            
            table_exists = cursor.fetchone()[0] > 0
            
            if not table_exists:
                return {
                    'status': 'FAILED',
                    'duration': time.time() - start_time,
                    'message': 'Tabela debug_logs não existe'
                }
            
            # Verificar estrutura da tabela
            cursor.execute("DESCRIBE debug_logs")
            columns = cursor.fetchall()
            
            expected_columns = [
                'id', 'log_id', 'session_id', 'timestamp', 'client_timestamp',
                'level', 'message', 'data', 'url', 'user_agent', 'ip_address',
                'server_time', 'request_id', 'created_at'
            ]
            
            actual_columns = [col[0] for col in columns]
            missing_columns = set(expected_columns) - set(actual_columns)
            extra_columns = set(actual_columns) - set(expected_columns)
            
            cursor.close()
            
            duration = time.time() - start_time
            
            if missing_columns:
                return {
                    'status': 'FAILED',
                    'duration': duration,
                    'message': f'Colunas faltando: {missing_columns}',
                    'missing_columns': list(missing_columns),
                    'extra_columns': list(extra_columns)
                }
            elif extra_columns:
                return {
                    'status': 'WARNING',
                    'duration': duration,
                    'message': f'Colunas extras encontradas: {extra_columns}',
                    'extra_columns': list(extra_columns)
                }
            else:
                return {
                    'status': 'PASSED',
                    'duration': duration,
                    'message': 'Estrutura da tabela está correta',
                    'columns': actual_columns
                }
                
        except mysql.connector.Error as e:
            return {
                'status': 'FAILED',
                'duration': time.time() - start_time,
                'message': f'Erro MySQL: {e}'
            }
    
    def check_indexes(self):
        """Verifica índices da tabela"""
        print("  🔍 Verificando índices...")
        start_time = time.time()
        
        try:
            cursor = self.connection.cursor()
            
            # Verificar índices existentes
            cursor.execute("""
                SELECT INDEX_NAME, COLUMN_NAME, NON_UNIQUE
                FROM information_schema.STATISTICS 
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'debug_logs'
                ORDER BY INDEX_NAME, SEQ_IN_INDEX
            """, (self.config['database']['database'],))
            
            indexes = cursor.fetchall()
            
            # Índices esperados
            expected_indexes = [
                'PRIMARY',
                'idx_session_timestamp',
                'idx_level_timestamp',
                'idx_url_timestamp',
                'idx_timestamp',
                'idx_log_id'
            ]
            
            actual_indexes = list(set([idx[0] for idx in indexes]))
            missing_indexes = set(expected_indexes) - set(actual_indexes)
            
            cursor.close()
            duration = time.time() - start_time
            
            if missing_indexes:
                return {
                    'status': 'WARNING',
                    'duration': duration,
                    'message': f'Índices faltando: {missing_indexes}',
                    'missing_indexes': list(missing_indexes),
                    'existing_indexes': actual_indexes
                }
            else:
                return {
                    'status': 'PASSED',
                    'duration': duration,
                    'message': 'Todos os índices necessários estão presentes',
                    'indexes': actual_indexes
                }
                
        except mysql.connector.Error as e:
            return {
                'status': 'FAILED',
                'duration': time.time() - start_time,
                'message': f'Erro MySQL: {e}'
            }
    
    def check_data_consistency(self):
        """Verifica consistência dos dados"""
        print("  🔄 Verificando consistência de dados...")
        start_time = time.time()
        
        try:
            cursor = self.connection.cursor()
            
            # Verificar logs com session_id nulo
            cursor.execute("SELECT COUNT(*) FROM debug_logs WHERE session_id IS NULL")
            null_sessions = cursor.fetchone()[0]
            
            # Verificar logs com message vazio
            cursor.execute("SELECT COUNT(*) FROM debug_logs WHERE message = '' OR message IS NULL")
            empty_messages = cursor.fetchone()[0]
            
            # Verificar logs com level inválido
            cursor.execute("""
                SELECT COUNT(*) FROM debug_logs 
                WHERE level NOT IN ('DEBUG', 'INFO', 'WARNING', 'ERROR')
            """)
            invalid_levels = cursor.fetchone()[0]
            
            # Verificar logs com timestamp futuro
            future_time = datetime.now() + timedelta(hours=1)
            cursor.execute("SELECT COUNT(*) FROM debug_logs WHERE timestamp > %s", (future_time,))
            future_timestamps = cursor.fetchone()[0]
            
            # Verificar duplicatas por log_id
            cursor.execute("""
                SELECT log_id, COUNT(*) as count 
                FROM debug_logs 
                GROUP BY log_id 
                HAVING COUNT(*) > 1
            """)
            duplicates = cursor.fetchall()
            
            cursor.close()
            duration = time.time() - start_time
            
            issues = []
            if null_sessions > 0:
                issues.append(f'{null_sessions} logs com session_id nulo')
            if empty_messages > 0:
                issues.append(f'{empty_messages} logs com message vazio')
            if invalid_levels > 0:
                issues.append(f'{invalid_levels} logs com level inválido')
            if future_timestamps > 0:
                issues.append(f'{future_timestamps} logs com timestamp futuro')
            if duplicates:
                issues.append(f'{len(duplicates)} log_ids duplicados')
            
            if issues:
                return {
                    'status': 'WARNING',
                    'duration': duration,
                    'message': f'Problemas de consistência encontrados: {", ".join(issues)}',
                    'issues': issues,
                    'null_sessions': null_sessions,
                    'empty_messages': empty_messages,
                    'invalid_levels': invalid_levels,
                    'future_timestamps': future_timestamps,
                    'duplicates': len(duplicates)
                }
            else:
                return {
                    'status': 'PASSED',
                    'duration': duration,
                    'message': 'Dados estão consistentes',
                    'null_sessions': null_sessions,
                    'empty_messages': empty_messages,
                    'invalid_levels': invalid_levels,
                    'future_timestamps': future_timestamps,
                    'duplicates': len(duplicates)
                }
                
        except mysql.connector.Error as e:
            return {
                'status': 'FAILED',
                'duration': time.time() - start_time,
                'message': f'Erro MySQL: {e}'
            }
    
    def check_performance(self):
        """Verifica performance das queries"""
        print("  ⚡ Verificando performance...")
        start_time = time.time()
        
        try:
            cursor = self.connection.cursor()
            
            # Teste 1: Query por session_id (deve usar índice)
            query_start = time.time()
            cursor.execute("""
                SELECT COUNT(*) FROM debug_logs 
                WHERE session_id = 'test_session' 
                AND timestamp > DATE_SUB(NOW(), INTERVAL 1 DAY)
            """)
            session_count = cursor.fetchone()[0]
            session_query_time = time.time() - query_start
            
            # Teste 2: Query por level (deve usar índice)
            query_start = time.time()
            cursor.execute("""
                SELECT COUNT(*) FROM debug_logs 
                WHERE level = 'ERROR' 
                AND timestamp > DATE_SUB(NOW(), INTERVAL 1 DAY)
            """)
            error_count = cursor.fetchone()[0]
            level_query_time = time.time() - query_start
            
            # Teste 3: Query por URL (deve usar índice)
            query_start = time.time()
            cursor.execute("""
                SELECT COUNT(*) FROM debug_logs 
                WHERE url LIKE '%segurosimediato.com.br%'
                AND timestamp > DATE_SUB(NOW(), INTERVAL 1 DAY)
            """)
            url_count = cursor.fetchone()[0]
            url_query_time = time.time() - query_start
            
            # Teste 4: Query complexa (múltiplos filtros)
            query_start = time.time()
            cursor.execute("""
                SELECT session_id, COUNT(*) as log_count
                FROM debug_logs 
                WHERE timestamp > DATE_SUB(NOW(), INTERVAL 1 DAY)
                GROUP BY session_id
                ORDER BY log_count DESC
                LIMIT 10
            """)
            top_sessions = cursor.fetchall()
            complex_query_time = time.time() - query_start
            
            cursor.close()
            duration = time.time() - start_time
            
            # Definir limites de performance (em segundos)
            max_query_time = 0.1  # 100ms
            
            performance_issues = []
            if session_query_time > max_query_time:
                performance_issues.append(f'Query por session_id: {session_query_time:.3f}s')
            if level_query_time > max_query_time:
                performance_issues.append(f'Query por level: {level_query_time:.3f}s')
            if url_query_time > max_query_time:
                performance_issues.append(f'Query por URL: {url_query_time:.3f}s')
            if complex_query_time > max_query_time * 2:
                performance_issues.append(f'Query complexa: {complex_query_time:.3f}s')
            
            if performance_issues:
                return {
                    'status': 'WARNING',
                    'duration': duration,
                    'message': f'Problemas de performance: {", ".join(performance_issues)}',
                    'performance_issues': performance_issues,
                    'query_times': {
                        'session_query': session_query_time,
                        'level_query': level_query_time,
                        'url_query': url_query_time,
                        'complex_query': complex_query_time
                    },
                    'max_acceptable_time': max_query_time
                }
            else:
                return {
                    'status': 'PASSED',
                    'duration': duration,
                    'message': 'Performance das queries está adequada',
                    'query_times': {
                        'session_query': session_query_time,
                        'level_query': level_query_time,
                        'url_query': url_query_time,
                        'complex_query': complex_query_time
                    },
                    'max_acceptable_time': max_query_time
                }
                
        except mysql.connector.Error as e:
            return {
                'status': 'FAILED',
                'duration': time.time() - start_time,
                'message': f'Erro MySQL: {e}'
            }
    
    def check_recent_logs(self):
        """Verifica logs recentes"""
        print("  📅 Verificando logs recentes...")
        start_time = time.time()
        
        try:
            cursor = self.connection.cursor()
            
            # Contar logs das últimas 24 horas
            cursor.execute("""
                SELECT COUNT(*) FROM debug_logs 
                WHERE timestamp > DATE_SUB(NOW(), INTERVAL 24 HOUR)
            """)
            recent_logs = cursor.fetchone()[0]
            
            # Contar logs por nível nas últimas 24 horas
            cursor.execute("""
                SELECT level, COUNT(*) as count 
                FROM debug_logs 
                WHERE timestamp > DATE_SUB(NOW(), INTERVAL 24 HOUR)
                GROUP BY level
                ORDER BY count DESC
            """)
            logs_by_level = cursor.fetchall()
            
            # Contar sessões únicas nas últimas 24 horas
            cursor.execute("""
                SELECT COUNT(DISTINCT session_id) FROM debug_logs 
                WHERE timestamp > DATE_SUB(NOW(), INTERVAL 24 HOUR)
            """)
            unique_sessions = cursor.fetchone()[0]
            
            # Verificar logs de teste (que devem ser removidos em produção)
            cursor.execute("""
                SELECT COUNT(*) FROM debug_logs 
                WHERE session_id LIKE '%test%' 
                OR message LIKE '%teste%'
                OR message LIKE '%Test%'
            """)
            test_logs = cursor.fetchone()[0]
            
            cursor.close()
            duration = time.time() - start_time
            
            return {
                'status': 'PASSED',
                'duration': duration,
                'message': f'Logs recentes verificados: {recent_logs} logs, {unique_sessions} sessões',
                'recent_logs_24h': recent_logs,
                'unique_sessions_24h': unique_sessions,
                'logs_by_level': dict(logs_by_level),
                'test_logs': test_logs
            }
            
        except mysql.connector.Error as e:
            return {
                'status': 'FAILED',
                'duration': time.time() - start_time,
                'message': f'Erro MySQL: {e}'
            }
    
    def determine_overall_status(self):
        """Determina status geral baseado nas verificações"""
        check_statuses = [check.get('status', 'UNKNOWN') for check in self.results['checks'].values()]
        
        if all(status == 'PASSED' for status in check_statuses):
            self.results['status'] = 'PASSED'
        elif any(status == 'FAILED' for status in check_statuses):
            self.results['status'] = 'FAILED'
        elif any(status == 'WARNING' for status in check_statuses):
            self.results['status'] = 'WARNING'
        else:
            self.results['status'] = 'UNKNOWN'
        
        # Contar resultados
        self.results['summary'] = {
            'total_checks': len(check_statuses),
            'passed': sum(1 for s in check_statuses if s == 'PASSED'),
            'failed': sum(1 for s in check_statuses if s == 'FAILED'),
            'warning': sum(1 for s in check_statuses if s == 'WARNING')
        }
