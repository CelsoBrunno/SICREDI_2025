"""
Módulo principal para gerenciamento de analistas.
CRUD de analistas, seguindo o padrão das outras áreas do projeto.
"""
from flask import Blueprint, render_template, request, jsonify

bp_analistas = Blueprint('analistas', __name__, url_prefix='/gerenciar_analistas')

from app.db.db_connection import get_db_connection as get_db_connection

@bp_analistas.route('/')
def pagina_analistas():
    """Renderiza a página de analistas."""
    db = get_db_connection()
    analistas = db.execute(
        "SELECT id_usuario as id, nome, email FROM usuarios WHERE cargo = 'A' ORDER BY nome"
    ).fetchall()
    db.close()
    return render_template('gerenciar_analistas/analistas.html', analistas=analistas)

@bp_analistas.route('/api/setores', methods=['GET'])
def listar_setores():
    db = get_db_connection()
    setores = db.execute('SELECT id_setor, nome_setor FROM setores ORDER BY nome_setor').fetchall()
    db.close()
    return jsonify([dict(s) for s in setores])

@bp_analistas.route('/api/analistas', methods=['GET'])
def listar_analistas():
    """Retorna a lista de analistas (JSON)."""
    db = get_db_connection()
    analistas = db.execute(
        "SELECT id_usuario as id, nome, email FROM usuarios WHERE cargo = 'A' ORDER BY nome"
    ).fetchall()
    db.close()
    return jsonify([dict(a) for a in analistas])

@bp_analistas.route('/api/analistas', methods=['POST'])
def criar_analista():
    """Cria um novo analista (salva na tabela usuarios como cargo 'A')."""
    from werkzeug.security import generate_password_hash
    from sqlite3 import IntegrityError, OperationalError
    data = request.json
    db = get_db_connection()
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha", "12345")
    senha_hash = generate_password_hash(senha)
    cargo = 'A'
    try:
        id_setor = int(data.get("id_setor"))
    except (TypeError, ValueError):
        db.close()
        return jsonify({'erro': 'Setor inválido.'}), 400
    try:
        cursor = db.execute(
            'INSERT INTO usuarios (nome, email, senha, cargo, id_setor) VALUES (?, ?, ?, ?, ?)',
            (nome, email, senha_hash, cargo, id_setor)
        )
        db.commit()
        novo_id = cursor.lastrowid
        novo = db.execute('SELECT id_usuario, nome, email, cargo, id_setor FROM usuarios WHERE id_usuario = ?', (novo_id,)).fetchone()
        db.close()
        return jsonify(dict(novo)), 201
    except IntegrityError as e:
        db.close()
        return jsonify({'erro': 'E-mail já cadastrado.'}), 409
    except OperationalError as e:
        db.close()
        if 'database is locked' in str(e):
            return jsonify({'erro': 'Banco de dados ocupado. Tente novamente em instantes.'}), 503
        return jsonify({'erro': 'Erro de banco de dados.'}), 500

@bp_analistas.route('/api/analistas/<int:id>/senha', methods=['POST'])
def ver_senha_analista(id):
    """Retorna a senha do analista se o gestor estiver autenticado."""
    data = request.json or {}
    email_gestor = data.get('email_gestor')
    senha_gestor = data.get('senha_gestor')
    if not email_gestor or not senha_gestor:
        return jsonify({'erro': 'Credenciais do gestor obrigatórias.'}), 400
    db = get_db_connection()
    gestor = db.execute('SELECT senha, cargo FROM usuarios WHERE email = ?', (email_gestor,)).fetchone()
    if not gestor or gestor['cargo'] != 'G':
        db.close()
        return jsonify({'erro': 'Gestor não encontrado.'}), 403
    from app.db.database import check_password
    if not check_password(gestor['senha'], senha_gestor):
        db.close()
        return jsonify({'erro': 'Senha do gestor incorreta.'}), 403
    analista = db.execute("SELECT senha FROM usuarios WHERE id_usuario = ? AND cargo = 'A'", (id,)).fetchone()
    db.close()
    if not analista:
        return jsonify({'erro': 'Analista não encontrado.'}), 404
    return jsonify({'senha': analista['senha']}), 200

@bp_analistas.route('/api/analistas/<int:id>', methods=['PUT'])
def atualizar_analista(id):
    """Atualiza um analista existente, exige autenticação do gestor."""
    data = request.json
    email_gestor = data.get('email_gestor')
    senha_gestor = data.get('senha_gestor')
    if not email_gestor or not senha_gestor:
        return jsonify({'erro': 'Credenciais do gestor obrigatórias.'}), 400
    db = get_db_connection()
    gestor = db.execute('SELECT senha, cargo FROM usuarios WHERE email = ?', (email_gestor,)).fetchone()
    if not gestor or gestor['cargo'] != 'G':
        db.close()
        return jsonify({'erro': 'Gestor não encontrado.'}), 403
    from app.db.database import check_password
    if not check_password(gestor['senha'], senha_gestor):
        db.close()
        return jsonify({'erro': 'Senha do gestor incorreta.'}), 403
    campos = []
    valores = []
    if data.get("nome"):
        campos.append("nome = ?")
        valores.append(data.get("nome"))
    if data.get("email"):
        campos.append("email = ?")
        valores.append(data.get("email"))
    if data.get("senha"):
        from werkzeug.security import generate_password_hash
        campos.append("senha = ?")
        valores.append(generate_password_hash(data.get("senha")))
    if not campos:
        db.close()
        return jsonify({"erro": "Nada para atualizar"}), 400
    valores.append(id)
    db.execute(f"UPDATE usuarios SET {', '.join(campos)} WHERE id_usuario = ? AND cargo = 'A'", valores)
    db.commit()
    analista = db.execute("SELECT id_usuario as id, nome, email FROM usuarios WHERE id_usuario = ? AND cargo = 'A'", (id,)).fetchone()
    db.close()
    if analista:
        return jsonify(dict(analista))
    else:
        return jsonify({"erro": "Analista não encontrado"}), 404

@bp_analistas.route('/api/analistas/<int:id>', methods=['DELETE'])
def deletar_analista(id):
    """Remove um analista, exige autenticação do gestor."""
    data = request.json or {}
    email_gestor = data.get('email_gestor')
    senha_gestor = data.get('senha_gestor')
    if not email_gestor or not senha_gestor:
        return jsonify({'erro': 'Credenciais do gestor obrigatórias.'}), 400
    db = get_db_connection()
    gestor = db.execute('SELECT senha, cargo FROM usuarios WHERE email = ?', (email_gestor,)).fetchone()
    if not gestor or gestor['cargo'] != 'G':
        db.close()
        return jsonify({'erro': 'Gestor não encontrado.'}), 403
    from app.db.database import check_password
    if not check_password(gestor['senha'], senha_gestor):
        db.close()
        return jsonify({'erro': 'Senha do gestor incorreta.'}), 403
    db.execute("DELETE FROM usuarios WHERE id_usuario = ? AND cargo = 'A'", (id,))
    db.commit()
    db.close()
    return '', 204
