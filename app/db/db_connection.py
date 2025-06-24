import sqlite3
import os

def get_db_connection():
    """
    Cria e retorna uma conexão com o banco de dados SQLite.
    """
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'sicredi.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    print(f'Conectando ao banco de dados em: {os.path.abspath(db_path)}')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn