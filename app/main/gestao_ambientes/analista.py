from flask import Blueprint, session, jsonify, request, render_template
from app.db.db_connection import get_db_connection

bp_analista_ambientes = Blueprint('analista_ambientes', __name__, url_prefix='/gestao_ambientes/analista')

# Utilitário para pegar usuário logado

def get_usuario_logado():
    print('[DEBUG] Conteúdo da sessão ao acessar get_usuario_logado:', dict(session))
    # Supondo que o id do usuário e setor estejam na sessão
    return {
        'id_usuario': session.get('user_id'),
        'id_setor': session.get('id_setor'),
        'nome': session.get('user_name'),
        'tipo': session.get('user_type')
    }

@bp_analista_ambientes.route('/api/me')
def api_me():
    user = get_usuario_logado()
    if not user['id_usuario']:
        return jsonify({'erro': 'Não autenticado'}), 401
    return jsonify(user)

@bp_analista_ambientes.route('/api/ambientes')
def api_ambientes():
    db = get_db_connection()
    ambientes = db.execute('''
        SELECT a.id, a.nome, a.localizacao, a.id_setor, s.nome_setor
        FROM ambientes a
        LEFT JOIN setores s ON a.id_setor = s.id_setor
        ORDER BY a.nome
    ''').fetchall()
    db.close()
    return jsonify([dict(a) for a in ambientes])

@bp_analista_ambientes.route('/api/ambiente_atual')
def api_ambiente_atual():
    user = get_usuario_logado()
    if not user['id_usuario']:
        return jsonify(None)
    db = get_db_connection()
    ambiente = db.execute('''
        SELECT a.id, a.nome, a.localizacao, a.id_setor, s.nome_setor
        FROM ambientes a
        LEFT JOIN setores s ON a.id_setor = s.id_setor
        INNER JOIN analista_ambiente aa ON aa.id_ambiente = a.id
        WHERE aa.id_analista = ? AND aa.ativo = 1
    ''', (user['id_usuario'],)).fetchone()
    db.close()
    return jsonify(dict(ambiente) if ambiente else None)

@bp_analista_ambientes.route('/api/entrar', methods=['POST'])
def api_entrar_ambiente():
    user = get_usuario_logado()
    if not user['id_usuario']:
        return jsonify({'erro': 'Não autenticado'}), 401
    id_ambiente = request.json.get('id_ambiente')
    db = get_db_connection()
    ambiente = db.execute('SELECT id_setor FROM ambientes WHERE id = ?', (id_ambiente,)).fetchone()
    print(f"[DEBUG] user['id_setor']: {user['id_setor']} (type: {type(user['id_setor'])})")
    print(f"[DEBUG] ambiente['id_setor']: {ambiente['id_setor']} (type: {type(ambiente['id_setor'])})")
    try:
        user_setor = int(user['id_setor']) if user['id_setor'] is not None else None
        ambiente_setor = int(ambiente['id_setor']) if ambiente and ambiente['id_setor'] is not None else None
    except Exception as e:
        print(f'[ERROR] Falha ao converter id_setor para inteiro: {e}')
        db.close()
        return jsonify({'erro': 'Erro interno ao validar setor. Contate o administrador.'}), 500
    if ambiente_setor is None or user_setor is None:
        print('[ERROR] id_setor do usuário ou ambiente está None!')
        db.close()
        return jsonify({'erro': 'Setor do usuário ou ambiente não definido.'}), 403
    if ambiente_setor != user_setor:
        print(f'[ERROR] Setores diferentes: user_setor={user_setor}, ambiente_setor={ambiente_setor}')
        db.close()
        return jsonify({'erro': 'Você não pertence ao setor deste ambiente.'}), 403
    # Verifica se já está em algum ambiente
    ativo = db.execute('SELECT 1 FROM analista_ambiente WHERE id_analista = ? AND ativo = 1', (user['id_usuario'],)).fetchone()
    if ativo:
        db.close()
        return jsonify({'erro': 'Você já está em um ambiente.'}), 400
    # Marca como ativo
    db.execute('INSERT INTO analista_ambiente (id_analista, id_ambiente, ativo) VALUES (?, ?, 1)', (user['id_usuario'], id_ambiente))
    db.commit()
    db.close()
    return jsonify({'ok': True})

@bp_analista_ambientes.route('/api/sair', methods=['POST'])
def api_sair_ambiente():
    user = get_usuario_logado()
    if not user['id_usuario']:
        return jsonify({'erro': 'Não autenticado'}), 401
    db = get_db_connection()
    db.execute('UPDATE analista_ambiente SET ativo = 0 WHERE id_analista = ? AND ativo = 1', (user['id_usuario'],))
    db.commit()
    db.close()
    return jsonify({'ok': True})

@bp_analista_ambientes.route('/')
def pagina_ambientes():
    return render_template('gestao_ambientes/analista/ambiente.html')
