const textarea = document.getElementById('input-text');
const charCount = document.getElementById('char-count');
const analyzeBtn = document.getElementById('analyze-btn');
const errorSection = document.getElementById('error-section');
const errorMessage = document.getElementById('error-message');
const resultsSection = document.getElementById('results-section');
const assumptionCount = document.getElementById('assumption-count');
const summary = document.getElementById('summary');
const assumptionsList = document.getElementById('assumptions-list');
const exampleCards = document.querySelectorAll('.example-card');

textarea.addEventListener('input', () => {
    charCount.textContent = textarea.value.length;
});

analyzeBtn.addEventListener('click', analyze);

textarea.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        analyze();
    }
});

exampleCards.forEach(card => {
    card.addEventListener('click', () => {
        textarea.value = card.dataset.text;
        charCount.textContent = textarea.value.length;
        textarea.focus();
    });
});

async function analyze() {
    const text = textarea.value.trim();
    
    if (text.length < 10) {
        showError('Please enter at least 10 characters to analyze.');
        return;
    }
    
    hideError();
    hideResults();
    setLoading(true);
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Analysis failed. Please try again.');
        }
        
        showResults(data);
    } catch (err) {
        showError(err.message || 'Something went wrong. Please try again.');
    } finally {
        setLoading(false);
    }
}

function setLoading(loading) {
    analyzeBtn.disabled = loading;
    analyzeBtn.classList.toggle('loading', loading);
}

function showError(message) {
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');
}

function hideError() {
    errorSection.classList.add('hidden');
}

function hideResults() {
    resultsSection.classList.add('hidden');
}

function showResults(data) {
    const count = data.assumptions.length;
    assumptionCount.textContent = `${count} assumption${count !== 1 ? 's' : ''} found`;
    
    summary.textContent = data.summary || 'Analysis complete.';
    
    assumptionsList.innerHTML = data.assumptions.map(a => createAssumptionCard(a)).join('');
    
    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function createAssumptionCard(assumption) {
    const confidencePercent = Math.round(assumption.confidence * 100);
    
    return `
        <div class="assumption-card">
            <div class="assumption-header">
                <span class="assumption-text">${escapeHtml(assumption.text)}</span>
                <span class="risk-badge ${assumption.risk}">${assumption.risk}</span>
            </div>
            <div class="assumption-meta">
                <div class="confidence">
                    <span>Confidence</span>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: ${confidencePercent}%"></div>
                    </div>
                    <span>${confidencePercent}%</span>
                </div>
            </div>
            <div class="assumption-details">
                <p><strong>Why it matters:</strong> ${escapeHtml(assumption.explanation)}</p>
                <p><strong>How to validate:</strong> ${escapeHtml(assumption.validation)}</p>
            </div>
        </div>
    `;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
