import streamlit as st
from ui_common import setup_page, render_footer

setup_page(
    "Google Play App Success Classification",
    "📱",
)

# ==========================================
# Home Page
# ==========================================

st.title("📱 Google Play App 成功預測系統")

st.subheader("App Success Prediction Research Prototype")

st.caption("Machine Learning Prediction & Cross-Validation")

st.markdown("""
本系統整合 es2 與 es3 研究模型，
提供 App Success Prediction（App 成功預測）
與模型比較之探索性研究功能。
""")

st.info(
    "🔬 研究原型使用說明\n\n"
    "請由左側選單選擇：\n\n"
    "📊 Research Overview｜研究總覽\n\n"
    "📱 es2 Prediction｜App 成功預測\n\n"
    "📲 es3 Prediction｜App 成功預測\n\n"
    "📊 es2 × es3 Cross-Validation｜模型比較"
)

st.warning(
    "本系統為 Exploratory Decision Support（探索性決策支援）"
    "研究原型。預測結果為模型估計，"
    "不代表 App 實際成功率、成功保證，"
    "亦非自動投資或專案核准依據。"
)

st.divider()

st.markdown("## 🧭 使用流程")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ① 輸入資料")
    st.write("填寫 App 屬性與必要欄位。")

with col2:
    st.markdown("### ② 驗證輸入")
    st.write("確認輸入資料符合系統驗證規則。")

with col3:
    st.markdown("### ③ 查看結果")
    st.write("查看預測結果及相關模型說明。")

render_footer()