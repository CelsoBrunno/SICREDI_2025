# Sistema de Gestão Sicredi - Arquivo principal
# Este arquivo integra todas as funcionalidades do sistema

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
# Importar módulos do projeto

from app.utils.auth import login_user, logout_user, login_required, gestor_required, analista_required, get_current_user

from app.db.database import init_db, hash_password, check_password
from app.db.db_connection import get_db_connection
# Inicializar aplicação Flask
app = Flask(__name__)
# Chave secreta mais segura para produção
app.secret_key = 'dev'  # Em produção, use uma chave forte e segura
# Configuração adicional para sessões
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hora
app.config['SESSION_COOKIE_SECURE'] = False  # True em produção com HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Função para conectar ao banco de dados
def get_db():
    return get_db_connection()

# Configurar pastas de templates e arquivos estáticos
# Define caminho absoluto para o diretório raiz do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))

# Pasta de templates (HTML)
app.template_folder = os.path.join(BASE_DIR, 'templates')
print(f"Pasta de templates definida para: {app.template_folder}")

# Pasta de arquivos estáticos (CSS, JS, imagens)
app.static_folder = os.path.join(BASE_DIR, 'static')
app.static_url_path = '/static'  # URL base para servir arquivos estáticos
print(f"Pasta de estáticos definida para: {app.static_folder} (url: {app.static_url_path})")

# Inicializar banco de dados ao iniciar a aplicação
with app.app_context():
    init_db()  # Isso criará as tabelas e os usuários padrão se não existirem

# Instanciadores removidos: GestorService e AnalistaService não existem mais.

# ===== ROTAS PRINCIPAIS =====

@app.route('/')
def index():
    """
    Rota principal corrigida: exibe SEMPRE a tela de login se o usuário não estiver autenticado.
    Se autenticado, redireciona para a dashboard de gestão.
    """
    print('\n=== ACESSANDO ROTA RAIZ ===')
    print(f'Sessão atual: {dict(session)}')
    if 'user_id' in session:
        print(f'Usuário autenticado. Redirecionando para a página de gestão...')
        return redirect(url_for('gestao'))
    print('Usuário não autenticado. Exibindo página de login...')
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print('\n=== INÍCIO DA ROTA DE LOGIN ===')
    print(f'Método da requisição: {request.method}')
    print(f'Dados do formulário: {request.form}')
    
    # Corrigido: GET sempre exibe a tela de login
    if request.method == 'GET':
        print('Método GET detectado. Exibindo tela de login.')
        return render_template('login.html')
    
    # Se for POST, processa o login normalmente
    email = request.form.get('usuario', '').strip()
    senha = request.form.get('senha', '')
    
    print('\n=== TENTATIVA DE LOGIN ===')
    print(f'Email fornecido: {email}')
    print(f'Senha fornecida: {senha}')
    
    if not email or not senha:
        print('Erro: Campos vazios')
        flash('Por favor, preencha todos os campos.', 'error')
        return render_template('login.html')
    
    db = get_db()
    print('Buscando usuário no banco de dados...')
    usuario = db.execute('SELECT id_usuario, nome, email, senha, cargo, id_setor FROM usuarios WHERE email = ?', (email,)).fetchone()
    
    if usuario:
        print(f'Usuário encontrado: ID={usuario["id_usuario"]}, Nome={usuario["nome"]}, Email={usuario["email"]}, Tipo={usuario["cargo"]}')
        print(f'Hash da senha no banco: {usuario["senha"]}')
        
        senha_correta = check_password(usuario['senha'], senha)
        print(f'A senha está correta? {senha_correta}')
        
        if senha_correta:
            print(f'Chaves disponíveis no usuário retornado: {list(usuario.keys())}')
            # Configura a sessão
            session['user_id'] = usuario['id_usuario']
            session['user_name'] = usuario['nome']
            session['user_email'] = usuario['email']
            session['user_type'] = usuario['cargo']
            # Só exige id_setor para analista
            tipo_usuario = session['user_type']
            if tipo_usuario == 'A':
                if 'id_setor' not in usuario.keys() or usuario['id_setor'] is None:
                    print('ERRO: Analista sem setor associado!')
                    flash('Erro interno: analista sem setor associado. Contate o administrador.', 'danger')
                    return redirect(url_for('index'))
                session['id_setor'] = usuario['id_setor']
            else:
                session['id_setor'] = None
            session.modified = True
            print('Sessão após login:', dict(session))
            print(f'Sessão após login: {dict(session)}')
            print(f'user_id: {session["user_id"]}')
            print(f'user_name: {session["user_name"]}')
            print(f'user_type: {session["user_type"]}')
            print(f'id_setor: {session["id_setor"]}')
            print('\nLogin bem-sucedido! Redirecionando para a página de gestão...')
            flash(f'Bem-vindo(a) de volta, {usuario["nome"]}!', 'success')
            return redirect(url_for('gestao'))
    print('\nFalha no login - Credenciais inválidas')
    flash('E-mail ou senha incorretos. Tente novamente.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Rota de logout - finaliza sessão do usuário
    """
    # Limpa a sessão
    session.clear()
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('index'))

# ===== DASHBOARD =====

@app.route('/gestao')
def gestao():
    print('\n=== ACESSANDO ROTA /GESTAO ===')
    print(f'Sessão atual: {dict(session)}')
    
    # Verifica se o usuário está autenticado
    if 'user_id' not in session:
        print('Usuário não autenticado. Redirecionando para a página inicial...')
        return redirect(url_for('index'))
    
    # Obtém os dados do usuário da sessão
    user = {
        'id': session.get('user_id'),
        'nome': session.get('user_name'),
        'email': session.get('user_email'),
        'tipo': session.get('user_type')
    }
    
    print(f'Dados do usuário: {user}')
    print('Renderizando template principal/gestao.html...')
    
    return render_template('principal/gestao.html', user=user)


