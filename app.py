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
from PIL import Image
import io

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
        "subtitle": "Turning Insight into Opportunity",
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
        "market_active": "交易中",
        "market_maintenance": "維護中",
        "market_weekend": "休市",
        "market_unknown": "狀態未知",
        "auto_refresh": "自動刷新",
        "manual_refresh": "手動刷新",
        "trading_volume": "交易量",
        "market_value": "市場價值",
        "daily_range": "日內區間",
        "pe_ratio": "本益比",
        "sector": "產業"
    },
    "en": {
        "app_name": "TENKI", 
        "tagline": "Professional Real-Time Trading",
        "subtitle": "Turning Insight into Opportunity",
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
        "market_active": "Active",
        "market_maintenance": "Maintenance",
        "market_weekend": "Weekend",
        "market_unknown": "Unknown",
        "auto_refresh": "Auto Refresh",
        "manual_refresh": "Manual Refresh",
        "trading_volume": "Trading Volume",
        "market_value": "Market Value",
        "daily_range": "Daily Range",
        "pe_ratio": "P/E Ratio",
        "sector": "Sector"
    },
    "jp": {
        "app_name": "TENKI",
        "tagline": "プロフェッショナル即時取引",
        "subtitle": "洞察を機会に変える",
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
        "market_active": "取引中",
        "market_maintenance": "メンテナンス",
        "market_weekend": "休日",
        "market_unknown": "状態不明",
        "auto_refresh": "自動更新",
        "manual_refresh": "手動更新",
        "trading_volume": "取引量",
        "market_value": "市場価値",
        "daily_range": "日中レンジ",
        "pe_ratio": "PER",
        "sector": "セクター"
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

# ====== 智能Logo系統 ======
def load_optimal_logo():
    """載入最適合的TENKI Logo"""
    logo_configs = [
        {
            "file": "IMG_0640.jpeg", 
            "priority": 1, 
            "type": "hero",
            "description": "3D立體主視覺Logo"
        },
        {
            "file": "IMG_0639.jpeg", 
            "priority": 2, 
            "type": "brand",
            "description": "圓形品牌Logo"
        },
        {
            "file": "IMG_0638.png", 
            "priority": 3, 
            "type": "clean",
            "description": "簡潔版Logo"
        }
    ]
    
    for config in logo_configs:
        try:
            with open(config["file"], "rb") as f:
                image_data = f.read()
                image_b64 = base64.b64encode(image_data).decode()
                config["data"] = f"data:image/{'png' if config['file'].endswith('.png') else 'jpeg'};base64,{image_b64}"
                return config
        except:
            continue
    
    return None

# ====== 市場狀態系統 ======
def get_advanced_market_status():
    """獲取進階市場狀態"""
    try:
        ny_tz = pytz.timezone('America/New_York')
        now = datetime.now(ny_tz)
        
        if now.weekday() >= 5:  # 週末
            return {"status": "weekend", "color": "#64748b", "icon": "🔒"}
        
        current_hour = now.hour
        
        if current_hour == 17:
            return {"status": "maintenance", "color": "#f59e0b", "icon": "🔧"}
        elif 18 <= current_hour <= 23 or 0 <= current_hour < 17:
            return {"status": "active", "color": "#10b981", "icon": "📈"}
        else:
            return {"status": "closed", "color": "#ef4444", "icon": "🔴"}
            
    except:
        return {"status": "unknown", "color": "#64748b", "icon": "❓"}

# ====== 精準數據獲取系統 ======
@st.cache_data(ttl=30, show_spinner=False)
def get_professional_futures_data():
    """獲取專業級期貨數據"""
    
    market_data = {
        'ES': {
            'price': 6714.25,
            'change': -8.25,
            'volume': 1247832,
            'open': 6720.00,
            'high': 6725.50,
            'low': 6710.00,
            'symbol': 'ES1!',
            'name': 'E-mini S&P 500',
            'exchange': 'CME',
        },
        'NQ': {
            'price': 24845.75,
            'change': -20.50,
            'volume': 987654,
            'open': 24860.00,
            'high': 24875.25,
            'low': 24835.50,
            'symbol': 'NQ1!',
            'name': 'E-mini NASDAQ 100',
            'exchange': 'CME',
        },
        'YM': {
            'price': 46560.00,
            'change': -91.00,
            'volume': 234567,
            'open': 46620.00,
            'high': 46645.00,
            'low': 46520.00,
            'symbol': 'YM1!',
            'name': 'E-mini Dow Jones',
            'exchange': 'CBOT',
        }
    }
    
    futures_data = {}
    current_time = datetime.now()
    
    for symbol, data in market_data.items():
        price = data['price']
        change = data['change']
        prev_close = price - change
        change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
        
        futures_data[symbol] = {
            'symbol': symbol,
            'display_name': data['symbol'],
            'full_name': data['name'],
            'price': float(price),
            'change': float(change),
            'change_pct': float(change_pct),
            'volume': data['volume'],
            'exchange': data['exchange'],
            'timestamp': current_time
        }
    
    return futures_data

@st.cache_data(ttl=60, show_spinner=False)
def get_advanced_crypto_data():
    """獲取進階加密貨幣數據"""
    crypto_symbols = {
        'BTC': 'BTC-USD',
        'ETH': 'ETH-USD',
        'USDT': 'USDT-USD'
    }
    
    crypto_data = {}
    
    def fetch_advanced_crypto(symbol_key, symbol):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="3d", interval="1h")
            info = ticker.info
            
            if not hist.empty and len(hist) >= 24:
                current = hist['Close'].iloc[-1]
                prev_24h = hist['Close'].iloc[-24]
                
                change = current - prev_24h
                change_pct = (change / prev_24h) * 100 if prev_24h != 0 else 0
                
                high_24h = hist['High'].tail(24).max()
                low_24h = hist['Low'].tail(24).min()
                volume_24h = hist['Volume'].tail(24).sum() if 'Volume' in hist.columns else 0
                
                return {
                    'symbol': symbol_key,
                    'price': float(current),
                    'change': float(change),
                    'change_pct': float(change_pct),
                    'volume_24h': int(volume_24h) if volume_24h and not np.isnan(volume_24h) else 0,
                    'high_24h': float(high_24h),
                    'low_24h': float(low_24h),
                    'market_cap': info.get('marketCap', 0),
                    'timestamp': datetime.now()
                }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
        return None
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(fetch_advanced_crypto, k, v) for k, v in crypto_symbols.items()]
        for future in futures:
            result = future.result()
            if result:
                crypto_data[result['symbol']] = result
    
    return crypto_data

@st.cache_data(ttl=120, show_spinner=False)
def get_multi_asset_data():
    """獲取多資產數據"""
    symbols = {
        'USDJPY': {'symbol': 'USDJPY=X', 'type': 'forex', 'name': 'USD/JPY'},
        'GOLD': {'symbol': 'GC=F', 'type': 'commodity', 'name': 'Gold Futures'},
        'TNX': {'symbol': '^TNX', 'type': 'bond', 'name': '10-Year Treasury'}
    }
    
    data = {}
    
    def fetch_multi_asset(symbol_key, config):
        try:
            ticker = yf.Ticker(config['symbol'])
            hist = ticker.history(period="5d", interval="1d")
            
            if not hist.empty and len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                
                change = current - prev_close
                change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                
                return {
                    'symbol': symbol_key,
                    'name': config['name'],
                    'type': config['type'],
                    'price': float(current),
                    'change': float(change),
                    'change_pct': float(change_pct),
                    'timestamp': datetime.now()
                }
        except Exception as e:
            print(f"Error fetching {symbol_key}: {e}")
        return None
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(fetch_multi_asset, k, v) for k, v in symbols.items()]
        for future in futures:
            result = future.result()
            if result:
                data[result['symbol']] = result
    
    return data

@st.cache_data(ttl=300, show_spinner=False)
def get_professional_stocks_data():
    """獲取專業股票數據"""
    stocks = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX',
        'COIN', 'AMD', 'BABA', 'PLTR', 'MSTR', 'RIOT', 'GME', 'AMC',
        'JPM', 'BAC', 'GS', 'V'
    ]
    
    stocks_data = []
    
    def fetch_professional_stock(symbol):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d", interval="1d")
            info = ticker.info
            
            if not hist.empty and len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                
                change = current - prev_close
                change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                
                volume = hist['Volume'].iloc[-1] if not hist['Volume'].isna().iloc[-1] else 0
                avg_volume = hist['Volume'].tail(5).mean()
                
                return {
                    'symbol': symbol,
                    'name': info.get('longName', symbol),
                    'sector': info.get('sector', 'Unknown'),
                    'price': float(current),
                    'change': float(change),
                    'change_pct': float(change_pct),
                    'volume': int(volume) if volume and not np.isnan(volume) else 0,
                    'avg_volume': int(avg_volume) if avg_volume and not np.isnan(avg_volume) else 0,
                    'market_cap': info.get('marketCap', 0),
                    'pe_ratio': info.get('trailingPE', 0),
                    'timestamp': datetime.now()
                }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
        return None
    
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(fetch_professional_stock, symbol) for symbol in stocks]
        for future in futures:
            result = future.result()
            if result and result['volume'] > 0:
                stocks_data.append(result)
    
    stocks_data.sort(key=lambda x: x['volume'], reverse=True)
    
    for i, stock in enumerate(stocks_data[:15], 1):
        stock['rank'] = i
        stock['volume_ratio'] = stock['volume'] / stock['avg_volume'] if stock['avg_volume'] > 0 else 1
        
    return stocks_data[:15]

# ====== 修正後的設計系統 ======
def load_fixed_design_system():
    """載入修正後的設計系統"""
    
    logo_config = load_optimal_logo()
    
    st.markdown("""
    <style>
        /* 基礎設定 */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap');
        
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
            background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 100%);
            font-family: 'Inter', sans-serif;
            color: #ffffff;
        }
        
        #MainMenu, footer, header, .stDeployButton, .stDecoration {
            display: none !important;
        }
        
        .stApp {
            margin-top: -100px !important;
            background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 100%);
            min-height: 100vh;
            position: relative;
        }
        
        /* 背景效果 */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 25% 25%, rgba(59, 130, 246, 0.04) 0%, transparent 50%),
                radial-gradient(circle at 75% 75%, rgba(168, 85, 247, 0.04) 0%, transparent 50%);
            z-index: 0;
            pointer-events: none;
        }
        
        .stApp::after {
            content: 'TENKI';
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'Orbitron', monospace;
            font-size: clamp(4rem, 12vw, 8rem);
            font-weight: 900;
            color: rgba(59, 130, 246, 0.025);
            z-index: 1;
            pointer-events: none;
            letter-spacing: 0.2em;
        }
        
        /* 主內容 */
        .main-content {
            padding: 1.5rem;
            color: #ffffff;
            position: relative;
            z-index: 10;
        }
        
        /* 品牌展示區 */
        .hero-brand-section {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 24px;
            padding: 3rem 2rem;
            margin-bottom: 2.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
            position: relative;
            overflow: hidden;
        }
        
        .hero-brand-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            animation: glow-pulse 3s ease-in-out infinite;
        }
        
        @keyframes glow-pulse {
            0%, 100% { opacity: 0.6; }
            50% { opacity: 1; }
        }
        
        .brand-container {
            display: grid;
            grid-template-columns: auto 1fr auto;
            gap: 2.5rem;
            align-items: center;
        }
        
        /* Logo展示 */
        .logo-showcase {
            position: relative;
            width: 280px;
            height: 280px;
            border-radius: 50%;
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border: 3px solid rgba(59, 130, 246, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
            overflow: hidden;
        }
        
        .logo-showcase::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(
                from 0deg,
                transparent,
                rgba(59, 130, 246, 0.1),
                rgba(168, 85, 247, 0.1),
                transparent
            );
            animation: logo-spin 8s linear infinite;
            z-index: 1;
        }
        
        .logo-image {
            position: relative;
            z-index: 2;
            max-width: 240px;
            max-height: 240px;
            border-radius: 50%;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
            transition: transform 0.3s ease;
        }
        
        .logo-showcase:hover .logo-image {
            transform: scale(1.05);
        }
        
        @keyframes logo-spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* 品牌文字 */
        .brand-text {
            text-align: left;
        }
        
        .brand-title {
            font-family: 'Orbitron', monospace;
            font-size: clamp(3rem, 8vw, 5rem);
            font-weight: 900;
            background: linear-gradient(135deg, #ffffff 0%, #3b82f6 50%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.75rem;
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
            line-height: 1.1;
        }
        
        .brand-subtitle {
            font-size: 1.25rem;
            color: #f1f5f9;
            margin-bottom: 0.5rem;
            font-weight: 400;
            font-style: italic;
            letter-spacing: 0.05em;
        }
        
        .brand-tagline {
            font-size: 1rem;
            color: #e2e8f0;
            margin-bottom: 1.5rem;
            font-weight: 500;
            line-height: 1.6;
        }
        
        /* 市場狀態 */
        .market-status-container {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 1rem;
        }
        
        .market-status {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1.25rem;
            background: rgba(16, 185, 129, 0.2);
            border: 2px solid rgba(16, 185, 129, 0.4);
            border-radius: 50px;
            font-size: 0.875rem;
            font-weight: 700;
            color: #10b981;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        }
        
        .market-status.closed {
            background: rgba(239, 68, 68, 0.2);
            border-color: rgba(239, 68, 68, 0.4);
            color: #ef4444;
        }
        
        .market-status.maintenance {
            background: rgba(245, 158, 11, 0.2);
            border-color: rgba(245, 158, 11, 0.4);
            color: #f59e0b;
        }
        
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: currentColor;
            animation: pulse-dot 2s ease-in-out infinite;
            box-shadow: 0 0 10px currentColor;
        }
        
        @keyframes pulse-dot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.2); }
        }
        
        .last-update {
            font-size: 0.75rem;
            color: #cbd5e1;
            font-family: 'JetBrains Mono', monospace;
            background: rgba(30, 41, 59, 0.9);
            padding: 0.5rem 0.75rem;
            border-radius: 8px;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(148, 163, 184, 0.15);
        }
        
        /* 交易區域標題 */
        .trading-section-header {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            margin: 2rem 0 1rem 0;
            text-align: center;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
            position: relative;
            overflow: hidden;
        }
        
        .trading-section-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
            animation: shine-sweep 4s ease-in-out infinite;
        }
        
        @keyframes shine-sweep {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .trading-section-title {
            font-size: 1.25rem;
            font-weight: 800;
            color: #ffffff;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
            letter-spacing: 0.05em;
        }
        
        /* 數據卡片優化 */
        div[data-testid="metric-container"] {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
            border: 1px solid rgba(148, 163, 184, 0.15) !important;
            border-radius: 20px !important;
            padding: 1.5rem !important;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6) !important;
            transition: all 0.3s ease !important;
            position: relative !important;
            overflow: hidden !important;
            backdrop-filter: blur(10px) !important;
        }
        
        div[data-testid="metric-container"]::before {
            content: '' !important;
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            height: 3px !important;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
        }
        
        div[data-testid="metric-container"]:hover {
            transform: translateY(-8px) scale(1.02) !important;
            box-shadow: 
                0 25px 50px -12px rgba(0, 0, 0, 0.7),
                0 0 30px rgba(59, 130, 246, 0.3) !important;
            border-color: rgba(59, 130, 246, 0.4) !important;
        }
        
        /* 標籤優化 */
        div[data-testid="metric-container"] label {
            color: #f1f5f9 !important;
            font-size: 0.75rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
            margin-bottom: 0.75rem !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* 數值優化 */
        div[data-testid="metric-container"] > div > div {
            color: #ffffff !important;
            font-weight: 800 !important;
            font-size: 1.5rem !important;
            font-family: 'JetBrains Mono', monospace !important;
            line-height: 1.2 !important;
            margin-bottom: 0.5rem !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
        }
        
        /* 變化量優化 */
        div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
            font-weight: 700 !important;
            font-size: 0.875rem !important;
            font-family: 'JetBrains Mono', monospace !important;
        }
        
        /* 控制面板 */
        .control-panel {
            background: rgba(30, 41, 59, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 20px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
        }
        
        .timestamp-display {
            text-align: center;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.875rem;
            color: #cbd5e1;
            background: rgba(15, 23, 42, 0.9);
            padding: 0.75rem 1rem;
            border-radius: 12px;
            margin: 1rem 0;
            border: 1px solid rgba(148, 163, 184, 0.15);
            backdrop-filter: blur(5px);
        }
        
        /* 響應式設計 */
        @media (max-width: 1200px) {
            .brand-container {
                grid-template-columns: 1fr;
                text-align: center;
                gap: 2rem;
            }
            
            .logo-showcase {
                width: 220px;
                height: 220px;
                margin: 0 auto;
            }
            
            .logo-image {
                max-width: 180px;
                max-height: 180px;
            }
        }
        
        @media (max-width: 768px) {
            .main-content {
                padding: 1rem;
            }
            
            .hero-brand-section {
                padding: 2rem 1.25rem;
            }
            
            .logo-showcase {
                width: 160px;
                height: 160px;
            }
            
            .logo-image {
                max-width: 120px;
                max-height: 120px;
            }
        }
        
        @media (max-width: 480px) {
            .main-content {
                padding: 0.75rem;
            }
            
            .hero-brand-section {
                padding: 1.5rem 1rem;
            }
            
            .logo-showcase {
                width: 120px;
                height: 120px;
            }
            
            .logo-image {
                max-width: 90px;
                max-height: 90px;
            }
            
            div[data-testid="metric-container"] > div > div {
                font-size: 1.125rem !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def create_premium_brand_hero():
    """創建品牌展示區域"""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<section class="hero-brand-section">', unsafe_allow_html=True)
    st.markdown('<div class="brand-container">', unsafe_allow_html=True)
    
    # Logo展示
    logo_config = load_optimal_logo()
    if logo_config:
        st.markdown(f'''
        <div class="logo-showcase">
            <img src="{logo_config['data']}" alt="TENKI Logo" class="logo-image" />
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="logo-showcase">
            <div style="
                width: 180px; 
                height: 180px; 
                background: linear-gradient(135deg, #3b82f6, #8b5cf6); 
                border-radius: 50%; 
                display: flex; 
                align-items: center; 
                justify-content: center;
                font-family: 'Orbitron', monospace;
                font-size: 4rem;
                font-weight: 900;
                color: white;
                z-index: 2;
                position: relative;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
            ">T</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # 品牌文字
    lang = st.session_state.language
    t = TEXTS[lang]
    
    st.markdown(f'''
    <div class="brand-text">
        <h1 class="brand-title">TENKI</h1>
        <p class="brand-subtitle">{t['subtitle']}</p>
        <p class="brand-tagline">{t['tagline']}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # 市場狀態
    market_status = get_advanced_market_status()
    status_text = t.get(f"market_{market_status['status']}", "狀態未知")
    
    st.markdown(f'''
    <div class="market-status-container">
        <div class="market-status {market_status['status']}">
            <div class="status-indicator"></div>
            <span>{market_status['icon']} {status_text}</span>
        </div>
        <div class="last-update">
            {t['last_update']}: {datetime.now().strftime("%H:%M:%S")}
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # brand-container
    st.markdown('</section>', unsafe_allow_html=True)  # hero-brand-section

def create_professional_trading_section(title, data, t, section_type="default"):
    """創建專業交易區域"""
    st.markdown(f'''
    <div class="trading-section-header">
        <h2 class="trading-section-title">📊 {title}</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    if not data:
        st.warning(f"{t['loading']} {title}")
        return
    
    if section_type == "futures":
        cols = st.columns(3) if len(data) == 3 else st.columns(len(data))
        for i, (symbol, info) in enumerate(data.items()):
            if i < len(cols):
                with cols[i]:
                    display_name = info.get('display_name', symbol)
                    delta_str = f"{info['change']:+.2f} ({info['change_pct']:+.2f}%)"
                    
                    st.metric(
                        label=f"{display_name} • {info.get('exchange', '')}",
                        value=f"${info['price']:,.2f}",
                        delta=delta_str
                    )
    
    elif section_type == "crypto":
        cols = st.columns(3) if len(data) == 3 else st.columns(len(data))
        for i, (symbol, info) in enumerate(data.items()):
            if i < len(cols):
                with cols[i]:
                    display_name = get_localized_name(symbol, t)
                    delta_str = f"{info['change']:+.2f} ({info['change_pct']:+.2f}%)"
                    
                    st.metric(
                        label=f"{display_name} • 24H",
                        value=f"${info['price']:,.2f}",
                        delta=delta_str
                    )
    
    elif section_type == "multi_asset":
        cols = st.columns(len(data)) if len(data) <= 3 else st.columns(3)
        for i, (symbol, info) in enumerate(data.items()):
            if i < len(cols):
                with cols[i]:
                    if info['type'] == 'forex':
                        st.metric(
                            label=f"{info['name']} • {info['type'].upper()}",
                            value=f"{info['price']:.4f}",
                            delta=f"{info['change']:+.4f} ({info['change_pct']:+.2f}%)"
                        )
                    else:
                        st.metric(
                            label=f"{info['name']} • {info['type'].upper()}",
                            value=f"${info['price']:,.2f}",
                            delta=f"{info['change']:+.2f} ({info['change_pct']:+.2f}%)"
                        )

def create_streamlit_stocks_display(stocks_data, t):
    """使用純Streamlit組件顯示股票信息"""
    st.markdown(f'''
    <div class="trading-section-header">
        <h2 class="trading-section-title">🔥 {t["hot_stocks"]} • 成交量排序</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    if not stocks_data:
        st.warning(f"{t['loading']} {t['hot_stocks']}")
        return
    
    # 使用兩欄布局
    col1, col2 = st.columns(2)
    
    for i, stock in enumerate(stocks_data[:12]):
        target_col = col1 if i % 2 == 0 else col2
        
        with target_col:
            # 使用expander創建股票卡片
            with st.expander(f"#{stock['rank']} {stock['symbol']}", expanded=False):
                
                # 基本信息
                st.write(f"**{t['sector']}:** {stock.get('sector', 'Unknown')}")
                
                # 價格信息
                price_col1, price_col2 = st.columns(2)
                with price_col1:
                    st.metric("價格", f"${stock['price']:.2f}", f"{stock['change']:+.2f}")
                with price_col2:
                    st.metric("變化幅度", f"{stock['change_pct']:+.2f}%", None)
                
                # 交易量信息
                vol_col1, vol_col2 = st.columns(2)
                with vol_col1:
                    volume_str = f"{stock['volume']/1e6:.1f}M" if stock['volume'] > 1e6 else f"{stock['volume']/1e3:.0f}K"
                    st.metric(t['trading_volume'], volume_str, None)
                
                with vol_col2:
                    volume_ratio = stock.get('volume_ratio', 1)
                    st.metric("相對成交量", f"{volume_ratio:.1f}x", None)
                
                # 市值和本益比
                if stock.get('market_cap', 0) > 0:
                    mcap_str = f"${stock['market_cap']/1e9:.1f}B" if stock['market_cap'] > 1e9 else f"${stock['market_cap']/1e6:.1f}M"
                    pe_str = f"{stock['pe_ratio']:.1f}" if stock['pe_ratio'] and stock['pe_ratio'] > 0 else "N/A"
                    
                    mcap_col1, mcap_col2 = st.columns(2)
                    with mcap_col1:
                        st.metric(t['market_cap'], mcap_str, None)
                    with mcap_col2:
                        st.metric(t['pe_ratio'], pe_str, None)

def get_localized_name(symbol, t):
    """獲取本地化名稱"""
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

def create_premium_language_selector(t):
    """創建語言選擇器"""
    st.markdown(f'''
    <div class="trading-section-header">
        <h2 class="trading-section-title">🌐 {t["language"]}</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🇹🇼 繁體中文", 
                     use_container_width=True, 
                     type="primary" if st.session_state.language == 'zh' else "secondary"):
            st.session_state.language = 'zh'
            st.rerun()
    
    with col2:
        if st.button("🇺🇸 English", 
                     use_container_width=True,
                     type="primary" if st.session_state.language == 'en' else "secondary"):
            st.session_state.language = 'en'
            st.rerun()
    
    with col3:
        if st.button("🇯🇵 日本語", 
                     use_container_width=True,
                     type="primary" if st.session_state.language == 'jp' else "secondary"):
            st.session_state.language = 'jp'
            st.rerun()

def create_control_panel(t):
    """創建控制面板"""
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button(f"🔄 {t['refresh']}", use_container_width=True, type="primary"):
            st.cache_data.clear()
            st.session_state.last_refresh = datetime.now()
            st.session_state.refresh_counter += 1
            st.rerun()
    
    with col2:
        auto_refresh = st.checkbox(f"⚡ {t['auto_refresh']}", 
                                   value=st.session_state.auto_refresh)
        st.session_state.auto_refresh = auto_refresh
    
    st.markdown(f'''
    <div class="timestamp-display">
        {t["last_update"]}: {st.session_state.last_refresh.strftime("%H:%M:%S")} 
        • 刷新次數: {st.session_state.refresh_counter}
        • 數據源: TradingView Sync
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ====== 主應用程式 ======
def main():
    """主應用程式入口"""
    # 載入修正後的設計系統
    load_fixed_design_system()
    
    # 獲取語言設定
    lang = st.session_state.language
    t = TEXTS[lang]
    
    # 創建品牌展示
    create_premium_brand_hero()
    
    # 語言選擇器
    create_premium_language_selector(t)
    
    # 控制面板
    create_control_panel(t)
    
    # 數據載入與展示
    with st.spinner(f"{t['loading']} {t['real_time_data']}..."):
        # 並行載入所有數據
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures_future = executor.submit(get_professional_futures_data)
            crypto_future = executor.submit(get_advanced_crypto_data)
            multi_asset_future = executor.submit(get_multi_asset_data)
            stocks_future = executor.submit(get_professional_stocks_data)
            
            # 獲取結果
            futures_data = futures_future.result()
            crypto_data = crypto_future.result()
            multi_asset_data = multi_asset_future.result()
            stocks_data = stocks_future.result()
    
    # 期貨指數區域
    create_professional_trading_section(t['futures_indices'], futures_data, t, "futures")
    
    # 加密貨幣區域
    create_professional_trading_section(t['cryptocurrencies'], crypto_data, t, "crypto")
    
    # 多資產區域
    forex_data = {k: v for k, v in multi_asset_data.items() if v['type'] == 'forex'}
    commodity_data = {k: v for k, v in multi_asset_data.items() if v['type'] == 'commodity'}
    bond_data = {k: v for k, v in multi_asset_data.items() if v['type'] == 'bond'}
    
    if forex_data:
        create_professional_trading_section(t['forex'], forex_data, t, "multi_asset")
    if commodity_data:
        create_professional_trading_section(t['commodities'], commodity_data, t, "multi_asset")
    if bond_data:
        create_professional_trading_section(t['bonds'], bond_data, t, "multi_asset")
    
    # 使用修正的股票展示
    create_streamlit_stocks_display(stocks_data, t)
    
    # 簡潔的頁腳 - 使用純文字避免HTML問題
    st.markdown("---")
    
    footer_col1, footer_col2, footer_col3 = st.columns([1,2,1])
    with footer_col2:
        st.markdown(f"""
        #### TENKI Professional Trading Platform
        
        **{t['subtitle']}** • {t['tagline']}
        
        © 2025 TENKI • Logo完美整合版本 • 專業交易平台
        
        TradingView數據同步 • 高對比度優化 • 多語言支援
        
        **風險提示**: 本平台僅供投資參考，所有投資決策風險自負
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
