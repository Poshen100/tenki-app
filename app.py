import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# ====== 頁面配置 ======
st.set_page_config(
    page_title="TENKI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====== 初始化 ======
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'

# ====== 獲取股票數據 ======
@st.cache_data(ttl=300, show_spinner=False)
def get_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1d", interval="5m")
        if not history.empty:
            current_price = history['Close'].iloc[-1]
            previous_close = ticker.info.get('previousClose', current_price)
            change = current_price - previous_close
            change_pct = (change / previous_close) if previous_close != 0 else 0
            return {
                'symbol': symbol,
                'price': float(current_price),
                'change_pct': float(change_pct)
            }
    except:
        pass
    return {'symbol': symbol, 'price': 100.0, 'change_pct': 0.01}

# ====== iPhone風格CSS ======
def load_iphone_style():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700;800;900&display=swap');
        
        /* 隱藏Streamlit元素 */
        #MainMenu, footer, header, .stDeployButton {visibility: hidden !important;}
        .main > div {padding-top: 0rem;}
        
        /* iPhone容器 */
        .main .block-container {
            padding: 0;
            max-width: 100%;
            background: #f5f5f7;
        }
        
        .iphone-container {
            max-width: 390px;
            margin: 20px auto;
            background: white;
            border-radius: 40px;
            box-shadow: 0 0 60px rgba(0,0,0,0.3);
            overflow: hidden;
            position: relative;
            min-height: 844px;
        }
        
        /* 狀態欄 */
        .status-bar {
            height: 50px;
            background: white;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'SF Pro Display', sans-serif;
            font-size: 17px;
            font-weight: 600;
            color: #1d1d1f;
            border-bottom: 0.5px solid #e5e5e7;
        }
        
        /* 主內容區 */
        .main-content {
            padding: 20px;
            min-height: 650px;
            background: #f5f5f7;
        }
        
        /* Logo區域 */
        .logo-section {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px 0;
            background: white;
            border-radius: 20px;
        }
        
        .app-logo {
            width: 80px;
            height: 80px;
            border-radius: 18px;
            margin: 0 auto 16px;
            display: block;
            box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        }
        
        .app-title {
            font-family: 'SF Pro Display', sans-serif;
            font-size: 32px;
            font-weight: 800;
            color: #1d1d1f;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }
        
        .app-subtitle {
            font-family: 'SF Pro Display', sans-serif;
            font-size: 16px;
            color: #86868b;
            font-weight: 400;
        }
        
        /* 今日亮點卡片 */
        .highlight-card {
            background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
            border-radius: 20px;
            padding: 24px;
            color: white;
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
        }
        
        .highlight-card::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        }
        
        .highlight-title {
            font-family: 'SF Pro Display', sans-serif;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 6px;
            position: relative;
            z-index: 1;
        }
        
        .highlight-subtitle {
            font-size: 16px;
            opacity: 0.8;
            margin-bottom: 12px;
            position: relative;
            z-index: 1;
        }
        
        .highlight-description {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
            position: relative;
            z-index: 1;
        }
        
        .highlight-detail {
            font-size: 14px;
            opacity: 0.8;
            margin-bottom: 20px;
            position: relative;
            z-index: 1;
        }
        
        .highlight-button {
            background: rgba(255,255,255,0.2);
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            color: white;
            font-size: 16px;
            font-weight: 600;
            backdrop-filter: blur(10px);
            position: relative;
            z-index: 1;
        }
        
        /* 股票網格 */
        .section-title {
            font-family: 'SF Pro Display', sans-serif;
            font-size: 22px;
            font-weight: 700;
            color: #1d1d1f;
            margin-bottom: 16px;
            letter-spacing: -0.3px;
        }
        
        .stock-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 30px;
        }
        
        .stock-item {
            background: white;
            border-radius: 16px;
            padding: 16px;
            text-align: center;
            border: 0.5px solid #e5e5e7;
            position: relative;
        }
        
        .stock-item.positive::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: #30d158;
            border-radius: 2px 0 0 2px;
        }
        
        .stock-item.negative::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: #ff3b30;
            border-radius: 2px 0 0 2px;
        }
        
        .stock-symbol {
            font-family: 'SF Pro Display', sans-serif;
            font-size: 16px;
            font-weight: 700;
            color: #1d1d1f;
            margin-bottom: 4px;
        }
        
        .stock-change {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 2px;
        }
        
        .stock-change.positive {
            color: #30d158;
        }
        
        .stock-change.negative {
            color: #ff3b30;
        }
        
        .stock-price {
            font-size: 12px;
            color: #86868b;
        }
        
        /* 底部導航 */
        .bottom-nav {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 90px;
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(20px);
            border-top: 0.5px solid rgba(0,0,0,0.05);
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding-bottom: 20px;
        }
        
        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-family: 'SF Pro Display', sans-serif;
            cursor: pointer;
        }
        
        .nav-icon {
            font-size: 24px;
            margin-bottom: 4px;
        }
        
        .nav-label {
            font-size: 11px;
            font-weight: 500;
            color: #86868b;
        }
        
        .nav-item.active .nav-label {
            color: #007AFF;
        }
        
        .nav-item.active .nav-icon {
            color: #007AFF;
        }
        
        /* 響應式 */
        @media (max-width: 480px) {
            .iphone-container {
                margin: 0;
                border-radius: 0;
                max-width: 100%;
                box-shadow: none;
            }
        }
        
    </style>
    """, unsafe_allow_html=True)

# ====== UI組件 ======
def create_iphone_layout():
    st.markdown("""
    <div class="iphone-container">
        <div class="status-bar">TENKI</div>
        <div class="main-content">
    """, unsafe_allow_html=True)
    
    # Logo區域
    st.markdown("""
    <div class="logo-section">
        <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/IMG_0638.png" alt="TENKI Logo" class="app-logo">
        <h1 class="app-title">TENKI</h1>
        <p class="app-subtitle">Turning Insight into Opportunity</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 今日亮點
    st.markdown("""
    <div class="highlight-card">
        <h2 class="highlight-title">今日甜機</h2>
        <p class="highlight-subtitle">(Today's Sweet Spot)</p>
        <p class="highlight-description">美股區塊鏈概念股</p>
        <p class="highlight-detail">比特幣ETF熱錢前，預期Q4漲幅15-20%</p>
        <button class="highlight-button">查看高性價比方案</button>
    </div>
    """, unsafe_allow_html=True)
    
    # 股票追蹤
    st.markdown('<h3 class="section-title">我的追蹤</h3>', unsafe_allow_html=True)
    
    # 獲取股票數據
    stocks = ['NVDA', 'AMD', 'BTC-USD', 'GOOGL', 'TSLA', 'ETH-USD', 'BNB-USD', 'SOL-USD']
    stock_data = []
    
    for symbol in stocks[:9]:  # 限制9個
        data = get_stock_data(symbol)
        stock_data.append(data)
    
    # 顯示股票網格
    st.markdown('<div class="stock-grid">', unsafe_allow_html=True)
    
    for stock in stock_data:
        trend = 'positive' if stock['change_pct'] >= 0 else 'negative'
        change_sign = '+' if stock['change_pct'] >= 0 else ''
        
        # 簡化symbol顯示
        display_symbol = stock['symbol'].replace('-USD', '').replace('L', '')
        
        st.markdown(f"""
        <div class="stock-item {trend}">
            <div class="stock-symbol">{display_symbol}</div>
            <div class="stock-change {trend}">{change_sign}{stock['change_pct']:.1%}</div>
            <div class="stock-price">${stock['price']:.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 關閉主內容區
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 底部導航
    st.markdown("""
    <div class="bottom-nav">
        <div class="nav-item active">
            <div class="nav-icon">🔵</div>
            <div class="nav-label">Dashboard</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">▶</div>
            <div class="nav-label">Auto-Guide</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">📊</div>
            <div class="nav-label">Portfolio</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">⭕</div>
            <div class="nav-label">Subscription</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 關閉iPhone容器
    st.markdown('</div>', unsafe_allow_html=True)

# ====== 主程式 ======
def main():
    load_iphone_style()
    create_iphone_layout()

if __name__ == "__main__":
    main()
