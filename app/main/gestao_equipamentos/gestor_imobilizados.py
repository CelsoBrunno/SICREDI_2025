from app.db.db_connection import get_db_connection as get_db
from flask import Blueprint, request, jsonify

bp_gestor_imobilizados = Blueprint('bp_gestor_imobilizados', __name__, url_prefix='/gestao_equipamentos/gestor')

# --- API REST para Imobilizados ---
@bp_gestor_imobilizados.route('/api/imobilizados', methods=['GET'])
def api_listar_imobilizados():
    db = get_db()
    imobilizados = db.execute('SELECT * FROM imobilizados ORDER BY nome').fetchall()
    return jsonify([dict(row) for row in imobilizados])

@bp_gestor_imobilizados.route('/api/imobilizados', methods=['POST'])
def api_adicionar_imobilizado():
    data = request.json
    db = get_db()
    try:
        cursor = db.execute(
            'INSERT INTO imobilizados (nome, modelo, codigo, marca, numero_serie, localizacao, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (
                data['nome'],
                data.get('modelo', ''),
                data.get('codigo', ''),
                data.get('marca', ''),
                data.get('serie', ''),
                data.get('local', ''),
                'A' # status inicial: ANALISE
            )
        )
        db.commit()
        novo_id = cursor.lastrowid
        imobilizado = db.execute('SELECT * FROM imobilizados WHERE id_imobilizado = ?', (novo_id,)).fetchone()
        return jsonify(dict(imobilizado)), 201
    except Exception as e:
        import sqlite3
        if isinstance(e, sqlite3.IntegrityError):
            return jsonify({'success': False, 'error': 'Número de série já cadastrado.'}), 400
        return jsonify({'success': False, 'error': str(e)}), 500

@bp_gestor_imobilizados.route('/api/imobilizados/<int:id_imobilizado>', methods=['PUT'])
def api_editar_imobilizado(id_imobilizado):
    data = request.json
    db = get_db()
    db.execute(
        'UPDATE imobilizados SET nome=?, modelo=?, codigo=?, marca=?, numero_serie=?, localizacao=?, status=? WHERE id_imobilizado=?',
        (
            data['nome'],
            data.get('modelo', ''),
            data.get('codigo', ''),
            data.get('marca', ''),
            data.get('serie', ''),
            data.get('local', ''),
            data.get('status', 'A'),
            id_imobilizado
        )
    )
    db.commit()
    imobilizado = db.execute('SELECT * FROM imobilizados WHERE id_imobilizado = ?', (id_imobilizado,)).fetchone()
    return jsonify(dict(imobilizado))

@bp_gestor_imobilizados.route('/api/imobilizados/<int:id_imobilizado>', methods=['DELETE'])
def api_deletar_imobilizado(id_imobilizado):
    db = get_db()
    try:
        db.execute('DELETE FROM imobilizados WHERE id_imobilizado = ?', (id_imobilizado,))
        db.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
