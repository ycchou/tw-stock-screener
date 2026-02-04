/**
 * 台股均線糾結篩選器 - K 線圖模組
 */

const ChartManager = {
    chart: null,
    candleSeries: null,
    maLines: {},
    container: null,

    MA_COLORS: {
        MA5: '#ff6b6b',
        MA10: '#ffd93d',
        MA20: '#6bcb77',
        MA60: '#4d96ff',
        MA120: '#ff9ff3',
        MA240: '#a29bfe',
    },

    init(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;
        this.createChart();
        this.setupResizeHandler();
    },

    createChart() {
        if (this.chart) {
            this.chart.remove();
            this.chart = null;
        }

        const placeholder = this.container.querySelector('.chart-placeholder');
        if (placeholder) placeholder.style.display = 'none';

        // 初始化圖例容器
        const oldLegend = this.container.querySelector('.chart-legend');
        if (oldLegend) oldLegend.remove();

        this.legendElement = document.createElement('div');
        this.legendElement.className = 'chart-legend';
        this.legendElement.style.display = 'none';
        this.container.appendChild(this.legendElement);

        this.chart = LightweightCharts.createChart(this.container, {
            width: this.container.clientWidth,
            height: this.container.clientHeight || 400,
            layout: {
                background: { type: 'solid', color: '#1a1a2e' },
                textColor: '#94a3b8',
            },
            grid: {
                vertLines: { color: 'rgba(255, 255, 255, 0.05)' },
                horzLines: { color: 'rgba(255, 255, 255, 0.05)' },
            },
            crosshair: { mode: LightweightCharts.CrosshairMode.Normal },
            rightPriceScale: { borderColor: 'rgba(255, 255, 255, 0.1)' },
            timeScale: { borderColor: 'rgba(255, 255, 255, 0.1)', timeVisible: true },
        });

        this.candleSeries = this.chart.addCandlestickSeries({
            upColor: '#ef5350',
            downColor: '#26a69a',
            borderUpColor: '#ef5350',
            borderDownColor: '#26a69a',
            wickUpColor: '#ef5350',
            wickDownColor: '#26a69a',
        });

        this.maLines = {};
    },

    setupResizeHandler() {
        const resizeObserver = new ResizeObserver((entries) => {
            if (this.chart && entries[0]) {
                const { width, height } = entries[0].contentRect;
                this.chart.resize(width, height);
            }
        });
        resizeObserver.observe(this.container);
    },

    setData(data) {
        if (!this.chart || !this.candleSeries) this.createChart();
        if (!data || !data.ohlc || data.ohlc.length === 0) return;

        // 清空舊圖例
        this.legendElement.innerHTML = '';
        this.legendElement.style.display = 'flex';

        const candleData = data.ohlc.map(item => ({
            time: item.time,
            open: item.open,
            high: item.high,
            low: item.low,
            close: item.close,
        }));

        this.candleSeries.setData(candleData);

        Object.values(this.maLines).forEach(series => this.chart.removeSeries(series));
        this.maLines = {};

        if (data.ma_lines) {
            Object.entries(data.ma_lines).forEach(([maName, maData]) => {
                if (maData && maData.length > 0) this.addMALine(maName, maData);
            });
        }

        this.chart.timeScale().fitContent();
    },

    addMALine(maName, maData) {
        const color = this.MA_COLORS[maName] || '#ffffff';
        const lineSeries = this.chart.addLineSeries({
            color: color,
            lineWidth: 1.5,
            priceLineVisible: false,
            lastValueVisible: false,
        });

        const lineData = maData
            .filter(item => item.value !== null)
            .map(item => ({ time: item.time, value: item.value }));

        if (lineData.length > 0) {
            lineSeries.setData(lineData);
            this.maLines[maName] = lineSeries;

            // 新增圖例項目
            const item = document.createElement('div');
            item.className = 'legend-item';
            item.innerHTML = `
                <div class="legend-color" style="background-color: ${color}"></div>
                <span>${maName}</span>
            `;
            this.legendElement.appendChild(item);
        }
    },

    clear() {
        if (this.candleSeries) this.candleSeries.setData([]);
        Object.values(this.maLines).forEach(s => this.chart && this.chart.removeSeries(s));
        this.maLines = {};
    },
};

window.ChartManager = ChartManager;
