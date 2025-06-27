from flask import Blueprint, render_template, request, jsonify, abort
from app.main.gestao_equipamentos import gestor as gestor_logic

# Renomeei o blueprint para ser mais específico e evitar conflitos.
gestor_mobilizados_bp = Blueprint(
    'gestor_mobilizados', 
    __name__,
    # O prefixo de URL será definido no __init__.py
)

# ROTA PRINCIPAL: Exibe a página com a lista de equipamentos
@gestor_mobilizados_bp.route('/')
def pagina_mobilizados():
    """Renderiza a página principal de gerenciamento de equipamentos mobilizados."""
    return render_template('gestao_equipamentos/gestor/equipamentos_mobilizados/mobilizados.html')

# --- API Endpoints para o JavaScript (CRUD) ---

@gestor_mobilizados_bp.route('/api/equipamentos', methods=['GET'])
def api_get_equipamentos():
    """API para listar todos os equipamentos. Retorna JSON."""
    try:
        equipamentos_db = gestor_logic.listar_todos_mobilizados()
        # Converte os objetos 'Row' do banco em dicionários para poder serializar para JSON.
        equipamentos = [dict(row) for row in equipamentos_db]
        return jsonify(equipamentos)
    except Exception as e:
        # Log do erro seria útil aqui
        return jsonify({'error': 'Erro ao buscar equipamentos.'}), 500


@gestor_mobilizados_bp.route('/api/equipamentos', methods=['POST'])
def api_add_equipamento():
    """API para adicionar um novo equipamento. Retorna JSON."""
    data = request.get_json()
    if not data or not 'nome' in data:
        abort(400, description="Dados inválidos. 'nome' é obrigatório.")
    
    nome = data['nome']
    # Categoria é opcional
    categoria = data.get('categoria', '')

    try:
        novo_id = gestor_logic.adicionar_mobilizado(nome, categoria)
        novo_equipamento = gestor_logic.buscar_mobilizado_por_id(novo_id)
        return jsonify(dict(novo_equipamento)), 201 # 201 Created
    except Exception as e:
        return jsonify({'error': 'Erro ao adicionar equipamento.'}), 500


@gestor_mobilizados_bp.route('/api/equipamentos/<int:id>', methods=['GET'])
def api_get_equipamento(id):
    """API para buscar um equipamento por ID. Retorna JSON."""
    try:
        equipamento = gestor_logic.buscar_mobilizado_por_id(id)
        if equipamento is None:
            abort(404, description="Equipamento não encontrado.")
        return jsonify(dict(equipamento))
    except Exception as e:
        return jsonify({'error': 'Erro ao buscar equipamento.'}), 500


@gestor_mobilizados_bp.route('/api/equipamentos/<int:id>', methods=['PUT'])
def api_update_equipamento(id):
    """API para atualizar um equipamento. Retorna JSON."""
    data = request.get_json()
    if not data or not 'nome' in data:
        abort(400, description="Dados inválidos.")

    try:
        gestor_logic.atualizar_mobilizado(id, data['nome'], data.get('categoria', ''))
        equipamento_atualizado = gestor_logic.buscar_mobilizado_por_id(id)
        return jsonify(dict(equipamento_atualizado))
    except Exception as e:
        return jsonify({'error': 'Erro ao atualizar equipamento.'}), 500


@gestor_mobilizados_bp.route('/api/equipamentos/<int:id>', methods=['DELETE'])
def api_delete_equipamento(id):
    """API para deletar um equipamento."""
    try:
        gestor_logic.deletar_mobilizado(id)
        return jsonify({'success': True, 'message': 'Equipamento deletado com sucesso.'})
    except Exception as e:
        return jsonify({'error': 'Erro ao deletar equipamento.'}), 500

