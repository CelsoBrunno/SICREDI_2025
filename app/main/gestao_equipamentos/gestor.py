# caminho do arquivo app/main/gestao_equipamentos/gestor.py

from app.db.db_connection import get_db_connection as get_db

from flask import Blueprint, render_template, request, jsonify

bp_gestor_equipamentos = Blueprint('bp_gestor_equipamentos', __name__, url_prefix='/gestao_equipamentos/gestor')

# Rotas REST para gestor de equipamentos mobilizados
@bp_gestor_equipamentos.route('/')
def pagina_mobilizados():
    equipamentos = listar_todos_mobilizados()
    return render_template('gestao_equipamentos/gestor/equipamentos_mobilizados/mobilizados.html', equipamentos=equipamentos)

# Rota para página de imobilizados (Materiais)
@bp_gestor_equipamentos.route('/imobilizados')
def pagina_imobilizados():
    # Aqui pode-se buscar os dados necessários para a página de imobilizados
    return render_template('gestao_equipamentos/gestor/equipamentos_imobilizados/imobilizados.html')

@bp_gestor_equipamentos.route('/api/mobilizados', methods=['GET'])
def api_listar_mobilizados():
    equipamentos = listar_todos_mobilizados()
    return jsonify([dict(e) for e in equipamentos])

# NOVAS ROTAS PARA RESERVAS DE MOBILIZADOS
@bp_gestor_equipamentos.route('/api/reservas', methods=['GET'])
def api_listar_reservas_mobilizados():
    reservas = listar_todas_reservas_mobilizados()
    return jsonify([dict(r) for r in reservas])

@bp_gestor_equipamentos.route('/api/reservas/<int:id>', methods=['PUT'])
def api_aprovar_recusar_reserva(id):
    data = request.json
    novo_status = data.get('status')
    if novo_status not in ['aprovada', 'recusada']:
        return jsonify({'error': 'Status inválido'}), 400
    atualizar_status_reserva(id, novo_status)
    return jsonify({'success': True, 'id': id, 'novo_status': novo_status})

@bp_gestor_equipamentos.route('/api/mobilizados', methods=['POST'])
def api_adicionar_mobilizado():
    data = request.json
    novo_id = adicionar_mobilizado(data['nome'], data['categoria'])
    equipamento = buscar_mobilizado_por_id(novo_id)
    return jsonify(dict(equipamento)), 201

@bp_gestor_equipamentos.route('/api/mobilizados/<int:id>', methods=['PUT'])
def api_atualizar_mobilizado(id):
    data = request.json
    atualizar_mobilizado(id, data['nome'], data['categoria'])
    equipamento = buscar_mobilizado_por_id(id)
    return jsonify(dict(equipamento))

@bp_gestor_equipamentos.route('/api/mobilizados/<int:id>', methods=['DELETE'])
def api_deletar_mobilizado(id):
    try:
        deletar_mobilizado(id)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# --- Funções para Equipamentos Mobilizados ---

def listar_todas_reservas_mobilizados():
    """Busca todas as reservas de equipamentos mobilizados, incluindo dados do equipamento e analista."""
    db = get_db()
    reservas = db.execute('''
        SELECT r.id, r.equipamento_id, r.analista_nome, r.data_inicio_reserva, r.data_fim_reserva, r.status, e.nome as equipamento_nome
        FROM reservas_mobilizados r
        JOIN equipamentos_mobilizados e ON r.equipamento_id = e.id
        ORDER BY r.data_inicio_reserva DESC
    ''').fetchall()
    return reservas

def atualizar_status_reserva(reserva_id, novo_status):
    """Atualiza o status de uma reserva (aprovada/recusada)."""
    db = get_db()
    db.execute('UPDATE reservas_mobilizados SET status = ? WHERE id = ?', (novo_status, reserva_id))
    db.commit()
    return True

def listar_todos_mobilizados():
    """Busca todos os equipamentos mobilizados no banco de dados."""
    db = get_db()
    equipamentos = db.execute(
        'SELECT id, nome, categoria, status, data_cadastro FROM equipamentos_mobilizados ORDER BY nome'
    ).fetchall()
    return equipamentos

def buscar_mobilizado_por_id(id):
    """Busca um único equipamento mobilizado pelo seu ID."""
    db = get_db()
    equipamento = db.execute(
        'SELECT id, nome, categoria, status FROM equipamentos_mobilizados WHERE id = ?', (id,)
    ).fetchone()
    return equipamento

def adicionar_mobilizado(nome, categoria):
    """Adiciona um novo equipamento mobilizado ao banco de dados."""
    db = get_db()
    cursor = db.execute(
        'INSERT INTO equipamentos_mobilizados (nome, categoria) VALUES (?, ?)',
        (nome, categoria)
    )
    db.commit()
    # Retorna o ID do novo equipamento inserido
    return cursor.lastrowid

def atualizar_mobilizado(id, nome, categoria):
    """Atualiza os dados de um equipamento mobilizado existente."""
    db = get_db()
    db.execute(
        'UPDATE equipamentos_mobilizados SET nome = ?, categoria = ? WHERE id = ?',
        (nome, categoria, id)
    )
    db.commit()
    return True

def deletar_mobilizado(id):
    """Deleta um equipamento mobilizado do banco de dados."""
    db = get_db()
    db.execute('DELETE FROM equipamentos_mobilizados WHERE id = ?', (id,))
    db.commit()
    return True
