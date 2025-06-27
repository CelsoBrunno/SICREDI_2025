import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .execute_db.sistema_centralizado import sistema_centralizado
from .execute_db.gestao_de_materiais import gestao_de_materiais
from .execute_db.avisos_internos import avisos_internos
from .execute_db.gestao_documentos import gestao_documentos
# Importa função de conexão ao banco de dados para ser reexportada neste módulo
from .db_connection import get_db_connection

# Funções utilitárias de hashing de senha usadas em todo o sistema

def hash_password(password: str) -> str:
    """Gera o hash seguro da senha utilizando Werkzeug."""
    return generate_password_hash(password)


def check_password(password_hash: str, plain_password: str) -> bool:
    """Compara a senha em texto plano com o hash armazenado no banco."""
    return check_password_hash(password_hash, plain_password)



def init_db():
    sistema_centralizado()
    gestao_de_materiais()
    avisos_internos()
    gestao_documentos()

