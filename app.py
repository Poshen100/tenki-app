import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime


# ------------------------
# 基本設定
# ------------------------
st.set_page_config(
    page_title="TENKI - Pivot Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 語言設置
LANGUAGES = {
    "🇹🇼 繁體中文": "zh",
    "🇺🇸 English": "en",
    "🇯🇵 日本語": "jp"
}
TEXTS = {
    "zh": {...},  # 省略，上文提供的繁中內容
    "en": {...},  # 省略，上文提供的英語內容
    "jp": {...},  # 省略，上文提供的日文內容
}

if "language" not in st.session_state:
    st.session_state.language = "zh"

# ------------------------
# 抓取即時價格API
# ------------------------
def fetch_live_price(symbol):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
    try:
        response = requests.get(url)
        result = response.json()
        quote = result["quoteResponse"]["result"][0]
        price = quote.get("regularMarketPrice", None)
        change = quote.get("regularMarketChange", None)
        change_percent = quote.get("regularMarketChangePercent", None)
        return price, change, change_percent / 100 if change_percent else None
    except:
        return None, None, None

def get_market_data():
    sp_prices = fetch_live_price("^GSPC")
    nasdaq_prices = fetch_live_price("^IXIC")
    dji_prices = fetch_live_price("^DJI")
    btc_prices = fetch_live_price("BTC-USD")

    data = {
        "indices": {
            "SP500": {"value": sp_prices[0], "change": sp_prices[1], "change_pct": sp_prices[2]},
            "NASDAQ": {"value": nasdaq_prices[0], "change": nasdaq_prices[1], "change_pct": nasdaq_prices[2]},
            "DJI": {"value": dji_prices[0], "change": dji_prices[1], "change_pct": dji_prices[2]},
            "BTC": {"value": btc_prices[0], "change": btc_prices[1], "change_pct": btc_prices[2]},
        },
        # 其他靜態資料省略
    }
    return data

# ------------------------
# CSS 與 UI 元件
# ------------------------
def load_style():
    st.markdown("""
    <style>
    /* 省略，貼入前面的頂級UI CSS */
    </style>
    """, unsafe_allow_html=True)

def create_navbar(t):
    st.markdown(f"""
    <div class="topnav">
        <img src="https://raw.githubusercontent.com/Poshen100/tenki/main/IMG_0640.jpeg" width="50" style="border-radius:8px;vertical-align:middle;">
        <span class="brand">{t['app_name']}</span>
    </div>
    """, unsafe_allow_html=True)

def language_selector():
    cols = st.columns(3)
    langs = list(LANGUAGES.items())
    for i, (name, code) in enumerate(langs):
        with cols[i]:
            is_selected = st.session_state.language == code
            btn = st.button(name, use_container_width=True, type="primary" if is_selected else "secondary")
            if btn:
                st.session_state.language = code
                st.experimental_rerun()
    st.markdown(f"*Current Language: **{[k for k,v in LANGUAGES.items() if v==st.session_state.language][0]}*")

# 省略完整UI元素函數同前面的定義: create_hero_section, create_feature_card, etc.

# ------------------------
# 主程式
# ------------------------
def main():
    load_style()
    lang = st.session_state.language
    t = TEXTS[lang]

    create_navbar(t)
    language_selector()
    st.markdown("---")
    # 其他內容根據需求自行貼

    market_data = get_market_data()
    # 顯示指數、股票列表、交易圖表、AI洞察等，使用之前提供各個函數

if __name__ == "__main__":
    main()
