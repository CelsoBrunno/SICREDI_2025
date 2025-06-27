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

// --- CARREGAMENTO INICIAL DOS IMOBILIZADOS ---
async function loadEquipamentos() {
    try {
        const response = await fetch('/gestao_equipamentos/gestor/api/imobilizados');
        if (!response.ok) throw new Error('Erro ao buscar imobilizados');
        const equipamentos = await response.json();
        equipmentTableBody.innerHTML = '';
        if (equipamentos.length === 0) {
            if (placeholderRow) placeholderRow.classList.remove('hidden');
        } else {
            if (placeholderRow) placeholderRow.classList.add('hidden');
            equipamentos.forEach(data => {
                const newRow = document.createElement('tr');
                newRow.dataset.id = data.id_imobilizado;
                newRow.dataset.nome = data.nome;
                newRow.dataset.modelo = data.modelo;
                newRow.dataset.codigo = data.codigo;
                newRow.dataset.marca = data.marca;
                newRow.dataset.serie = data.numero_serie;
                newRow.dataset.local = data.localizacao;
                newRow.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${data.nome}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${data.modelo}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${data.codigo}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${data.numero_serie}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 local-cell">${data.localizacao}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div class="flex items-center space-x-4">
                            <button class="view-btn text-gray-400 hover:text-blue-600" title="Ver"><svg class="w-5 h-5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg></button>
                            <button class="edit-btn text-gray-400 hover:text-green-600" title="Editar"><svg class="w-5 h-5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.536L16.732 3.732z"></path></svg></button>
                            <button class="delete-btn text-gray-400 hover:text-red-600" title="Excluir"><svg class="w-5 h-5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg></button>
                        </div>
                    </td>
                `;
                equipmentTableBody.appendChild(newRow);
            });
        }
    } catch (error) {
        if (placeholderRow) placeholderRow.classList.remove('hidden');
        console.error(error);
    }
}

// Chama o carregamento inicial ao abrir a página
window.addEventListener('DOMContentLoaded', loadEquipamentos);

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
// Overlay click for add modal is handled by the generic overlay variable

addEquipmentForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const nome = document.getElementById('equip-nome').value;
    const modelo = document.getElementById('equip-modelo').value;
    const codigo = document.getElementById('equip-codigo').value;
    const marca = document.getElementById('equip-marca').value;
    const serie = document.getElementById('equip-serie').value;
    const local = document.getElementById('equip-local').value;

    const payload = {
        nome,
        modelo,
        codigo,
        marca,
        serie,
        local
    };

    try {
        const response = await fetch('/gestao_equipamentos/gestor/api/imobilizados', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert('Erro ao salvar equipamento: ' + (errorData.error || response.status));
            return;
        }
        const data = await response.json();

        if (placeholderRow) placeholderRow.remove();

        const newRow = document.createElement('tr');
        newRow.dataset.nome = data.nome;
        newRow.dataset.modelo = data.modelo;
        newRow.dataset.codigo = data.codigo;
        newRow.dataset.marca = data.marca;
        newRow.dataset.serie = data.numero_serie;
        newRow.dataset.local = data.localizacao;

        newRow.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${data.nome}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${data.modelo}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${data.codigo}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${data.numero_serie}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 local-cell">${data.localizacao}</td>
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
    } catch (error) {
        alert('Erro ao salvar equipamento: ' + error);
    }
});

// --- LÓGICA DO MODAL EDITAR ---
const editEquipmentModal = document.getElementById('edit-equipment-modal');
const closeEditModalBtn = document.getElementById('close-edit-modal-btn');
const cancelEditModalBtn = document.getElementById('cancel-edit-modal-btn');
const editEquipmentForm = document.getElementById('edit-equipment-form');
let rowToEdit = null;
let rowToEditId = null;

const openEditModal = (row) => {
    rowToEdit = row;
    rowToEditId = row.dataset.id;
    document.getElementById('edit-equip-nome').value = row.dataset.nome;
    document.getElementById('edit-equip-modelo').value = row.dataset.modelo;
    document.getElementById('edit-equip-codigo').value = row.dataset.codigo;
    document.getElementById('edit-equip-marca').value = row.dataset.marca;
    document.getElementById('edit-equip-serie').value = row.dataset.serie;
    document.getElementById('edit-equip-local').value = row.dataset.local;
    editEquipmentModal.classList.remove('hidden');
    addEquipmentOverlay.classList.remove('hidden');
};

const closeEditModal = () => {
    rowToEdit = null;
    rowToEditId = null;
    editEquipmentModal.classList.add('hidden');
    addEquipmentOverlay.classList.add('hidden');
};

closeEditModalBtn.addEventListener('click', closeEditModal);
cancelEditModalBtn.addEventListener('click', closeEditModal);

editEquipmentForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!rowToEdit || !rowToEditId) return;
    const nome = document.getElementById('edit-equip-nome').value;
    const modelo = document.getElementById('edit-equip-modelo').value;
    const codigo = document.getElementById('edit-equip-codigo').value;
    const marca = document.getElementById('edit-equip-marca').value;
    const serie = document.getElementById('edit-equip-serie').value;
    const local = document.getElementById('edit-equip-local').value;
    const payload = { nome, modelo, codigo, marca, serie, local };
    try {
        const response = await fetch(`/gestao_equipamentos/gestor/api/imobilizados/${rowToEditId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!response.ok) throw new Error('Erro ao editar equipamento');
        const data = await response.json();
        // Atualiza a linha na tabela
        rowToEdit.dataset.nome = data.nome;
        rowToEdit.dataset.modelo = data.modelo;
        rowToEdit.dataset.codigo = data.codigo;
        rowToEdit.dataset.marca = data.marca;
        rowToEdit.dataset.serie = data.numero_serie;
        rowToEdit.dataset.local = data.localizacao;
        rowToEdit.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${data.nome}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${data.modelo}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${data.codigo}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${data.numero_serie}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 local-cell">${data.localizacao}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <div class="flex items-center space-x-4">
                    <button class="view-btn text-gray-400 hover:text-blue-600" title="Ver"><svg class="w-5 h-5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg></button>
                    <button class="edit-btn text-gray-400 hover:text-green-600" title="Editar"><svg class="w-5 h-5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.536L16.732 3.732z"></path></svg></button>
                    <button class="delete-btn text-gray-400 hover:text-red-600" title="Excluir"><svg class="w-5 h-5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg></button>
                </div>
            </td>
        `;
        closeEditModal();
    } catch (error) {
        alert('Erro ao editar equipamento: ' + error.message);
    }
});


// --- LÓGICA DO MODAL VER ---
const viewEquipmentModal = document.getElementById('view-equipment-modal');
const closeViewModalBtn = document.getElementById('close-view-modal-btn');
const okViewModalBtn = document.getElementById('ok-view-modal-btn');

const openViewModal = (row) => {
    // Preencher os detalhes
    document.getElementById('view-equip-nome').textContent = row.dataset.nome;
    document.getElementById('view-equip-modelo').textContent = row.dataset.modelo;
    document.getElementById('view-equip-codigo').textContent = row.dataset.codigo;
    document.getElementById('view-equip-marca').textContent = row.dataset.marca;
    document.getElementById('view-equip-serie').textContent = row.dataset.serie;
    document.getElementById('view-equip-local').textContent = row.dataset.local;

    viewEquipmentModal.classList.remove('hidden');
    addEquipmentOverlay.classList.remove('hidden');
};

const closeViewModal = () => {
    viewEquipmentModal.classList.add('hidden');
    addEquipmentOverlay.classList.add('hidden');
};

closeViewModalBtn.addEventListener('click', closeViewModal);
okViewModalBtn.addEventListener('click', closeViewModal);


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

confirmDeleteBtn.addEventListener('click', async () => {
    if (rowToDelete) {
        const id = rowToDelete.dataset.id;
        try {
            const response = await fetch(`/gestao_equipamentos/gestor/api/imobilizados/${id}`, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error('Erro ao excluir equipamento');
            rowToDelete.remove();
            if (equipmentTableBody.children.length === 0 && placeholderRow) {
                placeholderRow.classList.remove('hidden');
            }
        } catch (error) {
            alert('Erro ao excluir equipamento: ' + error.message);
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