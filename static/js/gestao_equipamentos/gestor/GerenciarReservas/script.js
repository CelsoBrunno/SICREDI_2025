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

// --- LÓGICA DAS AÇÕES DA TABELA ---
const reservationTableBody = document.getElementById('reservation-table-body');
reservationTableBody.addEventListener('click', (event) => {
    const button = event.target.closest('button');
    if (!button) return;

    const row = button.closest('tr');
    const statusCell = row.querySelector('.status-cell .status-badge');
    const actionButtons = row.querySelector('.action-buttons');

    if (button.classList.contains('approve-btn')) {
        statusCell.textContent = 'Aprovado';
        statusCell.classList.remove('bg-yellow-100', 'text-yellow-800', 'bg-red-100', 'text-red-800');
        statusCell.classList.add('bg-green-100', 'text-green-800');
        actionButtons.innerHTML = ''; // Remove botões após ação
    } else if (button.classList.contains('reject-btn')) {
        statusCell.textContent = 'Recusado';
        statusCell.classList.remove('bg-yellow-100', 'text-yellow-800', 'bg-green-100', 'text-green-800');
        statusCell.classList.add('bg-red-100', 'text-red-800');
        actionButtons.innerHTML = ''; // Remove botões após ação
    }
});