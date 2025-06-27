# rotas para as páginas do analista da pasta templates
from flask import Blueprint
from app.main.gestao_documentos.analista import analista_bp

# Importar as funções do arquivo principal
from app.main.gestao_documentos.analista import (
    documentos_pendentes,
    documentos_cadastrar,
    documentos_aprovados,
    documentos_reprovados
)

# Usando o blueprint importado do arquivo principal

# Mapear as rotas para as funções do arquivo principal
@analista_bp.route('/documentos_pendentes/')
def documentos_pendentes():
    return documentos_pendentes()

@analista_bp.route('/documentos_cadastrar/', methods=['GET', 'POST'])
def documentos_cadastrar():
    return documentos_cadastrar()

@analista_bp.route('/documentos_aprovados/')
def documentos_aprovados():
    return documentos_aprovados()

@analista_bp.route('/documentos_reprovados/')
def documentos_reprovados():
    return documentos_reprovados()