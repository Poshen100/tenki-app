import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# 頁面配置
st.set_page_config(
    page_title="TENKI - Investment Advisory",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 集中 CSS
st.markdown("""
<style>
    /* 隱藏Streamlit默認元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 主容器樣式 */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }
    
    /* 標題樣式 */
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    
    .logo-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: 3px;
        margin-bottom: 0.5rem;
    }
    
    .tagline {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Hero卡片樣式 */
    .hero-card {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.3);
    }
    
    .hero-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .content-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .insight-text {
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        opacity: 0.95;
    }
    
    /* 按鈕樣式 */
    .stButton > button {
        background: linear-gradient(135deg, #FB923C 0%, #F97316 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(251, 146, 60, 0.5);
    }
    
    /* 指標卡片樣式 */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #1E3A8A;
        margin: 1rem 0;
    }
    
    /* 表格樣式 */
    .stock-table {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# 函數：渲染標頭
def render_header():
    st.markdown("""
    <div style='width:100vw;min-width:100vw;margin-left:calc(-50vw + 50%);background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);padding:32px 0 24px 0;'>
        <div style='text-align:center;'>
            <span style='display:block; font-size:3rem; font-weight:800; letter-spacing:3px; color:white;'>TENKI</span>
            <span style='display:block; font-size:1.25rem; color:white;opacity:0.92;margin-top:0.5rem;'>Turning Insight into Opportunity</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 函數：生成價格數據 (快取)
@st.cache_data
def generate_price_data():
    dates = pd.date_range(start='2024-01-01', end='2024-09-21', freq='D')
    price_data = []
    np.random.seed(42)
    symbols = ['COIN', 'MSTR', 'RIOT']
    for symbol in symbols:
        base_price = df[df['Symbol'] == symbol]['Price'].iloc[0] * 0.8
        changes = np.random.normal(0, 0.02, len(dates))
        prices = base_price * np.cumprod(1 + changes)
        price_data.extend([{'Date': date, 'Symbol': symbol, 'Price': price} for date, price in zip(dates, prices)])
    return pd.DataFrame(price_data)

# 主程式
render_header()

# 美股報價區
st.markdown("### 📈 美股熱門標的")

try:
    st.html("""
    <!-- TradingView Widget BEGIN -->
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
        "largeChartUrl": "",
        "isTransparent": false,
        "showSymbolLogo": true,
        "plotLineColorGrowing": "rgba(41, 98, 255, 1)",
        "plotLineColorFalling": "rgba(41, 98, 255, 1)",
        "gridLineColor": "rgba(42, 46, 57, 0.06)",
        "scaleFontColor": "rgba(106, 109, 120, 1)",
        "belowLineFillColorGrowing": "rgba(41, 98, 255, 0.12)",
        "belowLineFillColorFalling": "rgba(41, 98, 255, 0.12)",
        "symbolActiveColor": "rgba(41, 98, 255, 0.12)",
        "tabs": [
          {
            "title": "指數",
            "symbols": [
              {"s": "FOREXCOM:SPXUSD", "d": "S&P 500"},
              {"s": "FOREXCOM:NSXUSD", "d": "US 100"},
              {"s": "FOREXCOM:DJI", "d": "Dow 30"},
              {"s": "INDEX:NKY", "d": "Nikkei 225"}
            ]
          },
          {
            "title": "熱門股票",
            "symbols": [
              {"s": "NASDAQ:AAPL"},
              {"s": "NASDAQ:MSFT"},
              {"s": "NASDAQ:AMZN"},
              {"s": "NASDAQ:GOOGL"},
              {"s": "NASDAQ:TSLA"}
            ]
          }
        ]
      }
      </script>
    </div>
    <!-- TradingView Widget END -->
    """, height=420)
except Exception as e:
    st.error("無法載入 TradingView widget。請檢查網路連線。")

# 主標題圖片
st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center; width: 100%;">
        <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/IMG_0639.jpeg" style="width: 100%; max-width: 420px; margin-top: 18px; margin-bottom: 18px;" alt="TENKI Logo">
    </div>
    """, unsafe_allow_html=True
)

# Hero區域
st.markdown("""
<div class="hero-card">
    <div class="hero-title">✨ 今日轉機 (Today's Sweet Spot)</div>
    <div class="content-title">美股區塊鏈概念股</div>
    <div class="insight-text">比特幣ETF熱潮帶動，預期Q4漲幅15-20%</div>
</div>
""", unsafe_allow_html=True)

# 行動按鈕
if st.button("查看完整解決方案", key="main_cta"):
    st.success("🎯 正在為您準備完整的投資解決方案...")

# 模擬數據
stock_data = {
    'Symbol': ['COIN', 'MSTR', 'RIOT', 'MARA', 'BTBT'],
    'Name': ['Coinbase Global', 'MicroStrategy', 'Riot Blockchain', 'Marathon Digital', 'Bit Digital'],
    'Price': [156.42, 1247.85, 8.94, 15.73, 2.89],
    'Change': [2.8, 5.2, 1.4, -0.8, 3.1],
    'Volume': ['2.1M', '145K', '5.8M', '12.3M', '3.2M']
}
df = pd.DataFrame(stock_data)

# 顏色函數
def color_change(val):
    color = '#16a34a' if val > 0 else '#dc2626'
    sign = '+' if val > 0 else ''
    return f'color: {color}; font-weight: bold'

# 創建顯示 DF
df_display = df.copy()
df_display['Change'] = df['Change'].apply(lambda x: f"{ '+' if x > 0 else ''}{x}%")

# 創建三欄佈局
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 市場概況")
    st.metric("比特幣價格", "$67,234", "2.1%", delta_color="normal")
    st.metric("區塊鏈指數", "1,284", "3.4%", delta_color="normal")

with col2:
    st.markdown("### 🎯 投資組合表現")
    st.metric("總收益", "$12,456", "8.7%", delta_color="normal")
    st.metric("今日收益", "$856", "1.2%", delta_color="normal")

with col3:
    st.markdown("### ⭐ 推薦評級")
    st.metric("強力買入", "3 檔", "")
    st.metric("買入", "2 檔", "")

# 股票表格
st.markdown("## 💼 我的追蹤")
st.markdown('<div class="stock-table">', unsafe_allow_html=True)
st.markdown("### 📈 區塊鏈概念股動態")
st.dataframe(
    df_display.style.applymap(color_change, subset=['Change']).format({'Price': '${:,.2f}'})
)
st.markdown('</div>', unsafe_allow_html=True)

# 圖表區域
st.markdown("## 📊 價格走勢分析")
price_df = generate_price_data()
fig = px.line(price_df, x='Date', y='Price', color='Symbol', 
              title='區塊鏈概念股價格走勢',
              labels={'Price': '股價 (USD)', 'Date': '日期'})
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(size=12),
    title_font_size=16,
    height=500
)
st.plotly_chart(fig, use_container_width=True)

# 底部導航
st.markdown("---")
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
with nav_col1:
    st.markdown("**🏠 Dashboard**")
with nav_col2:
    if st.button("🎯 Auto-Guide"):
        st.info("自動投資指引功能開發中...")
with nav_col3:
    if st.button("💼 Portfolio"):
        st.info("投資組合詳情功能開發中...")
with nav_col4:
    if st.button("⭐ Subscription"):
        st.info("訂閱服務功能開發中...")

# 側邊欄
with st.sidebar:
    st.markdown("## ⚙️ 設置")
    language = st.selectbox("語言 / Language", ["繁體中文", "English"])
    # TODO: 根據 language 動態翻譯內容
    theme = st.selectbox("主題模式", ["亮色主題", "暗色主題"])
    st.markdown("### 🔔 通知設置")
    st.checkbox("價格提醒", value=True)
    st.checkbox("新聞提醒", value=True)
    st.checkbox("研報提醒", value=False)
    st.markdown("---")
    st.markdown("**版本:** v1.0.0")
    st.markdown("**最後更新:** 2024-09-21")

# 頁腳
st.markdown("""
---
<div style='text-align: center; color: #64748b; padding: 2rem;'>
    <p>© 2024 TENKI Investment Advisory. All rights reserved.</p>
    <p>投資有風險，入市需謹慎</p>
</div>
""", unsafe_allow_html=True)
st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center;">
        <img src="https://raw.githubusercontent.com/Poshen100/tenki-app/main/IMG_0638.png" style="width:100%; max-width:420px;" alt="TENKI Footer Image">
    </div>
    """,
    unsafe_allow_html=True
)
