import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import time
import base64
import plotly.graph_objects as go
import plotly.express as px
from concurrent.futures import ThreadPoolExecutor
import json

# ====== 頁面配置 ======
st.set_page_config(
    page_title="TENKI - 転機 | Professional Investment Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====== 多語言支援系統（增加日文） ======
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
        "risk_level": "風險等級",
        "platform_usage": "平台使用",
        "solution_count": "解決方案生成",
        "portfolio_count": "投資組合追蹤",
        "usage_days": "累計使用天數"
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
        "risk_level": "Risk Level",
        "platform_usage": "Platform Usage",
        "solution_count": "Solutions Generated",
        "portfolio_count": "Portfolios Tracked",
        "usage_days": "Days Used"
    },
    "ja": {
        "app_name": "TENKI",
        "app_subtitle": "転機",
        "slogan": "Turning Insight into Opportunity",
        "tagline": "洞察力を機会に変える",
        "login": "ログイン",
        "register": "登録",
        "get_started": "始める",
        "email": "メール",
        "password": "パスワード",
        "google_login": "Googleでログイン",
        "apple_login": "Appleでログイン",
        "dashboard": "ダッシュボード",
        "virtual_portfolio": "バーチャルポートフォリオ",
        "my_subscription": "サブスクリプション",
        "settings": "設定",
        "auto_navigation": "自動ナビゲーション",
        "solution_generator": "ソリューション生成",
        "market_overview": "市場概況",
        "expert_insights": "専門家の洞察",
        "recommended_targets": "推奨銘柄",
        "action_plan": "アクションプラン",
        "add_to_watchlist": "ウォッチリストに追加",
        "logout": "ログアウト",
        "welcome": "おかえりなさい",
        "today_pnl": "本日の損益",
        "total_return": "総リターン",
        "win_rate": "勝率",
        "loading": "読み込み中...",
        "generate_solution": "ソリューション生成",
        "risk_preference": "リスク許容度",
        "investment_goal": "投資目標",
        "conservative": "保守的",
        "moderate": "中程度",
        "aggressive": "積極的",
        "growth": "成長重視",
        "income": "収益重視",
        "balanced": "バランス",
        "disclaimer": "免責事項：本プラットフォームの情報は参考のみであり、投資アドバイスではありません。投資にはリスクが伴います。",
        "features_title": "主要機能",
        "ai_insights": "AI分析",
        "ai_insights_desc": "人工知能を活用した市場トレンド分析",
        "portfolio_management": "ポートフォリオ管理",
        "portfolio_management_desc": "プロフェッショナルな仮想取引システム",
        "real_time_data": "リアルタイムデータ",
        "real_time_data_desc": "グローバル金融市場データの同期",
        "risk_control": "インテリジェントリスク管理",
        "risk_control_desc": "多層リスク評価システム",
        "entry_point": "エントリーポイント",
        "exit_point": "エグジットポイント",
        "expected_return": "期待リターン",
        "monthly_plan": "月額 $22",
        "next_billing": "次回請求",
        "payment_method": "支払い方法",
        "portfolio_value": "ポートフォリオ価値",
        "risk_level": "リスクレベル",
        "platform_usage": "プラットフォーム利用",
        "solution_count": "生成ソリューション数",
        "portfolio_count": "追跡ポートフォリオ数",
        "usage_days": "利用日数"
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
def get_logo_base64():
    """獲取Logo Base64"""
    logo_files = ["IMG_0640.jpeg", "IMG_0639.jpeg", "IMG_0638.png"]
    
    for logo_file in logo_files:
        try:
            with open(logo_file, "rb") as f:
                image_data = f.read()
                image_b64 = base64.b64encode(image_data).decode()
                image_type = "png" if logo_file.endswith('.png') else "jpeg"
                return f'data:image/{image_type};base64,{image_b64}'
        except:
            continue
    
    return None

# ====== 修正後的設計系統 ======
def load_css():
    """載入修正後的CSS樣式"""
    st.markdown("""
    <style>
        /* 字體導入 - 包含日文字體 */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;800;900&display=swap');
        
        /* 基礎設定 - 修正背景和字體 */
        .main .block-container {
            padding: 1rem !important;
            max-width: 1200px !important;
            background: linear-gradient(135deg, #0a0b0f 0%, #1c2128 100%) !important;
            font-family: 'Inter', 'Noto Sans JP', sans-serif !important;
            color: #ffffff !important; /* 加強字體對比度 */
        }
        
        #MainMenu, footer, header, .stDeployButton, .stDecoration {
            display: none !important;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0a0b0f 0%, #1c2128 100%) !important;
        }
        
        /* 修正Hero Section - 解決Logo歪斜問題 */
        .hero-section {
            text-align: center;
            padding: 4rem 2rem;
            background: linear-gradient(135deg, rgba(14, 165, 233, 0.08), rgba(139, 92, 246, 0.08));
            border-radius: 24px;
            margin-bottom: 3rem;
            border: 1px solid rgba(255, 255, 255, 0.15);
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
            background: 
                radial-gradient(circle at 20% 20%, rgba(14, 165, 233, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
            z-index: 0;
        }
        
        .hero-content {
            position: relative;
            z-index: 10;
        }
        
        /* 修正Logo顯示 - 防止歪斜 */
        .hero-logo-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 2rem;
        }
        
        .hero-logo {
            width: 100px;
            height: 100px;
            margin: 0 auto 1.5rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
            box-shadow: 0 0 40px rgba(14, 165, 233, 0.4);
            animation: gentle-pulse 3s infinite;
            /* 防止變形 */
            flex-shrink: 0;
            object-fit: cover;
            overflow: hidden;
        }
        
        .hero-logo img {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            object-fit: cover;
            /* 防止圖片變形 */
            transform: none !important;
        }
        
        @keyframes gentle-pulse {
            0%, 100% { 
                transform: scale(1);
                box-shadow: 0 0 40px rgba(14, 165, 233, 0.4);
            }
            50% { 
                transform: scale(1.02);
                box-shadow: 0 0 50px rgba(14, 165, 233, 0.5);
            }
        }
        
        /* 修正標題字體 - 提高清晰度 */
        .hero-title {
            font-family: 'Outfit', 'Noto Sans JP', sans-serif;
            font-size: clamp(2.5rem, 8vw, 4.5rem);
            font-weight: 800;
            margin-bottom: 1rem;
            /* 增強字體對比度 */
            color: #ffffff;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
            background: linear-gradient(135deg, #ffffff, #0ea5e9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.02em;
            line-height: 1.1;
        }
        
        .hero-subtitle {
            font-family: 'Noto Sans JP', serif;
            font-size: 1.5rem;
            color: #e6edf3;
            margin-bottom: 1rem;
            font-style: italic;
            font-weight: 300;
            letter-spacing: 0.1em;
            text-shadow: 0 1px 5px rgba(0, 0, 0, 0.3);
        }
        
        .hero-tagline {
            font-size: 1.25rem;
            color: #c9d1d9;
            margin-bottom: 1rem;
            font-weight: 500;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        }
        
        .hero-description {
            font-size: 1.1rem;
            color: #c9d1d9;
            line-height: 1.7;
            margin-bottom: 3rem;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        }
        
        /* 修正現代卡片 */
        .modern-card {
            background: linear-gradient(135deg, rgba(33, 38, 45, 0.95), rgba(45, 51, 59, 0.95));
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .modern-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
            opacity: 0.9;
        }
        
        .modern-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 25px 50px -12px rgba(14, 165, 233, 0.3);
            border-color: rgba(14, 165, 233, 0.3);
        }
        
        /* 增強卡片標題清晰度 */
        .card-title {
            font-family: 'Outfit', 'Noto Sans JP', sans-serif;
            font-size: 1.75rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 1rem;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        }
        
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        .card-icon {
            font-size: 2.5rem;
            opacity: 0.8;
            text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        }
        
        /* 修正指標卡片 */
        .metric-card {
            background: linear-gradient(135deg, rgba(33, 38, 45, 0.9), rgba(45, 51, 59, 0.9));
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
            opacity: 0.6;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            border-color: rgba(14, 165, 233, 0.4);
            box-shadow: 0 10px 25px rgba(14, 165, 233, 0.2);
        }
        
        .metric-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.25rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0.5rem;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        }
        
        .metric-label {
            color: #c9d1d9;
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        
        .positive { 
            color: #22c55e !important;
            text-shadow: 0 1px 3px rgba(34, 197, 94, 0.3);
        }
        .negative { 
            color: #ef4444 !important; 
            text-shadow: 0 1px 3px rgba(239, 68, 68, 0.3);
        }
        
        /* 修正導航 */
        .nav-container {
            background: rgba(33, 38, 45, 0.98);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-wrap: wrap;
            gap: 1rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        }
        
        .nav-brand {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .nav-logo {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 1.5rem;
            color: white;
            box-shadow: 0 0 20px rgba(14, 165, 233, 0.4);
        }
        
        .nav-logo img {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            object-fit: cover;
        }
        
        .nav-title {
            font-family: 'Outfit', 'Noto Sans JP', sans-serif;
            font-weight: 800;
            font-size: 1.5rem;
            color: #ffffff;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        }
        
        /* 修正按鈕樣式 */
        .stButton > button {
            background: linear-gradient(135deg, #0ea5e9, #8b5cf6) !important;
            border: none !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            padding: 0.875rem 1.75rem !important;
            transition: all 0.3s ease !important;
            font-family: 'Inter', 'Noto Sans JP', sans-serif !important;
            font-size: 1rem !important;
            box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3) !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) scale(0.98) !important;
        }
        
        /* 修正表單元件 */
        .stTextInput > div > div > input,
        .stPasswordInput > div > div > input {
            background: rgba(33, 38, 45, 0.9) !important;
            border: 2px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 10px !important;
            color: #ffffff !important;
            font-size: 1rem !important;
            padding: 0.75rem !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stPasswordInput > div > div > input:focus {
            border-color: #0ea5e9 !important;
            box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1) !important;
        }
        
        .stSelectbox > div > div {
            background: rgba(33, 38, 45, 0.9) !important;
            border: 2px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 10px !important;
            color: #ffffff !important;
        }
        
        /* 功能卡片 */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .feature-card {
            text-align: center;
            padding: 2.5rem 2rem;
            background: rgba(33, 38, 45, 0.8);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        
        .feature-card:hover {
            transform: translateY(-6px);
            background: rgba(33, 38, 45, 0.95);
            border-color: rgba(14, 165, 233, 0.4);
            box-shadow: 0 15px 35px rgba(14, 165, 233, 0.2);
        }
        
        .feature-icon {
            font-size: 4rem;
            margin-bottom: 1.5rem;
            display: block;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }
        
        .feature-title {
            color: #ffffff;
            font-size: 1.375rem;
            font-weight: 700;
            margin-bottom: 1rem;
            font-family: 'Outfit', 'Noto Sans JP', sans-serif;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        }
        
        .feature-desc {
            color: #c9d1d9;
            line-height: 1.6;
            font-size: 1rem;
        }
        
        /* 解決方案卡片 */
        .solution-card {
            background: linear-gradient(135deg, rgba(33, 38, 45, 0.95), rgba(45, 51, 59, 0.95));
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 24px;
            padding: 3rem;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(15px);
        }
        
        .solution-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
        }
        
        .solution-theme {
            font-family: 'Outfit', 'Noto Sans JP', sans-serif;
            font-size: 2.25rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 1.5rem;
            text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        }
        
        .solution-insight {
            color: #e6edf3;
            line-height: 1.7;
            margin-bottom: 2rem;
            font-size: 1.125rem;
        }
        
        .target-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .target-card {
            background: rgba(33, 38, 45, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 18px;
            padding: 2rem;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        
        .target-card:hover {
            background: rgba(33, 38, 45, 1);
            border-color: rgba(14, 165, 233, 0.4);
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(14, 165, 233, 0.2);
        }
        
        .target-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }
        
        .target-symbol {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.5rem;
            font-weight: 800;
            color: #ffffff;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        }
        
        .target-type {
            background: rgba(139, 92, 246, 0.25);
            color: #c4b5fd;
            padding: 0.375rem 1rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border: 1px solid rgba(139, 92, 246, 0.3);
        }
        
        .target-allocation {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.25rem;
            font-weight: 800;
            color: #22c55e;
            text-shadow: 0 2px 5px rgba(34, 197, 94, 0.3);
        }
        
        .target-analysis {
            color: #c9d1d9;
            font-size: 1rem;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }
        
        .target-details {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
        }
        
        .detail-item {
            text-align: center;
            padding: 1rem;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 12px;
        }
        
        .detail-label {
            color: #7d8590;
            font-size: 0.75rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .detail-value {
            color: #ffffff;
            font-size: 0.875rem;
            font-weight: 700;
        }
        
        /* 狀態指示器 */
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 600;
            backdrop-filter: blur(10px);
        }
        
        .status-success {
            background: rgba(34, 197, 94, 0.2);
            color: #22c55e;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }
        
        .status-success::before {
            content: '●';
            animation: gentle-pulse-dot 2s infinite;
        }
        
        @keyframes gentle-pulse-dot {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
        
        /* 訂閱統計 */
        .subscription-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }
        
        .stat-item {
            text-align: center;
            padding: 2rem 1.5rem;
            background: rgba(33, 38, 45, 0.8);
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .stat-item:hover {
            transform: translateY(-3px);
            border-color: rgba(14, 165, 233, 0.3);
            box-shadow: 0 10px 25px rgba(14, 165, 233, 0.2);
        }
        
        .stat-label {
            color: #c9d1d9;
            font-size: 0.875rem;
            margin-bottom: 0.75rem;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.05em;
        }
        
        .stat-value {
            color: #ffffff;
            font-size: 1.75rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            font-family: 'JetBrains Mono', monospace;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        }
        
        .stat-desc {
            color: #7d8590;
            font-size: 0.75rem;
        }
        
        /* 免責聲明 */
        .disclaimer {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 15px;
            padding: 1.5rem;
            color: #fca5a5;
            font-size: 0.95rem;
            margin: 2rem 0;
            text-align: center;
            backdrop-filter: blur(10px);
            line-height: 1.6;
        }
        
        /* 響應式設計 */
        @media (max-width: 768px) {
            .hero-title { 
                font-size: clamp(2rem, 10vw, 3rem) !important; 
            }
            .hero-section { 
                padding: 3rem 1.5rem; 
            }
            .modern-card { 
                padding: 1.5rem; 
                margin-bottom: 1.5rem; 
            }
            .target-details { 
                grid-template-columns: 1fr; 
                gap: 0.75rem; 
            }
            .nav-container {
                padding: 1rem;
                flex-direction: column;
                gap: 1rem;
            }
            .feature-grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
            .metric-value {
                font-size: 1.75rem;
            }
        }
        
        @media (max-width: 480px) {
            .hero-logo {
                width: 80px;
                height: 80px;
            }
            .hero-description {
                font-size: 1rem;
            }
            .card-title {
                font-size: 1.5rem;
            }
            .modern-card,
            .solution-card {
                padding: 1.25rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ====== 市場數據 ======
@st.cache_data(ttl=300)
def get_market_data():
    """獲取市場數據"""
    symbols = ['SPY', 'QQQ', 'AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'META']
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
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(fetch_data, symbol) for symbol in symbols]
        for future in futures:
            result = future.result()
            if result:
                market_data[result['symbol']] = result
    
    return market_data

# ====== 修正圖表生成 - 解決重疊問題 ======
def create_market_chart(market_data):
    """創建修正後的市場概況圖表"""
    if not market_data:
        return None
    
    symbols = list(market_data.keys())
    changes = [market_data[symbol]['change_pct'] for symbol in symbols]
    colors = ['#22c55e' if change >= 0 else '#ef4444' for change in changes]
    
    fig = go.Figure(data=[
        go.Bar(
            x=symbols,
            y=changes,
            marker_color=colors,
            marker_line_color='rgba(255,255,255,0.2)',
            marker_line_width=1.5,
            text=[f'{change:+.2f}%' for change in changes],
            textposition='outside',
            textfont=dict(
                family='JetBrains Mono, monospace', 
                size=14, 
                color='#ffffff',
                weight='bold'
            ),
            hovertemplate='<b>%{x}</b><br>變化: %{y:.2f}%<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='<b>市場表現概況</b>',
            font=dict(
                family='Outfit, Noto Sans JP, sans-serif', 
                size=24, 
                color='#ffffff',
                weight='bold'
            ),
            x=0.5,
            y=0.95,  # 調整標題位置避免重疊
            xanchor='center',
            yanchor='top'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Inter, Noto Sans JP, sans-serif', 
            color='#e6edf3',
            size=12
        ),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(size=13, color='#c9d1d9', weight='bold'),
            tickangle=0,  # 水平顯示避免重疊
            title=dict(
                text='<b>股票代碼</b>',
                font=dict(size=14, color='#c9d1d9')
            )
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            showline=True,
            linecolor='rgba(255, 255, 255, 0.1)',
            zeroline=True,
            zerolinecolor='rgba(255, 255, 255, 0.3)',
            zerolinewidth=2,
            tickfont=dict(size=13, color='#c9d1d9', weight='bold'),
            title=dict(
                text='<b>變化率 (%)</b>',
                font=dict(size=14, color='#c9d1d9')
            )
        ),
        height=450,  # 增加高度避免重疊
        margin=dict(l=80, r=80, t=100, b=80),  # 調整邊距
        showlegend=False,
        hovermode='x unified'
    )
    
    return fig

def create_portfolio_chart(portfolio_data):
    """創建修正後的投資組合圓餅圖"""
    if not portfolio_data:
        return None
    
    symbols = [item['symbol'] for item in portfolio_data]
    values = [item['quantity'] * item['current_price'] for item in portfolio_data]
    colors = [
        '#0ea5e9', '#8b5cf6', '#22c55e', '#f59e0b', 
        '#ef4444', '#06b6d4', '#84cc16', '#f97316'
    ]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=symbols,
            values=values,
            hole=0.45,
            marker=dict(
                colors=colors[:len(symbols)], 
                line=dict(color='#21262d', width=3)
            ),
            textfont=dict(
                family='Inter, Noto Sans JP, sans-serif', 
                size=13, 
                color='#ffffff',
                weight='bold'
            ),
            textinfo='label+percent',
            textposition='outside',
            hovertemplate='<b>%{label}</b><br>價值: $%{value:,.0f}<br>比例: %{percent}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='<b>投資組合配置</b>',
            font=dict(
                family='Outfit, Noto Sans JP, sans-serif', 
                size=24, 
                color='#ffffff',
                weight='bold'
            ),
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Inter, Noto Sans JP, sans-serif', 
            color='#e6edf3'
        ),
        height=450,
        margin=dict(l=50, r=50, t=100, b=50),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5,
            font=dict(size=12, color='#c9d1d9')
        )
    )
    
    return fig

# ====== 投資解決方案 ======
def generate_solution(risk_pref, investment_goal):
    """生成投資解決方案"""
    if risk_pref == 'conservative' and investment_goal == 'income':
        return {
            'theme': '2025年防禦型收益投資策略',
            'insight': '專注於穩定收益資產，包括高股息股票、政府債券和REIT基金，適合保守型投資者在當前市場環境下獲得穩健回報。',
            'targets': [
                {
                    'symbol': 'VYM',
                    'type': '高股息ETF',
                    'allocation': 40,
                    'entry_point': '$115以下分批進入',
                    'exit_point': '股息率降至2.5%以下',
                    'expected_return': '5-7%',
                    'analysis': '追蹤高股息美股指數，涵蓋400多檔優質股票，提供穩定現金流，適合收益型投資者長期配置'
                },
                {
                    'symbol': 'TLT',
                    'type': '長期公債ETF',
                    'allocation': 35,
                    'entry_point': '當前價位定期定額',
                    'exit_point': 'Fed明確轉向升息',
                    'expected_return': '4-6%',
                    'analysis': '追蹤20年以上美國公債，在降息環境下表現優異，提供穩定收益和避險功能'
                },
                {
                    'symbol': 'VNQ',
                    'type': 'REIT ETF',
                    'allocation': 25,
                    'entry_point': '回調至$90以下',
                    'exit_point': '利率大幅上升時',
                    'expected_return': '6-8%',
                    'analysis': '不動產投資信託ETF，提供租金收益分配，是通脹對沖的優質工具'
                }
            ]
        }
    elif risk_pref == 'moderate' and investment_goal == 'balanced':
        return {
            'theme': '2025年AI科技平衡配置策略',
            'insight': '結合科技成長股和防禦性資產，在AI浪潮中尋求平衡收益機會。重點關注AI產業鏈上下游機會，同時保持適度的債券配置。',
            'targets': [
                {
                    'symbol': 'QQQ',
                    'type': '科技ETF',
                    'allocation': 30,
                    'entry_point': '$380以下分批進入',
                    'exit_point': '估值過高時減碼',
                    'expected_return': '8-12%',
                    'analysis': '追蹤納斯達克100指數，科技股集中度高，受惠於AI浪潮和數位轉型趨勢'
                },
                {
                    'symbol': 'NVDA',
                    'type': 'AI晶片龍頭',
                    'allocation': 25,
                    'entry_point': '技術回調時分批進入',
                    'exit_point': '基本面轉弱時',
                    'expected_return': '15-25%',
                    'analysis': 'AI晶片絕對領導者，GPU在AI訓練和推理中不可替代，資料中心需求強勁'
                },
                {
                    'symbol': 'VTI',
                    'type': '全市場ETF',
                    'allocation': 25,
                    'entry_point': '當前價位定期定額',
                    'exit_point': '長期持有',
                    'expected_return': '7-10%',
                    'analysis': '全市場指數ETF，提供最佳分散效果，降低個股風險，適合核心配置'
                },
                {
                    'symbol': 'LQD',
                    'type': '投資級債券',
                    'allocation': 20,
                    'entry_point': '收益率4%以上時',
                    'exit_point': 'Fed轉向升息時',
                    'expected_return': '4-5%',
                    'analysis': '投資級企業債券ETF，提供穩定收益，降低組合整體波動性'
                }
            ]
        }
    else:  # aggressive + growth
        return {
            'theme': '2025年積極成長科技投資攻略',
            'insight': '積極型投資者重點佈局具有顛覆性創新潛力的成長股。AI、雲端運算、電動車、生技等領域仍有巨大成長空間。',
            'targets': [
                {
                    'symbol': 'ARKK',
                    'type': '創新ETF',
                    'allocation': 30,
                    'entry_point': '大幅回調至$45以下',
                    'exit_point': '創新主題降溫時',
                    'expected_return': '15-30%',
                    'analysis': '專注顛覆性創新的主動型ETF，包含基因療法、自動駕駛、太空探索等前沿領域'
                },
                {
                    'symbol': 'TSLA',
                    'type': '電動車龍頭',
                    'allocation': 25,
                    'entry_point': '$200-220區間',
                    'exit_point': '自動駕駛進展停滯時',
                    'expected_return': '20-40%',
                    'analysis': '電動車和自動駕駛雙重領導者，受惠於能源轉型和智慧駕駛技術發展'
                },
                {
                    'symbol': 'MSFT',
                    'type': '雲端AI巨頭',
                    'allocation': 25,
                    'entry_point': '$380以下分批',
                    'exit_point': '雲端成長明顯放緩',
                    'expected_return': '12-18%',
                    'analysis': 'Azure雲端服務和AI整合最完整，企業數位轉型的最大受惠者'
                },
                {
                    'symbol': 'SOXX',
                    'type': '半導體ETF',
                    'allocation': 20,
                    'entry_point': '產業週期低點進入',
                    'exit_point': '產業週期高點',
                    'expected_return': '18-25%',
                    'analysis': '半導體產業ETF，AI基礎設施建設的核心受惠標的，週期性成長強勁'
                }
            ]
        }

# ====== 頁面函數 ======
def show_landing_page():
    """修正後的Landing Page"""
    t = TEXTS[st.session_state.language]
    logo_b64 = get_logo_base64()
    
    # 修正後的Hero Section
    if logo_b64:
        hero_logo = f'<div class="hero-logo"><img src="{logo_b64}" alt="TENKI Logo" /></div>'
    else:
        hero_logo = '<div class="hero-logo">T</div>'
    
    st.markdown(f'''
    <div class="hero-section">
        <div class="hero-content">
            <div class="hero-logo-container">
                {hero_logo}
                <h1 class="hero-title">TENKI</h1>
                <p class="hero-subtitle">{t['app_subtitle']}</p>
            </div>
            <p class="hero-tagline">{t['slogan']}</p>
            <div class="hero-description">
                專業投資決策支援平台 • 運用AI智能分析市場趨勢 • 在關鍵轉折點做出理想決策 • 實現資產穩健增值
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # 語言切換 - 增加日文
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        lang_col1, lang_col2, lang_col3 = st.columns(3)
        
        with lang_col1:
            if st.button("🇹🇼 中文", key="lang_zh_main", use_container_width=True, 
                        type="primary" if st.session_state.language == 'zh' else "secondary"):
                st.session_state.language = 'zh'
                st.rerun()
        
        with lang_col2:
            if st.button("🇺🇸 English", key="lang_en_main", use_container_width=True,
                        type="primary" if st.session_state.language == 'en' else "secondary"):
                st.session_state.language = 'en'
                st.rerun()
        
        with lang_col3:
            if st.button("🇯🇵 日本語", key="lang_ja_main", use_container_width=True,
                        type="primary" if st.session_state.language == 'ja' else "secondary"):
                st.session_state.language = 'ja'
                st.rerun()
        
        st.markdown("---")
        
        # CTA按鈕
        if st.button(f"🚀 {t['get_started']}", key="get_started_main", use_container_width=True, type="primary"):
            st.session_state.current_page = 'login'
            st.rerun()
    
    # 核心功能
    st.markdown(f'<div class="modern-card"><div class="card-header"><h2 class="card-title">{t["features_title"]}</h2><div class="card-icon">⭐</div></div></div>', unsafe_allow_html=True)
    
    # 使用Grid佈局展示功能
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">{t['ai_insights']}</div>
            <div class="feature-desc">{t['ai_insights_desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <div class="feature-title">{t['risk_control']}</div>
            <div class="feature-desc">{t['risk_control_desc']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">💼</div>
            <div class="feature-title">{t['portfolio_management']}</div>
            <div class="feature-desc">{t['portfolio_management_desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">{t['real_time_data']}</div>
            <div class="feature-desc">{t['real_time_data_desc']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 免責聲明
    st.markdown(f'''
    <div class="disclaimer">
        ⚠️ {t['disclaimer']}
    </div>
    ''', unsafe_allow_html=True)

def show_login_page():
    """登入頁面"""
    t = TEXTS[st.session_state.language]
    logo_b64 = get_logo_base64()
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        # Logo和標題
        if logo_b64:
            logo_html = f'<img src="{logo_b64}" alt="TENKI Logo" style="width: 70px; height: 70px; border-radius: 50%; object-fit: cover;" />'
        else:
            logo_html = '<div class="nav-logo">T</div>'
        
        st.markdown(f'''
        <div style="text-align: center; margin-bottom: 2.5rem;">
            <div style="display: flex; justify-content: center; margin-bottom: 1.5rem;">
                {logo_html}
            </div>
            <h1 style="font-family: 'Outfit', 'Noto Sans JP', sans-serif; font-size: 2.5rem; font-weight: 800; color: #ffffff; margin: 1rem 0 0.75rem; text-shadow: 0 2px 5px rgba(0,0,0,0.3);">TENKI</h1>
            <p style="color: #c9d1d9; font-size: 1.1rem;">{t['tagline']}</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # 登入表單
        with st.form("login_form_main", clear_on_submit=False):
            email = st.text_input(t['email'], placeholder="your@email.com", key="login_email_main")
            password = st.text_input(t['password'], type="password", placeholder="••••••••", key="login_password_main")
            
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
        st.markdown(f"**{t['login']}**" if st.session_state.language == 'ja' else "**或使用以下方式登入**")
        col_x, col_y = st.columns(2)
        with col_x:
            if st.button(f"🔍 {t['google_login']}", key="google_login_main", use_container_width=True):
                st.session_state.user_logged_in = True
                st.session_state.user_email = "user@gmail.com"
                st.session_state.current_page = 'dashboard'
                st.rerun()
        with col_y:
            if st.button(f"🍎 {t['apple_login']}", key="apple_login_main", use_container_width=True):
                st.session_state.user_logged_in = True
                st.session_state.user_email = "user@icloud.com"
                st.session_state.current_page = 'dashboard'
                st.rerun()
        
        # 返回首頁
        if st.button("← 返回首頁" if st.session_state.language != 'ja' else "← ホームに戻る", key="back_home_main", use_container_width=True):
            st.session_state.current_page = 'landing'
            st.rerun()

def create_navigation():
    """修正後的導航"""
    t = TEXTS[st.session_state.language]
    logo_b64 = get_logo_base64()
    
    # 導航欄
    if logo_b64:
        logo_html = f'<img src="{logo_b64}" alt="TENKI Logo" />'
    else:
        logo_html = 'T'
    
    st.markdown(f'''
    <div class="nav-container">
        <div class="nav-brand">
            <div class="nav-logo">{logo_html}</div>
            <span class="nav-title">TENKI</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
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
            if st.button(page_name, key=f"nav_{page_key}_main", use_container_width=True,
                        type="primary" if st.session_state.current_page == page_key else "secondary"):
                st.session_state.current_page = page_key
                st.rerun()
    
    with cols[-1]:
        if st.button(f"🚪 {t['logout']}", key="logout_nav_main"):
            st.session_state.user_logged_in = False
            st.session_state.current_page = 'landing'
            st.rerun()

def show_dashboard():
    """修正後的儀表板"""
    t = TEXTS[st.session_state.language]
    
    # 歡迎標題
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h1 class="card-title">{t['welcome']}, {st.session_state.user_email.split('@')[0]}! 🎉</h1>
            <div class="card-icon">🚀</div>
        </div>
        <p style="color: #c9d1d9; font-size: 1.1rem; line-height: 1.6;">準備好開始您今天的投資之旅了嗎？讓我們一起在市場的關鍵轉折點中，做出理想的投資決策。</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # 績效指標
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">{t['today_pnl']}</div>
            <div class="metric-value positive">+$1,234</div>
            <div style="color: #22c55e; font-size: 0.875rem; margin-top: 0.25rem;">+2.3% 今日</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">{t['total_return']}</div>
            <div class="metric-value positive">+$12,567</div>
            <div style="color: #22c55e; font-size: 0.875rem; margin-top: 0.25rem;">+15.6% 總計</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">{t['win_rate']}</div>
            <div class="metric-value">68.5%</div>
            <div style="color: #c9d1d9; font-size: 0.875rem; margin-top: 0.25rem;">↗ 持續提升</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">{t['risk_level']}</div>
            <div class="metric-value positive">低風險</div>
            <div style="color: #c9d1d9; font-size: 0.875rem; margin-top: 0.25rem;">波動率: 12.3%</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # 市場數據
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h2 class="card-title">📊 {t['market_overview']}</h2>
            <div class="status-indicator status-success">即時更新</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    with st.spinner(t['loading']):
        market_data = get_market_data()
    
    if market_data:
        # 修正後的市場圖表
        chart = create_market_chart(market_data)
        if chart:
            st.plotly_chart(chart, use_container_width=True)
        
        # 市場數據表格
        cols = st.columns(len(market_data))
        for i, (symbol, data) in enumerate(market_data.items()):
            with cols[i]:
                change_class = "positive" if data['change_pct'] >= 0 else "negative"
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">{symbol}</div>
                    <div class="metric-value">${data['price']:.2f}</div>
                    <div class="metric-value {change_class}" style="font-size: 1rem; margin-top: 0.25rem;">{data['change']:+.2f} ({data['change_pct']:+.2f}%)</div>
                </div>
                ''', unsafe_allow_html=True)
    
    # 快速操作
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h2 class="card-title">⚡ 快速操作</h2>
            <div class="card-icon">🎯</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"🧭 {t['auto_navigation']}", key="quick_nav_main", use_container_width=True):
            st.session_state.current_page = 'auto_navigation'
            st.rerun()
    
    with col2:
        if st.button(f"⚡ {t['generate_solution']}", key="quick_solution_main", use_container_width=True):
            st.session_state.current_page = 'solution_generator'
            st.rerun()
    
    with col3:
        if st.button(f"💼 {t['virtual_portfolio']}", key="quick_portfolio_main", use_container_width=True):
            st.session_state.current_page = 'virtual_portfolio'
            st.rerun()

def show_auto_navigation():
    """自動導航模式"""
    t = TEXTS[st.session_state.language]
    
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h1 class="card-title">🧭 {t['auto_navigation']}</h1>
            <div class="card-icon">🎯</div>
        </div>
        <p style="color: #c9d1d9; font-size: 1.1rem; line-height: 1.6;">根據您的投資偏好和目標，為您提供個性化的投資建議。我們的AI系統將分析您的風險承受能力和投資目標，生成最適合的投資組合配置。</p>
    </div>
    ''', unsafe_allow_html=True)
    
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
            key="risk_select_main"
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
            key="goal_select_main"
        )
        st.session_state.investment_goal = invest_goal
    
    # 生成解決方案
    if st.button(f"🎯 {t['generate_solution']}", key="generate_auto_main", use_container_width=True, type="primary"):
        with st.spinner(t['loading']):
            solution = generate_solution(risk_pref, invest_goal)
            st.session_state.generated_solutions = [solution]
            time.sleep(1.5)
        
        st.success("✅ 已生成個性化投資解決方案！")
        st.session_state.current_page = 'solution_generator'
        st.rerun()
    
    # 當前設定
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h3 class="card-title">⚙️ 當前設定摘要</h3>
            <div class="status-indicator status-success">已配置</div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 1rem;">
            <div class="stat-item">
                <div class="stat-label">{t['risk_preference']}</div>
                <div class="stat-value">
                    {t['conservative'] if risk_pref == 'conservative' else t['moderate'] if risk_pref == 'moderate' else t['aggressive']}
                </div>
                <div class="stat-desc">
                    {'低風險' if risk_pref == 'conservative' else '中風險' if risk_pref == 'moderate' else '高風險'}
                </div>
            </div>
            <div class="stat-item">
                <div class="stat-label">{t['investment_goal']}</div>
                <div class="stat-value">
                    {t['income'] if invest_goal == 'income' else t['balanced'] if invest_goal == 'balanced' else t['growth']}
                </div>
                <div class="stat-desc">
                    {'收益優先' if invest_goal == 'income' else '平衡配置' if invest_goal == 'balanced' else '成長優先'}
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def show_solution_generator():
    """解決方案生成器"""
    t = TEXTS[st.session_state.language]
    
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h1 class="card-title">⚡ {t['solution_generator']}</h1>
            <div class="card-icon">🎯</div>
        </div>
        <p style="color: #c9d1d9; font-size: 1.1rem; line-height: 1.6;">基於AI分析和專家洞察，為您生成個性化投資解決方案。我們的系統會根據當前市場環境、您的風險偏好和投資目標，提供詳細的投資建議和具體行動計劃。</p>
    </div>
    ''', unsafe_allow_html=True)
    
    if st.session_state.generated_solutions:
        solution = st.session_state.generated_solutions[0]
        
        st.markdown(f'''
        <div class="solution-card">
            <h2 class="solution-theme">🎯 {solution['theme']}</h2>
            <p class="solution-insight">{solution['insight']}</p>
            
            <div style="margin: 2rem 0;">
                <h3 style="color: #ffffff; margin-bottom: 1rem; font-family: 'Outfit', 'Noto Sans JP', sans-serif; font-size: 1.5rem;">💡 {t['expert_insights']}</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem;">
                    <div style="text-align: center; padding: 1.5rem; background: rgba(14, 165, 233, 0.1); border: 1px solid rgba(14, 165, 233, 0.3); border-radius: 16px; backdrop-filter: blur(10px);">
                        <div style="color: #0ea5e9; font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">市場機會</div>
                        <div style="color: #22c55e; font-weight: 600; font-size: 0.9rem;">AI科技革命浪潮</div>
                    </div>
                    <div style="text-align: center; padding: 1.5rem; background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 16px; backdrop-filter: blur(10px);">
                        <div style="color: #f59e0b; font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">風險等級</div>
                        <div style="color: #f59e0b; font-weight: 600; font-size: 0.9rem;">中等風險</div>
                    </div>
                    <div style="text-align: center; padding: 1.5rem; background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 16px; backdrop-filter: blur(10px);">
                        <div style="color: #8b5cf6; font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">建議時程</div>
                        <div style="color: #8b5cf6; font-weight: 600; font-size: 0.9rem;">6-12個月</div>
                    </div>
                </div>
            </div>
            
            <h3 style="color: #ffffff; margin-bottom: 1.5rem; font-family: 'Outfit', 'Noto Sans JP', sans-serif; font-size: 1.5rem;">📊 {t['recommended_targets']}</h3>
        </div>
        ''', unsafe_allow_html=True)
        
        # 建議標的
        for target in solution['targets']:
            st.markdown(f'''
            <div class="target-card">
                <div class="target-header">
                    <div>
                        <div class="target-symbol">{target['symbol']}</div>
                        <div class="target-type">{target['type']}</div>
                    </div>
                    <div class="target-allocation">{target['allocation']}%</div>
                </div>
                <div class="target-analysis">{target['analysis']}</div>
                <div class="target-details">
                    <div class="detail-item">
                        <div class="detail-label">{t['entry_point']}</div>
                        <div class="detail-value">{target['entry_point']}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">{t['exit_point']}</div>
                        <div class="detail-value">{target['exit_point']}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">{t['expected_return']}</div>
                        <div class="detail-value">{target['expected_return']}</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # 操作按鈕
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"📌 {t['add_to_watchlist']}", key="add_watchlist_main", use_container_width=True):
                st.success("✅ 已加入追蹤清單！")
        
        with col2:
            if st.button("💼 加入虛擬組合", key="add_portfolio_main", use_container_width=True):
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
        st.markdown(f'''
        <div class="modern-card">
            <div style="text-align: center; padding: 4rem 2rem;">
                <div style="font-size: 5rem; margin-bottom: 2rem;">🎯</div>
                <h2 style="color: #ffffff; font-size: 2rem; font-weight: 700; margin-bottom: 1rem; font-family: 'Outfit', 'Noto Sans JP', sans-serif;">
                    尚無生成的投資解決方案
                </h2>
                <p style="color: #c9d1d9; margin-bottom: 2.5rem; font-size: 1.1rem; line-height: 1.6;">
                    請先前往自動導航模式設定您的投資偏好，<br/>
                    我們將為您生成專業的投資建議
                </p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("🧭 前往自動導航設定", key="goto_nav_main", use_container_width=True, type="primary"):
            st.session_state.current_page = 'auto_navigation'
            st.rerun()

def show_virtual_portfolio():
    """虛擬投資組合"""
    t = TEXTS[st.session_state.language]
    
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h1 class="card-title">💼 {t['virtual_portfolio']}</h1>
            <div class="card-icon">📈</div>
        </div>
        <p style="color: #c9d1d9; font-size: 1.1rem; line-height: 1.6;">無風險的虛擬交易環境，驗證您的投資策略。在這裡您可以模擬真實的投資操作，追蹤績效表現，並在實際投資前測試您的策略。</p>
    </div>
    ''', unsafe_allow_html=True)
    
    if st.session_state.virtual_portfolio:
        # 計算總績效
        total_value = sum(item['quantity'] * item['current_price'] for item in st.session_state.virtual_portfolio)
        total_cost = sum(item['quantity'] * item['entry_price'] for item in st.session_state.virtual_portfolio)
        total_pnl = total_value - total_cost
        total_return_pct = (total_pnl / total_cost * 100) if total_cost > 0 else 0
        
        # 績效指標
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">{t['portfolio_value']}</div>
                <div class="metric-value">${total_value:,.0f}</div>
                <div style="color: #7d8590; font-size: 0.8rem; margin-top: 0.25rem;">投入成本: ${total_cost:,.0f}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            pnl_class = "positive" if total_pnl >= 0 else "negative"
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">{t['total_return']}</div>
                <div class="metric-value {pnl_class}">${total_pnl:+,.0f}</div>
                <div class="metric-value {pnl_class}" style="font-size: 1rem; margin-top: 0.25rem;">{total_return_pct:+.2f}%</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            win_count = sum(1 for item in st.session_state.virtual_portfolio if item['current_price'] > item['entry_price'])
            win_rate = (win_count / len(st.session_state.virtual_portfolio)) * 100
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">{t['win_rate']}</div>
                <div class="metric-value">{win_rate:.1f}%</div>
                <div style="color: #7d8590; font-size: 0.8rem; margin-top: 0.25rem;">{win_count}/{len(st.session_state.virtual_portfolio)} 獲利</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">持倉數量</div>
                <div class="metric-value">{len(st.session_state.virtual_portfolio)}</div>
                <div style="color: #7d8590; font-size: 0.8rem; margin-top: 0.25rem;">檔標的</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # 修正後的投資組合圖表
        chart = create_portfolio_chart(st.session_state.virtual_portfolio)
        if chart:
            st.plotly_chart(chart, use_container_width=True)
        
        # 持倉明細
        st.markdown(f'<div class="modern-card"><h3 class="card-title">📊 持倉明細</h3></div>', unsafe_allow_html=True)
        
        for i, item in enumerate(st.session_state.virtual_portfolio):
            pnl = (item['current_price'] - item['entry_price']) * item['quantity']
            pnl_pct = ((item['current_price'] - item['entry_price']) / item['entry_price'] * 100) if item['entry_price'] > 0 else 0
            pnl_color = "#22c55e" if pnl >= 0 else "#ef4444"
            
            st.markdown(f'''
            <div class="modern-card" style="padding: 1.5rem; margin-bottom: 1rem;">
                <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 1.5rem; align-items: center;">
                    <div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 1.25rem; color: #ffffff; margin-bottom: 0.25rem;">{item['symbol']}</div>
                        <div style="color: #c9d1d9; font-size: 0.9rem;">{item['quantity']:.0f} 股</div>
                        <div style="margin-top: 0.5rem;">
                            <span style="background: rgba(14, 165, 233, 0.2); color: #0ea5e9; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">持有中</span>
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #ffffff; font-weight: 700; font-size: 1.1rem;">${item['entry_price']:.2f}</div>
                        <div style="color: #7d8590; font-size: 0.8rem; margin-top: 0.25rem;">買入價</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #ffffff; font-weight: 700; font-size: 1.1rem;">${item['current_price']:.2f}</div>
                        <div style="color: #7d8590; font-size: 0.8rem; margin-top: 0.25rem;">現價</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-family: 'JetBrains Mono', monospace; font-weight: 800; color: {pnl_color}; font-size: 1.1rem;">${pnl:+,.0f}</div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: {pnl_color}; font-size: 0.9rem; margin-top: 0.25rem;">{pnl_pct:+.2f}%</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # 操作按鈕
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 更新價格", key="update_prices_main", use_container_width=True):
                for item in st.session_state.virtual_portfolio:
                    change_pct = np.random.uniform(-0.05, 0.05)
                    item['current_price'] *= (1 + change_pct)
                st.success("✅ 價格已更新！")
                st.rerun()
        
        with col2:
            if st.button("📊 生成報告", key="generate_report_main", use_container_width=True):
                st.info("📄 績效報告功能開發中...")
        
        with col3:
            if st.button("🗑️ 清空組合", key="clear_portfolio_main", use_container_width=True):
                st.session_state.virtual_portfolio = []
                st.success("✅ 虛擬組合已清空！")
                st.rerun()
    
    else:
        st.markdown(f'''
        <div class="modern-card">
            <div style="text-align: center; padding: 4rem 2rem;">
                <div style="font-size: 5rem; margin-bottom: 2rem;">💼</div>
                <h2 style="color: #ffffff; font-size: 2rem; font-weight: 700; margin-bottom: 1rem; font-family: 'Outfit', 'Noto Sans JP', sans-serif;">
                    您的虛擬投資組合是空的
                </h2>
                <p style="color: #c9d1d9; margin-bottom: 2.5rem; font-size: 1.1rem; line-height: 1.6;">
                    透過解決方案生成器建立您的第一個投資組合，<br/>
                    開始無風險的投資策略驗證
                </p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("⚡ 前往解決方案生成器", key="goto_solution_main", use_container_width=True, type="primary"):
            st.session_state.current_page = 'solution_generator'
            st.rerun()

def show_subscription():
    """訂閱管理"""
    t = TEXTS[st.session_state.language]
    
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h1 class="card-title">💳 {t['my_subscription']}</h1>
            <div class="card-icon">⭐</div>
        </div>
        <p style="color: #c9d1d9; font-size: 1.1rem; line-height: 1.6;">管理您的訂閱方案和付款設定。享受專業級投資分析工具和個性化服務。</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # 訂閱狀態
    st.markdown('<div class="status-indicator status-success">訂閱有效</div>', unsafe_allow_html=True)
    
    st.markdown("### 📋 訂閱資訊")
    
    # 使用Streamlit原生組件顯示訂閱資訊
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
        <div class="stat-item">
            <div class="stat-label">當前方案</div>
            <div class="stat-value">{t['monthly_plan']}</div>
            <div class="stat-desc">✅ 無限制使用所有功能</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="stat-item">
            <div class="stat-label">{t['next_billing']}</div>
            <div class="stat-value">2025年11月22日</div>
            <div class="stat-desc">自動續訂</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="stat-item">
            <div class="stat-label">{t['payment_method']}</div>
            <div class="stat-value">•••• •••• •••• 1234</div>
            <div class="stat-desc">Visa 信用卡</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # 訂閱功能
    st.markdown("### 🎯 訂閱功能")
    
    features = [
        "無限制解決方案生成", "專家投資組合追蹤", "即時市場數據推送",
        "個性化投資建議", "風險管理工具", "24/7 客戶支援"
    ]
    
    cols = st.columns(2)
    for i, feature in enumerate(features):
        with cols[i % 2]:
            st.markdown(f'''
            <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 12px; margin-bottom: 1rem;">
                <div style="color: #22c55e; font-size: 1.25rem;">✅</div>
                <div style="color: #e6edf3; font-size: 1rem;">{feature}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    # 使用統計
    st.markdown("### 📊 使用統計")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">{t['solution_count']}</div>
            <div class="metric-value">23</div>
            <div style="color: #7d8590; font-size: 0.8rem; margin-top: 0.25rem;">本月使用次數</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">{t['portfolio_count']}</div>
            <div class="metric-value">156</div>
            <div style="color: #7d8590; font-size: 0.8rem; margin-top: 0.25rem;">累計建立組合數</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">{t['usage_days']}</div>
            <div class="metric-value">47</div>
            <div style="color: #7d8590; font-size: 0.8rem; margin-top: 0.25rem;">天（累計登入）</div>
        </div>
        ''', unsafe_allow_html=True)

def show_settings():
    """設定頁面"""
    t = TEXTS[st.session_state.language]
    
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h1 class="card-title">⚙️ {t['settings']}</h1>
            <div class="card-icon">🛠️</div>
        </div>
        <p style="color: #c9d1d9; font-size: 1.1rem; line-height: 1.6;">個性化您的TENKI體驗設定，調整語言偏好、投資風格和通知設定。</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # 語言設定 - 包含日文
    st.markdown("### 🌐 語言設定")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🇹🇼 繁體中文", key="set_zh_main",
                     use_container_width=True,
                     type="primary" if st.session_state.language == 'zh' else "secondary"):
            st.session_state.language = 'zh'
            st.rerun()
    
    with col2:
        if st.button("🇺🇸 English", key="set_en_main",
                     use_container_width=True,
                     type="primary" if st.session_state.language == 'en' else "secondary"):
            st.session_state.language = 'en'
            st.rerun()
    
    with col3:
        if st.button("🇯🇵 日本語", key="set_ja_main",
                     use_container_width=True,
                     type="primary" if st.session_state.language == 'ja' else "secondary"):
            st.session_state.language = 'ja'
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
            key="settings_risk_main"
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
            key="settings_goal_main"
        )
    
    if st.button("💾 儲存設定", key="save_settings_main", use_container_width=True, type="primary"):
        st.session_state.risk_preference = new_risk_pref
        st.session_state.investment_goal = new_invest_goal
        st.success("✅ 設定已儲存！")
    
    # 通知設定
    st.markdown("### 🔔 通知設定")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        email_notifications = st.checkbox("📧 電子郵件通知", value=True, key="email_notif_main")
    with col2:
        push_notifications = st.checkbox("📱 推播通知", value=True, key="push_notif_main")
    with col3:
        sms_notifications = st.checkbox("📞 簡訊通知", value=False, key="sms_notif_main")

# ====== 主應用程式 ======
def main():
    """TENKI主程式 - 修正版"""
    
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
        st.markdown(f'''
        <div class="disclaimer">
            ⚠️ {t['disclaimer']}
        </div>
        ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
