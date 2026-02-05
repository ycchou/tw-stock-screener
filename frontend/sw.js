/**
 * 台股均線糾結篩選器 - Service Worker
 * 提供離線快取功能
 */

const CACHE_NAME = 'tw-stock-screener-v18';
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/css/style.css',
    '/js/api.js',
    '/js/chart.js',
    '/js/app.js',
    '/manifest.json'
];

// 安裝事件 - 快取靜態資源
self.addEventListener('install', (event) => {
    console.log('[SW] 安裝中...');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[SW] 快取靜態資源');
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => {
                console.log('[SW] 安裝完成');
                return self.skipWaiting();
            })
    );
});

// 啟動事件 - 清理舊快取
self.addEventListener('activate', (event) => {
    console.log('[SW] 啟動中...');
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames
                        .filter((name) => name !== CACHE_NAME)
                        .map((name) => {
                            console.log('[SW] 刪除舊快取:', name);
                            return caches.delete(name);
                        })
                );
            })
            .then(() => {
                console.log('[SW] 啟動完成');
                return self.clients.claim();
            })
    );
});

// 請求攔截
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // API 請求使用 Network First 策略
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(networkFirst(request));
        return;
    }

    // 靜態資源使用 Cache First 策略
    event.respondWith(cacheFirst(request));
});

/**
 * Cache First 策略
 * 優先從快取取得，沒有才從網路取得
 */
async function cacheFirst(request) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
        return cachedResponse;
    }

    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        console.log('[SW] 網路請求失敗:', error);
        // 返回離線頁面或錯誤回應
        return new Response('離線中', {
            status: 503,
            statusText: 'Service Unavailable'
        });
    }
}

/**
 * Network First 策略
 * 優先從網路取得，失敗才從快取取得
 */
async function networkFirst(request) {
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            // 快取 API 回應（可選）
            const cache = await caches.open(CACHE_NAME + '-api');
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        console.log('[SW] API 請求失敗，嘗試從快取取得');
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        return new Response(JSON.stringify({ error: '離線中，無法取得資料' }), {
            status: 503,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}

// 接收來自主線程的訊息
self.addEventListener('message', (event) => {
    if (event.data === 'skipWaiting') {
        self.skipWaiting();
    }
});
