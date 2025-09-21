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
        "explore_features": "⚡ 探索功能",
        "view_plans": "💎 查看方案",
        "trading_chart": "專業交易圖表",
        "pivot_targets": "關鍵點標的追蹤",
        "pivot_score": "關鍵點評分",
        "confidence": "信心度",
        "risk": "風險",
        "time": "時間",
        "symbol": "代號",
        "company_name": "公司名稱",
        "price": "價格",
        "change": "漲跌",
        "volume": "成交量",
        "rating": "投資評級",
        "sp_500": "S&P 500",
        "nasdaq": "NASDAQ",
        "dji": "道瓊指數",
        "bitcoin": "Bitcoin",
        "strong_buy": "強力買入",
        "buy": "買入",
        "hold": "持有",
        "sell": "賣出",
        "market_disclaimer": "投資有風險，入市需謹慎",
        "disclaimer_details": "本平台提供的資訊僅供參考，不構成投資建議",
        "loading_market_data": "載入即時市場數據...",
        "current_language": "當前語言:"
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
        "explore_features": "⚡ Explore Features",
        "view_plans": "💎 View Plans",
        "trading_chart": "Professional Trading Chart",
        "pivot_targets": "Pivot Point Targets",
        "pivot_score": "Pivot Score",
        "confidence": "Confidence",
        "risk": "Risk",
        "time": "Time",
        "symbol": "Symbol",
        "company_name": "Company Name",
        "price": "Price",
        "change": "Change",
        "volume": "Volume",
        "rating": "Rating",
        "sp_500": "S&P 500",
        "nasdaq": "NASDAQ",
        "dji": "Dow Jones",
        "bitcoin": "Bitcoin",
        "strong_buy": "Strong Buy",
        "buy": "Buy",
        "hold": "Hold",
        "sell": "Sell",
        "market_disclaimer": "Investing involves risk, proceed with caution",
        "disclaimer_details": "Information provided on this platform is for reference only and does not constitute investment advice",
        "loading_market_data": "Loading real-time market data...",
        "current_language": "Current Language:"
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
        "explore_features": "⚡ 機能を探る",
        "view_plans": "💎 プランを見る",
        "trading_chart": "プロの取引チャート",
        "pivot_targets": "ピボットポイント目標",
        "pivot_score": "ピボットスコア",
        "confidence": "信頼度",
        "risk": "リスク",
        "time": "期間",
        "symbol": "シンボル",
        "company_name": "会社名",
        "price": "価格",
        "change": "変動",
        "volume": "出来高",
        "rating": "評価",
        "sp_500": "S&P 500",
        "nasdaq": "NASDAQ",
        "dji": "ダウ・ジョーンズ",
        "bitcoin": "ビットコイン",
        "strong_buy": "強力買い",
        "buy": "買い",
        "hold": "ホールド",
        "sell": "売り",
        "market_disclaimer": "投資にはリスクが伴います、慎重に進めてください",
        "disclaimer_details": "本プラットフォームで提供される情報は参照用であり、投資アドバイスを構成するものではありません",
        "loading_market_data": "リアルタイム市場データを読み込み中...",
        "current_language": "現在の言語:"
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

# ====== 頂級專業UI設計 ======
def load_premium_design_system():
    """載入頂級設計系統"""
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
        #MainMenu, footer, header, .stDeployButton, .st-emotion-cache-h5rgzm {visibility: hidden !important;}
        .st-emotion-cache-vk3377 { /* targeting the 'manage app' button */
            display: none !important;
        }
        
        /* === 主容器系統 === */
        .main .block-container {
            padding: 0rem 2rem 2rem 2rem; /* Adjusted horizontal padding */
            max-width: 1600px; /* Slightly reduced max width for better focus */
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        }
        
        /* === 頂部導航欄 === */
        .top-navigation {
            position: sticky;
            top: 0;
            left: 0;
            right: 0;
            height: 80px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: saturate(180%) blur(20px);
            border-bottom: 1px solid rgba(0, 0, 0, 0.08);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 2rem;
            margin-bottom: 2rem;
            border-radius: 0 0 20px 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }
        
        .nav-logo {
            display: flex;
            align-items: center;
            gap: 12px; /* Slightly reduced gap */
        }
        
        .nav-logo-img {
            width: 40px; /* Slightly smaller logo */
            height: 40px;
            border-radius: 10px; /* Slightly smaller radius */
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            object-fit: cover;
        }
        
        .nav-brand {
            font-size: 26px; /* Slightly smaller font */
            font-weight: 800;
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.02em;
        }
        
        /* === 語言選擇器在導航欄中 === */
        .language-selector-nav {
            display: flex;
            gap: 8px; /* Compact buttons */
        }
        
        .language-selector-nav .lang-btn {
            background: #e2e8f0; /* Lighter background for inactive */
            border: 1px solid #cbd5e1; /* Subtle border */
            border-radius: 8px; /* Slightly smaller radius */
            padding: 0.5rem 1rem; /* Smaller padding */
            font-size: 0.85rem; /* Smaller font */
            font-weight: 500;
            color: #475569;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }
        
        .language-selector-nav .lang-btn:hover {
            border-color: #3b82f6;
            color: #3b82f6;
            background: #eff6ff; /* Light blue on hover */
            transform: translateY(-1px);
        }
        
        .language-selector-nav .lang-btn.active {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            border-color: #1d4ed8;
            color: white;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
        }
        
        /* === Hero區域設計 === */
        .hero-section {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            padding: 4.5rem 2.5rem; /* Increased padding */
            border-radius: 28px; /* More rounded */
            margin-top: 2rem; /* Gap after nav */
            margin-bottom: 3.5rem; /* Larger gap below */
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 45px rgba(0, 0, 0, 0.25); /* Stronger shadow */
        }
        
        .hero-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 15% 85%, rgba(59, 130, 246, 0.35) 0%, transparent 40%),
                        radial-gradient(circle at 85% 15%, rgba(255, 255, 255, 0.08) 0%, transparent 40%);
            opacity: 0.8;
        }
        
        .hero-content {
            text-align: center;
            position: relative;
            z-index: 1;
            max-width: 850px; /* Wider content */
            margin: 0 auto;
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
            width: 110px; /* Larger logo */
            height: 110px;
            border-radius: 22px;
            filter: drop-shadow(0 10px 40px rgba(0, 0, 0, 0.6)); /* Stronger shadow */
            animation: heroFloat 6s ease-in-out infinite;
            object-fit: cover;
        }
        
        @keyframes heroFloat {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-12px) rotate(1deg); } /* Slightly more movement */
        }
        
        .hero-title {
            font-size: clamp(3.5rem, 8.5vw, 5.5rem); /* Larger and more responsive */
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
            font-size: clamp(1.2rem, 2.8vw, 1.6rem); /* Larger subtitle */
            font-weight: 400;
            color: #cbd5e1;
            margin-bottom: 2.5rem; /* Larger margin */
            letter-spacing: -0.01em;
        }
        
        .hero-cta {
            display: flex;
            justify-content: center;
            gap: 1.2rem; /* Slightly larger gap */
            flex-wrap: wrap;
        }
        
        .cta-primary, .cta-secondary {
            padding: 1.1rem 2.2rem; /* Larger buttons */
            border-radius: 14px; /* More rounded */
            font-weight: 600;
            font-size: 1.05rem; /* Slightly larger font */
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.6rem; /* Larger icon gap */
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
        }
        
        .cta-primary {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            color: white;
            box-shadow: 0 6px 24px rgba(59, 130, 246, 0.35); /* Stronger shadow */
        }
        
        .cta-primary:hover {
            transform: translateY(-3px); /* More pronounced lift */
            box-shadow: 0 10px 40px rgba(59, 130, 246, 0.45);
        }
        
        .cta-secondary {
            background: rgba(255, 255, 255, 0.15); /* Slightly less transparent */
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.25); /* Stronger border */
            backdrop-filter: saturate(180%) blur(20px);
        }
        
        .cta-secondary:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.4);
            transform: translateY(-1px);
        }
        
        /* === 區塊標題 === */
        h3 {
            font-size: 2rem; /* Larger section titles */
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 1.5rem;
            letter-spacing: -0.03em;
            margin-top: 3.5rem; /* Consistent top margin */
        }

        h4 {
            font-size: 1.4rem; /* Sub-section titles */
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 1.5rem;
            letter-spacing: -0.02em;
        }
        
        /* === 功能卡片系統 === */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2.5rem; /* Larger gap */
            margin: 3.5rem 0;
        }
        
        .feature-card {
            background: white;
            border-radius: 24px; /* More rounded */
            padding: 2.8rem; /* Increased padding */
            box-shadow: 0 6px 36px rgba(0, 0, 0, 0.09); /* Stronger shadow */
            border: 1px solid rgba(0, 0, 0, 0.06);
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
            height: 5px; /* Thicker accent line */
            background: linear-gradient(135deg, var(--accent-color) 0%, var(--accent-color-light) 100%);
        }
        
        .feature-card:hover {
            transform: translateY(-10px); /* More pronounced lift */
            box-shadow: 0 16px 56px rgba(0, 0, 0, 0.18); /* Stronger shadow on hover */
        }
        
        .feature-card.analytics { --accent-color: #3b82f6; --accent-color-light: #60a5fa; }
        .feature-card.portfolio { --accent-color: #8b5cf6; --accent-color-light: #a78bfa; }
        .feature-card.pulse { --accent-color: #06b6d4; --accent-color-light: #22d3ee; }
        .feature-card.academy { --accent-color: #10b981; --accent-color-light: #34d399; }
        
        .feature-icon {
            font-size: 3.2rem; /* Larger icon */
            margin-bottom: 1.6rem;
            display: block;
        }
        
        .feature-title {
            font-size: 1.55rem; /* Larger title */
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.85rem;
            letter-spacing: -0.02em;
        }
        
        .feature-description {
            color: #64748b;
            font-size: 1rem; /* Slightly larger description */
            line-height: 1.7;
            font-weight: 400;
        }
        
        /* === 指標卡片系統 === */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* Slightly wider min */
            gap: 1.8rem; /* Larger gap */
            margin: 3.5rem 0;
        }
        
        .metric-card {
            background: white;
            border-radius: 18px; /* More rounded */
            padding: 2.2rem; /* Increased padding */
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
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
            height: 4px; /* Thicker accent line */
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        }
        
        .metric-card:hover {
            transform: translateY(-5px); /* More pronounced lift */
            box-shadow: 0 10px 36px rgba(0, 0, 0, 0.15);
        }
        
        .metric-label {
            color: #64748b;
            font-size: 0.9rem; /* Slightly larger */
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.7px; /* More prominent */
            margin-bottom: 0.6rem;
        }
        
        .metric-value {
            font-size: 2.2rem; /* Larger value */
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 0.6rem;
            letter-spacing: -0.02em;
        }
        
        .metric-change {
            font-size: 0.9rem; /* Slightly larger */
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.3rem; /* Larger gap */
        }
        
        .metric-change.positive { color: #059669; }
        .metric-change.negative { color: #dc2626; }
        
        /* === AI洞察卡片 === */
        .insight-card {
            background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
            color: white;
            border-radius: 28px; /* More rounded */
            padding: 3.5rem; /* Increased padding */
            margin: 3.5rem 0;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 45px rgba(30, 64, 175, 0.35); /* Stronger shadow */
        }
        
        .insight-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2.2rem;
            flex-wrap: wrap;
            gap: 1.2rem;
        }
        
        .insight-title {
            font-size: 1.8rem; /* Larger title */
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        
        .pivot-score {
            background: rgba(255, 255, 255, 0.25); /* Slightly less transparent */
            color: white;
            padding: 0.6rem 1.1rem; /* Increased padding */
            border-radius: 24px; /* More rounded */
            font-size: 0.9rem; /* Slightly larger */
            font-weight: 600;
            backdrop-filter: saturate(180%) blur(20px);
        }
        
        .insight-content {
            font-size: 1.15rem; /* Slightly larger content */
            line-height: 1.75; /* Improved readability */
            opacity: 0.98; /* Less transparent */
            margin-bottom: 2.2rem;
        }
        
        .insight-badges {
            display: flex;
            gap: 1.2rem; /* Larger gap */
            flex-wrap: wrap;
        }
        
        .insight-badge {
            background: rgba(255, 255, 255, 0.2); /* Slightly less transparent */
            color: white;
            padding: 0.6rem 1.1rem; /* Increased padding */
            border-radius: 18px; /* More rounded */
            font-size: 0.9rem; /* Slightly larger */
            font-weight: 500;
            backdrop-filter: saturate(180%) blur(20px);
        }
        
        /* === 股票表格 === */
        .stocks-table {
            background: white;
            border-radius: 20px; /* More rounded */
            padding: 2.5rem; /* Increased padding */
            box-shadow: 0 6px 28px rgba(0, 0, 0, 0.09); /* Stronger shadow */
            margin: 2.
