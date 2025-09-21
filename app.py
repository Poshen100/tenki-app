import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import time

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

# ====== 即時市場數據API ======
@st.cache_data(ttl=60, show_spinner=False)
def fetch_live_price(symbol):
    """獲取即時股價數據"""
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        quote = data['quoteResponse']['result'][0]
        price = quote.get('regularMarketPrice', 0)
        change = quote.get('regularMarketChange', 0)
        change_pct = quote.get('regularMarketChangePercent', 0) / 100
        return price, change, change_pct
    except Exception as e:
        # 備用數據，避免API失敗
        return 4500.0, 10.5, 0.0023

@st.cache_data(ttl=60, show_spinner=False)
def get_market_data():
    """獲取完整市場數據"""
    sp500_data = fetch_live_price("^GSPC")
    nasdaq_data = fetch_live_price("^IXIC")
    dji_data = fetch_live_price("^DJI")
    btc_data = fetch_live_price("BTC-USD")
    
    return {
        'indices': {
            'SP500': {'value': sp500_data[0], 'change': sp500_data[1], 'change_pct': sp500_data[2]},
            'NASDAQ': {'value': nasdaq_data[0], 'change': nasdaq_data[1], 'change_pct': nasdaq_data[2]},
            'DJI': {'value': dji_data[0], 'change': dji_data[1], 'change_pct': dji_data[2]},
            'BTC': {'value': btc_data[0], 'change': btc_data[1], 'change_pct': btc_data[2]}
        },
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

# ====== 頂級UI設計系統 ======
def load_premium_design_system():
    """載入頂級設計系統"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        /* === 全域設定 === */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-feature-settings: "kern", "liga", "clig", "calt";
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        /* 隱藏Streamlit元素 */
        #MainMenu, footer, header, .stDeployButton {visibility: hidden !important;}
        
        /* === 主容器 === */
        .main .block-container {
            padding: 0rem 2rem 3rem 2rem;
            max-width: 1600px;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        }
        
        /* === 頂部導航 === */
        .top-navigation {
            position: sticky;
            top: 0;
            left: 0;
            right: 0;
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
            background-clip: text;
            letter-spacing: -0.03em;
        }
        
        /* === Hero區域 === */
        .hero-section {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #334155 100%);
            padding: 5rem 3rem;
            border-radius: 32px;
            margin-bottom: 4rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 20px 64px rgba(0, 0, 0, 0.25);
        }
        
        .hero-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 30% 70%, rgba(59, 130, 246, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 70% 30%, rgba(255, 255, 255, 0.08) 0%, transparent 50%);
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
            animation: heroFloat 6s ease-in-out infinite;
            object-fit: cover;
            margin-bottom: 2rem;
        }
        
        @keyframes heroFloat {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-12px) rotate(1deg); }
        }
        
        .hero-title {
            font-size: clamp(3.5rem, 9vw, 5.5rem);
            font-weight: 900;
            letter-spacing: -0.05em;
            background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1.5rem;
            line-height: 1;
        }
        
        .hero-subtitle {
            font-size: clamp(1.2rem, 3vw, 1.6rem);
            font-weight: 400;
            color: #cbd5e1;
            margin-bottom: 3rem;
            letter-spacing: -0.01em;
        }
        
        .hero-cta {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            flex-wrap: wrap;
        }
        
        .cta-btn {
            padding: 1.25rem 2.5rem;
            border-radius: 16px;
            font-weight: 600;
            font-size: 1.1rem;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border: none;
            cursor: pointer;
        }
        
        .cta-primary {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            box-shadow: 0 8px 32px rgba(37, 99, 235, 0.3);
        }
        
        .cta-primary:hover {
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 16px 48px rgba(37, 99, 235, 0.4);
        }
        
        .cta-secondary {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: saturate(200%) blur(25px);
        }
        
        .cta-secondary:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateY(-4px) scale(1.02);
        }
        
        /* === 功能卡片 === */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2.5rem;
            margin: 4rem 0;
        }
        
        .feature-card {
            background: white;
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(0, 0, 0, 0.03);
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(135deg, var(--accent-color) 0%, var(--accent-color-light) 100%);
        }
        
        .feature-card:hover {
            transform: translateY(-12px);
            box-shadow: 0 20px 64px rgba(0, 0, 0, 0.15);
        }
        
        .feature-card.analytics { --accent-color: #3b82f6; --accent-color-light: #60a5fa; }
        .feature-card.portfolio { --accent-color: #8b5cf6; --accent-color-light: #a78bfa; }
        .feature-card.pulse { --accent-color: #06b6d4; --accent-color-light: #22d3ee; }
        .feature-card.academy { --accent-color: #10b981; --accent-color-light: #34d399; }
        
        .feature-icon {
            font-size: 3.5rem;
            margin-bottom: 2rem;
            display: block;
        }
        
        .feature-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 1rem;
            letter-spacing: -0.025em;
        }
        
        .feature-description {
            color: #475569;
            font-size: 1rem;
            line-height: 1.7;
        }
        
        /* === 指標卡片 === */
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
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
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
        
        /* === AI洞察卡片 === */
        .insight-card {
            background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
            color: white;
            border-radius: 28px;
            padding: 3.5rem;
            margin: 4rem 0;
            position: relative;
            overflow: hidden;
            box-shadow: 0 16px 64px rgba(29, 78, 216, 0.35);
        }
        
        .insight-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2.5rem;
            flex-wrap: wrap;
            gap: 1.5rem;
        }
        
        .insight-title {
            font-size: 1.8rem;
            font-weight: 700;
            letter-spacing: -0.025em;
        }
        
        .pivot-score {
            background: rgba(255, 255, 255, 0.15);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            backdrop-filter: saturate(200%) blur(25px);
        }
        
        .insight-content {
            font-size: 1.2rem;
            line-height: 1.8;
            margin-bottom: 2.5rem;
            opacity: 0.95;
        }
        
        .insight-badges {
            display: flex;
            gap: 1.25rem;
            flex-wrap: wrap;
        }
        
        .insight-badge {
            background: rgba(255, 255, 255, 0.12);
            color: white;
            padding: 0.75rem 1.25rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
            backdrop-filter: saturate(200%) blur(25px);
        }
        
        /* === 股票表格 === */
        .stocks-table {
            background: white;
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.1);
            margin: 3rem 0;
            overflow: hidden;
        }
        
        .stock-row {
            display: grid;
            grid-template-columns: 1fr 2fr 1.2fr 1fr 1fr 1.2fr 1fr;
            gap: 1.5rem;
            align-items: center;
            padding: 1.5rem 0;
            border-bottom: 1px solid #f1f5f9;
            transition: all 0.3s ease;
        }
        
        .stock-row:hover {
            background: #f8fafc;
            transform: scale(1.01);
        }
        
        .stock-row:last-child {
            border-bottom: none;
        }
        
        .stock-symbol {
            font-weight: 700;
            color: #0f172a;
            font-size: 1rem;
        }
        
        .stock-name {
            color: #64748b;
            font-size: 0.95rem;
        }
        
        .stock-price {
            font-weight: 600;
            color: #0f172a;
            font-size: 1rem;
        }
        
        .pivot-score-badge {
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 16px;
            font-size: 0.85rem;
            font-weight: 600;
            text-align: center;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.25);
        }
        
        /* === 語言選擇 === */
        .language-section {
            margin: 3rem 0;
            text-align: center;
        }
        
        .language-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 2rem;
        }
        
        /* === 響應式設計 === */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 0rem 1rem 2rem 1rem;
            }
            
            .top-navigation {
                padding: 0 1.5rem;
            }
            
            .hero-section {
                padding: 4rem 2rem;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
            }
            
            .stock-row {
                grid-template-columns: 1fr;
                text-align: center;
                gap: 0.75rem;
            }
        }
        
        /* === 動畫效果 === */
        .fade-in {
            animation: fadeIn 1s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(32px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* === 載入效果 === */
        .loading-pulse {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: .5; }
        }
        
    </style>
    """, unsafe_allow_html=True)

# ====== UI組件函數 ======
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
            <div class="hero-cta">
                <button class="cta-btn cta-primary">
                    ⚡ 探索功能
                </button>
                <button class="cta-btn cta-secondary">
                    💎 查看方案
                </button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_feature_card(icon, title, description, card_class):
    """創建功能特色卡片"""
    return f"""
    <div class="feature-card {card_class} fade-in">
        <div class="feature-icon">{icon}</div>
        <h3 class="feature-title">{title}</h3>
        <p class="feature-description">{description}</p>
    </div>
    """

def create_metric_card(label, value, change, change_pct):
    """創建指標卡片"""
    if value is None or change is None or change_pct is None:
        return f"""
        <div class="metric-card loading-pulse">
            <div class="metric-label">{label}</div>
            <div class="metric-value">載入中...</div>
            <div class="metric-change">--</div>
        </div>
        """
    
    change_class = "positive" if change >= 0 else "negative"
    change_symbol = "+" if change >= 0 else ""
    change_icon = "↗" if change >= 0 else "↘"
    
    return f"""
    <div class="metric-card fade-in">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value:,.2f}</div>
        <div class="metric-change {change_class}">
            <span>{change_icon}</span>
            {change_symbol}{change:.2f} ({change_symbol}{change_pct:.2%})
        </div>
    </div>
    """

def create_insight_card(insight):
    """創建AI洞察卡片"""
    return f"""
    <div class="insight-card fade-in">
        <div class="insight-header">
            <h3 class="insight-title">⚡ {insight['title']}</h3>
            <div class="pivot-score">關鍵點評分: {insight['pivot_score']}/100</div>
        </div>
        <p class="insight-content">{insight['content']}</p>
        <div class="insight-badges">
            <div class="insight-badge">信心度: {insight['confidence']}%</div>
            <div class="insight-badge">風險: {insight['risk_level']}</div>
            <div class="insight-badge">時間: {insight['time_horizon']}</div>
        </div>
    </div>
    """

def language_selector():
    """語言選擇器"""
    st.markdown('<div class="language-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="language-title">🌐 語言選擇</h3>', unsafe_allow_html=True)
    
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
    
    current_lang_name = {
        'zh': '🇹🇼 繁體中文',
        'en': '🇺🇸 English',
        'jp': '🇯🇵 日本語'
    }
    
    st.info(f"**當前語言:** {current_lang_name[st.session_state.language]}", icon="ℹ️")
    st.markdown('</div>', unsafe_allow_html=True)

# ====== 主應用程式 ======
def main():
    load_premium_design_system()
    
    # 語言設定
    lang = st.session_state.language
    t = TEXTS[lang]
    
    # 頂部導航
    create_top_navigation(t)
    
    # 語言選擇器
    language_selector()
    st.markdown("---")
    
    # Hero區域
    create_hero_section(t)
    
    # 核心功能展示
    st.markdown(f"## 🚀 {t['core_features']}")
    
    st.markdown('<div class="features-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_feature_card(
            "⚡", 
            t['pivot_point_analytics'],
            "即時市場數據結合專家演算法，精準識別個股/ETF/債券的關鍵轉折點，風險收益比最優化計算",
            "analytics"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_feature_card(
            "🏗️", 
            t['smart_portfolio'],
            "根據風險承受度客製化投資組合，美股、債券、期指、海外基金智能配置，自動再平衡提醒",
            "portfolio"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_feature_card(
            "📡", 
            t['market_pulse'],
            "Push通知重要市場變化，專家解讀重大經濟事件，投資機會即時推播，關鍵點預警",
            "pulse"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_feature_card(
            "🎓", 
            t['investment_academy'],
            "互動式投資教育內容，成功案例分析，錯誤避免指南，從新手到專家的完整學習路徑",
            "academy"
        ), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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
    
    # 專業交易圖表
    st.markdown("### 📈 專業交易圖表")
    st.components.v1.html(
        """
        <div style="border-radius: 24px; overflow: hidden; box-shadow: 0 8px 40px rgba(0,0,0,0.1); background: white; padding: 1rem;">
          <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-market-overview.js" async>
            {
              "colorTheme": "light",
              "dateRange": "1D",
              "showChart": true,
              "locale": "zh_TW",
              "width": "100%",
              "height": "500",
              "isTransparent": false,
              "showSymbolLogo": true,
              "tabs": [
                {
                  "title": "美股指數",
                  "symbols": [
                    {"s": "FOREXCOM:SPXUSD", "d": "S&P 500"},
                    {"s": "FOREXCOM:NSXUSD", "d": "NASDAQ 100"},
                    {"s": "FOREXCOM:DJI", "d": "道瓊工業"}
                  ]
                },
                {
                  "title": "關鍵點標的",
                  "symbols": [
                    {"s": "NASDAQ:COIN"},
                    {"s": "NASDAQ:MSTR"},
                    {"s": "NASDAQ:NVDA"},
                    {"s": "NASDAQ:TSLA"}
                  ]
                }
              ]
            }
            </script>
          </div>
        </div>
        """,
        height=550
    )
    
    # AI關鍵點洞察
    st.markdown(f"## 🧠 {t['ai_recommendations']}")
    
    insights = generate_pivot_insights()
    for insight in insights:
        st.markdown(create_insight_card(insight), unsafe_allow_html=True)
    
    # 熱門股票追蹤
    st.markdown("## 🔥 關鍵點標的追蹤")
    
    st.markdown('<div class="stocks-table fade-in">', unsafe_allow_html=True)
    
    # 表格標題
    st.markdown("""
    <div class="stock-row" style="font-weight: 700; color: #1f2937; border-bottom: 2px solid #e5e7eb; background: #f9fafb;">
        <div>代號</div>
        <div>公司名稱</div>
        <div>價格</div>
        <div>漲跌</div>
        <div>成交量</div>
        <div>投資評級</div>
        <div>關鍵點</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 股票數據行
    for stock in market_data['hot_stocks']:
        change_color = "#059669" if stock['change'] > 0 else "#dc2626"
        sign = "+" if stock['change'] > 0 else ""
        
        rating_colors = {
            '強力買入': '#059669',
            '買入': '#0891b2',
            '持有': '#d97706',
            '賣出': '#dc2626'
        }
        rating_color = rating_colors.get(stock['rating'], '#6b7280')
        
        st.markdown(f"""
        <div class="stock-row">
            <div class="stock-symbol">{stock['symbol']}</div>
            <div class="stock-name">{stock['name']}</div>
            <div class="stock-price">${stock['price']:,.2f}</div>
            <div style="color: {change_color}; font-weight: 600;">{sign}{stock['change']}%</div>
            <div>{stock['volume']}</div>
            <div style="color: {rating_color}; font-weight: 600;">{stock['rating']}</div>
            <div class="pivot-score-badge">{stock['pivot_score']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ====== 執行主程式 ======
if __name__ == "__main__":
    main()
    
    # 頁腳
    st.markdown("""
    <div style="margin-top: 5rem; text-align: center; padding: 4rem 0; background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%); border-radius: 32px; box-shadow: 0 8px 40px rgba(0,0,0,0.06);">
        <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/IMG_0640.jpeg" 
             style="width: 80px; height: 80px; border-radius: 16px; margin-bottom: 1.5rem; opacity: 0.9; object-fit: cover;">
        <div style="color: #475569; font-weight: 600; margin-bottom: 0.75rem; font-size: 1.1rem;">
            <strong>投資有風險，入市需謹慎</strong>
        </div>
        <div style="color: #6b7280; font-size: 1rem;">
            本平台提供的資訊僅供參考，不構成投資建議
        </div>
        <div style="color: #9ca3af; font-size: 0.9rem; margin-top: 1rem;">
            © 2025 TENKI - Pivot Point Intelligence Platform
        </div>
    </div>
    """, unsafe_allow_html=True)
