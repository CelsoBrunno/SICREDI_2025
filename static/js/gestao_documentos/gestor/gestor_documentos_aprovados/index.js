function abrirModalRejeicao(documentoId) {
    document.getElementById('modalRejeicao' + documentoId).style.display = 'block';
  }
  
  function fecharModalRejeicao(documentoId) {
    document.getElementById('modalRejeicao' + documentoId).style.display = 'none';
  }
  
  // Fechar o modal se clicar fora dele
  window.onclick = function(event) {
    const modals = document.getElementsByClassName('modal-rejeicao');
    for (let modal of modals) {
      if (event.target == modal) {
        modal.style.display = 'none';
      }
    }
  }