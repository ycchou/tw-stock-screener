/**
 * 台股均線糾結篩選器 - 前端 UI 測試
 * Source: doc/test/frontend-ui-tests.md
 */
const { test, expect } = require('@playwright/test');

test.describe('頁面載入', () => {
    test('【前端元素】頁面應顯示標題「台股均線糾結篩選器」', async ({ page }) => {
        await page.goto('/');
        await expect(page.locator('h1')).toContainText('台股均線糾結篩選器');
    });

    test('【前端元素】設定面板應顯示均線選擇 checkbox', async ({ page }) => {
        await page.goto('/');
        // Checkboxes are hidden by CSS, verify they are attached to DOM
        const ids = ['#ma5', '#ma10', '#ma20', '#ma60', '#ma120', '#ma240'];
        for (const id of ids) {
            await expect(page.locator(id)).toBeAttached();
        }
    });

    test('【前端元素】糾結幅度滑桿應可見且可操作', async ({ page }) => {
        await page.goto('/');
        const slider = page.locator('#convergencePct');
        await expect(slider).toBeVisible();
        await expect(slider).toHaveAttribute('type', 'range');
    });

    test('【前端元素】「開始篩選」按鈕應存在', async ({ page }) => {
        await page.goto('/');
        const btn = page.locator('#screenBtn');
        await expect(btn).toBeVisible();
        await expect(btn).toBeEnabled();
    });
});

test.describe('參數設定互動', () => {
    test('【function 邏輯】拖動幅度滑桿時數值顯示應即時更新', async ({ page }) => {
        await page.goto('/');
        await page.locator('#convergencePct').fill('5');
        await expect(page.locator('#convergencePctValue')).toHaveText('5%');
    });

    test('【function 邏輯】拖動天數滑桿時數值顯示應即時更新', async ({ page }) => {
        await page.goto('/');
        await page.locator('#convergenceDays').fill('10');
        await expect(page.locator('#convergenceDaysValue')).toHaveText('10 天');
    });

    test('【前端元素】預設應選取 5日、10日、20日、60日 均線', async ({ page }) => {
        await page.goto('/');
        await expect(page.locator('#ma5')).toBeChecked();
        await expect(page.locator('#ma10')).toBeChecked();
        await expect(page.locator('#ma20')).toBeChecked();
        await expect(page.locator('#ma60')).toBeChecked();
        await expect(page.locator('#ma120')).not.toBeChecked();
        await expect(page.locator('#ma240')).not.toBeChecked();
    });
});

test.describe('篩選功能', () => {
    test('【function 邏輯】點擊篩選按鈕應顯示 loading 狀態', async ({ page }) => {
        await page.goto('/');
        await page.locator('#screenBtn').click();
        // Verify button disabled and spinner visible
        await expect(page.locator('#screenBtn')).toBeDisabled();
        // Loader implies SVG spinner or text change
        await expect(page.locator('.btn-loader')).toBeVisible();
    });

    test('【驗證邏輯】選擇少於兩條均線應顯示警告', async ({ page }) => {
        await page.goto('/');
        // Uncheck all first
        const ids = ['#ma5', '#ma10', '#ma20', '#ma60', '#ma120', '#ma240'];
        for (const id of ids) {
            await page.locator(id).uncheck({ force: true });
        }
        // Check one
        await page.locator('#ma5').check({ force: true });

        await page.locator('#screenBtn').click();
        await expect(page.locator('.toast')).toBeVisible();
        await expect(page.locator('.toast')).toContainText('至少選擇兩條均線');
    });

    test('【Mock API】篩選完成後應顯示股票列表', async ({ page }) => {
        await page.goto('/');
        await page.locator('#screenBtn').click();
        await page.waitForSelector('.stock-item', { timeout: 60000 });
        expect(await page.locator('.stock-item').count()).toBeGreaterThan(0);
    });
});

test.describe('股票列表', () => {
    test('【前端元素】股票項目應顯示代碼、名稱、價格', async ({ page }) => {
        await page.goto('/');
        await page.locator('#screenBtn').click();
        await page.waitForSelector('.stock-item', { timeout: 60000 });
        const item = page.locator('.stock-item').first();
        await expect(item.locator('.stock-code')).toBeVisible();
        await expect(item.locator('.stock-name')).toBeVisible();
        await expect(item.locator('.stock-price')).toBeVisible();
    });

    test('【function 邏輯】點擊股票應切換 active 狀態', async ({ page }) => {
        await page.goto('/');
        await page.locator('#screenBtn').click();
        await page.waitForSelector('.stock-item', { timeout: 60000 });
        const item = page.locator('.stock-item').first();
        await item.click();
        await expect(item).toHaveClass(/active/);
    });
});

test.describe('K 線圖顯示', () => {
    test('【function 邏輯】點擊股票後應載入 K 線圖', async ({ page }) => {
        await page.goto('/');
        await page.locator('#screenBtn').click();
        await page.waitForSelector('.stock-item', { timeout: 60000 });
        await page.locator('.stock-item').first().click();
        await expect(page.locator('#chartContainer canvas')).toBeVisible({ timeout: 60000 });
    });

    test('【前端元素】圖表標題應顯示股票名稱', async ({ page }) => {
        await page.goto('/');
        await page.locator('#screenBtn').click();
        await page.waitForSelector('.stock-item', { timeout: 60000 });
        await page.locator('.stock-item').first().click();
        await expect(page.locator('#chartStockName')).not.toHaveText('選擇股票查看 K 線圖', { timeout: 60000 });
    });

    test('【前端元素】選擇股票後應顯示資訊卡片', async ({ page }) => {
        await page.goto('/');
        await page.locator('#screenBtn').click();
        await page.waitForSelector('.stock-item', { timeout: 60000 });
        await page.locator('.stock-item').first().click();
        await page.waitForTimeout(3000); // Wait for transition/render
        await expect(page.locator('#infoCards')).toBeVisible({ timeout: 10000 });
    });

    test('【function 邏輯】點擊週期按鈕應切換圖表數據', async ({ page }) => {
        await page.goto('/');
        await page.locator('#screenBtn').click();
        await page.waitForSelector('.stock-item', { timeout: 60000 });
        await page.locator('.stock-item').first().click();
        const btn = page.locator('.period-btn[data-days="30"]');
        await btn.click();
        await expect(btn).toHaveClass(/active/);
    });
});
