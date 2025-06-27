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

// Função para carregar todos os equipamentos do backend
async function carregarEquipamentos() {
    equipmentTableBody.innerHTML = `<tr><td colspan="4" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center">Carregando equipamentos...</td></tr>`;
    try {
        const res = await fetch('/gestao_equipamentos/gestor/api/mobilizados');
        const equipamentos = await res.json();
        if (equipamentos.length === 0) {
            equipmentTableBody.innerHTML = `<tr><td colspan="4" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center">Nenhum equipamento encontrado.</td></tr>`;
            return;
        }
        equipmentTableBody.innerHTML = '';
        equipamentos.forEach(equip => {
            const row = document.createElement('tr');
            row.dataset.id = equip.id;
            row.dataset.nome = equip.nome;
            row.dataset.categoria = equip.categoria;
            row.dataset.status = equip.status || '';
            row.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 nome-cell">${equip.nome}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 categoria-cell">${equip.categoria}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 status-cell">${equip.status || ''}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div class="flex items-center space-x-4">
                        <button class="view-btn text-gray-400 hover:text-blue-600" title="Ver">Ver</button>
                        <button class="edit-btn text-gray-400 hover:text-green-600" title="Editar">Editar</button>
                        <button class="delete-btn text-gray-400 hover:text-red-600" title="Excluir">Excluir</button>
                    </div>
                </td>
            `;
            equipmentTableBody.appendChild(row);
        });
        adicionarListenersAcoes();
    } catch (err) {
        equipmentTableBody.innerHTML = `<tr><td colspan="4" class="px-6 py-4 text-center text-red-600">Erro ao carregar equipamentos.</td></tr>`;
    }
}

window.addEventListener('DOMContentLoaded', carregarEquipamentos);

// Função para adicionar listeners aos botões de ação
function adicionarListenersAcoes() {
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', (e) => openEditModal(e.target.closest('tr')));
    });
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', (e) => openDeleteModal(e.target.closest('tr')));
    });
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', (e) => openViewModal(e.target.closest('tr')));
    });
}

const openAddEquipmentModal = () => {
    addEquipmentModal.classList.remove('hidden');
    addEquipmentOverlay.classList.remove('hidden');
    console.log('[DEBUG] Modal de adicionar equipamento aberto');
};

const closeAddEquipmentModal = () => {
    addEquipmentModal.classList.add('hidden');
    addEquipmentOverlay.classList.add('hidden');
    addEquipmentForm.reset(); 
};

addEquipmentBtn.addEventListener('click', () => {
    console.log('[DEBUG] Botão + Novo Equipamento clicado');
    openAddEquipmentModal();
});
closeAddModalBtn.addEventListener('click', closeAddEquipmentModal);
cancelAddModalBtn.addEventListener('click', closeAddEquipmentModal);

addEquipmentForm.addEventListener('submit', async (event) => {
    event.preventDefault(); 
    const nome = document.getElementById('equip-nome').value;
    const categoria = document.getElementById('equip-categoria').value;
    try {
        const res = await fetch('/gestao_equipamentos/gestor/api/mobilizados', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, categoria })
        });
        if (res.ok) {
            await carregarEquipamentos();
            closeAddEquipmentModal();
        } else {
            alert('Erro ao adicionar equipamento.');
        }
    } catch {
        alert('Erro ao adicionar equipamento.');
    }
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

editEquipmentForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!rowToEdit) return;
    const id = rowToEdit.dataset.id;
    const newNome = document.getElementById('edit-equip-nome').value;
    const newCategoria = document.getElementById('edit-equip-categoria').value;
    try {
        const res = await fetch(`/gestao_equipamentos/gestor/api/mobilizados/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome: newNome, categoria: newCategoria })
        });
        if (res.ok) {
            await carregarEquipamentos();
            closeEditModal();
        } else {
            alert('Erro ao editar equipamento.');
        }
    } catch {
        alert('Erro ao editar equipamento.');
    }
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

// Função para abrir o modal de exclusão
const openDeleteModal = (row) => {
    rowToDelete = row;
    deleteConfirmModal.classList.remove('hidden');
    deleteConfirmOverlay.classList.remove('hidden');
};

// Função para fechar o modal de exclusão
const closeDeleteModal = () => {
    rowToDelete = null;
    deleteConfirmModal.classList.add('hidden');
    deleteConfirmOverlay.classList.add('hidden');
};

cancelDeleteBtn.addEventListener('click', closeDeleteModal);
deleteConfirmOverlay.addEventListener('click', closeDeleteModal);

confirmDeleteBtn.addEventListener('click', async () => {
    if (!rowToDelete) return;
    const id = rowToDelete.dataset.id;
    try {
        const res = await fetch(`/gestao_equipamentos/gestor/api/mobilizados/${id}`, {
            method: 'DELETE'
        });
        if (res.ok) {
            await carregarEquipamentos();
            closeDeleteModal();
        } else {
            alert('Erro ao excluir equipamento.');
        }
    } catch {
        alert('Erro ao excluir equipamento.');
    }
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