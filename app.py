import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time
import json

# ====== 頁面配置 ======
st.set_page_config(
    page_title="Sweet Spot - AI投資決策助手",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====== 多語言支援 ======
LANGUAGES = {
    "繁體中文": "zh",
    "English": "en", 
    "日本語": "jp"
}

TEXTS = {
    "zh": {
        "app_name": "Sweet Spot",
        "tagline": "讓每個投資決定都踩中甜蜜點",
        "sweet_spot_analytics": "甜蜜點分析",
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
        "free_trial": "免費試用",
        "market_overview": "市場概況",
        "portfolio_performance": "投資組合表現",
        "ai_recommendations": "AI 投資建議"
    },
    "en": {
        "app_name": "Sweet Spot",
        "tagline": "Hit the Sweet Spot in Every Investment Decision",
        "sweet_spot_analytics": "Sweet Spot Analytics",
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
        "free_trial": "Free Trial",
        "market_overview": "Market Overview",
        "portfolio_performance": "Portfolio Performance",
        "ai_recommendations": "AI Recommendations"
    },
    "jp": {
        "app_name": "Sweet Spot",
        "tagline": "全ての投資決定でスウィートスポットを見つける",
        "sweet_spot_analytics": "スウィートスポット分析",
        "smart_portfolio": "スマートポートフォリオ構築",
        "market_pulse": "マーケットパルス",
        "investment_academy": "投資アカデミー",
        "real_time_market": "リアルタイム市場データ",
        "expert_insight": "専門家の洞察",
        "pricing_plans": "料金プラン",
        "basic_plan": "ベーシック",
        "advanced_plan": "アドバンス",
        "enterprise_plan": "エンタープライズ",
        "subscribe": "今すぐ購読",
        "free_trial": "無料トライアル",
        "market_overview": "市場概況",
        "portfolio_performance": "ポートフォリオパフォーマンス",
        "ai_recommendations": "AI 投資提案"
    }
}

# ====== Session State 初始化 ======
if 'language' not in st.session_state:
    st.session_state.language = 'zh'
if 'user_plan' not in st.session_state:
    st.session_state.user_plan = 'basic'
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = {}

# ====== 快取數據函數 ======
@st.cache_data(ttl=300)
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
            {'symbol': 'COIN', 'name': 'Coinbase', 'price': 156.42, 'change': 2.8, 'volume': '2.1M', 'rating': '強力買入'},
            {'symbol': 'MSTR', 'name': 'MicroStrategy', 'price': 1247.85, 'change': 5.2, 'volume': '145K', 'rating': '買入'},
            {'symbol': 'RIOT', 'name': 'Riot Blockchain', 'price': 8.94, 'change': 1.4, 'volume': '5.8M', 'rating': '買入'},
            {'symbol': 'NVDA', 'name': 'NVIDIA', 'price': 445.67, 'change': -1.2, 'volume': '32.5M', 'rating': '持有'},
            {'symbol': 'TSLA', 'name': 'Tesla', 'price': 234.56, 'change': 3.4, 'volume': '45.2M', 'rating': '強力買入'}
        ]
    }

@st.cache_data(ttl=600)
def generate_ai_insights():
    """生成AI投資洞察"""
    insights = [
        {
            'title': '區塊鏈概念股爆發',
            'content': '比特幣ETF持續淨流入，帶動COIN、MSTR等概念股走強，預期Q4有15-20%上漲空間。',
            'confidence': 85,
            'risk_level': '中等',
            'time_horizon': '3-6個月',
            'tags': ['區塊鏈', 'ETF', '數位資產']
        },
        {
            'title': 'AI晶片供應鏈機會',
            'content': 'NVIDIA財報超預期，帶動整個AI供應鏈，建議關注台積電、AMD等相關標的。',
            'confidence': 78,
            'risk_level': '中高',
            'time_horizon': '6-12個月',
            'tags': ['AI', '半導體', '供應鏈']
        }
    ]
    return insights

# ====== 專業UI組件 ======
def load_professional_css():
    """載入專業級CSS樣式"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* 全域字體設定 */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* 隱藏Streamlit元素 */
        #MainMenu, footer, header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* 主容器優化 */
        .main .block-container {
            padding: 1rem 2rem;
            max-width: 1600px;
        }
        
        /* 全寬標題區 */
        .hero-section {
            width: 100vw;
            margin-left: calc(-50vw + 50%);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem 0;
            margin-bottom: 2rem;
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
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="white" opacity="0.1"/></svg>') repeat;
            animation: float 20s infinite linear;
        }
        
        @keyframes float {
            0% { transform: translateX(0px); }
            100% { transform: translateX(-100px); }
        }
        
        .hero-content {
            text-align: center;
            color: white;
            position: relative;
            z-index: 1;
        }
        
        .hero-title {
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 0.5rem;
        }
        
        .hero-subtitle {
            font-size: clamp(1.1rem, 2.5vw, 1.5rem);
            font-weight: 400;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
        }
        
        /* 功能卡片 */
        .feature-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 24px rgba(0,0,0,0.06);
            border: 1px solid rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            height: 100%;
        }
        
        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        }
        
        .feature-icon {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            margin-bottom: 1rem;
        }
        
        .feature-icon.analytics { background: linear-gradient(135deg, #667eea, #764ba2); }
        .feature-icon.portfolio { background: linear-gradient(135deg, #f093fb, #f5576c); }
        .feature-icon.pulse { background: linear-gradient(135deg, #4facfe, #00f2fe); }
        .feature-icon.academy { background: linear-gradient(135deg, #43e97b, #38f9d7); }
        
        .feature-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #1a202c;
            margin-bottom: 0.5rem;
        }
        
        .feature-description {
            color: #718096;
            font-size: 0.95rem;
            line-height: 1.6;
        }
        
        /* 指標卡片 */
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.05);
            text-align: center;
            border-left: 4px solid #667eea;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #1a202c;
            margin: 0.5rem 0;
        }
        
        .metric-label {
            color: #718096;
            font-size: 0.9rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .metric-change {
            font-size: 0.85rem;
            font-weight: 600;
        }
        
        .metric-change.positive { color: #38a169; }
        .metric-change.negative { color: #e53e3e; }
        
        /* 價格方案卡片 */
        .pricing-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 2px solid transparent;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .pricing-card.featured {
            border-color: #667eea;
            transform: scale(1.05);
        }
        
        .pricing-card.featured::before {
            content: '推薦';
            position: absolute;
            top: 0;
            right: 0;
            background: #667eea;
            color: white;
            padding: 0.5rem 1rem;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .pricing-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1a202c;
            margin-bottom: 0.5rem;
        }
        
        .pricing-price {
            font-size: 3rem;
            font-weight: 800;
            color: #667eea;
            margin-bottom: 0.5rem;
        }
        
        .pricing-period {
            color: #718096;
            font-size: 1rem;
        }
        
        .pricing-features {
            list-style: none;
            padding: 0;
            margin: 2rem 0;
        }
        
        .pricing-features li {
            padding: 0.5rem 0;
            color: #4a5568;
            display: flex;
            align-items: center;
        }
        
        .pricing-features li::before {
            content: '✓';
            color: #38a169;
            font-weight: bold;
            margin-right: 0.5rem;
        }
        
        /* 按鈕樣式 */
        .cta-button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            margin-top: 1rem;
        }
        
        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        .cta-button.secondary {
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }
        
        /* AI洞察卡片 */
        .insight-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 16px;
            padding: 2rem;
            margin: 2rem 0;
            position: relative;
            overflow: hidden;
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
        
        .insight-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        
        .insight-content {
            font-size: 1.1rem;
            line-height: 1.6;
            opacity: 0.95;
        }
        
        .confidence-badge {
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 1rem;
            display: inline-block;
        }
        
        /* 響應式設計 */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem;
            }
            
            .pricing-card.featured {
                transform: none;
            }
        }
        
        /* 動畫效果 */
        .fade-in {
            animation: fadeIn 0.6s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* 載入動畫 */
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
    """, unsafe_allow_html=True)

def create_feature_card(icon, title, description, icon_class):
    """創建功能特色卡片"""
    return f"""
    <div class="feature-card fade-in">
        <div class="feature-icon {icon_class}">{icon}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-description">{description}</div>
    </div>
    """

def create_metric_card(label, value, change, change_pct):
    """創建指標卡片"""
    change_class = "positive" if change >= 0 else "negative"
    change_symbol = "+" if change >= 0 else ""
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-change {change_class}">
            {change_symbol}{change:.2f} ({change_symbol}{change_pct:.2%})
        </div>
    </div>
    """

def create_pricing_card(title, price, period, features, is_featured=False, currency="USD"):
    """創建價格方案卡片"""
    featured_class = "featured" if is_featured else ""
    return f"""
    <div class="pricing-card {featured_class}">
        <div class="pricing-title">{title}</div>
        <div class="pricing-price">${price}</div>
        <div class="pricing-period">/{period}</div>
        <ul class="pricing-features">
            {''.join([f'<li>{feature}</li>' for feature in features])}
        </ul>
        <button class="cta-button" onclick="handleSubscription('{title}', {price})">
            {TEXTS[st.session_state.language]['subscribe']}
        </button>
    </div>
    """

def create_ai_insight_card(insight):
    """創建AI洞察卡片"""
    return f"""
    <div class="insight-card fade-in">
        <div class="insight-title">🎯 {insight['title']}</div>
        <div class="insight-content">{insight['content']}</div>
        <div class="confidence-badge">信心度: {insight['confidence']}%</div>
        <div class="confidence-badge">風險: {insight['risk_level']}</div>
        <div class="confidence-badge">時間: {insight['time_horizon']}</div>
    </div>
    """

# ====== 主應用程式 ======
def main():
    load_professional_css()
    
    # 語言選擇
    lang = st.session_state.language
    t = TEXTS[lang]
    
    # Hero區域
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-content">
            <div class="hero-title">{t['app_name']}</div>
            <div class="hero-subtitle">{t['tagline']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 核心功能展示
    st.markdown("### 🚀 核心功能")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_feature_card(
            "🎯", 
            t['sweet_spot_analytics'],
            "即時市場數據 + 專家判斷演算法，個股/ETF/債券進出場時機預警，風險收益比最優化計算",
            "analytics"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_feature_card(
            "🏗️", 
            t['smart_portfolio'],
            "根據風險承受度客製化投資組合，美股、債券、期指、海外基金配置，自動再平衡提醒",
            "portfolio"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_feature_card(
            "📡", 
            t['market_pulse'],
            "Push通知重要市場變化，專家解讀重大經濟事件，投資機會即時推播",
            "pulse"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_feature_card(
            "🎓", 
            t['investment_academy'],
            "互動式投資教育內容，成功案例分析，錯誤避免指南",
            "academy"
        ), unsafe_allow_html=True)
    
    # 即時市場數據
    st.markdown("### 📊 " + t['real_time_market'])
    
    market_data = get_market_data()
    
    # 主要指數
    col1, col2, col3, col4 = st.columns(4)
    
    indices = market_data['indices']
    with col1:
        sp_data = indices['SP500']
        st.markdown(create_metric_card("S&P 500", f"{sp_data['value']:,.2f}", sp_data['change'], sp_data['change_pct']), unsafe_allow_html=True)
    
    with col2:
        nasdaq_data = indices['NASDAQ']
        st.markdown(create_metric_card("NASDAQ", f"{nasdaq_data['value']:,.2f}", nasdaq_data['change'], nasdaq_data['change_pct']), unsafe_allow_html=True)
    
    with col3:
        dji_data = indices['DJI']
        st.markdown(create_metric_card("道瓊指數", f"{dji_data['value']:,.2f}", dji_data['change'], dji_data['change_pct']), unsafe_allow_html=True)
    
    with col4:
        btc_data = indices['BTC']
        st.markdown(create_metric_card("Bitcoin", f"${btc_data['value']:,}", btc_data['change'], btc_data['change_pct']), unsafe_allow_html=True)
    
    # TradingView整合
    with st.container():
        st.markdown("#### 📈 即時圖表")
        with st.spinner("載入市場數據中..."):
            st.components.v1.html(
                """
                <div class="tradingview-widget-container">
                  <div class="tradingview-widget-container__widget"></div>
                  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-market-overview.js" async>
                  {
                    "colorTheme": "light",
                    "dateRange": "1D",
                    "showChart": true,
                    "locale": "zh_TW",
                    "width": "100%",
                    "height": "400",
                    "isTransparent": false,
                    "showSymbolLogo": true,
                    "tabs": [
                      {
                        "title": "主要指數",
                        "symbols": [
                          {"s": "FOREXCOM:SPXUSD", "d": "S&P 500"},
                          {"s": "FOREXCOM:NSXUSD", "d": "NASDAQ"},
                          {"s": "FOREXCOM:DJI", "d": "道瓊指數"},
                          {"s": "TVC:VIX", "d": "恐慌指數"}
                        ]
                      },
                      {
                        "title": "熱門個股",
                        "symbols": [
                          {"s": "NASDAQ:AAPL"},
                          {"s": "NASDAQ:MSFT"},
                          {"s": "NASDAQ:GOOGL"},
                          {"s": "NASDAQ:AMZN"},
                          {"s": "NASDAQ:NVDA"},
                          {"s": "NASDAQ:TSLA"}
                        ]
                      },
                      {
                        "title": "區塊鏈概念",
                        "symbols": [
                          {"s": "NASDAQ:COIN"},
                          {"s": "NASDAQ:MSTR"},
                          {"s": "NASDAQ:RIOT"},
                          {"s": "NASDAQ:MARA"}
                        ]
                      }
                    ]
                  }
                  </script>
                </div>
                """,
                height=450
            )
    
    # AI專家洞察
    st.markdown("### 🧠 " + t['ai_recommendations'])
    
    insights = generate_ai_insights()
    for insight in insights:
        st.markdown(create_ai_insight_card(insight), unsafe_allow_html=True)
    
    # 熱門股票追蹤
    st.markdown("### 🔥 熱門追蹤標的")
    
    hot_stocks_df = pd.DataFrame(market_data['hot_stocks'])
    
    # 美化表格顯示
    for idx, stock in hot_stocks_df.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 1.5, 1, 1, 1.5])
        
        with col1:
            st.markdown(f"**{stock['symbol']}**")
        with col2:
            st.markdown(stock['name'])
        with col3:
            st.markdown(f"${stock['price']:,.2f}")
        with col4:
            change_color = "#16a34a" if stock['change'] > 0 else "#dc2626"
            sign = "+" if stock['change'] > 0 else ""
            st.markdown(f'<span style="color: {change_color}; font-weight: bold;">{sign}{stock["change"]}%</span>', 
                       unsafe_allow_html=True)
        with col5:
            st.markdown(stock['volume'])
        with col6:
            rating_color = "#16a34a" if "強力" in stock['rating'] else "#3b82f6" if "買入" in stock['rating'] else "#f59e0b"
            st.markdown(f'<span style="color: {rating_color}; font-weight: bold;">{stock["rating"]}</span>', 
                       unsafe_allow_html=True)
    
    # 訂閱方案
    st.markdown("### 💎 " + t['pricing_plans'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(create_pricing_card(
            t['basic_plan'],
            22,
            "月",
            [
                "甜蜜點分析基礎版",
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
                "完整甜蜜點分析",
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
    
    # JavaScript for subscription handling
    st.markdown("""
    <script>
    function handleSubscription(plan, price) {
        alert(`正在為您準備 ${plan} 方案的訂閱流程 (月費 $${price}USD)...`);
        // 這裡可以整合 Stripe 支付
    }
    </script>
    """, unsafe_allow_html=True)

# ====== 側邊欄設定 ======
def setup_sidebar():
    with st.sidebar:
        st.markdown("## ⚙️ 設定")
        
        # 語言選擇
        selected_lang = st.selectbox(
            "🌐 語言選擇",
            options=list(LANGUAGES.keys()),
            index=list(LANGUAGES.values()).index(st.session_state.language)
        )
        st.session_state.language = LANGUAGES[selected_lang]
        
        # 主題設定
        theme = st.selectbox("🎨 主題模式", ["淺色主題", "深色主題"])
        
        # 通知設定
        st.markdown("### 🔔 通知設定")
        price_alerts = st.toggle("價格提醒", True)
        news_alerts = st.toggle("新聞推播", True)
        report_alerts = st.toggle("分析報告", False)
        
        # 風險偏好
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
        
        # 版本資訊
        st.markdown("---")
        st.caption("Sweet Spot v2.0")
        st.caption("© 2024 TENKI Investment Advisory")
        st.caption("專為海外投資者設計")

# ====== 執行主程式 ======
if __name__ == "__main__":
    setup_sidebar()
    main()
    
    # 頁腳
    st.markdown("---")
    st.markdown(
        """
        <div style="display: flex; justify-content: center; padding: 2rem 0;">
            <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/IMG_0638.png" 
                 style="width: 160px; opacity: 0.7;">
        </div>
        <div style='text-align: center; color: #718096; padding: 1rem;'>
            <p><strong>投資有風險，入市需謹慎</strong></p>
            <p>本平台提供的資訊僅供參考，不構成投資建議</p>
        </div>
        """,
        unsafe_allow_html=True
    )
