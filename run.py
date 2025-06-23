# Sistema de Gestão Sicredi - Arquivo principal
# Este arquivo integra todas as funcionalidades do sistema

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
# Importar módulos do projeto

from app.utils.auth import login_user, logout_user, login_required, gestor_required, analista_required, get_current_user
from app.main.gestao_equipamentos.gestor import GestorService
from app.main.gestao_equipamentos.analista import AnalistaService
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

# Configurar pasta de templates
app.template_folder = 'templates'

# Inicializar banco de dados ao iniciar a aplicação
with app.app_context():
    init_db()  # Isso criará as tabelas e os usuários padrão se não existirem

# Instanciar serviços
gestor_service = GestorService()
analista_service = AnalistaService()

# ===== ROTAS PRINCIPAIS =====

@app.route('/')
def index():
    """
    Rota principal - redireciona para login se não autenticado
    ou para a página de gestão se autenticado
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
    
    # Se for GET, redireciona para a página inicial
    if request.method == 'GET':
        print('Método GET detectado. Redirecionando para a página inicial...')
        return redirect(url_for('index'))
        
    # Se for POST, processa o login
    email = request.form.get('usuario', '').strip()
    senha = request.form.get('senha', '')
    
    print('\n=== TENTATIVA DE LOGIN ===')
    print(f'Email fornecido: {email}')
    print(f'Senha fornecida: {senha}')
    
    if not email or not senha:
        print('Erro: Campos vazios')
        flash('Por favor, preencha todos os campos.', 'error')
        return redirect(url_for('index'))
    
    db = get_db()
    print('Buscando usuário no banco de dados...')
    usuario = db.execute('''
        SELECT id_usuario AS id,
               nome,
               email,
               senha,
               cargo AS tipo
        FROM usuarios
        WHERE email = ?
    ''', (email,)).fetchone()
    
    if usuario:
        print(f'Usuário encontrado: ID={usuario["id"]}, Nome={usuario["nome"]}, Email={usuario["email"]}, Tipo={usuario["tipo"]}')
        print(f'Hash da senha no banco: {usuario["senha"]}')
        
        # Verifica a senha
        # Verifica a senha usando utilitário unificado
        senha_correta = check_password(usuario['senha'], senha)
        print(f'A senha está correta? {senha_correta}')
        
        if senha_correta:
            # Configura a sessão
            session['user_id'] = usuario['id']
            session['user_name'] = usuario['nome']
            session['user_email'] = usuario['email']
            session['user_type'] = usuario['tipo']
            session.modified = True  # Garante que a sessão seja salva
            
            print('\n=== SESSÃO CONFIGURADA ===')
            print(f'Sessão após login: {dict(session)}')
            print(f'user_id: {session["user_id"]}')
            print(f'user_name: {session["user_name"]}')
            print(f'user_type: {session["user_type"]}')
            
            print('\nLogin bem-sucedido! Redirecionando para a página de gestão...')
            flash(f'Bem-vindo(a) de volta, {usuario["nome"]}!', 'success')
            
            # Redireciona para a rota de gestão
            response = redirect(url_for('gestao'))
            print(f'Headers da resposta: {response.headers}')
            return response
    
    print('\nFalha no login - Credenciais inválidas')
    flash('E-mail ou senha incorretos. Tente novamente.', 'error')
    return redirect(url_for('index'))
        
       

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

@app.route('/dashboard/gestor')
@login_required
def dashboard_gestor():
    """
    Dashboard principal do gestor
    """
    user = get_current_user()
    
    # Buscar estatísticas para o dashboard
    reservas_pendentes = len(gestor_service.listar_reservas('pendente'))
    total_analistas = len(gestor_service.listar_analistas())
    total_equipamentos = len(gestor_service.listar_equipamentos())
    total_ambientes = len(gestor_service.listar_ambientes())
    
    return render_template('Gestor/dashboard.html', 
                         user=user,
                         reservas_pendentes=reservas_pendentes,
                         total_analistas=total_analistas,
                         total_equipamentos=total_equipamentos,
                         total_ambientes=total_ambientes)

@app.route('/dashboard/analista')
@analista_required
def dashboard_analista():
    """
    Dashboard principal do analista
    """
    user = get_current_user()
    
    # Buscar estatísticas do analista
    minhas_reservas = analista_service.listar_minhas_reservas(user['id'])
    reservas_pendentes = len([r for r in minhas_reservas if r['status'] == 'pendente'])
    reservas_aprovadas = len([r for r in minhas_reservas if r['status'] == 'aprovada'])
    
    return render_template('Analista/dashboard.html',
                         user=user,
                         total_reservas=len(minhas_reservas),
                         reservas_pendentes=reservas_pendentes,
                         reservas_aprovadas=reservas_aprovadas)

# ===== ROTAS DO GESTOR =====

@app.route('/gestor/analistas')
@gestor_required
def gestor_analistas():
    """
    Página de gerenciamento de analistas pelo gestor
    """
    analistas = gestor_service.listar_analistas()
    user = get_current_user()
    return render_template('Gestor/GerenciarAnalistas/analistas.html', 
                         analistas=analistas, user=user)

@app.route('/gestor/analistas/criar', methods=['POST'])
@gestor_required
def criar_analista():
    """
    Criar um novo analista
    """
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    if not all([nome, email, senha]):
        flash('Todos os campos são obrigatórios.', 'error')
        return redirect(url_for('gestor_analistas'))
    
    resultado = gestor_service.criar_analista(nome, email, senha)
    
    if resultado['sucesso']:
        flash(resultado['mensagem'], 'success')
    else:
        flash(resultado['erro'], 'error')
    
    return redirect(url_for('gestor_analistas'))

@app.route('/gestor/analistas/atualizar/<int:analista_id>', methods=['POST'])
@gestor_required
def atualizar_analista(analista_id):
    """
    Atualizar dados de um analista
    """
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    ativo = request.form.get('ativo') == 'true'
    
    # Criar dicionário apenas com campos preenchidos
    dados = {}
    if nome: dados['nome'] = nome
    if email: dados['email'] = email
    if senha: dados['senha'] = senha
    dados['ativo'] = ativo
    
    resultado = gestor_service.atualizar_analista(analista_id, **dados)
    
    if resultado['sucesso']:
        flash(resultado['mensagem'], 'success')
    else:
        flash(resultado['erro'], 'error')
    
    return redirect(url_for('gestor_analistas'))

@app.route('/gestor/ambientes')
@gestor_required
def gestor_ambientes():
    """
    Página de gerenciamento de ambientes pelo gestor
    """
    ambientes = gestor_service.listar_ambientes()
    user = get_current_user()
    return render_template('Gestor/GerenciarAmbientes/ambiente.html', 
                         ambientes=ambientes, user=user)

@app.route('/gestor/ambientes/criar', methods=['POST'])
@gestor_required
def criar_ambiente():
    """
    Criar um novo ambiente
    """
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    capacidade = request.form.get('capacidade')
    equipamentos = request.form.get('equipamentos')
    
    if not nome:
        flash('Nome do ambiente é obrigatório.', 'error')
        return redirect(url_for('gestor_ambientes'))
    
    capacidade = int(capacidade) if capacidade else None
    
    resultado = gestor_service.criar_ambiente(nome, descricao, capacidade, equipamentos)
    
    if resultado['sucesso']:
        flash(resultado['mensagem'], 'success')
    else:
        flash(resultado['erro'], 'error')
    
    return redirect(url_for('gestor_ambientes'))

@app.route('/gestor/equipamentos/mobilizados')
@gestor_required
def gestor_equipamentos_mobilizados():
    """
    Página de gerenciamento de equipamentos mobilizados
    """
    equipamentos = gestor_service.listar_equipamentos('mobilizado')
    user = get_current_user()
    return render_template('Gestor/EquipamentosMobilizados/mobilizados.html', 
                         equipamentos=equipamentos, user=user)

@app.route('/gestor/equipamentos/imobilizados')
@gestor_required
def gestor_equipamentos_imobilizados():
    """
    Página de gerenciamento de equipamentos imobilizados
    """
    equipamentos = gestor_service.listar_equipamentos('imobilizado')
    user = get_current_user()
    return render_template('Gestor/EquipamentosImobilizados/imobilizados.html', 
                         equipamentos=equipamentos, user=user)

@app.route('/gestor/equipamentos/criar', methods=['POST'])
@gestor_required
def criar_equipamento():
    """
    Criar um novo equipamento
    """
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    tipo = request.form.get('tipo')
    codigo_patrimonio = request.form.get('codigo_patrimonio')
    status = request.form.get('status', 'disponivel')
    localizacao = request.form.get('localizacao')
    
    if not all([nome, tipo, codigo_patrimonio]):
        flash('Nome, tipo e código do patrimônio são obrigatórios.', 'error')
        return redirect(request.referrer)
    
    resultado = gestor_service.criar_equipamento(nome, descricao, tipo, codigo_patrimonio, status, localizacao)
    
    if resultado['sucesso']:
        flash(resultado['mensagem'], 'success')
    else:
        flash(resultado['erro'], 'error')
    
    return redirect(request.referrer)

@app.route('/gestor/reservas')
@gestor_required
def gestor_reservas():
    """
    Página de gerenciamento de reservas pelo gestor
    """
    status_filtro = request.args.get('status')
    reservas = gestor_service.listar_reservas(status_filtro)
    user = get_current_user()
    return render_template('Gestor/GerenciarReservas/reservas.html', 
                         reservas=reservas, user=user, status_filtro=status_filtro)

@app.route('/gestor/reservas/aprovar/<int:reserva_id>', methods=['POST'])
@gestor_required
def aprovar_reserva(reserva_id):
    """
    Aprovar uma reserva
    """
    observacoes = request.form.get('observacoes')
    resultado = gestor_service.aprovar_reserva(reserva_id, observacoes)
    
    if resultado['sucesso']:
        flash(resultado['mensagem'], 'success')
    else:
        flash(resultado['erro'], 'error')
    
    return redirect(url_for('gestor_reservas'))

@app.route('/gestor/reservas/rejeitar/<int:reserva_id>', methods=['POST'])
@gestor_required
def rejeitar_reserva(reserva_id):
    """
    Rejeitar uma reserva
    """
    observacoes = request.form.get('observacoes')
    resultado = gestor_service.rejeitar_reserva(reserva_id, observacoes)
    
    if resultado['sucesso']:
        flash(resultado['mensagem'], 'success')
    else:
        flash(resultado['erro'], 'error')
    
    return redirect(url_for('gestor_reservas'))

# ===== ROTAS DO ANALISTA =====

@app.route('/analista/equipamentos')
@analista_required
def analista_equipamentos():
    """
    Página de reserva de equipamentos pelo analista
    """
    tipo_filtro = request.args.get('tipo')
    equipamentos = analista_service.listar_equipamentos_disponiveis(tipo_filtro)
    user = get_current_user()
    minhas_reservas = analista_service.listar_minhas_reservas(user['id'])
    
    return render_template('Analista/ReservaEquipamento/equipamento.html', 
                         equipamentos=equipamentos, 
                         user=user, 
                         minhas_reservas=minhas_reservas,
                         tipo_filtro=tipo_filtro)

@app.route('/analista/equipamentos/reservar', methods=['POST'])
@analista_required
def reservar_equipamento():
    """
    Criar uma reserva de equipamento
    """
    user = get_current_user()
    
    equipamento_id = request.form.get('equipamento_id')
    data_inicio = request.form.get('data_inicio')
    data_fim = request.form.get('data_fim')
    observacoes = request.form.get('observacoes')
    
    if not all([equipamento_id, data_inicio, data_fim]):
        flash('Equipamento, data de início e fim são obrigatórios.', 'error')
        return redirect(url_for('analista_equipamentos'))
    
    resultado = analista_service.criar_reserva_equipamento(
        user['id'], int(equipamento_id), data_inicio, data_fim, observacoes
    )
    
    if resultado['sucesso']:
        flash(resultado['mensagem'], 'success')
    else:
        flash(resultado['erro'], 'error')
    
    return redirect(url_for('analista_equipamentos'))

@app.route('/analista/ambientes')
@analista_required
def analista_ambientes():
    """
    Página de acesso a ambientes pelo analista
    """
    ambientes = analista_service.listar_ambientes_disponiveis()
    user = get_current_user()
    minhas_reservas = analista_service.listar_minhas_reservas(user['id'])
    
    return render_template('Analista/AcessoAmbientes/ambiente.html', 
                         ambientes=ambientes, 
                         user=user,
                         minhas_reservas=minhas_reservas)

@app.route('/analista/ambientes/reservar', methods=['POST'])
@analista_required
def reservar_ambiente():
    """
    Criar uma reserva de ambiente
    """
    user = get_current_user()
    
    ambiente_id = request.form.get('ambiente_id')
    data_inicio = request.form.get('data_inicio')
    data_fim = request.form.get('data_fim')
    observacoes = request.form.get('observacoes')
    
    if not all([ambiente_id, data_inicio, data_fim]):
        flash('Ambiente, data de início e fim são obrigatórios.', 'error')
        return redirect(url_for('analista_ambientes'))
    
    resultado = analista_service.criar_reserva_ambiente(
        user['id'], int(ambiente_id), data_inicio, data_fim, observacoes
    )
    
    if resultado['sucesso']:
        flash(resultado['mensagem'], 'success')
    else:
        flash(resultado['erro'], 'error')
    
    return redirect(url_for('analista_ambientes'))

@app.route('/analista/reservas/cancelar/<int:reserva_id>', methods=['POST'])
@analista_required
def cancelar_reserva():
    """
    Cancelar uma reserva do analista
    """
    user = get_current_user()
    reserva_id = request.form.get('reserva_id')
    
    resultado = analista_service.cancelar_reserva(int(reserva_id), user['id'])
    
    if resultado['sucesso']:
        flash(resultado['mensagem'], 'success')
    else:
        flash(resultado['erro'], 'error')
    
    return redirect(request.referrer)

# ===== ROTAS API (JSON) =====

@app.route('/api/verificar-disponibilidade-ambiente')
@analista_required
def api_verificar_disponibilidade_ambiente():
    """
    API para verificar disponibilidade de ambiente
    """
    ambiente_id = request.args.get('ambiente_id')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    if not all([ambiente_id, data_inicio, data_fim]):
        return jsonify({'erro': 'Parâmetros obrigatórios não fornecidos'}), 400
    
    resultado = analista_service.verificar_disponibilidade_ambiente(
        int(ambiente_id), data_inicio, data_fim
    )
    
    return jsonify(resultado)

# ===== MANIPULADORES DE ERRO =====

@app.errorhandler(404)
def page_not_found(e):
    """
    Manipulador de erro 404 - Página não encontrada
    """
    return render_template('error.html', 
                         error_code=404, 
                         error_message='Página não encontrada'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """
    Manipulador de erro 500 - Erro interno do servidor
    """
    return render_template('error.html', 
                         error_code=500, 
                         error_message='Erro interno do servidor'), 500

# ===== CONTEXTO DE TEMPLATE =====

@app.context_processor
def inject_user():
    """
    Injeta dados do usuário atual em todos os templates
    """
    return {'current_user': get_current_user()}

# ===== EXECUÇÃO DA APLICAÇÃO =====

if __name__ == '__main__':
    # Configurações para desenvolvimento
    app.run(debug=True, host='0.0.0.0', port=5000)

