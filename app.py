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
        "auto_refresh": "自動刷新",
        "manual_refresh": "手動刷新",
        "trend_chart": "趨勢圖"
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
        "auto_refresh": "Auto Refresh",
        "manual_refresh": "Manual Refresh",
        "trend_chart": "Trend Chart"
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
        "auto_refresh": "自動更新",
        "manual_refresh": "手動更新",
        "trend_chart": "トレンドチャート"
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

# ====== 圖片載入系統 ======
def load_tenki_logo():
    """載入TENKI Logo - 智能選擇最佳版本，並優化載入順序"""
    logo_files = [
        ("IMG_0638.png", "primary"),    # PNG版本優先（更高品質）
        ("IMG_0639.jpeg", "secondary"), # 立體圓形
