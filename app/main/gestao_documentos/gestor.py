from cgi import print_environ
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
from app.db.db_connection import get_db_connection

# Cria o blueprint para as rotas do gestor de documentos
gestor_bp = Blueprint('gestor', __name__, url_prefix='/gestor')

def format_sqlite_date(date_str):
    """Converte a string de data do SQLite para objeto datetime"""
    try:
        if isinstance(date_str, str):
            return datetime.strptime(date_str, '%d-%m-%Y')
        return date_str
    except ValueError:
        return datetime.now()

def formatar_valor(valor):
    """Formata um valor numérico para o padrão brasileiro com 2 casas decimais e vírgula"""
    return f"R$ {valor:,.2f}".replace('.', ',')

@gestor_bp.route('/documentos_pendentes/')
def documentos_pendentes():
    
    # Verifica se o usuário está logado e é gestor
    if 'user_id' not in session:
        print("Usuário não está logado")
        return redirect(url_for('login'))
    
    if session.get('user_type') != 'G':
        print("Usuário não é gestor")
        return redirect(url_for('gestao'))
    
    conn = None
    try:
        conn = get_db_connection()
        documentos = conn.execute("""
            SELECT d.id_documento, d.titulo, u.nome as nome_analista, d.data_envio, d.valor_emprestimo, d.prazo_financiamento, d.valor_total_sicredi 
            FROM documentos d
            JOIN usuarios u ON d.id_responsavel = u.id_usuario
            WHERE d.status = 'P'
            ORDER BY d.data_envio DESC
        """).fetchall()
        
        documentos_processados = []
        for doc in documentos:
            doc_dict = dict(doc)
            doc_dict['data_envio'] = format_sqlite_date(doc_dict['data_envio'])
            doc_dict['valor_emprestimo'] = formatar_valor(doc_dict['valor_emprestimo'])
            doc_dict['valor_total_sicredi'] = formatar_valor(doc_dict['valor_total_sicredi'])
            documentos_processados.append(doc_dict)
        
        return render_template('gestao_documentos/gestor/gestor_documentos_pendentes/gestor_painel.html', 
                documentos=documentos_processados)
        
    except Exception as e:
        return render_template('gestao_documentos/gestor/gestor_documentos_pendentes/gestor_painel.html', documentos=[])
    finally:
        if conn:
            conn.close()
            
@gestor_bp.route('/documentos_aprovados/')
def documentos_aprovados():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = None
    try:
        conn = get_db_connection()
        documentos = conn.execute("""
            SELECT d.id_documento, d.titulo, u.nome as nome_analista, d.data_envio 
            FROM documentos d
            JOIN usuarios u ON d.id_responsavel = u.id_usuario
            WHERE d.status = 'AP'
            ORDER BY d.data_envio DESC
        """).fetchall()

        documentos_processados = []
        for doc in documentos:
            doc_dict = dict(doc)
            doc_dict['data_envio'] = format_sqlite_date(doc_dict['data_envio'])
            documentos_processados.append(doc_dict)
        
        return render_template('gestao_documentos/gestor/gestor_documentos_aprovados/gestor_documentos_aprovados.html', documentos=documentos_processados)
        
    except Exception as e:
        return render_template('gestao_documentos/gestor/gestor_documentos_aprovados/gestor_documentos_aprovados.html', documentos=[])
    finally:
        if conn:
            conn.close()
            
@gestor_bp.route('/gestor_aprovar_documento/<int:documento_id>', methods=['POST'])
def gestor_aprovar_documento(documento_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = None
    try:
        conn = get_db_connection()
        # Atualiza o status do documento para 'aprovado'
        conn.execute("""
            UPDATE documentos 
            SET status = 'AP' 
            WHERE id_documento = ?
        """, (documento_id,))
        conn.commit()
        
    except Exception as e:
        print(f'Erro ao aprovar documento: {str(e)}')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('gestor.documentos_pendentes'))

@gestor_bp.route('/documentos_reprovados/')
def documentos_reprovados():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = None
    try:
        conn = get_db_connection()
        print("Executando consulta SQL para documentos reprovados...")
        documentos = conn.execute("""
            SELECT d.id_documento, d.titulo, u.nome as nome_analista, d.data_envio, d.motivo_rejeicao
            FROM documentos d
            JOIN usuarios u ON d.id_responsavel = u.id_usuario
            WHERE d.status = 'R'
            ORDER BY d.data_envio DESC
        """).fetchall()

        documentos_processados = []
        for doc in documentos:
            doc_dict = dict(doc)
            doc_dict['data_envio'] = format_sqlite_date(doc_dict['data_envio'])
            documentos_processados.append(doc_dict)
        
        return render_template('gestao_documentos/gestor/gestor_documentos_reprovados/gestor_documentos_reprovados.html', documentos=documentos_processados)
        
    except Exception as e:
        print(f'Erro ao carregar documentos reprovados: {str(e)}')
        return render_template('gestao_documentos/gestor/gestor_documentos_reprovados/gestor_documentos_reprovados.html', documentos=[])
    finally:
        if conn:
            conn.close()
            
@gestor_bp.route('/gestor_reprovar_documento/<int:documento_id>', methods=['POST'])
def gestor_reprovar_documento(documento_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Pega o motivo da rejeição.
    motivo_rejeicao = request.form.get('motivo_rejeicao')
    
    # Verifica se o motivo da rejeição foi informado.
    if not motivo_rejeicao or not motivo_rejeicao.strip():
        flash('Por favor, informe o motivo da rejeição', 'danger')
        return redirect(url_for('gestor.documentos_pendentes'))
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Atualiza o status do documento e o motivo da rejeição.
        cursor.execute("""
            UPDATE documentos 
            SET status = 'R', 
                motivo_rejeicao = ?
            WHERE id_documento = ?
        """, (motivo_rejeicao.strip(), documento_id))
        
        if cursor.rowcount == 0:
            flash('Documento não encontrado', 'danger')
        else:
            conn.commit()
            
            
    except Exception as e:
        conn.rollback()
        print(f"Erro ao reprovar documento: {str(e)}")
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('gestor.documentos_pendentes'))