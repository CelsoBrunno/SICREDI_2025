// JS para listar e aprovar/recusar reservas de equipamentos mobilizados

document.addEventListener('DOMContentLoaded', carregarReservas);

async function carregarReservas() {
    const tbody = document.getElementById('reservas-table-body');
    tbody.innerHTML = `<tr><td colspan="6" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center">Carregando reservas...</td></tr>`;
    try {
        const res = await fetch('/gestao_equipamentos/gestor/api/reservas');
        const reservas = await res.json();
        if (!reservas.length) {
            tbody.innerHTML = `<tr><td colspan="6" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center">Nenhuma reserva encontrada.</td></tr>`;
            return;
        }
        tbody.innerHTML = '';
        reservas.forEach(r => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap text-sm">${r.equipamento_nome}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">${r.analista_nome}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">${formatarData(r.data_inicio_reserva)}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">${formatarData(r.data_fim_reserva)}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">${formatarStatus(r.status)}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                    ${gerarAcoes(r)}
                </td>
            `;
            tbody.appendChild(tr);
        });
        adicionarListenersAprovacao();
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="6" class="px-6 py-4 text-center text-red-600">Erro ao carregar reservas.</td></tr>`;
    }
}

function formatarData(dt) {
    if (!dt) return '';
    return new Date(dt).toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' });
}

function formatarStatus(status) {
    if (status === 'em_analise') return '<span class="text-yellow-600">Em análise</span>';
    if (status === 'aprovada') return '<span class="text-green-700">Aprovada</span>';
    if (status === 'recusada') return '<span class="text-red-700">Recusada</span>';
    return status;
}

function gerarAcoes(reserva) {
    if (reserva.status === 'em_analise') {
        return `
            <button class="aprovar-btn bg-green-500 hover:bg-green-700 text-white px-2 py-1 rounded mr-2" data-id="${reserva.id}">Aprovar</button>
            <button class="recusar-btn bg-red-500 hover:bg-red-700 text-white px-2 py-1 rounded" data-id="${reserva.id}">Recusar</button>
        `;
    }
    return '-';
}

function adicionarListenersAprovacao() {
    document.querySelectorAll('.aprovar-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const id = btn.getAttribute('data-id');
            await atualizarStatusReserva(id, 'aprovada');
        });
    });
    document.querySelectorAll('.recusar-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const id = btn.getAttribute('data-id');
            await atualizarStatusReserva(id, 'recusada');
        });
    });
}

async function atualizarStatusReserva(id, status) {
    try {
        const res = await fetch(`/gestao_equipamentos/gestor/api/reservas/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status })
        });
        if (res.ok) {
            await carregarReservas();
        } else {
            alert('Erro ao atualizar status da reserva.');
        }
    } catch {
        alert('Erro ao atualizar status da reserva.');
    }
}
