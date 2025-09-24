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
                return f'<img src="data:image/{image_type};base64,{image_b64}" alt="TENKI Logo" style="width: 64px; height: 64px; border-radius: 50%; object-fit: cover;" />'
        except:
            continue
    
    return '<div style="width: 64px; height: 64px; background: linear-gradient(135deg, #0ea5e9, #8b5cf6); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.5rem; color: white; box-shadow: 0 0 30px rgba(14, 165, 233, 0.4);">T</div>'

# ====== 頂級設計系統 ======
def load_premium_css():
    """載入頂級設計系統"""
    st.markdown("""
    <style>
        /* ===== 字體導入 ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800;900&display=swap');
        
        /* ===== 色彩與設計系統 ===== */
        :root {
            /* 主色調 - 極深藍黑基調 */
            --bg-primary: #0a0b0f;
            --bg-secondary: #0d1117;
            --bg-tertiary: #161b22;
            --bg-elevated: #1c2128;
            --bg-surface: #21262d;
            --bg-overlay: #2d333b;
            
            /* 冷金屬霧藍系列 */
            --metal-blue-50: #f0f9ff;
            --metal-blue-100: #e0f2fe;
            --metal-blue-200: #bae6fd;
            --metal-blue-300: #7dd3fc;
            --metal-blue-400: #38bdf8;
            --metal-blue-500: #0ea5e9;
            --metal-blue-600: #0284c7;
            --metal-blue-700: #0369a1;
            --metal-blue-800: #075985;
            --metal-blue-900: #0c4a6e;
            
            /* 品牌色彩 */
            --brand-primary: #0ea5e9;
            --brand-secondary: #8b5cf6;
            --brand-tertiary: #06b6d4;
            --brand-quaternary: #3b82f6;
            
            /* 現代亮綠系列 */
            --success-50: #ecfdf5;
            --success-100: #d1fae5;
            --success-200: #a7f3d0;
            --success-300: #6ee7b7;
            --success-400: #34d399;
            --success-500: #10b981;
            --success-600: #059669;
            --success-700: #047857;
            --success-800: #065f46;
            --success-900: #064e3b;
            
            /* 高飽和科技紫 */
            --purple-50: #faf5ff;
            --purple-100: #f3e8ff;
            --purple-200: #e9d5ff;
            --purple-300: #d8b4fe;
            --purple-400: #c084fc;
            --purple-500: #a855f7;
            --purple-600: #9333ea;
            --purple-700: #7c3aed;
            --purple-800: #6b21a8;
            --purple-900: #581c87;
            
            /* 危險色系 */
            --danger-50: #fef2f2;
            --danger-100: #fee2e2;
            --danger-200: #fecaca;
            --danger-300: #fca5a5;
            --danger-400: #f87171;
            --danger-500: #ef4444;
            --danger-600: #dc2626;
            --danger-700: #b91c1c;
            --danger-800: #991b1b;
            --danger-900: #7f1d1d;
            
            /* 警告色系 */
            --warning-50: #fffbeb;
            --warning-100: #fef3c7;
            --warning-200: #fde68a;
            --warning-300: #fcd34d;
            --warning-400: #fbbf24;
            --warning-500: #f59e0b;
            --warning-600: #d97706;
            --warning-700: #b45309;
            --warning-800: #92400e;
            --warning-900: #78350f;
            
            /* 文字色彩 */
            --text-primary: #f0f6fc;
            --text-secondary: #adbac7;
            --text-tertiary: #768390;
            --text-quaternary: #545d68;
            --text-muted: #373e47;
            
            /* 邊框色彩 */
            --border-primary: #373e47;
            --border-secondary: #444c56;
            --border-tertiary: #545d68;
            --border-focus: var(--brand-primary);
            
            /* 漸變效果 */
            --gradient-brand: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-secondary) 50%, var(--brand-tertiary) 100%);
            --gradient-success: linear-gradient(135deg, var(--success-400) 0%, var(--success-600) 100%);
            --gradient-danger: linear-gradient(135deg, var(--danger-400) 0%, var(--danger-600) 100%);
            --gradient-dark: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
            --gradient-surface: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-elevated) 100%);
            
            /* 陰影系統 */
            --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
            --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            --shadow-inner: inset 0 2px 4px 0 rgba(0, 0, 0, 0.05);
            --shadow-brand: 0 10px 40px rgba(14, 165, 233, 0.15);
            --shadow-brand-lg: 0 20px 60px rgba(14, 165, 233, 0.2);
            
            /* 間距系統 */
            --space-px: 1px;
            --space-0: 0px;
            --space-0-5: 0.125rem;
            --space-1: 0.25rem;
            --space-1-5: 0.375rem;
            --space-2: 0.5rem;
            --space-2-5: 0.625rem;
            --space-3: 0.75rem;
            --space-3-5: 0.875rem;
            --space-4: 1rem;
            --space-5: 1.25rem;
            --space-6: 1.5rem;
            --space-7: 1.75rem;
            --space-8: 2rem;
            --space-9: 2.25rem;
            --space-10: 2.5rem;
            --space-11: 2.75rem;
            --space-12: 3rem;
            --space-14: 3.5rem;
            --space-16: 4rem;
            --space-20: 5rem;
            --space-24: 6rem;
            --space-28: 7rem;
            --space-32: 8rem;
            --space-36: 9rem;
            --space-40: 10rem;
            --space-44: 11rem;
            --space-48: 12rem;
            --space-52: 13rem;
            --space-56: 14rem;
            --space-60: 15rem;
            --space-64: 16rem;
            --space-72: 18rem;
            --space-80: 20rem;
            --space-96: 24rem;
            
            /* 邊框半徑 */
            --radius-none: 0px;
            --radius-sm: 0.125rem;
            --radius-default: 0.25rem;
            --radius-md: 0.375rem;
            --radius-lg: 0.5rem;
            --radius-xl: 0.75rem;
            --radius-2xl: 1rem;
            --radius-3xl: 1.5rem;
            --radius-full: 9999px;
            
            /* 字體系統 */
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            --font-mono: 'JetBrains Mono', 'Fira Code', 'Monaco', 'Consolas', monospace;
            --font-brand: 'Outfit', var(--font-sans);
            --font-display: 'Geist', var(--font-sans);
            
            /* 字體大小 */
            --text-xs: 0.75rem;
            --text-sm: 0.875rem;
            --text-base: 1rem;
            --text-lg: 1.125rem;
            --text-xl: 1.25rem;
            --text-2xl: 1.5rem;
            --text-3xl: 1.875rem;
            --text-4xl: 2.25rem;
            --text-5xl: 3rem;
            --text-6xl: 3.75rem;
            --text-7xl: 4.5rem;
            --text-8xl: 6rem;
            --text-9xl: 8rem;
            
            /* 行高 */
            --leading-none: 1;
            --leading-tight: 1.25;
            --leading-snug: 1.375;
            --leading-normal: 1.5;
            --leading-relaxed: 1.625;
            --leading-loose: 2;
            
            /* 字重 */
            --font-thin: 100;
            --font-extralight: 200;
            --font-light: 300;
            --font-normal: 400;
            --font-medium: 500;
            --font-semibold: 600;
            --font-bold: 700;
            --font-extrabold: 800;
            --font-black: 900;
            
            /* 動畫時間 */
            --duration-75: 75ms;
            --duration-100: 100ms;
            --duration-150: 150ms;
            --duration-200: 200ms;
            --duration-300: 300ms;
            --duration-500: 500ms;
            --duration-700: 700ms;
            --duration-1000: 1000ms;
            
            /* 動畫緩動 */
            --ease-linear: linear;
            --ease-in: cubic-bezier(0.4, 0, 1, 1);
            --ease-out: cubic-bezier(0, 0, 0.2, 1);
            --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* ===== 全局重置與基礎樣式 ===== */
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
            background: var(--gradient-dark) !important;
            font-family: var(--font-sans) !important;
            color: var(--text-primary) !important;
            line-height: var(--leading-relaxed);
            font-weight: var(--font-normal);
            overflow-x: hidden;
        }
        
        #MainMenu, footer, header, .stDeployButton, .stDecoration {
            display: none !important;
        }
        
        .stApp {
            background: var(--gradient-dark) !important;
            min-height: 100vh;
        }
        
        /* ===== Hero Section 設計 ===== */
        .hero-container {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: var(--space-20) var(--space-8);
            background: var(--gradient-dark);
            position: relative;
            overflow: hidden;
        }
        
        .hero-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 20%, rgba(14, 165, 233, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 40% 60%, rgba(6, 182, 212, 0.05) 0%, transparent 50%);
            z-index: 0;
            pointer-events: none;
        }
        
        .hero-content {
            position: relative;
            z-index: 10;
            max-width: 900px;
            margin: 0 auto;
        }
        
        .hero-logo-container {
            margin-bottom: var(--space-8);
            position: relative;
        }
        
        .hero-logo {
            width: 120px;
            height: 120px;
            margin: 0 auto var(--space-6);
            position: relative;
            border-radius: var(--radius-full);
            background: var(--gradient-brand);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: var(--shadow-brand-lg);
            animation: logo-pulse 3s ease-in-out infinite;
            transition: transform var(--duration-300) var(--ease-out);
        }
        
        .hero-logo:hover {
            transform: scale(1.05);
        }
        
        .hero-logo::before {
            content: '';
            position: absolute;
            top: -4px;
            left: -4px;
            right: -4px;
            bottom: -4px;
            background: var(--gradient-brand);
            border-radius: var(--radius-full);
            opacity: 0.5;
            animation: logo-spin 8s linear infinite;
            z-index: -1;
        }
        
        @keyframes logo-pulse {
            0%, 100% { 
                transform: scale(1);
                box-shadow: var(--shadow-brand-lg);
            }
            50% { 
                transform: scale(1.02);
                box-shadow: 0 25px 80px rgba(14, 165, 233, 0.3);
            }
        }
        
        @keyframes logo-spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .hero-title {
            font-family: var(--font-brand);
            font-size: clamp(var(--text-4xl), 8vw, var(--text-8xl));
            font-weight: var(--font-black);
            line-height: var(--leading-none);
            margin-bottom: var(--space-4);
            background: linear-gradient(135deg, var(--text-primary) 0%, var(--brand-primary) 50%, var(--brand-secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.02em;
        }
        
        .hero-subtitle {
            font-family: 'Noto Sans JP', var(--font-sans);
            font-size: var(--text-2xl);
            font-weight: var(--font-light);
            color: var(--text-secondary);
            margin-bottom: var(--space-6);
            letter-spacing: 0.1em;
        }
        
        .hero-tagline {
            font-size: var(--text-xl);
            color: var(--text-tertiary);
            margin-bottom: var(--space-4);
            font-weight: var(--font-medium);
            font-style: italic;
        }
        
        .hero-description {
            font-size: var(--text-lg);
            color: var(--text-tertiary);
            line-height: var(--leading-loose);
            margin-bottom: var(--space-12);
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .hero-cta {
            display: flex;
            gap: var(--space-6);
            flex-wrap: wrap;
            justify-content: center;
            margin-bottom: var(--space-12);
        }
        
        .language-switcher {
            display: flex;
            gap: var(--space-3);
            justify-content: center;
            margin-top: var(--space-8);
        }
        
        /* ===== 現代卡片設計 ===== */
        .premium-card {
            background: var(--gradient-surface);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-3xl);
            padding: var(--space-8);
            box-shadow: var(--shadow-2xl);
            transition: all var(--duration-300) var(--ease-out);
            position: relative;
            overflow: hidden;
            margin-bottom: var(--space-8);
        }
        
        .premium-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--gradient-brand);
            opacity: 0.8;
        }
        
        .premium-card:hover {
            transform: translateY(-8px);
            box-shadow: var(--shadow-brand-lg);
            border-color: var(--brand-primary);
        }
        
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: var(--space-6);
            flex-wrap: wrap;
            gap: var(--space-4);
        }
        
        .card-title {
            font-family: var(--font-brand);
            font-size: var(--text-2xl);
            font-weight: var(--font-bold);
            color: var(--text-primary);
            margin: 0;
        }
        
        .card-icon {
            width: 56px;
            height: 56px;
            border-radius: var(--radius-xl);
            background: var(--gradient-brand);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: var(--text-2xl);
            box-shadow: var(--shadow-brand);
            transition: transform var(--duration-200) var(--ease-out);
        }
        
        .card-icon:hover {
            transform: scale(1.1);
        }
        
        .card-content {
            color: var(--text-secondary);
            line-height: var(--leading-loose);
            font-size: var(--text-base);
        }
        
        /* ===== 指標卡片 ===== */
        .metric-card {
            background: var(--gradient-surface);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-2xl);
            padding: var(--space-6);
            text-align: center;
            transition: all var(--duration-300) var(--ease-out);
            box-shadow: var(--shadow-lg);
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--gradient-brand);
            opacity: 0.6;
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            border-color: var(--brand-primary);
            box-shadow: var(--shadow-brand);
        }
        
        .metric-value {
            font-family: var(--font-mono);
            font-size: var(--text-3xl);
            font-weight: var(--font-bold);
            color: var(--text-primary);
            margin-bottom: var(--space-2);
            letter-spacing: -0.01em;
        }
        
        .metric-label {
            color: var(--text-tertiary);
            font-size: var(--text-sm);
            font-weight: var(--font-semibold);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: var(--space-1);
        }
        
        .metric-change {
            font-family: var(--font-mono);
            font-size: var(--text-sm);
            font-weight: var(--font-semibold);
        }
        
        .metric-positive {
            color: var(--success-400);
        }
        
        .metric-negative {
            color: var(--danger-400);
        }
        
        .metric-neutral {
            color: var(--text-secondary);
        }
        
        /* ===== 導航系統 ===== */
        .nav-container {
            background: rgba(13, 17, 23, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-2xl);
            padding: var(--space-4) var(--space-6);
            margin-bottom: var(--space-8);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: var(--space-4);
            position: sticky;
            top: var(--space-4);
            z-index: 50;
            box-shadow: var(--shadow-xl);
        }
        
        .nav-brand {
            display: flex;
            align-items: center;
            gap: var(--space-3);
            font-family: var(--font-brand);
            font-weight: var(--font-bold);
            font-size: var(--text-xl);
            color: var(--text-primary);
        }
        
        .nav-logo {
            width: 40px;
            height: 40px;
            border-radius: var(--radius-lg);
            background: var(--gradient-brand);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: var(--font-bold);
            font-size: var(--text-lg);
            box-shadow: var(--shadow-brand);
        }
        
        .nav-links {
            display: flex;
            gap: var(--space-2);
            flex-wrap: wrap;
        }
        
        /* ===== 按鈕設計 ===== */
        .stButton > button {
            background: var(--gradient-brand) !important;
            border: none !important;
            border-radius: var(--radius-xl) !important;
            color: var(--text-primary) !important;
            font-weight: var(--font-semibold) !important;
            padding: var(--space-3) var(--space-6) !important;
            transition: all var(--duration-300) var(--ease-out) !important;
            font-family: var(--font-sans) !important;
            font-size: var(--text-base) !important;
            box-shadow: var(--shadow-brand) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .stButton > button::before {
            content: '' !important;
            position: absolute !important;
            top: 50% !important;
            left: 50% !important;
            width: 0 !important;
            height: 0 !important;
            background: rgba(255, 255, 255, 0.1) !important;
            border-radius: 50% !important;
            transform: translate(-50%, -50%) !important;
            transition: width var(--duration-300) var(--ease-out), height var(--duration-300) var(--ease-out) !important;
            z-index: 0 !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: var(--shadow-brand-lg) !important;
        }
        
        .stButton > button:hover::before {
            width: 300px !important;
            height: 300px !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) scale(0.98) !important;
        }
        
        /* 次要按鈕 */
        .stButton > button[kind="secondary"] {
            background: transparent !important;
            border: 2px solid var(--border-secondary) !important;
            color: var(--text-secondary) !important;
            box-shadow: var(--shadow-md) !important;
        }
        
        .stButton > button[kind="secondary"]:hover {
            border-color: var(--brand-primary) !important;
            color: var(--brand-primary) !important;
            background: rgba(14, 165, 233, 0.05) !important;
        }
        
        /* ===== 表單元件優化 ===== */
        .stTextInput > div > div > input,
        .stPasswordInput > div > div > input {
            background: var(--bg-elevated) !important;
            border: 2px solid var(--border-primary) !important;
            border-radius: var(--radius-lg) !important;
            color: var(--text-primary) !important;
            padding: var(--space-3) var(--space-4) !important;
            font-family: var(--font-sans) !important;
            font-size: var(--text-base) !important;
            transition: all var(--duration-200) var(--ease-out) !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stPasswordInput > div > div > input:focus {
            border-color: var(--brand-primary) !important;
            box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1) !important;
            outline: none !important;
        }
        
        .stSelectbox > div > div {
            background: var(--bg-elevated) !important;
            border: 2px solid var(--border-primary) !important;
            border-radius: var(--radius-lg) !important;
            color: var(--text-primary) !important;
            transition: all var(--duration-200) var(--ease-out) !important;
        }
        
        .stSelectbox > div > div:focus-within {
            border-color: var(--brand-primary) !important;
            box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1) !important;
        }
        
        /* ===== 登入表單設計 ===== */
        .login-container {
            max-width: 450px;
            margin: var(--space-8) auto;
            background: var(--gradient-surface);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-3xl);
            padding: var(--space-12) var(--space-8);
            box-shadow: var(--shadow-2xl);
            position: relative;
            overflow: hidden;
        }
        
        .login-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-brand);
        }
        
        .login-header {
            text-align: center;
            margin-bottom: var(--space-8);
        }
        
        .login-title {
            font-family: var(--font-brand);
            font-size: var(--text-3xl);
            font-weight: var(--font-bold);
            color: var(--text-primary);
            margin-bottom: var(--space-2);
        }
        
        .login-subtitle {
            color: var(--text-secondary);
            font-size: var(--text-lg);
            line-height: var(--leading-relaxed);
        }
        
        /* ===== 解決方案卡片 ===== */
        .solution-card {
            background: var(--gradient-surface);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-3xl);
            padding: var(--space-10);
            margin-bottom: var(--space-8);
            box-shadow: var(--shadow-2xl);
            position: relative;
            overflow: hidden;
        }
        
        .solution-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-brand);
        }
        
        .solution-theme {
            font-family: var(--font-brand);
            font-size: var(--text-3xl);
            font-weight: var(--font-bold);
            color: var(--text-primary);
            margin-bottom: var(--space-6);
            background: var(--gradient-brand);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: var(--leading-tight);
        }
        
        .solution-insight {
            color: var(--text-secondary);
            line-height: var(--leading-loose);
            margin-bottom: var(--space-8);
            font-size: var(--text-lg);
        }
        
        .target-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: var(--space-6);
            margin-bottom: var(--space-8);
        }
        
        .target-card {
            background: var(--bg-elevated);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-2xl);
            padding: var(--space-6);
            transition: all var(--duration-300) var(--ease-out);
            position: relative;
            overflow: hidden;
        }
        
        .target-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--gradient-brand);
            opacity: 0.6;
        }
        
        .target-card:hover {
            background: var(--bg-surface);
            border-color: var(--brand-primary);
            transform: translateY(-2px);
            box-shadow: var(--shadow-brand);
        }
        
        .target-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: var(--space-4);
        }
        
        .target-symbol {
            font-family: var(--font-mono);
            font-size: var(--text-xl);
            font-weight: var(--font-bold);
            color: var(--text-primary);
        }
        
        .target-type {
            font-size: var(--text-xs);
            color: var(--brand-secondary);
            font-weight: var(--font-semibold);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            background: rgba(139, 92, 246, 0.1);
            padding: var(--space-1) var(--space-2);
            border-radius: var(--radius-md);
            border: 1px solid rgba(139, 92, 246, 0.2);
        }
        
        .target-allocation {
            font-family: var(--font-mono);
            font-size: var(--text-2xl);
            font-weight: var(--font-bold);
            color: var(--success-400);
        }
        
        .target-analysis {
            color: var(--text-tertiary);
            font-size: var(--text-base);
            line-height: var(--leading-relaxed);
            margin-bottom: var(--space-4);
        }
        
        .target-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: var(--space-4);
        }
        
        .detail-item {
            text-align: center;
        }
        
        .detail-label {
            font-size: var(--text-xs);
            color: var(--text-quaternary);
            font-weight: var(--font-medium);
            margin-bottom: var(--space-1);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .detail-value {
            font-size: var(--text-sm);
            color: var(--text-primary);
            font-weight: var(--font-semibold);
        }
        
        /* ===== 免責聲明 ===== */
        .disclaimer {
            background: rgba(239, 68, 68, 0.08);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: var(--radius-xl);
            padding: var(--space-6);
            color: var(--danger-300);
            font-size: var(--text-base);
            line-height: var(--leading-relaxed);
            margin: var(--space-8) 0;
            text-align: center;
        }
        
        .disclaimer-icon {
            display: inline-block;
            margin-right: var(--space-2);
            font-size: var(--text-lg);
        }
        
        /* ===== 響應式設計 ===== */
        @media (max-width: 768px) {
            .hero-container {
                padding: var(--space-12) var(--space-4);
            }
            
            .hero-title {
                font-size: clamp(var(--text-3xl), 10vw, var(--text-5xl));
            }
            
            .hero-subtitle {
                font-size: var(--text-xl);
            }
            
            .hero-cta {
                flex-direction: column;
                align-items: center;
            }
            
            .nav-container {
                padding: var(--space-3) var(--space-4);
                flex-direction: column;
                gap: var(--space-3);
            }
            
            .nav-links {
                width: 100%;
                justify-content: center;
            }
            
            .target-grid {
                grid-template-columns: 1fr;
            }
            
            .premium-card,
            .solution-card {
                padding: var(--space-6);
                margin-bottom: var(--space-6);
            }
            
            .login-container {
                margin: var(--space-4);
                padding: var(--space-8) var(--space-6);
            }
        }
        
        @media (max-width: 480px) {
            .hero-description {
                font-size: var(--text-base);
            }
            
            .card-title {
                font-size: var(--text-xl);
            }
            
            .premium-card,
            .solution-card {
                padding: var(--space-4);
            }
            
            .metric-value {
                font-size: var(--text-2xl);
            }
        }
        
        /* ===== 滾動條美化 ===== */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--bg-secondary);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--gradient-brand);
            border-radius: var(--radius-md);
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--brand-primary);
        }
        
        /* ===== 載入動畫 ===== */
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid var(--border-primary);
            border-radius: 50%;
            border-top-color: var(--brand-primary);
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* ===== 特殊效果 ===== */
        .glow-effect {
            position: relative;
        }
        
        .glow-effect::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: inherit;
            padding: 2px;
            background: var(--gradient-brand);
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask-composite: exclude;
            opacity: 0;
            transition: opacity var(--duration-300) var(--ease-out);
        }
        
        .glow-effect:hover::after {
            opacity: 1;
        }
        
        /* ===== 資料視覺化增強 ===== */
        .chart-container {
            background: var(--gradient-surface);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-2xl);
            padding: var(--space-6);
            margin-bottom: var(--space-6);
            box-shadow: var(--shadow-lg);
        }
        
        .chart-title {
            font-family: var(--font-brand);
            font-size: var(--text-xl);
            font-weight: var(--font-semibold);
            color: var(--text-primary);
            margin-bottom: var(--space-4);
            text-align: center;
        }
        
        /* ===== 狀態指示器 ===== */
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: var(--space-2);
            padding: var(--space-1) var(--space-3);
            border-radius: var(--radius-full);
            font-size: var(--text-sm);
            font-weight: var(--font-medium);
        }
        
        .status-success {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: var(--success-400);
        }
        
        .status-warning {
            background: rgba(245, 158, 11, 0.1);
            border: 1px solid rgba(245, 158, 11, 0.2);
            color: var(--warning-400);
        }
        
        .status-danger {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: var(--danger-400);
        }
        
        .status-indicator::before {
            content: '';
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: currentColor;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        /* ===== 工具提示 ===== */
        .tooltip {
            position: relative;
            cursor: help;
        }
        
        .tooltip::after {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: var(--bg-overlay);
            color: var(--text-primary);
            padding: var(--space-2) var(--space-3);
            border-radius: var(--radius-lg);
            font-size: var(--text-sm);
            white-space: nowrap;
            opacity: 0;
            pointer-events: none;
            transition: opacity var(--duration-200) var(--ease-out);
            z-index: 100;
            border: 1px solid var(--border-primary);
            box-shadow: var(--shadow-lg);
        }
        
        .tooltip:hover::after {
            opacity: 1;
        }
        
        /* ===== 進度條 ===== */
        .progress-bar {
            width: 100%;
            height: 8px;
            background: var(--bg-tertiary);
            border-radius: var(--radius-full);
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: var(--gradient-brand);
            border-radius: var(--radius-full);
            transition: width var(--duration-500) var(--ease-out);
        }
        
        /* ===== 標籤系統 ===== */
        .tag {
            display: inline-flex;
            align-items: center;
            gap: var(--space-1);
            padding: var(--space-1) var(--space-2);
            border-radius: var(--radius-md);
            font-size: var(--text-xs);
            font-weight: var(--font-medium);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .tag-primary {
            background: rgba(14, 165, 233, 0.1);
            border: 1px solid rgba(14, 165, 233, 0.2);
            color: var(--brand-primary);
        }
        
        .tag-success {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: var(--success-400);
        }
        
        .tag-warning {
            background: rgba(245, 158, 11, 0.1);
            border: 1px solid rgba(245, 158, 11, 0.2);
            color: var(--warning-400);
        }
        
        .tag-danger {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: var(--danger-400);
        }
    </style>
    """, unsafe_allow_html=True)

# ====== 市場數據系統 ======
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
                volume = float(hist['Volume'].iloc[-1]) if not hist['Volume'].isna().iloc[-1] else 0
                return {
                    'symbol': symbol,
                    'price': current,
                    'change': change,
                    'change_pct': change_pct,
                    'volume': volume
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

# ====== 圖表生成系統 ======
def create_market_chart(market_data):
    """創建市場概況圖表"""
    if not market_data:
        return None
    
    symbols = list(market_data.keys())
    prices = [market_data[symbol]['price'] for symbol in symbols]
    changes = [market_data[symbol]['change_pct'] for symbol in symbols]
    
    colors = ['#10b981' if change >= 0 else '#ef4444' for change in changes]
    
    fig = go.Figure(data=[
        go.Bar(
            x=symbols,
            y=changes,
            marker_color=colors,
            marker_line_color='rgba(255,255,255,0.1)',
            marker_line_width=1,
            text=[f'{change:+.2f}%' for change in changes],
            textposition='outside',
            textfont=dict(
                family='JetBrains Mono',
                size=12,
                color='#f0f6fc'
            )
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='市場表現概況',
            font=dict(
                family='Outfit',
                size=20,
                color='#f0f6fc',
                weight='bold'
            ),
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Inter',
            color='#adbac7'
        ),
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            tickfont=dict(size=12, color='#adbac7')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(173, 186, 199, 0.1)',
            showline=False,
            zeroline=True,
            zerolinecolor='rgba(173, 186, 199, 0.3)',
            tickfont=dict(size=12, color='#adbac7'),
            title=dict(
                text='變化 (%)',
                font=dict(size=14, color='#adbac7')
            )
        ),
        height=400,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig

def create_portfolio_chart(portfolio_data):
    """創建投資組合餅圖"""
    if not portfolio_data:
        return None
    
    symbols = [item['symbol'] for item in portfolio_data]
    values = [item['quantity'] * item['current_price'] for item in portfolio_data]
    
    # 使用品牌色彩方案
    colors = ['#0ea5e9', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444', '#06b6d4', '#84cc16', '#f97316']
    
    fig = go.Figure(data=[
        go.Pie(
            labels=symbols,
            values=values,
            hole=0.4,
            marker=dict(
                colors=colors[:len(symbols)],
                line=dict(color='#21262d', width=2)
            ),
            textfont=dict(
                family='Inter',
                size=12,
                color='#f0f6fc'
            ),
            textinfo='label+percent',
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='投資組合配置',
            font=dict(
                family='Outfit',
                size=20,
                color='#f0f6fc',
                weight='bold'
            ),
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Inter',
            color='#adbac7'
        ),
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        showlegend=True,
        legend=dict(
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=1.05,
            font=dict(
                size=12,
                color='#adbac7'
            )
        )
    )
    
    return fig

# ====== 投資解決方案系統 ======
def generate_solution(risk_pref, investment_goal):
    """生成投資解決方案"""
    solutions_db = {
        ('conservative', 'income'): {
            'theme': '2025年防禦型收益投資策略',
            'insight': '在當前市場環境下，專注於穩定收益資產配置。美國長期公債和高評級企業債券提供相對穩定的收益來源，同時高股息股票和REIT基金可提供持續現金流。建議採用分散配置策略，降低單一資產風險，並關注利率政策變化對債券價格的影響。',
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
            ],
            'risk_factors': ['利率風險', '通脹風險', '流動性風險', '信用風險'],
            'monitoring_indicators': ['10年期美債收益率', 'Fed利率政策', '通膨數據CPI', 'REITs利率敏感性']
        },
        
        ('moderate', 'balanced'): {
            'theme': '2025年AI科技平衡配置策略',
            'insight': '人工智慧革命正在重塑各個行業，但市場波動性增加。建議平衡配置科技龍頭股、成長型ETF和防禦性資產，在追求成長的同時控制風險。重點關注AI產業鏈上下游機會，同時保持適度的債券配置作為緩衝，以應對市場波動。',
            'targets': [
                {
                    'symbol': 'QQQ',
                    'type': '科技ETF',
                    'allocation': 30,
                    'entry_point': '回調至$380以下',
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
            ],
            'risk_factors': ['科技股波動', '利率變化', '市場系統風險', 'AI泡沫風險'],
            'monitoring_indicators': ['AI產業發展', '科技股估值水準', 'Fed政策變化', 'VIX恐慌指數']
        },
        
        ('aggressive', 'growth'): {
            'theme': '2025年積極成長科技投資攻略',
            'insight': '積極型投資者可重點佈局具有顛覆性創新潛力的成長股。AI、雲端運算、電動車、生技等領域仍有巨大成長空間，但需承擔相應的高波動風險。建議集中投資於具有強勁基本面和清晰成長路徑的龍頭企業，並密切關注技術創新進展。',
            'targets': [
                {
                    'symbol': 'ARKK',
                    'type': '創新ETF',
                    'allocation': 25,
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
                    'allocation': 25,
                    'entry_point': '產業週期低點進入',
                    'exit_point': '產業週期高點',
                    'expected_return': '18-25%',
                    'analysis': '半導體產業ETF，AI基礎設施建設的核心受惠標的，週期性成長強勁'
                }
            ],
            'risk_factors': ['高波動性', '估值風險', '產業週期風險', '監管政策風險'],
            'monitoring_indicators': ['科技創新進展', '市場情緒指標', '成長股估值水準', '產業政策變化']
        }
    }
    
    key = (risk_pref, investment_goal)
    if key in solutions_db:
        return solutions_db[key]
    else:
        return solutions_db[('moderate', 'balanced')]

# ====== 頁面函數 ======
def show_landing_page():
    """顯示Landing Page"""
    t = TEXTS[st.session_state.language]
    logo_html = get_logo_html()
    
    st.markdown(f"""
    <div class="hero-container">
        <div class="hero-content">
            <div class="hero-logo-container">
                <div class="hero-logo">
                    {logo_html}
                </div>
                <h1 class="hero-title">TENKI</h1>
                <p class="hero-subtitle">{t['app_subtitle']}</p>
            </div>
            
            <p class="hero-tagline">{t['slogan']}</p>
            <div class="hero-description">
                專業投資決策支援平台 • 運用AI智能分析市場趨勢 • 在關鍵轉折點做出理想決策 • 實現資產穩健增值
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 語言切換和CTA
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        lang_col1, lang_col2 = st.columns(2)
        
        with lang_col1:
            if st.button("🇹🇼 繁體中文", key="lang_zh", use_container_width=True, 
                        type="primary" if st.session_state.language == 'zh' else "secondary"):
                st.session_state.language = 'zh'
                st.rerun()
        
        with lang_col2:
            if st.button("🇺🇸 English", key="lang_en", use_container_width=True,
                        type="primary" if st.session_state.language == 'en' else "secondary"):
                st.session_state.language = 'en'
                st.rerun()
        
        st.markdown("---")
        
        if st.button(f"🚀 {t['get_started']}", key="get_started", use_container_width=True, type="primary"):
            st.session_state.current_page = 'login'
            st.rerun()
    
    # 核心功能展示
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-header">
            <h2 class="card-title">{t['features_title']}</h2>
            <div class="card-icon">⭐</div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: var(--space-8); margin-top: var(--space-6);">
            <div style="text-align: center; padding: var(--space-6); background: var(--bg-elevated); border-radius: var(--radius-2xl); border: 1px solid var(--border-primary); transition: all var(--duration-300) var(--ease-out);" class="glow-effect">
                <div style="font-size: var(--text-4xl); margin-bottom: var(--space-4);">🤖</div>
                <h3 style="color: var(--text-primary); margin-bottom: var(--space-2); font-family: var(--font-brand); font-weight: var(--font-semibold);">{t['ai_insights']}</h3>
                <p style="color: var(--text-secondary); line-height: var(--leading-relaxed);">{t['ai_insights_desc']}</p>
            </div>
            
            <div style="text-align: center; padding: var(--space-6); background: var(--bg-elevated); border-radius: var(--radius-2xl); border: 1px solid var(--border-primary); transition: all var(--duration-300) var(--ease-out);" class="glow-effect">
                <div style="font-size: var(--text-4xl); margin-bottom: var(--space-4);">💼</div>
                <h3 style="color: var(--text-primary); margin-bottom: var(--space-2); font-family: var(--font-brand); font-weight: var(--font-semibold);">{t['portfolio_management']}</h3>
                <p style="color: var(--text-secondary); line-height: var(--leading-relaxed);">{t['portfolio_management_desc']}</p>
            </div>
            
            <div style="text-align: center; padding: var(--space-6); background: var(--bg-elevated); border-radius: var(--radius-2xl); border: 1px solid var(--border-primary); transition: all var(--duration-300) var(--ease-out);" class="glow-effect">
                <div style="font-size: var(--text-4xl); margin-bottom: var(--space-4);">📊</div>
                <h3 style="color: var(--text-primary); margin-bottom: var(--space-2); font-family: var(--font-brand); font-weight: var(--font-semibold);">{t['real_time_data']}</h3>
                <p style="color: var(--text-secondary); line-height: var(--leading-relaxed);">{t['real_time_data_desc']}</p>
            </div>
            
            <div style="text-align: center; padding: var(--space-6); background: var(--bg-elevated); border-radius: var(--radius-2xl); border: 1px solid var(--border-primary); transition: all var(--duration-300) var(--ease-out);" class="glow-effect">
                <div style="font-size: var(--text-4xl); margin-bottom: var(--space-4);">🛡️</div>
                <h3 style="color: var(--text-primary); margin-bottom: var(--space-2); font-family: var(--font-brand); font-weight: var(--font-semibold);">{t['risk_control']}</h3>
                <p style="color: var(--text-secondary); line-height: var(--leading-relaxed);">{t['risk_control_desc']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 免責聲明
    st.markdown(f"""
    <div class="disclaimer">
        <span class="disclaimer-icon">⚠️</span>
        {t['disclaimer']}
    </div>
    """, unsafe_allow_html=True)

def show_login_page():
    """顯示登入頁面"""
    t = TEXTS[st.session_state.language]
    logo_html = get_logo_html()
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f"""
        <div class="login-container">
            <div class="login-header">
                <div style="margin-bottom: var(--space-4);">
                    {logo_html}
                </div>
                <h1 class="login-title">TENKI</h1>
                <p class="login-subtitle">{t['tagline']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 登入表單
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input(t['email'], placeholder="your@email.com", key="login_email")
            password = st.text_input(t['password'], type="password", placeholder="••••••••", key="login_password")
            
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
        
        st.markdown('</div>', unsafe_allow_html=True)

def create_navigation():
    """創建導航系統"""
    t = TEXTS[st.session_state.language]
    logo_html = get_logo_html()
    
    st.markdown(f"""
    <div class="nav-container">
        <div class="nav-brand">
            {logo_html}
            <span>TENKI</span>
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
    """顯示儀表板"""
    t = TEXTS[st.session_state.language]
    
    # 歡迎標題
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-header">
            <h1 class="card-title">{t['welcome']}, {st.session_state.user_email.split('@')[0]}! 🎉</h1>
            <div class="status-indicator status-success">
                投資就緒
            </div>
        </div>
        <div class="card-content">
            準備好開始您今天的投資之旅了嗎？讓我們一起在市場的關鍵轉折點中，做出理想的投資決策。
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 績效指標
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t['today_pnl']}</div>
            <div class="metric-value metric-positive">+$1,234</div>
            <div class="metric-change metric-positive">+2.3% 今日</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t['total_return']}</div>
            <div class="metric-value metric-positive">+$12,567</div>
            <div class="metric-change metric-positive">+15.6% 總計</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t['win_rate']}</div>
            <div class="metric-value metric-neutral">68.5%</div>
            <div class="metric-change metric-positive">↗ 持續提升</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t['risk_level']}</div>
            <div class="metric-value metric-positive">低風險</div>
            <div class="metric-change metric-neutral">波動率: 12.3%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 市場數據與圖表
    with st.spinner(f"{t['loading']}"):
        market_data = get_market_data()
    
    if market_data:
        # 市場概況卡片
        st.markdown(f"""
        <div class="premium-card">
            <div class="card-header">
                <h2 class="card-title">📊 {t['market_overview']}</h2>
                <div class="tag tag-primary">即時更新</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 市場圖表
        chart = create_market_chart(market_data)
        if chart:
            st.plotly_chart(chart, use_container_width=True)
        
        # 市場數據表格
        cols = st.columns(len(market_data))
        for i, (symbol, data) in enumerate(market_data.items()):
            with cols[i]:
                change_class = "metric-positive" if data['change_pct'] >= 0 else "metric-negative"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{symbol}</div>
                    <div class="metric-value">${data['price']:.2f}</div>
                    <div class="metric-change {change_class}">{data['change']:+.2f} ({data['change_pct']:+.2f}%)</div>
                </div>
                """, unsafe_allow_html=True)
    
    # 快速操作
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-header">
            <h2 class="card-title">⚡ 快速操作</h2>
            <div class="card-icon">🚀</div>
        </div>
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
    """顯示自動導航模式"""
    t = TEXTS[st.session_state.language]
    
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-header">
            <h1 class="card-title">🧭 {t['auto_navigation']}</h1>
            <div class="card-icon">🎯</div>
        </div>
        <div class="card-content">
            根據您的投資偏好和目標，為您提供個性化的投資建議。我們的AI系統將分析您的風險承受能力和投資目標，生成最適合的投資組合配置。
        </div>
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
    
    # 當前設定摘要
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-header">
            <h3 class="card-title">⚙️ 當前設定摘要</h3>
            <div class="tag tag-success">已配置</div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-8); margin-top: var(--space-6);">
            <div style="text-align: center; padding: var(--space-6); background: var(--bg-elevated); border-radius: var(--radius-xl); border: 1px solid var(--border-primary);">
                <div style="color: var(--text-tertiary); font-size: var(--text-sm); margin-bottom: var(--space-2); font-weight: var(--font-medium); text-transform: uppercase; letter-spacing: 0.05em;">{t['risk_preference']}</div>
                <div style="color: var(--text-primary); font-weight: var(--font-semibold); font-size: var(--text-xl); font-family: var(--font-brand);">
                    {t['conservative'] if risk_pref == 'conservative' else t['moderate'] if risk_pref == 'moderate' else t['aggressive']}
                </div>
                <div style="margin-top: var(--space-2);">
                    <span class="tag tag-{'success' if risk_pref == 'conservative' else 'warning' if risk_pref == 'moderate' else 'danger'}">
                        {'低風險' if risk_pref == 'conservative' else '中風險' if risk_pref == 'moderate' else '高風險'}
                    </span>
                </div>
            </div>
            <div style="text-align: center; padding: var(--space-6); background: var(--bg-elevated); border-radius: var(--radius-xl); border: 1px solid var(--border-primary);">
                <div style="color: var(--text-tertiary); font-size: var(--text-sm); margin-bottom: var(--space-2); font-weight: var(--font-medium); text-transform: uppercase; letter-spacing: 0.05em;">{t['investment_goal']}</div>
                <div style="color: var(--text-primary); font-weight: var(--font-semibold); font-size: var(--text-xl); font-family: var(--font-brand);">
                    {t['income'] if invest_goal == 'income' else t['balanced'] if invest_goal == 'balanced' else t['growth']}
                </div>
                <div style="margin-top: var(--space-2);">
                    <span class="tag tag-primary">
                        {'收益優先' if invest_goal == 'income' else '平衡配置' if invest_goal == 'balanced' else '成長優先'}
                    </span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_solution_generator():
    """顯示解決方案生成器"""
    t = TEXTS[st.session_state.language]
    
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-header">
            <h1 class="card-title">⚡ {t['solution_generator']}</h1>
            <div class="card-icon">🎯</div>
        </div>
        <div class="card-content">
            基於AI分析和專家洞察，為您生成個性化投資解決方案。我們的系統會根據當前市場環境、您的風險偏好和投資目標，提供詳細的投資建議和具體行動計劃。
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.generated_solutions:
        solution = st.session_state.generated_solutions[0]
        
        # 解決方案主卡片
        st.markdown(f"""
        <div class="solution-card">
            <h2 class="solution-theme">🎯 {solution['theme']}</h2>
            <div class="solution-insight">{solution['insight']}</div>
            
            <div style="margin-bottom: var(--space-8);">
                <h3 style="color: var(--text-primary); margin-bottom: var(--space-6); font-family: var(--font-brand); font-size: var(--text-2xl); font-weight: var(--font-semibold);">💡 {t['expert_insights']}</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: var(--space-6);">
                    <div style="text-align: center; padding: var(--space-6); background: rgba(14, 165, 233, 0.08); border: 1px solid rgba(14, 165, 233, 0.2); border-radius: var(--radius-xl);">
                        <div style="color: var(--brand-primary); font-weight: var(--font-semibold); margin-bottom: var(--space-2); font-size: var(--text-lg);">市場機會</div>
                        <div style="color: var(--success-400); font-weight: var(--font-semibold);">AI科技革命浪潮</div>
                    </div>
                    <div style="text-align: center; padding: var(--space-6); background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.2); border-radius: var(--radius-xl);">
                        <div style="color: var(--warning-400); font-weight: var(--font-semibold); margin-bottom: var(--space-2); font-size: var(--text-lg);">風險等級</div>
                        <div style="color: var(--warning-400); font-weight: var(--font-semibold);">中等風險</div>
                    </div>
                    <div style="text-align: center; padding: var(--space-6); background: rgba(139, 92, 246, 0.08); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: var(--radius-xl);">
                        <div style="color: var(--brand-secondary); font-weight: var(--font-semibold); margin-bottom: var(--space-2); font-size: var(--text-lg);">建議時程</div>
                        <div style="color: var(--brand-secondary); font-weight: var(--font-semibold);">6-12個月</div>
                    </div>
                </div>
            </div>
            
            <h3 style="color: var(--text-primary); margin-bottom: var(--space-6); font-family: var(--font-brand); font-size: var(--text-2xl); font-weight: var(--font-semibold);">📊 {t['recommended_targets']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # 建議標的卡片
        st.markdown('<div class="target-grid">', unsafe_allow_html=True)
        
        for target in solution['targets']:
            st.markdown(f"""
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
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 風險分析和監控指標
        st.markdown(f"""
        <div class="premium-card">
            <h3 style="color: var(--text-primary); margin-bottom: var(--space-6); font-family: var(--font-brand); font-size: var(--text-2xl); font-weight: var(--font-semibold);">📋 {t['action_plan']}</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: var(--space-6);">
                <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: var(--radius-xl); padding: var(--space-6);">
                    <div style="color: var(--danger-400); font-weight: var(--font-semibold); margin-bottom: var(--space-4); display: flex; align-items: center; gap: var(--space-2); font-size: var(--text-lg);">
                        <span>⚠️</span> 風險監控
                    </div>
                    <ul style="color: var(--text-secondary); font-size: var(--text-base); margin: 0; padding-left: var(--space-5); line-height: var(--leading-relaxed);">
                        {"".join([f"<li style='margin-bottom: var(--space-2);'>{risk}</li>" for risk in solution['risk_factors']])}
                    </ul>
                </div>
                <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: var(--radius-xl); padding: var(--space-6);">
                    <div style="color: var(--success-400); font-weight: var(--font-semibold); margin-bottom: var(--space-4); display: flex; align-items: center; gap: var(--space-2); font-size: var(--text-lg);">
                        <span>📊</span> 監控指標
                    </div>
                    <ul style="color: var(--text-secondary); font-size: var(--text-base); margin: 0; padding-left: var(--space-5); line-height: var(--leading-relaxed);">
                        {"".join([f"<li style='margin-bottom: var(--space-2);'>{indicator}</li>" for indicator in solution['monitoring_indicators']])}
                    </ul>
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
        <div class="premium-card">
            <div style="text-align: center; padding: var(--space-12);">
                <div style="font-size: var(--text-8xl); margin-bottom: var(--space-6);">🎯</div>
                <h2 style="color: var(--text-primary); font-size: var(--text-3xl); font-weight: var(--font-semibold); margin-bottom: var(--space-4); font-family: var(--font-brand);">
                    尚無生成的投資解決方案
                </h2>
                <p style="color: var(--text-secondary); margin-bottom: var(--space-8); line-height: var(--leading-loose); font-size: var(--text-lg);">
                    請先前往自動導航模式設定您的投資偏好，<br/>
                    我們將為您生成專業的投資建議
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🧭 前往自動導航設定", key="goto_nav", use_container_width=True, type="primary"):
            st.session_state.current_page = 'auto_navigation'
            st.rerun()

def show_virtual_portfolio():
    """顯示虛擬投資組合"""
    t = TEXTS[st.session_state.language]
    
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-header">
            <h1 class="card-title">💼 {t['virtual_portfolio']}</h1>
            <div class="card-icon">📈</div>
        </div>
        <div class="card-content">
            無風險的虛擬交易環境，驗證您的投資策略。在這裡您可以模擬真實的投資操作，追蹤績效表現，並在實際投資前測試您的策略。
        </div>
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
                <div class="metric-label">{t['portfolio_value']}</div>
                <div class="metric-value">${total_value:,.0f}</div>
                <div style="color: var(--text-tertiary); font-size: var(--text-xs); margin-top: var(--space-1);">投入成本: ${total_cost:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            pnl_class = "metric-positive" if total_pnl >= 0 else "metric-negative"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{t['total_return']}</div>
                <div class="metric-value {pnl_class}">${total_pnl:+,.0f}</div>
                <div class="metric-change {pnl_class}">{total_return_pct:+.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            win_count = sum(1 for item in st.session_state.virtual_portfolio if item['current_price'] > item['entry_price'])
            win_rate = (win_count / len(st.session_state.virtual_portfolio)) * 100
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{t['win_rate']}</div>
                <div class="metric-value metric-positive">{win_rate:.1f}%</div>
                <div style="color: var(--text-tertiary); font-size: var(--text-xs); margin-top: var(--space-1);">{win_count}/{len(st.session_state.virtual_portfolio)} 獲利</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">持倉數量</div>
                <div class="metric-value metric-neutral">{len(st.session_state.virtual_portfolio)}</div>
                <div style="color: var(--text-tertiary); font-size: var(--text-xs); margin-top: var(--space-1);">檔標的</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 投資組合圖表
        chart = create_portfolio_chart(st.session_state.virtual_portfolio)
        if chart:
            st.plotly_chart(chart, use_container_width=True)
        
        # 持倉明細
        st.markdown("### 📊 持倉明細")
        for i, item in enumerate(st.session_state.virtual_portfolio):
            pnl = (item['current_price'] - item['entry_price']) * item['quantity']
            pnl_pct = ((item['current_price'] - item['entry_price']) / item['entry_price'] * 100) if item['entry_price'] > 0 else 0
            pnl_color = "var(--success-400)" if pnl >= 0 else "var(--danger-400)"
            
            st.markdown(f"""
            <div class="premium-card" style="padding: var(--space-6); margin-bottom: var(--space-4);">
                <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: var(--space-4); align-items: center;">
                    <div>
                        <div style="font-family: var(--font-mono); font-weight: var(--font-bold); font-size: var(--text-xl); color: var(--text-primary); margin-bottom: var(--space-1);">{item['symbol']}</div>
                        <div style="color: var(--text-tertiary); font-size: var(--text-sm);">{item['quantity']:.0f} 股</div>
                        <div style="margin-top: var(--space-2);">
                            <span class="tag tag-primary">持有中</span>
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: var(--text-primary); font-weight: var(--font-semibold); font-size: var(--text-lg);">${item['entry_price']:.2f}</div>
                        <div style="color: var(--text-tertiary); font-size: var(--text-xs); margin-top: var(--space-1);">買入價</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: var(--text-primary); font-weight: var(--font-semibold); font-size: var(--text-lg);">${item['current_price']:.2f}</div>
                        <div style="color: var(--text-tertiary); font-size: var(--text-xs); margin-top: var(--space-1);">現價</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-family: var(--font-mono); font-weight: var(--font-bold); color: {pnl_color}; font-size: var(--text-lg);">${pnl:+,.0f}</div>
                        <div style="font-family: var(--font-mono); font-weight: var(--font-semibold); color: {pnl_color}; font-size: var(--text-sm);">{pnl_pct:+.2f}%</div>
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
        <div class="premium-card">
            <div style="text-align: center; padding: var(--space-12);">
                <div style="font-size: var(--text-8xl); margin-bottom: var(--space-6);">💼</div>
                <h2 style="color: var(--text-primary); font-size: var(--text-3xl); font-weight: var(--font-semibold); margin-bottom: var(--space-4); font-family: var(--font-brand);">
                    您的虛擬投資組合是空的
                </h2>
                <p style="color: var(--text-secondary); margin-bottom: var(--space-8); line-height: var(--leading-loose); font-size: var(--text-lg);">
                    透過解決方案生成器建立您的第一個投資組合，<br/>
                    開始無風險的投資策略驗證
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚡ 前往解決方案生成器", key="goto_solution", use_container_width=True, type="primary"):
            st.session_state.current_page = 'solution_generator'
            st.rerun()

def show_subscription():
    """顯示訂閱管理"""
    t = TEXTS[st.session_state.language]
    
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-header">
            <h1 class="card-title">💳 {t['my_subscription']}</h1>
            <div class="card-icon">⭐</div>
        </div>
        <div class="card-content">
            管理您的訂閱方案和付款設定。享受專業級投資分析工具和個性化服務。
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 訂閱狀態
    st.markdown(f"""
    <div class="premium-card">
        <div style="margin-bottom: var(--space-6);">
            <div class="status-indicator status-success" style="font-size: var(--text-base); padding: var(--space-2) var(--space-4);">
                訂閱有效
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: var(--space-6); margin: var(--space-8) 0;">
            <div style="text-align: center; padding: var(--space-6); background: var(--bg-elevated); border-radius: var(--radius-2xl); border: 1px solid var(--border-primary);">
                <div style="color: var(--text-tertiary); font-size: var(--text-sm); margin-bottom: var(--space-2); font-weight: var(--font-medium); text-transform: uppercase; letter-spacing: 0.05em;">當前方案</div>
                <div style="color: var(--text-primary); font-size: var(--text-2xl); font-weight: var(--font-bold); margin-bottom: var(--space-2); font-family: var(--font-mono);">{t['monthly_plan']}</div>
                <div style="color: var(--success-400); font-size: var(--text-sm);">✅ 無限制使用所有功能</div>
            </div>
            <div style="text-align: center; padding: var(--space-6); background: var(--bg-elevated); border-radius: var(--radius-2xl); border: 1px solid var(--border-primary);">
                <div style="color: var(--text-tertiary); font-size: var(--text-sm); margin-bottom: var(--space-2); font-weight: var(--font-medium); text-transform: uppercase; letter-spacing: 0.05em;">{t['next_billing']}</div>
                <div style="color: var(--text-primary); font-size: var(--text-lg); font-weight: var(--font-semibold); margin-bottom: var(--space-2);">2025年11月22日</div>
                <div style="color: var(--text-tertiary); font-size: var(--text-sm);">自動續訂</div>
            </div>
            <div style="text-align: center; padding: var(--space-6); background: var(--bg-elevated); border-radius: var(--radius-2xl); border: 1px solid var(--border-primary);">
                <div style="color: var(--text-tertiary); font-size: var(--text-sm); margin-bottom: var(--space-2); font-weight: var(--font-medium); text-transform: uppercase; letter-spacing: 0.05em;">{t['payment_method']}</div>
                <div style="color: var(--text-primary); font-size: var(--text-lg); font-weight: var(--font-semibold); margin-bottom: var(--space-2); font-family: var(--font-mono);">•••• •••• •••• 1234</div>
                <div style="color: var(--text-tertiary); font-size: var(--text-sm);">Visa 信用卡</div>
            </div>
        </div>
        
        <div style="margin-top: var(--space-8);">
            <h3 style="color: var(--text-primary); margin-bottom: var(--space-6); font-family: var(--font-brand); font-size: var(--text-xl); font-weight: var(--font-semibold);">📋 訂閱功能</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: var(--space-4);">
                <div style="display: flex; align-items: center; gap: var(--space-3); padding: var(--space-4); background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: var(--radius-lg);">
                    <div style="color: var(--success-400); font-size: var(--text-xl);">✅</div>
                    <div style="color: var(--text-secondary); font-size: var(--text-base);">無限制解決方案生成</div>
                </div>
                <div style="display: flex; align-items: center; gap: var(--space-3); padding: var(--space-4); background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: var(--radius-lg);">
                    <div style="color: var(--success-400); font-size: var(--text-xl);">✅</div>
                    <div style="color: var(--text-secondary); font-size: var(--text-base);">專家投資組合追蹤</div>
                </div>
                <div style="display: flex; align-items: center; gap: var(--space-3); padding: var(--space-4); background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: var(--radius-lg);">
                    <div style="color: var(--success-400); font-size: var(--text-xl);">✅</div>
                    <div style="color: var(--text-secondary); font-size: var(--text-base);">即時市場數據推送</div>
                </div>
                <div style="display: flex; align-items: center; gap: var(--space-3); padding: var(--space-4); background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: var(--radius-lg);">
                    <div style="color: var(--success-400); font-size: var(--text-xl);">✅</div>
                    <div style="color: var(--text-secondary); font-size: var(--text-base);">個性化投資建議</div>
                </div>
                <div style="display: flex; align-items: center; gap: var(--space-3); padding: var(--space-4); background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: var(--radius-lg);">
                    <div style="color: var(--success-400); font-size: var(--text-xl);">✅</div>
                    <div style="color: var(--text-secondary); font-size: var(--text-base);">風險管理工具</div>
                </div>
                <div style="display: flex; align-items: center; gap: var(--space-3); padding: var(--space-4); background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: var(--radius-lg);">
                    <div style="color: var(--success-400); font-size: var(--text-xl);">✅</div>
                    <div style="color: var(--text-secondary); font-size: var(--text-base);">24/7 客戶支援</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 使用統計
    st.markdown("### 📊 使用統計")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t['solution_count']}</div>
            <div class="metric-value metric-positive">23</div>
            <div style="color: var(--text-tertiary); font-size: var(--text-xs); margin-top: var(--space-1);">本月使用次數</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t['portfolio_count']}</div>
            <div class="metric-value metric-positive">156</div>
            <div style="color: var(--text-tertiary); font-size: var(--text-xs); margin-top: var(--space-1);">累計建立組合數</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t['usage_days']}</div>
            <div class="metric-value metric-positive">47</div>
            <div style="color: var(--text-tertiary); font-size: var(--text-xs); margin-top: var(--space-1);">天（累計登入）</div>
        </div>
        """, unsafe_allow_html=True)

def show_settings():
    """顯示設定頁面"""
    t = TEXTS[st.session_state.language]
    
    st.markdown(f"""
    <div class="premium-card">
        <div class="card-header">
            <h1 class="card-title">⚙️ {t['settings']}</h1>
            <div class="card-icon">🛠️</div>
        </div>
        <div class="card-content">
            個性化您的TENKI體驗設定，調整語言偏好、投資風格和通知設定。
        </div>
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
    
    # 通知設定
    st.markdown("### 🔔 通知設定")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        email_notifications = st.checkbox("📧 電子郵件通知", value=True, key="email_notif")
    with col2:
        push_notifications = st.checkbox("📱 推播通知", value=True, key="push_notif")
    with col3:
        sms_notifications = st.checkbox("📞 簡訊通知", value=False, key="sms_notif")

# ====== 主應用程式 ======
def main():
    """TENKI頂級主程式"""
    
    # 初始化
    init_session_state()
    load_premium_css()
    
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
            <span class="disclaimer-icon">⚠️</span>
            {t['disclaimer']}
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
