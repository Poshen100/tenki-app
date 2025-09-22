import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import time
import requests
import json
from concurrent.futures import ThreadPoolExecutor
import plotly.graph_objects as go
import plotly.express as px

# ====== 頁面配置 ======
st.set_page_config(
    page_title="TENKI - Real-Time Trading Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====== 多語言支援系統 ======
LANGUAGES = {
    "🇹🇼 繁體中文": "zh",
    "🇺🇸 English": "en", 
    "🇯🇵 日本語": "jp"
}

TEXTS = {
    "zh": {
        "app_name": "TENKI",
        "tagline": "即時交易智能平台",
        "futures_indices": "期貨指數",
        "cryptocurrencies": "加密貨幣",
        "forex": "外匯市場",
        "commodities": "商品期貨",
        "bonds": "債券市場",
        "hot_stocks": "熱門股票",
        "market_overview": "市場總覽",
        "real_time_data": "即時數據",
        "volume": "成交量",
        "change": "漲跌",
        "price": "價格",
        "language": "語言",
        "last_update": "最後更新",
        "market_cap": "市值",
        "sp_futures": "標普期指",
        "nasdaq_futures": "納指期指", 
        "dow_futures": "道瓊期指",
        "bitcoin": "比特幣",
        "ethereum": "以太幣",
        "usdt": "泰達幣",
        "usd_jpy": "美元日圓",
        "gold_futures": "黃金期貨",
        "treasury_10y": "10年期公債",
        "loading": "載入中...",
        "error": "無法載入",
        "refresh": "刷新數據"
    },
    "en": {
        "app_name": "TENKI",
        "tagline": "Real-Time Trading Intelligence",
        "futures_indices": "Futures Indices",
        "cryptocurrencies": "Cryptocurrencies",
        "forex": "Forex Market",
        "commodities": "Commodities",
        "bonds": "Bond Market",
        "hot_stocks": "Hot Stocks",
        "market_overview": "Market Overview",
        "real_time_data": "Real-Time Data",
        "volume": "Volume",
        "change": "Change",
        "price": "Price",
        "language": "Language",
        "last_update": "Last Update",
        "market_cap": "Market Cap",
        "sp_futures": "S&P Futures",
        "nasdaq_futures": "NASDAQ Futures",
        "dow_futures": "Dow Futures",
        "bitcoin": "Bitcoin",
        "ethereum": "Ethereum",
        "usdt": "Tether",
        "usd_jpy": "USD/JPY",
        "gold_futures": "Gold Futures",
        "treasury_10y": "10Y Treasury",
        "loading": "Loading...",
        "error": "Load Error",
        "refresh": "Refresh Data"
    },
    "jp": {
        "app_name": "TENKI",
        "tagline": "リアルタイム取引インテリジェンス",
        "futures_indices": "先物指数",
        "cryptocurrencies": "暗号通貨",
        "forex": "外国為替市場",
        "commodities": "商品先物",
        "bonds": "債券市場",
        "hot_stocks": "人気株式",
        "market_overview": "市場概況",
        "real_time_data": "リアルタイムデータ",
        "volume": "出来高",
        "change": "変動",
        "price": "価格",
        "language": "言語",
        "last_update": "最終更新",
        "market_cap": "時価総額",
        "sp_futures": "S&P先物",
        "nasdaq_futures": "NASDAQ先物",
        "dow_futures": "ダウ先物",
        "bitcoin": "ビットコイン",
        "ethereum": "イーサリアム",
        "usdt": "テザー",
        "usd_jpy": "米ドル円",
        "gold_futures": "金先物",
        "treasury_10y": "10年国債",
        "loading": "読み込み中...",
        "error": "読み込みエラー",
        "refresh": "データを更新"
    }
}

# ====== Session State 初始化 ======
if 'language' not in st.session_state:
    st.session_state.language = 'zh'
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'market_data_cache' not in st.session_state:
    st.session_state.market_data_cache = {}

# ====== 數據獲取系統 ======

@st.cache_data(ttl=60, show_spinner=False)
def get_futures_data():
    """獲取期貨指數數據"""
    futures_symbols = {
        'ES': 'ES=F',  # S&P 500 期貨
        'NQ': 'NQ=F',  # NASDAQ 期貨  
        'YM': 'YM=F'   # Dow Jones 期貨
    }
    
    futures_data = {}
    
    def fetch_single_future(symbol_key, symbol):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d", interval="1m")
            if not hist.empty:
                current = hist['Close'].iloc[-1]
                prev_close = ticker.info.get('previousClose', current)
                change = current - prev_close
                change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                volume = hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0
                
                return {
                    'symbol': symbol_key,
                    'price': float(current),
                    'change': float(change),
                    'change_pct': float(change_pct),
                    'volume': int(volume),
                    'timestamp': datetime.now()
                }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
        return None
    
    # 並行獲取數據
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(fetch_single_future, k, v) for k, v in futures_symbols.items()]
        for future in futures:
            result = future.result()
            if result:
                futures_data[result['symbol']] = result
    
    return futures_data

@st.cache_data(ttl=60, show_spinner=False)
def get_crypto_data():
    """獲取加密貨幣數據"""
    crypto_symbols = {
        'BTC': 'BTC-USD',
        'ETH': 'ETH-USD', 
        'USDT': 'USDT-USD'
    }
    
    crypto_data = {}
    
    def fetch_single_crypto(symbol_key, symbol):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d", interval="1m")
            info = ticker.info
            
            if not hist.empty:
                current = hist['Close'].iloc[-1]
                prev_close = info.get('previousClose', current)
                change = current - prev_close  
                change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                volume = hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0
                market_cap = info.get('marketCap', 0)
                
                return {
                    'symbol': symbol_key,
                    'price': float(current),
                    'change': float(change),
                    'change_pct': float(change_pct),
                    'volume': int(volume),
                    'market_cap': int(market_cap) if market_cap else 0,
                    'timestamp': datetime.now()
                }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
        return None
    
    # 並行獲取數據
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(fetch_single_crypto, k, v) for k, v in crypto_symbols.items()]
        for future in futures:
            result = future.result()
            if result:
                crypto_data[result['symbol']] = result
    
    return crypto_data

@st.cache_data(ttl=60, show_spinner=False)
def get_forex_commodities_bonds():
    """獲取外匯、商品、債券數據"""
    symbols = {
        'USDJPY': 'JPY=X',     # 美元/日圓
        'GOLD': 'GC=F',        # 黃金期貨
        'TNX': '^TNX'          # 10年期美國公債
    }
    
    data = {}
    
    def fetch_single_asset(symbol_key, symbol):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d", interval="1m")
            info = ticker.info
            
            if not hist.empty:
                current = hist['Close'].iloc[-1]
                prev_close = info.get('previousClose', current)
                change = current - prev_close
                change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                volume = hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0
                
                return {
                    'symbol': symbol_key,
                    'price': float(current),
                    'change': float(change),
                    'change_pct': float(change_pct),
                    'volume': int(volume),
                    'timestamp': datetime.now()
                }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
        return None
    
    # 並行獲取數據
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(fetch_single_asset, k, v) for k, v in symbols.items()]
        for future in futures:
            result = future.result()
            if result:
                data[result['symbol']] = result
    
    return data

@st.cache_data(ttl=300, show_spinner=False)
def get_hot_stocks():
    """獲取熱門股票（按成交量排序）"""
    # 美股熱門股票代碼
    popular_stocks = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 
        'NVDA', 'META', 'NFLX', 'COIN', 'AMD',
        'BABA', 'PLTR', 'MSTR', 'RIOT', 'GME'
    ]
    
    stocks_data = []
    
    def fetch_stock_data(symbol):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d", interval="1m")
            info = ticker.info
            
            if not hist.empty:
                current = hist['Close'].iloc[-1]
                prev_close = info.get('previousClose', current)
                change = current - prev_close
                change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                volume = hist['Volume'].sum()  # 當日總成交量
                
                return {
                    'symbol': symbol,
                    'name': info.get('longName', symbol),
                    'price': float(current),
                    'change': float(change),
                    'change_pct': float(change_pct),
                    'volume': int(volume),
                    'market_cap': info.get('marketCap', 0),
                    'timestamp': datetime.now()
                }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
        return None
    
    # 並行獲取股票數據
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_stock_data, symbol) for symbol in popular_stocks]
        for future in futures:
            result = future.result()
            if result and result['volume'] > 0:
                stocks_data.append(result)
    
    # 按成交量排序
    stocks_data.sort(key=lambda x: x['volume'], reverse=True)
    return stocks_data[:10]  # 返回前10名

# ====== UI設計系統 ======
def load_trading_app_design():
    """載入交易APP風格設計"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        /* 重置預設樣式 */
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
            background: #0a0e1a;
        }
        
        #MainMenu, footer, header, .stDeployButton, .stDecoration {
            visibility: hidden !important;
            height: 0 !important;
        }
        
        .stApp {
            margin-top: -100px !important;
            background: #0a0e1a;
        }
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        /* 主內容區域 */
        .main-content {
            padding: 1rem;
            background: #0a0e1a;
            color: white;
        }
        
        /* 頂部橫幅 - 深色主題 */
        .top-banner {
            background: linear-gradient(135deg, #1a1f2e 0%, #16213e 100%);
            padding: 1rem;
            border-radius: 16px;
            margin-bottom: 1rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* 交易面板標題 */
        .trading-header {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            padding: 1rem;
            border-radius: 12px;
            margin: 1rem 0 0.5rem 0;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .trading-header h3 {
            font-size: 1.1rem;
            font-weight: 700;
            margin: 0;
            color: #e2e8f0;
        }
        
        /* 數據卡片 - 交易APP風格 */
        div[data-testid="metric-container"] {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-radius: 12px;
            padding: 1rem !important;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        div[data-testid="metric-container"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }
        
        /* 指標標籤 */
        div[data-testid="metric-container"] label {
            color: #94a3b8 !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }
        
        /* 指標數值 */
        div[data-testid="metric-container"] > div > div {
            color: #f1f5f9 !important;
            font-weight: 700 !important;
        }
        
        /* 漲跌顏色 */
        div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
            font-weight: 600 !important;
        }
        
        /* 正數 - 綠色 */
        div[data-testid="metric-container"] div[data-testid="stMetricDelta"] svg[fill="#09ab3b"] {
            fill: #22c55e !important;
        }
        
        /* 負數 - 紅色 */
        div[data-testid="metric-container"] div[data-testid="stMetricDelta"] svg[fill="#ff2b2b"] {
            fill: #ef4444 !important;
        }
        
        /* 股票信息卡片 */
        .stock-card {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .stock-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }
        
        /* 股票標題 */
        .stock-symbol {
            color: #f1f5f9;
            font-size: 1.1rem;
            font-weight: 700;
        }
        
        .stock-name {
            color: #94a3b8;
            font-size: 0.8rem;
        }
        
        .stock-price {
            color: #f1f5f9;
            font-size: 1.3rem;
            font-weight: 800;
        }
        
        /* 漲跌幅顏色 */
        .positive {
            color: #22c55e !important;
        }
        
        .negative {
            color: #ef4444 !important;
        }
        
        /* 刷新按鈕 */
        .refresh-container {
            text-align: center;
            margin: 1rem 0;
        }
        
        /* 時間戳 */
        .timestamp {
            color: #64748b;
            font-size: 0.7rem;
            text-align: center;
            margin: 0.5rem 0;
        }
        
        /* 響應式設計 */
        @media (max-width: 768px) {
            .main-content {
                padding: 0.5rem;
            }
            
            .trading-header h3 {
                font-size: 1rem;
            }
        }
        
        @media (max-width: 480px) {
            .main-content {
                padding: 0.3rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def create_top_banner():
    """創建頂部交易平台橫幅"""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<div class="top-banner">', unsafe_allow_html=True)
    
    try:
        st.image("IMG_0638.png", use_container_width=True)
    except:
        st.markdown("""
        <div style="text-align: center;">
            <div style="display: inline-flex; align-items: center; gap: 1rem;">
                <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); 
                            border-radius: 50%; display: flex; align-items: center; justify-content: center;
                            box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);">
                    <span style="color: white; font-size: 1.3rem; font-weight: bold;">T</span>
                </div>
                <div>
                    <div style="font-size: 2rem; font-weight: 900; color: #f1f5f9; margin-bottom: 0.2rem;">TENKI</div>
                    <div style="font-size: 0.9rem; color: #94a3b8;">Real-Time Trading Intelligence</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_trading_section(title, data, t, asset_type="default"):
    """創建統一的交易數據區域"""
    st.markdown(f'<div class="trading-header"><h3>📊 {title}</h3></div>', unsafe_allow_html=True)
    
    if not data:
        st.warning(f"{t['loading']} {title}")
        return
    
    # 根據資產類型決定列數
    if asset_type == "futures":
        cols = st.columns(3)
    elif asset_type == "crypto":
        cols = st.columns(3)
    elif asset_type == "others":
        cols = st.columns(3)
    else:
        cols = st.columns(len(data))
    
    for i, (symbol, info) in enumerate(data.items()):
        if i < len(cols):
            with cols[i]:
                # 根據資產類型決定顯示格式
                if asset_type == "crypto" and info.get('market_cap', 0) > 0:
                    # 加密貨幣顯示市值
                    market_cap_str = f"${info['market_cap']/1e9:.1f}B" if info['market_cap'] > 1e9 else f"${info['market_cap']/1e6:.1f}M"
                    delta_str = f"{info['change']:+.2f} ({info['change_pct']:+.2f}%) | 市值: {market_cap_str}"
                elif asset_type == "forex":
                    # 外匯顯示更多小數位
                    delta_str = f"{info['change']:+.4f} ({info['change_pct']:+.2f}%)"
                    price_str = f"{info['price']:.4f}"
                else:
                    # 一般格式
                    delta_str = f"{info['change']:+.2f} ({info['change_pct']:+.2f}%)"
                    price_str = f"{info['price']:,.2f}"
                
                # 獲取本地化名稱
                display_name = get_localized_name(symbol, t)
                
                st.metric(
                    label=display_name,
                    value=price_str if asset_type == "forex" else f"${info['price']:,.2f}",
                    delta=delta_str
                )

def get_localized_name(symbol, t):
    """獲取本地化的資產名稱"""
    name_mapping = {
        'ES': t.get('sp_futures', 'S&P Futures'),
        'NQ': t.get('nasdaq_futures', 'NASDAQ Futures'),
        'YM': t.get('dow_futures', 'Dow Futures'),
        'BTC': t.get('bitcoin', 'Bitcoin'),
        'ETH': t.get('ethereum', 'Ethereum'),
        'USDT': t.get('usdt', 'Tether'),
        'USDJPY': t.get('usd_jpy', 'USD/JPY'),
        'GOLD': t.get('gold_futures', 'Gold Futures'),
        'TNX': t.get('treasury_10y', '10Y Treasury')
    }
    return name_mapping.get(symbol, symbol)

def create_hot_stocks_section(stocks_data, t):
    """創建熱門股票區域"""
    st.markdown(f'<div class="trading-header"><h3>🔥 {t["hot_stocks"]} (按成交量排序)</h3></div>', unsafe_allow_html=True)
    
    if not stocks_data:
        st.warning(f"{t['loading']} {t['hot_stocks']}")
        return
    
    for i, stock in enumerate(stocks_data[:8], 1):  # 顯示前8名
        with st.container():
            st.markdown('<div class="stock-card">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f'<div class="stock-symbol">#{i} {stock["symbol"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="stock-name">{stock["name"][:30]}...</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'<div class="stock-price">${stock["price"]:.2f}</div>', unsafe_allow_html=True)
                change_class = "positive" if stock["change"] >= 0 else "negative"
                st.markdown(f'<div class="{change_class}">{stock["change"]:+.2f} ({stock["change_pct"]:+.2f}%)</div>', unsafe_allow_html=True)
            
            with col3:
                volume_str = f"{stock['volume']/1e6:.1f}M" if stock['volume'] > 1e6 else f"{stock['volume']/1e3:.0f}K"
                st.markdown(f"**{t['volume']}:** {volume_str}")
                if stock.get('market_cap', 0) > 0:
                    mcap_str = f"${stock['market_cap']/1e9:.1f}B" if stock['market_cap'] > 1e9 else f"${stock['market_cap']/1e6:.1f}M"
                    st.markdown(f"**{t['market_cap']}:** {mcap_str}")
            
            st.markdown('</div>', unsafe_allow_html=True)

def language_selector(t):
    """語言選擇器"""
    st.markdown(f"""
    <div class="trading-header">
        <h3>🌐 {t['language']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🇹🇼 繁體中文", use_container_width=True, 
                     type="primary" if st.session_state.language == 'zh' else "secondary"):
            st.session_state.language = 'zh'
            st.rerun()
    
    with col2:
        if st.button("🇺🇸 English", use_container_width=True,
                     type="primary" if st.session_state.language == 'en' else "secondary"):
            st.session_state.language = 'en'
            st.rerun()
    
    with col3:
        if st.button("🇯🇵 日本語", use_container_width=True,
                     type="primary" if st.session_state.language == 'jp' else "secondary"):
            st.session_state.language = 'jp'
            st.rerun()

# ====== 主應用程式 ======
def main():
    # 載入交易APP設計
    load_trading_app_design()
    
    # 獲取當前語言設定
    lang = st.session_state.language
    t = TEXTS[lang]
    
    # 頂部橫幅
    create_top_banner()
    
    # 語言選擇器
    language_selector(t)
    
    # 數據刷新控制
    st.markdown('<div class="refresh-container">', unsafe_allow_html=True)
    if st.button(f"🔄 {t['refresh']}", use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.session_state.last_refresh = datetime.now()
        st.rerun()
    
    # 顯示最後更新時間
    st.markdown(f'<div class="timestamp">{t["last_update"]}: {st.session_state.last_refresh.strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 數據載入狀態
    with st.spinner(f"{t['loading']} {t['real_time_data']}..."):
        
        # 並行載入所有數據
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures_future = executor.submit(get_futures_data)
            crypto_future = executor.submit(get_crypto_data)  
            other_future = executor.submit(get_forex_commodities_bonds)
            stocks_future = executor.submit(get_hot_stocks)
            
            # 獲取結果
            futures_data = futures_future.result()
            crypto_data = crypto_future.result()
            other_data = other_future.result()
            stocks_data = stocks_future.result()
    
    # 期貨指數區域
    create_trading_section(t['futures_indices'], futures_data, t, "futures")
    
    # 加密貨幣區域  
    create_trading_section(t['cryptocurrencies'], crypto_data, t, "crypto")
    
    # 外匯、商品、債券區域
    forex_data = {k: v for k, v in other_data.items() if k in ['USDJPY']}
    commodities_data = {k: v for k, v in other_data.items() if k in ['GOLD']}
    bonds_data = {k: v for k, v in other_data.items() if k in ['TNX']}
    
    if forex_data:
        create_trading_section(t['forex'], forex_data, t, "forex")
    
    if commodities_data:
        create_trading_section(t['commodities'], commodities_data, t, "others")
    
    if bonds_data:
        create_trading_section(t['bonds'], bonds_data, t, "others")
    
    # 熱門股票區域
    create_hot_stocks_section(stocks_data, t)
    
    # 底部資訊
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 1rem; color: #64748b; margin-top: 2rem; 
                border-top: 1px solid rgba(255, 255, 255, 0.1);">
        <p style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; color: #e2e8f0;">
            <strong>TENKI</strong> - {t['tagline']}
        </p>
        <p style="margin-bottom: 1rem; color: #94a3b8;">© 2025 TENKI Real-Time Trading Platform</p>
        <p style="font-size: 0.8rem; opacity: 0.8;">
            {t.get('disclaimer', '本平台僅供投資參考，投資有風險，請謹慎評估')}
        </p>
    </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
