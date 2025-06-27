document.addEventListener('DOMContentLoaded', function() {
    // Botão para abrir o menu
    const openMenuBtn = document.getElementById('open-menu-btn');
    if (openMenuBtn) {
        openMenuBtn.addEventListener('click', function() {
            document.getElementById('sidebar-menu').classList.remove('-translate-x-full');
            document.getElementById('sidebar-overlay').classList.remove('hidden');
        });
    }

    // Botão para fechar o menu
    const closeMenuBtn = document.getElementById('close-menu-btn');
    if (closeMenuBtn) {
        closeMenuBtn.addEventListener('click', function() {
            document.getElementById('sidebar-menu').classList.add('-translate-x-full');
            document.getElementById('sidebar-overlay').classList.add('hidden');
        });
    }

    // Fechar o menu ao clicar no overlay
    const overlay = document.getElementById('sidebar-overlay');
    if (overlay) {
        overlay.addEventListener('click', function() {
            document.getElementById('sidebar-menu').classList.add('-translate-x-full');
            this.classList.add('hidden');
        });
    }

    // Menu do perfil do usuário
    const profileMenuBtn = document.getElementById('profile-menu-btn');
    const profileDropdown = document.getElementById('profile-dropdown');

    if (profileMenuBtn && profileDropdown) {
        // Abrir/fechar menu do perfil
        profileMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            profileDropdown.classList.toggle('hidden');
        });

        // Fechar menu ao clicar fora dele
        document.addEventListener('click', function(event) {
            if (!profileMenuBtn.contains(event.target) && !profileDropdown.contains(event.target)) {
                profileDropdown.classList.add('hidden');
            }
        });
    }
});
