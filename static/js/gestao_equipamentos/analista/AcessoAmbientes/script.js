// --- LÓGICA DO MENU LATERAL ---
const openMenuBtn = document.getElementById('open-menu-btn');
const closeMenuBtn = document.getElementById('close-menu-btn');
const sidebarMenu = document.getElementById('sidebar-menu');
const sidebarOverlay = document.getElementById('sidebar-overlay');
openMenuBtn.addEventListener('click', () => {
    sidebarMenu.classList.remove('-translate-x-full');
    sidebarOverlay.classList.remove('hidden');
});
const closeMenu = () => {
    sidebarMenu.classList.add('-translate-x-full');
    sidebarOverlay.classList.add('hidden');
};
closeMenuBtn.addEventListener('click', closeMenu);
sidebarOverlay.addEventListener('click', closeMenu);

// --- LÓGICA DO MENU DE PERFIL ---
const profileMenuBtn = document.getElementById('profile-menu-btn');
const profileDropdown = document.getElementById('profile-dropdown');
profileMenuBtn.addEventListener('click', () => profileDropdown.classList.toggle('hidden'));
window.addEventListener('click', (event) => {
    if (!profileMenuBtn.contains(event.target) && !profileDropdown.contains(event.target)) {
        profileDropdown.classList.add('hidden');
    }
});

// --- LÓGICA DO CONTROLE DE ACESSO ---
let isUserInsideARoom = false; // Variável para controlar se o usuário já está em uma sala

const accessButtons = document.querySelectorAll('.access-btn');
const permissionDeniedModal = document.getElementById('permission-denied-modal');
const permissionDeniedOverlay = document.getElementById('permission-denied-overlay');
const okPermissionDeniedBtn = document.getElementById('ok-permission-denied-btn');

const multipleRoomsModal = document.getElementById('multiple-rooms-modal');
const multipleRoomsOverlay = document.getElementById('multiple-rooms-modal').previousElementSibling;
const okMultipleRoomsBtn = document.getElementById('ok-multiple-rooms-btn');

const openPermissionModal = () => {
    permissionDeniedModal.classList.remove('hidden');
    permissionDeniedOverlay.classList.remove('hidden');
};
const closePermissionModal = () => {
    permissionDeniedModal.classList.add('hidden');
    permissionDeniedOverlay.classList.add('hidden');
};
okPermissionDeniedBtn.addEventListener('click', closePermissionModal);
permissionDeniedOverlay.addEventListener('click', closePermissionModal);

const openMultipleRoomsModal = () => {
    multipleRoomsModal.classList.remove('hidden');
    multipleRoomsOverlay.classList.remove('hidden');
};

const closeMultipleRoomsModal = () => {
    multipleRoomsModal.classList.add('hidden');
    multipleRoomsOverlay.classList.add('hidden');
};
okMultipleRoomsBtn.addEventListener('click', closeMultipleRoomsModal);
multipleRoomsOverlay.addEventListener('click', closeMultipleRoomsModal);


accessButtons.forEach(button => {
    button.addEventListener('click', () => {
        const hasPermission = button.dataset.hasPermission === 'true';

        if (hasPermission) {
            const isInside = button.dataset.isInside === 'true';
            if (isInside) {
                // Ação de Sair
                button.textContent = 'Entrar';
                button.classList.remove('bg-red-500', 'hover:bg-red-700');
                button.classList.add('bg-[#3b8114]', 'hover:bg-[#326d11]');
                button.dataset.isInside = 'false';
                isUserInsideARoom = false; // Libera para entrar em outra sala
            } else {
                // Ação de Entrar
                if (isUserInsideARoom) {
                    openMultipleRoomsModal(); // Alerta que já está em uma sala
                } else {
                    button.textContent = 'Sair';
                    button.classList.remove('bg-[#3b8114]', 'hover:bg-[#326d11]');
                    button.classList.add('bg-red-500', 'hover:bg-red-700');
                    button.dataset.isInside = 'true';
                    isUserInsideARoom = true; // Bloqueia para não entrar em outra
                }
            }
        } else {
            // Sem permissão
            openPermissionModal();
        }
    });
});