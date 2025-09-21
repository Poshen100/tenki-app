import streamlit as st
import yfinance as yf
import requests
import pandas as pd
from datetime import datetime

# ====== 頁面配置 ======
st.set_page_config(
    page_title="TENKI",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ====== 獲取Yahoo財經數據 ======
@st.cache_data(ttl=300, show_spinner=False)
def get_yahoo_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1m")
        if not data.empty:
            current = data['Close'].iloc[-1]
            previous = ticker.info.get('previousClose', current)
            change = current - previous
            change_pct = (change / previous) * 100 if previous != 0 else 0
            return {
                'symbol': symbol,
                'price': float(current),
                'change_pct': float(change_pct)
            }
    except:
        pass
    return {'symbol': symbol, 'price': 150.0, 'change_pct': 1.5}

# ====== 極簡iPhone風格CSS ======
def load_clean_style():
    st.markdown("""
    <style>
        /* 隱藏Streamlit元素 */
        #MainMenu, footer, header, .stDeployButton, .stDecoration {display: none !important;}
        .main > div {padding-top: 0rem !important;}
        
        /* 基礎設定 */
        * {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
            -webkit-font-smoothing: antialiased;
        }
        
        .main .block-container {
            padding: 0rem;
            max-width: 100% !important;
            background: #000000;
        }
        
        /* iPhone容器 */
        .iphone-frame {
            max-width: 375px;
            margin: 20px auto;
            background: white;
            border-radius: 30px;
            overflow: hidden;
            box-shadow: 0 0 40px rgba(0,0,0,0.8);
            position: relative;
            min-height: 812px;
        }
        
        /* 狀態欄 */
        .status-bar {
            height: 44px;
            background: white;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 17px;
            font-weight: 600;
            color: #000;
        }
        
        /* 主內容 */
        .content {
            background: #000000;
            min-height: 720px;
            padding: 0;
        }
        
        /* Logo卡片 */
        .logo-card {
            background: white;
            margin: 20px;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
        }
        
        .logo {
            width: 80px;
            height: 80px;
            margin: 0 auto 16px;
            display: block;
            border-radius: 16px;
        }
        
        .logo-title {
            font-size: 28px;
            font-weight: 800;
            color: #007AFF;
            margin-bottom: 8px;
        }
        
        .logo-subtitle {
            font-size: 14px;
            color: #8E8E93;
            margin: 0;
        }
        
        /* 今日甜機卡片 */
        .sweet-spot-card {
            background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
            margin: 20px;
            border-radius: 20px;
            padding: 24px;
            color: white;
            position: relative;
            overflow: hidden;
        }
        
        .sweet-spot-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        }
        
        .sweet-title {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 6px;
            position: relative;
            z-index: 1;
        }
        
        .sweet-subtitle {
            font-size: 16px;
            opacity: 0.9;
            margin-bottom: 12px;
            position: relative;
            z-index: 1;
        }
        
        .sweet-desc {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
            position: relative;
            z-index: 1;
        }
        
        .sweet-detail {
            font-size: 14px;
            opacity: 0.8;
            margin-bottom: 20px;
            position: relative;
            z-index: 1;
        }
        
        .sweet-btn {
            background: rgba(255,255,255,0.2);
            border: none;
            border-radius: 12px;
            padding: 12px 20px;
            color: white;
            font-size: 14px;
            font-weight: 600;
            position: relative;
            z-index: 1;
            backdrop-filter: blur(10px);
            width: 100%;
        }
        
        /* 追蹤標題 */
        .watchlist-title {
            color: white;
            font-size: 22px;
            font-weight: 700;
            margin: 30px 20px 20px 20px;
        }
        
        /* 股票列表 */
        .stock-list {
            padding: 0 20px 100px 20px;
        }
        
        .stock-item {
            background: white;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
        }
        
        .stock-left {
            display: flex;
            align-items: center;
        }
        
        .stock-indicator {
            width: 4px;
            height: 40px;
            border-radius: 2px;
            margin-right: 16px;
        }
        
        .stock-indicator.green {
            background: #34C759;
        }
        
        .stock-indicator.red {
            background: #FF3B30;
        }
        
        .stock-info h3 {
            font-size: 18px;
            font-weight: 700;
            color: #000;
            margin: 0 0 4px 0;
        }
        
        .stock-price {
            font-size: 14px;
            color: #8E8E93;
            margin: 0;
        }
        
        .stock-change {
            font-size: 16px;
            font-weight: 600;
            text-align: right;
        }
        
        .stock-change.green {
            color: #34C759;
        }
        
        .stock-change.red {
            color: #FF3B30;
        }
        
        /* 底部導航 */
        .bottom-nav {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 80px;
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(20px);
            border-top: 0.5px solid rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding-bottom: 20px;
        }
        
        .nav-btn {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-decoration: none;
            color: #8E8E93;
            font-size: 10px;
        }
        
        .nav-btn.active {
            color: #007AFF;
        }
        
        .nav-icon {
            font-size: 24px;
            margin-bottom: 2px;
        }
        
        /* 響應式 */
        @media (max-width: 400px) {
            .iphone-frame {
                margin: 0;
                border-radius: 0;
                max-width: 100%;
            }
        }
        
    </style>
    """, unsafe_allow_html=True)

# ====== UI組件 ======
def create_logo_section():
    st.markdown("""
    <div class="logo-card">
        <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/IMG_0638.png" alt="TENKI" class="logo">
        <h1 class="logo-title">TENKI</h1>
        <p class="logo-subtitle">Turning Insight into Opportunity</p>
    </div>
    """, unsafe_allow_html=True)

def create_sweet_spot_card():
    st.markdown("""
    <div class="sweet-spot-card">
        <h2 class="sweet-title">今日甜機</h2>
        <p class="sweet-subtitle">(Today's Sweet Spot)</p>
        <p class="sweet-desc">美股區塊鏈概念股</p>
        <p class="sweet-detail">比特幣ETF熱錢前，預期Q4漲幅15-20%</p>
        <button class="sweet-btn">查看高性價比方案</button>
    </div>
    """, unsafe_allow_html=True)

def create_stock_list():
    st.markdown('<div class="watchlist-title">我的追蹤</div>', unsafe_allow_html=True)
    st.markdown('<div class="stock-list">', unsafe_allow_html=True)
    
    # 股票清單
    stocks = [
        'NVDA', 'AMD', 'BTC-USD', 'GOOGL', 'TSLA', 
        'ETH-USD', 'BNB-USD', 'SOL-USD', 'AAPL'
    ]
    
    for symbol in stocks:
        data = get_yahoo_price(symbol)
        
        # 判斷漲跌
        is_positive = data['change_pct'] >= 0
        indicator_class = 'green' if is_positive else 'red'
        change_class = 'green' if is_positive else 'red'
        change_sign = '+' if is_positive else ''
        
        # 簡化symbol顯示
        display_symbol = symbol.replace('-USD', '').replace('L', '')
        
        st.markdown(f"""
        <div class="stock-item">
            <div class="stock-left">
                <div class="stock-indicator {indicator_class}"></div>
                <div class="stock-info">
                    <h3>{display_symbol}</h3>
                    <p class="stock-price">${data['price']:.0f}</p>
                </div>
            </div>
            <div class="stock-change {change_class}">
                {change_sign}{data['change_pct']:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_bottom_nav():
    st.markdown("""
    <div class="bottom-nav">
        <div class="nav-btn active">
            <div class="nav-icon">🔵</div>
            Dashboard
        </div>
        <div class="nav-btn">
            <div class="nav-icon">▶️</div>
            Auto-Guide
        </div>
        <div class="nav-btn">
            <div class="nav-icon">📊</div>
            Portfolio
        </div>
        <div class="nav-btn">
            <div class="nav-icon">⭕</div>
            Subscription
        </div>
    </div>
    """, unsafe_allow_html=True)

# ====== 主程式 ======
def main():
    load_clean_style()
    
    # iPhone框架開始
    st.markdown('<div class="iphone-frame">', unsafe_allow_html=True)
    st.markdown('<div class="status-bar">TENKI</div>', unsafe_allow_html=True)
    st.markdown('<div class="content">', unsafe_allow_html=True)
    
    # 主要內容
    create_logo_section()
    create_sweet_spot_card()
    create_stock_list()
    
    # 關閉內容區
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 底部導航
    create_bottom_nav()
    
    # 關閉iPhone框架
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
