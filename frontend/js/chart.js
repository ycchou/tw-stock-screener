/**
 * 台股均線糾結篩選器 - K 線圖模組 (TradingView Widget 版)
 */

const ChartManager = {
    widget: null,
    containerId: null,
    currentSymbol: null,
    currentInterval: 'D',

    init(containerId) {
        this.containerId = containerId;
    },

    /**
     * 載入圖表
     * @param {string} code 股票代碼 (e.g., '2330')
     * @param {string} market 市場類型 (e.g., 'TW', 'TWO')
     * @param {string} interval K線週期 (e.g., '1d', '15m')
     * @param {Array} maPeriods 均線設定 (optional)
     */
    loadChart(code, market, interval, maPeriods = []) {
        const symbol = this.getTradingViewSymbol(code, market);
        const tvInterval = this.mapInterval(interval);

        // 如果已經有 Widget 且 Symbol 一樣，只是一樣的圖表，可能不需要重繪
        // 但為了確保 Interval 正確，我們還是重新載入或者使用 Widget API 切換

        // 這裡直接重新建立 Widget，確保乾淨
        // 清空容器
        document.getElementById(this.containerId).innerHTML = '';

        // 轉換 MA 設定為 TradingView studies
        // TradingView Widget 允許傳入 studies
        const studies = maPeriods.map(period => ({
            id: "MASimple@tv-basicstudies",
            inputs: { length: period }
        }));

        // 如果沒有指定 MA，預設至少一定要有 MA
        if (studies.length === 0) {
            studies.push({ id: "MASimple@tv-basicstudies", inputs: { length: 5 } });
            studies.push({ id: "MASimple@tv-basicstudies", inputs: { length: 20 } });
        }

        this.widget = new TradingView.widget({
            "width": "100%",
            "height": 500,
            "symbol": symbol,
            "interval": tvInterval,
            "timezone": "Asia/Taipei",
            "theme": "dark",
            "style": "1", // 1=Candles
            "locale": "zh_TW",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "hide_top_toolbar": false,
            "hide_legend": false,
            "save_image": false,
            "container_id": this.containerId,
            "studies": studies,
            "disabled_features": [
                "use_localstorage_for_settings",
            ],
            "enabled_features": [
                "study_templates"
            ]
        });

        this.currentSymbol = symbol;
        this.currentInterval = tvInterval;
    },

    /**
     * 將應用程式的 interval 轉換為 TradingView 格式
     */
    mapInterval(interval) {
        const map = {
            '15m': '15',
            '30m': '30',
            '1h': '60',
            '4h': '240',
            '1d': 'D',
            '1wk': 'W',
            '1mo': 'M'
        };
        return map[interval] || 'D';
    },

    /**
     * 轉換股票代碼為 TradingView Symbol
     */
    getTradingViewSymbol(code, market) {
        // 去除可能的 .TW 後綴
        const cleanCode = code.replace('.TW', '').replace('.TWO', '');

        if (market === 'TWO') {
            return `TPEX:${cleanCode}`;
        }
        // 預設為 TWSE (上市)
        return `TWSE:${cleanCode}`;
    },

    clear() {
        if (this.containerId) {
            document.getElementById(this.containerId).innerHTML = '';
        }
    }
};

window.ChartManager = ChartManager;
