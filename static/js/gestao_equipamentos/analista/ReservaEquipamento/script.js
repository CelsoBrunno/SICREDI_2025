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

// --- LÓGICA DO FORMULÁRIO DE SOLICITAÇÃO ---
const requestReservationForm = document.getElementById('request-reservation-form');
const myReservationsTableBody = document.getElementById('my-reservations-table-body');

requestReservationForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const equipamento = document.getElementById('reserva-equip').value;
    const inicio = new Date(document.getElementById('reserva-inicio').value);
    const fim = new Date(document.getElementById('reserva-fim').value);
    
    const formatDate = (date) => date.toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });

    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${equipamento}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">De: ${formatDate(inicio)}<br>Até: ${formatDate(fim)}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm status-cell">
            <span class="status-badge px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                Em Análise
            </span>
        </td>
    `;
    
    myReservationsTableBody.prepend(newRow); // Adiciona no topo da lista
    requestReservationForm.reset();
});
