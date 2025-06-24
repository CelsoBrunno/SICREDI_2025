from app.db.database import get_db_connection, hash_password
from datetime import datetime
import sqlite3

class GestorService:
    """
    Classe com serviços para funcionalidades do gestor
    """
    
    def __init__(self):
        """
        Inicializa o serviço do gestor
        """
        pass
    
    # ===== GERENCIAMENTO DE ANALISTAS =====
    
    def listar_analistas(self):
        """
        Lista todos os analistas cadastrados
        Returns:
            list: Lista de analistas
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nome, email, ativo, data_criacao, data_atualizacao
            FROM usuarios 
            WHERE tipo = 'analista'
            ORDER BY nome
        ''')
        
        analistas = cursor.fetchall()
        conn.close()
        
        return [dict(analista) for analista in analistas]
    
    def criar_analista(self, nome, email, senha):
        """
        Cria um novo analista
        Args:
            nome (str): Nome do analista
            email (str): Email do analista
            senha (str): Senha do analista
        Returns:
            dict: Resultado da operação com sucesso/erro
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar se o email já existe
            cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
            if cursor.fetchone():
                return {'sucesso': False, 'erro': 'Email já está em uso'}
            
            # Inserir novo analista
            senha_hash = hash_password(senha)
            cursor.execute('''
                INSERT INTO usuarios (nome, email, senha, tipo)
                VALUES (?, ?, ?, 'analista')
            ''', (nome, email, senha_hash))
            
            conn.commit()
            analista_id = cursor.lastrowid
            
            conn.close()
            return {'sucesso': True, 'id': analista_id, 'mensagem': 'Analista criado com sucesso'}
            
        except sqlite3.Error as e:
            conn.close()
            return {'sucesso': False, 'erro': f'Erro ao criar analista: {str(e)}'}
    
    def atualizar_analista(self, analista_id, nome=None, email=None, senha=None, ativo=None):
        """
        Atualiza dados de um analista
        Args:
            analista_id (int): ID do analista
            nome (str, optional): Novo nome
            email (str, optional): Novo email
            senha (str, optional): Nova senha
            ativo (bool, optional): Status ativo/inativo
        Returns:
            dict: Resultado da operação
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Construir query de atualização dinamicamente
            updates = []
            params = []
            
            if nome:
                updates.append('nome = ?')
                params.append(nome)
            
            if email:
                # Verificar se o email já está em uso por outro usuário
                cursor.execute('SELECT id FROM usuarios WHERE email = ? AND id != ?', (email, analista_id))
                if cursor.fetchone():
                    return {'sucesso': False, 'erro': 'Email já está em uso'}
                
                updates.append('email = ?')
                params.append(email)
            
            if senha:
                updates.append('senha = ?')
                params.append(hash_password(senha))
            
            if ativo is not None:
                updates.append('ativo = ?')
                params.append(ativo)
            
            if updates:
                updates.append('data_atualizacao = ?')
                params.append(datetime.now())
                params.append(analista_id)
                
                query = f'UPDATE usuarios SET {", ".join(updates)} WHERE id = ? AND tipo = "analista"'
                cursor.execute(query, params)
                
                if cursor.rowcount == 0:
                    return {'sucesso': False, 'erro': 'Analista não encontrado'}
                
                conn.commit()
            
            conn.close()
            return {'sucesso': True, 'mensagem': 'Analista atualizado com sucesso'}
            
        except sqlite3.Error as e:
            conn.close()
            return {'sucesso': False, 'erro': f'Erro ao atualizar analista: {str(e)}'}
    
    def excluir_analista(self, analista_id):
        """
        Exclui (inativa) um analista
        Args:
            analista_id (int): ID do analista
        Returns:
            dict: Resultado da operação
        """
        return self.atualizar_analista(analista_id, ativo=False)
    
    # ===== GERENCIAMENTO DE AMBIENTES =====
    
    def listar_ambientes(self):
        """
        Lista todos os ambientes cadastrados
        Returns:
            list: Lista de ambientes
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nome, descricao, capacidade, equipamentos, ativo, data_criacao, data_atualizacao
            FROM ambientes 
            WHERE ativo = 1
            ORDER BY nome
        ''')
        
        ambientes = cursor.fetchall()
        conn.close()
        
        return [dict(ambiente) for ambiente in ambientes]
    
    def criar_ambiente(self, nome, descricao=None, capacidade=None, equipamentos=None):
        """
        Cria um novo ambiente
        Args:
            nome (str): Nome do ambiente
            descricao (str): Descrição do ambiente
            capacidade (int): Capacidade de pessoas
            equipamentos (str): Lista de equipamentos
        Returns:
            dict: Resultado da operação
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO ambientes (nome, descricao, capacidade, equipamentos)
                VALUES (?, ?, ?, ?)
            ''', (nome, descricao, capacidade, equipamentos))
            
            conn.commit()
            ambiente_id = cursor.lastrowid
            
            conn.close()
            return {'sucesso': True, 'id': ambiente_id, 'mensagem': 'Ambiente criado com sucesso'}
            
        except sqlite3.Error as e:
            conn.close()
            return {'sucesso': False, 'erro': f'Erro ao criar ambiente: {str(e)}'}
    
    def atualizar_ambiente(self, ambiente_id, nome=None, descricao=None, capacidade=None, equipamentos=None):
        """
        Atualiza dados de um ambiente
        Args:
            ambiente_id (int): ID do ambiente
            nome (str, optional): Novo nome
            descricao (str, optional): Nova descrição
            capacidade (int, optional): Nova capacidade
            equipamentos (str, optional): Novos equipamentos
        Returns:
            dict: Resultado da operação
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            updates = []
            params = []
            
            if nome:
                updates.append('nome = ?')
                params.append(nome)
            
            if descricao is not None:
                updates.append('descricao = ?')
                params.append(descricao)
            
            if capacidade is not None:
                updates.append('capacidade = ?')
                params.append(capacidade)
            
            if equipamentos is not None:
                updates.append('equipamentos = ?')
                params.append(equipamentos)
            
            if updates:
                updates.append('data_atualizacao = ?')
                params.append(datetime.now())
                params.append(ambiente_id)
                
                query = f'UPDATE ambientes SET {", ".join(updates)} WHERE id = ?'
                cursor.execute(query, params)
                
                if cursor.rowcount == 0:
                    return {'sucesso': False, 'erro': 'Ambiente não encontrado'}
                
                conn.commit()
            
            conn.close()
            return {'sucesso': True, 'mensagem': 'Ambiente atualizado com sucesso'}
            
        except sqlite3.Error as e:
            conn.close()
            return {'sucesso': False, 'erro': f'Erro ao atualizar ambiente: {str(e)}'}
    
    def excluir_ambiente(self, ambiente_id):
        """
        Exclui (inativa) um ambiente
        Args:
            ambiente_id (int): ID do ambiente
        Returns:
            dict: Resultado da operação
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('UPDATE ambientes SET ativo = 0 WHERE id = ?', (ambiente_id,))
            
            if cursor.rowcount == 0:
                return {'sucesso': False, 'erro': 'Ambiente não encontrado'}
            
            conn.commit()
            conn.close()
            return {'sucesso': True, 'mensagem': 'Ambiente excluído com sucesso'}
            
        except sqlite3.Error as e:
            conn.close()
            return {'sucesso': False, 'erro': f'Erro ao excluir ambiente: {str(e)}'}
    
    # ===== GERENCIAMENTO DE EQUIPAMENTOS =====
    
    def listar_equipamentos(self, tipo=None):
        """
        Lista equipamentos por tipo
        Args:
            tipo (str, optional): Tipo do equipamento ('mobilizado' ou 'imobilizado')
        Returns:
            list: Lista de equipamentos
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if tipo:
            cursor.execute('''
                SELECT id, nome, descricao, tipo, codigo_patrimonio, status, localizacao, ativo, data_criacao
                FROM equipamentos 
                WHERE tipo = ? AND ativo = 1
                ORDER BY nome
            ''', (tipo,))
        else:
            cursor.execute('''
                SELECT id, nome, descricao, tipo, codigo_patrimonio, status, localizacao, ativo, data_criacao
                FROM equipamentos 
                WHERE ativo = 1
                ORDER BY tipo, nome
            ''')
        
        equipamentos = cursor.fetchall()
        conn.close()
        
        return [dict(equipamento) for equipamento in equipamentos]
    
    def criar_equipamento(self, nome, descricao, tipo, codigo_patrimonio, status='disponivel', localizacao=None):
        """
        Cria um novo equipamento
        Args:
            nome (str): Nome do equipamento
            descricao (str): Descrição do equipamento
            tipo (str): Tipo ('mobilizado' ou 'imobilizado')
            codigo_patrimonio (str): Código do patrimônio
            status (str): Status do equipamento
            localizacao (str): Localização do equipamento
        Returns:
            dict: Resultado da operação
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar se o código do patrimônio já existe
            cursor.execute('SELECT id FROM equipamentos WHERE codigo_patrimonio = ?', (codigo_patrimonio,))
            if cursor.fetchone():
                return {'sucesso': False, 'erro': 'Código do patrimônio já está em uso'}
            
            cursor.execute('''
                INSERT INTO equipamentos (nome, descricao, tipo, codigo_patrimonio, status, localizacao)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, descricao, tipo, codigo_patrimonio, status, localizacao))
            
            conn.commit()
            equipamento_id = cursor.lastrowid
            
            conn.close()
            return {'sucesso': True, 'id': equipamento_id, 'mensagem': 'Equipamento criado com sucesso'}
            
        except sqlite3.Error as e:
            conn.close()
            return {'sucesso': False, 'erro': f'Erro ao criar equipamento: {str(e)}'}
    
    def atualizar_equipamento(self, equipamento_id, nome=None, descricao=None, codigo_patrimonio=None, status=None, localizacao=None):
        """
        Atualiza dados de um equipamento
        Args:
            equipamento_id (int): ID do equipamento
            nome (str, optional): Novo nome
            descricao (str, optional): Nova descrição
            codigo_patrimonio (str, optional): Novo código do patrimônio
            status (str, optional): Novo status
            localizacao (str, optional): Nova localização
        Returns:
            dict: Resultado da operação
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            updates = []
            params = []
            
            if nome:
                updates.append('nome = ?')
                params.append(nome)
            
            if descricao is not None:
                updates.append('descricao = ?')
                params.append(descricao)
            
            if codigo_patrimonio:
                # Verificar se o código já está em uso por outro equipamento
                cursor.execute('SELECT id FROM equipamentos WHERE codigo_patrimonio = ? AND id != ?', (codigo_patrimonio, equipamento_id))
                if cursor.fetchone():
                    return {'sucesso': False, 'erro': 'Código do patrimônio já está em uso'}
                
                updates.append('codigo_patrimonio = ?')
                params.append(codigo_patrimonio)
            
            if status:
                updates.append('status = ?')
                params.append(status)
            
            if localizacao is not None:
                updates.append('localizacao = ?')
                params.append(localizacao)
            
            if updates:
                updates.append('data_atualizacao = ?')
                params.append(datetime.now())
                params.append(equipamento_id)
                
                query = f'UPDATE equipamentos SET {", ".join(updates)} WHERE id = ?'
                cursor.execute(query, params)
                
                if cursor.rowcount == 0:
                    return {'sucesso': False, 'erro': 'Equipamento não encontrado'}
                
                conn.commit()
            
            conn.close()
            return {'sucesso': True, 'mensagem': 'Equipamento atualizado com sucesso'}
            
        except sqlite3.Error as e:
            conn.close()
            return {'sucesso': False, 'erro': f'Erro ao atualizar equipamento: {str(e)}'}
    
    def excluir_equipamento(self, equipamento_id):
        """
        Exclui (inativa) um equipamento
        Args:
            equipamento_id (int): ID do equipamento
        Returns:
            dict: Resultado da operação
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('UPDATE equipamentos SET ativo = 0 WHERE id = ?', (equipamento_id,))
            
            if cursor.rowcount == 0:
                return {'sucesso': False, 'erro': 'Equipamento não encontrado'}
            
            conn.commit()
            conn.close()
            return {'sucesso': True, 'mensagem': 'Equipamento excluído com sucesso'}
            
        except sqlite3.Error as e:
            conn.close()
            return {'sucesso': False, 'erro': f'Erro ao excluir equipamento: {str(e)}'}
    
    # ===== GERENCIAMENTO DE RESERVAS =====
    
    def listar_reservas(self, status=None):
        """
        Lista todas as reservas
        Args:
            status (str, optional): Filtrar por status
        Returns:
            list: Lista de reservas
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''
                SELECT r.id, r.data_inicio, r.data_fim, r.status, r.observacoes, r.data_criacao,
                       u.nome as usuario_nome, u.email as usuario_email,
                       e.nome as equipamento_nome, e.codigo_patrimonio,
                       a.nome as ambiente_nome
                FROM reservas r
                JOIN usuarios u ON r.usuario_id = u.id
                LEFT JOIN equipamentos e ON r.equipamento_id = e.id
                LEFT JOIN ambientes a ON r.ambiente_id = a.id
                WHERE r.status = ?
                ORDER BY r.data_criacao DESC
            ''', (status,))
        else:
            cursor.execute('''
                SELECT r.id, r.data_inicio, r.data_fim, r.status, r.observacoes, r.data_criacao,
                       u.nome as usuario_nome, u.email as usuario_email,
                       e.nome as equipamento_nome, e.codigo_patrimonio,
                       a.nome as ambiente_nome
                FROM reservas r
                JOIN usuarios u ON r.usuario_id = u.id
                LEFT JOIN equipamentos e ON r.equipamento_id = e.id
                LEFT JOIN ambientes a ON r.ambiente_id = a.id
                ORDER BY r.data_criacao DESC
            ''')
        
        reservas = cursor.fetchall()
        conn.close()
        
        return [dict(reserva) for reserva in reservas]
    
    def aprovar_reserva(self, reserva_id, observacoes=None):
        """
        Aprova uma reserva
        Args:
            reserva_id (int): ID da reserva
            observacoes (str, optional): Observações da aprovação
        Returns:
            dict: Resultado da operação
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Atualizar status da reserva
            cursor.execute('''
                UPDATE reservas 
                SET status = 'aprovada', observacoes = ?, data_atualizacao = ?
                WHERE id = ?
            ''', (observacoes, datetime.now(), reserva_id))
            
            if cursor.rowcount == 0:
                return {'sucesso': False, 'erro': 'Reserva não encontrada'}
            
            # Atualizar status do equipamento para reservado
            cursor.execute('''
                UPDATE equipamentos 
                SET status = 'reservado'
                WHERE id = (SELECT equipamento_id FROM reservas WHERE id = ?)
            ''', (reserva_id,))
            
            conn.commit()
            conn.close()
            return {'sucesso': True, 'mensagem': 'Reserva aprovada com sucesso'}
            
        except sqlite3.Error as e:
            conn.close()
            return {'sucesso': False, 'erro': f'Erro ao aprovar reserva: {str(e)}'}
    
    def rejeitar_reserva(self, reserva_id, observacoes=None):
        """
        Rejeita uma reserva
        Args:
            reserva_id (int): ID da reserva
            observacoes (str, optional): Observações da rejeição
        Returns:
            dict: Resultado da operação
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE reservas 
                SET status = 'rejeitada', observacoes = ?, data_atualizacao = ?
                WHERE id = ?
            ''', (observacoes, datetime.now(), reserva_id))
            
            if cursor.rowcount == 0:
                return {'sucesso': False, 'erro': 'Reserva não encontrada'}
            
            conn.commit()
            conn.close()
            return {'sucesso': True, 'mensagem': 'Reserva rejeitada com sucesso'}
            
        except sqlite3.Error as e:
            conn.close()
            return {'sucesso': False, 'erro': f'Erro ao rejeitar reserva: {str(e)}'}
