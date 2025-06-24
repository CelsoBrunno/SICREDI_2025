from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Função para conectar ao banco de dados
def get_db():
    db = sqlite3.connect('sicredi.db')
    db.row_factory = sqlite3.Row
    return db

# Função para inicializar o banco e criar usuários iniciais
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
        
        cursor = db.cursor()
        cursor.execute(
            'INSERT OR IGNORE INTO usuarios (email, senha, tipo) VALUES (?, ?, ?)',
            ('gestor@sicredi.com.br', generate_password_hash('gestor123'), 'gestor')
        )
        cursor.execute(
            'INSERT OR IGNORE INTO usuarios (email, senha, tipo) VALUES (?, ?, ?)',
            ('analista@sicredi.com.br', generate_password_hash('analista123'), 'analista')
        )
        db.commit()

# Página inicial: se logado, redireciona para o dashboard certo
@app.route('/')
def home():
    if 'usuario_id' in session:
        if session['tipo_usuario'] == 'gestor':
            return redirect(url_for('dashboard_gestor'))
        else:
            return redirect(url_for('dashboard_analista'))
    return render_template('login.html')

# Rota para processar o login (apenas POST)
@app.route('/login', methods=['POST'])
def login():
    email = request.form['usuario']
    senha = request.form['senha']
    
    db = get_db()
    usuario = db.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
    
    if usuario and check_password_hash(usuario['senha'], senha):
        session['usuario_id'] = usuario['id']
        session['tipo_usuario'] = usuario['tipo']
        
        if usuario['tipo'] == 'gestor':
            return redirect(url_for('dashboard_gestor'))
        else:
            return redirect(url_for('dashboard_analista'))
    
    return redirect(url_for('home'))

# Rota para logout: limpa sessão e volta para a tela inicial
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Dashboard do gestor: só acessa se for gestor
@app.route('/dashboard-gestor')
def dashboard_gestor():
    if 'usuario_id' not in session or session['tipo_usuario'] != 'gestor':
        return redirect(url_for('home'))
    return render_template('gestao.html', tipo_usuario='gestor')

# Dashboard do analista: só acessa se for analista
@app.route('/dashboard-analista')
def dashboard_analista():
    if 'usuario_id' not in session or session['tipo_usuario'] != 'analista':
        return redirect(url_for('home'))
    return render_template('gestao.html', tipo_usuario='analista')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
