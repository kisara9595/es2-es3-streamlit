
"""
Shared UI helpers for the Google Play App Success Classification app.
Modern AI Research Dashboard UI.
所有頁面共用此模組，統一視覺風格與 UI 元件。
"""

import streamlit as st


# =========================================================
# Step 1：Design Tokens｜全站設計變數
# =========================================================

COLOR_PRIMARY = "#6846D8"
COLOR_PRIMARY_DARK = "#5030B0"
COLOR_PRIMARY_LIGHT = "#9279F2"

COLOR_HEADING = "#202744"
COLOR_TEXT = "#34405B"
COLOR_MUTED = "#727D95"

COLOR_BG = "#F4F6FC"
COLOR_SURFACE = "#FFFFFF"
COLOR_SIDEBAR = "#F0EEFA"
COLOR_BORDER = "#E3E6F2"

COLOR_SUCCESS = "#16866A"
COLOR_WARNING = "#B7791F"
COLOR_DANGER = "#D94F70"

FOOTER_TEXT = (
    "Research Prototype｜研究原型｜"
    "Model estimates are not guarantees."
)


# =========================================================
# Step 2：Global CSS｜科技感全域樣式
# =========================================================

GLOBAL_CSS = f"""
<style>

/* =======================================================
   A. Global Foundation｜全站基礎
   ======================================================= */

:root {{
    --ui-primary: {COLOR_PRIMARY};
    --ui-primary-dark: {COLOR_PRIMARY_DARK};
    --ui-primary-light: {COLOR_PRIMARY_LIGHT};
    --ui-heading: {COLOR_HEADING};
    --ui-text: {COLOR_TEXT};
    --ui-muted: {COLOR_MUTED};
    --ui-bg: {COLOR_BG};
    --ui-surface: {COLOR_SURFACE};
    --ui-border: {COLOR_BORDER};
    --ui-radius: 16px;
    --ui-shadow: 0 5px 20px rgba(46, 43, 92, 0.055);
    --ui-shadow-hover: 0 10px 28px rgba(80, 48, 176, 0.12);
}}

html,
body {{
    font-size: 16px;
    color: var(--ui-text);
    scroll-behavior: smooth;
}}

.stApp {{
    background:
        radial-gradient(
            ellipse at 5% 0%,
            rgba(146, 121, 242, 0.10),
            transparent 34%
        ),
        radial-gradient(
            ellipse at 100% 8%,
            rgba(104, 70, 216, 0.055),
            transparent 30%
        ),
        var(--ui-bg);
    color: var(--ui-text);
}}

/* 主要內容區域 */

.main .block-container,
.block-container {{
    max-width: 1440px;
    padding-top: 2.2rem;
    padding-bottom: 3.5rem;
    padding-left: clamp(1rem, 3vw, 2.5rem);
    padding-right: clamp(1rem, 3vw, 2.5rem);
}}

/* 隱藏 Streamlit 預設裝飾列，保留功能 */

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

/* =======================================================
   B. Typography｜字體與文字層次
   ======================================================= */

h1, h2, h3, h4 {{
    color: var(--ui-heading);
    font-family:
        "Inter",
        "Noto Sans TC",
        "Microsoft JhengHei",
        sans-serif;
    line-height: 1.45 !important;
}}

h1 {{
    color: var(--ui-primary) !important;
    font-size: clamp(1.9rem, 3vw, 2.45rem) !important;
    font-weight: 800 !important;
    letter-spacing: -0.7px;
    margin-bottom: 0.75rem !important;
}}

h2 {{
    font-size: 1.55rem !important;
    font-weight: 750 !important;
    letter-spacing: -0.3px;
    margin-top: 1.8rem !important;
    margin-bottom: 0.9rem !important;
}}

h3 {{
    color: var(--ui-primary) !important;
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    margin-top: 1.3rem !important;
    margin-bottom: 0.7rem !important;
}}

h4 {{
    font-size: 1.1rem !important;
    font-weight: 700 !important;
}}

p, li {{
    color: var(--ui-text);
    font-size: 1rem !important;
    line-height: 1.8 !important;
}}

[data-testid="stCaptionContainer"] p {{
    color: var(--ui-muted) !important;
    font-size: 0.875rem !important;
    line-height: 1.65 !important;
}}

/* 副標題 */

[data-testid="stHeadingWithActionElements"] h2 {{
    scroll-margin-top: 1.5rem;
}}

/* =======================================================
   C. Sidebar｜側邊導覽
   ======================================================= */

section[data-testid="stSidebar"] {{
    background:
        linear-gradient(
            180deg,
            #F2EFFD 0%,
            #F8F7FD 52%,
            #F0EEFA 100%
        );
    border-right: 1px solid rgba(104, 70, 216, 0.13);
}}

section[data-testid="stSidebar"] > div {{
    padding-top: 1.5rem;
}}

section[data-testid="stSidebar"] p {{
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
}}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong {{
    color: var(--ui-primary-dark);
}}

section[data-testid="stSidebar"] hr {{
    border-color: rgba(104, 70, 216, 0.15);
}}

/* =======================================================
   D. Inputs｜輸入框與下拉選單
   ======================================================= */

[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stTextArea label {{
    color: var(--ui-heading) !important;
    font-size: 0.96rem !important;
    font-weight: 650 !important;
    line-height: 1.6 !important;
}}

input,
textarea,
[data-baseweb="select"] {{
    font-size: 1rem !important;
}}

/* 輸入框圓角與邊框 */

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea,
[data-baseweb="select"] > div {{
    border-radius: 10px !important;
    border-color: #D9DDEE !important;
    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease,
        background-color 0.2s ease;
}}

/* Focus 狀態 */

[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {{
    border-color: var(--ui-primary) !important;
    box-shadow: 0 0 0 3px rgba(104, 70, 216, 0.13) !important;
}}

/* 元件垂直間距 */

div[data-testid="stSelectbox"],
div[data-testid="stNumberInput"],
div[data-testid="stTextInput"],
div[data-testid="stTextArea"] {{
    margin-bottom: 0.65rem;
}}

/* =======================================================
   E. Forms｜表單容器
   ======================================================= */

[data-testid="stForm"] {{
    background: rgba(255, 255, 255, 0.94);
    border: 1px solid var(--ui-border);
    border-radius: var(--ui-radius);
    padding: 1.4rem 1.5rem;
    box-shadow: var(--ui-shadow);
    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}}

[data-testid="stForm"]:hover {{
    border-color: #D4CCF3;
    box-shadow: var(--ui-shadow-hover);
}}

/* =======================================================
   F. Buttons｜科技感按鈕
   ======================================================= */

.stButton button,
[data-testid="stFormSubmitButton"] button {{
    min-height: 44px;
    border-radius: 11px !important;
    font-size: 0.98rem !important;
    font-weight: 700 !important;
    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease,
        border-color 0.18s ease,
        background-color 0.18s ease;
}}

/* Primary button */

.stButton button[kind="primary"],
[data-testid="stFormSubmitButton"] button[kind="primary"] {{
    background: linear-gradient(
        135deg,
        {COLOR_PRIMARY} 0%,
        {COLOR_PRIMARY_DARK} 100%
    ) !important;
    border: 1px solid transparent !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 12px rgba(104, 70, 216, 0.20);
}}

.stButton button[kind="primary"]:hover,
[data-testid="stFormSubmitButton"] button[kind="primary"]:hover {{
    box-shadow: 0 7px 20px rgba(104, 70, 216, 0.30);
    transform: translateY(-1px);
}}

/* Secondary button */

.stButton button[kind="secondary"]:hover,
[data-testid="stFormSubmitButton"] button[kind="secondary"]:hover {{
    border-color: var(--ui-primary) !important;
    color: var(--ui-primary) !important;
    background: #F6F3FF !important;
    transform: translateY(-1px);
}}

/* Keyboard accessibility */

.stButton button:focus-visible,
[data-testid="stFormSubmitButton"] button:focus-visible {{
    outline: 3px solid rgba(104, 70, 216, 0.35) !important;
    outline-offset: 2px;
}}

/* =======================================================
   G. Metrics｜數據卡片
   ======================================================= */

div[data-testid="stMetric"] {{
    position: relative;
    overflow: hidden;
    background: linear-gradient(
        145deg,
        #FFFFFF 0%,
        #FBFAFF 100%
    );
    border: 1px solid var(--ui-border);
    border-radius: 15px;
    padding: 1.15rem 1.25rem;
    box-shadow: var(--ui-shadow);
    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease,
        border-color 0.2s ease;
}}

div[data-testid="stMetric"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(
        90deg,
        {COLOR_PRIMARY},
        {COLOR_PRIMARY_LIGHT},
        #B8A9FF
    );
    opacity: 0.85;
}}

div[data-testid="stMetric"]:hover {{
    border-color: #D1C7F5;
    box-shadow: var(--ui-shadow-hover);
    transform: translateY(-2px);
}}

[data-testid="stMetricLabel"] p {{
    color: var(--ui-muted) !important;
    font-size: 0.9rem !important;
    font-weight: 650 !important;
}}

[data-testid="stMetricValue"] {{
    color: var(--ui-heading) !important;
    font-size: clamp(1.35rem, 2vw, 2rem) !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}}

[data-testid="stMetricDelta"] {{
    font-size: 0.85rem !important;
}}

/* =======================================================
   H. Alerts｜提示訊息
   ======================================================= */

div[data-testid="stAlert"] {{
    border-radius: 13px;
    padding: 1rem 1.2rem;
    border: 1px solid rgba(104, 70, 216, 0.12);
}}

div[data-testid="stAlert"] p {{
    line-height: 1.75 !important;
}}

/* =======================================================
   I. DataFrame｜資料表格
   ======================================================= */

div[data-testid="stDataFrame"] {{
    border: 1px solid var(--ui-border);
    border-radius: 13px;
    overflow: hidden;
    box-shadow: var(--ui-shadow);
}}

/* =======================================================
   J. Expander｜可展開區塊
   ======================================================= */

div[data-testid="stExpander"] {{
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid var(--ui-border);
    border-radius: 12px;
    overflow: hidden;
    transition: border-color 0.2s ease;
}}

div[data-testid="stExpander"]:hover {{
    border-color: #D1C7F5;
}}

div[data-testid="stExpander"] summary {{
    font-weight: 650;
}}

/* =======================================================
   K. Tabs｜分頁標籤
   ======================================================= */

button[data-baseweb="tab"] {{
    font-size: 0.96rem !important;
    font-weight: 650 !important;
    transition: color 0.2s ease;
}}

button[data-baseweb="tab"]:hover {{
    color: var(--ui-primary) !important;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    color: var(--ui-primary) !important;
}}

/* =======================================================
   L. Progress / Slider｜進度與滑桿
   ======================================================= */

div[data-testid="stProgress"] > div > div {{
    background: linear-gradient(
        90deg,
        {COLOR_PRIMARY},
        {COLOR_PRIMARY_LIGHT}
    );
    border-radius: 99px;
}}

div[data-testid="stSlider"] [role="slider"] {{
    border-color: var(--ui-primary) !important;
}}

/* =======================================================
   M. Divider｜分隔線
   ======================================================= */

hr {{
    border: none;
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        #D9D5EC 15%,
        #D9D5EC 85%,
        transparent
    );
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}}

/* =======================================================
   N. Links｜連結
   ======================================================= */

a {{
    color: var(--ui-primary);
    text-decoration-thickness: 1px;
    text-underline-offset: 3px;
}}

a:hover {{
    color: var(--ui-primary-dark);
}}

/* =======================================================
   O. Responsive｜響應式版面
   ======================================================= */

@media (max-width: 768px) {{
    .main .block-container,
    .block-container {{
        padding-top: 1.25rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }}

    h1 {{
        font-size: 1.75rem !important;
    }}

    h2 {{
        font-size: 1.35rem !important;
    }}

    [data-testid="stForm"] {{
        padding: 1rem;
    }}

    div[data-testid="stMetric"] {{
        padding: 0.9rem;
    }}
}}

/* 尊重使用者的減少動態效果設定 */

@media (prefers-reduced-motion: reduce) {{
    *,
    *::before,
    *::after {{
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
        animation-duration: 0.01ms !important;
    }}
}}

</style>
"""


# =========================================================
# Step 3：Page Setup｜頁面初始化
# =========================================================

def setup_page(page_title: str, page_icon: str) -> None:
    """
    每個 Streamlit 頁面最先執行的設定。
    設定頁面標題、圖示、寬版版面與全站 CSS。
    """
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
    )
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# =========================================================
# Step 4：Page Header｜共用頁首
# =========================================================

def page_header(
    title: str,
    subtitle: str,
    caption: str,
) -> None:
    """統一顯示頁面標題、副標題與說明。"""
    st.title(title)
    st.subheader(subtitle)
    st.caption(caption)


# =========================================================
# Step 5：Footer｜共用頁尾
# =========================================================

def render_footer() -> None:
    """統一顯示研究原型聲明。"""
    st.divider()
    st.caption(FOOTER_TEXT)


# =========================================================
# Step 6：Research Target｜研究目標定義
# =========================================================

def render_target_definition() -> None:
    """顯示成功分類的研究目標定義。"""
    st.markdown("## Research Target")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Success = 1",
            value="≥ 10,000",
            help="Installs 大於或等於 10,000。",
        )
        st.caption("Installs ≥ 10,000")

    with col2:
        st.metric(
            label="Success = 0",
            value="< 10,000",
            help="Installs 小於 10,000。",
        )
        st.caption("Installs < 10,000")


# =========================================================
# Step 7：Class Probabilities｜類別分數
# =========================================================

def get_class_probabilities(model, X):
    """
    依據 model.classes_ 對應類別標籤與 predict_proba 輸出。

    回傳：
        (P(Not Success), P(Success))

    注意：
        這是模型輸出的類別分數，不代表已校準的實際成功機率。
    """
    probs = model.predict_proba(X)[0]
    classes = list(getattr(model, "classes_", [0, 1]))

    p_not = (
        float(probs[classes.index(0)])
        if 0 in classes
        else 0.0
    )

    p_success = (
        float(probs[classes.index(1)])
        if 1 in classes
        else 0.0
    )

    return p_not, p_success


# =========================================================
# Step 8：Prediction Results｜預測結果
# =========================================================

def render_prediction_result(
    prediction,
    p_not: float,
    p_success: float,
    horizontal: bool = True,
) -> None:
    """
    共用預測結果區塊。

    horizontal=True：
        三個指標水平排列，適用於單模型預測頁。

    horizontal=False：
        三個指標垂直排列，適用於比較頁。

    不修改模型、不重新計算預測結果。
    """
    predicted_class = int(prediction)

    if predicted_class == 1:
        st.success("Prediction Result: Success")
    else:
        st.warning("Prediction Result: Not Success")

    if horizontal:
        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Predicted Class",
                predicted_class,
            )

        with c2:
            st.metric(
                "P(Not Success)",
                f"{p_not:.4f}",
            )

        with c3:
            st.metric(
                "P(Success)",
                f"{p_success:.4f}",
            )

    else:
        st.metric(
            "Predicted Class",
            predicted_class,
        )

        st.metric(
            "P(Not Success)",
            f"{p_not:.4f}",
        )

        st.metric(
            "P(Success)",
            f"{p_success:.4f}",
        )


# =========================================================
# Step 9：Probability Disclaimer｜機率解讀聲明
# =========================================================

def render_probability_disclaimer() -> None:
    """
    說明模型分數的限制。
    不將分類模型輸出直接解讀為實際市場成功率。
    """
    st.info(
        "P(Not Success) 與 P(Success) 為分類模型輸出的分數。"
        "本研究未進行 Probability Calibration（機率校準），"
        "因此這些數值不應直接解讀為實際市場成功率、"
        "校準後機率或成功保證。"
    )
