# rotas para as páginas do gestor da pasta templates

from flask import Blueprint, render_template
from app.main.gestao_documentos.gestor import gestor_bp

from app.main.gestao_documentos.gestor import (
    gestor_painel,
    gestor_documentos_aprovados,
    gestor_documentos_reprovados,
)

@gestor_bp.route('/documentos_pendentes/')
def documentos_pendentes():
    return gestor_painel()

@gestor_bp.route('/documentos_reprovados/')
def documentos_reprovados():
    return gestor_documentos_reprovados()

@gestor_bp.route('/documentos_aprovados/')
def documentos_aprovados():
    return gestor_documentos_aprovados()

