/**
 * 台股均線糾結篩選器 - 主應用程式
 */

const App = {
    state: {
        stocks: [],
        selectedStock: null,
        selectedDays: 120,
        selectedInterval: '1d',
        isLoading: false,
    },

    elements: {},

    init() {
        this.cacheElements();
        this.bindEvents();
        this.updateSliderValues();
        ChartManager.init('chartContainer');
        console.log('App initialized');
    },

    cacheElements() {
        this.elements = {
            screenBtn: document.getElementById('screenBtn'),
            refreshBtn: document.getElementById('refreshBtn'),
            stockList: document.getElementById('stockList'),
            resultCount: document.getElementById('resultCount'),
            chartStockName: document.getElementById('chartStockName'),
            chartStockCode: document.getElementById('chartStockCode'),
            convergencePct: document.getElementById('convergencePct'),
            convergencePctInput: document.getElementById('convergencePctInput'),
            convergenceDays: document.getElementById('convergenceDays'),
            convergenceDaysValue: document.getElementById('convergenceDaysValue'),
            loadingOverlay: document.getElementById('loadingOverlay'),
            loadingProgress: document.getElementById('loadingProgress'),
            infoCards: document.getElementById('infoCards'),
            infoClose: document.getElementById('infoClose'),
            infoConvergence: document.getElementById('infoConvergence'),
            infoMarket: document.getElementById('infoMarket'),
            toastContainer: document.getElementById('toastContainer'),
        };
    },

    bindEvents() {
        this.elements.screenBtn.addEventListener('click', () => this.handleScreen());
        this.elements.refreshBtn.addEventListener('click', () => this.handleRefresh());

        // 雙向綁定：Slider <-> Input
        this.elements.convergencePct.addEventListener('input', () => {
            this.elements.convergencePctInput.value = this.elements.convergencePct.value;
        });

        this.elements.convergencePctInput.addEventListener('input', () => {
            this.elements.convergencePct.value = this.elements.convergencePctInput.value;
        });

        this.elements.convergenceDays.addEventListener('input', () => this.updateSliderValues());

        // 顯示天數按鈕
        document.querySelectorAll('.period-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handlePeriodChange(e));
        });

        // K線週期選擇
        document.querySelectorAll('.interval-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleIntervalChange(e));
        });
    },

    updateSliderValues() {
        // 初始化同步
        this.elements.convergencePctInput.value = this.elements.convergencePct.value;

        // 更新天數顯示
        const days = this.elements.convergenceDays.value;
        this.elements.convergenceDaysValue.textContent = `${days} 天`;
    },

    getSelectedMAPeriods() {
        const periods = [];
        // 使用新的 ma-input-item 結構
        document.querySelectorAll('.ma-input-item').forEach(item => {
            const checkbox = item.querySelector('.ma-checkbox');
            const input = item.querySelector('.ma-period-input');
            if (checkbox && checkbox.checked && input) {
                const value = parseInt(input.value);
                if (value > 0 && value <= 500) {
                    periods.push(value);
                }
            }
        });
        return periods;
    },

    getSelectedMarket() {
        const radio = document.querySelector('input[name="market"]:checked');
        return radio ? radio.value : 'all';
    },

    async handleScreen() {
        const maPeriods = this.getSelectedMAPeriods();
        if (maPeriods.length < 2) {
            this.showToast('請至少選擇兩條均線', 'warning');
            return;
        }

        const params = {
            maPeriods,
            convergencePct: parseFloat(this.elements.convergencePctInput.value),
            convergenceDays: parseInt(this.elements.convergenceDays.value),
            market: this.getSelectedMarket(),
        };

        this.showLoading(true);
        this.setButtonLoading(true);

        try {
            const stocks = await API.screenStocks(params);
            this.state.stocks = stocks;
            this.renderStockList(stocks);
            this.showToast(`找到 ${stocks.length} 檔符合條件的股票`, 'success');
        } catch (error) {
            console.error('Screen error:', error);
            this.showToast(error.message, 'error');
        } finally {
            this.showLoading(false);
            this.setButtonLoading(false);
        }
    },

    handleRefresh() {
        if (this.state.selectedStock) {
            this.loadStockChart(this.state.selectedStock.code);
        }
    },

    handlePeriodChange(e) {
        document.querySelectorAll('.period-btn').forEach(btn => btn.classList.remove('active'));
        e.target.classList.add('active');
        this.state.selectedDays = parseInt(e.target.dataset.days);

        if (this.state.selectedStock) {
            this.loadStockChart(this.state.selectedStock.code);
        }
    },

    handleIntervalChange(e) {
        // 切換 active 狀態
        document.querySelectorAll('.interval-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');

        this.state.selectedInterval = e.target.dataset.interval;

        if (this.state.selectedStock) {
            this.loadStockChart(this.state.selectedStock.code);
        }
    },

    renderStockList(stocks) {
        this.elements.resultCount.textContent = `${stocks.length} 檔`;

        if (stocks.length === 0) {
            this.elements.stockList.innerHTML = `
                <div class="empty-state">
                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="15" y1="9" x2="9" y2="15"></line>
                        <line x1="9" y1="9" x2="15" y2="15"></line>
                    </svg>
                    <p>沒有符合條件的股票</p>
                </div>`;
            return;
        }

        this.elements.stockList.innerHTML = stocks.map(stock => `
            <div class="stock-item" data-code="${stock.code}">
                <div class="stock-info">
                    <span class="stock-code">${stock.code}</span>
                    <span class="stock-name">${stock.name}</span>
                </div>
                <div class="stock-meta">
                    <div class="stock-price">${stock.close || '-'}</div>
                    <div class="stock-convergence">${stock.convergence_pct}%</div>
                </div>
            </div>
        `).join('');

        this.elements.stockList.querySelectorAll('.stock-item').forEach(item => {
            item.addEventListener('click', () => this.handleStockClick(item.dataset.code));
        });
    },

    async handleStockClick(code) {
        const stock = this.state.stocks.find(s => s.code === code);
        if (!stock) return;

        this.state.selectedStock = stock;

        document.querySelectorAll('.stock-item').forEach(item => {
            item.classList.toggle('active', item.dataset.code === code);
        });

        this.elements.chartStockName.textContent = stock.name;
        this.elements.chartStockCode.textContent = stock.code;

        await this.loadStockChart(code);

        this.elements.infoCards.style.display = 'grid';
        this.elements.infoClose.textContent = stock.close || '-';
        this.elements.infoConvergence.textContent = `${stock.convergence_pct}%`;
        this.elements.infoMarket.textContent = stock.market === 'TW' ? '上市' : '上櫃';
    },

    async loadStockChart(code) {
        try {
            const maPeriods = this.getSelectedMAPeriods();
            const data = await API.getStockKline(
                code,
                this.state.selectedDays,
                maPeriods,
                this.state.selectedInterval
            );
            ChartManager.setData(data);
        } catch (error) {
            console.error('Load chart error:', error);
            this.showToast(`載入圖表失敗: ${error.message}`, 'error');
        }
    },

    showLoading(show) {
        this.elements.loadingOverlay.style.display = show ? 'flex' : 'none';
    },

    setButtonLoading(loading) {
        const btn = this.elements.screenBtn;
        btn.disabled = loading;
        btn.querySelector('.btn-text').style.display = loading ? 'none' : 'inline';
        btn.querySelector('.btn-loader').style.display = loading ? 'inline-flex' : 'none';
    },

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `<span class="toast-message">${message}</span>`;
        this.elements.toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },
};

document.addEventListener('DOMContentLoaded', () => App.init());
