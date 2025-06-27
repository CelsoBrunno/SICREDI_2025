from flask import Blueprint, request, jsonify
from app.db.db_connection import get_db_connection

bp_gestor_salas = Blueprint('gestor_salas', __name__, url_prefix='/gestao_ambientes/gestor')

@bp_gestor_salas.route('/api/salas', methods=['GET'])
def listar_salas():
    db = get_db_connection()
    salas = db.execute(
        'SELECT id, nome, localizacao, descricao FROM salas ORDER BY nome'
    ).fetchall()
    db.close()
    return jsonify([dict(s) for s in salas])

@bp_gestor_salas.route('/api/salas', methods=['POST'])
def criar_sala():
    data = request.json
    db = get_db_connection()
    cursor = db.execute(
        'INSERT INTO salas (nome, localizacao, descricao) VALUES (?, ?, ?)',
        (data.get("nome"), data.get("localizacao"), data.get("descricao"))
    )
    db.commit()
    novo_id = cursor.lastrowid
    nova = db.execute('SELECT id, nome, localizacao, descricao FROM salas WHERE id = ?', (novo_id,)).fetchone()
    db.close()
    return jsonify(dict(nova)), 201

@bp_gestor_salas.route('/api/salas/<int:id>', methods=['PUT'])
def atualizar_sala(id):
    data = request.json
    db = get_db_connection()
    db.execute(
        'UPDATE salas SET nome = ?, localizacao = ?, descricao = ? WHERE id = ?',
        (data.get("nome"), data.get("localizacao"), data.get("descricao"), id)
    )
    db.commit()
    sala = db.execute('SELECT id, nome, localizacao, descricao FROM salas WHERE id = ?', (id,)).fetchone()
    db.close()
    if sala:
        return jsonify(dict(sala))
    else:
        return jsonify({"erro": "Sala não encontrada"}), 404

@bp_gestor_salas.route('/api/salas/<int:id>', methods=['DELETE'])
def deletar_sala(id):
    db = get_db_connection()
    db.execute('DELETE FROM salas WHERE id = ?', (id,))
    db.commit()
    db.close()
    return '', 204
