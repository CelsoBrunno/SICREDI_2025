import sqlite3
from werkzeug.security import generate_password_hash
from ..db_connection import get_db_connection

# Função para conectar ao banco de dados

def avisos_internos():
    try:
            # Conectar ao banco de dados (ou criar se não existir)
        conn = get_db_connection()
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS avisos (
                id_aviso INT AUTO_INCREMENT PRIMARY KEY,
                titulo VARCHAR(255) NOT NULL,
                descricao TEXT NOT NULL,
                id_autor INT NOT NULL, 
                id_setor INT NULL, 
                data_publicacao DATETIME NOT NULL,
                data_validade DATETIME NOT NULL,
                FOREIGN KEY (id_autor) REFERENCES Usuarios(id_usuario),
                FOREIGN KEY (id_setor) REFERENCES Setores(id_setor) 
                -- Chaves estrangeiras da tabela Usuario, sendo elas: id_usuario,id_setor
            );
        ''')

        print("Tabela 'avisos' criada com sucesso ou já existentes.")


    # Cria tabela de Leituras com as colunas 'id_leitura', ' id_usuario', 'id_aviso','data_leitura' e tem duas chaves estrangeiras: id_usuario, id_aviso.
        c.execute('''
            CREATE TABLE IF NOT EXISTS leituras (
                id_leitura INT AUTO_INCREMENT PRIMARY KEY,
                id_usuario INT NOT NULL,
                id_aviso INT NOT NULL,
                data_leitura DATETIME NOT NULL,
                FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
                FOREIGN KEY (id_aviso) REFERENCES Avisos(id_aviso),
                UNIQUE (id_usuario, id_aviso) 
                -- evita marcar como lido 2 vezes
    );
    ''')


        print("Tabela 'leituras' criada com sucesso ou já existentes.")

    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")

    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")










