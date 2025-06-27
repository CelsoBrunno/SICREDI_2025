from flask import Blueprint, render_template, request, jsonify, abort
from app.main.gestao_equipamentos import analista as analista_logic

analista_bp = Blueprint(
    'analista_reservas', 
    __name__
)

# ROTA PRINCIPAL: Exibe a página de reserva para o analista
@analista_bp.route('/')
def pagina_reserva_equipamentos():
    """Renderiza a página principal de reserva de equipamentos para o analista."""
    # A página será populada dinamicamente via chamadas de API do JavaScript
    return render_template('gestao_equipamentos/analista/reserva_mobilizado/equipamento.html')

# --- API Endpoints para o JavaScript ---

@analista_bp.route('/api/equipamentos-disponiveis', methods=['GET'])
def api_get_equipamentos():
    """API para listar todos os equipamentos disponíveis para reserva."""
    try:
        equipamentos_db = analista_logic.listar_equipamentos_para_reserva()
        equipamentos = [dict(row) for row in equipamentos_db]
        return jsonify(equipamentos)
    except Exception as e:
        print(f"Erro na API de equipamentos: {e}")
        return jsonify({'error': 'Erro ao buscar equipamentos.'}), 500

@analista_bp.route('/api/minhas-reservas', methods=['GET'])
def api_get_minhas_reservas():
    """API para listar as reservas de um analista específico."""
    # Em um sistema real, o nome do analista viria de uma sessão de login.
    # Por enquanto, usaremos um nome fixo para o exemplo.
    analista_nome = "José da Silva" 
    try:
        reservas_db = analista_logic.listar_reservas_por_analista(analista_nome)
        reservas = [dict(row) for row in reservas_db]
        return jsonify(reservas)
    except Exception as e:
        print(f"Erro na API de minhas reservas: {e}")
        return jsonify({'error': 'Erro ao buscar reservas.'}), 500

@analista_bp.route('/api/reservas', methods=['POST'])
def api_add_reserva():
    """API para criar uma nova solicitação de reserva."""
    data = request.get_json()
    if not data or not all(k in data for k in ['equipamento_id', 'data_inicio', 'data_fim']):
        abort(400, description="Dados incompletos para a reserva.")
    
    # Nome fixo para o exemplo
    analista_nome = "José da Silva"

    try:
        analista_logic.criar_reserva(
            data['equipamento_id'],
            analista_nome,
            data['data_inicio'],
            data['data_fim']
        )
        return jsonify({'success': True, 'message': 'Solicitação de reserva enviada com sucesso!'}), 201
    except Exception as e:
        print(f"Erro ao criar reserva: {e}")
        return jsonify({'error': 'Erro ao criar a solicitação de reserva.'}), 500
