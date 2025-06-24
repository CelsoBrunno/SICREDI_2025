import sqlite3
from ..db_connection import get_db_connection

def gestao_de_materiais():

    try:
        # Conectar ao banco de dados (ou criar se não existir)
        conn = get_db_connection()
        cursor = conn.cursor()

        # Gerenciamento de Imobilizados

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS imobilizados (
                id_imobilizado INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(50) NOT NULL,
                codigo TEXT NOT NULL,
                marca VARCHAR(25),
                modelo VARCHAR(25),
                numero_serie VARCHAR(25) UNIQUE NOT NULL,
                data_aquisicao DATE,
                localizacao TEXT,
                responsavel_id INTEGER,
                status NOT NULL CHECK(status IN ('A', 'U', 'D')), -- A: ANALISE / U: USO / D: DISPONIVEL
                    
                FOREIGN KEY (responsavel_id) REFERENCES usuarios(id_usuario)
            );
        ''')
        print("Tabela 'imobilizados' criada com sucesso ou já existente.")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historico_movimentacao_ativos (
                id_historico INTEGER PRIMARY KEY AUTOINCREMENT,
                id_ativo INTEGER NOT NULL,
                local_anterior TEXT,
                local_novo TEXT NOT NULL,
                data_movimentacao DATE NOT NULL,
                id_usuario_responsavel INTEGER,
                    
                FOREIGN KEY (id_ativo) REFERENCES imobilizados(id_imobilizados),
                FOREIGN KEY (id_usuario_responsavel) REFERENCES usuarios(id_usuario)
            );
        ''')
        print("Tabela 'historico_movimentacao_ativos' criada com sucesso ou já existente.")

        # Gerenciamento de Mobilizados

        cursor.execute('''
            -- Criação da tabela equipamentos
            CREATE TABLE IF NOT EXISTS equipamentos (
                id_equipamento INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(50) NOT NULL,
                categoria VARCHAR(50) NOT NULL,
                status VARCHAR(1) CHECK(status IN ('D', 'U', 'M')) NOT NULL
            );
        ''')
        print("Tabela 'equipamentos' criada com sucesso ou já existente.")

        cursor.execute('''
            -- Criação da tabela reservas
            CREATE TABLE IF NOT EXISTS reservas (
                id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
                id_equipamento INTEGER NOT NULL,
                id_usuario INTEGER NOT NULL,
                data_inicio DATETIME NOT NULL,
                data_fim DATETIME NOT NULL,
                status TEXT CHECK(status IN ('em análise', 'aprovado', 'recusado')) NOT NULL,
                
                FOREIGN KEY (id_equipamento) REFERENCES Equipamentos(id),
                FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
            );
        ''')
        print("Tabela 'reservas' criada com sucesso ou já existente.")

        # Gerenciamento de Ambientes

        cursor.execute('''
            -- Criação da tabela salas
            CREATE TABLE IF NOT EXISTS salas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(50) NOT NULL,
                localizacao TEXT NOT NULL,
                descricao TEXT
            );
        ''')
        print("Tabela 'salas' criada com sucesso ou já existente.")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historico_acesso (
                id_historico_acesso INTEGER PRIMARY KEY AUTOINCREMENT,
                id_sala INTEGER NOT NULL,
                id_usuario INTEGER NOT NULL,
                data_hora_entrada DATETIME NOT NULL,
                data_hora_saida DATETIME,
                    
                FOREIGN KEY (id_sala) REFERENCES salas(id),
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
            );
        ''')
        print("Tabela 'historico_acesso' criada com sucesso ou já existente.")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS autorizacoes_acesso (
                id_autorizacoes_acesso INTEGER PRIMARY KEY AUTOINCREMENT,
                id_sala INTEGER NOT NULL,
                cargo_acesso VARCHAR(1) CHECK(cargo_acesso IN ('A', 'G')) NOT NULL, -- 'G' - 'Gestor', 'A' - 'Analista'
                FOREIGN KEY (id_sala) REFERENCES salas(id)
            );
        ''')
        print("Tabela 'autorizacoes_acesso' criada com sucesso ou já existente.")

    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")

    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")


