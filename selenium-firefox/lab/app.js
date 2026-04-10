function text(id, value) {
    const node = document.getElementById(id);
    if (node) {
        node.textContent = value;
    }
}

function show(id) {
    document.getElementById(id)?.classList.remove('hidden');
}

function hide(id) {
    document.getElementById(id)?.classList.add('hidden');
}

function setupHomePage() {
    const button = document.getElementById('run-home-search');
    const input = document.getElementById('global-search');
    if (!button || !input) {
        return;
    }
    button.addEventListener('click', () => {
        const query = input.value.trim() || 'sin texto';
        text('home-search-result', `Consulta ejecutada: ${query}`);
    });
}

function setupFormsPage() {
    const form = document.getElementById('practice-form');
    const reset = document.getElementById('reset-form');
    if (!form) {
        return;
    }

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const data = new FormData(form);
        const plan = data.get('plan') || 'sin plan';
        const remember = data.get('remember') === 'yes' ? 'sí' : 'no';
        const terms = data.get('terms') === 'yes' ? 'aceptados' : 'pendientes';
        text('result-username', data.get('username') || 'vacío');
        text('result-role', data.get('role') || 'sin rol');
        text('result-country', data.get('country') || 'sin país');
        text('result-plan', plan);
        text('result-bio', data.get('bio') || 'sin bio');
        text('result-remember', remember);
        text('result-terms', terms);
        text('submit-status', 'Formulario enviado correctamente');
        document.getElementById('form-result')?.classList.remove('hidden');
    });

    reset?.addEventListener('click', () => {
        form.reset();
        document.getElementById('form-result')?.classList.add('hidden');
        text('submit-status', 'Esperando envío');
    });
}

function setupWindowsPage() {
    document.getElementById('show-alert')?.addEventListener('click', () => {
        alert('Alerta de laboratorio Selenium');
    });

    document.getElementById('show-confirm')?.addEventListener('click', () => {
        const accepted = confirm('¿Confirmas la operación de prueba?');
        text('dialog-status', accepted ? 'Confirm aceptado' : 'Confirm cancelado');
    });

    document.getElementById('show-prompt')?.addEventListener('click', () => {
        const value = prompt('Escribe un alias de prueba', 'lucentia');
        text('dialog-status', value === null ? 'Prompt cancelado' : `Prompt recibido: ${value}`);
    });

    document.getElementById('open-report-tab')?.addEventListener('click', () => {
        window.open('popup.html?mode=tab', '_blank');
        text('window-status', 'Nueva pestaña solicitada');
    });

    document.getElementById('open-help-window')?.addEventListener('click', () => {
        window.open('popup.html?mode=popup', 'lab-popup', 'width=720,height=520');
        text('window-status', 'Nueva ventana solicitada');
    });
}

function setupActionsPage() {
    const hoverTarget = document.getElementById('hover-target');
    const hoverZone = document.getElementById('hover-zone');
    hoverTarget?.addEventListener('mouseenter', () => hoverZone?.classList.add('force-open'));
    hoverTarget?.addEventListener('mouseleave', () => hoverZone?.classList.remove('force-open'));

    const doubleBox = document.getElementById('double-box');
    let doubleCount = 0;
    doubleBox?.addEventListener('dblclick', () => {
        doubleCount += 1;
        text('double-status', `Doble clic detectado: ${doubleCount}`);
    });

    document.getElementById('context-zone')?.addEventListener('contextmenu', (event) => {
        event.preventDefault();
        text('context-status', 'Click derecho capturado');
    });

    const dragChip = document.getElementById('drag-chip');
    const dropZone = document.getElementById('drop-zone');
    if (dragChip && dropZone) {
        dragChip.addEventListener('dragstart', (event) => {
            event.dataTransfer?.setData('text/plain', 'chip');
            document.body.dataset.dragging = 'true';
        });

        dragChip.addEventListener('mousedown', () => {
            document.body.dataset.dragging = 'true';
        });

        document.addEventListener('mouseup', () => {
            delete document.body.dataset.dragging;
        });

        dropZone.addEventListener('dragover', (event) => event.preventDefault());

        const completeDrop = () => {
            dropZone.classList.add('dropped');
            dropZone.textContent = 'Elemento soltado correctamente';
            text('drop-status', 'Drag and drop completado');
        };

        dropZone.addEventListener('drop', (event) => {
            event.preventDefault();
            completeDrop();
            delete document.body.dataset.dragging;
        });

        dropZone.addEventListener('mouseenter', () => {
            if (document.body.dataset.dragging === 'true') {
                completeDrop();
            }
        });

        dropZone.addEventListener('mouseup', () => {
            if (document.body.dataset.dragging === 'true') {
                completeDrop();
                delete document.body.dataset.dragging;
            }
        });
    }

    document.getElementById('scroll-button')?.addEventListener('click', () => {
        text('scroll-status', 'Objetivo activado tras scroll');
    });
}

function setupWaitsPage() {
    document.getElementById('unlock-button')?.setAttribute('disabled', 'disabled');
    setTimeout(() => {
        document.getElementById('unlock-button')?.removeAttribute('disabled');
        text('unlock-status', 'Botón habilitado');
    }, 2000);

    document.getElementById('load-profile')?.addEventListener('click', () => {
        text('profile-status', 'Cargando perfil...');
        setTimeout(() => {
            const slot = document.getElementById('profile-slot');
            if (slot && !document.getElementById('delayed-profile')) {
                const card = document.createElement('article');
                card.id = 'delayed-profile';
                card.className = 'lab-card';
                card.innerHTML = '<h3>Perfil tardío</h3><p>Este bloque aparece después de una espera explícita.</p>';
                slot.appendChild(card);
            }
            text('profile-status', 'Perfil cargado');
        }, 1400);
    });

    document.getElementById('run-async-search')?.addEventListener('click', () => {
        show('search-spinner');
        hide('result-list');
        text('async-status', 'Buscando resultados...');
        const query = document.getElementById('async-query')?.value || 'consulta';
        setTimeout(() => {
            const resultList = document.getElementById('result-list');
            if (resultList) {
                resultList.innerHTML = '';
                ['primer resultado', 'segundo resultado', 'tercer resultado'].forEach((label, index) => {
                    const item = document.createElement('div');
                    item.className = 'result-item';
                    item.textContent = `${index + 1}. ${label} para ${query}`;
                    resultList.appendChild(item);
                });
            }
            hide('search-spinner');
            show('result-list');
            text('async-status', 'Resultados visibles');
        }, 1200);
    });

    document.getElementById('trigger-toast')?.addEventListener('click', () => {
        setTimeout(() => {
            show('sync-toast');
            text('toast-status', 'Toast visible');
            setTimeout(() => {
                hide('sync-toast');
                text('toast-status', 'Toast oculto');
            }, 1800);
        }, 800);
    });

    document.getElementById('load-orders')?.addEventListener('click', () => {
        text('orders-status', 'Cargando pedidos...');
        setTimeout(() => {
            const tbody = document.getElementById('orders-body');
            if (tbody && !tbody.children.length) {
                [
                    ['ORD-100', 'Pendiente'],
                    ['ORD-200', 'Validado'],
                    ['ORD-300', 'Enviado']
                ].forEach(([code, status]) => {
                    const row = document.createElement('tr');
                    row.innerHTML = `<td>${code}</td><td>${status}</td>`;
                    tbody.appendChild(row);
                });
            }
            text('orders-status', 'Pedidos cargados');
        }, 1600);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const page = document.body.dataset.page;
    if (page === 'home') setupHomePage();
    if (page === 'forms') setupFormsPage();
    if (page === 'windows') setupWindowsPage();
    if (page === 'actions') setupActionsPage();
    if (page === 'waits') setupWaitsPage();
});