import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import time
import requests
import json
from concurrent.futures import ThreadPoolExecutor
import plotly.graph_objects as go
import plotly.express as px
import pytz
import base64
from PIL import Image
import io
import hashlib

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
        "app_description": "專業投資決策支援平台",
        "slogan": "Turning Insight into Opportunity",
        "tagline": "將洞察力轉化為機會",
        "hero_title": "在關鍵轉折點",
        "hero_subtitle": "做出理想決策",
        "hero_cta": "開始投資旅程",
        "login": "登入",
        "register": "註冊", 
        "get_started": "立即開始",
        "learn_more": "了解更多",
        "email": "電子郵件",
        "password": "密碼",
        "forgot_password": "忘記密碼？",
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
        "virtual_trading": "模擬交易",
        "portfolio_performance": "績效追蹤",
        "expert_portfolio": "專家虛擬倉",
        "real_time_quotes": "即時報價",
        "subscription_status": "訂閱狀態",
        "next_billing": "下次計費",
        "payment_method": "付款方式",
        "cancel_subscription": "取消訂閱",
        "monthly_plan": "$22 美元/月",
        "risk_preference": "風險偏好",
        "investment_goal": "投資目標",
        "conservative": "保守型",
        "moderate": "穩健型", 
        "aggressive": "積極型",
        "growth": "成長導向",
        "income": "收益導向",
        "balanced": "平衡配置",
        "us_stocks": "美股",
        "bonds": "債券",
        "futures": "期貨",
        "funds": "基金",
        "disclaimer": "免責聲明：本平台提供的資訊僅供參考，不構成任何投資建議。投資有風險，請謹慎決策。",
        "logout": "登出",
        "welcome": "歡迎回來",
        "today_pnl": "今日損益",
        "total_return": "總報酬",
        "win_rate": "勝率",
        "loading": "載入中...",
        "generate_solution": "生成解決方案",
        "market_opportunity": "市場機會",
        "risk_analysis": "風險分析",
        "entry_point": "進場點位",
        "exit_point": "出場點位",
        "expected_return": "預期報酬",
        "allocation_ratio": "配置比例",
        "monitoring_indicators": "觀察指標",
        "buy": "買入",
        "sell": "賣出",
        "quantity": "數量",
        "current_price": "當前價格",
        "pnl": "損益",
        "change": "漲跌",
        "volume": "成交量",
        "features_title": "核心功能",
        "ai_insights": "AI智能分析",
        "ai_insights_desc": "運用人工智慧分析市場趨勢，提供個性化投資建議",
        "portfolio_management": "投資組合管理",
        "portfolio_management_desc": "專業的虛擬交易系統，零風險驗證投資策略",
        "real_time_data": "即時市場數據",
        "real_time_data_desc": "同步全球金融市場，掌握投資先機",
        "risk_control": "智能風險控制",
        "risk_control_desc": "多層次風險評估，保護您的投資安全",
        "pricing_title": "訂閱方案",
        "free_plan": "免費試用",
        "premium_plan": "專業版",
        "contact_us": "聯絡我們",
        "about_us": "關於我們",
        "privacy_policy": "隱私政策",
        "terms_of_service": "服務條款"
    },
    "en": {
        "app_name": "TENKI",
        "app_subtitle": "転機", 
        "app_description": "Professional Investment Decision Support Platform",
        "slogan": "Turning Insight into Opportunity",
        "tagline": "Transform Market Intelligence into Investment Success",
        "hero_title": "At Critical Turning Points",
        "hero_subtitle": "Make Informed Decisions",
        "hero_cta": "Start Your Journey",
        "login": "Login",
        "register": "Register",
        "get_started": "Get Started",
        "learn_more": "Learn More",
        "email": "Email",
        "password": "Password",
        "forgot_password": "Forgot Password?",
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
        "virtual_trading": "Virtual Trading",
        "portfolio_performance": "Portfolio Performance",
        "expert_portfolio": "Expert Portfolio",
        "real_time_quotes": "Real-time Quotes",
        "subscription_status": "Subscription Status",
        "next_billing": "Next Billing",
        "payment_method": "Payment Method",
        "cancel_subscription": "Cancel Subscription",
        "monthly_plan": "$22 USD/month",
        "risk_preference": "Risk Preference",
        "investment_goal": "Investment Goal",
        "conservative": "Conservative",
        "moderate": "Moderate",
        "aggressive": "Aggressive",
        "growth": "Growth-Oriented",
        "income": "Income-Oriented",
        "balanced": "Balanced",
        "us_stocks": "US Stocks",
        "bonds": "Bonds",
        "futures": "Futures",
        "funds": "Funds",
        "disclaimer": "Disclaimer: Information provided is for reference only, not investment advice. Investments involve risks.",
        "logout": "Logout",
        "welcome": "Welcome Back",
        "today_pnl": "Today's P&L",
        "total_return": "Total Return",
        "win_rate": "Win Rate",
        "loading": "Loading...",
        "generate_solution": "Generate Solution",
        "market_opportunity": "Market Opportunity",
        "risk_analysis": "Risk Analysis",
        "entry_point": "Entry Point",
        "exit_point": "Exit Point",
        "expected_return": "Expected Return",
        "allocation_ratio": "Allocation Ratio",
        "monitoring_indicators": "Key Indicators",
        "buy": "Buy",
        "sell": "Sell",
        "quantity": "Quantity",
        "current_price": "Current Price",
        "pnl": "P&L",
        "change": "Change",
        "volume": "Volume",
        "features_title": "Core Features",
        "ai_insights": "AI-Powered Insights",
        "ai_insights_desc": "Leverage artificial intelligence to analyze market trends and provide personalized investment recommendations",
        "portfolio_management": "Portfolio Management",
        "portfolio_management_desc": "Professional virtual trading system to validate investment strategies risk-free",
        "real_time_data": "Real-time Market Data",
        "real_time_data_desc": "Synchronized global financial markets data for better investment timing",
        "risk_control": "Intelligent Risk Control", 
        "risk_control_desc": "Multi-layered risk assessment to protect your investments",
        "pricing_title": "Subscription Plans",
        "free_plan": "Free Trial",
        "premium_plan": "Premium",
        "contact_us": "Contact Us",
        "about_us": "About Us",
        "privacy_policy": "Privacy Policy",
        "terms_of_service": "Terms of Service"
    }
}

# ====== Session State 初始化 ======
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
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
if 'subscription_active' not in st.session_state:
    st.session_state.subscription_active = True
if 'generated_solutions' not in st.session_state:
    st.session_state.generated_solutions = []

# ====== 智能Logo系統 ======
def load_optimal_logo():
    """載入最適合的TENKI Logo"""
    logo_configs = [
        {
            "file": "IMG_0640.jpeg", 
            "priority": 1, 
            "type": "hero",
            "description": "3D立體主視覺Logo"
        },
        {
            "file": "IMG_0639.jpeg", 
            "priority": 2, 
            "type": "brand",
            "description": "圓形品牌Logo"
        },
        {
            "file": "IMG_0638.png", 
            "priority": 3, 
            "type": "clean",
            "description": "簡潔版Logo"
        }
    ]
    
    for config in logo_configs:
        try:
            with open(config["file"], "rb") as f:
                image_data = f.read()
                image_b64 = base64.b64encode(image_data).decode()
                config["data"] = f"data:image/{'png' if config['file'].endswith('.png') else 'jpeg'};base64,{image_b64}"
                return config
        except:
            continue
    
    return None

# ====== 市場數據系統 ======
@st.cache_data(ttl=60, show_spinner=False)
def get_market_data():
    """獲取市場數據"""
    # 主要指數
    major_indices = {
        'SPY': 'SPDR S&P 500 ETF',
        'QQQ': 'Invesco QQQ ETF',
        'DIA': 'SPDR Dow Jones ETF',
        'VTI': 'Vanguard Total Stock Market ETF'
    }
    
    # 熱門股票
    hot_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX']
    
    # 債券ETF
    bond_etfs = ['TLT', 'IEF', 'LQD', 'HYG']
    
    market_data = {}
    
    def fetch_symbol_data(symbol):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d", interval="1d")
            info = ticker.info
            
            if not hist.empty and len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                change = current - prev_close
                change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                volume = hist['Volume'].iloc[-1] if not hist['Volume'].isna().iloc[-1] else 0
                
                return {
                    'symbol': symbol,
                    'name': info.get('longName', symbol),
                    'price': float(current),
                    'change': float(change),
                    'change_pct': float(change_pct),
                    'volume': int(volume) if volume and not np.isnan(volume) else 0,
                    'market_cap': info.get('marketCap', 0),
                    'pe_ratio': info.get('trailingPE', 0)
                }
        except:
            return None
    
    all_symbols = list(major_indices.keys()) + hot_stocks + bond_etfs
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_symbol_data, symbol) for symbol in all_symbols]
        for future in futures:
            result = future.result()
            if result:
                market_data[result['symbol']] = result
    
    return market_data

# ====== 投資解決方案生成系統 ======
def generate_investment_solution(risk_pref, investment_goal, market_data):
    """生成個性化投資解決方案"""
    
    # 根據風險偏好和投資目標生成解決方案
    solutions_db = {
        ('conservative', 'income'): {
            'theme': '2024年防禦型收益投資策略',
            'insight': '在當前市場環境下，投資者應重點關注穩定收益資產。美國長期公債和高評級企業債券提供相對穩定的收益來源，同時高股息股票和REIT基金可提供持續現金流。建議採用分散配置策略，降低單一資產風險。',
            'targets': [
                {
                    'symbol': 'TLT',
                    'type': '長期公債ETF',
                    'allocation': 40,
                    'entry_point': '當前價位分批進入',
                    'exit_point': 'Fed降息循環結束',
                    'expected_return': '4-6%',
                    'analysis': '20年以上美國公債ETF，在降息環境下表現優異，提供穩定收益'
                },
                {
                    'symbol': 'VYM',
                    'type': '高股息ETF',
                    'allocation': 35,
                    'entry_point': '回調至$110以下',
                    'exit_point': '股息率降至2%以下',
                    'expected_return': '5-7%',
                    'analysis': '追蹤高股息美股，提供穩定現金流，適合收益型投資者'
                },
                {
                    'symbol': 'VNQ',
                    'type': 'REIT ETF',
                    'allocation': 25,
                    'entry_point': '當前價位定期定額',
                    'exit_point': '利率大幅上升時',
                    'expected_return': '6-8%',
                    'analysis': '不動產投資信託ETF，通脹對沖工具，提供租金收益'
                }
            ],
            'risk_factors': ['利率風險', '通脹風險', '流動性風險', '信用風險'],
            'monitoring_indicators': ['10年期美債收益率', 'Fed利率政策', '通膨數據CPI', 'REITs利率敏感性']
        },
        
        ('moderate', 'balanced'): {
            'theme': '2024年AI科技平衡配置策略',
            'insight': '人工智慧革命正在重塑各個行業，但市場波動性增加。建議平衡配置科技龍頭股、成長型ETF和防禦性資產，在追求成長的同時控制風險。關注AI產業鏈上下游機會，同時保持適度的債券配置作為緩衝。',
            'targets': [
                {
                    'symbol': 'QQQ',
                    'type': '科技ETF',
                    'allocation': 30,
                    'entry_point': '回調至$360以下',
                    'exit_point': '估值過高時減碼',
                    'expected_return': '8-12%',
                    'analysis': '追蹤納斯達克100指數，科技股集中度高，受惠於AI浪潮'
                },
                {
                    'symbol': 'NVDA',
                    'type': 'AI晶片龍頭',
                    'allocation': 20,
                    'entry_point': '技術回調時分批進入',
                    'exit_point': '基本面轉弱時',
                    'expected_return': '15-25%',
                    'analysis': 'AI晶片絕對領導者，GPU在AI訓練和推理中不可替代'
                },
                {
                    'symbol': 'VTI',
                    'type': '全市場ETF',
                    'allocation': 30,
                    'entry_point': '當前價位定期定額',
                    'exit_point': '長期持有',
                    'expected_return': '7-10%',
                    'analysis': '全市場指數ETF，提供最佳分散效果，降低個股風險'
                },
                {
                    'symbol': 'LQD',
                    'type': '投資級債券',
                    'allocation': 20,
                    'entry_point': '收益率4%以上時',
                    'exit_point': 'Fed轉向升息時',
                    'expected_return': '4-5%',
                    'analysis': '投資級企業債券ETF，提供穩定收益，降低組合波動'
                }
            ],
            'risk_factors': ['科技股波動', '利率變化', '市場系統風險', 'AI泡沫風險'],
            'monitoring_indicators': ['AI產業發展', '科技股估值水準', 'Fed政策變化', 'VIX恐慌指數']
        },
        
        ('aggressive', 'growth'): {
            'theme': '2024年成長型科技投資攻略',
            'insight': '積極型投資者可重點佈局具有顛覆性創新潛力的成長股。AI、雲端運算、電動車、生技等領域仍有巨大成長空間，但需承擔相應的高波動風險。建議集中投資於具有強勁基本面和清晰成長路徑的龍頭企業。',
            'targets': [
                {
                    'symbol': 'ARKK',
                    'type': '創新ETF',
                    'allocation': 25,
                    'entry_point': '大幅回調至$40以下',
                    'exit_point': '創新主題降溫時',
                    'expected_return': '15-30%',
                    'analysis': '專注顛覆性創新的主動型ETF，包含基因療法、自動駕駛等'
                },
                {
                    'symbol': 'TSLA',
                    'type': '電動車龍頭',
                    'allocation': 20,
                    'entry_point': '$180-200區間',
                    'exit_point': '自動駕駛進展停滯時',
                    'expected_return': '20-40%',
                    'analysis': '電動車和自動駕駛雙重領導者，受惠於能源轉型'
                },
                {
                    'symbol': 'MSFT',
                    'type': '雲端AI巨頭',
                    'allocation': 25,
                    'entry_point': '$320以下分批',
                    'exit_point': '雲端成長明顯放緩',
                    'expected_return': '12-18%',
                    'analysis': 'Azure雲端服務和AI整合最完整，企業數位轉型受惠者'
                },
                {
                    'symbol': 'SOXX',
                    'type': '半導體ETF',
                    'allocation': 30,
                    'entry_point': '產業週期低點進入',
                    'exit_point': '產業週期高點',
                    'expected_return': '18-25%',
                    'analysis': '半導體產業ETF，AI基礎設施建設的核心受惠標的'
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
        # 預設解決方案
        return solutions_db[('moderate', 'balanced')]

# ====== 修正後的設計系統 ======
def load_fixed_tenki_design():
    """載入修正後的TENKI設計系統"""
    
    st.markdown("""
    <style>
        /* 導入現代字體 */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&display=swap');
        
        /* 基礎設定 */
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
            background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 100%);
            font-family: 'Inter', sans-serif;
            color: #ffffff;
            min-height: 100vh;
        }
        
        #MainMenu, footer, header, .stDeployButton, .stDecoration {
            display: none !important;
        }
        
        .stApp {
            margin-top: -100px !important;
            background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 100%);
            min-height: 100vh;
        }
        
        /* 主容器 */
        .main-container {
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* 品牌展示 */
        .tenki-hero {
            text-align: center;
            padding: 4rem 2rem;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
            border-radius: 24px;
            margin-bottom: 3rem;
            position: relative;
            overflow: hidden;
        }
        
        .tenki-hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6, #10b981);
            animation: glow-pulse 3s ease-in-out infinite;
        }
        
        @keyframes glow-pulse {
            0%, 100% { opacity: 0.6; }
            50% { opacity: 1; }
        }
        
        .tenki-logo {
            width: 120px;
            height: 120px;
            margin: 0 auto 2rem;
            border-radius: 50%;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
            position: relative;
        }
        
        .tenki-logo::before {
            content: '';
            position: absolute;
            top: -4px;
            left: -4px;
            right: -4px;
            bottom: -4px;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            border-radius: 50%;
            opacity: 0.5;
            animation: logo-spin 8s linear infinite;
            z-index: -1;
        }
        
        @keyframes logo-spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .tenki-logo img {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            object-fit: cover;
        }
        
        .tenki-logo-fallback {
            font-family: 'Outfit', sans-serif;
            font-size: 3rem;
            font-weight: 800;
            color: white;
        }
        
        .tenki-title {
            font-family: 'Outfit', sans-serif;
            font-size: clamp(3rem, 8vw, 5rem);
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #ffffff 0%, #3b82f6 50%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .tenki-subtitle {
            font-family: 'Noto Sans JP', sans-serif;
            font-size: 1.5rem;
            color: #94a3b8;
            margin-bottom: 1rem;
        }
        
        .tenki-slogan {
            font-size: 1.25rem;
            color: #cbd5e1;
            margin-bottom: 1rem;
            font-style: italic;
        }
        
        .tenki-description {
            font-size: 1rem;
            color: #94a3b8;
            line-height: 1.6;
            margin-bottom: 2rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* 導航系統 */
        .nav-container {
            background: rgba(30, 41, 59, 0.9);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 16px;
            padding: 1rem;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        .nav-brand {
            display: flex;
            align-items: center;
            gap: 1rem;
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1.25rem;
            color: #ffffff;
        }
        
        .nav-links {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        
        /* 現代卡片設計 */
        .modern-card {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            margin-bottom: 2rem;
        }
        
        .modern-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6, #10b981);
        }
        
        .modern-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 25px 50px -12px rgba(59, 130, 246, 0.25);
            border-color: rgba(59, 130, 246, 0.3);
        }
        
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.5rem;
        }
        
        .card-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: #ffffff;
        }
        
        .card-icon {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        
        /* 指標卡片 */
        .metric-card {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            border-color: rgba(59, 130, 246, 0.4);
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
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }
        
        .metric-change {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.875rem;
            font-weight: 600;
        }
        
        .metric-positive {
            color: #10b981;
        }
        
        .metric-negative {
            color: #ef4444;
        }
        
        /* 解決方案卡片 */
        .solution-card {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 24px;
            padding: 2.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4);
        }
        
        .solution-theme {
            font-family: 'Outfit', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .solution-insight {
            color: #cbd5e1;
            line-height: 1.7;
            margin-bottom: 2rem;
            font-size: 1rem;
        }
        
        .target-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .target-card {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.2s ease;
        }
        
        .target-card:hover {
            background: rgba(30, 41, 59, 0.8);
            border-color: rgba(59, 130, 246, 0.3);
        }
        
        .target-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }
        
        .target-symbol {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.25rem;
            font-weight: 700;
            color: #ffffff;
        }
        
        .target-type {
            font-size: 0.75rem;
            color: #8b5cf6;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            background: rgba(139, 92, 246, 0.1);
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
        }
        
        .target-allocation {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.5rem;
            font-weight: 700;
            color: #10b981;
        }
        
        .target-analysis {
            color: #94a3b8;
            font-size: 0.9rem;
            line-height: 1.6;
            margin-bottom: 1rem;
        }
        
        .target-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1rem;
        }
        
        .detail-item {
            text-align: center;
        }
        
        .detail-label {
            font-size: 0.75rem;
            color: #6b7280;
            font-weight: 500;
            margin-bottom: 0.25rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .detail-value {
            font-size: 0.9rem;
            color: #ffffff;
            font-weight: 600;
        }
        
        /* 登入表單 */
        .login-container {
            max-width: 400px;
            margin: 2rem auto;
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 24px;
            padding: 3rem 2rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .login-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.75rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0.5rem;
        }
        
        .login-subtitle {
            color: #94a3b8;
            font-size: 1rem;
        }
        
        /* 響應式設計 */
        @media (max-width: 768px) {
            .main-container {
                padding: 1rem;
            }
            
            .tenki-hero {
                padding: 2rem 1rem;
            }
            
            .tenki-title {
                font-size: 2.5rem;
            }
            
            .nav-container {
                padding: 1rem 0.75rem;
            }
            
            .nav-links {
                width: 100%;
                justify-content: center;
            }
            
            .target-grid {
                grid-template-columns: 1fr;
            }
            
            .modern-card {
                padding: 1.5rem;
            }
            
            .login-container {
                margin: 1rem;
                padding: 2rem 1.5rem;
            }
        }
        
        /* Streamlit 組件優化 */
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
            border: none !important;
            border-radius: 12px !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 0.75rem 1.5rem !important;
            transition: all 0.3s ease !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3) !important;
        }
        
        .stSelectbox > div > div {
            background: rgba(30, 41, 59, 0.8) !important;
            border: 1px solid rgba(148, 163, 184, 0.2) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
        }
        
        .stTextInput > div > div > input {
            background: rgba(30, 41, 59, 0.8) !important;
            border: 1px solid rgba(148, 163, 184, 0.2) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            padding: 0.75rem !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
        }
        
        /* 免責聲明 */
        .disclaimer {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            color: #fca5a5;
            font-size: 0.9rem;
            line-height: 1.6;
            margin: 2rem 0;
        }
        
        .disclaimer-icon {
            display: inline-block;
            margin-right: 0.5rem;
            font-size: 1.1rem;
        }
    </style>
    """, unsafe_allow_html=True)

# ====== Landing Page ======
def show_landing_page():
    """顯示Landing Page"""
    lang = st.session_state.language
    t = TEXTS[lang]
    
    # Hero Section
    logo_config = load_optimal_logo()
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 品牌展示區域
    if logo_config:
        logo_element = f'<img src="{logo_config["data"]}" alt="TENKI Logo" />'
    else:
        logo_element = '<div class="tenki-logo-fallback">T</div>'
    
    st.markdown(f'''
    <div class="tenki-hero">
        <div class="tenki-logo">
            {logo_element}
        </div>
        <h1 class="tenki-title">TENKI</h1>
        <p class="tenki-subtitle">{t['app_subtitle']}</p>
        <p class="tenki-slogan">{t['slogan']}</p>
        <div class="tenki-description">
            {t['app_description']} • 在關鍵轉折點做出理想決策 • 實現資產增值
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # 語言切換和CTA按鈕
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        # 語言切換
        lang_col1, lang_col2, lang_col3 = st.columns(3)
        
        with lang_col1:
            if st.button("🇹🇼 中文", use_container_width=True, 
                        type="primary" if lang == 'zh' else "secondary"):
                st.session_state.language = 'zh'
                st.rerun()
        
        with lang_col2:
            if st.button("🇺🇸 English", use_container_width=True,
                        type="primary" if lang == 'en' else "secondary"):
                st.session_state.language = 'en'
                st.rerun()
        
        st.markdown("---")
        
        # CTA按鈕
        if st.button(f"🚀 {t['get_started']}", use_container_width=True, type="primary"):
            st.session_state.current_page = 'login'
            st.rerun()
        
        if st.button(f"📖 {t['learn_more']}", use_container_width=True):
            st.info("💡 更多功能介紹即將推出...")
    
    # 核心功能介紹
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h2 class="card-title">{t['features_title']}</h2>
            <div class="card-icon">⭐</div>
        </div>
        
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
    ''', unsafe_allow_html=True)
    
    # 免責聲明
    st.markdown(f'''
    <div class="disclaimer">
        <span class="disclaimer-icon">⚠️</span>
        {t['disclaimer']}
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ====== 登入頁面 ======
def show_login_page():
    """顯示登入頁面"""
    lang = st.session_state.language
    t = TEXTS[lang]
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 品牌區域
    logo_config = load_optimal_logo()
    
    if logo_config:
        st.markdown(f'''
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="width: 80px; height: 80px; margin: 0 auto 1rem; border-radius: 50%; background: linear-gradient(135deg, #3b82f6, #8b5cf6); display: flex; align-items: center; justify-content: center;">
                <img src="{logo_config['data']}" alt="TENKI Logo" style="width: 60px; height: 60px; border-radius: 50%;" />
            </div>
            <h1 style="font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 700; color: #ffffff; margin-bottom: 0.5rem;">TENKI</h1>
            <p style="color: #94a3b8;">{t['tagline']}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # 登入表單
    with st.form("login_form"):
        email = st.text_input(t['email'], placeholder="your@email.com")
        password = st.text_input(t['password'], type="password", placeholder="••••••••")
        
        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button(t['login'], use_container_width=True)
        with col2:
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
    
    st.markdown(f'<p style="text-align: center; margin: 1rem 0;"><a href="#" style="color: #3b82f6;">{t["forgot_password"]}</a></p>', unsafe_allow_html=True)
    
    # 社群登入
    st.markdown("**或使用以下方式登入**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"🔍 {t['google_login']}", use_container_width=True):
            st.session_state.user_logged_in = True
            st.session_state.user_email = "user@gmail.com"
            st.session_state.current_page = 'dashboard'
            st.rerun()
    with col2:
        if st.button(f"🍎 {t['apple_login']}", use_container_width=True):
            st.session_state.user_logged_in = True
            st.session_state.user_email = "user@icloud.com"
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    # 返回Landing Page
    if st.button(f"← 返回首頁", use_container_width=True):
        st.session_state.current_page = 'landing'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ====== 導航系統 ======
def create_navigation():
    """創建導航系統"""
    lang = st.session_state.language
    t = TEXTS[lang]
    
    if st.session_state.user_logged_in:
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        
        # 品牌區域
        logo_config = load_optimal_logo()
        if logo_config:
            brand_logo = f'<img src="{logo_config["data"]}" alt="TENKI" style="width: 32px; height: 32px; border-radius: 50%;" />'
        else:
            brand_logo = '<div style="width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #3b82f6, #8b5cf6); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1rem; color: white;">T</div>'
        
        st.markdown(f'''
        <div class="nav-brand">
            {brand_logo}
            <span>TENKI</span>
        </div>
        ''', unsafe_allow_html=True)
        
        # 導航選項
        nav_items = [
            ('dashboard', '🏠 ' + t['dashboard']),
            ('auto_navigation', '🧭 ' + t['auto_navigation']),
            ('solution_generator', '⚡ ' + t['solution_generator']),
            ('virtual_portfolio', '💼 ' + t['virtual_portfolio']),
            ('subscription', '💳 ' + t['my_subscription']),
            ('settings', '⚙️ ' + t['settings'])
        ]
        
        cols = st.columns([2] + [1] * len(nav_items) + [1])
        
        # 空佔位
        with cols[0]:
            st.write("")
        
        # 導航連結
        for i, (page_key, page_name) in enumerate(nav_items, 1):
            with cols[i]:
                if st.button(page_name, use_container_width=True,
                           type="primary" if st.session_state.current_page == page_key else "secondary"):
                    st.session_state.current_page = page_key
                    st.rerun()
        
        # 登出
        with cols[-1]:
            if st.button(f"🚪 {t['logout']}"):
                st.session_state.user_logged_in = False
                st.session_state.current_page = 'landing'
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# ====== 儀表板 ======
def show_dashboard():
    """顯示儀表板"""
    lang = st.session_state.language
    t = TEXTS[lang]
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 歡迎標題
    st.markdown(f'''
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 style="font-family: 'Outfit', sans-serif; font-size: 2.5rem; font-weight: 700; color: #ffffff; margin-bottom: 0.5rem;">
            {t['welcome']}, {st.session_state.user_email.split('@')[0]}! 🎉
        </h1>
        <p style="color: #94a3b8; font-size: 1.125rem;">準備好開始您今天的投資之旅了嗎？</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # 績效指標卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">{t['today_pnl']}</div>
            <div class="metric-value metric-positive">+$1,234</div>
            <div class="metric-change metric-positive">+2.3% 今日</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">{t['total_return']}</div>
            <div class="metric-value metric-positive">+$12,567</div>
            <div class="metric-change metric-positive">+15.6% 總計</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">{t['win_rate']}</div>
            <div class="metric-value">68.5%</div>
            <div class="metric-change metric-positive">↗ 持續提升</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">風險指標</div>
            <div class="metric-value" style="color: #10b981;">低風險</div>
            <div class="metric-change">波動率: 12.3%</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # 市場概況
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h2 class="card-title">📊 {t['market_overview']}</h2>
            <div class="card-icon">📈</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # 載入市場數據
    with st.spinner(f"{t['loading']}"):
        market_data = get_market_data()
    
    if market_data:
        # 主要指數
        st.markdown("**主要指數**")
        index_cols = st.columns(4)
        indices = ['SPY', 'QQQ', 'DIA', 'VTI']
        
        for i, symbol in enumerate(indices):
            if symbol in market_data:
                data = market_data[symbol]
                with index_cols[i]:
                    st.metric(
                        label=symbol,
                        value=f"${data['price']:.2f}",
                        delta=f"{data['change']:+.2f} ({data['change_pct']:+.2f}%)"
                    )
        
        # 熱門股票
        st.markdown("**熱門股票**")
        stock_cols = st.columns(4)
        hot_stocks = ['AAPL', 'MSFT', 'GOOGL', 'NVDA']
        
        for i, symbol in enumerate(hot_stocks):
            if symbol in market_data:
                data = market_data[symbol]
                with stock_cols[i]:
                    st.metric(
                        label=symbol,
                        value=f"${data['price']:.2f}",
                        delta=f"{data['change']:+.2f} ({data['change_pct']:+.2f}%)"
                    )
    
    # 快速操作區域
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h2 class="card-title">⚡ 快速操作</h2>
            <div class="card-icon">🚀</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"🧭 {t['auto_navigation']}", use_container_width=True):
            st.session_state.current_page = 'auto_navigation'
            st.rerun()
    
    with col2:
        if st.button(f"⚡ {t['generate_solution']}", use_container_width=True):
            st.session_state.current_page = 'solution_generator'
            st.rerun()
    
    with col3:
        if st.button(f"💼 {t['virtual_portfolio']}", use_container_width=True):
            st.session_state.current_page = 'virtual_portfolio'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ====== 自動導航模式 ======
def show_auto_navigation():
    """顯示自動導航模式"""
    lang = st.session_state.language
    t = TEXTS[lang]
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h1 class="card-title">🧭 {t['auto_navigation']}</h1>
            <div class="card-icon">🎯</div>
        </div>
        <p style="color: #94a3b8; margin-bottom: 2rem;">根據您的投資偏好和目標，為您提供個性化的投資建議</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # 用戶偏好設定
    st.markdown("### 📊 投資偏好設定")
    
    col1, col2 = st.columns(2)
    
    with col1:
        risk_pref = st.selectbox(
            t['risk_preference'],
            options=['conservative', 'moderate', 'aggressive'],
            format_func=lambda x: {'conservative': t['conservative'], 'moderate': t['moderate'], 'aggressive': t['aggressive']}[x],
            index=['conservative', 'moderate', 'aggressive'].index(st.session_state.risk_preference)
        )
        st.session_state.risk_preference = risk_pref
    
    with col2:
        invest_goal = st.selectbox(
            t['investment_goal'],
            options=['income', 'balanced', 'growth'],
            format_func=lambda x: {'income': t['income'], 'balanced': t['balanced'], 'growth': t['growth']}[x],
            index=['income', 'balanced', 'growth'].index(st.session_state.investment_goal)
        )
        st.session_state.investment_goal = invest_goal
    
    # 生成個性化建議
    if st.button(f"🎯 {t['generate_solution']}", use_container_width=True, type="primary"):
        with st.spinner(f"{t['loading']}"):
            market_data = get_market_data()
            solution = generate_investment_solution(risk_pref, invest_goal, market_data)
            st.session_state.generated_solutions = [solution]
        
        st.success("✅ 已生成個性化投資解決方案！")
        time.sleep(1)
        st.session_state.current_page = 'solution_generator'
        st.rerun()
    
    # 當前設定摘要
    st.markdown("### ⚙️ 當前設定")
    
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h3 class="card-title">您的投資組合設定</h3>
            <div class="card-icon">🎯</div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 1rem;">
            <div style="text-align: center;">
                <div style="color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.5rem;">{t['risk_preference']}</div>
                <div style="color: #ffffff; font-weight: 600; font-size: 1.125rem;">
                    {'保守型' if risk_pref == 'conservative' else '穩健型' if risk_pref == 'moderate' else '積極型'}
                </div>
            </div>
            <div style="text-align: center;">
                <div style="color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.5rem;">{t['investment_goal']}</div>
                <div style="color: #ffffff; font-weight: 600; font-size: 1.125rem;">
                    {'收益導向' if invest_goal == 'income' else '平衡配置' if invest_goal == 'balanced' else '成長導向'}
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ====== 解決方案生成器 ======
def show_solution_generator():
    """顯示解決方案生成器"""
    lang = st.session_state.language
    t = TEXTS[lang]
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h1 class="card-title">⚡ {t['solution_generator']}</h1>
            <div class="card-icon">🎯</div>
        </div>
        <p style="color: #94a3b8;">基於AI分析和專家洞察，為您生成個性化投資解決方案</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # 顯示生成的解決方案
    if st.session_state.generated_solutions:
        for i, solution in enumerate(st.session_state.generated_solutions):
            st.markdown(f'''
            <div class="solution-card">
                <h2 class="solution-theme">🎯 {solution['theme']}</h2>
                <div class="solution-insight">{solution['insight']}</div>
                
                <div style="margin-bottom: 2rem;">
                    <h3 style="color: #ffffff; margin-bottom: 1rem;">💡 {t['expert_insights']}</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem;">
                        <div style="text-align: center; padding: 1rem; background: rgba(59, 130, 246, 0.1); border-radius: 12px;">
                            <div style="color: #3b82f6; font-weight: 600; margin-bottom: 0.5rem;">市場機會</div>
                            <div style="color: #10b981; font-weight: 600;">AI科技革命浪潮</div>
                        </div>
                        <div style="text-align: center; padding: 1rem; background: rgba(245, 158, 11, 0.1); border-radius: 12px;">
                            <div style="color: #f59e0b; font-weight: 600; margin-bottom: 0.5rem;">風險等級</div>
                            <div style="color: #f59e0b; font-weight: 600;">中等風險</div>
                        </div>
                        <div style="text-align: center; padding: 1rem; background: rgba(139, 92, 246, 0.1); border-radius: 12px;">
                            <div style="color: #8b5cf6; font-weight: 600; margin-bottom: 0.5rem;">建議時程</div>
                            <div style="color: #8b5cf6; font-weight: 600;">6-12個月</div>
                        </div>
                    </div>
                </div>
                
                <h3 style="color: #ffffff; margin-bottom: 1.5rem;">📊 {t['recommended_targets']}</h3>
            </div>
            ''', unsafe_allow_html=True)
            
            # 建議標的
            st.markdown('<div class="target-grid">', unsafe_allow_html=True)
            
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
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 行動計劃
            st.markdown(f'''
            <div class="solution-card">
                <h3 style="color: #ffffff; margin-bottom: 1.5rem;">📋 {t['action_plan']}</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
                    <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 12px; padding: 1.5rem;">
                        <div style="color: #ef4444; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                            <span>⚠️</span> 風險監控
                        </div>
                        <ul style="color: #cbd5e1; font-size: 0.9rem; margin: 0; padding-left: 1.2rem; line-height: 1.6;">
                            {"".join([f"<li style='margin-bottom: 0.5rem;'>{risk}</li>" for risk in solution['risk_factors']])}
                        </ul>
                    </div>
                    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 1.5rem;">
                        <div style="color: #10b981; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                            <span>📊</span> {t['monitoring_indicators']}
                        </div>
                        <ul style="color: #cbd5e1; font-size: 0.9rem; margin: 0; padding-left: 1.2rem; line-height: 1.6;">
                            {"".join([f"<li style='margin-bottom: 0.5rem;'>{indicator}</li>" for indicator in solution['monitoring_indicators']])}
                        </ul>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            # 操作按鈕
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"📌 {t['add_to_watchlist']}", use_container_width=True):
                    st.success("✅ 已加入追蹤清單！")
            
            with col2:
                if st.button(f"💼 加入虛擬組合", use_container_width=True):
                    # 將解決方案標的加入虛擬投資組合
                    for target in solution['targets']:
                        portfolio_item = {
                            'symbol': target['symbol'],
                            'quantity': int(target['allocation'] * 100),  # 假設$10000總額
                            'entry_price': np.random.uniform(100, 500),  # 模擬價格
                            'current_price': np.random.uniform(100, 500),
                            'entry_date': datetime.now()
                        }
                        st.session_state.virtual_portfolio.append(portfolio_item)
                    
                    st.success("✅ 已加入虛擬投資組合！")
    
    else:
        st.markdown(f'''
        <div class="modern-card">
            <div style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem; margin-bottom: 1.5rem;">🎯</div>
                <h2 style="color: #ffffff; font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;">
                    尚無生成的投資解決方案
                </h2>
                <p style="color: #94a3b8; margin-bottom: 2rem; line-height: 1.6;">
                    請先前往自動導航模式設定您的投資偏好，<br/>
                    我們將為您生成專業的投資建議
                </p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button(f"🧭 前往自動導航設定", use_container_width=True, type="primary"):
            st.session_state.current_page = 'auto_navigation'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ====== 虛擬投資組合 ======
def show_virtual_portfolio():
    """顯示虛擬投資組合"""
    lang = st.session_state.language
    t = TEXTS[lang]
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h1 class="card-title">💼 {t['virtual_portfolio']}</h1>
            <div class="card-icon">📈</div>
        </div>
        <p style="color: #94a3b8;">無風險的虛擬交易環境，驗證您的投資策略</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # 組合績效總覽
    if st.session_state.virtual_portfolio:
        total_value = 0
        total_cost = 0
        
        for item in st.session_state.virtual_portfolio:
            total_value += item['quantity'] * item['current_price']
            total_cost += item['quantity'] * item['entry_price']
        
        total_pnl = total_value - total_cost
        total_return_pct = (total_pnl / total_cost * 100) if total_cost > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">組合價值</div>
                <div class="metric-value">${total_value:,.0f}</div>
                <div style="color: #94a3b8; font-size: 0.8rem;">投入成本: ${total_cost:,.0f}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            pnl_class = "metric-positive" if total_pnl >= 0 else "metric-negative"
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">{t['total_return']}</div>
                <div class="metric-value {pnl_class}">${total_pnl:+,.0f}</div>
                <div class="metric-change {pnl_class}">{total_return_pct:+.2f}%</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            win_count = sum(1 for item in st.session_state.virtual_portfolio if item['current_price'] > item['entry_price'])
            win_rate = (win_count / len(st.session_state.virtual_portfolio)) * 100
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">{t['win_rate']}</div>
                <div class="metric-value">{win_rate:.1f}%</div>
                <div style="color: #94a3b8; font-size: 0.8rem;">{win_count}/{len(st.session_state.virtual_portfolio)} 獲利</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-label">持倉數量</div>
                <div class="metric-value">{len(st.session_state.virtual_portfolio)}</div>
                <div style="color: #94a3b8; font-size: 0.8rem;">檔標的</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # 持倉明細
        st.markdown("### 📊 持倉明細")
        
        for item in st.session_state.virtual_portfolio:
            pnl = (item['current_price'] - item['entry_price']) * item['quantity']
            pnl_pct = ((item['current_price'] - item['entry_price']) / item['entry_price'] * 100) if item['entry_price'] > 0 else 0
            pnl_color = "#10b981" if pnl >= 0 else "#ef4444"
            
            st.markdown(f'''
            <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(148, 163, 184, 0.1); border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 1rem; align-items: center;">
                <div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 1.1rem; color: #ffffff;">{item['symbol']}</div>
                    <div style="color: #94a3b8; font-size: 0.85rem;">{item['quantity']} 股</div>
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
            ''', unsafe_allow_html=True)
        
        # 操作按鈕
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 更新價格", use_container_width=True):
                # 模擬價格更新
                for item in st.session_state.virtual_portfolio:
                    change_pct = np.random.uniform(-0.05, 0.05)  # ±5% 隨機變化
                    item['current_price'] *= (1 + change_pct)
                st.success("✅ 價格已更新！")
                st.rerun()
        
        with col2:
            if st.button("📊 生成報告", use_container_width=True):
                st.info("📄 績效報告功能開發中...")
        
        with col3:
            if st.button("🗑️ 清空組合", use_container_width=True):
                st.session_state.virtual_portfolio = []
                st.success("✅ 虛擬組合已清空！")
                st.rerun()
    
    else:
        st.markdown(f'''
        <div class="modern-card">
            <div style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem; margin-bottom: 1.5rem;">💼</div>
                <h2 style="color: #ffffff; font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;">
                    您的虛擬投資組合是空的
                </h2>
                <p style="color: #94a3b8; margin-bottom: 2rem; line-height: 1.6;">
                    透過解決方案生成器建立您的第一個投資組合，<br/>
                    開始無風險的投資策略驗證
                </p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button(f"⚡ 前往解決方案生成器", use_container_width=True, type="primary"):
            st.session_state.current_page = 'solution_generator'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ====== 訂閱管理 ======
def show_subscription():
    """顯示訂閱管理"""
    lang = st.session_state.language
    t = TEXTS[lang]
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h1 class="card-title">💳 {t['my_subscription']}</h1>
            <div class="card-icon">⭐</div>
        </div>
        <p style="color: #94a3b8;">管理您的訂閱方案和付款設定</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # 訂閱狀態卡片
    st.markdown(f'''
    <div class="modern-card">
        <div style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #10b981, #059669); color: white; border-radius: 50px; font-size: 0.9rem; font-weight: 600; margin-bottom: 2rem;">
            <div style="width: 8px; height: 8px; border-radius: 50%; background: currentColor; animation: pulse 2s infinite;"></div>
            <span>訂閱有效</span>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin: 2rem 0;">
            <div style="text-align: center;">
                <div style="color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.5rem;">當前方案</div>
                <div style="color: #ffffff; font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem;">{t['monthly_plan']}</div>
                <div style="color: #10b981; font-size: 0.8rem;">✅ 無限制使用所有功能</div>
            </div>
            
            <div style="text-align: center;">
                <div style="color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.5rem;">{t['next_billing']}</div>
                <div style="color: #ffffff; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">2024年11月22日</div>
                <div style="color: #94a3b8; font-size: 0.8rem;">自動續訂</div>
            </div>
            
            <div style="text-align: center;">
                <div style="color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.5rem;">{t['payment_method']}</div>
                <div style="color: #ffffff; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">•••• •••• •••• 1234</div>
                <div style="color: #94a3b8; font-size: 0.8rem;">Visa 信用卡</div>
            </div>
        </div>
        
        <div style="margin-top: 2rem;">
            <h3 style="color: #ffffff; margin-bottom: 1.5rem;">📋 訂閱功能</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem; background: rgba(16, 185, 129, 0.1); border-radius: 8px;">
                    <div style="color: #10b981; font-size: 1.2rem;">✅</div>
                    <div style="color: #cbd5e1; font-size: 0.9rem;">無限制解決方案生成</div>
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem; background: rgba(16, 185, 129, 0.1); border-radius: 8px;">
                    <div style="color: #10b981; font-size: 1.2rem;">✅</div>
                    <div style="color: #cbd5e1; font-size: 0.9rem;">專家投資組合追蹤</div>
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem; background: rgba(16, 185, 129, 0.1); border-radius: 8px;">
                    <div style="color: #10b981; font-size: 1.2rem;">✅</div>
                    <div style="color: #cbd5e1; font-size: 0.9rem;">即時市場數據推送</div>
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem; background: rgba(16, 185, 129, 0.1); border-radius: 8px;">
                    <div style="color: #10b981; font-size: 1.2rem;">✅</div>
                    <div style="color: #cbd5e1; font-size: 0.9rem;">個性化投資建議</div>
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem; background: rgba(16, 185, 129, 0.1); border-radius: 8px;">
                    <div style="color: #10b981; font-size: 1.2rem;">✅</div>
                    <div style="color: #cbd5e1; font-size: 0.9rem;">風險管理工具</div>
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem; background: rgba(16, 185, 129, 0.1); border-radius: 8px;">
                    <div style="color: #10b981; font-size: 1.2rem;">✅</div>
                    <div style="color: #cbd5e1; font-size: 0.9rem;">24/7 客戶支援</div>
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # 訂閱管理按鈕
    st.markdown("### ⚙️ 訂閱管理")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💳 更改付款方式", use_container_width=True):
            st.info("🔄 付款方式更新功能開發中...")
    
    with col2:
        if st.button("📧 修改帳單地址", use_container_width=True):
            st.info("📝 帳單地址更新功能開發中...")
    
    with col3:
        if st.button("❌ 取消訂閱", use_container_width=True):
            if st.button("⚠️ 確認取消訂閱", use_container_width=True):
                st.session_state.subscription_active = False
                st.warning("⚠️ 訂閱已取消，您可以繼續使用到期日：2024年11月22日")
    
    # 使用統計
    st.markdown("### 📊 使用統計")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">解決方案生成</div>
            <div class="metric-value">23</div>
            <div style="color: #94a3b8; font-size: 0.8rem;">本月使用次數</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">投資組合追蹤</div>
            <div class="metric-value">156</div>
            <div style="color: #94a3b8; font-size: 0.8rem;">累計建立組合數</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">平台使用</div>
            <div class="metric-value">47</div>
            <div style="color: #94a3b8; font-size: 0.8rem;">天（累計登入）</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ====== 設定頁面 ======
def show_settings():
    """顯示設定頁面"""
    lang = st.session_state.language
    t = TEXTS[lang]
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="modern-card">
        <div class="card-header">
            <h1 class="card-title">⚙️ {t['settings']}</h1>
            <div class="card-icon">🛠️</div>
        </div>
        <p style="color: #94a3b8;">個性化您的TENKI體驗設定</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # 語言設定
    st.markdown("### 🌐 語言設定")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇹🇼 繁體中文", 
                     use_container_width=True,
                     type="primary" if st.session_state.language == 'zh' else "secondary"):
            st.session_state.language = 'zh'
            st.rerun()
    
    with col2:
        if st.button("🇺🇸 English", 
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
            format_func=lambda x: {'conservative': t['conservative'], 'moderate': t['moderate'], 'aggressive': t['aggressive']}[x],
            index=['conservative', 'moderate', 'aggressive'].index(st.session_state.risk_preference)
        )
    
    with col2:
        new_invest_goal = st.selectbox(
            t['investment_goal'],
            options=['income', 'balanced', 'growth'],
            format_func=lambda x: {'income': t['income'], 'balanced': t['balanced'], 'growth': t['growth']}[x],
            index=['income', 'balanced', 'growth'].index(st.session_state.investment_goal)
        )
    
    if st.button("💾 儲存設定", use_container_width=True, type="primary"):
        st.session_state.risk_preference = new_risk_pref
        st.session_state.investment_goal = new_invest_goal
        st.success("✅ 設定已儲存！")
    
    # 通知設定
    st.markdown("### 🔔 通知設定")
    
    notification_email = st.checkbox("📧 電子郵件通知", value=True)
    notification_push = st.checkbox("📱 推播通知", value=True)
    notification_sms = st.checkbox("📞 簡訊通知", value=False)
    
    # 資料管理
    st.markdown("### 📊 資料管理")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤 匯出資料", use_container_width=True):
            st.info("📄 資料匯出功能開發中...")
    
    with col2:
        if st.button("🗑️ 清除快取", use_container_width=True):
            st.cache_data.clear()
            st.success("✅ 快取已清除！")
    
    with col3:
        if st.button("🔄 重設APP", use_container_width=True):
            if st.button("⚠️ 確認重設", use_container_width=True):
                # 重設所有session state
                for key in list(st.session_state.keys()):
                    if key != 'user_logged_in' and key != 'current_page':
                        del st.session_state[key]
                st.success("✅ APP已重設！")
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ====== 主應用程式 ======
def main():
    """TENKI主應用程式"""
    
    # 載入修正後的設計系統
    load_fixed_tenki_design()
    
    # 路由系統
    if st.session_state.current_page == 'landing':
        show_landing_page()
    elif st.session_state.current_page == 'login':
        show_login_page()
    elif st.session_state.user_logged_in:
        # 顯示導航
        create_navigation()
        
        # 根據當前頁面顯示相應內容
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
        # 未登入用戶預設返回landing page
        st.session_state.current_page = 'landing'
        show_landing_page()
    
    # 頁面底部免責聲明
    if st.session_state.user_logged_in:
        lang = st.session_state.language
        t = TEXTS[lang]
        
        st.markdown(f'''
        <div class="disclaimer">
            <span class="disclaimer-icon">⚠️</span>
            {t['disclaimer']}
        </div>
        ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
