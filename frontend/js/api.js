/**
 * 台股均線糾結篩選器 - API 模組
 * 處理與後端的所有 HTTP 通訊
 */

const API = {
    // 後端 API 基礎 URL
    // 如果是 Port 3000 (開發用)，則連線到 :8000
    // 否則 (Port 8000 或其他)，代表是由後端直接服務，使用當前 Origin
    BASE_URL: window.location.port === '3000'
        ? `http://${window.location.hostname}:8000`
        : window.location.origin,

    /**
     * 設定 API 基礎 URL
     * @param {string} url - 新的基礎 URL
     */
    setBaseUrl(url) {
        this.BASE_URL = url;
    },

    /**
     * 通用請求方法
     * @param {string} endpoint - API 端點
     * @param {Object} options - fetch 選項
     * @returns {Promise<any>} - 回應資料
     */
    async request(endpoint, options = {}) {
        const url = `${this.BASE_URL}${endpoint}`;

        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const mergedOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers,
            },
        };

        try {
            const response = await fetch(url, mergedOptions);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
                throw new Error('無法連接到伺服器，請確認後端服務是否啟動');
            }
            throw error;
        }
    },

    /**
     * 取得股票列表
     * @param {string} market - 市場類型 (all, TW, TWO)
     * @param {number} limit - 回傳筆數限制
     * @returns {Promise<Array>} - 股票列表
     */
    async getStocks(market = 'all', limit = 100) {
        return this.request(`/api/stocks?market=${market}&limit=${limit}`);
    },

    /**
     * 篩選均線糾結股票
     * @param {Object} params - 篩選參數
     * @param {number[]} params.maPeriods - 均線週期列表
     * @param {number} params.convergencePct - 糾結幅度百分比
     * @param {number} params.convergenceDays - 連續糾結天數
     * @param {string} params.market - 市場類型
     * @param {string} params.interval - K線週期
     * @returns {Promise<Array>} - 符合條件的股票列表
     */
    async screenStocks({ maPeriods, convergencePct, convergenceDays, market, interval = '1d' }) {
        return this.request('/api/screen', {
            method: 'POST',
            body: JSON.stringify({
                ma_periods: maPeriods,
                convergence_pct: convergencePct,
                convergence_days: convergenceDays,
                market: market,
                interval: interval,
            }),
        });
    },

    /**
     * 取得個股 K 線數據
     * @param {string} code - 股票代碼
     * @param {number} days - 取幾天的數據
     * @param {number[]} maPeriods - 要計算的均線週期
     * @param {string} interval - K 線週期 (1m, 5m, 15m, 30m, 1h, 4h, 1d, 1wk, 1mo)
     * @returns {Promise<Object>} - K 線數據與均線
     */
    async getStockKline(code, days = 120, maPeriods = [5, 10, 20, 60], interval = '1d') {
        const maPeriodsStr = maPeriods.join(',');
        return this.request(`/api/stock/${code}/kline?days=${days}&ma_periods=${maPeriodsStr}&interval=${interval}`);
    },

    /**
     * 健康檢查
     * @returns {Promise<Object>} - 健康狀態
     */
    async healthCheck() {
        return this.request('/api/health');
    },
};

// 匯出 API 模組
window.API = API;
