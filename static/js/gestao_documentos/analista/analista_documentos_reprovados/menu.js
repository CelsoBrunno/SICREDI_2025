document.addEventListener('DOMContentLoaded', function() {
    // Botões do menu
    const openMenuBtn = document.getElementById('open-menu-btn');
    const closeMenuBtn = document.getElementById('close-menu-btn');
    const sidebarMenu = document.getElementById('sidebar-menu');
    const sidebarOverlay = document.getElementById('sidebar-overlay');
    const profileMenuBtn = document.getElementById('profile-menu-btn');
    const profileDropdown = document.getElementById('profile-dropdown');

    // Função para abrir o menu
    function openMenu() {
        sidebarMenu.classList.remove('transform', '-translate-x-full');
        sidebarMenu.classList.add('translate-x-0');
        sidebarOverlay.classList.remove('hidden');
    }

    // Função para fechar o menu
    function closeMenu() {
        sidebarMenu.classList.remove('translate-x-0');
        sidebarMenu.classList.add('transform', '-translate-x-full');
        sidebarOverlay.classList.add('hidden');
    }

    // Função para mostrar/ocultar o dropdown do perfil
    function toggleProfileDropdown() {
        profileDropdown.classList.toggle('hidden');
    }

    // Event listeners
    if (openMenuBtn) {
        openMenuBtn.addEventListener('click', openMenu);
    }
    if (closeMenuBtn) {
        closeMenuBtn.addEventListener('click', closeMenu);
    }
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeMenu);
    }
    if (profileMenuBtn) {
        profileMenuBtn.addEventListener('click', toggleProfileDropdown);
    }
    
    // Fechar dropdown quando clicar fora
    document.addEventListener('click', function(event) {
        if (!profileDropdown.contains(event.target) && !profileMenuBtn.contains(event.target)) {
            profileDropdown.classList.add('hidden');
        }
    });
});
