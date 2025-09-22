import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import time
import base64
from concurrent.futures import ThreadPoolExecutor

# ====== 頁面配置 ======
st.set_page_config(
    page_title="TENKI - 転機 | Professional Investment Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====== 多語言支援系統 ======
TEXTS = {
    "zh": {
        "app_name": "TENKI",
        "app_subtitle": "転機",
        "slogan": "Turning Insight into Opportunity",
        "tagline": "將洞察力轉化為機會",
        "login": "登入",
        "register": "註冊", 
        "get_started": "立即開始",
        "email": "電子郵件",
        "password": "密碼",
        "google_login": "使用 Google 登入",
        "apple_login": "使用 Apple 登入",
        "dashboard": "儀表板",
        "virtual_portfolio": "美股虛擬倉",
        "my_subscription": "我的訂閱",
        "settings": "設定",
        "auto_navigation": "自動導航模式",
        "solution_generator": "一鍵生成解決方案",
        "market_overview": "市場概況",
        "expert_insights": "專家洞察",
        "recommended_targets": "建議標的",
        "action_plan": "行動計劃",
        "add_to_watchlist": "加入追蹤",
        "logout": "登出",
        "welcome": "歡迎回來",
        "today_pnl": "今日損益",
        "total_return": "總報酬",
        "win_rate": "勝率",
        "loading": "載入中...",
        "generate_solution": "生成解決方案",
        "risk_preference": "風險偏好",
        "investment_goal": "投資目標",
        "conservative": "保守型",
        "moderate": "穩健型", 
        "aggressive": "積極型",
        "growth": "成長導向",
        "income": "收益導向",
        "balanced": "平衡配置",
        "disclaimer": "免責聲明：本平台提供的資訊僅供參考，不構成任何投資建議。投資有風險，請謹慎決策。",
        "features_title": "核心功能",
        "ai_insights": "AI智能分析",
        "ai_insights_desc": "運用人工智慧分析市場趨勢，提供個性化投資建議",
        "portfolio_management": "投資組合管理",
        "portfolio_management_desc": "專業的虛擬交易系統，零風險驗證投資策略",
        "real_time_data": "即時市場數據",
        "real_time_data_desc": "同步全球金融市場，掌握投資先機",
        "risk_control": "智能風險控制",
        "risk_control_desc": "多層次風險評估，保護您的投資安全",
        "entry_point": "進場點位",
        "exit_point": "出場點位",
        "expected_return": "預期報酬",
        "monthly_plan": "$22 美元/月",
        "next_billing": "下次計費",
        "payment_method": "付款方式"
    },
    "en": {
        "app_name": "TENKI",
        "app_subtitle": "転機",
        "slogan": "Turning Insight into Opportunity",
        "tagline": "Transform Market Intelligence into Investment Success",
        "login": "Login",
        "register": "Register",
        "get_started": "Get Started",
        "email": "Email",
        "password": "Password",
        "google_login": "Login with Google",
        "apple_login": "Login with Apple",
        "dashboard": "Dashboard",
        "virtual_portfolio": "Virtual US Portfolio",
        "my_subscription": "My Subscription",
        "settings": "Settings",
        "auto_navigation": "Auto-Navigation Mode",
        "solution_generator": "Solution Generator",
        "market_overview": "Market Overview",
        "expert_insights": "Expert Insights",
        "recommended_targets": "Recommended Targets",
        "action_plan": "Action Plan",
        "add_to_watchlist": "Add to Watchlist",
        "logout": "Logout",
        "welcome": "Welcome Back",
        "today_pnl": "Today's P&L",
        "total_return": "Total Return",
        "win_rate": "Win Rate",
        "loading": "Loading...",
        "generate_solution": "Generate Solution",
        "risk_preference": "Risk Preference",
        "investment_goal": "Investment Goal",
        "conservative": "Conservative",
        "moderate": "Moderate",
        "aggressive": "Aggressive",
        "growth": "Growth-Oriented",
        "income": "Income-Oriented",
        "balanced": "Balanced",
        "disclaimer": "Disclaimer: Information provided is for reference only, not investment advice.",
        "features_title": "Core Features",
        "ai_insights": "AI-Powered Insights",
        "ai_insights_desc": "Leverage artificial intelligence to analyze market trends",
        "portfolio_management": "Portfolio Management",
        "portfolio_management_desc": "Professional virtual trading system",
        "real_time_data": "Real-time Market Data",
        "real_time_data_desc": "Synchronized global financial markets data",
        "risk_control": "Intelligent Risk Control", 
        "risk_control_desc": "Multi-layered risk assessment",
        "entry_point": "Entry Point",
        "exit_point": "Exit Point",
        "expected_return": "Expected Return",
        "monthly_plan": "$22 USD/month",
        "next_billing": "Next Billing",
        "payment_method": "Payment Method"
    }
}

# ====== Session State 初始化 ======
def init_session_state():
    if 'language' not in st.session_state:
        st.session_state.language = 'zh'
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'landing'
    if 'user_logged_in' not in st.session_state:
        st.session_state.user_logged_in = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = ''
    if 'risk_preference' not in st.session_state:
        st.session_state.risk_preference = 'moderate'
    if 'investment_goal' not in st.session_state:
        st.session_state.investment_goal = 'balanced'
    if 'virtual_portfolio' not in st.session_state:
        st.session_state.virtual_portfolio = []
    if 'generated_solutions' not in st.session_state:
        st.session_state.generated_solutions = []

# ====== Logo系統 ======
def get_logo_html():
    """獲取Logo HTML"""
    logo_files = ["IMG_0640.jpeg", "IMG_0639.jpeg", "IMG_0638.png"]
    
    for logo_file in logo_files:
        try:
            with open(logo_file, "rb") as f:
                image_data = f.read()
                image_b64 = base64.b64encode(image_data).decode()
                image_type = "png" if logo_file.endswith('.png') else "jpeg"
                return f'<img src="data:image/{image_type};base64,{image_b64}" alt="TENKI Logo" style="width: 60px; height: 60px; border-radius: 50%;" />'
        except:
            continue
    
    return '<div style="width: 60px; height: 60px; background: linear-gradient(135deg, #3b82f6, #8b5cf6); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.5rem; color: white;">T</div>'

# ====== 設計系統 ======
def load_css():
    """載入CSS樣式"""
    st.markdown("""
    <style>
        /* 基礎設定 */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');
        
        .main .block-container {
            padding: 1rem !important;
            max-width: 1200px !important;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
            font-family: 'Inter', sans-serif !important;
            color: #ffffff !important;
        }
        
        #MainMenu, footer, header, .stDeployButton, .stDecoration {
            display: none !important;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
        }
        
        /* Hero Section */
        .hero-section {
            text-align: center;
            padding: 4rem 2rem;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(168, 85, 247, 0.1));
            border-radius: 24px;
            margin-bottom: 3rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .hero-logo {
            margin: 0 auto 2rem;
            display: flex;
            justify-content: center;
        }
        
        .hero-title {
            font-family: 'Outfit', sans-serif;
            font-size: 4rem;
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #ffffff, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .hero-subtitle {
            font-size: 1.5rem;
            color: #94a3b8;
            margin-bottom: 1rem;
        }
        
        .hero-tagline {
            font-size: 1.25rem;
            color: #cbd5e1;
            margin-bottom: 2rem;
            font-style: italic;
        }
        
        .hero-description {
            font-size: 1rem;
            color: #94a3b8;
            line-height: 1.6;
            margin-bottom: 3rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* 現代卡片 */
        .modern-card {
            background: linear-gradient(135deg, #1e293b, #334155);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4);
            transition: all 0.3s ease;
        }
        
        .modern-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 25px 50px -12px rgba(59, 130, 246, 0.25);
        }
        
        .card-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 1rem;
        }
        
        /* 指標卡片 */
        .metric-card {
            background: linear-gradient(135deg, #1e293b, #334155);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .metric-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0.5rem;
        }
        
        .metric-label {
            color: #94a3b8;
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        .positive { color: #10b981; }
        .negative { color: #ef4444; }
        
        /* 導航 */
        .nav-container {
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 1rem;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        /* 按鈕優化 */
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
            border: none !important;
            border-radius: 12px !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 0.75rem 1.5rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3) !important;
        }
        
        /* 表單優化 */
        .stTextInput > div > div > input {
            background: rgba(30, 41, 59, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
        }
        
        .stSelectbox > div > div {
            background: rgba(30, 41, 59, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
        }
        
        /* 免責聲明 */
        .disclaimer {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            color: #fca5a5;
            font-size: 0.9rem;
            margin: 2rem 0;
            text-align: center;
        }
        
        /* 響應式 */
        @media (max-width: 768px) {
            .hero-title { font-size: 2.5rem; }
            .hero-section { padding: 2rem 1rem; }
            .modern-card { padding: 1.5rem; }
        }
    </style>
    """, unsafe_allow_html=True)

# ====== 市場數據 ======
@st.cache_data(ttl=300)
def get_market_data():
    """獲取市場數據"""
    symbols = ['SPY', 'QQQ', 'AAPL', 'MSFT', 'GOOGL', 'NVDA']
    market_data = {}
    
    def fetch_data(symbol):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")
            if len(hist) >= 2:
                current = float(hist['Close'].iloc[-1])
                previous = float(hist['Close'].iloc[-2])
                change = current - previous
                change_pct = (change / previous) * 100
                return {
                    'symbol': symbol,
                    'price': current,
                    'change': change,
                    'change_pct': change_pct
                }
        except:
            pass
        return None
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(fetch_data, symbol) for symbol in symbols]
        for future in futures:
            result = future.result()
            if result:
                market_data[result['symbol']] = result
    
    return market_data

# ====== 投資解決方案 ======
def generate_solution(risk_pref, investment_goal):
    """生成投資解決方案"""
    if risk_pref == 'conservative' and investment_goal == 'income':
        return {
            'theme': '2024年防禦型收益投資策略',
            'insight': '專注於穩定收益資產，包括高股息股票、政府債券和REIT基金，適合保守型投資者。',
            'targets': [
                {
                    'symbol': 'VYM',
                    'type': '高股息ETF',
                    'allocation': 40,
                    'entry_point': '$110以下',
                    'exit_point': '股息率降至2%',
                    'expected_return': '5-7%',
                    'analysis': '追蹤高股息美股，提供穩定現金流'
                },
                {
                    'symbol': 'TLT',
                    'type': '長期公債ETF',
                    'allocation': 35,
                    'entry_point': '當前價位',
                    'exit_point': 'Fed升息時',
                    'expected_return': '4-6%',
                    'analysis': '20年以上美國公債，降息環境受惠'
                },
                {
                    'symbol': 'VNQ',
                    'type': 'REIT ETF',
                    'allocation': 25,
                    'entry_point': '回調時進入',
                    'exit_point': '利率上升時',
                    'expected_return': '6-8%',
                    'analysis': '不動產投資信託，通脹對沖'
                }
            ]
        }
    elif risk_pref == 'moderate' and investment_goal == 'balanced':
        return {
            'theme': '2024年AI科技平衡配置',
            'insight': '結合科技成長股和防禦性資產，在AI浪潮中尋找平衡收益機會。',
            'targets': [
                {
                    'symbol': 'QQQ',
                    'type': '科技ETF',
                    'allocation': 30,
                    'entry_point': '$360以下',
                    'exit_point': '估值過高時',
                    'expected_return': '8-12%',
                    'analysis': '納斯達克100，受惠AI革命'
                },
                {
                    'symbol': 'NVDA',
                    'type': 'AI晶片龍頭',
                    'allocation': 25,
                    'entry_point': '技術回調時',
                    'exit_point': '基本面轉弱',
                    'expected_return': '15-25%',
                    'analysis': 'AI晶片領導者，GPU不可替代'
                },
                {
                    'symbol': 'VTI',
                    'type': '全市場ETF',
                    'allocation': 25,
                    'entry_point': '定期定額',
                    'exit_point': '長期持有',
                    'expected_return': '7-10%',
                    'analysis': '全市場指數，最佳分散'
                },
                {
                    'symbol': 'LQD',
                    'type': '投資級債券',
                    'allocation': 20,
                    'entry_point': '收益率4%+',
                    'exit_point': 'Fed升息時',
                    'expected_return': '4-5%',
                    'analysis': '企業債券，穩定收益'
                }
            ]
        }
    else:  # aggressive + growth
        return {
            'theme': '2024年積極成長投資策略',
            'insight': '專注高成長潛力股票，包括AI、電動車、生技等顛覆性創新領域。',
            'targets': [
                {
                    'symbol': 'ARKK',
                    'type': '創新ETF',
                    'allocation': 30,
                    'entry_point': '大幅回調時',
                    'exit_point': '創新降溫時',
                    'expected_return': '15-30%',
                    'analysis': '專注顛覆性創新投資'
                },
                {
                    'symbol': 'TSLA',
                    'type': '電動車龍頭',
                    'allocation': 25,
                    'entry_point': '$180-200',
                    'exit_point': '自駕停滯時',
                    'expected_return': '20-40%',
                    'analysis': '電動車和自動駕駛領導者'
                },
                {
                    'symbol': 'MSFT',
                    'type': '雲端AI巨頭',
                    'allocation': 25,
                    'entry_point': '$320以下',
                    'exit_point': '雲端成長減緩',
                    'expected_return': '12-18%',
                    'analysis': 'Azure雲端和AI整合最完整'
                },
                {
                    'symbol': 'SOXX',
                    'type': '半導體ETF',
                    'allocation': 20,
                    'entry_point': '週期低點',
                    'exit_point': '週期高點',
                    'expected_return': '18-25%',
                    'analysis': '半導體產業，AI基礎建設'
                }
            ]
        }

# ====== 頁面函數 ======
def show_landing_page():
    """Landing Page"""
    t = TEXTS[st.session_state.language]
    logo_html = get_logo_html()
    
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-logo">
            {logo_html}
        </div>
        <h1 class="hero-title">TENKI</h1>
        <p class="hero-subtitle">{t['app_subtitle']}</p>
        <p class="hero-tagline">{t['slogan']}</p>
        <div class="hero-description">
            專業投資決策支援平台 • 在關鍵轉折點做出理想決策 • 實現資產增值
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 語言切換
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        lang_col1, lang_col2 = st.columns(2)
        
        with lang_col1:
            if st.button("🇹🇼 中文", key="lang_zh", use_container_width=True, 
                        type="primary" if st.session_state.language == 'zh' else "secondary"):
                st.session_state.language = 'zh'
                st.rerun()
        
        with lang_col2:
            if st.button("🇺🇸 English", key="lang_en", use_container_width=True,
                        type="primary" if st.session_state.language == 'en' else "secondary"):
                st.session_state.language = 'en'
                st.rerun()
        
        st.markdown("---")
        
        # CTA按鈕
        if st.button(f"🚀 {t['get_started']}", key="get_started", use_container_width=True, type="primary"):
            st.session_state.current_page = 'login'
            st.rerun()
    
    # 核心功能
    st.markdown(f"""
    <div class="modern-card">
        <h2 class="card-title">{t['features_title']}</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-top: 1.5rem;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">🤖</div>
                <h3 style="color: #ffffff; margin-bottom: 0.5rem;">{t['ai_insights']}</h3>
                <p style="color: #94a3b8; font-size: 0.9rem;">{t['ai_insights_desc']}</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">💼</div>
                <h3 style="color: #ffffff; margin-bottom: 0.5rem;">{t['portfolio_management']}</h3>
                <p style="color: #94a3b8; font-size: 0.9rem;">{t['portfolio_management_desc']}</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">📊</div>
                <h3 style="color: #ffffff; margin-bottom: 0.5rem;">{t['real_time_data']}</h3>
                <p style="color: #94a3b8; font-size: 0.9rem;">{t['real_time_data_desc']}</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">🛡️</div>
                <h3 style="color: #ffffff; margin-bottom: 0.5rem;">{t['risk_control']}</h3>
                <p style="color: #94a3b8; font-size: 0.9rem;">{t['risk_control_desc']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 免責聲明
    st.markdown(f"""
    <div class="disclaimer">
        ⚠️ {t['disclaimer']}
    </div>
    """, unsafe_allow_html=True)

def show_login_page():
    """登入頁面"""
    t = TEXTS[st.session_state.language]
    logo_html = get_logo_html()
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="margin-bottom: 1rem;">
                {logo_html}
            </div>
            <h1 style="font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 700; color: #ffffff; margin-bottom: 0.5rem;">TENKI</h1>
            <p style="color: #94a3b8;">{t['tagline']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 登入表單
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input(t['email'], placeholder="your@email.com")
            password = st.text_input(t['password'], type="password", placeholder="••••••••")
            
            col_a, col_b = st.columns(2)
            with col_a:
                login_btn = st.form_submit_button(t['login'], use_container_width=True)
            with col_b:
                register_btn = st.form_submit_button(t['register'], use_container_width=True)
            
            if login_btn or register_btn:
                if email and password:
                    st.session_state.user_logged_in = True
                    st.session_state.user_email = email
                    st.session_state.current_page = 'dashboard'
                    st.success(f"✅ {t['welcome']}, {email}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("請填寫所有欄位")
        
        # 社群登入
        st.markdown("**或使用以下方式登入**")
        col_x, col_y = st.columns(2)
        with col_x:
            if st.button(f"🔍 {t['google_login']}", key="google_login", use_container_width=True):
                st.session_state.user_logged_in = True
                st.session_state.user_email = "user@gmail.com"
                st.session_state.current_page = 'dashboard'
                st.rerun()
        with col_y:
            if st.button(f"🍎 {t['apple_login']}", key="apple_login", use_container_width=True):
                st.session_state.user_logged_in = True
                st.session_state.user_email = "user@icloud.com"
                st.session_state.current_page = 'dashboard'
                st.rerun()
        
        # 返回首頁
        if st.button("← 返回首頁", key="back_home", use_container_width=True):
            st.session_state.current_page = 'landing'
            st.rerun()

def create_navigation():
    """創建導航"""
    t = TEXTS[st.session_state.language]
    logo_html = get_logo_html()
    
    st.markdown(f"""
    <div class="nav-container">
        <div style="display: flex; align-items: center; gap: 1rem;">
            {logo_html}
            <span style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.25rem; color: #ffffff;">TENKI</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 導航按鈕
    nav_items = [
        ('dashboard', '🏠 ' + t['dashboard']),
        ('auto_navigation', '🧭 ' + t['auto_navigation']),
        ('solution_generator', '⚡ ' + t['solution_generator']),
        ('virtual_portfolio', '💼 ' + t['virtual_portfolio']),
        ('subscription', '💳 ' + t['my_subscription']),
        ('settings', '⚙️ ' + t['settings'])
    ]
    
    cols = st.columns(len(nav_items) + 1)
    
    for i, (page_key, page_name) in enumerate(nav_items):
        with cols[i]:
            if st.button(page_name, key=f"nav_{page_key}", use_container_width=True,
                        type="primary" if st.session_state.current_page == page_key else "secondary"):
                st.session_state.current_page = page_key
                st.rerun()
    
    with cols[-1]:
        if st.button(f"🚪 {t['logout']}", key="logout_nav"):
            st.session_state.user_logged_in = False
            st.session_state.current_page = 'landing'
            st.rerun()

def show_dashboard():
    """儀表板"""
    t = TEXTS[st.session_state.language]
    
    st.markdown(f"""
    <div class="modern-card">
        <h1 class="card-title">{t['welcome']}, {st.session_state.user_email.split('@')[0]}! 🎉</h1>
        <p style="color: #94a3b8;">準備好開始您今天的投資之旅了嗎？</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 績效指標
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t['today_pnl']}</div>
            <div class="metric-value positive">+$1,234</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t['total_return']}</div>
            <div class="metric-value positive">+$12,567</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t['win_rate']}</div>
            <div class="metric-value">68.5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">風險指標</div>
            <div class="metric-value positive">低風險</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 市場數據
    st.markdown(f"""
    <div class="modern-card">
        <h2 class="card-title">📊 {t['market_overview']}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner(t['loading']):
        market_data = get_market_data()
    
    if market_data:
        cols = st.columns(len(market_data))
        for i, (symbol, data) in enumerate(market_data.items()):
            with cols[i]:
                st.metric(
                    label=symbol,
                    value=f"${data['price']:.2f}",
                    delta=f"{data['change']:+.2f} ({data['change_pct']:+.2f}%)"
                )
    
    # 快速操作
    st.markdown("""
    <div class="modern-card">
        <h2 class="card-title">⚡ 快速操作</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"🧭 {t['auto_navigation']}", key="quick_nav", use_container_width=True):
            st.session_state.current_page = 'auto_navigation'
            st.rerun()
    
    with col2:
        if st.button(f"⚡ {t['generate_solution']}", key="quick_solution", use_container_width=True):
            st.session_state.current_page = 'solution_generator'
            st.rerun()
    
    with col3:
        if st.button(f"💼 {t['virtual_portfolio']}", key="quick_portfolio", use_container_width=True):
            st.session_state.current_page = 'virtual_portfolio'
            st.rerun()

def show_auto_navigation():
    """自動導航模式"""
    t = TEXTS[st.session_state.language]
    
    st.markdown(f"""
    <div class="modern-card">
        <h1 class="card-title">🧭 {t['auto_navigation']}</h1>
        <p style="color: #94a3b8;">根據您的投資偏好和目標，為您提供個性化的投資建議</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 偏好設定
    col1, col2 = st.columns(2)
    
    with col1:
        risk_pref = st.selectbox(
            t['risk_preference'],
            options=['conservative', 'moderate', 'aggressive'],
            format_func=lambda x: {
                'conservative': t['conservative'], 
                'moderate': t['moderate'], 
                'aggressive': t['aggressive']
            }[x],
            index=['conservative', 'moderate', 'aggressive'].index(st.session_state.risk_preference),
            key="risk_select"
        )
        st.session_state.risk_preference = risk_pref
    
    with col2:
        invest_goal = st.selectbox(
            t['investment_goal'],
            options=['income', 'balanced', 'growth'],
            format_func=lambda x: {
                'income': t['income'], 
                'balanced': t['balanced'], 
                'growth': t['growth']
            }[x],
            index=['income', 'balanced', 'growth'].index(st.session_state.investment_goal),
            key="goal_select"
        )
        st.session_state.investment_goal = invest_goal
    
    # 生成解決方案
    if st.button(f"🎯 {t['generate_solution']}", key="generate_auto", use_container_width=True, type="primary"):
        with st.spinner(t['loading']):
            solution = generate_solution(risk_pref, invest_goal)
            st.session_state.generated_solutions = [solution]
            time.sleep(1)
        
        st.success("✅ 已生成個性化投資解決方案！")
        st.session_state.current_page = 'solution_generator'
        st.rerun()
    
    # 當前設定
    st.markdown(f"""
    <div class="modern-card">
        <h3 class="card-title">⚙️ 當前設定</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 1rem;">
            <div style="text-align: center;">
                <div style="color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.5rem;">{t['risk_preference']}</div>
                <div style="color: #ffffff; font-weight: 600; font-size: 1.125rem;">
                    {t['conservative'] if risk_pref == 'conservative' else t['moderate'] if risk_pref == 'moderate' else t['aggressive']}
                </div>
            </div>
            <div style="text-align: center;">
                <div style="color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.5rem;">{t['investment_goal']}</div>
                <div style="color: #ffffff; font-weight: 600; font-size: 1.125rem;">
                    {t['income'] if invest_goal == 'income' else t['balanced'] if invest_goal == 'balanced' else t['growth']}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_solution_generator():
    """解決方案生成器"""
    t = TEXTS[st.session_state.language]
    
    st.markdown(f"""
    <div class="modern-card">
        <h1 class="card-title">⚡ {t['solution_generator']}</h1>
        <p style="color: #94a3b8;">基於AI分析和專家洞察，為您生成個性化投資解決方案</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.generated_solutions:
        solution = st.session_state.generated_solutions[0]
        
        st.markdown(f"""
        <div class="modern-card">
            <h2 style="color: #3b82f6; margin-bottom: 1.5rem;">🎯 {solution['theme']}</h2>
            <p style="color: #cbd5e1; line-height: 1.7; margin-bottom: 2rem;">{solution['insight']}</p>
            
            <h3 style="color: #ffffff; margin-bottom: 1.5rem;">📊 {t['recommended_targets']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # 建議標的
        for target in solution['targets']:
            st.markdown(f"""
            <div class="modern-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                    <div>
                        <h4 style="color: #ffffff; font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; margin-bottom: 0.5rem;">{target['symbol']}</h4>
                        <span style="background: rgba(139, 92, 246, 0.2); color: #8b5cf6; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">{target['type']}</span>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #10b981; font-size: 1.5rem; font-weight: 700; font-family: 'JetBrains Mono', monospace;">{target['allocation']}%</div>
                    </div>
                </div>
                <p style="color: #94a3b8; margin-bottom: 1rem;">{target['analysis']}</p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 1rem;">
                    <div style="text-align: center;">
                        <div style="color: #6b7280; font-size: 0.75rem; margin-bottom: 0.25rem;">{t['entry_point']}</div>
                        <div style="color: #ffffff; font-weight: 600;">{target['entry_point']}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #6b7280; font-size: 0.75rem; margin-bottom: 0.25rem;">{t['exit_point']}</div>
                        <div style="color: #ffffff; font-weight: 600;">{target['exit_point']}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #6b7280; font-size: 0.75rem; margin-bottom: 0.25rem;">{t['expected_return']}</div>
                        <div style="color: #ffffff; font-weight: 600;">{target['expected_return']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 操作按鈕
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"📌 {t['add_to_watchlist']}", key="add_watchlist", use_container_width=True):
                st.success("✅ 已加入追蹤清單！")
        
        with col2:
            if st.button("💼 加入虛擬組合", key="add_portfolio", use_container_width=True):
                for target in solution['targets']:
                    portfolio_item = {
                        'symbol': target['symbol'],
                        'quantity': target['allocation'] * 10,
                        'entry_price': np.random.uniform(100, 500),
                        'current_price': np.random.uniform(100, 500),
                        'entry_date': datetime.now()
                    }
                    st.session_state.virtual_portfolio.append(portfolio_item)
                
                st.success("✅ 已加入虛擬投資組合！")
    
    else:
        st.markdown(f"""
        <div class="modern-card">
            <div style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem; margin-bottom: 1.5rem;">🎯</div>
                <h2 style="color: #ffffff; font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;">
                    尚無生成的投資解決方案
                </h2>
                <p style="color: #94a3b8; margin-bottom: 2rem;">
                    請先前往自動導航模式設定您的投資偏好
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🧭 前往自動導航設定", key="goto_nav", use_container_width=True, type="primary"):
            st.session_state.current_page = 'auto_navigation'
            st.rerun()

def show_virtual_portfolio():
    """虛擬投資組合"""
    t = TEXTS[st.session_state.language]
    
    st.markdown(f"""
    <div class="modern-card">
        <h1 class="card-title">💼 {t['virtual_portfolio']}</h1>
        <p style="color: #94a3b8;">無風險的虛擬交易環境，驗證您的投資策略</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.virtual_portfolio:
        # 計算總績效
        total_value = sum(item['quantity'] * item['current_price'] for item in st.session_state.virtual_portfolio)
        total_cost = sum(item['quantity'] * item['entry_price'] for item in st.session_state.virtual_portfolio)
        total_pnl = total_value - total_cost
        total_return_pct = (total_pnl / total_cost * 100) if total_cost > 0 else 0
        
        # 績效指標
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">組合價值</div>
                <div class="metric-value">${total_value:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            pnl_class = "positive" if total_pnl >= 0 else "negative"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{t['total_return']}</div>
                <div class="metric-value {pnl_class}">${total_pnl:+,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            win_count = sum(1 for item in st.session_state.virtual_portfolio if item['current_price'] > item['entry_price'])
            win_rate = (win_count / len(st.session_state.virtual_portfolio)) * 100
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{t['win_rate']}</div>
                <div class="metric-value">{win_rate:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">持倉數量</div>
                <div class="metric-value">{len(st.session_state.virtual_portfolio)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 持倉明細
        st.markdown("### 📊 持倉明細")
        for i, item in enumerate(st.session_state.virtual_portfolio):
            pnl = (item['current_price'] - item['entry_price']) * item['quantity']
            pnl_pct = ((item['current_price'] - item['entry_price']) / item['entry_price'] * 100) if item['entry_price'] > 0 else 0
            pnl_color = "#10b981" if pnl >= 0 else "#ef4444"
            
            st.markdown(f"""
            <div class="modern-card">
                <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 1rem; align-items: center;">
                    <div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 1.1rem; color: #ffffff;">{item['symbol']}</div>
                        <div style="color: #94a3b8; font-size: 0.85rem;">{item['quantity']:.0f} 股</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #ffffff; font-weight: 600;">${item['entry_price']:.2f}</div>
                        <div style="color: #94a3b8; font-size: 0.8rem;">買入價</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #ffffff; font-weight: 600;">${item['current_price']:.2f}</div>
                        <div style="color: #94a3b8; font-size: 0.8rem;">現價</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: {pnl_color};">${pnl:+,.0f}</div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-weight: 600; color: {pnl_color}; font-size: 0.85rem;">{pnl_pct:+.2f}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 操作按鈕
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 更新價格", key="update_prices", use_container_width=True):
                for item in st.session_state.virtual_portfolio:
                    change_pct = np.random.uniform(-0.05, 0.05)
                    item['current_price'] *= (1 + change_pct)
                st.success("✅ 價格已更新！")
                st.rerun()
        
        with col2:
            if st.button("📊 生成報告", key="generate_report", use_container_width=True):
                st.info("📄 績效報告功能開發中...")
        
        with col3:
            if st.button("🗑️ 清空組合", key="clear_portfolio", use_container_width=True):
                st.session_state.virtual_portfolio = []
                st.success("✅ 虛擬組合已清空！")
                st.rerun()
    
    else:
        st.markdown(f"""
        <div class="modern-card">
            <div style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem; margin-bottom: 1.5rem;">💼</div>
                <h2 style="color: #ffffff; font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;">
                    您的虛擬投資組合是空的
                </h2>
                <p style="color: #94a3b8; margin-bottom: 2rem;">
                    透過解決方案生成器建立您的第一個投資組合
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚡ 前往解決方案生成器", key="goto_solution", use_container_width=True, type="primary"):
            st.session_state.current_page = 'solution_generator'
            st.rerun()

def show_subscription():
    """訂閱管理"""
    t = TEXTS[st.session_state.language]
    
    st.markdown(f"""
    <div class="modern-card">
        <h1 class="card-title">💳 {t['my_subscription']}</h1>
        <p style="color: #94a3b8;">管理您的訂閱方案和付款設定</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 訂閱狀態
    st.markdown(f"""
    <div class="modern-card">
        <div style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #10b981, #059669); color: white; border-radius: 50px; font-weight: 600; margin-bottom: 2rem;">
            <div style="width: 8px; height: 8px; border-radius: 50%; background: currentColor;"></div>
            <span>訂閱有效</span>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin: 2rem 0;">
            <div style="text-align: center;">
                <div style="color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.5rem;">當前方案</div>
                <div style="color: #ffffff; font-size: 1.25rem; font-weight: 700;">{t['monthly_plan']}</div>
            </div>
            <div style="text-align: center;">
                <div style="color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.5rem;">{t['next_billing']}</div>
                <div style="color: #ffffff; font-size: 1.1rem; font-weight: 600;">2024年11月22日</div>
            </div>
            <div style="text-align: center;">
                <div style="color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.5rem;">{t['payment_method']}</div>
                <div style="color: #ffffff; font-size: 1.1rem; font-weight: 600;">•••• 1234</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 使用統計
    st.markdown("### 📊 使用統計")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">解決方案生成</div>
            <div class="metric-value">23</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">投資組合追蹤</div>
            <div class="metric-value">156</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">平台使用</div>
            <div class="metric-value">47</div>
        </div>
        """, unsafe_allow_html=True)

def show_settings():
    """設定頁面"""
    t = TEXTS[st.session_state.language]
    
    st.markdown(f"""
    <div class="modern-card">
        <h1 class="card-title">⚙️ {t['settings']}</h1>
        <p style="color: #94a3b8;">個性化您的TENKI體驗設定</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 語言設定
    st.markdown("### 🌐 語言設定")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇹🇼 繁體中文", key="set_zh",
                     use_container_width=True,
                     type="primary" if st.session_state.language == 'zh' else "secondary"):
            st.session_state.language = 'zh'
            st.rerun()
    
    with col2:
        if st.button("🇺🇸 English", key="set_en",
                     use_container_width=True,
                     type="primary" if st.session_state.language == 'en' else "secondary"):
            st.session_state.language = 'en'
            st.rerun()
    
    # 投資偏好
    st.markdown("### 🎯 投資偏好")
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_risk_pref = st.selectbox(
            t['risk_preference'],
            options=['conservative', 'moderate', 'aggressive'],
            format_func=lambda x: {
                'conservative': t['conservative'], 
                'moderate': t['moderate'], 
                'aggressive': t['aggressive']
            }[x],
            index=['conservative', 'moderate', 'aggressive'].index(st.session_state.risk_preference),
            key="settings_risk"
        )
    
    with col2:
        new_invest_goal = st.selectbox(
            t['investment_goal'],
            options=['income', 'balanced', 'growth'],
            format_func=lambda x: {
                'income': t['income'], 
                'balanced': t['balanced'], 
                'growth': t['growth']
            }[x],
            index=['income', 'balanced', 'growth'].index(st.session_state.investment_goal),
            key="settings_goal"
        )
    
    if st.button("💾 儲存設定", key="save_settings", use_container_width=True, type="primary"):
        st.session_state.risk_preference = new_risk_pref
        st.session_state.investment_goal = new_invest_goal
        st.success("✅ 設定已儲存！")

# ====== 主應用程式 ======
def main():
    """TENKI主程式"""
    
    # 初始化
    init_session_state()
    load_css()
    
    # 路由系統
    if st.session_state.current_page == 'landing':
        show_landing_page()
    elif st.session_state.current_page == 'login':
        show_login_page()
    elif st.session_state.user_logged_in:
        # 顯示導航
        create_navigation()
        
        # 根據頁面顯示內容
        if st.session_state.current_page == 'dashboard':
            show_dashboard()
        elif st.session_state.current_page == 'auto_navigation':
            show_auto_navigation()
        elif st.session_state.current_page == 'solution_generator':
            show_solution_generator()
        elif st.session_state.current_page == 'virtual_portfolio':
            show_virtual_portfolio()
        elif st.session_state.current_page == 'subscription':
            show_subscription()
        elif st.session_state.current_page == 'settings':
            show_settings()
        else:
            show_dashboard()
    else:
        st.session_state.current_page = 'landing'
        show_landing_page()
    
    # 免責聲明
    if st.session_state.user_logged_in:
        t = TEXTS[st.session_state.language]
        st.markdown(f"""
        <div class="disclaimer">
            ⚠️ {t['disclaimer']}
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
