import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from ui_common import setup_page, page_header, render_footer

setup_page(
    "Research Overview | Google Play App Success Classification",
    "📊",
)

# Research overview for two independent projects. No retraining or methodology changes.

page_header(
    "📊 Research Overview",
    "Google Play App Success Classification",
    "Research overview · Feature analysis · Machine learning classification · Model explainability",
)

st.markdown(
    "本頁整理 es2 與 es3 各自的研究定位、特徵規模與既有模型評估紀錄。"
    "**es2 與 es3 為兩個獨立研究專案**；本頁僅提供成果導覽，不合併模型、不重新訓練模型，也不變更研究方法。"
)

st.info(
    "研究問題：哪些可於早期取得的 App Features，具有預測 App Success 的能力？\n\n"
    "研究解讀：可於早期取得的 App 特徵具有一定的預測訊號，但整體預測能力仍有限。"
)

st.divider()

# ==========================================
# Dataset & Target
# ==========================================

st.markdown("## Dataset & Target")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Dataset Records", "11,500")
with c2:
    st.metric("es2 Input Features", "11")
with c3:
    st.metric("es3 Input Features", "8")

st.markdown(
    "**Target definition — Success**\n\n"
    "Success = 1 when `Installs >= 10,000`; otherwise Success = 0.\n\n"
    "資料集筆數與目標定義來自既有研究紀錄；本頁不會重新讀取或修改研究資料。"
)

st.divider()

# ==========================================
# es2
# ==========================================

st.markdown("## es2 — Feature Analysis")
st.caption(
    "Google Play App Success Classification: "
    "A Machine Learning Analysis Based on App Features"
)

a, b, c = st.columns(3)
with a:
    st.metric("Research Input Features", "11")
with b:
    st.metric("Transformed Features", "97")
with c:
    st.metric("Test F1 Score", "0.268012")

d, e, f = st.columns(3)
with d:
    st.metric("Test Balanced Accuracy", "0.488648")
with e:
    st.metric("Best CV F1 Score", "0.271828")

st.markdown(
    "既有正式模型：經調校的 Decision Tree（決策樹）分類器。參數："
    "`class_weight='balanced'`、`max_depth=5`、`min_samples_leaf=5`、"
    "`min_samples_split=2`、`random_state=42`。"
)

st.caption(
    "來源註記：es2 的模型參數、轉換後特徵數與 Test F1 由專案內 metadata 支持；"
    "Balanced Accuracy 與 CV F1 為既有研究紀錄，本頁未重新執行評估。"
)

st.markdown("### es2 Feature Interpretation")
st.write("既有特徵重要性分析中，排名較前的原始特徵如下：")
st.dataframe(
    {
        "Feature": [
            "Size_MB", "Genre_Secondary", "Genre_Primary",
            "Content Rating", "Android_Min_Version", "Category",
        ],
        "Importance": [
            0.426534, 0.178136, 0.135912,
            0.126578, 0.068191, 0.064649,
        ],
    },
    hide_index=True,
    use_container_width=True,
)

st.divider()

# ==========================================
# es3
# ==========================================

st.markdown("## es3 — Experimental & Validation Analysis")
st.caption(
    "Google Play App Success Classification: "
    "Experimental and Validation Analysis of Machine Learning Models"
)

a, b, c = st.columns(3)
with a:
    st.metric("Research Input Features", "8")
with b:
    st.metric("Test F1 Score", "0.2384")
with c:
    st.metric("Test Balanced Accuracy", "0.4936")

st.write(
    "既有模型檔為包含前處理與分類器的 Pipeline（管線），分類器為 Decision Tree（決策樹）。"
    "模型原始輸入特徵為 8 個；分類器的轉換後特徵數不等同於原始輸入特徵數。"
)

st.warning(
    "es3 評估指標與特徵解釋數值目前來自既有研究報告紀錄；"
    "es3 專案資料夾內未找到對應的 model_metadata.json 或 feature_metadata.json，"
    "因此以下數值尚未由專案內 metadata 獨立交叉核對。"
)

st.markdown("### es3 Feature Interpretation")
st.write("既有報告記載的 Decision Tree 特徵重要性如下（非本頁重新計算）：")
st.dataframe(
    {
        "Feature": [
            "Android Ver", "Genres", "Category", "Size",
            "Content Rating", "Ad Supported", "Price", "Type",
        ],
        "Importance": [
            0.318752, 0.244897, 0.141600, 0.126511,
            0.109653, 0.033585, 0.020374, 0.004628,
        ],
    },
    hide_index=True,
    use_container_width=True,
)

st.caption(
    "來源註記：es3 Test F1、Balanced Accuracy 與特徵重要性均為既有報告紀錄，"
    "不應解讀為本頁已重新驗證的結果。"
)

st.divider()

# ==========================================
# Project Navigation
# ==========================================

st.markdown("## Project Navigation")

n1, n2, n3 = st.columns(3)
with n1:
    st.markdown("### 📱 es2 Prediction")
    st.write("使用 es2 的 11 個輸入特徵，查看 es2 正式模型的預測結果。")
with n2:
    st.markdown("### 📲 es3 Prediction")
    st.write("使用 es3 的 8 個輸入特徵，查看 es3 正式模型的預測結果。")
with n3:
    st.markdown("### 📊 Prediction Comparison")
    st.write("查看兩個獨立模型各自的預測輸出；此頁不代表新增的合併模型。")

st.warning(
    "解讀限制：模型預測為估計結果，不代表 App 實際成功率或成功保證。"
    "研究結果顯示的預測訊號有限，不應作為單一決策依據。"
)

render_footer()