"""Entry point for the Sicredi management system.

This script imports the Flask application instance (``app``) defined in
``app/routes/principal/principal.py`` and starts the development server so that
executing ``python run.py`` will launch the web application.
"""

from app.routes.principal.principal import app
# Importação direta dos blueprints das suas áreas
from app.main.gestao_documentos.gestor import gestor_bp
from app.main.gestao_documentos.analista import analista_bp
from app.main.gestao_equipamentos.gestor import bp_gestor_equipamentos
from app.main.gestao_equipamentos.analista import bp_analista_equipamentos
from app.main.gestao_ambientes.gestor import bp_gestor_ambientes
from app.main.gerenciar_analistas.analistas import bp_analistas
from app.db.db_connection import get_db_connection

# Inicialização/ajuste das tabelas do banco para as áreas do usuário
with get_db_connection() as db:
    db.execute('''CREATE TABLE IF NOT EXISTS analistas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL
    )''')
    db.execute('''CREATE TABLE IF NOT EXISTS ambientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        localizacao TEXT
    )''')
    db.execute('''CREATE TABLE IF NOT EXISTS equipamentos_mobilizados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT,
        status TEXT DEFAULT 'disponivel',
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    db.execute('''CREATE TABLE IF NOT EXISTS reservas_mobilizados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipamento_id INTEGER NOT NULL,
        analista_nome TEXT NOT NULL,
        data_inicio_reserva TIMESTAMP NOT NULL,
        data_fim_reserva TIMESTAMP NOT NULL,
        status TEXT DEFAULT 'pendente',
        FOREIGN KEY (equipamento_id) REFERENCES equipamentos_mobilizados(id)
    )''')
    db.commit()

# Registrar os blueprints no app principal
app.register_blueprint(gestor_bp)
app.register_blueprint(analista_bp)
app.register_blueprint(bp_gestor_equipamentos)
app.register_blueprint(bp_analista_equipamentos)
app.register_blueprint(bp_gestor_ambientes)
app.register_blueprint(bp_analistas)

if __name__ == "__main__":
    # Run the Flask development server
    # Set host to 0.0.0.0 so the app is accessible on the local network if needed
    app.run(host="0.0.0.0", port=5000, debug=True)
