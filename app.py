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
        
        # 市場時間: 9:30 AM - 4:00 PM ET
        market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
        
        return market_open <= now <= market_close
    except:
        return True  # 預設假設市場開放

def get_market_status(t):
    """獲取市場狀態文字"""
    return t['market_open'] if is_market_open() else t['market_closed']

# ====== 修復的期貨數據獲取系統 ======
@st.cache_data(ttl=30, show_spinner=False)
def get_fixed_futures_data():
    """修復的期貨指數數據獲取 - 使用多重備援策略"""
    
    # 使用多個可能的期貨代碼進行備援
    futures_symbols = {
        'ES': ['ES=F', '^GSPC', 'SPY'],  # S&P 500 多重備援
        'NQ': ['NQ=F', '^IXIC', 'QQQ'],  # NASDAQ 多重備援  
        'YM': ['YM=F', '^DJI', 'DIA']    # Dow Jones 多重備援
    }
    
    futures_data = {}
    
    def fetch_futures_with_backup(symbol_key, symbol_list):
        """使用備援策略獲取期貨數據"""
        for symbol in symbol_list:
            try:
                ticker = yf.Ticker(symbol)
                
                # 嘗試獲取最新數據
                hist = ticker.history(period="5d", interval="1d")  # 改用日線數據
                info = ticker.info
                
                if not hist.empty and len(hist) >= 2:
                    current = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2]  # 前一交易日收盤價
                    
                    # 如果是期貨，嘗試獲取更準確的數據
                    if '=F' in symbol:
                        # 嘗試分鐘數據
                        minute_hist = ticker.history(period="1d", interval="1m")
                        if not minute_hist.empty:
                            current = minute_hist['Close'].iloc[-1]
                    
                    change = current - prev_close
                    change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                    
                    # 確保變化不為0（除非真的沒變化）
                    if abs(change) < 0.01:
                        # 嘗試使用盤前數據或延伸時間數據
                        extended_hist = ticker.history(period="2d", interval="1m")
                        if not extended_hist.empty and len(extended_hist) > 1:
                            current = extended_hist['Close'].iloc[-1]
                            prev_close = extended_hist['Close'].iloc[-390] if len(extended_hist) > 390 else extended_hist['Close'].iloc[0]
                            change = current - prev_close
                            change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                    
                    volume = hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0
                    
                    return {
                        'symbol': symbol_key,
                        'price': float(current),
                        'change': float(change),
                        'change_pct': float(change_pct),
                        'volume': int(volume) if volume and not np.isnan(volume) else 0,
                        'prev_close': float(prev_close),
                        'high': float(hist['High'].iloc[-1]),
                        'low': float(hist['Low'].iloc[-1]),
                        'timestamp': datetime.now(),
                        'source': symbol  # 記錄數據源
                    }
                
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                continue
                
        return None
    
    # 並行獲取數據
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures_list = [executor.submit(fetch_futures_with_backup, k, v) for k, v in futures_symbols.items()]
        for future in futures_list:
            result = future.result()
            if result:
                futures_data[result['symbol']] = result
    
    return futures_data

@st.cache_data(ttl=30, show_spinner=False)
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
            
            # 獲取最近的數據
            hist = ticker.history(period="2d", interval="1h")  # 使用小時數據更可靠
            if hist.empty:
                hist = ticker.history(period="5d", interval="1d")
            
            info = ticker.info
            
            if not hist.empty and len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                
                # 計算24小時變化
                day_ago_idx = max(0, len(hist) - 24) if len(hist) > 24 else 0
                prev_close = hist['Close'].iloc[day_ago_idx]
                
                change = current - prev_close
                change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                
                # 24小時成交量
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
    
    # 並行獲取數據
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(fetch_enhanced_crypto, k, v) for k, v in crypto_symbols.items()]
        for future in futures:
            result = future.result()
            if result:
                crypto_data[result['symbol']] = result
    
    return crypto_data

@st.cache_data(ttl=60, show_spinner=False)
def get_enhanced_forex_commodities_bonds():
    """獲取增強的外匯、商品、債券數據"""
    symbols = {
        'USDJPY': 'USDJPY=X',  
        'GOLD': 'GC=F',        
        'TNX': '^TNX'          
    }
    
    data = {}
    
    def fetch_enhanced_asset(symbol_key, symbol):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d", interval="1d")
            info = ticker.info
            
            if not hist.empty and len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                
                change = current - prev_close
                change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                
                volume = hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0
                
                return {
                    'symbol': symbol_key,
                    'price': float(current),
                    'change': float(change),
                    'change_pct': float(change_pct),
                    'volume': int(volume) if volume and not np.isnan(volume) else 0,
                    'high': float(hist['High'].iloc[-1]),
                    'low': float(hist['Low'].iloc[-1]),
                    'timestamp': datetime.now()
                }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
        return None
    
    # 並行獲取數據
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(fetch_enhanced_asset, k, v) for k, v in symbols.items()]
        for future in futures:
            result = future.result()
            if result:
                data[result['symbol']] = result
    
    return data

@st.cache_data(ttl=300, show_spinner=False)
def get_enhanced_hot_stocks():
    """獲取增強的熱門股票數據"""
    popular_stocks = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX',
        'COIN', 'AMD', 'BABA', 'PLTR', 'MSTR', 'RIOT', 'GME', 'AMC'
    ]
    
    stocks_data = []
    
    def fetch_enhanced_stock(symbol):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d", interval="1d")
            info = ticker.info
            
            if not hist.empty and len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                
                change = current - prev_close
                change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                
                # 獲取當日分鐘數據來計算成交量
                today_hist = ticker.history(period="1d", interval="1m")
                volume = today_hist['Volume'].sum() if not today_hist.empty else hist['Volume'].iloc[-1]
                
                return {
                    'symbol': symbol,
                    'name': info.get('longName', symbol),
                    'price': float(current),
                    'change': float(change),
                    'change_pct': float(change_pct),
                    'volume': int(volume) if volume and not np.isnan(volume) else 0,
                    'market_cap': info.get('marketCap', 0),
                    'high': float(hist['High'].iloc[-1]),
                    'low': float(hist['Low'].iloc[-1]),
                    'timestamp': datetime.now()
                }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
        return None
    
    # 並行獲取股票數據
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_enhanced_stock, symbol) for symbol in popular_stocks]
        for future in futures:
            result = future.result()
            if result and result['volume'] > 0:
                stocks_data.append(result)
    
    # 按成交量排序
    stocks_data.sort(key=lambda x: x['volume'], reverse=True)
    return stocks_data[:12]

# ====== 修復的專業交易平台設計系統 ======
def load_fixed_professional_design():
    """載入修復的專業交易平台設計"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        /* 重置預設樣式 */
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
            background: #0a0e1a;
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
        
        /* 修復的背景浮水印 */
        .stApp::after {
            content: '';
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 350px;
            height: 350px;
            background-image: radial-gradient(circle, rgba(59,130,246,0.08) 0%, transparent 70%);
            border: 2px solid rgba(59,130,246,0.1);
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
            font-size: 4rem;
            font-weight: 900;
            color: rgba(59,130,246,0.05);
            z-index: 0;
            pointer-events: none;
            text-shadow: 0 0 50px rgba(59,130,246,0.1);
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
        
        /* 頂部橫幅 - 專業交易風格 */
        .trading-banner {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 1.5rem;
            border-radius: 16px;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(59, 130, 246, 0.2);
            position: relative;
            overflow: hidden;
            z-index: 10;
        }
        
        .trading-banner::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #3b82f6, #1d4ed8, #3b82f6);
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
        }
        
        /* 市場狀態指示器 */
        .market-status {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: rgba(34, 197, 94, 0.2);
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-top: 1rem;
        }
        
        .market-status.closed {
            background: rgba(239, 68, 68, 0.2);
            color: #fca5a5;
        }
        
        .market-status.open {
            background: rgba(34, 197, 94, 0.2);
            color: #86efac;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
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
            padding: 1rem;
            border-radius: 12px;
            margin: 1.5rem 0 0.8rem 0;
            text-align: center;
            box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
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
            font-size: 1.1rem;
            font-weight: 700;
            margin: 0;
            color: #e2e8f0;
            text-shadow: 0 1px 2px rgba(0,0,0,0.5);
        }
        
        /* 增強的數據卡片 */
        div[data-testid="metric-container"] {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-radius: 16px;
            padding: 1.5rem !important;
            border: 1px solid rgba(148, 163, 184, 0.15);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            z-index: 10;
        }
        
        div[data-testid="metric-container"]:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 12px 40px rgba(59, 130, 246, 0.2);
            border-color: rgba(59, 130, 246, 0.3);
        }
        
        div[data-testid="metric-container"]::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #3b82f6, #1d4ed8);
        }
        
        /* 指標樣式 */
        div[data-testid="metric-container"] label {
            color: #94a3b8 !important;
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }
        
        div[data-testid="metric-container"] > div > div {
            color: #f1f5f9 !important;
            font-weight: 800 !important;
            font-size: 1.8rem !important;
        }
        
        /* 漲跌幅顏色優化 */
        div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
            font-weight: 700 !important;
            font-size: 0.9rem !important;
        }
        
        /* 股票卡片 */
        .stock-card {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 0.8rem 0;
            border: 1px solid rgba(148, 163, 184, 0.15);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            z-index: 10;
        }
        
        .stock-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(59, 130, 246, 0.15);
            border-color: rgba(59, 130, 246, 0.3);
        }
        
        .stock-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, #3b82f6, #1d4ed8);
        }
        
        /* 其餘樣式保持不變 */
        .stock-rank {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 700;
            display: inline-block;
            margin-bottom: 0.5rem;
        }
        
        .stock-symbol {
            color: #f1f5f9;
            font-size: 1.2rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }
        
        .stock-name {
            color: #94a3b8;
            font-size: 0.8rem;
            margin-bottom: 1rem;
        }
        
        .stock-price {
            color: #f1f5f9;
            font-size: 1.4rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        
        .positive {
            color: #22c55e !important;
        }
        
        .negative {
            color: #ef4444 !important;
        }
        
        /* 控制按鈕區域 */
        .controls-section {
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 1rem;
            margin: 1rem 0;
            border: 1px solid rgba(148, 163, 184, 0.2);
            z-index: 10;
            position: relative;
        }
        
        /* 時間戳樣式 */
        .timestamp {
            color: #64748b;
            font-size: 0.8rem;
            text-align: center;
            margin: 0.5rem 0;
            background: rgba(15, 23, 42, 0.5);
            padding: 0.5rem;
            border-radius: 8px;
        }
        
        /* 響應式設計 */
        @media (max-width: 768px) {
            .main-content {
                padding: 0.5rem;
            }
            
            .trading-banner {
                padding: 1rem;
            }
            
            .stApp::before {
                font-size: 3rem;
            }
            
            .stApp::after {
                width: 250px;
                height: 250px;
            }
        }
        
        @media (max-width: 480px) {
            .main-content {
                padding: 0.3rem;
            }
            
            .trading-section h3 {
                font-size: 1rem;
            }
            
            div[data-testid="metric-container"] > div > div {
                font-size: 1.5rem !important;
            }
            
            .stApp::before {
                font-size: 2rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def create_professional_banner():
    """創建專業交易平台頂部橫幅"""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<div class="trading-banner">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        try:
            # 嘗試載入您的Logo圖片
            for img_name in ["IMG_0638.png", "IMG_0639.jpeg", "IMG_0640.jpeg"]:
                try:
                    st.image(img_name, width=120)
                    break
                except:
                    continue
            else:
                # 備用Logo
                st.markdown("""
                <div style="text-align: center;">
                    <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); 
                                border-radius: 50%; display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3); margin: 0 auto;">
                        <span style="color: white; font-size: 1.8rem; font-weight: bold;">T</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        except:
            pass
    
    with col2:
        lang = st.session_state.language
        t = TEXTS[lang]
        
        st.markdown(f"""
        <div>
            <div style="font-size: 2.2rem; font-weight: 900; color: #f1f5f9; margin-bottom: 0.5rem; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                TENKI
            </div>
            <div style="font-size: 1rem; color: #94a3b8; margin-bottom: 0.5rem;">
                {t['tagline']}
            </div>
            <div class="market-status {'open' if is_market_open() else 'closed'}">
                <div class="status-dot"></div>
                {get_market_status(t)}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

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
                if asset_type == "crypto" and info.get('market_cap', 0) > 0:
                    market_cap_str = f"${info['market_cap']/1e9:.1f}B" if info['market_cap'] > 1e9 else f"${info['market_cap']/1e6:.1f}M"
                    delta_str = f"{info['change']:+.2f} ({info['change_pct']:+.2f}%)"
                elif asset_type == "forex":
                    delta_str = f"{info['change']:+.4f} ({info['change_pct']:+.2f}%)"
                    price_str = f"{info['price']:.4f}"
                else:
                    delta_str = f"{info['change']:+.2f} ({info['change_pct']:+.2f}%)"
                    price_str = f"{info['price']:,.2f}"
                
                # 獲取本地化名稱
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
    st.markdown(f'<div class="trading-section"><h3>🔥 {t["hot_stocks"]} (即時成交量排序)</h3></div>', unsafe_allow_html=True)
    
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
    # 載入修復的專業交易平台設計
    load_fixed_professional_design()
    
    # 獲取當前語言設定
    lang = st.session_state.language
    t = TEXTS[lang]
    
    # 專業交易平台頂部橫幅
    create_professional_banner()
    
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
            futures_future = executor.submit(get_fixed_futures_data)  # 使用修復的期貨數據函數
            crypto_future = executor.submit(get_enhanced_crypto_data)
            other_future = executor.submit(get_enhanced_forex_commodities_bonds)
            stocks_future = executor.submit(get_enhanced_hot_stocks)
            
            # 獲取結果
            futures_data = futures_future.result()
            crypto_data = crypto_future.result()
            other_data = other_future.result()
            stocks_data = stocks_future.result()
    
    # 期貨指數區域 - 使用修復的數據
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
        <p style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; color: #e2e8f0;">
            <strong>TENKI</strong> - {t['tagline']}
        </p>
        <p style="margin-bottom: 1rem; color: #94a3b8;">© 2025 TENKI Professional Trading Platform</p>
        <p style="font-size: 0.8rem; opacity: 0.8;">
            數據來源: Yahoo Finance | 期貨採用主力合約 | 僅供投資參考
        </p>
    </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
