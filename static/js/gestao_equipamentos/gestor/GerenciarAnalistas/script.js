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

// --- LÓGICA DO CRUD DE ANALISTAS ---
const addAnalystBtn = document.getElementById('add-analyst-btn');
const addAnalystModal = document.getElementById('add-analyst-modal');
const addAnalystOverlay = document.getElementById('add-analyst-overlay');
const closeAddModalBtn = document.getElementById('close-add-modal-btn');
const cancelAddModalBtn = document.getElementById('cancel-add-modal-btn');
const addAnalystForm = document.getElementById('add-analyst-form');
const analystTableBody = document.getElementById('analyst-table-body');
const placeholderRow = document.getElementById('placeholder-row');

const editAnalystModal = document.getElementById('edit-analyst-modal');
const closeEditModalBtn = document.getElementById('close-edit-modal-btn');
const cancelEditModalBtn = document.getElementById('cancel-edit-modal-btn');
const editAnalystForm = document.getElementById('edit-analyst-form');

const deleteConfirmModal = document.getElementById('delete-confirm-modal');
const deleteConfirmOverlay = document.getElementById('delete-confirm-overlay');
const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
const cancelDeleteBtn = document.getElementById('cancel-delete-btn');

const viewPasswordModal = document.getElementById('view-password-modal');
const viewPasswordForm = document.getElementById('view-password-form');
const cancelViewPasswordBtn = document.getElementById('cancel-view-password-btn');

let rowToEdit = null;
let rowToDelete = null;
let rowToShowPassword = null;

const eyeIcon = `<svg class="w-5 h-5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>`;
const eyeSlashedIcon = `<svg class="w-5 h-5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7 1.274-4.057 5.064-7 9.542-7 .847 0 1.673.124 2.468.352M15 12a3 3 0 11-6 0 3 3 0 016 0zm6 0a9.953 9.953 0 01-1.288 4.718M21 21l-4.35-4.35m-1.414-1.414L3 3l1.414 1.414"></path></svg>`;

const openAddModal = () => {
    addAnalystModal.classList.remove('hidden');
    addAnalystOverlay.classList.remove('hidden');
};

const closeAddModal = () => {
    addAnalystModal.classList.add('hidden');
    addAnalystOverlay.classList.add('hidden');
    addAnalystForm.reset(); 
};

const openEditModal = (row) => {
    rowToEdit = row;
    document.getElementById('edit-analyst-name').value = row.dataset.name;
    document.getElementById('edit-analyst-email').value = row.dataset.email;
    document.getElementById('edit-analyst-password').value = ''; // Limpa campo de senha
    editAnalystModal.classList.remove('hidden');
    addAnalystOverlay.classList.remove('hidden');
};

const closeEditModal = () => {
    rowToEdit = null;
    editAnalystModal.classList.add('hidden');
    addAnalystOverlay.classList.add('hidden');
};

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

const openViewPasswordModal = (row) => {
    rowToShowPassword = row;
    viewPasswordModal.classList.remove('hidden');
    addAnalystOverlay.classList.remove('hidden');
};

const closeViewPasswordModal = () => {
    rowToShowPassword = null;
    viewPasswordModal.classList.add('hidden');
    addAnalystOverlay.classList.add('hidden');
    viewPasswordForm.reset();
};

addAnalystBtn.addEventListener('click', openAddModal);
closeAddModalBtn.addEventListener('click', closeAddModal);
cancelAddModalBtn.addEventListener('click', closeAddModal);
addAnalystOverlay.addEventListener('click', () => {
    closeAddModal();
    closeEditModal();
    closeViewPasswordModal();
});

closeEditModalBtn.addEventListener('click', closeEditModal);
cancelEditModalBtn.addEventListener('click', closeEditModal);
cancelViewPasswordBtn.addEventListener('click', closeViewPasswordModal);
cancelDeleteBtn.addEventListener('click', closeDeleteModal);
deleteConfirmOverlay.addEventListener('click', closeDeleteModal);

addAnalystForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const name = document.getElementById('analyst-name').value;
    const email = document.getElementById('analyst-email').value;
    const password = document.getElementById('analyst-password').value;

    if (placeholderRow) placeholderRow.remove();

    const newRow = document.createElement('tr');
    newRow.dataset.name = name;
    newRow.dataset.email = email;
    newRow.dataset.password = password;
    newRow.dataset.passwordVisible = 'false'; // Estado inicial
    newRow.innerHTML = `
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 name-cell">${name}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 email-cell">${email}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 password-cell">
            <span class="password-hidden">********</span>
            <span class="password-visible hidden">${password}</span>
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
            <div class="flex items-center space-x-4">
                <button class="view-password-btn text-gray-400 hover:text-blue-600" title="Ver Senha">${eyeIcon}</button>
                <button class="edit-btn text-gray-400 hover:text-green-600" title="Editar"><svg class="w-5 h-5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.536L16.732 3.732z"></path></svg></button>
                <button class="delete-btn text-gray-400 hover:text-red-600" title="Excluir"><svg class="w-5 h-5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg></button>
            </div>
        </td>
    `;
    analystTableBody.appendChild(newRow);
    closeAddModal();
});

editAnalystForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const newName = document.getElementById('edit-analyst-name').value;
    const newEmail = document.getElementById('edit-analyst-email').value;
    const newPassword = document.getElementById('edit-analyst-password').value;
    
    rowToEdit.querySelector('.name-cell').textContent = newName;
    rowToEdit.querySelector('.email-cell').textContent = newEmail;
    
    rowToEdit.dataset.name = newName;
    rowToEdit.dataset.email = newEmail;

    if (newPassword) {
        rowToEdit.dataset.password = newPassword;
        rowToEdit.querySelector('.password-visible').textContent = newPassword;
        rowToEdit.querySelector('.password-hidden').classList.remove('hidden');
        rowToEdit.querySelector('.password-visible').classList.add('hidden');
        rowToEdit.querySelector('.view-password-btn').innerHTML = eyeIcon;
        rowToEdit.dataset.passwordVisible = 'false';
    }
    
    closeEditModal();
});

confirmDeleteBtn.addEventListener('click', () => {
    if (rowToDelete) {
        rowToDelete.remove();
        if (analystTableBody.childElementCount === 0 && placeholderRow) {
             analystTableBody.appendChild(placeholderRow);
        }
    }
    closeDeleteModal();
});

viewPasswordForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const managerPassword = document.getElementById('manager-password').value;
    if (rowToShowPassword && managerPassword) {
        rowToShowPassword.querySelector('.password-hidden').classList.add('hidden');
        rowToShowPassword.querySelector('.password-visible').classList.remove('hidden');
        rowToShowPassword.dataset.passwordVisible = 'true';
        rowToShowPassword.querySelector('.view-password-btn').innerHTML = eyeSlashedIcon;
    }
    closeViewPasswordModal();
});

analystTableBody.addEventListener('click', (event) => {
    const button = event.target.closest('button');
    if (!button) return;

    const row = button.closest('tr');
    if (button.classList.contains('edit-btn')) {
        openEditModal(row);
    } else if (button.classList.contains('delete-btn')) {
        openDeleteModal(row);
    } else if (button.classList.contains('view-password-btn')) {
        const isVisible = row.dataset.passwordVisible === 'true';
        if (isVisible) {
            row.querySelector('.password-hidden').classList.remove('hidden');
            row.querySelector('.password-visible').classList.add('hidden');
            button.innerHTML = eyeIcon;
            row.dataset.passwordVisible = 'false';
        } else {
            openViewPasswordModal(row);
        }
    }
});