"""
Módulo principal para gerenciamento de ambientes (gestor).
CRUD de ambientes, seguindo o padrão das outras áreas do projeto.
"""
from flask import Blueprint, render_template, request, jsonify
from app.db.db_connection import get_db_connection as get_db_connection
from .salas import bp_gestor_salas

bp_gestor_ambientes = Blueprint('gestor_ambientes', __name__, url_prefix='/gestao_ambientes/gestor')

# CRUD real de ambientes usando SQLite

def init_app(app):
    app.register_blueprint(bp_gestor_ambientes)
    app.register_blueprint(bp_gestor_salas)


@bp_gestor_ambientes.route('/api/analistas', methods=['GET'])
def listar_analistas_para_ambiente():
    db = get_db_connection()
    analistas = db.execute(
        "SELECT id_usuario, nome, email FROM usuarios WHERE cargo = 'A' ORDER BY nome"
    ).fetchall()
    db.close()
    return jsonify([dict(a) for a in analistas])

@bp_gestor_ambientes.route('/api/setores', methods=['GET'])
def listar_setores():
    """Retorna todos os setores para seleção de ambiente."""
    try:
        db = get_db_connection()
        setores = db.execute('SELECT id_setor, nome_setor FROM setores ORDER BY nome_setor').fetchall()
        db.close()
        return jsonify([dict(s) for s in setores])
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar setores: {str(e)}"}), 500


@bp_gestor_ambientes.route('/')
def pagina_ambientes():
    """Renderiza a página de ambientes para o gestor."""
    db = get_db_connection()
    ambientes = db.execute(
        'SELECT id, nome, localizacao FROM ambientes ORDER BY nome'
    ).fetchall()
    db.close()
    return render_template('gestao_ambientes/gestor/GerenciarAmbientes/ambiente.html', ambientes=ambientes)

@bp_gestor_ambientes.route('/api/ambientes', methods=['GET'])
def listar_ambientes():
    """Retorna a lista de ambientes (JSON)."""
    try:
        db = get_db_connection()
        ambientes = db.execute(
            'SELECT id, nome, localizacao FROM ambientes ORDER BY nome'
        ).fetchall()
        db.close()
        return jsonify([dict(a) for a in ambientes])
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar ambientes: {str(e)}"}), 500

@bp_gestor_ambientes.route('/api/ambientes', methods=['POST'])
def criar_ambiente():
    """Cria um novo ambiente."""
    data = request.json
    nome = data.get("nome", "").strip()
    id_setor = data.get("id_setor")
    localizacao = data.get("localizacao", "")
    if not nome:
        return jsonify({"erro": "Nome do ambiente é obrigatório."}), 400
    if not id_setor:
        return jsonify({"erro": "Setor responsável é obrigatório."}), 400
    try:
        db = get_db_connection()
        cursor = db.execute(
            'INSERT INTO ambientes (nome, localizacao, id_setor) VALUES (?, ?, ?)',
            (nome, localizacao, id_setor)
        )
        db.commit()
        novo_id = cursor.lastrowid
        novo = db.execute('''SELECT a.id, a.nome, a.localizacao, a.id_setor, s.nome_setor FROM ambientes a LEFT JOIN setores s ON a.id_setor = s.id_setor WHERE a.id = ?''', (novo_id,)).fetchone()
        db.close()
        return jsonify(dict(novo)), 201
    except Exception as e:
        return jsonify({"erro": f"Erro ao criar ambiente: {str(e)}"}), 500


@bp_gestor_ambientes.route('/api/ambientes/<int:id>', methods=['PUT'])
def atualizar_ambiente(id):
    """Atualiza um ambiente existente."""
    data = request.json
    db = get_db_connection()
    db.execute(
        'UPDATE ambientes SET nome = ?, localizacao = ? WHERE id = ?',
        (data.get("nome"), data.get("localizacao"), id)
    )
    db.commit()
    ambiente = db.execute('SELECT id, nome, localizacao FROM ambientes WHERE id = ?', (id,)).fetchone()
    db.close()
    if ambiente:
        return jsonify(dict(ambiente))
    else:
        return jsonify({"erro": "Ambiente não encontrado"}), 404

@bp_gestor_ambientes.route('/api/ambientes/<int:id>', methods=['DELETE'])
def deletar_ambiente(id):
    """Remove um ambiente."""
    db = get_db_connection()
    db.execute('DELETE FROM ambientes WHERE id = ?', (id,))
    db.commit()
    db.close()
    return '', 204
