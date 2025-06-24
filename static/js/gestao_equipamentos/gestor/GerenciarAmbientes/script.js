// --- LÓGICA DO MENU LATERAL ---
const openMenuBtn = document.getElementById('open-menu-btn');
const closeMenuBtn = document.getElementById('close-menu-btn');
const sidebarMenu = document.getElementById('sidebar-menu');
const sidebarOverlay = document.getElementById('sidebar-overlay');

const openMenu = () => {
    sidebarMenu.classList.remove('-translate-x-full');
    sidebarOverlay.classList.remove('hidden');
};

const closeMenu = () => {
    sidebarMenu.classList.add('-translate-x-full');
    sidebarOverlay.classList.add('hidden');
};

openMenuBtn.addEventListener('click', openMenu);
closeMenuBtn.addEventListener('click', closeMenu);
sidebarOverlay.addEventListener('click', closeMenu);

// --- LÓGICA DO MENU DE PERFIL ---
const profileMenuBtn = document.getElementById('profile-menu-btn');
const profileDropdown = document.getElementById('profile-dropdown');

profileMenuBtn.addEventListener('click', () => {
    profileDropdown.classList.toggle('hidden');
});

window.addEventListener('click', (event) => {
    if (!profileMenuBtn.contains(event.target) && !profileDropdown.contains(event.target)) {
        profileDropdown.classList.add('hidden');
    }
});

// --- LÓGICA DO MODAL NOVO AMBIENTE ---
const addEnvironmentBtn = document.getElementById('add-environment-btn');
const addEnvironmentModal = document.getElementById('add-environment-modal');
const addEnvironmentOverlay = document.getElementById('add-environment-overlay');
const closeAddModalBtn = document.getElementById('close-add-modal-btn');
const cancelAddModalBtn = document.getElementById('cancel-add-modal-btn');
const addEnvironmentForm = document.getElementById('add-environment-form');
const environmentsTableBody = document.getElementById('environments-table-body');
const placeholderRow = document.getElementById('placeholder-row');

const openAddEnvironmentModal = () => {
    addEnvironmentModal.classList.remove('hidden');
    addEnvironmentOverlay.classList.remove('hidden');
};

const closeAddEnvironmentModal = () => {
    addEnvironmentModal.classList.add('hidden');
    addEnvironmentOverlay.classList.add('hidden');
    addEnvironmentForm.reset(); 
};

addEnvironmentBtn.addEventListener('click', openAddEnvironmentModal);
closeAddModalBtn.addEventListener('click', closeAddEnvironmentModal);
cancelAddModalBtn.addEventListener('click', closeAddEnvironmentModal);
addEnvironmentOverlay.addEventListener('click', closeAddEnvironmentModal);

addEnvironmentForm.addEventListener('submit', (event) => {
    event.preventDefault(); 
    const environmentName = document.getElementById('ambiente-nome').value;
    const selectedUsersCheckboxes = document.querySelectorAll('input[name="users"]:checked');
    const selectedUsers = Array.from(selectedUsersCheckboxes).map(cb => cb.value);

    if(placeholderRow && !placeholderRow.classList.contains('hidden')){
        placeholderRow.classList.add('hidden');
    }
    
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td class="px-6 py-4 whitespace-nowrap">
            <div class="text-sm font-medium text-gray-900">${environmentName}</div>
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
            <div class="text-sm text-gray-700">${selectedUsers.join(', ') || 'Nenhum usuário selecionado'}</div>
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
            <div class="flex items-center space-x-4">
                <button class="text-gray-400 hover:text-blue-600" title="Ver">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
                </button>
                <button class="text-gray-400 hover:text-green-600" title="Editar">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.536L16.732 3.732z"></path></svg>
                </button>
                <button class="delete-btn text-gray-400 hover:text-red-600" title="Excluir">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </button>
            </div>
        </td>
    `;
    
    environmentsTableBody.appendChild(newRow);
    closeAddEnvironmentModal();
});

// --- LÓGICA DO MODAL DE EXCLUSÃO ---
const deleteConfirmModal = document.getElementById('delete-confirm-modal');
const deleteConfirmOverlay = document.getElementById('delete-confirm-overlay');
const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
const cancelDeleteBtn = document.getElementById('cancel-delete-btn');
let rowToDelete = null;

const openDeleteModal = (row) => {
    rowToDelete = row;
    deleteConfirmModal.classList.remove('hidden');
    deleteConfirmOverlay.classList.remove('hidden');
};

const closeDeleteModal = () => {
    rowToDelete = null;
    deleteConfirmModal.classList.add('hidden');
    deleteConfirmOverlay.classList.add('hidden');
};

cancelDeleteBtn.addEventListener('click', closeDeleteModal);
deleteConfirmOverlay.addEventListener('click', closeDeleteModal);

confirmDeleteBtn.addEventListener('click', () => {
    if (rowToDelete) {
        rowToDelete.remove();
        if (environmentsTableBody.childElementCount === 1) { // Apenas o cabeçalho está no table (ou o placeholder)
             if(placeholderRow) placeholderRow.classList.remove('hidden');
        }
    }
    closeDeleteModal();
});

// Event listener na tabela para os botões de ação (Event Delegation)
environmentsTableBody.addEventListener('click', (event) => {
    const button = event.target.closest('button');
    if (!button) return;

    if (button.classList.contains('delete-btn')) {
        const row = button.closest('tr');
        openDeleteModal(row);
    }
    // Adicionar lógica para 'Ver' e 'Editar' aqui no futuro
});