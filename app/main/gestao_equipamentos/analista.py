from app.db.db_connection import get_db_connection
from flask import Blueprint, render_template, request, jsonify
from datetime import datetime

bp_analista_equipamentos = Blueprint('bp_analista_equipamentos', __name__, url_prefix='/gestao_equipamentos/analista')

# Rotas REST para analista de equipamentos
@bp_analista_equipamentos.route('/')
def pagina_reserva_mobilizado():
    equipamentos = listar_equipamentos_para_reserva()
    return render_template('gestao_equipamentos/analista/reserva_mobilizado/equipamento.html', equipamentos=equipamentos)

@bp_analista_equipamentos.route('/api/equipamentos-disponiveis', methods=['GET'])
def api_equipamentos_disponiveis():
    equipamentos = listar_equipamentos_para_reserva()
    return jsonify([dict(e) for e in equipamentos])

@bp_analista_equipamentos.route('/api/minhas-reservas', methods=['GET'])
def api_minhas_reservas():
    analista_nome = request.args.get('analista_nome', '')
    if not analista_nome:
        from flask import session
        analista_nome = session.get('user_name', '')
    reservas = listar_reservas_por_analista(analista_nome)
    return jsonify([dict(r) for r in reservas])

# Rotas alternativas para compatibilidade de frontend analista
# Essas rotas devem ser registradas diretamente no app principal, não no blueprint.
try:
    from app.routes.principal.principal import app

    @app.route('/analista/reservas/api/equipamentos-disponiveis', methods=['GET'])
    def alt_api_equipamentos_disponiveis():
        return api_equipamentos_disponiveis()

    @app.route('/analista/reservas/api/minhas-reservas', methods=['GET'])
    def alt_api_minhas_reservas():
        return api_minhas_reservas()

    @app.route('/analista/reservas/api/reservas', methods=['POST'])
    def alt_api_criar_reserva():
        return api_criar_reserva()
except ImportError:
    # Durante importações de blueprint, ignore para evitar erro circular
    pass

@bp_analista_equipamentos.route('/api/reservas', methods=['GET'])
def api_listar_reservas():
    analista_nome = request.args.get('analista_nome', '')
    reservas = listar_reservas_por_analista(analista_nome)
    return jsonify([dict(r) for r in reservas])

@bp_analista_equipamentos.route('/api/reservas', methods=['POST'])
def api_criar_reserva():
    data = request.json
    analista_nome = data.get('analista_nome')
    if not analista_nome:
        # Busca o nome do analista da sessão Flask
        from flask import session
        analista_nome = session.get('user_name', '')
    reserva_id = criar_reserva(data['equipamento_id'], analista_nome, data['data_inicio'], data['data_fim'])
    return jsonify({'id': reserva_id}), 201


def listar_equipamentos_para_reserva():
    """Busca todos os equipamentos disponíveis para reserva (sem reserva em análise/aprovada)."""
    db = get_db_connection()
    equipamentos = db.execute('''
        SELECT e.id, e.nome
        FROM equipamentos_mobilizados e
        WHERE e.id NOT IN (
            SELECT r.equipamento_id
            FROM reservas_mobilizados r
            WHERE r.status IN ('em_analise', 'aprovada')
        )
        ORDER BY e.nome
    ''').fetchall()
    return equipamentos

def criar_reserva(equipamento_id, analista_nome, data_inicio, data_fim):
    """Cria uma nova solicitação de reserva no banco de dados."""
    db = get_db_connection()
    
    # Converte as strings de data/hora para objetos datetime
    # O formato de entrada do datetime-local é 'YYYY-MM-DDTHH:MM'
    inicio_dt = datetime.fromisoformat(data_inicio)
    fim_dt = datetime.fromisoformat(data_fim)

    cursor = db.execute(
        'INSERT INTO reservas_mobilizados (equipamento_id, analista_nome, data_inicio_reserva, data_fim_reserva, status) VALUES (?, ?, ?, ?, ?)',
        (equipamento_id, analista_nome, inicio_dt, fim_dt, 'em_analise')
    )
    db.commit()
    return cursor.lastrowid

def listar_reservas_por_analista(analista_nome):
    """
    Busca todas as reservas de um analista específico, juntando com o nome do equipamento.
    """
    db = get_db_connection()
    reservas = db.execute(
        """
        SELECT 
            r.id, 
            r.data_inicio_reserva, 
            r.data_fim_reserva, 
            r.status,
            e.nome as equipamento_nome
        FROM reservas_mobilizados r
        JOIN equipamentos_mobilizados e ON r.equipamento_id = e.id
        WHERE r.analista_nome = ?
        ORDER BY r.data_inicio_reserva DESC
        """,
        (analista_nome,)
    ).fetchall()
    return reservas
