import sqlite3
from ..db_connection import get_db_connection

def gestao_documentos():
    try:
        # Conectar ao banco de dados (ou criar se não existir)
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS processos (
                id_processo INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) NOT NULL,
                descricao TEXT
            );
        ''')
        print("Tabela 'processos' criada com sucesso ou já existente.")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documentos (
                id_documento INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo VARCHAR(255) NOT NULL,
                descricao TEXT,
                status VARCHAR(20) CHECK(status IN ('P', 'AN', 'AP', 'R')) NOT NULL, -- P - PENDENTE / AN - ANALISE / AP - APROVADO / R - REJEITADO.
                data_envio TIMESTAMP,
                id_responsavel INT,
                id_processo INT,
                nivel_aprovacao_atual SMALLINT,
                motivo_rejeicao TEXT,
                valor_emprestimo DECIMAL(10,2),
                prazo_financiamento INT,
                valor_total_sicredi DECIMAL(10,2),
                FOREIGN KEY (id_responsavel) REFERENCES usuarios(id_usuario),
                FOREIGN KEY (id_processo) REFERENCES processos(id_processo)
            );
        ''')
        print("Tabela 'documentos' criada com sucesso ou já existente.")






    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")

    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")