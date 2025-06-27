// Função para abrir modal de rejeição
function abrirModalRejeicao(documentoId) {
    const modal = document.getElementById('modalRejeicao' + documentoId);
    if (modal) {
        modal.style.display = 'block';
    }
}

// Função para fechar modal de rejeição
function fecharModalRejeicao(documentoId) {
    const modal = document.getElementById('modalRejeicao' + documentoId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// Fechar modal se clicar fora dele
window.onclick = function(event) {
    if (event.target.classList.contains('modal-rejeicao')) {
        event.target.style.display = 'none';
    }
};

// Adicionar evento de clique para o botão de cancelar nos modais
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('cancelar')) {
        const modal = event.target.closest('.modal-rejeicao');
        if (modal) {
            modal.style.display = 'none';
        }
    }
});