import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import time
import requests

# ====== 頁面配置 ======
st.set_page_config(
    page_title="TENKI - Pivot Point Intelligence",
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
        "tagline": "Turning Insight into Opportunity",
        "today_sweet_spot": "今日甜機",
        "today_desc": "Today's Sweet Spot",
        "my_watchlist": "我的追蹤",
        "dashboard": "Dashboard",
        "auto_guide": "Auto-Guide",
        "portfolio": "Portfolio",
        "subscription": "Subscription",
        "market_analysis": "市場分析",
        "news_feed": "新聞動態",
        "technical_indicators": "技術指標",
        "pivot_analysis": "關鍵點分析",
        "ai_recommendations": "AI 投資建議",
        "risk_management": "風險管理",
        "performance_tracking": "績效追蹤"
    },
    "en": {
        "app_name": "TENKI",
        "tagline": "Turning Insight into Opportunity",
        "today_sweet_spot": "Today's Sweet Spot",
        "today_desc": "Market Opportunities",
        "my_watchlist": "My Watchlist",
        "dashboard": "Dashboard",
        "auto_guide": "Auto-Guide",
        "portfolio": "Portfolio", 
        "subscription": "Subscription",
        "market_analysis": "Market Analysis",
        "news_feed": "News Feed",
        "technical_indicators": "Technical Indicators",
        "pivot_analysis": "Pivot Analysis",
        "ai_recommendations": "AI Recommendations",
        "risk_management": "Risk Management",
        "performance_tracking": "Performance Tracking"
    },
    "jp": {
        "app_name": "TENKI",
        "tagline": "洞察を機会に変える",
        "today_sweet_spot": "今日のスイートスポット",
        "today_desc": "市場機会",
        "my_watchlist": "ウォッチリスト",
        "dashboard": "ダッシュボード",
        "auto_guide": "オートガイド",
        "portfolio": "ポートフォリオ",
        "subscription": "サブスクリプション",
        "market_analysis": "市場分析",
        "news_feed": "ニュースフィード",
        "technical_indicators": "テクニカル指標",
        "pivot_analysis": "ピボット分析",
        "ai_recommendations": "AI推奨",
        "risk_management": "リスク管理",
        "performance_tracking": "パフォーマンス追跡"
    }
}

# ====== Session State 初始化 ======
if 'language' not in st.session_state:
    st.session_state.language = 'zh'
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ['NVDA', 'AMD', 'BTC', 'GOOG', 'TSLA', 'ETH', 'BNB', 'SOL']
if 'user_subscribed' not in st.session_state:
    st.session_state.user_subscribed = False

# ====== 進階數據獲取系統 ======
@st.cache_data(ttl=300, show_spinner=False)
def get_comprehensive_stock_data(symbol):
    """獲取綜合股票數據"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        history = ticker.history(period="1d", interval="5m")
        
        if not history.empty:
            current_price = history['Close'].iloc[-1]
            previous_close = info.get('previousClose', current_price)
            change = current_price - previous_close
            change_pct = (change / previous_close) if previous_close != 0 else 0
            volume = history['Volume'].iloc[-1] if 'Volume' in history.columns else 0
            
            # 技術指標計算
            pivot_score = calculate_pivot_score(history)
            rsi = calculate_rsi(history['Close'])
            
            return {
                'symbol': symbol,
                'price': float(current_price),
                'change': float(change),
                'change_pct': float(change_pct),
                'volume': format_volume(volume),
                'pivot_score': pivot_score,
                'rsi': rsi,
                'trend': 'up' if change > 0 else 'down'
            }
    except Exception as e:
        return None

def calculate_pivot_score(history):
    """計算關鍵點評分"""
    if len(history) < 20:
        return 50
    
    # 簡化的關鍵點算法
    recent_high = history['High'].tail(20).max()
    recent_low = history['Low'].tail(20).min()
    current_price = history['Close'].iloc[-1]
    
    position = (current_price - recent_low) / (recent_high - recent_low)
    return min(100, max(0, int(position * 100)))

def calculate_rsi(prices, period=14):
    """計算相對強弱指數"""
    if len(prices) < period:
        return 50
    
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1]) if not rsi.empty else 50

def format_volume(volume):
    """格式化成交量"""
    if volume >= 1e9:
        return f"{volume/1e9:.1f}B"
    elif volume >= 1e6:
        return f"{volume/1e6:.1f}M"
    elif volume >= 1e3:
        return f"{volume/1e3:.1f}K"
    else:
        return str(int(volume))

@st.cache_data(ttl=600, show_spinner=False)
def get_market_news():
    """獲取市場新聞"""
    return [
        {
            'title': '比特幣ETF持續淨流入創新高',
            'summary': 'Q4預期15-20%漲幅，技術面突破關鍵阻力位',
            'time': '2小時前',
            'impact': 'positive'
        },
        {
            'title': 'NVIDIA財報超預期',
            'summary': 'AI晶片需求強勁，上調Q4指引',
            'time': '4小時前',
            'impact': 'positive'
        },
        {
            'title': '聯準會暗示降息放緩',
            'summary': '通膨數據仍有壓力，科技股承壓',
            'time': '6小時前',
            'impact': 'negative'
        }
    ]

# ====== 頂級移動端UI設計系統 ======
def load_mobile_premium_design():
    """載入移動端頂級設計系統"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700;800;900&display=swap');
        
        /* === 全域移動端優化 === */
        * {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            box-sizing: border-box;
        }
        
        html, body {
            margin: 0;
            padding: 0;
            background: #f5f5f7;
        }
        
        /* 隱藏Streamlit元素 */
        #MainMenu, footer, header, .stDeployButton {visibility: hidden !important;}
        .main > div {padding-top: 0rem;}
        
        /* === 移動端容器 === */
        .main .block-container {
            padding: 0rem;
            max-width: 100%;
            background: #f5f5f7;
        }
        
        /* === App容器 === */
        .app-container {
            max-width: 420px;
            margin: 0 auto;
            background: white;
            min-height: 100vh;
            box-shadow: 0 0 50px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }
        
        /* === 狀態欄 === */
        .status-bar {
            height: 44px;
            background: white;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 17px;
            font-weight: 600;
            color: #1d1d1f;
            border-bottom: 1px solid #f2f2f7;
        }
        
        /* === Hero區域 === */
        .hero-section {
            text-align: center;
            padding: 30px 20px 40px 20px;
            background: linear-gradient(135deg, #f5f5f7 0%, #ffffff 100%);
        }
        
        .app-logo {
            width: 80px;
            height: 80px;
            border-radius: 18px;
            margin: 0 auto 16px auto;
            display: block;
            box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        }
        
        .app-title {
            font-size: 32px;
            font-weight: 800;
            color: #1d1d1f;
            margin-bottom: 4px;
            letter-spacing: -0.5px;
        }
        
        .app-subtitle {
            font-size: 16px;
            color: #86868b;
            font-weight: 400;
            margin-bottom: 0;
        }
        
        /* === 今日亮點卡片 === */
        .highlight-card {
            margin: 20px;
            background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
            border-radius: 20px;
            padding: 24px;
            color: white;
            position: relative;
            overflow: hidden;
        }
        
        .highlight-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 80% 20%, rgba(255,255,255,0.1) 0%, transparent 50%);
        }
        
        .highlight-content {
            position: relative;
            z-index: 1;
        }
        
        .highlight-title {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 4px;
            letter-spacing: -0.3px;
        }
        
        .highlight-subtitle {
            font-size: 16px;
            opacity: 0.8;
            margin-bottom: 12px;
        }
        
        .highlight-description {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .highlight-detail {
            font-size: 14px;
            opacity: 0.8;
            margin-bottom: 20px;
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
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .highlight-button:hover {
            background: rgba(255,255,255,0.3);
            transform: scale(1.02);
        }
        
        /* === 追蹤列表 === */
        .watchlist-section {
            padding: 0 20px 100px 20px;
        }
        
        .section-title {
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
            margin-bottom: 24px;
        }
        
        .stock-item {
            background: white;
            border-radius: 16px;
            padding: 16px 12px;
            text-align: center;
            border: 1px solid #f2f2f7;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .stock-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        }
        
        .stock-item.positive {
            border-left: 4px solid #30d158;
        }
        
        .stock-item.negative {
            border-left: 4px solid #ff3b30;
        }
        
        .stock-symbol {
            font-size: 16px;
            font-weight: 700;
            color: #1d1d1f;
            margin-bottom: 4px;
        }
        
        .stock-change {
            font-size: 14px;
            font-weight: 600;
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
            margin-top: 2px;
        }
        
        /* === 新聞卡片 === */
        .news-section {
            margin-top: 32px;
        }
        
        .news-item {
            background: white;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 12px;
            border: 1px solid #f2f2f7;
            transition: all 0.2s ease;
        }
        
        .news-item:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        }
        
        .news-title {
            font-size: 16px;
            font-weight: 600;
            color: #1d1d1f;
            margin-bottom: 6px;
            line-height: 1.4;
        }
        
        .news-summary {
            font-size: 14px;
            color: #86868b;
            line-height: 1.4;
            margin-bottom: 8px;
        }
        
        .news-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .news-time {
            font-size: 12px;
            color: #86868b;
        }
        
        .news-impact {
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .news-impact.positive {
            background: #e8f5e8;
            color: #30d158;
        }
        
        .news-impact.negative {
            background: #ffeaea;
            color: #ff3b30;
        }
        
        /* === 底部導航 === */
        .bottom-navigation {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 420px;
            height: 83px;
            background: rgba(255,255,255,0.95);
            backdrop-filter: saturate(180%) blur(20px);
            border-top: 1px solid rgba(0,0,0,0.05);
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding-top: 8px;
            padding-bottom: env(safe-area-inset-bottom, 0px);
        }
        
        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            cursor: pointer;
            transition: all 0.2s ease;
            padding: 8px 12px;
            border-radius: 12px;
        }
        
        .nav-item:hover {
            background: rgba(0,122,255,0.1);
        }
        
        .nav-item.active {
            color: #007AFF;
        }
        
        .nav-icon {
            font-size: 24px;
            margin-bottom: 2px;
        }
        
        .nav-label {
            font-size: 11px;
            font-weight: 500;
            color: #86868b;
        }
        
        .nav-item.active .nav-label {
            color: #007AFF;
        }
        
        /* === 技術指標卡片 === */
        .indicator-card {
            background: white;
            border-radius: 16px;
            padding: 20px;
            margin: 12px 0;
            border: 1px solid #f2f2f7;
        }
        
        .indicator-title {
            font-size: 18px;
            font-weight: 600;
            color: #1d1d1f;
            margin-bottom: 12px;
        }
        
        .indicator-value {
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 8px;
        }
        
        .indicator-description {
            font-size: 14px;
            color: #86868b;
        }
        
        /* === 語言選擇器 === */
        .language-selector {
            position: fixed;
            top: 60px;
            right: 20px;
            z-index: 1000;
        }
        
        .lang-button {
            background: rgba(255,255,255,0.9);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0,0,0,0.1);
            border-radius: 20px;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: 500;
            color: #1d1d1f;
            cursor: pointer;
            margin-left: 8px;
            transition: all 0.2s ease;
        }
        
        .lang-button:hover, .lang-button.active {
            background: #007AFF;
            color: white;
            border-color: #007AFF;
        }
        
        /* === 響應式優化 === */
        @media (max-width: 480px) {
            .app-container {
                max-width: 100%;
                box-shadow: none;
            }
            
            .stock-grid {
                grid-template-columns: repeat(3, 1fr);
                gap: 8px;
            }
            
            .highlight-card {
                margin: 16px;
            }
            
            .watchlist-section {
                padding: 0 16px 100px 16px;
            }
        }
        
        /* === 動畫效果 === */
        .fade-in {
            animation: fadeIn 0.6s ease-out;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .slide-up {
            animation: slideUp 0.4s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
    </style>
    """, unsafe_allow_html=True)

# ====== UI組件函數 ======
def create_app_header(t):
    """創建App頂部"""
    st.markdown(f"""
    <div class="app-container">
        <div class="status-bar">
            {t['app_name']}
        </div>
        
        <div class="hero-section">
            <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/IMG_0638.png" alt="TENKI Logo" class="app-logo">
            <h1 class="app-title">{t['app_name']}</h1>
            <p class="app-subtitle">{t['tagline']}</p>
        </div>
    """, unsafe_allow_html=True)

def create_language_selector():
    """創建語言選擇器"""
    st.markdown('<div class="language-selector">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🇹🇼", key="zh", help="繁體中文"):
            st.session_state.language = 'zh'
            st.rerun()
    
    with col2:
        if st.button("🇺🇸", key="en", help="English"):
            st.session_state.language = 'en'
            st.rerun()
    
    with col3:
        if st.button("🇯🇵", key="jp", help="日本語"):
            st.session_state.language = 'jp'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_today_highlight(t):
    """創建今日亮點卡片"""
    st.markdown(f"""
    <div class="highlight-card fade-in">
        <div class="highlight-content">
            <h2 class="highlight-title">{t['today_sweet_spot']}</h2>
            <p class="highlight-subtitle">({t['today_desc']})</p>
            <p class="highlight-description">美股區塊鏈概念股</p>
            <p class="highlight-detail">比特幣ETF熱錢前，預期Q4漲幅15-20%</p>
            <button class="highlight-button">查看高性價比方案</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_watchlist_section(t):
    """創建追蹤列表"""
    st.markdown(f"""
    <div class="watchlist-section">
        <h3 class="section-title">{t['my_watchlist']}</h3>
        <div class="stock-grid">
    """, unsafe_allow_html=True)
    
    # 獲取追蹤股票數據
    watchlist_data = []
    for symbol in st.session_state.watchlist:
        data = get_comprehensive_stock_data(symbol)
        if data:
            watchlist_data.append(data)
    
    # 顯示股票網格
    for i, stock in enumerate(watchlist_data[:9]):  # 限制9個
        trend_class = 'positive' if stock['change'] >= 0 else 'negative'
        change_sign = '+' if stock['change'] >= 0 else ''
        
        st.markdown(f"""
        <div class="stock-item {trend_class}">
            <div class="stock-symbol">{stock['symbol']}</div>
            <div class="stock-change {trend_class}">{change_sign}{stock['change_pct']:.1%}</div>
            <div class="stock-price">${stock['price']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def create_news_section(t):
    """創建新聞區域"""
    news_items = get_market_news()
    
    st.markdown(f"""
    <div class="news-section">
        <h3 class="section-title">{t.get('news_feed', '市場動態')}</h3>
    """, unsafe_allow_html=True)
    
    for news in news_items:
        impact_class = news['impact']
        impact_text = '利好' if impact_class == 'positive' else '利空'
        
        st.markdown(f"""
        <div class="news-item slide-up">
            <h4 class="news-title">{news['title']}</h4>
            <p class="news-summary">{news['summary']}</p>
            <div class="news-meta">
                <span class="news-time">{news['time']}</span>
                <span class="news-impact {impact_class}">{impact_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_technical_indicators(t):
    """創建技術指標頁面"""
    st.markdown(f"""
    <div class="watchlist-section">
        <h3 class="section-title">{t.get('technical_indicators', '技術指標')}</h3>
    """, unsafe_allow_html=True)
    
    # 市場恐慌指數
    st.markdown(f"""
    <div class="indicator-card fade-in">
        <h4 class="indicator-title">恐慌貪婪指數</h4>
        <div class="indicator-value" style="color: #ff9500;">73</div>
        <p class="indicator-description">當前市場情緒偏向貪婪，建議謹慎操作</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bitcoin dominance
    st.markdown(f"""
    <div class="indicator-card fade-in">
        <h4 class="indicator-title">比特幣市場占比</h4>
        <div class="indicator-value" style="color: #007AFF;">54.2%</div>
        <p class="indicator-description">BTC主導地位穩固，山寨幣輪動機會增加</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_portfolio_page(t):
    """創建投資組合頁面"""
    st.markdown(f"""
    <div class="watchlist-section">
        <h3 class="section-title">{t.get('portfolio', 'Portfolio')}</h3>
        
        <div class="indicator-card fade-in">
            <h4 class="indicator-title">總資產價值</h4>
            <div class="indicator-value" style="color: #30d158;">$25,847.92</div>
            <p class="indicator-description">今日收益 +$1,247.83 (+5.08%)</p>
        </div>
        
        <div class="indicator-card fade-in">
            <h4 class="indicator-title">持股分布</h4>
            <div style="margin: 16px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>科技股</span>
                    <span style="color: #30d158;">45%</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>加密貨幣</span>
                    <span style="color: #ff9500;">30%</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>ETF</span>
                    <span style="color: #007AFF;">25%</span>
                </div>
            </div>
        </div>
        
        <div class="indicator-card fade-in">
            <h4 class="indicator-title">風險評估</h4>
            <div class="indicator-value" style="color: #ff9500;">中等風險</div>
            <p class="indicator-description">建議適度分散投資，關注市場波動</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_subscription_page(t):
    """創建訂閱頁面"""
    st.markdown(f"""
    <div class="watchlist-section">
        <h3 class="section-title">{t.get('subscription', 'Subscription')}</h3>
        
        <div class="indicator-card fade-in">
            <h4 class="indicator-title">當前方案</h4>
            <div class="indicator-value" style="color: #007AFF;">基礎版</div>
            <p class="indicator-description">享受基礎功能，升級解鎖更多特色</p>
        </div>
        
        <div class="highlight-card" style="margin: 20px 0;">
            <div class="highlight-content">
                <h2 class="highlight-title">升級至專業版</h2>
                <p class="highlight-subtitle">解鎖全部高級功能</p>
                <p class="highlight-detail">• AI智能投資建議<br>• 實時關鍵點提醒<br>• 專業技術分析<br>• 優先客服支持</p>
                <button class="highlight-button">立即升級 - $29.99/月</button>
            </div>
        </div>
        
        <div class="indicator-card fade-in">
            <h4 class="indicator-title">功能對比</h4>
            <div style="margin: 16px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #f2f2f7;">
                    <span>基礎市場數據</span>
                    <span style="color: #30d158;">✓</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #f2f2f7;">
                    <span>AI投資建議</span>
                    <span style="color: #ff3b30;">僅限3次/日</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #f2f2f7;">
                    <span>關鍵點提醒</span>
                    <span style="color: #ff3b30;">✗</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <span>專業技術指標</span>
                    <span style="color: #ff3b30;">✗</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_bottom_navigation(t):
    """創建底部導航"""
    pages = {
        'dashboard': {'icon': '🏠', 'label': t.get('dashboard', 'Dashboard')},
        'auto_guide': {'icon': '🤖', 'label': t.get('auto_guide', 'Auto-Guide')},
        'portfolio': {'icon': '📊', 'label': t.get('portfolio', 'Portfolio')},
        'subscription': {'icon': '⭐', 'label': t.get('subscription', 'Subscription')}
    }
    
    st.markdown('<div class="bottom-navigation">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(f"{pages['dashboard']['icon']}\n{pages['dashboard']['label']}", key="nav_dashboard", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    with col2:
        if st.button(f"{pages['auto_guide']['icon']}\n{pages['auto_guide']['label']}", key="nav_auto_guide", use_container_width=True):
            st.session_state.current_page = 'auto_guide'
            st.rerun()
    
    with col3:
        if st.button(f"{pages['portfolio']['icon']}\n{pages['portfolio']['label']}", key="nav_portfolio", use_container_width=True):
            st.session_state.current_page = 'portfolio'
            st.rerun()
    
    with col4:
        if st.button(f"{pages['subscription']['icon']}\n{pages['subscription']['label']}", key="nav_subscription", use_container_width=True):
            st.session_state.current_page = 'subscription'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ====== 主應用程式 ======
def main():
    load_mobile_premium_design()
    
    lang = st.session_state.language
    t = TEXTS[lang]
    
    # App頂部
    create_app_header(t)
    
    # 語言選擇器
    create_language_selector()
    
    # 根據當前頁面顯示內容
    if st.session_state.current_page == 'dashboard':
        create_today_highlight(t)
        create_watchlist_section(t)
        create_news_section(t)
    
    elif st.session_state.current_page == 'auto_guide':
        create_technical_indicators(t)
    
    elif st.session_state.current_page == 'portfolio':
        create_portfolio_page(t)
    
    elif st.session_state.current_page == 'subscription':
        create_subscription_page(t)
    
    # 關閉App容器
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 底部導航
    create_bottom_navigation(t)

# ====== 執行主程式 ======
if __name__ == "__main__":
    main()
