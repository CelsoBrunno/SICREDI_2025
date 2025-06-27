from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime
from app.db.db_connection import get_db_connection

# Cria o blueprint para as rotas do analista de documentos
analista_bp = Blueprint('analista', __name__, url_prefix='/analista')


def format_sqlite_date(date_str):
    """Converte a string de data do SQLite para objeto datetime"""
    try:
        if isinstance(date_str, str):
            return datetime.strptime(date_str, '%d-%m-%Y ')
        return date_str
    except ValueError:
        return datetime.now()

def formatar_valor(valor):
    """Formata um valor numérico para o padrão brasileiro com 2 casas decimais e vírgula"""
    return f"R$ {valor:,.2f}".replace('.', ',')

@analista_bp.route('/documentos_pendentes/')
def documentos_pendentes():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        conn = get_db_connection()
        documentos = conn.execute("""
            SELECT d.id_documento, d.titulo, u.nome as nome_analista, d.data_envio, d.valor_emprestimo, d.prazo_financiamento, d.valor_total_sicredi 
            FROM documentos d
            JOIN usuarios u ON d.id_responsavel = u.id_usuario
            WHERE d.status = 'P' AND d.id_responsavel = ?
            ORDER BY d.data_envio DESC
        """, (session['user_id'],)).fetchall()

        documentos_processados = []
        for doc in documentos:
            doc_dict = dict(doc)
            doc_dict['data_envio'] = format_sqlite_date(doc_dict['data_envio'])
            doc_dict['valor_emprestimo'] = formatar_valor(doc_dict['valor_emprestimo'])
            doc_dict['valor_total_sicredi'] = formatar_valor(doc_dict['valor_total_sicredi'])
            documentos_processados.append(doc_dict)
        
        return render_template('gestao_documentos/analista/analista_documentos/analista_documentos.html', documentos=documentos_processados)
        
    except Exception as e:
        print(f'Erro ao buscar documentos: {str(e)}')
        return redirect(url_for('analista.documentos_pendentes'))
    finally:
        if conn:
            conn.close()
            
@analista_bp.route('/documentos_cadastrar/', methods=['GET', 'POST'])
def documentos_cadastrar():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('gestao_documentos/analista/analista_documentos_cadastrar/analista_documentos_cadastrar.html')

    try:
        nome = request.form.get('nome')
        cpf = request.form.get('CPF')
        estabelecimento = request.form.get('Estabelecimento')
        valor_emprestimo = float(request.form.get('valor_emprestimo'))
        prazo_financiamento = int(request.form.get('prazo_financiamento'))
        
        # Calculando o valor total do Sicredi (1.5% ao mês)
        taxa_sicredi = 0.015
        parcela = (valor_emprestimo * taxa_sicredi) / (1 - (1 + taxa_sicredi) ** -prazo_financiamento)
        valor_total_sicredi = parcela * prazo_financiamento
        
        if not all([nome, cpf, estabelecimento]):
            flash('Preencha todos os campos obrigatórios', 'danger')
            return redirect(url_for('analista.documentos_cadastrar'))

        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11:
            flash('CPF deve conter 11 dígitos', 'danger')
            return redirect(url_for('analista.documentos_cadastrar'))

        conn = get_db_connection()
        try:
            conn.execute("""
                INSERT INTO documentos 
                (titulo, descricao, status, id_responsavel, nivel_aprovacao_atual, data_envio, valor_emprestimo, prazo_financiamento, valor_total_sicredi) 
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?, ?)
            """, (
                f"Empréstimo - {nome}",
                f"Cliente: {nome}\nCPF: {cpf}\nEstabelecimento: {estabelecimento}",
                'P',
                session['user_id'],
                1,
                valor_emprestimo,
                prazo_financiamento,
                valor_total_sicredi
            ))
            conn.commit()
            print('Documento cadastrado com sucesso!')
            return redirect(url_for('analista.documentos_pendentes'))
            
        except sqlite3.Error as e:
            conn.rollback()
            print(f'Erro no banco de dados: {str(e)}')
            return redirect(url_for('analista.documentos_cadastrar'))
            
        finally:
            conn.close()
            
    except Exception as e:
        print(f'Erro inesperado: {str(e)}')
        return redirect(url_for('analista.documentos_cadastrar'))

@analista_bp.route('/documentos_aprovados/')
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
            WHERE d.status = 'AP' AND d.id_responsavel = ?
            ORDER BY d.data_envio DESC
        """, (session['user_id'],)).fetchall()

        documentos_processados = []
        for doc in documentos:
            doc_dict = dict(doc)
            doc_dict['data_envio'] = format_sqlite_date(doc_dict['data_envio'])
            documentos_processados.append(doc_dict)
        
        return render_template('gestao_documentos/analista/analista_documentos_aprovados/analista_documentos_aprovados.html', documentos=documentos_processados)
        
    except Exception as e:
        print(f'Erro ao carregar documentos aprovados: {str(e)}')
        return redirect(url_for('analista.documentos_pendentes'))
    finally:
        if conn:
            conn.close()

@analista_bp.route('/documentos_reprovados/')
def documentos_reprovados():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = None
    try:
        conn = get_db_connection()
        documentos = conn.execute("""
            SELECT d.id_documento, d.titulo, u.nome as nome_analista, d.data_envio, d.motivo_rejeicao 
            FROM documentos d
            JOIN usuarios u ON d.id_responsavel = u.id_usuario
            WHERE d.status = 'R' AND d.id_responsavel = ?
            ORDER BY d.data_envio DESC
        """, (session['user_id'],)).fetchall()

        documentos_processados = []
        for doc in documentos:
            doc_dict = dict(doc)
            doc_dict['data_envio'] = format_sqlite_date(doc_dict['data_envio'])
            documentos_processados.append(doc_dict)
        
        return render_template('gestao_documentos/analista/analista_documentos_reprovados/analista_documentos_reprovados.html', documentos=documentos_processados)
        
    except Exception as e:
        print(f'Erro ao carregar documentos reprovados: {str(e)}')
        return redirect(url_for('analista.documentos_pendentes'))
    finally:
        if conn:
            conn.close()