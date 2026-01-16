/**
 * Logic for No No Fake News Popup
 */

const API_BASE = "http://127.0.0.1:8000";
const API_KEY = "nnfn_dev_key";

document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyzeBtn');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', startAnalysis);
    }
    
    // Auto-start analysis if possible? 
    // For now, let's keep it manual but we could trigger it on open.
});

async function startAnalysis() {
    const initialState = document.getElementById('initialState');
    const loader = document.getElementById('loader');
    const resultView = document.getElementById('resultView');

    // UI Transition
    if (initialState) initialState.classList.add('hidden');
    if (loader) loader.classList.remove('hidden');
    if (resultView) resultView.classList.add('hidden');

    try {
        // 1. Get current tab URL
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (!tab || !tab.url) {
            throw new Error("Impossible de récupérer l'URL de l'onglet actif.");
        }

        const url = tab.url;

        // 2. Call API
        const response = await fetch(`${API_BASE}/api/analyze?api_key=${API_KEY}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': API_KEY
            },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            throw new Error(`Erreur API (${response.status})`);
        }

        const data = await response.json();

        // 3. Display Results
        displayResults(data);

    } catch (error) {
        console.error("Analysis failed:", error);
        alert(error instanceof Error ? error.message : String(error));
        if (loader) loader.classList.add('hidden');
        if (initialState) initialState.classList.remove('hidden');
    }
}

/**
 * @param {any} data
 */
function displayResults(data) {
    const loader = document.getElementById('loader');
    const resultView = document.getElementById('resultView');
    const scoreValue = document.getElementById('scoreValue');
    const progressCircle = document.getElementById('scoreProgress');
    const verdictBadge = document.getElementById('verdictBadge');
    const titleEl = document.getElementById('articleTitle');
    const messageEl = document.getElementById('verdictMessage');
    const fullReportBtn = document.getElementById('fullReportBtn');

    if (loader) loader.classList.add('hidden');
    if (resultView) resultView.classList.remove('hidden');

    if (scoreValue) scoreValue.textContent = (data.score || 0).toString();
    
    if (titleEl) titleEl.textContent = data.title || "Article analysé";
    if (messageEl) messageEl.textContent = data.verdict?.message || "";

    const color = data.verdict?.color || "#3b82f6";

    if (progressCircle && progressCircle instanceof SVGElement) {
        const offset = 283 - ((data.score || 0) / 100) * 283;
        progressCircle.style.strokeDashoffset = offset.toString();
        progressCircle.style.stroke = color;
    }

    if (verdictBadge) {
        verdictBadge.textContent = data.verdict?.label || "Analyse";
        verdictBadge.style.backgroundColor = `${color}15`;
        verdictBadge.style.color = color;
        verdictBadge.style.borderColor = `${color}30`;
    }

    if (fullReportBtn && fullReportBtn instanceof HTMLAnchorElement) {
        // Deep link to our web app if needed, or just the URL
        fullReportBtn.href = `${API_BASE}/#analysis-${data.id || ''}`;
    }
}
