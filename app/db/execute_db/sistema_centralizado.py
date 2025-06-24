import datetime
import sqlite3
import uuid
from werkzeug.security import generate_password_hash
from ..db_connection import get_db_connection 


def sistema_centralizado():
    try:
        # Conectar ao banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;")

        # Criação da tabela Setores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS setores (
                id_setor INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_setor VARCHAR(100) NOT NULL UNIQUE,
                descricao VARCHAR(255)
            );
        ''')
        print("Tabela 'setores' criada com sucesso ou já existente.")

        # Inserindo setor exemplo
        setor_exemplo = ('TI', 'Setor de Tecnologia da Informação')
        cursor.execute("INSERT OR IGNORE INTO setores(nome_setor, descricao) VALUES (?, ?)", setor_exemplo)

        # Criação da tabela Usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(20) NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                cargo TEXT CHECK(cargo IN ('A', 'G')) NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                id_setor INTEGER,
                FOREIGN KEY (id_setor) REFERENCES setores(id_setor)
            );
        ''')
        print("Tabela 'usuarios' criada com sucesso ou já existente.")

        # Inserindo usuário exemplo
        usuario_exemplo = ('admin', 'admin@gmail.com', generate_password_hash('12345'), 'G', 1)
        usuario_exemplo = ('analista', 'analista@gmail.com', generate_password_hash('12345'), 'A', 1)
        cursor.execute("INSERT OR IGNORE INTO usuarios(nome, email, senha, cargo, id_setor) VALUES (?, ?, ?, ?, ?)", usuario_exemplo)

        # Confirma as alterações

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessoes (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                usuario_id INTEGER,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario)
            );
''')
        sessao_id = str(uuid.uuid4())
        data_atual = "2025-06-23T14:53:10.123"
        cursor.execute('''
            INSERT INTO sessoes (id, data, usuario_id)
            VALUES (?, ?, ?)
        ''', (sessao_id, data_atual, 1))


        conn.commit()




    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")

    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")
