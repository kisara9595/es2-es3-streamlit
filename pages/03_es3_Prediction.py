import sys
import time
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

# ==========================================
# Project Paths and Imports
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ui_common import (
    setup_page,
    page_header,
    render_footer,
    render_target_definition,
    get_class_probabilities,
    render_prediction_result,
    render_probability_disclaimer,
)

from score_gauge import render_score_gauge


# ==========================================
# Page Setup
# ==========================================

setup_page("es3 Prediction | App Success Prediction", "📲")

page_header(
    "📲 es3 Prediction",
    "8 App Features",
    "Prediction results are model estimates, "
    "not guarantees of real-world app success.",
)

st.write(
    "本頁使用 es3 正式模型，根據 8 個 App Features "
    "進行 App Success Classification（App 成功分類）。"
)


# ==========================================
# Load Formal es3 Model Pipeline
# ==========================================

MODEL_PATH = (
    BASE_DIR
    / "es3"
    / "models"
    / "best_dt_tuned_pipeline.pkl"
)

if not MODEL_PATH.exists():
    st.error(f"找不到 Model：{MODEL_PATH}")
    st.stop()

try:
    model = joblib.load(MODEL_PATH)

except Exception as e:
    st.error("Model 載入失敗。")
    st.exception(e)
    st.stop()

st.success("Formal es3 model pipeline loaded successfully.")

st.divider()


# ==========================================
# Research Target
# ==========================================

render_target_definition()

st.divider()


# ==========================================
# Interactive Input Form
# 3 / 3 / 2 Layout
# ==========================================

st.markdown("## App Feature Inputs")
st.write("請輸入 es3 的 8 個 App Features。")

with st.form("es3_prediction_form"):

    # Row 1: Category / Size / Type
    col1, col2, col3 = st.columns(3)

    with col1:
        category = st.selectbox(
            "Category",
            ["ART_AND_DESIGN"],
        )

    with col2:
        size = st.number_input(
            "Size (MB)",
            min_value=0.0,
            value=10.0,
            step=1.0,
        )

    with col3:
        app_type = st.selectbox(
            "Type",
            ["Free", "Paid"],
        )

    # Row 2: Price / Content Rating / Genres
    col1, col2, col3 = st.columns(3)

    with col1:
        price = st.number_input(
            "Price",
            min_value=0.0,
            value=0.0,
            step=0.01,
        )

    with col2:
        content_rating = st.selectbox(
            "Content Rating",
            ["Everyone"],
        )

    with col3:
        genres = st.selectbox(
            "Genres",
            ["Art And Design"],
        )

    # Row 3: Android Ver / Ad Supported
    col1, col2, col3 = st.columns(3)

    with col1:
        android_ver = st.selectbox(
            "Android Ver",
            ["4.4 and up", "10 and up"],
        )

    with col2:
        ad_supported = st.selectbox(
            "Ad Supported",
            ["Yes", "No"],
        )

    submitted = st.form_submit_button(
        "Predict App Success",
        use_container_width=True,
    )


# ==========================================
# Prediction
# ==========================================

if submitted:

    # 建立 es3 的 8-feature input
    input_data = pd.DataFrame([{
        "Category": category,
        "Size": f"{size}M",
        "Type": app_type,
        "Price": price,
        "Content Rating": content_rating,
        "Genres": genres,
        "Android Ver": android_ver,
        "Ad Supported": ad_supported,
    }])

    # --------------------------------------
    # Run Formal Model Pipeline
    # --------------------------------------
    try:
        prediction = model.predict(input_data)[0]

        p_not, p_success = get_class_probabilities(
            model,
            input_data,
        )

    except Exception as e:
        st.error("Model prediction failed.")
        st.exception(e)
        st.stop()

    st.divider()

    # ======================================
    # Dynamic Score Gauge
    # Display Gauge Before Results
    # ======================================

    st.markdown("## Dynamic Model-estimated Score Gauge")

    render_score_gauge(
        float(p_success),
        title=(
            "Dynamic Model-estimated Score Gauge"
            "（動態模型估計分數儀表板）"
        ),
        subtitle=(
            "指針與百分比同步顯示模型估計分數；"
            "此分數不代表經校準的真實成功機率。"
        ),
        key="es3_model_score_gauge",
    )

    # 等待目前 score_gauge.py 的 6.5 秒動畫完成
    # 額外預留 0.2 秒
    time.sleep(6.7)

    # ======================================
    # Prediction Results
    # Show After Gauge Animation
    # ======================================

    st.divider()
    st.markdown("## Prediction Results")

    render_prediction_result(
        prediction,
        p_not,
        p_success,
    )

    # ======================================
    # Research Interpretation
    # ======================================

    st.markdown("## Research Interpretation")

    st.write(
        f"模型將此 App 分類為 Success = {int(prediction)}。"
        "以上結果是既有 es3 分類模型依據 8 個輸入特徵"
        "產生的預測結果。"
    )

    render_probability_disclaimer()

    st.info(
        "研究限制：模型的整體預測能力仍有限，"
        "單筆預測結果應視為模型分類結果，"
        "不應解釋為 App 成功的保證或因果關係。"
    )

    # ======================================
    # Input Data Preview
    # ======================================

    with st.expander("View Input DataFrame"):
        st.dataframe(
            input_data,
            use_container_width=True,
        )


# ==========================================
# Footer
# ==========================================

render_footer()
