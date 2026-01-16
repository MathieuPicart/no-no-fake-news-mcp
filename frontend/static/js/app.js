async function analyzeUrl() {
    const input = document.getElementById('urlInput');
    const url = input.value.trim();
    if (!url) return;

    // UI Loading State
    const btn = document.getElementById('analyzeBtn');
    const btnText = document.getElementById('btnText');
    const spinner = document.getElementById('btnSpinner');
    const results = document.getElementById('results');
    const emptyState = document.getElementById('emptyState');
    const skeletonLoader = document.getElementById('skeletonLoader');

    btn.disabled = true;
    btnText.style.display = 'none';
    spinner.style.display = 'block';
    btn.classList.remove('pulse');
    
    // Show Skeletons, Hide Results & Empty State
    results.classList.add('hidden');
    results.classList.remove('visible');
    if (emptyState) emptyState.classList.add('hidden');
    if (skeletonLoader) {
        skeletonLoader.classList.remove('hidden');
        skeletonLoader.classList.add('visible');
    }

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            throw new Error('Analysis failed');
        }

        const data = await response.json();
        
        // Hide Skeleton and Display Results
        if (skeletonLoader) {
            skeletonLoader.classList.add('hidden');
            skeletonLoader.classList.remove('visible');
        }
        
        displayResults(data);
        loadHistory(); 

    } catch (error) {
        alert('Error: ' + error.message);
        if (emptyState && !results.classList.contains('visible')) {
            emptyState.classList.remove('hidden');
        }
    } finally {
        btn.disabled = false;
        btnText.style.display = 'block';
        spinner.style.display = 'none';
    }
}

function displayResults(data) {
    const results = document.getElementById('results');
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
    
    if (container && progressCircle) {
        const scoreColor = data.verdict.color || '#3b82f6';
        
        // Apply color to container for CSS variables and to circle explicitly
        container.style.setProperty('--accent', scoreColor);
        progressCircle.style.stroke = scoreColor;

        // Reset animation state
        progressCircle.style.transition = 'none';
        progressCircle.style.strokeDashoffset = '283';
        
        // Force reflow and start animation in next frames
        requestAnimationFrame(() => {
            progressCircle.getBoundingClientRect();
            requestAnimationFrame(() => {
                progressCircle.style.transition = 'stroke-dashoffset 1.5s cubic-bezier(0.34, 1.56, 0.64, 1)';
                const offset = 283 - (data.score / 100) * 283;
                progressCircle.style.strokeDashoffset = offset.toString();
            });
        });
    }

    // Animate Number
    if (scoreVal) {
        animateValue(scoreVal, 0, data.score, 1200);
    }

    // Verdict Badge
    const badge = document.getElementById('verdictBadge');
    if (badge) {
        const color = data.verdict.color || '#3b82f6';
        badge.textContent = data.verdict.label || data.verdict.badge || 'Analyse';
        badge.style.backgroundColor = `${color}15`;
        badge.style.color = color;
        badge.style.borderColor = `${color}40`;
    }
    
    document.getElementById('verdictMessage').textContent = data.verdict.message;
    document.getElementById('sourceNameDisplay').textContent = data.details.source.name || 'Inconnue';
    const sourceLink = document.getElementById('sourceLink');
    if (sourceLink) {
        sourceLink.href = data.url;
    }

    // Metrics - Linguistic
    // Emotivity: 0 bad (too emotional), 10 good (neutral). 
    // Bar should reflect "goodness". So if 10/10, fill 100%.
    const emotivityPct = (data.details.linguistic.emotivity / 10) * 100;
    document.getElementById('emotivityBar').style.width = `${emotivityPct}%`;
    document.getElementById('emotivityBar').style.backgroundColor = getColorForMetric(emotivityPct);

    const clickbaitPct = (data.details.linguistic.clickbait / 10) * 100;
    document.getElementById('clickbaitBar').style.width = `${clickbaitPct}%`;
    document.getElementById('clickbaitBar').style.backgroundColor = getColorForMetric(clickbaitPct);
    
    document.getElementById('sentimentLabel').textContent = data.details.linguistic.sentiment;
    document.getElementById('clickbaitScoreDisplay').textContent = `${data.details.linguistic.clickbait}/10`;

    // Metrics - Source
    // Domain: 0-15. Author: 0-10.
    const domainPct = (data.details.source.domain_score / 15) * 100;
    document.getElementById('domainBar').style.width = `${domainPct}%`;
    document.getElementById('domainBar').style.backgroundColor = getColorForMetric(domainPct);
    
    const authorPct = (data.details.source.author_score / 10) * 100;
    document.getElementById('authorBar').style.width = `${authorPct}%`;
    document.getElementById('authorBar').style.backgroundColor = getColorForMetric(authorPct);

    // Metrics - Propagation (Max 20 pts)
    const propPct = (data.details.propagation.score / 20) * 100;
    document.getElementById('propagationBar').style.width = `${propPct}%`;
    document.getElementById('propagationBar').style.backgroundColor = getColorForMetric(propPct);
    document.getElementById('propagationCountDisplay').textContent = `${data.details.propagation.count} articles trouvés`;
    
    const propSources = document.getElementById('propagationSources');
    if (data.details.propagation.sources && data.details.propagation.sources.length > 0) {
        propSources.innerHTML = '<h4>Relayé par :</h4><ul>' + 
            data.details.propagation.sources.map(s => `<li>${s}</li>`).join('') + 
            '</ul>';
    } else {
        propSources.innerHTML = '<p class="loading-text">Aucune autre source majeure détectée par NewsAPI.</p>';
    }

    // Entities (NLP)
    const entitiesList = document.getElementById('entitiesList');
    if (data.entities && data.entities.length > 0) {
        // Filter unique entities to avoid duplicates
        const uniqueEntities = Array.from(new Set(data.entities.map(e => `${e.text}|${e.label}`)))
            .map(s => {
                const [text, label] = s.split('|');
                return { text, label };
            });

        entitiesList.innerHTML = uniqueEntities.map(ent => `
            <span class="entity-tag ${ent.label.toLowerCase()}" title="${ent.label}">
                ${ent.text}
            </span>
        `).join('');
    } else {
        entitiesList.innerHTML = '<p class="loading-text">Aucun sujet spécifique identifié.</p>';
    }
}

function getColorForMetric(pct) {
    if (pct < 40) return '#ef4444';
    if (pct < 70) return '#f59e0b';
    return '#10b981';
}

function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

async function loadHistory() {
    console.log("Loading history...");
    try {
        const response = await fetch('/api/history');
        if (!response.ok) throw new Error('Failed to fetch history');
        const data = await response.json();
        console.log("History data received:", data);
        displayHistory(data);
    } catch (error) {
        console.error('Error loading history:', error);
        const list = document.getElementById('historyList');
        if (list) list.innerHTML = `<div class="loading-text" style="color: var(--score-red)">Erreur de chargement de l'historique : ${error.message}</div>`;
    }
}

function displayHistory(items) {
    const list = document.getElementById('historyList');
    if (items.length === 0) {
        list.innerHTML = '<div class="loading-text">Aucune analyse pour le moment.</div>';
        return;
    }

    list.innerHTML = items.map(item => `
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
                <span class="h-badge">${item.verdict.badge}</span>
                <span class="h-score" style="color: ${getColorForMetric(item.score)}">${item.score}/100</span>
            </div>
        </div>
    `).join('');
}

async function loadSingleAnalysis(id) {
    try {
        const response = await fetch(`/api/analysis/${id}`);
        const data = await response.json();
        displayResults(data);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (error) {
        alert('Error loading analysis: ' + error.message);
    }
}

// Bind enter key
document.getElementById('urlInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        analyzeUrl();
    }
});

// Dynamic pulse for analyze button
document.getElementById('urlInput').addEventListener('input', function(e) {
    const btn = document.getElementById('analyzeBtn');
    if (e.target.value.trim().length > 5) {
        btn.classList.add('pulse');
    } else {
        btn.classList.remove('pulse');
    }
});

// Paste what's in the clipboard to the input
function pasteFromClipboard() {
    const input = document.getElementById('urlInput');
    navigator.clipboard.readText().then(text => {
        if (text) input.value = text;
    });
}

// Initial load
loadHistory();