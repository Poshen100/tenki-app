import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import time

# ====== 頁面配置 ======
def create_top_navigation(t):
    st.markdown(f"""
    <div class="top-navigation">
        <div class="nav-logo">
            <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/IMG_0638.png" alt="TENKI Logo" class="nav-logo-img">
            <div class="nav-brand">{t['app_name']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
        "tagline": "讓每個投資決定都踩中關鍵點",
        "pivot_point_analytics": "關鍵點分析",
        "smart_portfolio": "智能組合建構",
        "market_pulse": "市場脈動",
        "investment_academy": "投資學院",
        "real_time_market": "即時市場數據",
        "expert_insight": "專家洞察",
        "pricing_plans": "方案選擇",
        "basic_plan": "基礎版",
        "advanced_plan": "進階版", 
        "enterprise_plan": "企業版",
        "subscribe": "立即訂閱",
        "market_overview": "市場概況",
        "ai_recommendations": "AI 投資建議",
        "core_features": "核心功能",
        "language": "語言"
    },
    "en": {
        "app_name": "TENKI",
        "tagline": "Turning Insight into Opportunity",
        "pivot_point_analytics": "Pivot Point Analytics",
        "smart_portfolio": "Smart Portfolio Builder",
        "market_pulse": "Market Pulse",
        "investment_academy": "Investment Academy",
        "real_time_market": "Real-time Market Data",
        "expert_insight": "Expert Insights",
        "pricing_plans": "Pricing Plans",
        "basic_plan": "Basic",
        "advanced_plan": "Advanced",
        "enterprise_plan": "Enterprise",
        "subscribe": "Subscribe Now",
        "market_overview": "Market Overview",
        "ai_recommendations": "AI Recommendations",
        "core_features": "Core Features",
        "language": "Language"
    },
    "jp": {
        "app_name": "TENKI",
        "tagline": "洞察を機会に変える",
        "pivot_point_analytics": "ピボットポイント分析",
        "smart_portfolio": "スマートポートフォリオ",
        "market_pulse": "マーケットパルス",
        "investment_academy": "投資アカデミー",
        "real_time_market": "リアルタイム市場データ",
        "expert_insight": "専門家の洞察",
        "pricing_plans": "料金プラン",
        "basic_plan": "ベーシック",
        "advanced_plan": "アドバンス",
        "enterprise_plan": "エンタープライズ",
        "subscribe": "今すぐ購読",
        "market_overview": "市場概況",
        "ai_recommendations": "AI 投資提案",
        "core_features": "コア機能",
        "language": "言語"
    }
}

# ====== Session State 初始化 ======
if 'language' not in st.session_state:
    st.session_state.language = 'zh'

# ====== 更穩定的市場數據API ======
@st.cache_data(ttl=120, show_spinner=False)
def fetch_live_price_yfinance(symbol):
    """使用 yfinance 獲取即時股價數據"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        history = ticker.history(period="1d", interval="1m")
        
        if not history.empty:
            current_price = history['Close'].iloc[-1]
            previous_close = info.get('previousClose', current_price)
            change = current_price - previous_close
            change_pct = (change / previous_close) if previous_close != 0 else 0
            
            return float(current_price), float(change), float(change_pct)
    except Exception as e:
        st.error(f"無法獲取 {symbol} 的數據: {str(e)}")
    
    return None, None, None

@st.cache_data(ttl=120, show_spinner=False)
def get_market_data():
    """獲取完整市場數據"""
    
    # 定義股票代碼映射
    symbols = {
        'SP500': '^GSPC',
        'NASDAQ': '^IXIC', 
        'DJI': '^DJI',
        'BTC': 'BTC-USD'
    }
    
    indices = {}
    
    for name, symbol in symbols.items():
        price, change, change_pct = fetch_live_price_yfinance(symbol)
        indices[name] = {
            'value': price,
            'change': change, 
            'change_pct': change_pct
        }
    
    return {
        'indices': indices,
        'hot_stocks': [
            {'symbol': 'COIN', 'name': 'Coinbase', 'price': 156.42, 'change': 2.8, 'volume': '2.1M', 'rating': '強力買入', 'pivot_score': 85},
            {'symbol': 'MSTR', 'name': 'MicroStrategy', 'price': 1247.85, 'change': 5.2, 'volume': '145K', 'rating': '買入', 'pivot_score': 78},
            {'symbol': 'RIOT', 'name': 'Riot Blockchain', 'price': 8.94, 'change': 1.4, 'volume': '5.8M', 'rating': '買入', 'pivot_score': 72},
            {'symbol': 'NVDA', 'name': 'NVIDIA', 'price': 445.67, 'change': -1.2, 'volume': '32.5M', 'rating': '持有', 'pivot_score': 68},
            {'symbol': 'TSLA', 'name': 'Tesla', 'price': 234.56, 'change': 3.4, 'volume': '45.2M', 'rating': '強力買入', 'pivot_score': 82}
        ]
    }

def generate_pivot_insights():
    """生成關鍵點分析洞察"""
    return [
        {
            'title': '區塊鏈概念股關鍵突破點',
            'content': '比特幣ETF持續淨流入創新高，COIN突破關鍵阻力位$155，技術面顯示強勢上攻態勢，預期目標價$180-200區間。',
            'confidence': 87,
            'risk_level': '中等',
            'time_horizon': '2-4週',
            'pivot_score': 85
        },
        {
            'title': 'AI晶片供應鏈的關鍵轉折',
            'content': 'NVIDIA財報超預期後，整個AI生態鏈進入新一輪上升週期，關注TSM、AMD等在$150關鍵支撐位的表現。',
            'confidence': 82,
            'risk_level': '中高',
            'time_horizon': '4-8週',
            'pivot_score': 78
        }
    ]

# ====== UI設計系統 ======
def load_premium_design_system():
    """載入頂級設計系統"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
        }
        
        #MainMenu, footer, header, .stDeployButton {visibility: hidden !important;}
        
        .main .block-container {
            padding: 0rem 2rem 3rem 2rem;
            max-width: 1600px;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        }
        
        .top-navigation {
            position: sticky;
            top: 0;
            height: 75px;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: saturate(200%) blur(25px);
            border-bottom: 1px solid rgba(0, 0, 0, 0.06);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 3rem;
            margin-bottom: 2rem;
            border-radius: 0 0 24px 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        }
        
        .nav-logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .nav-logo-img {
            width: 45px;
            height: 45px;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
            object-fit: cover;
        }
        
        .nav-brand {
            font-size: 26px;
            font-weight: 800;
            background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .hero-section {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #334155 100%);
            padding: 5rem 3rem;
            border-radius: 32px;
            margin-bottom: 4rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 20px 64px rgba(0, 0, 0, 0.25);
        }
        
        .hero-content {
            text-align: center;
            position: relative;
            z-index: 1;
            max-width: 900px;
            margin: 0 auto;
        }
        
        .hero-logo {
            width: 120px;
            height: 120px;
            border-radius: 24px;
            filter: drop-shadow(0 12px 48px rgba(0, 0, 0, 0.4));
            object-fit: cover;
            margin-bottom: 2rem;
        }
        
        .hero-title {
            font-size: clamp(3.5rem, 9vw, 5.5rem);
            font-weight: 900;
            letter-spacing: -0.05em;
            background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1.5rem;
            line-height: 1;
        }
        
        .hero-subtitle {
            font-size: clamp(1.2rem, 3vw, 1.6rem);
            color: #cbd5e1;
            margin-bottom: 3rem;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            margin: 4rem 0;
        }
        
        .metric-card {
            background: white;
            border-radius: 20px;
            padding: 2.5rem;
            box-shadow: 0 6px 32px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        }
        
        .metric-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 16px 64px rgba(0, 0, 0, 0.15);
        }
        
        .metric-label {
            color: #64748b;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 1rem;
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 1rem;
            letter-spacing: -0.03em;
        }
        
        .metric-change {
            font-size: 1rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }
        
        .metric-change.positive { color: #059669; }
        .metric-change.negative { color: #dc2626; }
        .metric-change.loading { color: #6b7280; }
        
        .error-message {
            background: #fee2e2;
            border: 1px solid #fecaca;
            color: #dc2626;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            text-align: center;
        }
        
        @media (max-width: 768px) {
            .main .block-container {
                padding: 0rem 1rem 2rem 1rem;
            }
            .metrics-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def create_top_navigation(t):
    """創建頂部導航欄"""
    st.markdown(f"""
    <div class="top-navigation">
        <div class="nav-logo">
            <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/IMG_0640.jpeg" alt="TENKI Logo" class="nav-logo-img">
            <div class="nav-brand">{t['app_name']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_hero_section(t):
    """創建Hero區域"""
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-content">
            <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/IMG_0640.jpeg" alt="TENKI Logo" class="hero-logo">
            <h1 class="hero-title">{t['app_name']}</h1>
            <p class="hero-subtitle">{t['tagline']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(label, value, change, change_pct):
    """創建指標卡片"""
    if value is None or change is None or change_pct is None:
        return f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">數據載入中...</div>
            <div class="metric-change loading">⏳ 請稍候</div>
        </div>
        """
    
    change_class = "positive" if change >= 0 else "negative"
    change_symbol = "+" if change >= 0 else ""
    change_icon = "↗" if change >= 0 else "↘"
    
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value:,.2f}</div>
        <div class="metric-change {change_class}">
            <span>{change_icon}</span>
            {change_symbol}{change:.2f} ({change_symbol}{change_pct:.2%})
        </div>
    </div>
    """

def language_selector():
    """語言選擇器"""
    st.markdown("### 🌐 語言選擇")
    
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
    load_premium_design_system()
    
    lang = st.session_state.language
    t = TEXTS[lang]
    
    create_top_navigation(t)
    language_selector()
    st.markdown("---")
    create_hero_section(t)
    
    # 即時市場數據
    st.markdown(f"## 📊 {t['real_time_market']}")
    
    with st.spinner("載入即時市場數據..."):
        market_data = get_market_data()
    
    st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
    
    indices = market_data['indices']
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        sp_data = indices['SP500']
        st.markdown(create_metric_card("S&P 500", sp_data['value'], sp_data['change'], sp_data['change_pct']), unsafe_allow_html=True)
    
    with col2:
        nasdaq_data = indices['NASDAQ']
        st.markdown(create_metric_card("NASDAQ", nasdaq_data['value'], nasdaq_data['change'], nasdaq_data['change_pct']), unsafe_allow_html=True)
    
    with col3:
        dji_data = indices['DJI']
        st.markdown(create_metric_card("道瓊指數", dji_data['value'], dji_data['change'], dji_data['change_pct']), unsafe_allow_html=True)
    
    with col4:
        btc_data = indices['BTC']
        st.markdown(create_metric_card("Bitcoin", btc_data['value'], btc_data['change'], btc_data['change_pct']), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
