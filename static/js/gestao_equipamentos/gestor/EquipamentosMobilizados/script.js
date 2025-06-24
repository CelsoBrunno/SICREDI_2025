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

// --- LÓGICA DO MODAL ADICIONAR EQUIPAMENTO ---
const addEquipmentBtn = document.getElementById('add-equipment-btn');
const addEquipmentModal = document.getElementById('add-equipment-modal');
const addEquipmentOverlay = document.getElementById('add-equipment-overlay');
const closeAddModalBtn = document.getElementById('close-add-modal-btn');
const cancelAddModalBtn = document.getElementById('cancel-add-modal-btn');
const addEquipmentForm = document.getElementById('add-equipment-form');
const equipmentTableBody = document.getElementById('equipment-table-body');
const placeholderRow = document.getElementById('placeholder-row');

const openAddEquipmentModal = () => {
    addEquipmentModal.classList.remove('hidden');
    addEquipmentOverlay.classList.remove('hidden');
};

const closeAddEquipmentModal = () => {
    addEquipmentModal.classList.add('hidden');
    addEquipmentOverlay.classList.add('hidden');
    addEquipmentForm.reset(); 
};

addEquipmentBtn.addEventListener('click', openAddEquipmentModal);
closeAddModalBtn.addEventListener('click', closeAddEquipmentModal);
cancelAddModalBtn.addEventListener('click', closeAddEquipmentModal);

addEquipmentForm.addEventListener('submit', (event) => {
    event.preventDefault(); 
    
    const nome = document.getElementById('equip-nome').value;
    const categoria = document.getElementById('equip-categoria').value;

    if(placeholderRow) placeholderRow.remove();
    
    const newRow = document.createElement('tr');
    newRow.dataset.nome = nome;
    newRow.dataset.categoria = categoria;

    newRow.innerHTML = `
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 nome-cell">${nome}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 categoria-cell">${categoria}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
            <div class="flex items-center space-x-4">
                <button class="view-btn text-gray-400 hover:text-blue-600" title="Ver"><svg class="w-5 h-5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg></button>
                <button class="edit-btn text-gray-400 hover:text-green-600" title="Editar"><svg class="w-5 h-5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.536L16.732 3.732z"></path></svg></button>
                <button class="delete-btn text-gray-400 hover:text-red-600" title="Excluir"><svg class="w-5 h-5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg></button>
            </div>
        </td>
    `;
    
    equipmentTableBody.appendChild(newRow);
    closeAddEquipmentModal();
});

// --- LÓGICA DO MODAL EDITAR ---
const editEquipmentModal = document.getElementById('edit-equipment-modal');
const closeEditModalBtn = document.getElementById('close-edit-modal-btn');
const cancelEditModalBtn = document.getElementById('cancel-edit-modal-btn');
const editEquipmentForm = document.getElementById('edit-equipment-form');
let rowToEdit = null;

const openEditModal = (row) => {
    rowToEdit = row;
    document.getElementById('edit-equip-nome').value = row.dataset.nome;
    document.getElementById('edit-equip-categoria').value = row.dataset.categoria;
    editEquipmentModal.classList.remove('hidden');
    addEquipmentOverlay.classList.remove('hidden');
};

const closeEditModal = () => {
    rowToEdit = null;
    editEquipmentModal.classList.add('hidden');
    addEquipmentOverlay.classList.add('hidden');
};

closeEditModalBtn.addEventListener('click', closeEditModal);
cancelEditModalBtn.addEventListener('click', closeEditModal);

editEquipmentForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const newNome = document.getElementById('edit-equip-nome').value;
    const newCategoria = document.getElementById('edit-equip-categoria').value;

    rowToEdit.querySelector('.nome-cell').textContent = newNome;
    rowToEdit.querySelector('.categoria-cell').textContent = newCategoria;

    rowToEdit.dataset.nome = newNome;
    rowToEdit.dataset.categoria = newCategoria;
    closeEditModal();
});


// --- LÓGICA DO MODAL VER ---
const viewEquipmentModal = document.getElementById('view-equipment-modal');
const closeViewModalBtn = document.getElementById('close-view-modal-btn');
const okViewModalBtn = document.getElementById('ok-view-modal-btn');

const openViewModal = (row) => {
    document.getElementById('view-equip-nome').textContent = row.dataset.nome;
    document.getElementById('view-equip-categoria').textContent = row.dataset.categoria;
    viewEquipmentModal.classList.remove('hidden');
    addEquipmentOverlay.classList.remove('hidden');
};

const closeViewModal = () => {
    viewEquipmentModal.classList.add('hidden');
    addEquipmentOverlay.classList.add('hidden');
};

closeViewModalBtn.addEventListener('click', closeViewModal);
okViewModalBtn.addEventListener('click', closeViewModal);

addEquipmentOverlay.addEventListener('click', () => {
    closeAddEquipmentModal();
    closeEditModal();
    closeViewModal();
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
        if (equipmentTableBody.children.length === 1 && placeholderRow) { 
             placeholderRow.classList.remove('hidden');
        }
    }
    closeDeleteModal();
});

// --- DELEGAÇÃO DE EVENTOS PARA A TABELA ---
equipmentTableBody.addEventListener('click', (event) => {
    const button = event.target.closest('button');
    if (!button) return;

    const row = button.closest('tr');
    if (!row) return;

    if (button.classList.contains('delete-btn')) {
        openDeleteModal(row);
    } else if (button.classList.contains('edit-btn')) {
        openEditModal(row);
    } else if (button.classList.contains('view-btn')) {
        openViewModal(row);
    }
});