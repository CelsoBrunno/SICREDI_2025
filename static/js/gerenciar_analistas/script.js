// JS para CRUD de analistas

document.addEventListener('DOMContentLoaded', function() {
    // Modal de novo analista
    const openBtn = document.querySelector('.btn-novo-analista');
    const modal = document.getElementById('add-analyst-modal');
    const overlay = document.getElementById('add-analyst-overlay');
    const closeBtn = document.getElementById('close-add-modal-btn');
    const form = document.getElementById('add-analyst-form');
    const tableBody = document.getElementById('analyst-table-body');

    if (openBtn && modal && overlay && closeBtn) {
        openBtn.addEventListener('click', () => {
            // Preencher dropdown de setores
            const sectorSelect = document.getElementById('analyst-sector');
            if (sectorSelect) {
                sectorSelect.innerHTML = '<option value="">Carregando setores...</option>';
                fetch('/gerenciar_analistas/api/setores')
                    .then(res => res.json())
                    .then(setores => {
                        sectorSelect.innerHTML = '<option value="">Selecione um setor</option>';
                        setores.forEach(setor => {
                            const opt = document.createElement('option');
                            opt.value = setor.id_setor;
                            opt.textContent = setor.nome_setor;
                            sectorSelect.appendChild(opt);
                        });
                    })
                    .catch(() => {
                        sectorSelect.innerHTML = '<option value="">Erro ao carregar setores</option>';
                    });
            }
            modal.classList.remove('hidden');
            overlay.classList.remove('hidden');
        });
        closeBtn.addEventListener('click', () => {
            modal.classList.add('hidden');
            overlay.classList.add('hidden');
        });
        overlay.addEventListener('click', () => {
            modal.classList.add('hidden');
            overlay.classList.add('hidden');
        });
    }

    // CRUD: Adicionar Analista
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const nome = document.getElementById('analyst-name').value;
            const email = document.getElementById('analyst-email').value;
            const senha = document.getElementById('analyst-password').value;
            const id_setor = document.getElementById('analyst-sector').value;
            fetch('/gerenciar_analistas/api/analistas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nome, email, senha, id_setor })
            })
            .then(res => {
                if (!res.ok) {
                    if (res.status === 409) {
                        alert('E-mail já cadastrado!');
                        return;
                    } else if (res.status === 503) {
                        alert('Banco de dados ocupado. Tente novamente.');
                        return;
                    } else {
                        alert('Erro ao cadastrar analista.');
                        return;
                    }
                }
                return res.json();
            })
            .then(data => {
                if (data && data.id_usuario) {
                    addAnalystRow(data);
                    form.reset();
                    modal.classList.add('hidden');
                    overlay.classList.add('hidden');
                }
            });
        });
    }

    // Função para adicionar linha na tabela
    function addAnalystRow(analista) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${analista.nome}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${analista.email}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-center">
                <button class="view-password-btn text-gray-600 hover:text-green-700" title="Ver senha" data-id="${analista.id}">
                    <i class="fa-solid fa-eye"></i>
                </button>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-center">
                <button class="edit-analyst-btn text-blue-600 hover:text-blue-800 mr-2" title="Editar" data-id="${analista.id}">
                    <i class="fa-solid fa-pen-to-square"></i>
                </button>
                <button class="delete-analyst-btn text-red-600 hover:text-red-800" title="Excluir" data-id="${analista.id}">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </td>
        `;
        if (tableBody) {
            const placeholder = document.getElementById('placeholder-row');
            if (placeholder) placeholder.remove();
            tableBody.appendChild(row);
        }

        // Evento para abrir o modal de confirmação ao clicar no olho
        const viewBtn = row.querySelector('.view-password-btn');
        if (viewBtn) {
            viewBtn.addEventListener('click', function(e) {
                e.preventDefault();
                // Abre modal de confirmação de senha do gestor
                const viewModal = document.getElementById('view-password-modal');
                if (viewModal) {
                    viewModal.classList.remove('hidden');
                }
                // Salva o ID do analista para uso posterior (ex: buscar senha via AJAX)
                viewModal.setAttribute('data-analyst-id', analista.id);
                // Simula salvar a senha do analista (apenas para demo)
                viewModal.setAttribute('data-analyst-password', analista.senha || 'senha_simulada');
            });
        }

        // Lógica do modal de senha do gestor
        const viewModal = document.getElementById('view-password-modal');
        if (viewModal && !viewModal.hasListener) {
            const cancelBtn = document.getElementById('cancel-view-password-btn');
            const form = document.getElementById('view-password-form');
            const passwordInput = document.getElementById('manager-password');

            if (cancelBtn) {
                cancelBtn.addEventListener('click', function() {
                    viewModal.classList.add('hidden');
                    passwordInput.value = '';
                });
            }
            if (form) {
                form.addEventListener('submit', function(e) {
                    e.preventDefault();
                    const senhaGestor = passwordInput.value;
                    const viewModal = document.getElementById('view-password-modal');
                    const analystId = viewModal.getAttribute('data-analyst-id');
                    const emailGestor = 'admin@gmail.com'; // fixo para demo, pode pegar do input se preferir
                    fetch(`/gerenciar_analistas/api/analistas/${analystId}/senha`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email_gestor: emailGestor, senha_gestor: senhaGestor })
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.senha) {
                            alert('Senha do analista: ' + data.senha);
                            viewModal.classList.add('hidden');
                            passwordInput.value = '';
                        } else {
                            alert(data.erro || 'Erro ao obter senha.');
                            passwordInput.value = '';
                        }
                    });
                });
            }
            // Evita múltiplos listeners
            viewModal.hasListener = true;
        }
        // Eventos para editar
        const editBtn = row.querySelector('.edit-analyst-btn');
        if (editBtn) {
            editBtn.addEventListener('click', function(e) {
                e.preventDefault();
                // Preenche modal de edição
                document.getElementById('edit-analyst-name').value = analista.nome;
                document.getElementById('edit-analyst-email').value = analista.email;
                document.getElementById('edit-analyst-modal').classList.remove('hidden');
                // Ao submeter edição
                const editForm = document.getElementById('edit-analyst-form');
                editForm.onsubmit = function(ev) {
                    ev.preventDefault();
                    // Solicita senha do gestor
                    const senhaGestor = prompt('Digite a senha do gestor para confirmar edição:');
                    if (!senhaGestor) return;
                    const nome = document.getElementById('edit-analyst-name').value;
                    const email = document.getElementById('edit-analyst-email').value;
                    const emailGestor = 'admin@gmail.com'; // fixo demo
                    fetch(`/gerenciar_analistas/api/analistas/${analista.id}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ nome, email, email_gestor: emailGestor, senha_gestor: senhaGestor })
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.id) {
                            alert('Analista atualizado!');
                            window.location.reload();
                        } else {
                            alert(data.erro || 'Erro ao atualizar.');
                        }
                    });
                }
            });
        }
        // Evento para excluir
        const deleteBtn = row.querySelector('.delete-analyst-btn');
        if (deleteBtn) {
            deleteBtn.addEventListener('click', function(e) {
                e.preventDefault();
                if (!confirm('Tem certeza que deseja excluir este analista?')) return;
                // Solicita senha do gestor
                const senhaGestor = prompt('Digite a senha do gestor para confirmar exclusão:');
                if (!senhaGestor) return;
                const emailGestor = 'admin@gmail.com'; // fixo demo
                fetch(`/gerenciar_analistas/api/analistas/${analista.id}`, {
                    method: 'DELETE',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email_gestor: emailGestor, senha_gestor: senhaGestor })
                })
                .then(res => {
                    if (res.status === 204) {
                        alert('Analista excluído!');
                        window.location.reload();
                    } else {
                        return res.json().then(data => { alert(data.erro || 'Erro ao excluir.'); });
                    }
                });
            });
        }
    }

    // Carregar analistas ao abrir página
    fetch('/gerenciar_analistas/api/analistas')
        .then(res => res.json())
        .then(analistas => {
            if (analistas && analistas.length > 0) {
                tableBody.innerHTML = '';
                analistas.forEach(addAnalystRow);
            }
        });
});
