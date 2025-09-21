import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
import time

# ====== 頁面配置 (必須在最頂部) ======
st.set_page_config(
    page_title="TENKI - Investment Advisory",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====== 快取數據函數 ======
@st.cache_data(ttl=300)  # 5分鐘快取
def get_stock_data():
    """獲取股票模擬數據"""
    return {
        'Symbol': ['COIN', 'MSTR', 'RIOT', 'MARA', 'BTBT'],
        'Name': ['Coinbase Global', 'MicroStrategy', 'Riot Blockchain', 'Marathon Digital', 'Bit Digital'],
        'Price': [156.42, 1247.85, 8.94, 15.73, 2.89],
        'Change': [2.8, 5.2, 1.4, -0.8, 3.1],
        'Volume': ['2.1M', '145K', '5.8M', '12.3M', '3.2M']
    }

@st.cache_data(ttl=600)  # 10分鐘快取
def generate_price_history(df):
    """生成價格走勢數據"""
    dates = pd.date_range(start='2024-01-01', end='2024-09-21', freq='D')
    np.random.seed(42)
    price_data = []
    
    for symbol in ['COIN', 'MSTR', 'RIOT']:
        base_price = df[df['Symbol'] == symbol]['Price'].iloc[0]
        current_price = base_price * 0.8
        prices = []
        
        for _ in dates:
            change = np.random.normal(0, 0.02)
            current_price *= (1 + change)
            prices.append(current_price)
        
        for i, date in enumerate(dates):
            price_data.append({
                'Date': date,
                'Symbol': symbol,
                'Price': prices[i]
            })
    
    return pd.DataFrame(price_data)

# ====== 統一CSS樣式 ======
def load_css():
    st.markdown("""
    <style>
        /* 隱藏Streamlit元素 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* 響應式容器 */
        .main .block-container {
            padding: 1rem 2rem;
            max-width: 1400px;
        }
        
        /* 全寬頁首 */
        .full-width-header {
            width: 100vw;
            margin-left: calc(-50vw + 50%);
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
            padding: 2rem 0;
            margin-bottom: 2rem;
        }
        
        .header-content {
            text-align: center;
            color: white;
        }
        
        .header-title {
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 800;
            letter-spacing: 3px;
            margin-bottom: 0.5rem;
        }
        
        .header-subtitle {
            font-size: clamp(1rem, 3vw, 1.25rem);
            opacity: 0.9;
        }
        
        /* 卡片樣式 */
        .insight-card {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            margin: 2rem 0;
            box-shadow: 0 8px 24px rgba(37, 99, 235, 0.2);
        }
        
        /* 按鈕優化 */
        .stButton > button {
            background: linear-gradient(135deg, #FB923C 0%, #F97316 100%);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 10px;
            font-weight: 600;
            width: 100%;
            transition: transform 0.2s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
        }
        
        /* 響應式表格 */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem;
            }
        }
        
        /* Loading動畫 */
        .loading {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 200px;
        }
    </style>
    """, unsafe_allow_html=True)

# ====== 工具函數 ======
def format_change(value):
    """格式化變化率顯示"""
    color = "#16a34a" if value > 0 else "#dc2626"
    sign = "+" if value > 0 else ""
    return f'<span style="color: {color}; font-weight: bold;">{sign}{value}%</span>'

def create_metric_card(title, value, change, icon="📊"):
    """創建指標卡片"""
    return f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center;">
        <h4>{icon} {title}</h4>
        <h2 style="margin: 0.5rem 0; color: #1E3A8A;">{value}</h2>
        <p style="margin: 0; {f'color: #16a34a' if change.startswith('+') else 'color: #dc2626'};">{change}</p>
    </div>
    """

# ====== 主程式開始 ======
def main():
    load_css()
    
    # 頁首區域
    st.markdown("""
    <div class="full-width-header">
        <div class="header-content">
            <div class="header-title">TENKI</div>
            <div class="header-subtitle">Turning Insight into Opportunity</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # TradingView 圖表
    with st.container():
        st.markdown("### 📈 美股即時行情")
        
        # 加入loading狀態
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
                          {"s": "FOREXCOM:DJI", "d": "道瓊指數"}
                        ]
                      },
                      {
                        "title": "區塊鏈概念股",
                        "symbols": [
                          {"s": "NASDAQ:COIN"},
                          {"s": "NASDAQ:MSTR"},
                          {"s": "NASDAQ:RIOT"}
                        ]
                      }
                    ]
                  }
                  </script>
                </div>
                """,
                height=450
            )
    
    # 今日洞察
    st.markdown("""
    <div class="insight-card">
        <h3>✨ 今日投資洞察</h3>
        <h2>美股區塊鏈概念股</h2>
        <p>比特幣ETF持續流入，帶動相關概念股走強。建議關注 COIN、MSTR 等龍頭標的，預期Q4有15-20%上漲空間。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 獲取數據
    stock_data = get_stock_data()
    df = pd.DataFrame(stock_data)
    
    # 關鍵指標
    st.markdown("## 📊 市場概況")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card("比特幣", "$67,234", "+2.1%", "₿"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_metric_card("總收益", "$12,456", "+8.7%", "💰"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_metric_card("今日收益", "$856", "+1.2%", "📈"), unsafe_allow_html=True)
    with col4:
        st.markdown(create_metric_card("強力買入", "3 檔", "", "⭐"), unsafe_allow_html=True)
    
    # 股票列表
    st.markdown("## 💼 追蹤標的")
    
    # 使用原生 Streamlit 表格，更簡潔
    display_df = df.copy()
    display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:,.2f}")
    display_df['Change (%)'] = display_df['Change'].apply(lambda x: f"{'+' if x > 0 else ''}{x}%")
    
    st.dataframe(
        display_df[['Symbol', 'Name', 'Price', 'Change (%)', 'Volume']],
        use_container_width=True,
        hide_index=True
    )
    
    # 價格走勢圖
    st.markdown("## 📊 價格走勢")
    
    with st.spinner("生成走勢圖中..."):
        price_df = generate_price_history(df)
        
        fig = px.line(
            price_df, 
            x='Date', 
            y='Price', 
            color='Symbol',
            title='區塊鏈概念股90日走勢',
            labels={'Price': '股價 (USD)', 'Date': '日期'}
        )
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 底部功能
    st.markdown("---")
    st.markdown("### 🚀 探索更多功能")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 AI 投資建議", use_container_width=True):
            st.success("AI 正在分析最佳投資時機...")
    
    with col2:
        if st.button("💼 組合優化", use_container_width=True):
            st.info("投資組合優化功能即將推出...")
    
    with col3:
        if st.button("📧 訂閱服務", use_container_width=True):
            st.info("訂閱每日投資洞察報告...")

# 側邊欄
def setup_sidebar():
    with st.sidebar:
        st.markdown("## ⚙️ 設定")
        
        language = st.selectbox("語言", ["繁體中文", "English", "日本語"])
        theme = st.selectbox("主題", ["淺色", "深色"])
        
        st.markdown("### 🔔 通知設定")
        price_alert = st.toggle("價格提醒", True)
        news_alert = st.toggle("新聞提醒", True)
        
        st.markdown("---")
        st.caption("© 2024 TENKI Investment Advisory")

# ====== 執行主程式 ======
if __name__ == "__main__":
    setup_sidebar()
    main()
    
    # 頁腳 Logo
    st.markdown("---")
    st.markdown(
        """
        <div style="display: flex; justify-content: center; padding: 2rem 0;">
            <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/IMG_0638.png" 
                 style="width: 200px; opacity: 0.6;">
        </div>
        """,
        unsafe_allow_html=True
    )
