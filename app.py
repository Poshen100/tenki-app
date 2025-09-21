import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import time
import requests
from PIL import Image

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
        "language": "語言",
        "feature_expansion": "功能擴展",
        "data_enhancement": "數據豐富化",
        "business_preparation": "商業化準備",
        "add_more_stocks": "添加更多股票追蹤",
        "add_portfolio": "增加投資組合功能",
        "implement_login": "實現用戶登入系統",
        "integrate_more_apis": "整合更多金融API",
        "add_news_feeds": "添加新聞資訊",
        "add_technical_indicators": "增加技術指標",
        "add_subscription": "訂閱付費功能",
        "hot_stocks": "熱門股票",
        "pivot_score": "關鍵分數",
        "volume": "成交量",
        "rating": "評級",
        "roadmap": "發展路線圖"
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
        "language": "Language",
        "feature_expansion": "Feature Expansion",
        "data_enhancement": "Data Enhancement",
        "business_preparation": "Business Preparation",
        "add_more_stocks": "Add more stock tracking",
        "add_portfolio": "Add portfolio functionality",
        "implement_login": "Implement user login system",
        "integrate_more_apis": "Integrate more financial APIs",
        "add_news_feeds": "Add news feeds",
        "add_technical_indicators": "Add technical indicators",
        "add_subscription": "Add subscription features",
        "hot_stocks": "Hot Stocks",
        "pivot_score": "Pivot Score",
        "volume": "Volume",
        "rating": "Rating",
        "roadmap": "Development Roadmap"
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
        "language": "言語",
        "feature_expansion": "機能拡張",
        "data_enhancement": "データ充実化",
        "business_preparation": "ビジネス化準備",
        "add_more_stocks": "株式追跡機能の追加",
        "add_portfolio": "ポートフォリオ機能の追加",
        "implement_login": "ユーザーログインシステムの実装",
        "integrate_more_apis": "金融APIの統合拡張",
        "add_news_feeds": "ニュースフィードの追加",
        "add_technical_indicators": "テクニカル指標の追加",
        "add_subscription": "サブスクリプション機能の追加",
        "hot_stocks": "注目株",
        "pivot_score": "ピボットスコア",
        "volume": "出来高",
        "rating": "評価",
        "roadmap": "開発ロードマップ"
    }
}

# ====== Session State 初始化 ======
if 'language' not in st.session_state:
    st.session_state.language = 'zh'

# ====== 市場數據API ======
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

def generate_pivot_insights(t):
    """生成關鍵點分析洞察"""
    return [
        {
            'title': '區塊鏈概念股關鍵突破點' if t == TEXTS['zh'] else 'Blockchain Stock Breakthrough',
            'content': '比特幣ETF持續淨流入創新高，COIN突破關鍵阻力位$155，技術面顯示強勢上攻態勢，預期目標價$180-200區間。' if t == TEXTS['zh'] else 'Bitcoin ETF net inflows hit new highs, COIN breaks key resistance at $155, technical analysis shows strong bullish momentum, target price $180-200.',
            'confidence': 87,
            'risk_level': '中等' if t == TEXTS['zh'] else 'Medium',
            'time_horizon': '2-4週' if t == TEXTS['zh'] else '2-4 weeks',
            'pivot_score': 85
        },
        {
            'title': 'AI晶片供應鏈的關鍵轉折' if t == TEXTS['zh'] else 'AI Chip Supply Chain Pivot',
            'content': 'NVIDIA財報超預期後，整個AI生態鏈進入新一輪上升週期，關注TSM、AMD等在$150關鍵支撐位的表現。' if t == TEXTS['zh'] else 'After NVIDIA\'s earnings beat, AI ecosystem enters new growth cycle. Watch TSM, AMD performance at $150 key support level.',
            'confidence': 82,
            'risk_level': '中高' if t == TEXTS['zh'] else 'Medium-High',
            'time_horizon': '4-8週' if t == TEXTS['zh'] else '4-8 weeks',
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
        
        .top-banner {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 2rem 0;
            background: white;
            border-radius: 24px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .top-banner img {
            max-width: 100%;
            height: auto;
            border-radius: 16px;
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
        
        .section-header {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            padding: 2.5rem;
            border-radius: 20px;
            margin: 3rem 0 2rem 0;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
        }
        
        .section-header h2 {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
        }
        
        .section-header p {
            font-size: 1.2rem;
            opacity: 0.8;
            margin: 0;
        }
        
        .stock-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
            border-left: 4px solid #3b82f6;
        }
        
        .stock-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        }
        
        .stock-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .stock-symbol {
            font-size: 1.4rem;
            font-weight: 700;
            color: #1e293b;
        }
        
        .stock-name {
            color: #64748b;
            font-size: 0.9rem;
            margin-top: 0.2rem;
        }
        
        .stock-price {
            font-size: 1.8rem;
            font-weight: 800;
            color: #0f172a;
        }
        
        .stock-metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1rem;
            margin-top: 1.5rem;
        }
        
        .stock-metric {
            text-align: center;
            padding: 1rem;
            background: #f8fafc;
            border-radius: 12px;
        }
        
        .stock-metric-label {
            font-size: 0.8rem;
            color: #64748b;
            font-weight: 600;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
        }
        
        .stock-metric-value {
            font-size: 1.1rem;
            font-weight: 700;
            color: #1e293b;
        }
        
        .insight-card {
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            border: 1px solid #bae6fd;
            border-radius: 16px;
            padding: 2rem;
            margin: 1rem 0;
            position: relative;
            overflow: hidden;
        }
        
        .insight-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        }
        
        .insight-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #0c4a6e;
            margin-bottom: 1rem;
        }
        
        .insight-content {
            color: #164e63;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }
        
        .insight-metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .insight-metric {
            text-align: center;
            padding: 0.8rem;
            background: rgba(255, 255, 255, 0.7);
            border-radius: 8px;
        }
        
        .roadmap-container {
            background: white;
            border-radius: 20px;
            padding: 3rem;
            margin: 2rem 0;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        }
        
        .roadmap-phase {
            margin-bottom: 3rem;
            position: relative;
            padding-left: 2rem;
        }
        
        .roadmap-phase::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0.5rem;
            width: 1rem;
            height: 1rem;
            background: #3b82f6;
            border-radius: 50%;
        }
        
        .roadmap-phase h3 {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 1rem;
        }
        
        .roadmap-item {
            display: flex;
            align-items: center;
            padding: 0.8rem;
            margin: 0.5rem 0;
            background: #f8fafc;
            border-radius: 12px;
            transition: all 0.2s ease;
        }
        
        .roadmap-item:hover {
            background: #e2e8f0;
            transform: translateX(8px);
        }
        
        .roadmap-item::before {
            content: '●';
            color: #64748b;
            margin-right: 1rem;
            font-size: 0.8rem;
        }
        
        .language-selector {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin: 2rem 0;
            padding: 1.5rem;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }
        
        .lang-button {
            padding: 0.8rem 1.5rem;
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            background: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
        }
        
        .lang-button:hover {
            border-color: #3b82f6;
            background: #f0f9ff;
        }
        
        .lang-button.active {
            border-color: #3b82f6;
            background: #3b82f6;
            color: white;
        }
        
        @media (max-width: 768px) {
            .main .block-container {
                padding: 0rem 1rem 2rem 1rem;
            }
            .metrics-grid {
                grid-template-columns: 1fr;
            }
            .stock-metrics {
                grid-template-columns: repeat(2, 1fr);
            }
            .insight-metrics {
                grid-template-columns: repeat(2, 1fr);
            }
            .language-selector {
                flex-direction: column;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def create_top_banner():
    """創建頂部橫幅 - 使用IMG_0638.png"""
    try:
        # 嘗試載入本地圖片
        st.markdown('<div class="top-banner">', unsafe_allow_html=True)
        
        # 方法1: 如果圖片在本地目錄
        try:
            st.image("IMG_0638.png", use_column_width=True)
        except:
            # 方法2: 如果是附件中的image.jpeg
            try:
                st.image("image.jpeg", use_column_width=True)
            except:
                # 方法3: 使用GitHub URL (需要先上傳)
                st.markdown("""
                <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/IMG_0638.png" 
                     alt="TENKI Banner" style="width: 100%; max-width: 800px; height: auto; border-radius: 16px;">
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"無法載入橫幅圖片: {str(e)}")

def create_hero_section(t):
    """創建Hero區域"""
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-content">
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

def language_selector(t):
    """語言選擇器"""
    st.markdown(f"""
    <div class="section-header">
        <h2>🌐 {t['language']}</h2>
        <p>選擇您的語言偏好 / Choose your language preference</p>
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

def create_hot_stocks_section(hot_stocks, t):
    """創建熱門股票區域"""
    st.markdown(f"""
    <div class="section-header">
        <h2>🔥 {t['hot_stocks']}</h2>
        <p>基於關鍵點分析的熱門投資標的</p>
    </div>
    """, unsafe_allow_html=True)
    
    for stock in hot_stocks:
        change_class = "positive" if stock['change'] >= 0 else "negative"
        change_symbol = "+" if stock['change'] >= 0 else ""
        
        st.markdown(f"""
        <div class="stock-card">
            <div class="stock-header">
                <div>
                    <div class="stock-symbol">{stock['symbol']}</div>
                    <div class="stock-name">{stock['name']}</div>
                </div>
                <div class="stock-price">${stock['price']:.2f}</div>
            </div>
            <div class="stock-metrics">
                <div class="stock-metric">
                    <div class="stock-metric-label">{t['volume']}</div>
                    <div class="stock-metric-value">{stock['volume']}</div>
                </div>
                <div class="stock-metric">
                    <div class="stock-metric-label">變動</div>
                    <div class="stock-metric-value metric-change {change_class}">
                        {change_symbol}{stock['change']:.1f}%
                    </div>
                </div>
                <div class="stock-metric">
                    <div class="stock-metric-label">{t['rating']}</div>
                    <div class="stock-metric-value">{stock['rating']}</div>
                </div>
                <div class="stock-metric">
                    <div class="stock-metric-label">{t['pivot_score']}</div>
                    <div class="stock-metric-value">{stock['pivot_score']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_pivot_insights_section(insights, t):
    """創建關鍵點洞察區域"""
    st.markdown(f"""
    <div class="section-header">
        <h2>🎯 {t['pivot_point_analytics']}</h2>
        <p>AI驅動的市場關鍵轉折點分析</p>
    </div>
    """, unsafe_allow_html=True)
    
    for insight in insights:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">{insight['title']}</div>
            <div class="insight-content">{insight['content']}</div>
            <div class="insight-metrics">
                <div class="insight-metric">
                    <div class="stock-metric-label">信心度</div>
                    <div class="stock-metric-value">{insight['confidence']}%</div>
                </div>
                <div class="insight-metric">
                    <div class="stock-metric-label">風險等級</div>
                    <div class="stock-metric-value">{insight['risk_level']}</div>
                </div>
                <div class="insight-metric">
                    <div class="stock-metric-label">時間範圍</div>
                    <div class="stock-metric-value">{insight['time_horizon']}</div>
                </div>
                <div class="insight-metric">
                    <div class="stock-metric-label">{t['pivot_score']}</div>
                    <div class="stock-metric-value">{insight['pivot_score']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_roadmap_section(t):
    """創建發展路線圖區域"""
    st.markdown(f"""
    <div class="section-header">
        <h2>🗺️ {t['roadmap']}</h2>
        <p>TENKI 平台未來發展計劃</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="roadmap-container">
        <div class="roadmap-phase">
            <h3>1. {t['feature_expansion']}</h3>
            <div class="roadmap-item">{t['add_more_stocks']}</div>
            <div class="roadmap-item">{t['add_portfolio']}</div>
            <div class="roadmap-item">{t['implement_login']}</div>
        </div>
        
        <div class="roadmap-phase">
            <h3>2. {t['data_enhancement']}</h3>
            <div class="roadmap-item">{t['integrate_more_apis']}</div>
            <div class="roadmap-item">{t['add_news_feeds']}</div>
            <div class="roadmap-item">{t['add_technical_indicators']}</div>
        </div>
        
        <div class="roadmap-phase">
            <h3>3. {t['business_preparation']}</h3>
            <div class="roadmap-item">{t['add_subscription']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ====== 主應用程式 ======
def main():
    load_premium_design_system()
    
    lang = st.session_state.language
    t = TEXTS[lang]
    
    # 頂部橫幅 - 使用 IMG_0638.png
    create_top_banner()
    
    # 語言選擇器
    language_selector(t)
    
    # Hero 區域
    create_hero_section(t)
    
    # 即時市場數據
    st.markdown(f"""
    <div class="section-header">
        <h2>📊 {t['real_time_market']}</h2>
        <p>全球主要指數即時追蹤</p>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # 熱門股票區域
    create_hot_stocks_section(market_data['hot_stocks'], t)
    
    # 關鍵點分析洞察
    insights = generate_pivot_insights(t)
    create_pivot_insights_section(insights, t)
    
    # 發展路線圖
    create_roadmap_section(t)
    
    # 底部資訊
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; color: #64748b;">
        <p><strong>TENKI</strong> - {t['tagline']}</p>
        <p>© 2025 TENKI Financial Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
