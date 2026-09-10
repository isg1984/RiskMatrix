/**
 * RiskMatrix v2.9.1 - Frontend JavaScript
 */

// ========================================
// DOM Elements
// ========================================

const form = document.getElementById('uploadForm');
const matrixFileInput = document.getElementById('matrixFile');
const catalogFileInput = document.getElementById('catalogFile');
const matrixFileName = document.getElementById('matrixFileName');
const catalogFileName = document.getElementById('catalogFileName');
const submitBtn = document.getElementById('submitBtn');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');
const successMessage = document.getElementById('successMessage');
const successStats = document.getElementById('successStats');
const downloadBtn = document.getElementById('downloadBtn');

// ========================================
// File Upload Handlers
// ========================================

matrixFileInput.addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name || 'Nenhum arquivo selecionado';
    matrixFileName.textContent = `✓ ${fileName}`;
    matrixFileName.style.color = e.target.files[0] ? '#059669' : '#6b7280';
    updateFormState();
});

catalogFileInput.addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name || 'Nenhum arquivo selecionado';
    catalogFileName.textContent = `✓ ${fileName}`;
    catalogFileName.style.color = e.target.files[0] ? '#059669' : '#6b7280';
    updateFormState();
});

function updateFormState() {
    const bothFilesSelected = matrixFileInput.files.length > 0 && catalogFileInput.files.length > 0;
    submitBtn.disabled = !bothFilesSelected;
    
    if (bothFilesSelected) {
        submitBtn.style.opacity = '1';
        submitBtn.style.cursor = 'pointer';
    } else {
        submitBtn.style.opacity = '0.6';
        submitBtn.style.cursor = 'not-allowed';
    }
}

// ========================================
// Form Submission
// ========================================

form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Reset previous messages
    hideAllMessages();
    
    // Validação
    if (!matrixFileInput.files[0] || !catalogFileInput.files[0]) {
        showError('Por favor, selecione ambos os arquivos.');
        return;
    }
    
    // Validar tipos de arquivo
    const validExtensions = ['xlsx', 'xls'];
    const matrixExt = matrixFileInput.files[0].name.split('.').pop().toLowerCase();
    const catalogExt = catalogFileInput.files[0].name.split('.').pop().toLowerCase();
    
    if (!validExtensions.includes(matrixExt) || !validExtensions.includes(catalogExt)) {
        showError('Os arquivos devem estar em formato .xlsx ou .xls');
        return;
    }
    
    // Mostrar loading
    showLoading();
    submitBtn.disabled = true;
    
    try {
        // Criar FormData
        const formData = new FormData();
        formData.append('matrix_file', matrixFileInput.files[0]);
        formData.append('catalog_file', catalogFileInput.files[0]);
        
        // Fazer requisição
        const response = await fetch('/api/process', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        hideLoading();
        
        if (!response.ok) {
            showError(data.error || 'Erro ao processar os arquivos.');
            return;
        }
        
        // Sucesso
        showSuccess(data);
        
    } catch (error) {
        hideLoading();
        console.error('Erro:', error);
        showError(`Erro de conexão: ${error.message}`);
    } finally {
        submitBtn.disabled = false;
    }
});

// ========================================
// UI Functions
// ========================================

function hideAllMessages() {
    errorMessage.classList.add('hidden');
    successMessage.classList.add('hidden');
    loading.classList.add('hidden');
}

function showError(message) {
    hideAllMessages();
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showLoading() {
    hideAllMessages();
    loading.classList.remove('hidden');
}

function hideLoading() {
    loading.classList.add('hidden');
}

function showSuccess(data) {
    hideAllMessages();
    
    // Preparar estatísticas
    const stats = data.stats || {};
    const statsHTML = `
        <div class="stat-item">
            <div class="stat-label">Total de Controles</div>
            <div class="stat-value">${stats.total_controls || 0}</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Classificados</div>
            <div class="stat-value">${stats.classified || 0}</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Confiança Média</div>
            <div class="stat-value">${stats.avg_confidence || 'N/A'}</div>
        </div>
    `;
    
    successStats.innerHTML = statsHTML;
    
    // Configurar botão de download
    if (data.download_url) {
        downloadBtn.href = data.download_url;
        downloadBtn.download = data.download_url.split('/').pop();
    }
    
    successMessage.classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ========================================
// Initialization
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // Limpar inputs ao carregar a página
    matrixFileInput.value = '';
    catalogFileInput.value = '';
    updateFormState();
    
    // Adicionar listeners para mudanças de arquivo
    matrixFileInput.addEventListener('change', updateFormState);
    catalogFileInput.addEventListener('change', updateFormState);
    
    console.log('RiskMatrix v2.9.1 - Carregado com sucesso');
});

// ========================================
// Drag & Drop Support (opcional)
// ========================================

const fileInputs = document.querySelectorAll('.file-input');

fileInputs.forEach(input => {
    const container = input.parentElement;
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        container.addEventListener(eventName, preventDefaults, false);
    });
    
    ['dragenter', 'dragover'].forEach(eventName => {
        container.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        container.addEventListener(eventName, unhighlight, false);
    });
    
    container.addEventListener('drop', handleDrop, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    const container = e.target.closest('.form-group');
    if (container) {
        const input = container.querySelector('.file-input');
        input.style.borderColor = '#2563eb';
        input.style.backgroundColor = '#f0f4ff';
    }
}

function unhighlight(e) {
    const container = e.target.closest('.form-group');
    if (container) {
        const input = container.querySelector('.file-input');
        input.style.borderColor = '#e5e7eb';
        input.style.backgroundColor = '#f9fafb';
    }
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    const container = e.target.closest('.form-group');
    
    if (container) {
        const input = container.querySelector('.file-input');
        input.files = files;
        
        // Trigger change event
        const event = new Event('change', { bubbles: true });
        input.dispatchEvent(event);
    }
}
