const snippetCache = new Map();

function escapeHtml(text) {
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

async function fetchSnippet(filePath) {
    if (snippetCache.has(filePath)) {
        return snippetCache.get(filePath);
    }
    const embeddedSnippetFile = window.COURSE_SNIPPET_FILES?.[filePath];
    if (embeddedSnippetFile) {
        snippetCache.set(filePath, embeddedSnippetFile);
        return embeddedSnippetFile;
    }
    const response = await fetch(filePath);
    if (!response.ok) {
        throw new Error(`No se pudo cargar ${filePath}`);
    }
    const text = await response.text();
    snippetCache.set(filePath, text);
    return text;
}

function extractSnippet(fileText, snippetName) {
    const startMarker = `# --- EXAMPLE START: ${snippetName} ---`;
    const endMarker = `# --- EXAMPLE END: ${snippetName} ---`;
    const startIndex = fileText.indexOf(startMarker);
    const endIndex = fileText.indexOf(endMarker);

    if (startIndex === -1 || endIndex === -1 || endIndex <= startIndex) {
        throw new Error(`No se encontró el snippet ${snippetName}`);
    }

    return fileText
        .slice(startIndex + startMarker.length, endIndex)
        .replace(/^\n+/, '')
        .replace(/\n+$/, '');
}

async function loadCodeExamples() {
    const examples = document.querySelectorAll('[data-snippet-file]');
    for (const block of examples) {
        const filePath = block.dataset.snippetFile;
        const snippetName = block.dataset.snippetName;
        const pre = block.querySelector('pre code');
        const placeholder = block.querySelector('.code-placeholder');

        try {
            const fileText = await fetchSnippet(filePath);
            const snippet = extractSnippet(fileText, snippetName);
            pre.innerHTML = escapeHtml(snippet);
            if (placeholder) {
                placeholder.remove();
            }
        } catch (error) {
            if (placeholder) {
                placeholder.textContent = `${error.message}. Si abriste el HTML directamente desde disco, usa los snippets embebidos o sirve la carpeta con python -m http.server 8765.`;
                placeholder.classList.add('error');
            }
        }
    }
}

function setupCopyButtons() {
    document.querySelectorAll('.copy-btn').forEach((button) => {
        button.addEventListener('click', async () => {
            const code = button.closest('.code-block').querySelector('pre').innerText;
            await navigator.clipboard.writeText(code);
            button.textContent = 'Copiado';
            button.classList.add('copied');
            setTimeout(() => {
                button.textContent = 'Copiar';
                button.classList.remove('copied');
            }, 1800);
        });
    });
}

function setupMobileNav() {
    const toggle = document.getElementById('courseNavToggle');
    const links = document.getElementById('courseNavLinks');
    if (!toggle || !links) {
        return;
    }
    toggle.addEventListener('click', () => links.classList.toggle('open'));
}

document.addEventListener('DOMContentLoaded', async () => {
    setupMobileNav();
    setupCopyButtons();
    await loadCodeExamples();
});