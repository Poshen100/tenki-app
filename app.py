import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests
from datetime import datetime

st.set_page_config(
    page_title="TENKI - Pivot Point Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 多語言設定略，使用前面你提供的 LANGUAGES 和 TEXTS 字典

if 'language' not in st.session_state:
    st.session_state.language = 'zh'

# 取得即時指數價格（使用 Yahoo Finance API 範例）
def fetch_live_index_price(symbol):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
    try:
        res = requests.get(url)
        data = res.json()
        price = data['quoteResponse']['result'][0]['regularMarketPrice']
        change = data['quoteResponse']['result'][0]['regularMarketChange']
        change_pct = data['quoteResponse']['result'][0]['regularMarketChangePercent'] / 100
        return price, change, change_pct
    except Exception:
        return None, None, None

def get_live_market_data():
    sp_price, sp_change, sp_change_pct = fetch_live_index_price("^GSPC")  # S&P 500
    nasdaq_price, nasdaq_change, nasdaq_change_pct = fetch_live_index_price("^IXIC")  # NASDAQ
    dji_price, dji_change, dji_change_pct = fetch_live_index_price("^DJI")  # Dow Jones
    btc_price, btc_change, btc_change_pct = fetch_live_index_price("BTC-USD")  # Bitcoin
    
    data = {
        'indices': {
            'SP500': {'value': sp_price, 'change': sp_change, 'change_pct': sp_change_pct},
            'NASDAQ': {'value': nasdaq_price, 'change': nasdaq_change, 'change_pct': nasdaq_change_pct},
            'DJI': {'value': dji_price, 'change': dji_change, 'change_pct': dji_change_pct},
            'BTC': {'value': btc_price, 'change': btc_change, 'change_pct': btc_change_pct}
        },
        # 其他資料保持不變或同前，可擴展
    }
    return data

# 其餘功能與 UI 設計請參考之前提供的優化版，並將指數價格改用這個:

def main():
    load_premium_design_system()
    lang = st.session_state.language
    t = TEXTS[lang]

    create_top_navigation(t)
    language_selector()
    st.markdown("---")
    st.markdown(create_hero_section(t), unsafe_allow_html=True)

    # 更新此處取得即時數據
    market_data = get_live_market_data()

    # 顯示指數
    st.markdown(f"### 📊 {t['real_time_market']}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        sp = market_data['indices']['SP500']
        st.markdown(create_metric_card("S&P 500", f"{sp['value']:.2f}", sp['change'], sp['change_pct']), unsafe_allow_html=True)
    with col2:
        ns = market_data['indices']['NASDAQ']
        st.markdown(create_metric_card("NASDAQ", f"{ns['value']:.2f}", ns['change'], ns['change_pct']), unsafe_allow_html=True)
    with col3:
        dj = market_data['indices']['DJI']
        st.markdown(create_metric_card("Dow Jones", f"{dj['value']:.2f}", dj['change'], dj['change_pct']), unsafe_allow_html=True)
    with col4:
        btc = market_data['indices']['BTC']
        st.markdown(create_metric_card("Bitcoin", f"${btc['value']:.0f}", btc['change'], btc['change_pct']), unsafe_allow_html=True)

    # 其餘程式碼照舊 (包括TradingView整合、AI洞察、股票追蹤等)

if __name__ == "__main__":
    main()
    # 頁腳保持不變


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
        "core_features": "核心功能"
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
        "core_features": "Core Features"
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
        "core_features": "コア機能"
    }
}

# ====== Session State 初始化 ======
if 'language' not in st.session_state:
    st.session_state.language = 'zh'

# ====== 快取數據函數 ======
@st.cache_data(ttl=300, show_spinner=False)
def get_market_data():
    """獲取市場數據"""
    return {
        'indices': {
            'SP500': {'value': 4521.32, 'change': 0.85, 'change_pct': 0.019},
            'NASDAQ': {'value': 14125.91, 'change': 125.44, 'change_pct': 0.0089},
            'DJI': {'value': 34567.45, 'change': -45.23, 'change_pct': -0.0013},
            'BTC': {'value': 67234, 'change': 1423, 'change_pct': 0.021}
        },
        'hot_stocks': [
            {'symbol': 'COIN', 'name': 'Coinbase', 'price': 156.42, 'change': 2.8, 'volume': '2.1M', 'rating': '強力買入', 'pivot_score': 85},
            {'symbol': 'MSTR', 'name': 'MicroStrategy', 'price': 1247.85, 'change': 5.2, 'volume': '145K', 'rating': '買入', 'pivot_score': 78},
            {'symbol': 'RIOT', 'name': 'Riot Blockchain', 'price': 8.94, 'change': 1.4, 'volume': '5.8M', 'rating': '買入', 'pivot_score': 72},
            {'symbol': 'NVDA', 'name': 'NVIDIA', 'price': 445.67, 'change': -1.2, 'volume': '32.5M', 'rating': '持有', 'pivot_score': 68},
            {'symbol': 'TSLA', 'name': 'Tesla', 'price': 234.56, 'change': 3.4, 'volume': '45.2M', 'rating': '強力買入', 'pivot_score': 82}
        ]
    }

@st.cache_data(ttl=600, show_spinner=False)
def generate_pivot_insights():
    """生成關鍵點分析洞察"""
    insights = [
        {
            'title': '區塊鏈概念股關鍵突破點',
            'content': '比特幣ETF持續淨流入創新高，COIN突破關鍵阻力位$155，技術面顯示強勢上攻態勢，預期目標價$180-200區間。',
            'confidence': 87,
            'risk_level': '中等',
            'time_horizon': '2-4週',
            'pivot_score': 85,
            'tags': ['技術突破', '資金流入', '關鍵阻力']
        },
        {
            'title': 'AI晶片供應鏈的關鍵轉折',
            'content': 'NVIDIA財報超預期後，整個AI生態鏈進入新一輪上升週期，關注TSM、AMD等在$150關鍵支撐位的表現。',
            'confidence': 82,
            'risk_level': '中高',
            'time_horizon': '4-8週',
            'pivot_score': 78,
            'tags': ['財報驅動', '生態效應', '關鍵支撐']
        }
    ]
    return insights

# ====== 頂級專業UI設計系統（優化版） ======
def load_premium_design_system():
    """載入頂級設計系統 - 提升美感：更細膩的漸層、更流暢動畫、優化間距、提升對比"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        /* === 全域字體系統 === */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-feature-settings: "kern", "liga", "clig", "calt";
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        /* === 隱藏Streamlit元素 === */
        #MainMenu, footer, header, .stDeployButton {visibility: hidden !important;}
        
        /* === 主容器系統 - 提升背景細膩度 === */
        .main .block-container {
            padding: 0rem 2rem 4rem 2rem;
            max-width: 1600px;
            background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        }
        
        /* === 頂部導航欄 - 增加透明度與陰影 === */
        .top-navigation {
            position: sticky;
            top: 0;
            left: 0;
            right: 0;
            height: 72px;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: saturate(200%) blur(24px);
            border-bottom: 1px solid rgba(0, 0, 0, 0.05);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 3rem;
            margin-bottom: 3rem;
            border-radius: 0 0 24px 24px;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.08);
        }
        
        .nav-logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .nav-logo-img {
            width: 40px;
            height: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
            object-fit: cover;
        }
        
        .nav-brand {
            font-size: 24px;
            font-weight: 800;
            background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.03em;
        }
        
        /* === Hero區域設計 - 提升動畫與漸層 === */
        .hero-section {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #475569 100%);
            padding: 6rem 3rem;
            border-radius: 32px;
            margin-bottom: 4rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 12px 48px rgba(0, 0, 0, 0.25);
        }
        
        .hero-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 30% 70%, rgba(59, 130, 246, 0.25) 0%, transparent 60%),
                        radial-gradient(circle at 70% 30%, rgba(255, 255, 255, 0.08) 0%, transparent 60%);
            opacity: 0.8;
        }
        
        .hero-content {
            text-align: center;
            position: relative;
            z-index: 1;
            max-width: 900px;
            margin: 0 auto;
        }
        
        .hero-logo-container {
            margin-bottom: 2.5rem;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            gap: 1.5rem;
        }
        
        .hero-logo {
            width: 120px;
            height: 120px;
            border-radius: 24px;
            filter: drop-shadow(0 12px 48px rgba(0, 0, 0, 0.4));
            animation: heroFloat 5s ease-in-out infinite;
            object-fit: cover;
        }
        
        @keyframes heroFloat {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-12px) rotate(1deg); }
        }
        
        .hero-title {
            font-size: clamp(3.5rem, 9vw, 5.5rem);
            font-weight: 900;
            letter-spacing: -0.05em;
            background: linear-gradient(135deg, #ffffff 0%, #dbeafe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1.25rem;
            line-height: 1;
        }
        
        .hero-subtitle {
            font-size: clamp(1.2rem, 3vw, 1.5rem);
            font-weight: 400;
            color: #d1d5db;
            margin-bottom: 2.5rem;
            letter-spacing: -0.01em;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .hero-cta {
            display: flex;
            justify-content: center;
            gap: 1.25rem;
            flex-wrap: wrap;
        }
        
        .cta-primary, .cta-secondary {
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
            box-shadow: 0 6px 24px rgba(37, 99, 235, 0.3);
        }
        
        .cta-primary:hover {
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 12px 48px rgba(37, 99, 235, 0.4);
        }
        
        .cta-secondary {
            background: rgba(255, 255, 255, 0.08);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.15);
            backdrop-filter: saturate(200%) blur(24px);
        }
        
        .cta-secondary:hover {
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(255, 255, 255, 0.25);
            transform: translateY(-4px) scale(1.02);
        }
        
        /* === 功能卡片系統 - 提升陰影與過渡 === */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2.5rem;
            margin: 4rem 0;
        }
        
        .feature-card {
            background: white;
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 6px 32px rgba(0, 0, 0, 0.1);
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
            transition: height 0.4s ease;
        }
        
        .feature-card:hover::before {
            height: 100%;
            opacity: 0.1;
        }
        
        .feature-card:hover {
            transform: translateY(-12px);
            box-shadow: 0 16px 64px rgba(0, 0, 0, 0.15);
        }
        
        .feature-card.analytics { --accent-color: #3b82f6; --accent-color-light: #60a5fa; }
        .feature-card.portfolio { --accent-color: #8b5cf6; --accent-color-light: #a78bfa; }
        .feature-card.pulse { --accent-color: #06b6d4; --accent-color-light: #22d3ee; }
        .feature-card.academy { --accent-color: #10b981; --accent-color-light: #34d399; }
        
        .feature-icon {
            font-size: 3.5rem;
            margin-bottom: 1.75rem;
            display: block;
            opacity: 0.9;
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
            line-height: 1.6;
            font-weight: 400;
        }
        
        /* === 指標卡片系統 - 增加圓角與動畫 === */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 2rem;
            margin: 4rem 0;
        }
        
        .metric-card {
            background: white;
            border-radius: 20px;
            padding: 2.5rem;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(0, 0, 0, 0.03);
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
            transform: translateY(-6px) scale(1.02);
            box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
        }
        
        .metric-label {
            color: #475569;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin-bottom: 0.75rem;
        }
        
        .metric-value {
            font-size: 2.25rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 0.75rem;
            letter-spacing: -0.03em;
        }
        
        .metric-change {
            font-size: 0.95rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.3rem;
        }
        
        .metric-change.positive { color: #059669; }
        .metric-change.negative { color: #dc2626; }
        
        /* === AI洞察卡片 - 提升漸層與徽章設計 === */
        .insight-card {
            background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
            color: white;
            border-radius: 28px;
            padding: 3.5rem;
            margin: 4rem 0;
            position: relative;
            overflow: hidden;
            box-shadow: 0 12px 48px rgba(30, 64, 175, 0.35);
        }
        
        .insight-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2.5rem;
            flex-wrap: wrap;
            gap: 1.25rem;
        }
        
        .insight-title {
            font-size: 1.75rem;
            font-weight: 700;
            letter-spacing: -0.025em;
        }
        
        .pivot-score {
            background: rgba(255, 255, 255, 0.15);
            color: white;
            padding: 0.6rem 1.25rem;
            border-radius: 24px;
            font-size: 0.9rem;
            font-weight: 600;
            backdrop-filter: saturate(200%) blur(24px);
        }
        
        .insight-content {
            font-size: 1.15rem;
            line-height: 1.75;
            opacity: 0.95;
            margin-bottom: 2.5rem;
        }
        
        .insight-badges {
            display: flex;
            gap: 1.25rem;
            flex-wrap: wrap;
        }
        
        .insight-badge {
            background: rgba(255, 255, 255, 0.12);
            color: white;
            padding: 0.6rem 1.25rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
            backdrop-filter: saturate(200%) blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* === 股票表格 - 提升表格美感與互動 === */
        .stocks-table {
            background: white;
            border-radius: 20px;
            padding: 2.5rem;
            box-shadow: 0 6px 32px rgba(0, 0, 0, 0.1);
            margin: 3rem 0;
            overflow: hidden;
        }
        
        .stock-row {
            display: grid;
            grid-template-columns: 1fr 2fr 1.2fr 1fr 1fr 1.2fr 1fr;
            gap: 1.25rem;
            align-items: center;
            padding: 1.25rem 0;
            border-bottom: 1px solid #f3f4f6;
            transition: all 0.3s ease;
        }
        
        .stock-row:hover {
            background: #f9fafb;
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
            color: #475569;
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
            padding: 0.3rem 0.9rem;
            border-radius: 16px;
            font-size: 0.85rem;
            font-weight: 600;
            text-align: center;
            box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2);
        }
        
        /* === 語言選擇按鈕 - 提升互動性 === */
        .language-buttons {
            display: flex;
            gap: 0.75rem;
            justify-content: center;
            margin: 3rem 0;
        }
        
        .lang-btn {
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 16px;
            padding: 1rem 2rem;
            font-weight: 600;
            color: #374151;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .lang-btn:hover {
            border-color: #2563eb;
            color: #2563eb;
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 6px 24px rgba(37, 99, 235, 0.2);
        }
        
        .lang-btn.active {
            background: #2563eb;
            border-color: #2563eb;
            color: white;
            box-shadow: 0 6px 24px rgba(37, 99, 235, 0.3);
        }
        
        /* === 響應式設計 - 優化移動端 === */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 0rem 1rem 3rem 1rem;
            }
            
            .top-navigation {
                padding: 0 1.5rem;
            }
            
            .hero-section {
                padding: 4rem 2rem;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
                gap: 2rem;
            }
            
            .metrics-grid {
                grid-template-columns: 1fr;
            }
            
            .stock-row {
                grid-template-columns: 1fr;
                gap: 0.75rem;
                text-align: center;
            }
            
            .language-buttons {
                flex-direction: column;
            }
        }
        
        /* === 動畫效果 - 更流暢 === */
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
        
    </style>
    """, unsafe_allow_html=True)

# ====== UI組件函數（優化：減少重複，增加模組化） ======
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
    return f"""
    <div class="hero-section">
        <div class="hero-content">
            <div class="hero-logo-container">
                <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/IMG_0640.jpeg" alt="TENKI Logo" class="hero-logo">
            </div>
            <h1 class="hero-title">{t['app_name']}</h1>
            <p class="hero-subtitle">{t['tagline']}</p>
            <div class="hero-cta">
                <button class="cta-primary">
                    ⚡ 探索功能
                </button>
                <button class="cta-secondary">
                    💎 查看方案
                </button>
            </div>
        </div>
    </div>
    """

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
    change_class = "positive" if change >= 0 else "negative"
    change_symbol = "+" if change >= 0 else ""
    change_icon = "↗" if change >= 0 else "↘"
    return f"""
    <div class="metric-card fade-in">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
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

# ====== 語言選擇器（優化：更緊湊，增加回饋） ======
def language_selector():
    """語言選擇器"""
    st.markdown("### 🌐 語言選擇")
    
    cols = st.columns(3)
    languages = list(LANGUAGES.keys())
    for i, col in enumerate(cols):
        with col:
            if st.button(languages[i], use_container_width=True, 
                         type="primary" if st.session_state.language == LANGUAGES[languages[i]] else "secondary"):
                st.session_state.language = LANGUAGES[languages[i]]
                st.rerun()
    
    current_lang_name = {v: k for k, v in LANGUAGES.items()}[st.session_state.language]
    st.info(f"**當前語言:** {current_lang_name}", icon="ℹ️")

# ====== 主應用程式（優化：更好結構，減少嵌套） ======
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
    st.markdown(create_hero_section(t), unsafe_allow_html=True)
    
    # 核心功能展示
    st.markdown(f"### 🚀 {t['core_features']}")
    
    st.markdown('<div class="features-grid">', unsafe_allow_html=True)
    
    cols = st.columns([1,1,1,1])
    features = [
        ("⚡", t['pivot_point_analytics'], "即時市場數據結合專家演算法，精準識別個股/ETF/債券的關鍵轉折點，風險收益比最優化計算", "analytics"),
        ("🏗️", t['smart_portfolio'], "根據風險承受度客製化投資組合，美股、債券、期指、海外基金智能配置，自動再平衡提醒", "portfolio"),
        ("📡", t['market_pulse'], "Push通知重要市場變化，專家解讀重大經濟事件，投資機會即時推播，關鍵點預警", "pulse"),
        ("🎓", t['investment_academy'], "互動式投資教育內容，成功案例分析，錯誤避免指南，從新手到專家的完整學習路徑", "academy")
    ]
    
    for col, feature in zip(cols, features):
        with col:
            st.markdown(create_feature_card(*feature), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 即時市場數據
    st.markdown(f"### 📊 {t['real_time_market']}")
    
    market_data = get_market_data()
    
    # 主要指數指標卡片
    st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
    
    indices = market_data['indices']
    cols = st.columns(4)
    
    index_data = [
        ("S&P 500", f"{indices['SP500']['value']:,.0f}", indices['SP500']['change'], indices['SP500']['change_pct']),
        ("NASDAQ", f"{indices['NASDAQ']['value']:,.0f}", indices['NASDAQ']['change'], indices['NASDAQ']['change_pct']),
        ("道瓊指數", f"{indices['DJI']['value']:,.0f}", indices['DJI']['change'], indices['DJI']['change_pct']),
        ("Bitcoin", f"${indices['BTC']['value']:,}", indices['BTC']['change'], indices['BTC']['change_pct'])
    ]
    
    for col, data in zip(cols, index_data):
        with col:
            st.markdown(create_metric_card(*data), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # TradingView整合圖表（優化：增加邊框與載入提示）
    with st.container():
        st.markdown("#### 📈 專業交易圖表")
        with st.spinner("載入即時市場數據..."):
            st.components.v1.html(
                """
                <div class="tradingview-widget-container" style="border-radius: 20px; overflow: hidden; box-shadow: 0 6px 32px rgba(0,0,0,0.12); background: white;">
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
                """,
                height=520
            )
    
    # AI關鍵點洞察
    st.markdown(f"### 🧠 {t['ai_recommendations']}")
    
    insights = generate_pivot_insights()
    for insight in insights:
        st.markdown(create_insight_card(insight), unsafe_allow_html=True)
    
    # 熱門股票追蹤
    st.markdown("### 🔥 關鍵點標的追蹤")
    
    st.markdown('<div class="stocks-table fade-in">', unsafe_allow_html=True)
    
    # 表格標題
    st.markdown("""
    <div class="stock-row" style="font-weight: 700; color: #1f2937; border-bottom: 2px solid #e5e7eb;">
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
    
    # 頁腳（優化：增加漸層與間距）
    st.markdown("""
    <div style="margin-top: 5rem; text-align: center; padding: 4rem 0; background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%); border-radius: 28px; box-shadow: 0 4px 24px rgba(0,0,0,0.05);">
        <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/IMG_0640.jpeg" 
             style="width: 80px; height: 80px; border-radius: 16px; margin-bottom: 1.5rem; opacity: 0.85; object-fit: cover;">
        <div style="color: #475569; font-weight: 500; margin-bottom: 0.75rem; font-size: 1.1rem;">
            <strong>投資有風險，入市需謹慎</strong>
        </div>
        <div style="color: #6b7280; font-size: 0.95rem;">
            本平台提供的資訊僅供參考，不構成投資建議
        </div>
    </div>
    """, unsafe_allow_html=True)
