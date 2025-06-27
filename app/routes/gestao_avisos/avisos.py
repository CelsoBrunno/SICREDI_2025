from flask import Blueprint, flash, redirect, url_for, session
from app.db.db_connection import get_db_connection as get_db
from flask import Blueprint, flash, redirect, url_for, session, render_template

# Cria blueprint para rotas de avisos
bp = Blueprint('avisos', __name__, url_prefix='/avisos')

@bp.route('/')
def listar_avisos():
    """
    Mostra avisos não lidos para o usuário atual
    e marca como lido quando visualizado
    """
    db = get_db()
    
    # Busca avisos não lidos para o setor do usuário
    avisos = db.execute(
        """SELECT a.* FROM avisos a 
           LEFT JOIN leituras l ON a.id_aviso = l.id_aviso AND l.id_usuario = ? 
           WHERE l.id_leitura IS NULL AND (a.id_setor IS NULL OR a.id_setor = ?) 
           AND datetime(a.data_validade) >= datetime('now')""",
        (session['user_id'], session['id_setor'])
    ).fetchall()
    
    # Marca cada aviso como lido
    for aviso in avisos:
        db.execute(
            "INSERT OR IGNORE INTO leituras (id_usuario, id_aviso) VALUES (?, ?)",
            (session['user_id'], aviso['id_aviso'])
        )
        # Mostra mensagem flash com o título do aviso
        flash(f"Novo aviso: {aviso['titulo']}", 'info')
    
    db.commit()
    return render_template('gestao_avisos/gestor/painel_avisos/painel.html', avisos=avisos)

@bp.route('/gestao_avisos')
def gestao_avisos():
    """
    Painel de gestão de avisos
    Acesso restrito a gestores
    Mostra todos os avisos com contagem de visualizações
    """
    if session['user_type'] != 'G':
        return redirect(url_for('index'))
        
    db = get_db()
    
    # Busca avisos com contagem de quem visualizou
    avisos = db.execute(
        """SELECT a.*, COUNT(l.id_leitura) as visualizacoes 
           FROM avisos a LEFT JOIN leituras l ON a.id_aviso = l.id_aviso 
           GROUP BY a.id_aviso"""
    ).fetchall()
    
    return render_template('gestao_avisos/gestor/tabela_leitura.html', avisos=avisos)