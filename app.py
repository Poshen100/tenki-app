import streamlit as st

# --- 多語言詞典 ---
TEXT = {
    "login_title": {
        "zh": "登入你的 TENKI 戶口",
        "en": "Sign in to Your TENKI Account",
        "jp": "TENKIアカウントにログイン"
    },
    "username": {"zh":"電子郵件", "en":"Email", "jp":"メールアドレス"},
    "password": {"zh":"密碼", "en":"Password", "jp":"パスワード"},
    "btn_login": {"zh":"登入", "en":"Login", "jp":"ログイン"},
    "btn_logout": {"zh":"登出", "en":"Logout", "jp":"ログアウト"},
    "login_success": {"zh":"登入成功！", "en":"Login successful!", "jp":"ログイン成功！"},
    "login_fail": {"zh":"帳號或密碼錯誤", "en":"Wrong username or password", "jp":"ユーザー名またはパスワードが違います"},

    "dashboard": {"zh":"甜蜜點/投資儀表板", "en":"Sweet Spot / Dashboard", "jp":"スウィートスポット・ダッシュボード"},
    "switch_lang": {"zh":"語言切換", "en":"Language", "jp":"言語切替"},
    "profile": {"zh":"個人設定", "en":"Profile", "jp":"プロフィール"},
    "virtual_portfolio": {"zh":"虛擬組合", "en":"Virtual Portfolio", "jp":"バーチャルポートフォリオ"},
    "sweet_spot": {"zh":"今日甜蜜點", "en":"Today's Sweet Spot", "jp":"本日のスウィートスポット"},
    "add_stock": {"zh": "新增持股", "en":"Add holding", "jp":"銘柄追加"},
    "stock": {"zh":"股票代號", "en":"Stock", "jp":"銘柄"},
    "qty": {"zh":"股數", "en":"Quantity", "jp":"株数"},
    "confirm": {"zh":"確認", "en":"Confirm", "jp":"確認"},
    "success_add": {"zh":"已加入虛擬組合", "en":"Added to virtual portfolio", "jp":"バーチャルポートフォリオに追加されました"},
    "theme": {"zh":"主題", "en":"Theme", "jp":"テーマ"},
    "insight": {"zh":"洞察", "en":"Insight", "jp":"インサイト"},
    "targets": {"zh":"重點標的", "en":"Targets", "jp":"ターゲット"},
    "expected_return": {"zh":"預期報酬", "en":"Expected Return", "jp":"予想リターン"},
    "investment_pref": {"zh":"投資偏好設定", "en":"Investment Preferences", "jp":"投資設定"},
    "risk": {"zh":"風險承受度", "en":"Risk Level", "jp":"リスク許容度"},
    "goal": {"zh":"投資目標", "en":"Investment Goal", "jp":"投資目標"}
}

LANGS = {"繁體中文":"zh", "日本語":"jp", "English":"en"}

# --- 語言切換 ---
if "ui_lang" not in st.session_state:
    st.session_state["ui_lang"] = "zh"

lang_selection = st.sidebar.selectbox(
    TEXT["switch_lang"][st.session_state["ui_lang"]],
    options=list(LANGS.keys()),
    format_func=lambda x: x,
    index=list(LANGS.values()).index(st.session_state["ui_lang"])
)
st.session_state["ui_lang"] = LANGS[lang_selection]
LANG = st.session_state["ui_lang"]

# --- 假用戶資料 & Session 狀態
DEMO_USER = {"email":"demo@tenki.jp", "password":"pass123"}
if "user" not in st.session_state:
    st.session_state["user"] = None
if "portfolio" not in st.session_state:
    st.session_state["portfolio"] = {}

# --- 登入頁 ---
if not st.session_state["user"]:
    st.title("TENKI")
    st.subheader(TEXT["login_title"][LANG])
    user = st.text_input(TEXT["username"][LANG])
    pw = st.text_input(TEXT["password"][LANG], type="password")
    if st.button(TEXT["btn_login"][LANG]):
        if user == DEMO_USER["email"] and pw == DEMO_USER["password"]:
            st.success(TEXT["login_success"][LANG])
            st.session_state["user"] = user
        else:
            st.error(TEXT["login_fail"][LANG])
    st.stop()

# --- 登出 ---
if st.button(TEXT["btn_logout"][LANG]):
    st.session_state["user"] = None
    st.experimental_rerun()

st.title(TEXT["dashboard"][LANG])

# --- 今日甜蜜點範例 ---
sweet_spots = [
    {"theme":{"zh":"美股區塊鏈概念股","en":"US Blockchain Stocks","jp":"米国ブロックチェーン関連"}, 
     "insight": {"zh":"比特幣ETF熱潮帶動Q4漲勢", "en":"BTC ETF hot drives up Q4", "jp":"ビットコインETFが相場を牽引"}, 
     "targets": ["COIN", "MSTR"], 
     "expected_return": "15-20%"},
    {"theme":{"zh":"短期公司債佈局","en":"Short-Term Bonds","jp":"短期債券戦略境"}, 
     "insight": {"zh":"高利息利率、波動小", "en":"High yield, lower risk", "jp":"高利回りで低リスク"}, 
     "targets":["LQD ETF"], 
     "expected_return":"4-6%"}
]

import random
idx = random.randint(0, len(sweet_spots)-1)
spot = sweet_spots[idx]
st.subheader(TEXT["sweet_spot"][LANG])
st.write(f"**{TEXT['theme'][LANG]}:** {spot['theme'][LANG]}")
st.write(f"**{TEXT['insight'][LANG]}:** {spot['insight'][LANG]}")
st.write(f"**{TEXT['targets'][LANG]}:** {', '.join(spot['targets'])}")
st.write(f"**{TEXT['expected_return'][LANG]}:** {spot['expected_return']}")

# --- 虛擬組合 ---
st.subheader(TEXT["virtual_portfolio"][LANG])
portfolio = st.session_state["portfolio"]
if portfolio:
    st.table(
        {TEXT["stock"][LANG]: list(portfolio.keys()), 
         TEXT["qty"][LANG]: list(portfolio.values())}
    )
else:
    st.info(TEXT["virtual_portfolio"][LANG] + " (" + TEXT["profile"][LANG] + "): 空")

# --- 新增持股 ---
st.markdown("### " + TEXT["add_stock"][LANG])
with st.form("add_stock"):
    stock = st.text_input(TEXT["stock"][LANG])
    qty = st.number_input(TEXT["qty"][LANG], min_value=1, value=1)
    submitted = st.form_submit_button(TEXT["confirm"][LANG])
    if submitted:
        if stock:
            portfolio[stock.upper()] = portfolio.get(stock.upper(), 0) + int(qty)
            st.session_state["portfolio"] = portfolio
            st.success(TEXT["success_add"][LANG])
        else:
            st.warning(TEXT["stock"][LANG] + " " + TEXT["confirm"][if not st.session_state["user"]:
    st.image("https://raw.githubusercontent.com/Poshen100/tenki-app/main/IMG_0638.png", width=220)
    st.markdown("<h2 style='text-align: center; margin-top: 0;'>TENKI</h2>", unsafe_allow_html=True)
    st.write("<p style='text-align: center; color: grey;'>Turning Insight into Opportunity</p>", unsafe_allow_html=True)
    st.subheader(TEXT["login_title"][LANG])
    user = st.text_input(TEXT["username"][LANG])
    pw = st.text_input(TEXT["password"][LANG], type="password")
    if st.button(TEXT["btn_login"][LANG]):
        if user == DEMO_USER["email"] and pw == DEMO_USER["password"]:
            st.success(TEXT["login_success"][LANG])
            st.session_state["user"] = user
        else:
            st.error(TEXT["login_fail"][LANG])
    st.stop()
