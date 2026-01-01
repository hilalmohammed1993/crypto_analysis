const API_BASE = '/api/analysis';

const coinInput = document.getElementById('coinInput');
const searchBtn = document.getElementById('searchBtn');

const loading = document.getElementById('loading');
const error = document.getElementById('error');
const dashboard = document.getElementById('dashboard');

// Elements to Populate
const els = {
    symbol: document.getElementById('displaySymbol'),
    price: document.getElementById('displayPrice'),
    trendText: document.getElementById('trendText'),
    trendBadge: document.getElementById('trendBadge'),
    res: document.getElementById('valRes'),
    sup: document.getElementById('valSup'),
    rsiVal: document.getElementById('rsiValue'),
    rsiSig: document.getElementById('rsiSignal'),
    rsiFill: document.getElementById('rsiFill'),
    volCur: document.getElementById('volCur'),
    volAvg: document.getElementById('volAvg'),
    volStatus: document.getElementById('volStatus'),
    sma50: document.getElementById('sma50'),
    sma200: document.getElementById('sma200'),
    newsGrid: document.getElementById('newsGrid')
};

// Chart Global Variable
let myChart = null;

async function analyzeCoin(symbol) {
    if (!symbol) return;

    // UI State
    dashboard.classList.add('hidden');
    error.classList.add('hidden');
    loading.classList.remove('hidden');
    document.getElementById('loadingSymbol').innerText = symbol;

    try {
        const res = await fetch(`${API_BASE}/${symbol}`);
        if (!res.ok) throw new Error('Failed to fetch data');
        const data = await res.json();

        renderDashboard(data);

        loading.classList.add('hidden');
        dashboard.classList.remove('hidden');

    } catch (err) {
        loading.classList.add('hidden');
        error.classList.remove('hidden');
        document.getElementById('errorMessage').innerText = err.message || "Failed to analyze coin";
    }
}

function renderDashboard(data) {
    const market = data.market_analysis;
    const news = data.news;

    // Header
    els.symbol.innerText = data.symbol;
    els.price.innerText = formatMoney(market.price);

    // Trend
    const trendText = market.trend.status;
    els.trendText.innerText = trendText;

    let trendColor = 'var(--text-muted)';
    if (trendText.includes('Bullish')) trendColor = 'var(--success)';
    if (trendText.includes('Bearish')) trendColor = 'var(--danger)';
    els.trendBadge.style.color = trendColor;
    els.trendBadge.style.borderColor = trendColor;

    // Support/Res
    els.res.innerText = formatMoney(market.support_resistance.resistance);
    els.sup.innerText = formatMoney(market.support_resistance.support);

    // RSI
    const rsi = market.indicators.rsi.value;
    els.rsiVal.innerText = rsi.toFixed(1);
    els.rsiSig.innerText = market.indicators.rsi.signal;
    els.rsiFill.style.width = `${rsi}%`;

    if (rsi > 70) els.rsiFill.style.backgroundColor = 'var(--danger)';
    else if (rsi < 30) els.rsiFill.style.backgroundColor = 'var(--success)';
    else els.rsiFill.style.backgroundColor = 'var(--primary)';

    // Volume
    els.volCur.innerText = formatNumber(market.indicators.volume.current);
    els.volAvg.innerText = formatNumber(market.indicators.volume.sma);
    els.volStatus.innerText = market.indicators.volume.status;

    // Moving Averages
    els.sma50.innerText = formatMoney(market.trend.sma50);
    els.sma200.innerText = formatMoney(market.trend.sma200);

    // --- CHART RENDERING ---
    if (market.history) {
        renderChart(market.history, market.support_resistance.support, market.support_resistance.resistance);
    }

    // News
    els.newsGrid.innerHTML = '';
    news.forEach(item => {
        const sentimentClass = item.sentiment.toLowerCase(); // positive, negative, neutral
        const card = document.createElement('a');
        card.className = `news-card ${sentimentClass}`;
        card.href = item.link;
        card.target = '_blank';

        card.innerHTML = `
            <h4>${item.title}</h4>
            <div class="news-meta">
                <span>${new Date(item.pub_date).toLocaleDateString()}</span>
                <span>${item.sentiment}</span>
            </div>
        `;
        els.newsGrid.appendChild(card);
    });
}

function renderChart(history, support, resistance) {
    const ctx = document.getElementById('priceChart').getContext('2d');

    if (myChart) {
        myChart.destroy();
    }

    const labels = history.map(h => h.date);
    const prices = history.map(h => h.price);

    // Constant lines for S/R
    const supportLine = Array(labels.length).fill(support);
    const resistanceLine = Array(labels.length).fill(resistance);

    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Price',
                    data: prices,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 2,
                    tension: 0.1,
                    fill: {
                        target: 'origin',
                        above: 'rgba(59, 130, 246, 0.1)'
                    },
                    pointRadius: 0
                },
                {
                    label: 'Resistance',
                    data: resistanceLine,
                    borderColor: '#ef4444',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: false
                },
                {
                    label: 'Support',
                    data: supportLine,
                    borderColor: '#10b981',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index',
            },
            plugins: {
                legend: {
                    labels: { color: '#94a3b8' }
                }
            },
            scales: {
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8', maxTicksLimit: 10 }
                }
            }
        }
    });
}

// Helpers
function formatMoney(num) {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(num);
}

function formatNumber(num) {
    return new Intl.NumberFormat('en-US', { notation: "compact", compactDisplay: "short" }).format(num);
}

// Event Listeners
searchBtn.addEventListener('click', () => {
    analyzeCoin(coinInput.value);
});

coinInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') analyzeCoin(coinInput.value);
});

// Initial Load
analyzeCoin(coinInput.value);
