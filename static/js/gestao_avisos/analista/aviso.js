// <!-- Script para controlar a exibição do overlay -->

  const btnLido = document.getElementById('btnLido');
  const overlay = document.getElementById('overlay');
  const conteudoSite = document.getElementById('conteudoSite');

  btnLido.addEventListener('click', () => {
    overlay.classList.add('hidden');  // Esconde o overlay
    conteudoSite.style.display = 'block';  // Exibe o conteúdo principal do site
  });
