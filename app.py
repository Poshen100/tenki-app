import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
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
@st.cache_data(ttl=300, show_spinner=False)
def fetch_live_price_yfinance(symbol):
    """使用 yfinance 獲取即時股價數據"""
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="2d")
        
        if not history.empty:
            current_price = history['Close'].iloc[-1]
            previous_close = history['Close'].iloc[-2] if len(history) > 1 else current_price
            change = current_price - previous_close
            change_pct = (change / previous_close) if previous_close != 0 else 0
            
            return float(current_price), float(change), float(change_pct)
    except Exception as e:
        print(f"Error fetching {symbol}: {str(e)}")
    
    return None, None, None

@st.cache_data(ttl=300, show_spinner=False)
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
    if t == TEXTS['zh']:
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
    elif t == TEXTS['en']:
        return [
            {
                'title': 'Blockchain Stock Breakthrough Point',
                'content': 'Bitcoin ETF net inflows hit new highs, COIN breaks key resistance at $155, technical analysis shows strong bullish momentum, target price $180-200.',
                'confidence': 87,
                'risk_level': 'Medium',
                'time_horizon': '2-4 weeks',
                'pivot_score': 85
            },
            {
                'title': 'AI Chip Supply Chain Pivot',
                'content': 'After NVIDIA earnings beat, AI ecosystem enters new growth cycle. Watch TSM, AMD performance at $150 key support level.',
                'confidence': 82,
                'risk_level': 'Medium-High',
                'time_horizon': '4-8 weeks',
                'pivot_score': 78
            }
        ]
    else:  # Japanese
        return [
            {
                'title': 'ブロックチェーン株のブレイクポイント',
                'content': 'ビットコインETFの純流入が新高値を記録、COINが重要な抵抗線155ドルを突破、テクニカル分析では強気の勢いを示し、目標価格は180-200ドル。',
                'confidence': 87,
                'risk_level': '中程度',
                'time_horizon': '2-4週間',
                'pivot_score': 85
            },
            {
                'title': 'AIチップサプライチェーンの転換点',
                'content': 'NVIDIA決算超過後、AI生態系は新たな成長サイクルに入る。TSM、AMDの150ドル重要サポートレベルでのパフォーマンスに注目。',
                'confidence': 82,
                'risk_level': '中高',
                'time_horizon': '4-8週間',
                'pivot_score': 78
            }
        ]

# ====== UI設計系統 ======
def load_premium_design_system():
    """載入頂級設計系統 - 純Streamlit組件版本"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        /* 完全重置 Streamlit 預設樣式 */
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        }
        
        /* 隱藏所有 Streamlit 預設元素 */
        #MainMenu, footer, header, .stDeployButton, .stDecoration {
            visibility: hidden !important;
            height: 0 !important;
        }
        
        /* 移除頂部空間 */
        .stApp {
            margin-top: -100px !important;
            padding-top: 0 !important;
        }
        
        .stApp > header {
            height: 0 !important;
            visibility: hidden !important;
        }
        
        /* 全域字體設定 */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
        }
        
        /* 主要內容容器 */
        .main-content {
            padding: 1rem;
            margin: 0;
            width: 100%;
        }
        
        /* 頂部品牌區域 */
        .top-banner {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 1rem;
            background: white;
            border-radius: 20px;
            margin: 0 0 1.5rem 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
            width: 100%;
        }
        
        .hero-section {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #334155 100%);
            padding: 3rem 1.5rem;
            border-radius: 20px;
            margin: 0 0 2rem 0;
            text-align: center;
            color: white;
            box-shadow: 0 16px 48px rgba(0, 0, 0, 0.2);
        }
        
        .hero-title {
            font-size: clamp(2.5rem, 8vw, 3.5rem);
            font-weight: 900;
            letter-spacing: -0.05em;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .hero-subtitle {
            font-size: clamp(1rem, 4vw, 1.3rem);
            color: #cbd5e1;
            margin-bottom: 1.5rem;
        }
        
        .section-header {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 16px;
            margin: 1.5rem 0 1rem 0;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        }
        
        .section-header h2 {
            font-size: clamp(1.5rem, 5vw, 2rem);
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        
        .section-header p {
            font-size: clamp(0.9rem, 3vw, 1rem);
            opacity: 0.9;
            margin: 0;
        }
        
        /* Streamlit 指標卡片樣式 */
        div[data-testid="metric-container"] {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        
        div[data-testid="metric-container"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        }
        
        div[data-testid="metric-container"] > div {
            color: #1e293b !important;
        }
        
        /* 股票卡片樣式優化 */
        .stock-info-card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border-left: 4px solid #3b82f6;
        }
        
        .insight-info-card {
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            border: 1px solid #bae6fd;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        }
        
        /* 手機端優化 */
        @media (max-width: 768px) {
            .main-content {
                padding: 0.5rem;
            }
            
            .hero-section {
                padding: 2rem 1rem;
            }
            
            .section-header {
                padding: 1rem;
            }
        }
        
        @media (max-width: 480px) {
            .main-content {
                padding: 0.3rem;
            }
            
            .top-banner {
                padding: 0.8rem;
                margin: 0 0 1rem 0;
            }
            
            .hero-section {
                padding: 1.5rem 0.8rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def create_top_banner():
    """創建頂部橫幅 - 完全無空白設計"""
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<div class="top-banner">', unsafe_allow_html=True)
    
    # 嘗試載入圖片的多種方式
    try:
        # 方法1: 本地圖片檔案
        st.image("IMG_0638.png", use_container_width=True)
    except:
        try:
            # 方法2: 使用附件中的圖片
            st.image("image.jpeg", use_container_width=True)
        except:
            # 方法3: 使用內嵌的TENKI Logo HTML
            st.markdown("""
            <div style="text-align: center;">
                <div style="display: inline-flex; align-items: center; gap: 1rem;">
                    <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); 
                                border-radius: 50%; display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);">
                        <span style="color: white; font-size: 1.5rem; font-weight: bold;">T</span>
                    </div>
                    <div>
                        <div style="font-size: 2.5rem; font-weight: 900; color: #1e293b; margin-bottom: 0.2rem;">TENKI</div>
                        <div style="font-size: 1.1rem; color: #64748b;">Turning Insight into Opportunity</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_hero_section(t):
    """創建Hero區域"""
    st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">{t['app_name']}</h1>
        <p class="hero-subtitle">{t['tagline']}</p>
    </div>
    """, unsafe_allow_html=True)

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

def create_market_data_section(market_data, t):
    """創建市場數據區域 - 使用Streamlit原生組件避免HTML問題"""
    st.markdown(f"""
    <div class="section-header">
        <h2>📊 {t['real_time_market']}</h2>
        <p>全球主要指數即時追蹤</p>
    </div>
    """, unsafe_allow_html=True)
    
    indices = market_data['indices']
    
    # 使用Streamlit原生的columns和metric組件
    col1, col2, col3, col4 = st.columns(4)
    
    # S&P 500
    with col1:
        data = indices['SP500']
        if data['value'] is not None:
            st.metric(
                label="S&P 500",
                value=f"{data['value']:,.2f}",
                delta=f"{data['change']:.2f} ({data['change_pct']:.2%})"
            )
        else:
            st.metric(
                label="S&P 500",
                value="載入中...",
                delta="請稍候"
            )
    
    # NASDAQ
    with col2:
        data = indices['NASDAQ']
        if data['value'] is not None:
            st.metric(
                label="NASDAQ",
                value=f"{data['value']:,.2f}",
                delta=f"{data['change']:.2f} ({data['change_pct']:.2%})"
            )
        else:
            st.metric(
                label="NASDAQ",
                value="載入中...",
                delta="請稍候"
            )
    
    # 道瓊指數
    with col3:
        data = indices['DJI']
        if data['value'] is not None:
            st.metric(
                label="道瓊指數",
                value=f"{data['value']:,.2f}",
                delta=f"{data['change']:.2f} ({data['change_pct']:.2%})"
            )
        else:
            st.metric(
                label="道瓊指數",
                value="載入中...",
                delta="請稍候"
            )
    
    # Bitcoin
    with col4:
        data = indices['BTC']
        if data['value'] is not None:
            st.metric(
                label="Bitcoin",
                value=f"${data['value']:,.2f}",
                delta=f"{data['change']:.2f} ({data['change_pct']:.2%})"
            )
        else:
            st.metric(
                label="Bitcoin",
                value="載入中...",
                delta="請稍候"
            )

def create_hot_stocks_section(hot_stocks, t):
    """創建熱門股票區域 - 使用Streamlit原生組件"""
    st.markdown(f"""
    <div class="section-header">
        <h2>🔥 {t['hot_stocks']}</h2>
        <p>基於關鍵點分析的熱門投資標的</p>
    </div>
    """, unsafe_allow_html=True)
    
    for stock in hot_stocks:
        with st.container():
            st.markdown('<div class="stock-info-card">', unsafe_allow_html=True)
            
            # 股票標題行
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"### {stock['symbol']}")
                st.markdown(f"**{stock['name']}**")
            with col2:
                st.markdown(f"## ${stock['price']:.2f}")
            
            # 股票指標行
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(label=t['volume'], value=stock['volume'])
            with col2:
                change_symbol = "+" if stock['change'] >= 0 else ""
                st.metric(label="變動", value=f"{change_symbol}{stock['change']:.1f}%")
            with col3:
                st.metric(label=t['rating'], value=stock['rating'])
            with col4:
                st.metric(label=t['pivot_score'], value=stock['pivot_score'])
            
            st.markdown('</div>', unsafe_allow_html=True)

def create_pivot_insights_section(insights, t):
    """創建關鍵點洞察區域 - 使用Streamlit原生組件"""
    st.markdown(f"""
    <div class="section-header">
        <h2>🎯 {t['pivot_point_analytics']}</h2>
        <p>AI驅動的市場關鍵轉折點分析</p>
    </div>
    """, unsafe_allow_html=True)
    
    for insight in insights:
        with st.container():
            st.markdown('<div class="insight-info-card">', unsafe_allow_html=True)
            
            st.markdown(f"### {insight['title']}")
            st.markdown(insight['content'])
            
            # 分析指標
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(label="信心度", value=f"{insight['confidence']}%")
            with col2:
                st.metric(label="風險等級", value=insight['risk_level'])
            with col3:
                st.metric(label="時間範圍", value=insight['time_horizon'])
            with col4:
                st.metric(label=t['pivot_score'], value=insight['pivot_score'])
            
            st.markdown('</div>', unsafe_allow_html=True)

def create_roadmap_section(t):
    """創建發展路線圖區域 - 使用Streamlit原生組件"""
    st.markdown(f"""
    <div class="section-header">
        <h2>🗺️ {t['roadmap']}</h2>
        <p>TENKI 平台未來發展計劃</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 第一階段：功能擴展
    st.markdown("### 🔧 1. 功能擴展")
    st.markdown("---")
    
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.markdown("🔵")
    with col2:
        st.markdown("**添加更多股票追蹤**")
        
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.markdown("🔵")
    with col2:
        st.markdown("**增加投資組合功能**")
        
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.markdown("🔵")
    with col2:
        st.markdown("**實現用戶登入系統**")
    
    st.markdown("")
    
    # 第二階段：數據豐富化
    st.markdown("### 📈 2. 數據豐富化")
    st.markdown("---")
    
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.markdown("🟢")
    with col2:
        st.markdown("**整合更多金融API**")
        
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.markdown("🟢")
    with col2:
        st.markdown("**添加新聞資訊**")
        
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.markdown("🟢")
    with col2:
        st.markdown("**增加技術指標**")
    
    st.markdown("")
    
    # 第三階段：商業化準備
    st.markdown("### 💰 3. 商業化準備")
    st.markdown("---")
    
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.markdown("🟡")
    with col2:
        st.markdown("**訂閱付費功能**")

# ====== 主應用程式 ======
def main():
    # 載入完全優化的設計系統
    load_premium_design_system()
    
    # 獲取當前語言設定
    lang = st.session_state.language
    t = TEXTS[lang]
    
    # 頂部品牌橫幅 - 完全無空白
    create_top_banner()
    
    # 語言選擇器
    language_selector(t)
    
    # Hero 區域
    create_hero_section(t)
    
    # 即時市場數據 - 使用修復版本
    with st.spinner("載入市場數據中..."):
        market_data = get_market_data()
    
    create_market_data_section(market_data, t)
    
    # 熱門股票區域
    create_hot_stocks_section(market_data['hot_stocks'], t)
    
    # 關鍵點分析洞察
    insights = generate_pivot_insights(t)
    create_pivot_insights_section(insights, t)
    
    # 發展路線圖
    create_roadmap_section(t)
    
    # 底部資訊
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 1rem; color: #64748b; margin-top: 2rem;">
        <p style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">
            <strong>TENKI</strong> - {t['tagline']}
        </p>
        <p style="margin-bottom: 1rem;">© 2025 TENKI Financial Intelligence Platform</p>
        <p style="font-size: 0.8rem; opacity: 0.8;">
            本平台僅供投資參考，投資有風險，請謹慎評估
        </p>
    </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
