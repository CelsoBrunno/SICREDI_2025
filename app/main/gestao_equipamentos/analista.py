from app.db.database import get_db_connection
from datetime import datetime
import sqlite3

class AnalistaService:
    """
    Classe com serviços para funcionalidades do analista
    """
    
    def __init__(self):
        """
        Inicializa o serviço do analista
        """
        pass
    
    # ===== RESERVA DE EQUIPAMENTOS =====
    
    def listar_equipamentos_disponiveis(self, tipo=None):
        """
        Lista equipamentos disponíveis para reserva
        Args:
            tipo (str, optional): Tipo do equipamento ('mobilizado' ou 'imobilizado')
        Returns:
            list: Lista de equipamentos disponíveis
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if tipo:
            cursor.execute('''
                SELECT id, nome, descricao, tipo, codigo_patrimonio, localizacao, data_criacao
                FROM equipamentos 
                WHERE tipo = ? AND status = 'disponivel' AND ativo = 1
                ORDER BY nome
            ''', (tipo,))
        else:
            cursor.execute('''
                SELECT id, nome, descricao, tipo, codigo_patrimonio, localizacao, data_criacao
                FROM equipamentos 
                WHERE status = 'disponivel' AND ativo = 1
                ORDER BY tipo, nome
            ''')
        
        equipamentos = cursor.fetchall()
        conn.close()
        
        return [dict(equipamento) for equipamento in equipamentos]
    
    def criar_reserva_equipamento(self, usuario_id, equipamento_id, data_inicio, data_fim, observacoes=None):
        """
        Cria uma nova reserva de equipamento
        Args:
            usuario_id (int): ID do usuário que está fazendo a reserva
            equipamento_id (int): ID do equipamento a ser reservado
            data_inicio (str): Data/hora de início da reserva
            data_fim (str): Data/hora de fim da reserva
            observacoes (str, optional): Observações da reserva
        Returns:
            dict: Resultado da operação
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar se o equipamento está disponível
            cursor.execute('''
                SELECT id, nome, status FROM equipamentos 
                WHERE id = ? AND ativo = 1
            ''', (equipamento_id,))
            
            equipamento = cursor.fetchone()
            if not equipamento:
                return {'sucesso': False, 'erro': 'Equipamento não encontrado'}
            
            if equipamento['status'] != 'disponivel':
                return {'sucesso': False, 'erro': 'Equipamento não está disponível'}
            
            # Verificar se já existe uma reserva conflitante
            cursor.execute('''
                SELECT id FROM reservas 
                WHERE equipamento_id = ? 
                AND status IN ('pendente', 'aprovada')
                AND (
                    (data_inicio <= ? AND data_fim >= ?) OR
                    (data_inicio <= ? AND data_fim >= ?) OR
                    (data_inicio >= ? AND data_fim <= ?)
                )
            ''', (equipamento_id, data_inicio, data_inicio, data_fim, data_fim, data_inicio, data_fim))
            
            conflito = cursor.fetchone()
            if conflito:
                return {'sucesso': False, 'erro': 'Já existe uma reserva para este período'}
            
            # Criar a reserva
            cursor.execute('''
                INSERT INTO reservas (usuario_id, equipamento_id, data_inicio, data_fim, observacoes)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuario_id, equipamento_id, data_inicio, data_fim, observacoes))
            
            conn.commit()
            reserva_id = cursor.lastrowid
            
            conn.close()
            return {'sucesso': True, 'id': reserva_id, 'mensagem': 'Reserva criada com sucesso. Aguarde aprovação do gestor.'}
            
        except sqlite3.Error as e:
            conn.close()
            return {'sucesso': False, 'erro': f'Erro ao criar reserva: {str(e)}'}
    
    def listar_minhas_reservas(self, usuario_id, status=None):
        """
        Lista as reservas do analista
        Args:
            usuario_id (int): ID do usuário
            status (str, optional): Filtrar por status
        Returns:
            list: Lista de reservas do usuário
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''
                SELECT r.id, r.data_inicio, r.data_fim, r.status, r.observacoes, r.data_criacao,
                       e.nome as equipamento_nome, e.codigo_patrimonio, e.tipo as equipamento_tipo,
                       a.nome as ambiente_nome
                FROM reservas r
                LEFT JOIN equipamentos e ON r.equipamento_id = e.id
                LEFT JOIN ambientes a ON r.ambiente_id = a.id
                WHERE r.usuario_id = ? AND r.status = ?
                ORDER BY r.data_criacao DESC
            ''', (usuario_id, status))
        else:
            cursor.execute('''
                SELECT r.id, r.data_inicio, r.data_fim, r.status, r.observacoes, r.data_criacao,
                       e.nome as equipamento_nome, e.codigo_patrimonio, e.tipo as equipamento_tipo,
                       a.nome as ambiente_nome
                FROM reservas r
                LEFT JOIN equipamentos e ON r.equipamento_id = e.id
                LEFT JOIN ambientes a ON r.ambiente_id = a.id
                WHERE r.usuario_id = ?
                ORDER BY r.data_criacao DESC
            ''', (usuario_id,))
        
        reservas = cursor.fetchall()
        conn.close()
        
        return [dict(reserva) for reserva in reservas]
    
    def cancelar_reserva(self, reserva_id, usuario_id):
        """
        Cancela uma reserva do analista
        Args:
            reserva_id (int): ID da reserva
            usuario_id (int): ID do usuário (para verificar se é o dono da reserva)
        Returns:
            dict: Resultado da operação
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar se a reserva pertence ao usuário e pode ser cancelada
            cursor.execute('''
                SELECT id, status FROM reservas 
                WHERE id = ? AND usuario_id = ?
            ''', (reserva_id, usuario_id))
            
            reserva = cursor.fetchone()
            if not reserva:
                return {'sucesso': False, 'erro': 'Reserva não encontrada ou você não tem permissão para cancelá-la'}
            
            if reserva['status'] in ['cancelada', 'rejeitada']:
                return {'sucesso': False, 'erro': 'Esta reserva já foi cancelada ou rejeitada'}
            
            # Cancelar a reserva
            cursor.execute('''
                UPDATE reservas 
                SET status = 'cancelada', data_atualizacao = ?
                WHERE id = ?
            ''', (datetime.now(), reserva_id))
            
            # Se a reserva estava aprovada, liberar o equipamento
            if reserva['status'] == 'aprovada':
                cursor.execute('''
                    UPDATE equipamentos 
                    SET status = 'disponivel'
                    WHERE id = (SELECT equipamento_id FROM reservas WHERE id = ?)
                ''', (reserva_id,))
            
            conn.commit()
            conn.close()
            return {'sucesso': True, 'mensagem': 'Reserva cancelada com sucesso'}
            
        except sqlite3.Error as e:
            conn.close()
            return {'sucesso': False, 'erro': f'Erro ao cancelar reserva: {str(e)}'}
    
    # ===== ACESSO A AMBIENTES =====
    
    def listar_ambientes_disponiveis(self):
        """
        Lista todos os ambientes disponíveis
        Returns:
            list: Lista de ambientes
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nome, descricao, capacidade, equipamentos, data_criacao
            FROM ambientes 
            WHERE ativo = 1
            ORDER BY nome
        ''')
        
        ambientes = cursor.fetchall()
        conn.close()
        
        return [dict(ambiente) for ambiente in ambientes]
    
    def criar_reserva_ambiente(self, usuario_id, ambiente_id, data_inicio, data_fim, observacoes=None):
        """
        Cria uma nova reserva de ambiente
        Args:
            usuario_id (int): ID do usuário que está fazendo a reserva
            ambiente_id (int): ID do ambiente a ser reservado
            data_inicio (str): Data/hora de início da reserva
            data_fim (str): Data/hora de fim da reserva
            observacoes (str, optional): Observações da reserva
        Returns:
            dict: Resultado da operação
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar se o ambiente existe
            cursor.execute('''
                SELECT id, nome FROM ambientes 
                WHERE id = ? AND ativo = 1
            ''', (ambiente_id,))
            
            ambiente = cursor.fetchone()
            if not ambiente:
                return {'sucesso': False, 'erro': 'Ambiente não encontrado'}
            
            # Verificar se já existe uma reserva conflitante
            cursor.execute('''
                SELECT id FROM reservas 
                WHERE ambiente_id = ? 
                AND status IN ('pendente', 'aprovada')
                AND (
                    (data_inicio <= ? AND data_fim >= ?) OR
                    (data_inicio <= ? AND data_fim >= ?) OR
                    (data_inicio >= ? AND data_fim <= ?)
                )
            ''', (ambiente_id, data_inicio, data_inicio, data_fim, data_fim, data_inicio, data_fim))
            
            conflito = cursor.fetchone()
            if conflito:
                return {'sucesso': False, 'erro': 'Já existe uma reserva para este período'}
            
            # Criar a reserva
            cursor.execute('''
                INSERT INTO reservas (usuario_id, ambiente_id, data_inicio, data_fim, observacoes)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuario_id, ambiente_id, data_inicio, data_fim, observacoes))
            
            conn.commit()
            reserva_id = cursor.lastrowid
            
            conn.close()
            return {'sucesso': True, 'id': reserva_id, 'mensagem': 'Reserva de ambiente criada com sucesso. Aguarde aprovação do gestor.'}
            
        except sqlite3.Error as e:
            conn.close()
            return {'sucesso': False, 'erro': f'Erro ao criar reserva de ambiente: {str(e)}'}
    
    def verificar_disponibilidade_ambiente(self, ambiente_id, data_inicio, data_fim):
        """
        Verifica se um ambiente está disponível em um período
        Args:
            ambiente_id (int): ID do ambiente
            data_inicio (str): Data/hora de início
            data_fim (str): Data/hora de fim
        Returns:
            dict: Resultado da verificação
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar conflitos de reserva
            cursor.execute('''
                SELECT COUNT(*) as conflitos FROM reservas 
                WHERE ambiente_id = ? 
                AND status IN ('pendente', 'aprovada')
                AND (
                    (data_inicio <= ? AND data_fim >= ?) OR
                    (data_inicio <= ? AND data_fim >= ?) OR
                    (data_inicio >= ? AND data_fim <= ?)
                )
            ''', (ambiente_id, data_inicio, data_inicio, data_fim, data_fim, data_inicio, data_fim))
            
            resultado = cursor.fetchone()
            disponivel = resultado['conflitos'] == 0
            
            conn.close()
            return {
                'disponivel': disponivel,
                'mensagem': 'Ambiente disponível' if disponivel else 'Ambiente ocupado neste período'
            }
            
        except sqlite3.Error as e:
            conn.close()
            return {
                'disponivel': False,
                'mensagem': f'Erro ao verificar disponibilidade: {str(e)}'
            }
    
    def obter_historico_reservas(self, usuario_id, limite=10):
        """
        Obtém o histórico de reservas do analista
        Args:
            usuario_id (int): ID do usuário
            limite (int): Limite de registros a retornar
        Returns:
            list: Lista com histórico de reservas
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT r.id, r.data_inicio, r.data_fim, r.status, r.observacoes, r.data_criacao,
                   e.nome as equipamento_nome, e.codigo_patrimonio,
                   a.nome as ambiente_nome,
                   CASE 
                       WHEN r.equipamento_id IS NOT NULL THEN 'equipamento'
                       WHEN r.ambiente_id IS NOT NULL THEN 'ambiente'
                   END as tipo_reserva
            FROM reservas r
            LEFT JOIN equipamentos e ON r.equipamento_id = e.id
            LEFT JOIN ambientes a ON r.ambiente_id = a.id
            WHERE r.usuario_id = ?
            ORDER BY r.data_criacao DESC
            LIMIT ?
        ''', (usuario_id, limite))
        
        reservas = cursor.fetchall()
        conn.close()
        
        return [dict(reserva) for reserva in reservas]
