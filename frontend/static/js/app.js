/**
 * FRONTEND JS for No No Fake News
 * Robust and clean implementation
 */

async function analyzeUrl() {
    const input = document.getElementById('urlInput');
    if (!input || !(input instanceof HTMLInputElement)) return;
    
    const url = input.value.trim();
    if (!url) return;

    // UI Loading State Elements
    const btn = document.getElementById('analyzeBtn');
    const btnText = document.getElementById('btnText');
    const spinner = document.getElementById('btnSpinner');
    const results = document.getElementById('results');
    const emptyState = document.getElementById('emptyState');
    const skeletonLoader = document.getElementById('skeletonLoader');

    // Safe UI state update
    if (btn) {
        if (btn instanceof HTMLButtonElement) btn.disabled = true;
        btn.classList.remove('pulse');
    }
    if (btnText) btnText.style.display = 'none';
    if (spinner) spinner.style.display = 'block';
    
    // Show Skeletons, Hide Results & Empty State
    if (results) {
        results.classList.add('hidden');
        results.classList.remove('visible');
    }
    if (emptyState) emptyState.classList.add('hidden');
    if (skeletonLoader) {
        skeletonLoader.classList.remove('hidden');
        skeletonLoader.classList.add('visible');
    }

    try {
        const apiKey = 'nnfn_dev_key';
        const response = await fetch(`/api/analyze?api_key=${apiKey}`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-API-Key': apiKey
            },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            if (response.status === 401 || response.status === 403) {
                throw new Error('Problème d\'authentification (Clé API). Essayez de rafraîchir la page (Cmd+R).');
            }
            throw new Error(`Analyse échouée (Code ${response.status})`);
        }

        const data = await response.json();
        
        // Hide Skeleton
        if (skeletonLoader) {
            skeletonLoader.classList.add('hidden');
            skeletonLoader.classList.remove('visible');
        }
        
        displayResults(data);
        loadHistory(); 

    } catch (error) {
        const msg = error instanceof Error ? error.message : String(error);
        alert('Error: ' + msg);
        if (emptyState && results && !results.classList.contains('visible')) {
            emptyState.classList.remove('hidden');
        }
    } finally {
        if (btn) {
            if (btn instanceof HTMLButtonElement) btn.disabled = false;
        }
        if (btnText) btnText.style.display = 'block';
        if (spinner) spinner.style.display = 'none';
    }
}

function displayResults(data) {
    const results = document.getElementById('results');
    if (!results) return;

    results.classList.remove('hidden');
    results.classList.add('visible');

    // Apply staggered animation to cards
    const cards = results.querySelectorAll('.detail-card');
    cards.forEach((card, index) => {
        card.className = 'detail-card'; // Reset
        card.classList.add(`stagger-${(index % 4) + 1}`);
    });

    // Score & SVG Progress
    const scoreVal = results.querySelector('#scoreValue');
    const container = results.querySelector('.score-circle-container');
    const progressCircle = results.querySelector('#scoreProgress');
    
    if (container && progressCircle && container instanceof HTMLElement && progressCircle instanceof SVGElement) {
        const scoreColor = data.verdict?.color || '#3b82f6';
        
        container.style.setProperty('--accent', scoreColor);
        // progressCircle is an SVGElement, it has a style property in modern browsers
        const circleStyle = progressCircle.style;
        circleStyle.stroke = scoreColor;

        // Reset animation state
        circleStyle.transition = 'none';
        circleStyle.strokeDashoffset = '283';
        
        // Force reflow and start animation in next frames
        requestAnimationFrame(() => {
            progressCircle.getBoundingClientRect();
            requestAnimationFrame(() => {
                circleStyle.transition = 'stroke-dashoffset 1.5s cubic-bezier(0.34, 1.56, 0.64, 1)';
                const offset = 283 - (data.score / 100) * 283;
                circleStyle.strokeDashoffset = offset.toString();
            });
        });
    }

    // Animate Number
    if (scoreVal) {
        animateValue(scoreVal, 0, data.score || 0, 1200);
    }

    // Verdict Badge
    const badge = document.getElementById('verdictBadge');
    if (badge) {
        const color = data.verdict?.color || '#3b82f6';
        badge.textContent = data.verdict?.label || data.verdict?.badge || 'Analyse';
        badge.style.backgroundColor = `${color}15`;
        badge.style.color = color;
        badge.style.borderColor = `${color}40`;
    }
    
    const verdictMsg = document.getElementById('verdictMessage');
    if (verdictMsg) verdictMsg.textContent = data.verdict?.message || '';

    // Safely access nested details
    const det = data.details || {};
    const src = det.source || {};
    const ling = det.linguistic || {};
    const prop = det.propagation || {};

    const srcDisplay = document.getElementById('sourceNameDisplay');
    if (srcDisplay) srcDisplay.textContent = src.name || 'Inconnue';

    const sourceLink = document.getElementById('sourceLink');
    if (sourceLink && sourceLink instanceof HTMLAnchorElement) {
        sourceLink.href = data.url || '#';
    }

    // Metrics - Linguistic
    const emotivityPct = ((ling.emotivity || 0) / 10) * 100;
    const emotivityBar = document.getElementById('emotivityBar');
    if (emotivityBar) {
        emotivityBar.style.width = `${emotivityPct}%`;
        emotivityBar.style.backgroundColor = getColorForMetric(emotivityPct);
    }

    const clickbaitPct = ((ling.clickbait || 0) / 10) * 100;
    const clickbaitBar = document.getElementById('clickbaitBar');
    if (clickbaitBar) {
        clickbaitBar.style.width = `${clickbaitPct}%`;
        clickbaitBar.style.backgroundColor = getColorForMetric(clickbaitPct);
    }
    
    const sentimentLabel = document.getElementById('sentimentLabel');
    if (sentimentLabel) sentimentLabel.textContent = ling.sentiment || '-';

    const clickbaitDisplay = document.getElementById('clickbaitScoreDisplay');
    if (clickbaitDisplay) clickbaitDisplay.textContent = `${ling.clickbait || 0}/10`;

    // Metrics - Source
    const domainPct = ((src.domain_score || 0) / 15) * 100;
    const domainBar = document.getElementById('domainBar');
    if (domainBar) {
        domainBar.style.width = `${domainPct}%`;
        domainBar.style.backgroundColor = getColorForMetric(domainPct);
    }
    
    const authorPct = ((src.author_score || 0) / 10) * 100;
    const authorBar = document.getElementById('authorBar');
    const authorName = document.getElementById('authorName');
    
    if (authorBar) {
        authorBar.style.width = `${authorPct}%`;
        authorBar.style.backgroundColor = getColorForMetric(authorPct);
    }
    
    if (authorName) {
        authorName.textContent = src.author_name || 'Non identifié';
    }

    // Metrics - Propagation
    const propPct = ((prop.score || 0) / 20) * 100;
    const propBar = document.getElementById('propagationBar');
    if (propBar) {
        propBar.style.width = `${propPct}%`;
        propBar.style.backgroundColor = getColorForMetric(propPct);
    }
    const propCountDisplay = document.getElementById('propagationCountDisplay');
    if (propCountDisplay) propCountDisplay.textContent = `${prop.count || 0} articles trouvés`;
    
    const propSources = document.getElementById('propagationSources');
    if (propSources) {
        if (prop.sources && prop.sources.length > 0) {
            propSources.innerHTML = prop.sources.map((/** @type {any} */ s) => {
                const name = typeof s === 'string' ? s : (s.name || 'Source');
                const date = (s.date ? new Date(s.date).toLocaleDateString() : '');
                return `
                    <div class="prop-source-item">
                        <span class="prop-source-name">${name}</span>
                        <span class="prop-source-date">${date}</span>
                    </div>
                `;
            }).join('');
        } else {
            propSources.innerHTML = '<p class="small-text">Aucune propagation détectée hors source originale.</p>';
        }
    }

    // Entities (NLP)
    const entitiesList = document.getElementById('entitiesList');
    if (entitiesList) {
        const entities = data.entities || [];
        if (entities.length > 0) {
            const seen = new Set();
            const unique = entities.filter((/** @type {any} */ e) => {
                const key = `${e.text}|${e.label}`.toLowerCase();
                if (seen.has(key)) return false;
                seen.add(key);
                return true;
            });

            entitiesList.innerHTML = unique.map((/** @type {any} */ e) => `
                <span class="entity-tag ${e.label?.toLowerCase() || 'misc'}" title="${e.label || ''}">
                    ${e.text}
                </span>
            `).join('');
        } else {
            entitiesList.innerHTML = '<p class="small-text">Aucun sujet spécifique identifié.</p>';
        }
    }
}

function getColorForMetric(pct) {
    if (pct < 40) return '#ef4444';
    if (pct < 70) return '#f59e0b';
    return '#10b981';
}

function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
/**
 * @param {number} timestamp
 */
const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    obj.innerHTML = Math.floor(progress * (end - start) + start).toString();
    if (progress < 1) {
        window.requestAnimationFrame(step);
    }
};
    window.requestAnimationFrame(step);
}

async function loadHistory() {
    try {
        const apiKey = 'nnfn_dev_key';
        const response = await fetch(`/api/history?api_key=${apiKey}`, {
            headers: { 'X-API-Key': apiKey }
        });
        if (!response.ok) throw new Error('Failed to fetch history');
        const data = await response.json();
        displayHistory(data);
    } catch (error) {
        console.error('Error loading history:', error);
        const list = document.getElementById('historyList');
        const msg = error instanceof Error ? error.message : String(error);
        if (list) {
            list.innerHTML = `<div class="loading-text" style="color: var(--score-red)">Erreur de chargement de l'historique : ${msg}</div>`;
        }
    }
}

function displayHistory(items) {
    const list = document.getElementById('historyList');
    if (!list) return;

    if (!items || items.length === 0) {
        list.innerHTML = '<div class="loading-text">Aucune analyse pour le moment.</div>';
        return;
    }

    list.innerHTML = items.map(item => {
        const color = item.verdict?.color || getColorForMetric(item.score || 0);
        return `
            <div class="history-item" onclick="loadSingleAnalysis(${item.id})">
                <div class="history-item-header">
                    <div>
                        <div class="item-source">${item.source_name || 'Source Inconnue'}</div>
                        <h4>${item.title || item.url}</h4>
                    </div>
                    <a href="${item.url}" target="_blank" class="external-link" onclick="event.stopPropagation()" title="Ouvrir l'article original">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                    </a>
                </div>
                <div class="h-meta">
                    <span class="h-badge" style="color: ${color}; background: ${color}15; border: 1px solid ${color}30; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem;">
                        ${item.verdict?.badge || 'Analyse'}
                    </span>
                    <span class="h-score" style="color: ${color}">
                        ${item.score}/100
                    </span>
                </div>
            </div>
        `;
    }).join('');
}

async function loadSingleAnalysis(id) {
    try {
        const apiKey = 'nnfn_dev_key';
        const response = await fetch(`/api/analysis/${id}?api_key=${apiKey}`, {
            headers: { 'X-API-Key': apiKey }
        });
        if (!response.ok) throw new Error('Failed to fetch analysis details');
        const data = await response.json();
        displayResults(data);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (error) {
        const msg = error instanceof Error ? error.message : String(error);
        console.error('Error loading analysis:', error);
        alert('Error loading analysis: ' + msg);
    }
}

// Bind enter key
const urlInput = document.getElementById('urlInput');
if (urlInput) {
    /**
 * @param {KeyboardEvent} e
 */
urlInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        analyzeUrl();
    }
});

/**
 * @param {Event} e
 */
urlInput.addEventListener('input', function(e) {
    const target = e.target;
    if (target instanceof HTMLInputElement) {
        const btn = document.getElementById('analyzeBtn');
        if (btn) {
            if (target.value.trim().length > 5) {
                btn.classList.add('pulse');
            } else {
                btn.classList.remove('pulse');
            }
        }
    }
});
}

// Paste what's in the clipboard to the input
function pasteFromClipboard() {
    const input = document.getElementById('urlInput');
    if (input && input instanceof HTMLInputElement) {
        navigator.clipboard.readText().then(text => {
            if (text) input.value = text;
        }).catch(err => {
            console.error('Failed to read clipboard:', err);
        });
    }
}

// Initial load
document.addEventListener('DOMContentLoaded', () => {
    loadHistory();

    // Check for hash routing (e.g. #analysis-123)
    const hash = window.location.hash;
    if (hash && hash.startsWith('#analysis-')) {
        const id = hash.replace('#analysis-', '');
        if (id) {
            setTimeout(() => {
                loadSingleAnalysis(id);
            }, 300);
        }
    }
});