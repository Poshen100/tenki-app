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
import pytz
import base64

# ====== 頁面配置 ======
st.set_page_config(
    page_title="TENKI - Professional Trading Platform",
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
        "tagline": "專業即時交易平台",
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
        "refresh": "刷新數據",
        "market_open": "開市中",
        "market_closed": "休市中",
        "auto_refresh": "自動刷新",
        "manual_refresh": "手動刷新"
    },
    "en": {
        "app_name": "TENKI", 
        "tagline": "Professional Real-Time Trading",
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
        "refresh": "Refresh Data",
        "market_open": "Market Open",
        "market_closed": "Market Closed",
        "auto_refresh": "Auto Refresh",
        "manual_refresh": "Manual Refresh"
    },
    "jp": {
        "app_name": "TENKI",
        "tagline": "プロフェッショナル即時取引",
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
        "refresh": "データを更新",
        "market_open": "市場オープン",
        "market_closed": "市場クローズ",
        "auto_refresh": "自動更新",
        "manual_refresh": "手動更新"
    }
}

# ====== Session State 初始化 ======
if 'language' not in st.session_state:
    st.session_state.language = 'zh'
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'refresh_counter' not in st.session_state:
    st.session_state.refresh_counter = 0

# ====== 市場時間檢查 ======
def is_market_open():
    """檢查美股市場是否開市"""
    try:
        ny_tz = pytz.timezone('America/New_York')
        now = datetime.now(ny_tz)
        
        # 檢查是否為週末
        if now.weekday() >= 5:  # 週六、週日
            return False
        
        # 市場時間: 9:30 AM - 4:00 PM ET (正常交易)
        # 期貨交易時間: 6:00 PM - 5:00 PM ET (幾乎24小時)
        market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
        
        return market_open <= now <= market_close
    except:
        return True

def get_market_status(t):
    """獲取市場狀態文字"""
    return t['market_open'] if is_market_open() else t['market_closed']

# ====== 精準的期貨數據獲取系統 ======
@st.cache_data(ttl=60, show_spinner=False)  # 增加到60秒緩存，減少API調用
def get_accurate_futures_data():
    """獲取精準的期貨指數數據 - 對標TradingView"""
    
    # 使用更精確的期貨代碼映射
    futures_symbols = {
        'ES': {
            'primary': 'ES=F',      # E-mini S&P 500期貨
            'backup': '^GSPC',      # S&P 500指數  
            'name': 'ES1!'
        },
        'NQ': {
            'primary': 'NQ=F',      # E-mini NASDAQ期貨
            'backup': '^IXIC',      # NASDAQ指數
            'name': 'NQ1!'
        },
        'YM': {
            'primary': 'YM=F',      # E-mini Dow期貨
            'backup': '^DJI',       # 道瓊指數
            'name': 'YM1!'
        }
    }
    
    futures_data = {}
    
    def fetch_precise_futures(symbol_key, symbol_info):
        """獲取精確的期貨數據"""
        for attempt, symbol in enumerate([symbol_info['primary'], symbol_info['backup']]):
            try:
                ticker = yf.Ticker(symbol)
                
                # 獲取更長時間的數據以確保準確性
                hist = ticker.history(period="5d", interval="1d")
                info = ticker.info
                
                if not hist.empty and len(hist) >= 2:
                    # 獲取最新價格
                    current = hist['Close'].iloc[-1]
                    
                    # 獲取前一交易日收盤價
                    prev_close = hist['Close'].iloc[-2]
                    
                    # 如果是期貨，嘗試獲取實時數據
                    if '=F' in symbol:
                        try:
                            # 嘗試獲取實時分鐘數據
                            real_time = ticker.history(period="1d", interval="1m")
                            if not real_time.empty:
                                current = real_time['Close'].iloc[-1]
                                # 使用info中的previousClose作為前收盤
                                if 'previousClose' in info and info['previousClose']:
                                    prev_close = info['previousClose']
                        except:
                            pass
                    
                    # 計算變化
                    change = current - prev_close
                    change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                    
                    # 獲取成交量
                    volume = hist['Volume'].iloc[-1] if 'Volume' in hist.columns and not hist['Volume'].isna().iloc[-1] else 0
                    
                    return {
                        'symbol': symbol_key,
                        'display_name': symbol_info['name'],
                        'price': float(current),
                        'change': float(change),
                        'change_pct': float(change_pct),
                        'volume': int(volume) if volume and not np.isnan(volume) else 0,
                        'prev_close': float(prev_close),
                        'high': float(hist['High'].iloc[-1]),
                        'low': float(hist['Low'].iloc[-1]),
                        'timestamp': datetime.now(),
                        'source': symbol,
                        'attempt': attempt
                    }
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {symbol}: {e}")
                continue
                
        return None
    
    # 並行獲取數據
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures_list = [executor.submit(fetch_precise_futures, k, v) for k, v in futures_symbols.items()]
        for future in futures_list:
            result = future.result()
            if result:
                futures_data[result['symbol']] = result
    
    return futures_data

@st.cache_data(ttl=60, show_spinner=False)
def get_enhanced_crypto_data():
    """獲取增強的加密貨幣數據"""
    crypto_symbols = {
        'BTC': 'BTC-USD',
        'ETH': 'ETH-USD',
        'USDT': 'USDT-USD'
    }
    
    crypto_data = {}
    
    def fetch_enhanced_crypto(symbol_key, symbol):
        try:
            ticker = yf.Ticker(symbol)
            
            # 獲取24小時數據
            hist = ticker.history(period="2d", interval="1h")
            info = ticker.info
            
            if not hist.empty and len(hist) >= 24:
                current = hist['Close'].iloc[-1]
                
                # 24小時前的價格
                prev_24h = hist['Close'].iloc[-24]
                
                change = current - prev_24h
                change_pct = (change / prev_24h) * 100 if prev_24h != 0 else 0
                
                volume_24h = hist['Volume'].sum() if 'Volume' in hist.columns else 0
                market_cap = info.get('marketCap', 0)
                
                return {
                    'symbol': symbol_key,
                    'price': float(current),
                    'change': float(change),
                    'change_pct': float(change_pct),
                    'volume': int(volume_24h) if volume_24h and not np.isnan(volume_24h) else 0,
                    'market_cap': int(market_cap) if market_cap else 0,
                    'high_24h': float(hist['High'].max()),
                    'low_24h': float(hist['Low'].min()),
                    'timestamp': datetime.now()
                }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
        return None
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(fetch_enhanced_crypto, k, v) for k, v in crypto_symbols.items()]
        for future in futures:
            result = future.result()
            if result:
                crypto_data[result['symbol']] = result
    
    return crypto_data

@st.cache_data(ttl=120, show_spinner=False)
def get_forex_commodities_bonds():
    """獲取外匯、商品、債券數據"""
    symbols = {
        'USDJPY': 'USDJPY=X',  
        'GOLD': 'GC=F',        
        'TNX': '^TNX'          
    }
    
    data = {}
    
    def fetch_asset(symbol_key, symbol):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d", interval="1d")
            
            if not hist.empty and len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                
                change = current - prev_close
                change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                
                volume = hist['Volume'].iloc[-1] if 'Volume' in hist.columns and not hist['Volume'].isna().iloc[-1] else 0
                
                return {
                    'symbol': symbol_key,
                    'price': float(current),
                    'change': float(change),
                    'change_pct': float(change_pct),
                    'volume': int(volume) if volume and not np.isnan(volume) else 0,
                    'timestamp': datetime.now()
                }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
        return None
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(fetch_asset, k, v) for k, v in symbols.items()]
        for future in futures:
            result = future.result()
            if result:
                data[result['symbol']] = result
    
    return data

@st.cache_data(ttl=300, show_spinner=False)
def get_enhanced_hot_stocks():
    """獲取熱門股票數據"""
    popular_stocks = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX',
        'COIN', 'AMD', 'BABA', 'PLTR', 'MSTR', 'RIOT', 'GME', 'AMC'
    ]
    
    stocks_data = []
    
    def fetch_stock(symbol):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d", interval="1d")
            info = ticker.info
            
            if not hist.empty and len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                
                change = current - prev_close
                change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                
                # 當日成交量
                volume = hist['Volume'].iloc[-1] if not hist['Volume'].isna().iloc[-1] else 0
                
                return {
                    'symbol': symbol,
                    'name': info.get('longName', symbol),
                    'price': float(current),
                    'change': float(change),
                    'change_pct': float(change_pct),
                    'volume': int(volume) if volume and not np.isnan(volume) else 0,
                    'market_cap': info.get('marketCap', 0),
                    'timestamp': datetime.now()
                }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
        return None
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_stock, symbol) for symbol in popular_stocks]
        for future in futures:
            result = future.result()
            if result and result['volume'] > 0:
                stocks_data.append(result)
    
    stocks_data.sort(key=lambda x: x['volume'], reverse=True)
    return stocks_data[:12]

# ====== 優化的專業交易平台設計 ======
def load_optimized_professional_design():
    """載入優化的專業交易平台設計"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        /* 重置預設樣式 */
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
            background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 100%);
            position: relative;
        }
        
        #MainMenu, footer, header, .stDeployButton, .stDecoration {
            visibility: hidden !important;
            height: 0 !important;
        }
        
        .stApp {
            margin-top: -100px !important;
            background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 100%);
            min-height: 100vh;
            position: relative;
        }
        
        /* 優化的背景浮水印 */
        .stApp::after {
            content: '';
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(59,130,246,0.05) 0%, transparent 70%);
            border: 3px solid rgba(59,130,246,0.08);
            border-radius: 50%;
            z-index: 0;
            pointer-events: none;
        }
        
        .stApp::before {
            content: 'TENKI';
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 5rem;
            font-weight: 900;
            color: rgba(59,130,246,0.04);
            z-index: 0;
            pointer-events: none;
            text-shadow: 0 0 100px rgba(59,130,246,0.1);
            letter-spacing: 0.2em;
        }
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        /* 主內容區域 */
        .main-content {
            padding: 1rem;
            background: transparent;
            color: white;
            position: relative;
            z-index: 10;
        }
        
        /* 大幅優化的頂部橫幅 - 突出TENKI品牌 */
        .brand-banner {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 2rem 1.5rem;
            border-radius: 20px;
            margin-bottom: 1.5rem;
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(59, 130, 246, 0.3);
            position: relative;
            overflow: hidden;
            z-index: 10;
        }
        
        .brand-banner::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #3b82f6, #1d4ed8, #3b82f6);
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
        }
        
        /* TENKI品牌展示區 */
        .tenki-brand {
            display: flex;
            align-items: center;
            gap: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .tenki-logo-large {
            flex-shrink: 0;
        }
        
        .tenki-text {
            flex: 1;
        }
        
        .tenki-title {
            font-size: clamp(2.5rem, 8vw, 4rem);
            font-weight: 900;
            color: #f1f5f9;
            margin-bottom: 0.5rem;
            text-shadow: 0 4px 8px rgba(0,0,0,0.3);
            letter-spacing: -0.02em;
        }
        
        .tenki-subtitle {
            font-size: clamp(1.1rem, 4vw, 1.4rem);
            color: #94a3b8;
            margin-bottom: 1rem;
            font-weight: 500;
        }
        
        /* 市場狀態指示器 */
        .market-status {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.6rem 1.2rem;
            background: rgba(34, 197, 94, 0.25);
            border-radius: 25px;
            font-size: 0.85rem;
            font-weight: 700;
            border: 2px solid rgba(34, 197, 94, 0.3);
        }
        
        .market-status.closed {
            background: rgba(239, 68, 68, 0.25);
            color: #fca5a5;
            border-color: rgba(239, 68, 68, 0.3);
        }
        
        .market-status.open {
            background: rgba(34, 197, 94, 0.25);
            color: #86efac;
            border-color: rgba(34, 197, 94, 0.3);
        }
        
        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: currentColor;
            animation: blink 1.5s ease-in-out infinite;
        }
        
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0.3; }
        }
        
        /* 交易面板標題 */
        .trading-section {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            padding: 1.2rem;
            border-radius: 12px;
            margin: 1.5rem 0 0.8rem 0;
            text-align: center;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(148, 163, 184, 0.2);
            position: relative;
            overflow: hidden;
            z-index: 10;
        }
        
        .trading-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            animation: shine 3s ease-in-out infinite;
        }
        
        @keyframes shine {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .trading-section h3 {
            font-size: 1.2rem;
            font-weight: 800;
            margin: 0;
            color: #e2e8f0;
            text-shadow: 0 1px 2px rgba(0,0,0,0.5);
        }
        
        /* 增強的數據卡片 */
        div[data-testid="metric-container"] {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-radius: 16px;
            padding: 1.8rem !important;
            border: 1px solid rgba(148, 163, 184, 0.15);
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.25);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            z-index: 10;
        }
        
        div[data-testid="metric-container"]:hover {
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 15px 50px rgba(59, 130, 246, 0.2);
            border-color: rgba(59, 130, 246, 0.4);
        }
        
        div[data-testid="metric-container"]::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #3b82f6, #1d4ed8);
        }
        
        /* 指標樣式優化 */
        div[data-testid="metric-container"] label {
            color: #94a3b8 !important;
            font-size: 0.8rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin-bottom: 0.8rem !important;
        }
        
        div[data-testid="metric-container"] > div > div {
            color: #f1f5f9 !important;
            font-weight: 800 !important;
            font-size: 2rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* 漲跌幅顏色 */
        div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
            font-weight: 700 !important;
            font-size: 1rem !important;
        }
        
        /* 股票卡片優化 */
        .stock-card {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-radius: 16px;
            padding: 1.8rem;
            margin: 1rem 0;
            border: 1px solid rgba(148, 163, 184, 0.15);
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.25);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            z-index: 10;
        }
        
        .stock-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 50px rgba(59, 130, 246, 0.15);
            border-color: rgba(59, 130, 246, 0.3);
        }
        
        .stock-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 5px;
            height: 100%;
            background: linear-gradient(180deg, #3b82f6, #1d4ed8);
        }
        
        .stock-rank {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 25px;
            font-size: 0.75rem;
            font-weight: 800;
            display: inline-block;
            margin-bottom: 0.8rem;
        }
        
        .stock-symbol {
            color: #f1f5f9;
            font-size: 1.3rem;
            font-weight: 800;
            margin-bottom: 0.3rem;
        }
        
        .stock-name {
            color: #94a3b8;
            font-size: 0.85rem;
            margin-bottom: 1.2rem;
        }
        
        .stock-price {
            color: #f1f5f9;
            font-size: 1.5rem;
            font-weight: 800;
            margin-bottom: 0.6rem;
        }
        
        .positive {
            color: #22c55e !important;
        }
        
        .negative {
            color: #ef4444 !important;
        }
        
        /* 控制區域優化 */
        .controls-section {
            background: rgba(30, 41, 59, 0.9);
            backdrop-filter: blur(15px);
            border-radius: 16px;
            padding: 1.2rem;
            margin: 1rem 0;
            border: 1px solid rgba(148, 163, 184, 0.2);
            z-index: 10;
            position: relative;
        }
        
        /* 時間戳樣式 */
        .timestamp {
            color: #64748b;
            font-size: 0.85rem;
            text-align: center;
            margin: 0.8rem 0;
            background: rgba(15, 23, 42, 0.6);
            padding: 0.8rem;
            border-radius: 10px;
            font-weight: 600;
        }
        
        /* 響應式設計 */
        @media (max-width: 768px) {
            .main-content {
                padding: 0.5rem;
            }
            
            .brand-banner {
                padding: 1.5rem 1rem;
            }
            
            .tenki-brand {
                flex-direction: column;
                text-align: center;
                gap: 1rem;
            }
            
            .tenki-title {
                font-size: 2.5rem;
            }
            
            .tenki-subtitle {
                font-size: 1rem;
            }
            
            .stApp::before {
                font-size: 3rem;
            }
            
            .stApp::after {
                width: 300px;
                height: 300px;
            }
        }
        
        @media (max-width: 480px) {
            .main-content {
                padding: 0.3rem;
            }
            
            .brand-banner {
                padding: 1rem;
            }
            
            .tenki-title {
                font-size: 2rem;
            }
            
            div[data-testid="metric-container"] > div > div {
                font-size: 1.6rem !important;
            }
            
            .stApp::before {
                font-size: 2.5rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def create_optimized_brand_banner():
    """創建優化的品牌橫幅 - 突出TENKI形象"""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<div class="brand-banner">', unsafe_allow_html=True)
    
    # TENKI品牌展示區
    st.markdown('<div class="tenki-brand">', unsafe_allow_html=True)
    
    # Logo區域
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="tenki-logo-large">', unsafe_allow_html=True)
        
        # 嘗試載入您的Logo圖片，並放大尺寸
        logo_loaded = False
        for img_name in ["IMG_0638.png", "IMG_0639.jpeg", "IMG_0640.jpeg"]:
            try:
                st.image(img_name, width=200)  # 從120px增加到200px
                logo_loaded = True
                break
            except:
                continue
        
        if not logo_loaded:
            # 備用Logo - 更大更突出
            st.markdown("""
            <div style="text-align: center;">
                <div style="width: 120px; height: 120px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); 
                            border-radius: 50%; display: flex; align-items: center; justify-content: center;
                            box-shadow: 0 15px 40px rgba(59, 130, 246, 0.4); margin: 0 auto;
                            border: 3px solid rgba(255, 255, 255, 0.2);">
                    <span style="color: white; font-size: 2.5rem; font-weight: 900;">T</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        lang = st.session_state.language
        t = TEXTS[lang]
        
        st.markdown('<div class="tenki-text">', unsafe_allow_html=True)
        st.markdown(f'<h1 class="tenki-title">TENKI</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="tenki-subtitle">{t["tagline"]}</p>', unsafe_allow_html=True)
        
        # 市場狀態
        market_status_class = 'open' if is_market_open() else 'closed'
        st.markdown(f"""
        <div class="market-status {market_status_class}">
            <div class="status-dot"></div>
            {get_market_status(t)}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # 關閉tenki-brand
    st.markdown('</div>', unsafe_allow_html=True)  # 關閉brand-banner

def create_enhanced_trading_section(title, data, t, asset_type="default"):
    """創建增強的交易數據區域"""
    st.markdown(f'<div class="trading-section"><h3>📊 {title}</h3></div>', unsafe_allow_html=True)
    
    if not data:
        st.warning(f"{t['loading']} {title}")
        return
    
    # 根據數據數量決定列數
    if len(data) <= 3:
        cols = st.columns(len(data))
    else:
        cols = st.columns(3)
    
    for i, (symbol, info) in enumerate(data.items()):
        if i < len(cols):
            with cols[i]:
                # 根據資產類型決定顯示格式
                if asset_type == "futures":
                    # 期貨顯示格式 - 使用display_name
                    display_name = info.get('display_name', get_localized_name(symbol, t))
                    delta_str = f"{info['change']:+.2f} ({info['change_pct']:+.2f}%)"
                    price_str = f"{info['price']:,.2f}"
                elif asset_type == "crypto" and info.get('market_cap', 0) > 0:
                    market_cap_str = f"${info['market_cap']/1e9:.1f}B" if info['market_cap'] > 1e9 else f"${info['market_cap']/1e6:.1f}M"
                    delta_str = f"{info['change']:+.2f} ({info['change_pct']:+.2f}%)"
                    display_name = get_localized_name(symbol, t)
                elif asset_type == "forex":
                    delta_str = f"{info['change']:+.4f} ({info['change_pct']:+.2f}%)"
                    price_str = f"{info['price']:.4f}"
                    display_name = get_localized_name(symbol, t)
                else:
                    delta_str = f"{info['change']:+.2f} ({info['change_pct']:+.2f}%)"
                    price_str = f"{info['price']:,.2f}"
                    display_name = get_localized_name(symbol, t)
                
                # 顯示指標
                if asset_type == "forex":
                    st.metric(
                        label=display_name,
                        value=price_str,
                        delta=delta_str
                    )
                else:
                    st.metric(
                        label=display_name,
                        value=f"${info['price']:,.2f}",
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

def create_enhanced_hot_stocks_section(stocks_data, t):
    """創建增強的熱門股票區域"""
    st.markdown(f'<div class="trading-section"><h3>🔥 {t["hot_stocks"]} (成交量排序)</h3></div>', unsafe_allow_html=True)
    
    if not stocks_data:
        st.warning(f"{t['loading']} {t['hot_stocks']}")
        return
    
    for i, stock in enumerate(stocks_data[:10], 1):
        with st.container():
            st.markdown('<div class="stock-card">', unsafe_allow_html=True)
            
            st.markdown(f'<div class="stock-rank">#{i}</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f'<div class="stock-symbol">{stock["symbol"]}</div>', unsafe_allow_html=True)
                stock_name = stock["name"][:35] + "..." if len(stock["name"]) > 35 else stock["name"]
                st.markdown(f'<div class="stock-name">{stock_name}</div>', unsafe_allow_html=True)
            
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
    st.markdown(f'<div class="trading-section"><h3>🌐 {t["language"]}</h3></div>', unsafe_allow_html=True)
    
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
    # 載入優化的專業交易平台設計
    load_optimized_professional_design()
    
    # 獲取當前語言設定
    lang = st.session_state.language
    t = TEXTS[lang]
    
    # 優化的品牌橫幅 - 突出TENKI
    create_optimized_brand_banner()
    
    # 語言選擇器
    language_selector(t)
    
    # 數據刷新控制區域
    st.markdown('<div class="controls-section">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button(f"🔄 {t['refresh']}", use_container_width=True, type="primary"):
            st.cache_data.clear()
            st.session_state.last_refresh = datetime.now()
            st.session_state.refresh_counter += 1
            st.rerun()
    
    with col2:
        auto_refresh = st.checkbox(f"⚡ {t['auto_refresh']}", value=st.session_state.auto_refresh)
        st.session_state.auto_refresh = auto_refresh
    
    # 顯示最後更新時間
    st.markdown(f'<div class="timestamp">{t["last_update"]}: {st.session_state.last_refresh.strftime("%H:%M:%S")} | 刷新次數: {st.session_state.refresh_counter}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 數據載入狀態
    with st.spinner(f"{t['loading']} {t['real_time_data']}..."):
        
        # 並行載入所有數據
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures_future = executor.submit(get_accurate_futures_data)  # 使用精準的期貨數據
            crypto_future = executor.submit(get_enhanced_crypto_data)
            other_future = executor.submit(get_forex_commodities_bonds)
            stocks_future = executor.submit(get_enhanced_hot_stocks)
            
            # 獲取結果
            futures_data = futures_future.result()
            crypto_data = crypto_future.result()
            other_data = other_future.result()
            stocks_data = stocks_future.result()
    
    # 期貨指數區域 - 使用精準數據
    create_enhanced_trading_section(t['futures_indices'], futures_data, t, "futures")
    
    # 加密貨幣區域
    create_enhanced_trading_section(t['cryptocurrencies'], crypto_data, t, "crypto")
    
    # 外匯、商品、債券區域
    forex_data = {k: v for k, v in other_data.items() if k in ['USDJPY']}
    commodities_data = {k: v for k, v in other_data.items() if k in ['GOLD']}
    bonds_data = {k: v for k, v in other_data.items() if k in ['TNX']}
    
    if forex_data:
        create_enhanced_trading_section(t['forex'], forex_data, t, "forex")
    
    if commodities_data:
        create_enhanced_trading_section(t['commodities'], commodities_data, t, "others")
    
    if bonds_data:
        create_enhanced_trading_section(t['bonds'], bonds_data, t, "others")
    
    # 熱門股票區域
    create_enhanced_hot_stocks_section(stocks_data, t)
    
    # 底部資訊
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 1rem; color: #64748b; margin-top: 2rem; 
                border-top: 1px solid rgba(148, 163, 184, 0.2);">
        <p style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem; color: #e2e8f0;">
            <strong>TENKI</strong> - {t['tagline']}
        </p>
        <p style="margin-bottom: 1rem; color: #94a3b8;">© 2025 TENKI Professional Trading Platform</p>
        <p style="font-size: 0.8rem; opacity: 0.8;">
            數據來源: Yahoo Finance | 對標TradingView精準度 | 僅供投資參考
        </p>
    </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
