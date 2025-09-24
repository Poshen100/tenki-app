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
    page_icon="⚡", # 更換為閃電圖示，更具動感和機會感
    layout="wide",
    initial_sidebar_state="expanded" # 將側邊欄預設展開，方便導航，並在登入後隱藏
)

# ====== 多語言支援系統 (保留不變) ======
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
        "payment_method": "付款方式",
        "portfolio_value": "組合價值",
        "holdings_count": "持倉數量",
        "buy_price": "買入價",
        "current_price": "現價",
        "update_prices": "更新價格",
        "generate_report": "生成報告",
        "clear_portfolio": "清空組合",
        "no_solution_title": "尚無生成的投資解決方案",
        "no_solution_desc": "請先前往自動導航模式設定您的投資偏好",
        "go_to_nav_settings": "前往自動導航設定",
        "no_portfolio_title": "您的虛擬投資組合是空的",
        "no_portfolio_desc": "透過解決方案生成器建立您的第一個投資組合",
        "go_to_solution_generator": "前往解決方案生成器",
        "subscription_active": "訂閱有效",
        "current_plan": "當前方案",
        "billing_date": "計費日期",
        "usage_stats": "使用統計",
        "solutions_generated": "解決方案生成",
        "portfolios_tracked": "投資組合追蹤",
        "platform_usage": "平台使用",
        "language_settings": "語言設定",
        "investment_preferences": "投資偏好",
        "save_settings": "儲存設定",
        "settings_saved": "設定已儲存！",
        "add_to_watchlist_success": "已加入追蹤清單！",
        "add_to_portfolio_success": "已加入虛擬投資組合！",
        "prices_updated": "價格已更新！",
        "report_coming_soon": "績效報告功能開發中...",
        "portfolio_cleared": "虛擬組合已清空！"
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
        "payment_method": "Payment Method",
        "portfolio_value": "Portfolio Value",
        "holdings_count": "Number of Holdings",
        "buy_price": "Buy Price",
        "current_price": "Current Price",
        "update_prices": "Update Prices",
        "generate_report": "Generate Report",
        "clear_portfolio": "Clear Portfolio",
        "no_solution_title": "No Investment Solution Generated Yet",
        "no_solution_desc": "Please go to Auto-Navigation Mode to set your investment preferences first",
        "go_to_nav_settings": "Go to Auto-Navigation Settings",
        "no_portfolio_title": "Your Virtual Portfolio is Empty",
        "no_portfolio_desc": "Create your first investment portfolio via the Solution Generator",
        "go_to_solution_generator": "Go to Solution Generator",
        "subscription_active": "Subscription Active",
        "current_plan": "Current Plan",
        "billing_date": "Billing Date",
        "usage_stats": "Usage Statistics",
        "solutions_generated": "Solutions Generated",
        "portfolios_tracked": "Portfolios Tracked",
        "platform_usage": "Platform Usage",
        "language_settings": "Language Settings",
        "investment_preferences": "Investment Preferences",
        "save_settings": "Save Settings",
        "settings_saved": "Settings Saved!",
        "add_to_watchlist_success": "Added to Watchlist!",
        "add_to_portfolio_success": "Added to Virtual Portfolio!",
        "prices_updated": "Prices updated!",
        "report_coming_soon": "Performance report feature under development...",
        "portfolio_cleared": "Virtual portfolio cleared!"
    }
}

# ====== Session State 初始化 (保留不變) ======
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

# ====== Logo 系統 (優化樣式) ======
def get_logo_html():
    """獲取 Logo HTML，優化圖片顯示樣式"""
    logo_files = ["IMG_0640.jpeg", "IMG_0639.jpeg", "IMG_0638.png"]
    
    for logo_file in logo_files:
        try:
            with open(logo_file, "rb") as f:
                image_data = f.read()
                image_b64 = base64.b64encode(image_data).decode()
                image_type = "png" if logo_file.endswith('.png') else "jpeg"
                return f'<img src="data:image/{image_type};base64,{image_b64}" alt="TENKI Logo" style="width: 48px; height: 48px; border-radius: 50%; object-fit: cover; box-shadow: 0 0 0 2px var(--accent-color-blue);" />'
        except FileNotFoundError:
            continue
    
    # 如果找不到圖片，則回傳一個帶有漸變背景的圓形 div
    return '<div style="width: 48px; height: 48px; background: linear-gradient(135deg, var(--accent-color-blue), var(--accent-color-purple)); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.2rem; color: white; box-shadow: 0 0 0 2px var(--accent-color-blue);">T</div>'

# ====== 設計系統 - 全面重新設計 ======
def load_css():
    """載入CSS樣式 - 全面優化為專業金融平台風格"""
    st.markdown("""
    <style>
        /* 全局字體導入 */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=IBM+Plex+Sans:wght@400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');
        
        /* CSS 變數：定義全局顏色、字體、間距等 */
        :root {
            --primary-bg: #0D1117; /* 主背景色 - 深藍灰 */
            --secondary-bg: #161B22; /* 次要背景色 (卡片、區塊) - 稍淺的深藍灰 */
            --tertiary-bg: #21262D; /* 第三級背景色 (懸停、活躍) */
            --border-color: rgba(60, 60, 60, 0.5); /* 邊框顏色 */
            --text-color-primary: #E6EDF3; /* 主要文字顏色 - 淺灰白 */
            --text-color-secondary: #8B949E; /* 次要文字顏色 - 中灰 */
            --accent-color-blue: #58A6FF; /* 強調藍色 */
            --accent-color-purple: #C77DFF; /* 強調紫色 */
            --positive-color: #3FB950; /* 正收益綠色 */
            --negative-color: #F85149; /* 負收益紅色 */
            --neutral-color: #C9D1D9; /* 中性色 */
            --border-radius-lg: 16px; /* 大圓角 */
            --border-radius-md: 10px; /* 中圓角 */
            --border-radius-sm: 6px; /* 小圓角 */
            --gradient-primary: linear-gradient(135deg, var(--accent-color-blue) 0%, var(--accent-color-purple) 100%);
            --gradient-secondary: linear-gradient(135deg, #334155, #1e293b); /* 用於卡片背景 */
        }

        /* Streamlit 應用程式基礎樣式 */
        .main .block-container {
            padding: 2.5rem !important; /* 增加整體內邊距 */
            max-width: 1600px !important; /* 增加最大寬度 */
            background-color: var(--primary-bg) !important;
            font-family: 'Inter', sans-serif !important;
            color: var(--text-color-primary) !important;
        }
        
        .stApp {
            background-color: var(--primary-bg) !important;
            color: var(--text-color-primary) !important;
            animation: fadeIn 0.8s ease-out; /* 頁面載入動畫 */
        }

        /* 隱藏預設 Streamlit UI */
        #MainMenu, footer, header, .stDeployButton, .stDecoration {
            display: none !important;
        }
        
        /* 側邊欄樣式 */
        .stSidebar {
            background-color: var(--secondary-bg) !important; /* 側邊欄背景 */
            padding-top: 2rem;
            border-right: 1px solid var(--border-color);
            box-shadow: 2px 0 10px rgba(0,0,0,0.3);
        }
        .stSidebar .stButton > button {
            width: 100%;
            display: flex;
            justify-content: flex-start;
            align-items: center;
            gap: 12px;
            padding: 0.75rem 1.25rem !important;
            margin-bottom: 0.5rem;
            background: none !important;
            border: none !important;
            color: var(--text-color-secondary) !important;
            font-weight: 500 !important;
            font-size: 1.05rem;
            transition: all 0.2s ease;
        }
        .stSidebar .stButton > button:hover {
            color: var(--text-color-primary) !important;
            background-color: var(--tertiary-bg) !important;
            transform: translateX(5px);
        }
        .stSidebar .stButton > button.st-emotion-cache-xx6afc.e1nzilvr5 { /* Selected button */
            color: var(--text-color-primary) !important;
            background-color: var(--tertiary-bg) !important;
            border-left: 4px solid var(--accent-color-blue) !important; /* 活躍狀態指示 */
            font-weight: 700 !important;
        }
        .stSidebar .stButton > button > div > p {
            font-size: 1.05rem !important; /* 調整側邊欄文字大小 */
        }
        
        /* 標題與文字樣式 */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', sans-serif; /* 使用更現代的標題字體 */
            color: var(--text-color-primary);
            font-weight: 700;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
        }
        h1 { 
            font-size: 2.8rem; 
            letter-spacing: -0.03em;
            background: linear-gradient(90deg, var(--text-color-primary), #A0AEC0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        h2 { font-size: 2.2rem; margin-top: 2rem; }
        h3 { font-size: 1.8rem; margin-top: 1.8rem; }
        p {
            color: var(--text-color-secondary);
            line-height: 1.6;
            margin-bottom: 1rem;
        }

        /* Hero Section (登陸頁面主視覺) */
        .hero-section {
            text-align: center;
            padding: 6rem 3rem;
            background: linear-gradient(135deg, rgba(88, 166, 255, 0.1), rgba(199, 125, 255, 0.1)); /* 柔和漸變背景 */
            border-radius: var(--border-radius-lg);
            margin-bottom: 3rem;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        
        .hero-logo {
            margin: 0 auto 1.5rem;
            display: flex;
            justify-content: center;
        }
        
        .hero-title {
            font-family: 'Outfit', sans-serif;
            font-size: 4.5rem; /* 更大的標題 */
            font-weight: 800;
            margin-bottom: 1rem;
            background: var(--gradient-primary); /* 使用預定義的漸變 */
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.1;
        }
        
        .hero-subtitle {
            font-size: 1.8rem;
            color: var(--text-color-secondary);
            margin-bottom: 0.8rem;
            font-weight: 500;
        }
        
        .hero-tagline {
            font-size: 1.4rem;
            color: var(--neutral-color);
            margin-bottom: 2rem;
            font-style: italic;
            font-weight: 300;
        }
        
        .hero-description {
            font-size: 1.1rem;
            color: var(--text-color-secondary);
            line-height: 1.7;
            margin-bottom: 3rem;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* 現代卡片 - 全面重新設計 */
        .modern-card {
            background: var(--secondary-bg);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius-lg);
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden; /* 確保內部內容不會溢出圓角 */
        }
        
        .modern-card:hover {
            transform: translateY(-5px); /* 輕微上浮效果 */
            box-shadow: 0 12px 35px rgba(var(--accent-color-blue-rgb), 0.25); /* 帶有藍色光暈的陰影 */
        }
        
        .card-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--text-color-primary);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .card-subtitle {
            font-size: 1rem;
            color: var(--text-color-secondary);
            margin-bottom: 1.5rem;
        }

        /* 指標卡片 */
        .metric-card {
            background: var(--secondary-bg);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius-md);
            padding: 1.5rem;
            text-align: center;
            margin-bottom: 1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: transform 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-3px);
        }
        
        .metric-value {
            font-family: 'IBM Plex Sans', monospace; /* 數據使用等寬字體更專業 */
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--text-color-primary);
            margin-bottom: 0.5rem;
            letter-spacing: -0.05em;
        }
        
        .metric-label {
            color: var(--text-color-secondary);
            font-size: 0.9rem;
            font-weight: 500;
            text-transform: uppercase;
        }
        
        .positive { color: var(--positive-color) !important; }
        .negative { color: var(--negative-color) !important; }
        .neutral { color: var(--neutral-color) !important; } /* for win rate */

        /* Streamlit 內建 metric 優化 */
        .st-emotion-cache-1g8fg0f.e1nzilvr1 { /* target the metric container */
            background-color: var(--secondary-bg);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius-md);
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: transform 0.2s ease;
        }
        .st-emotion-cache-1g8fg0f.e1nzilvr1:hover {
            transform: translateY(-3px);
        }
        .st-emotion-cache-1g8fg0f.e1nzilvr1 .st-emotion-cache-e3g6d0.e1nzilvr4 { /* label */
            color: var(--text-color-secondary);
            font-size: 0.9rem;
            text-transform: uppercase;
            font-weight: 500;
        }
        .st-emotion-cache-1g8fg0f.e1nzilvr1 .st-emotion-cache-e3g6d0.e1nzilvr3 { /* value */
            font-family: 'IBM Plex Sans', monospace;
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--text-color-primary);
            margin-top: 0.3rem;
            margin-bottom: 0.3rem;
            letter-spacing: -0.03em;
        }
        .st-emotion-cache-1g8fg0f.e1nzilvr1 .st-emotion-cache-e3g6d0.e1nzilvr2 { /* delta */
            font-family: 'IBM Plex Sans', monospace;
            font-size: 1.1rem;
            font-weight: 600;
        }
        .st-emotion-cache-e3g6d0.e1nzilvr2.positive { color: var(--positive-color); }
        .st-emotion-cache-e3g6d0.e1nzilvr2.negative { color: var(--negative-color); }
        .st-emotion-cache-e3g6d0.e1nzilvr2.neutral { color: var(--neutral-color); }


        /* 按鈕優化 */
        .stButton > button {
            background: var(--gradient-primary) !important; /* 使用漸變背景 */
            border: none !important;
            border-radius: var(--border-radius-md) !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 0.8rem 1.8rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            font-size: 1.05rem;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(88, 166, 255, 0.3) !important; /* 藍色光暈陰影 */
            filter: brightness(1.1); /* 輕微提亮 */
        }
        /* 次要按鈕 */
        .stButton button[data-testid="stFormSubmitButton"] { /* 鎖定提交按鈕 */
             background: var(--accent-color-blue) !important; /* 單一藍色 */
             box-shadow: none !important;
             transition: all 0.2s ease;
        }
        .stButton button[data-testid="stFormSubmitButton"]:hover {
             filter: brightness(1.2);
             transform: translateY(-2px) !important;
             box-shadow: 0 4px 10px rgba(88, 166, 255, 0.3) !important;
        }
        /* 針對 secondary 按鈕 */
        .stButton > button[kind="secondary"] {
            background: var(--secondary-bg) !important;
            color: var(--accent-color-blue) !important;
            border: 1px solid var(--border-color) !important;
            box-shadow: none !important;
        }
        .stButton > button[kind="secondary"]:hover {
            background: var(--tertiary-bg) !important;
            color: var(--text-color-primary) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
        }


        /* 表單優化 */
        .stTextInput > div > div > input {
            background: var(--secondary-bg) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: var(--border-radius-md) !important;
            color: var(--text-color-primary) !important;
            padding: 0.8rem 1rem !important;
            font-size: 1.05rem;
            transition: all 0.2s ease;
        }
        .stTextInput > div > div > input:focus {
            border-color: var(--accent-color-blue) !important;
            box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.3);
        }
        .stTextInput label {
            color: var(--text-color-secondary) !important;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }
        
        .stSelectbox > div > div {
            background: var(--secondary-bg) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: var(--border-radius-md) !important;
            color: var(--text-color-primary) !important;
            padding: 0.5rem 1rem !important;
            font-size: 1.05rem;
            transition: all 0.2s ease;
        }
        .stSelectbox > div > div:focus-within {
             border-color: var(--accent-color-blue) !important;
             box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.3);
        }
        .stSelectbox label {
            color: var(--text-color-secondary) !important;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }

        /* 警告/訊息框 */
        .stAlert {
            border-radius: var(--border-radius-md) !important;
            margin-bottom: 1rem;
        }
        .stAlert.success {
            background-
