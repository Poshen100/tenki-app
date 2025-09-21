import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
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
    "繁體中文": "zh",
    "English": "en", 
    "日本語": "jp"
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
if 'user_plan' not in st.session_state:
    st.session_state.user_plan = 'basic'

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

# ====== 頂級專業UI設計 ======
def load_premium_design_system():
    """載入頂級設計系統"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700;800;900&family=SF+Mono:wght@400;500;600&display=swap');
        
        /* === 全域字體系統 === */
        * {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-feature-settings: "kern", "liga", "clig", "calt";
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        /* === 隱藏Streamlit元素 === */
        #MainMenu, footer, header, .stDeployButton {visibility: hidden !important;}
        
        /* === 主容器系統 === */
        .main .block-container {
            padding: 0rem 2rem 2rem 2rem;
            max-width: 1800px;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        }
        
        /* === 頂部導航欄 === */
        .top-navigation {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 80px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: saturate(180%) blur(20px);
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 2rem;
        }
        
        .nav-logo {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        
        .nav-logo img {
            width: 48px;
            height: 48px;
        }
        
        .nav-brand {
            font-size: 24px;
            font-weight: 800;
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .nav-controls {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        
        .language-selector {
            background: white;
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: 500;
            color: #374151;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        .language-selector:hover {
            border-color: #3b82f6;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
        }
        
        /* === Hero區域設計 === */
        .hero-section {
            margin-top: 80px;
            width: 100vw;
            margin-left: calc(-50vw + 50%);
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            padding: 6rem 0 4rem 0;
            position: relative;
            overflow: hidden;
        }
        
        .hero-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                        radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
        }
        
        .hero-content {
            text-align: center;
            position: relative;
            z-index: 1;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }
        
        .hero-logo-container {
            margin-bottom: 2rem;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            gap: 1rem;
        }
        
        .hero-logo {
            width: 120px;
            height: 120px;
            filter: drop-shadow(0 8px 32px rgba(0, 0, 0, 0.3));
            animation: heroFloat 6s ease-in-out infinite;
        }
        
        @keyframes heroFloat {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .hero-title {
            font-size: clamp(3rem, 8vw, 6rem);
            font-weight: 900;
            letter-spacing: -0.04em;
            background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
            line-height: 0.9;
        }
        
        .hero-subtitle {
            font-size: clamp(1.25rem, 3vw, 1.75rem);
            font-weight: 400;
            color: #cbd5e1;
            margin-bottom: 2rem;
            letter-spacing: -0.01em;
        }
        
        .hero-cta {
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
        }
        
        .cta-primary {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            color: white;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1.1rem;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
        }
        
        .cta-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 32px rgba(59, 130, 246, 0.4);
        }
        
        .cta-secondary {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1.1rem;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.2);
            cursor: pointer;
            backdrop-filter: saturate(180%) blur(20px);
        }
        
        .cta-secondary:hover {
            background: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.3);
        }
        
        /* === 核心功能卡片系統 === */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2rem;
            margin: 4rem 0;
            padding: 0 1rem;
        }
        
        .feature-card {
            background: white;
            border-radius: 20px;
            padding: 2.5rem;
            box-shadow: 0 4px 32px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(0, 0, 0, 0.05);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, var(--accent-color) 0%, var(--accent-color-light) 100%);
        }
        
        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
        }
        
        .feature-card.analytics { --accent-color: #3b82f6; --accent-color-light: #60a5fa; }
        .feature-card.portfolio { --accent-color: #8b5cf6; --accent-color-light: #a78bfa; }
        .feature-card.pulse { --accent-color: #06b6d4; --accent-color-light: #22d3ee; }
        .feature-card.academy { --accent-color: #10b981; --accent-color-light: #34d399; }
        
        .feature-icon {
            width: 64px;
            height: 64px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, var(--accent-color), var(--accent-color-light));
            color: white;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        }
        
        .feature-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.75rem;
            letter-spacing: -0.02em;
        }
        
        .feature-description {
            color: #64748b;
            font-size: 1rem;
            line-height: 1.7;
            font-weight: 400;
        }
        
        /* === 指標卡片系統 === */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 3rem 0;
        }
        
        .metric-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(0, 0, 0, 0.05);
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        }
        
        .metric-label {
            color: #64748b;
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }
        
        .metric-value {
            font-size: 2.25rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }
        
        .metric-change {
            font-size: 0.875rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.25rem;
        }
        
        .metric-change.positive { color: #059669; }
        .metric-change.negative { color: #dc2626; }
        
        /* === AI洞察卡片 === */
        .insight-card {
            background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
            color: white;
            border-radius: 24px;
            padding: 3rem;
            margin: 3rem 0;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 40px rgba(30, 64, 175, 0.3);
        }
        
        .insight-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        }
        
        .insight-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        .insight-title {
            font-size: 1.75rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        
        .pivot-score {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 600;
            backdrop-filter: saturate(180%) blur(20px);
        }
        
        .insight-content {
            font-size: 1.125rem;
            line-height: 1.7;
            opacity: 0.95;
            margin-bottom: 2rem;
        }
        
        .insight-badges {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }
        
        .insight-badge {
            background: rgba(255, 255, 255, 0.15);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 16px;
            font-size: 0.875rem;
            font-weight: 500;
            backdrop-filter: saturate(180%) blur(20px);
        }
        
        /* === 價格方案卡片 === */
        .pricing-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }
        
        .pricing-card {
            background: white;
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 4px 32px rgba(0, 0, 0, 0.1);
            border: 2px solid transparent;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .pricing-card.featured {
            border-color: #3b82f6;
            transform: scale(1.05);
            box-shadow: 0 12px 48px rgba(59, 130, 246, 0.2);
        }
        
        .pricing-card.featured::before {
            content: '推薦';
            position: absolute;
            top: 0;
            right: 0;
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            color: white;
            padding: 0.75rem 1.5rem;
            font-size: 0.875rem;
            font-weight: 600;
            border-bottom-left-radius: 16px;
        }
        
        .pricing-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .pricing-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.5rem;
        }
        
        .pricing-price {
            font-size: 3.5rem;
            font-weight: 900;
            color: #3b82f6;
            margin-bottom: 0.5rem;
            letter-spacing: -0.04em;
        }
        
        .pricing-period {
            color: #64748b;
            font-size: 1rem;
            font-weight: 500;
        }
        
        .pricing-features {
            list-style: none;
            padding: 0;
            margin: 2rem 0;
        }
        
        .pricing-features li {
            padding: 0.75rem 0;
            color: #374151;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 0.95rem;
        }
        
        .pricing-features li::before {
            content: '✓';
            color: #059669;
            font-weight: bold;
            font-size: 1.1rem;
            width: 20px;
            height: 20px;
            background: #ecfdf5;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        
        .subscribe-btn {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 1rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
        }
        
        .subscribe-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
        }
        
        /* === 股票表格 === */
        .stocks-table {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
            margin: 2rem 0;
            overflow: hidden;
        }
        
        .stock-row {
            display: grid;
            grid-template-columns: 1fr 2fr 1.5fr 1fr 1fr 1.2fr 1fr;
            gap: 1rem;
            align-items: center;
            padding: 1rem 0;
            border-bottom: 1px solid #f1f5f9;
            transition: all 0.2s ease;
        }
        
        .stock-row:hover {
            background: #f8fafc;
        }
        
        .stock-row:last-child {
            border-bottom: none;
        }
        
        .stock-symbol {
            font-weight: 700;
            color: #0f172a;
            font-size: 0.95rem;
        }
        
        .stock-name {
            color: #64748b;
            font-size: 0.9rem;
        }
        
        .stock-price {
            font-weight: 600;
            color: #0f172a;
            font-size: 0.95rem;
        }
        
        .stock-change {
            font-weight: 600;
            font-size: 0.9rem;
        }
        
        .stock-volume {
            color: #64748b;
            font-size: 0.9rem;
        }
        
        .pivot-score-badge {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            text-align: center;
        }
        
        /* === 響應式設計 === */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 0rem 1rem 2rem 1rem;
            }
            
            .top-navigation {
                padding: 0 1rem;
            }
            
            .hero-content {
                padding: 0 1rem;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
            
            .pricing-card.featured {
                transform: none;
            }
            
            .stock-row {
                grid-template-columns: 1fr;
                gap: 0.5rem;
                text-align: center;
            }
            
            .nav-controls {
                flex-direction: column;
                gap: 8px;
            }
        }
        
        /* === 動畫效果 === */
        .fade-in {
            animation: fadeIn 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(24px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
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
            <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/image.jpeg" alt="TENKI Logo">
            <div class="nav-brand">{t['app_name']}</div>
        </div>
        <div class="nav-controls">
            <div class="language-selector" id="language-selector">
                🌐 {t['language']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_hero_section(t):
    """創建Hero區域"""
    return f"""
    <div class="hero-section">
        <div class="hero-content">
            <div class="hero-logo-container">
                <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/image.jpeg" alt="TENKI Logo" class="hero-logo">
            </div>
            <h1 class="hero-title">{t['app_name']}</h1>
            <p class="hero-subtitle">{t['tagline']}</p>
            <div class="hero-cta">
                <button class="cta-primary" onclick="scrollToFeatures()">
                    ⚡ 探索功能
                </button>
                <button class="cta-secondary" onclick="scrollToPricing()">
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
    <div class="metric-card">
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

def create_pricing_card(title, price, period, features, is_featured=False):
    """創建價格方案卡片"""
    featured_class = "featured" if is_featured else ""
    return f"""
    <div class="pricing-card {featured_class}">
        <div class="pricing-header">
            <h3 class="pricing-title">{title}</h3>
            <div class="pricing-price">${price}</div>
            <div class="pricing-period">/{period}</div>
        </div>
        <ul class="pricing-features">
            {''.join([f'<li>{feature}</li>' for feature in features])}
        </ul>
        <button class="subscribe-btn" onclick="handleSubscription('{title}', {price})">
            立即訂閱
        </button>
    </div>
    """

# ====== 主應用程式 ======
def main():
    load_premium_design_system()
    
    # 語言設定
    lang = st.session_state.language
    t = TEXTS[lang]
    
    # 頂部導航
    create_top_navigation(t)
    
    # Hero區域
    st.markdown(create_hero_section(t), unsafe_allow_html=True)
    
    # 核心功能展示
    st.markdown('<div id="features"></div>', unsafe_allow_html=True)
    st.markdown(f"### 🚀 {t['core_features']}")
    
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
    st.markdown(f"### 📊 {t['real_time_market']}")
    
    market_data = get_market_data()
    
    # 主要指數指標卡片
    st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
    
    indices = market_data['indices']
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        sp_data = indices['SP500']
        st.markdown(create_metric_card("S&P 500", f"{sp_data['value']:,.0f}", sp_data['change'], sp_data['change_pct']), unsafe_allow_html=True)
    
    with col2:
        nasdaq_data = indices['NASDAQ']
        st.markdown(create_metric_card("NASDAQ", f"{nasdaq_data['value']:,.0f}", nasdaq_data['change'], nasdaq_data['change_pct']), unsafe_allow_html=True)
    
    with col3:
        dji_data = indices['DJI']
        st.markdown(create_metric_card("道瓊指數", f"{dji_data['value']:,.0f}", dji_data['change'], dji_data['change_pct']), unsafe_allow_html=True)
    
    with col4:
        btc_data = indices['BTC']
        st.markdown(create_metric_card("Bitcoin", f"${btc_data['value']:,}", btc_data['change'], btc_data['change_pct']), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # TradingView整合圖表
    with st.container():
        st.markdown("#### 📈 專業交易圖表")
        with st.spinner("載入即時市場數據..."):
            st.components.v1.html(
                """
                <div class="tradingview-widget-container" style="border-radius: 16px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.1);">
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
                          {"s": "FOREXCOM:DJI", "d": "道瓊工業"},
                          {"s": "AMEX:VTI", "d": "整體市場ETF"}
                        ]
                      },
                      {
                        "title": "關鍵點標的",
                        "symbols": [
                          {"s": "NASDAQ:COIN"},
                          {"s": "NASDAQ:MSTR"},
                          {"s": "NASDAQ:NVDA"},
                          {"s": "NASDAQ:TSLA"},
                          {"s": "NASDAQ:AAPL"},
                          {"s": "NASDAQ:MSFT"}
                        ]
                      },
                      {
                        "title": "債券 & 商品",
                        "symbols": [
                          {"s": "AMEX:TLT", "d": "美國長債"},
                          {"s": "AMEX:GLD", "d": "黃金ETF"},
                          {"s": "AMEX:USO", "d": "原油ETF"},
                          {"s": "FOREXCOM:USDTWD", "d": "美元台幣"}
                        ]
                      }
                    ]
                  }
                  </script>
                </div>
                """,
                height=550
            )
    
    # AI關鍵點洞察
    st.markdown(f"### 🧠 {t['ai_recommendations']}")
    
    insights = generate_pivot_insights()
    for insight in insights:
        st.markdown(create_insight_card(insight), unsafe_allow_html=True)
    
    # 熱門股票追蹤
    st.markdown("### 🔥 關鍵點標的追蹤")
    
    st.markdown('<div class="stocks-table">', unsafe_allow_html=True)
    
    # 表格標題
    st.markdown("""
    <div class="stock-row" style="font-weight: 600; color: #374151; border-bottom: 2px solid #e5e7eb;">
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
        change_class = "positive" if stock['change'] > 0 else "negative"
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
            <div class="stock-change" style="color: {change_color};">{sign}{stock['change']}%</div>
            <div class="stock-volume">{stock['volume']}</div>
            <div style="color: {rating_color}; font-weight: 600;">{stock['rating']}</div>
            <div class="pivot-score-badge">{stock['pivot_score']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 訂閱方案
    st.markdown('<div id="pricing"></div>', unsafe_allow_html=True)
    st.markdown(f"### 💎 {t['pricing_plans']}")
    
    st.markdown('<div class="pricing-grid">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(create_pricing_card(
            t['basic_plan'],
            22,
            "月",
            [
                "關鍵點分析基礎版",
                "5個股票追蹤",
                "基本市場數據",
                "月度投資報告",
                "社群支援"
            ]
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_pricing_card(
            t['advanced_plan'],
            39,
            "月",
            [
                "完整關鍵點分析",
                "無限股票追蹤",
                "即時市場數據",
                "AI投資建議",
                "智能組合建構",
                "市場脈動推播",
                "週報分析",
                "優先客服支援"
            ],
            is_featured=True
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_pricing_card(
            t['enterprise_plan'],
            99,
            "月",
            [
                "企業級完整功能",
                "團隊帳戶管理",
                "自定義分析",
                "API存取權限",
                "專屬客戶經理",
                "客製化報告",
                "白標解決方案",
                "電話支援"
            ]
        ), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # JavaScript功能
    st.markdown("""
    <script>
    function handleSubscription(plan, price) {
        alert(`正在為您準備 ${plan} 方案的訂閱流程 (月費 $${price} USD)\\n\\n功能包含：\\n• 完整關鍵點分析\\n• AI投資建議\\n• 即時市場數據\\n• 專業客服支援`);
        // 這裡可以整合 Stripe 或其他支付系統
    }
    
    function scrollToFeatures() {
        document.getElementById('features').scrollIntoView({behavior: 'smooth'});
    }
    
    function scrollToPricing() {
        document.getElementById('pricing').scrollIntoView({behavior: 'smooth'});
    }
    
    // 語言選擇功能
    document.getElementById('language-selector').addEventListener('click', function() {
        const langs = ['繁體中文', 'English', '日本語'];
        const current = '繁體中文'; // 這裡可以動態獲取當前語言
        const nextIndex = (langs.indexOf(current) + 1) % langs.length;
        const nextLang = langs[nextIndex];
        alert(`切換到 ${nextLang}\\n\\n此功能需要重新載入頁面`);
        // 這裡可以實現實際的語言切換邏輯
    });
    </script>
    """, unsafe_allow_html=True)

# ====== 語言選擇邊欄（保留但隱藏） ======
def setup_language_selector():
    """設置語言選擇器（在隱藏的側邊欄中）"""
    with st.sidebar:
        st.markdown("## ⚙️ 設定")
        
        # 語言選擇
        selected_lang = st.selectbox(
            "🌐 語言選擇",
            options=list(LANGUAGES.keys()),
            index=list(LANGUAGES.values()).index(st.session_state.language),
            key="lang_select"
        )
        
        if LANGUAGES[selected_lang] != st.session_state.language:
            st.session_state.language = LANGUAGES[selected_lang]
            st.rerun()
        
        # 其他設定
        st.markdown("### 📊 投資偏好")
        risk_tolerance = st.select_slider(
            "風險承受度",
            options=["保守", "穩健", "積極", "激進"],
            value="穩健"
        )
        
        investment_horizon = st.selectbox(
            "投資時間",
            ["短期 (< 1年)", "中期 (1-3年)", "長期 (> 3年)"]
        )
        
        st.markdown("---")
        st.caption("TENKI v3.0 - Pivot Point Intelligence")
        st.caption("© 2024 專為海外投資者設計")

# ====== 執行主程式 ======
if __name__ == "__main__":
    setup_language_selector()  # 隱藏的語言選擇器
    main()
    
    # 頁腳
    st.markdown("""
    <div style="margin-top: 6rem; text-align: center; padding: 3rem 0; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 24px;">
        <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/image.jpeg" 
             style="width: 80px; height: 80px; margin-bottom: 1rem; opacity: 0.8;">
        <div style="color: #64748b; font-weight: 500; margin-bottom: 0.5rem;">
            <strong>投資有風險，入市需謹慎</strong>
        </div>
        <div style="color: #94a3b8; font-size: 0.9rem;">
            本平台提供的資訊僅供參考，不構成投資建議
        </div>
    </div>
    """, unsafe_allow_html=True)
