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

setup_page("es2 × es3 Prediction Comparison", "📊")

page_header(
    "📊 es2 × es3 Prediction Comparison",
    "Independent Feature Inputs",
    "es2 and es3 are independent models with different feature sets. "
    "Their inputs are not mapped or merged.",
)

st.write(
    "本頁分別使用 es2 與 es3 的正式模型，"
    "根據各自的輸入特徵產生 App Success Classification"
    "（App 成功分類）預測結果。"
)


# ==========================================
# Load Formal Models
# ==========================================

ES2_PREPROCESSOR_PATH = (
    BASE_DIR / "es2" / "models" / "preprocessor.pkl"
)

ES2_MODEL_PATH = (
    BASE_DIR / "es2" / "models" / "tuned_decision_tree.pkl"
)

ES3_MODEL_PATH = (
    BASE_DIR / "es3" / "models" / "best_dt_tuned_pipeline.pkl"
)


@st.cache_resource
def load_formal_models(
    es2_preprocessor_path,
    es2_model_path,
    es3_model_path,
):
    es2_preprocessor = joblib.load(es2_preprocessor_path)
    es2_model = joblib.load(es2_model_path)
    es3_model = joblib.load(es3_model_path)

    return es2_preprocessor, es2_model, es3_model


for path in [
    ES2_PREPROCESSOR_PATH,
    ES2_MODEL_PATH,
    ES3_MODEL_PATH,
]:
    if not path.exists():
        st.error(f"找不到檔案：{path}")
        st.stop()


try:
    es2_preprocessor, es2_model, es3_model = load_formal_models(
        str(ES2_PREPROCESSOR_PATH),
        str(ES2_MODEL_PATH),
        str(ES3_MODEL_PATH),
    )

except Exception as e:
    st.error("Model 載入失敗。")
    st.exception(e)
    st.stop()


st.success("Formal es2 / es3 models loaded successfully.")

st.divider()


# ==========================================
# Research Target
# ==========================================

render_target_definition()

st.divider()


# ==========================================
# Independent Feature Input Form
# ==========================================

st.markdown("## App Feature Inputs")

CONTENT_RATINGS = [
    "Everyone",
    "Everyone 10+",
    "Teen",
    "Mature 17+",
    "Adults only 18+",
    "Unrated",
]


with st.form("es2_es3_comparison_form"):

    # ======================================
    # es2 — 11 Features
    # ======================================

    st.markdown("### es2 — 11 Features")

    st.caption(
        "輸入 es2 專屬的 11 個 Features。"
        "這些欄位僅供 es2 模型使用。"
    )

    # Row 1
    col1, col2, col3 = st.columns(3)

    with col1:
        es2_category = st.selectbox(
            "es2 Category",
            ["ART_AND_DESIGN", "ARTIFICIAL_INTELLIGENCE"],
            key="es2_category",
        )

    with col2:
        es2_type = st.selectbox(
            "es2 Type",
            ["Free", "Paid"],
            key="es2_type",
        )

    with col3:
        es2_content_rating = st.selectbox(
            "es2 Content Rating",
            CONTENT_RATINGS,
            key="es2_content_rating",
        )

    # Row 2
    col1, col2, col3 = st.columns(3)

    with col1:
        es2_genre_primary = st.selectbox(
            "es2 Genre_Primary",
            ["Art And Design", "Artificial Intelligence"],
            key="es2_genre_primary",
        )

    with col2:
        es2_genre_secondary = st.selectbox(
            "es2 Genre_Secondary",
            [
                "Action", "Board", "Card", "Casual",
                "Creativity", "Puzzle", "RPG",
                "Shooter", "Simulation", "Strategy",
            ],
            key="es2_genre_secondary",
        )

    with col3:
        es2_ad_supported = st.selectbox(
            "es2 Ad Supported",
            ["No", "Yes"],
            key="es2_ad_supported",
        )

    # Row 3
    col1, col2, col3 = st.columns(3)

    with col1:
        es2_size_mb = st.number_input(
            "es2 Size_MB",
            min_value=0.0,
            value=10.0,
            step=0.1,
            key="es2_size_mb",
        )

    with col2:
        es2_size_varies = st.number_input(
            "es2 Size_Varies",
            min_value=0,
            max_value=1,
            value=0,
            step=1,
            key="es2_size_varies",
        )

    with col3:
        es2_price = st.number_input(
            "es2 Price",
            min_value=0.0,
            value=0.0,
            step=0.01,
            key="es2_price",
        )

    # Row 4
    col1, col2, col3 = st.columns(3)

    with col1:
        es2_android_min_version = st.number_input(
            "es2 Android_Min_Version",
            min_value=0.0,
            value=4.4,
            step=0.1,
            key="es2_android_min_version",
        )

    with col2:
        es2_android_varies = st.number_input(
            "es2 Android_Varies",
            min_value=0,
            max_value=1,
            value=0,
            step=1,
            key="es2_android_varies",
        )

    # ======================================
    # es3 — 8 Features
    # ======================================

    st.divider()

    st.markdown("### es3 — 8 Features")

    st.caption(
        "輸入 es3 專屬的 8 個 Features。"
        "這些欄位僅供 es3 Pipeline 使用。"
    )

    # Row 1
    col1, col2, col3 = st.columns(3)

    with col1:
        es3_category = st.selectbox(
            "es3 Category",
            ["ART_AND_DESIGN", "ARTIFICIAL_INTELLIGENCE"],
            key="es3_category",
        )

    with col2:
        es3_size = st.text_input(
            "es3 Size",
            value="10.0M",
            key="es3_size",
        )

    with col3:
        es3_type = st.selectbox(
            "es3 Type",
            ["Free", "Paid"],
            key="es3_type",
        )

    # Row 2
    col1, col2, col3 = st.columns(3)

    with col1:
        es3_price = st.number_input(
            "es3 Price",
            min_value=0.0,
            value=0.0,
            step=0.01,
            key="es3_price",
        )

    with col2:
        es3_content_rating = st.selectbox(
            "es3 Content Rating",
            CONTENT_RATINGS,
            key="es3_content_rating",
        )

    with col3:
        es3_genres = st.text_input(
            "es3 Genres",
            value="Art And Design",
            key="es3_genres",
        )

    # Row 3
    col1, col2, col3 = st.columns(3)

    with col1:
        es3_android_ver = st.text_input(
            "es3 Android Ver",
            value="4.4 and up",
            key="es3_android_ver",
        )

    with col2:
        es3_ad_supported = st.selectbox(
            "es3 Ad Supported",
            ["No", "Yes"],
            key="es3_ad_supported",
        )

    # ======================================
    # Submit
    # ======================================

    st.divider()

    submitted = st.form_submit_button(
        "Predict App Success",
        use_container_width=True,
    )


# ==========================================
# Run Predictions Only After Submission
# ==========================================

if submitted:

    # --------------------------------------
    # es2 Input DataFrame
    # --------------------------------------

    es2_input = pd.DataFrame([{
        "Category": es2_category,
        "Size_MB": es2_size_mb,
        "Size_Varies": es2_size_varies,
        "Type": es2_type,
        "Price": es2_price,
        "Content Rating": es2_content_rating,
        "Genre_Primary": es2_genre_primary,
        "Genre_Secondary": es2_genre_secondary,
        "Android_Min_Version": es2_android_min_version,
        "Android_Varies": es2_android_varies,
        "Ad Supported": es2_ad_supported,
    }])

    # --------------------------------------
    # es3 Input DataFrame
    # --------------------------------------

    es3_input = pd.DataFrame([{
        "Category": es3_category,
        "Size": es3_size,
        "Type": es3_type,
        "Price": es3_price,
        "Content Rating": es3_content_rating,
        "Genres": es3_genres,
        "Android Ver": es3_android_ver,
        "Ad Supported": es3_ad_supported,
    }])

    # ======================================
    # Model Prediction
    # ======================================

    try:
        # es2 prediction
        es2_transformed = es2_preprocessor.transform(es2_input)

        es2_prediction = es2_model.predict(
            es2_transformed
        )[0]

        es2_p_not, es2_p_success = get_class_probabilities(
            es2_model,
            es2_transformed,
        )

        # es3 prediction
        es3_prediction = es3_model.predict(
            es3_input
        )[0]

        es3_p_not, es3_p_success = get_class_probabilities(
            es3_model,
            es3_input,
        )

    except Exception as e:
        st.error("Prediction failed.")
        st.exception(e)
        st.stop()

    # ======================================
    # Dynamic Gauge Dashboards
    # ======================================

    st.divider()

    st.markdown("## Dynamic Prediction Gauge Dashboard")

    st.caption(
        "兩個模型分別顯示各自的 P(Success)。"
        "儀表板僅呈現模型輸出的估計分數。"
    )

    gauge_col1, gauge_col2 = st.columns(2)

    # --------------------------------------
    # es2 Gauge
    # --------------------------------------

    with gauge_col1:

        st.markdown("### es2 — 11 Features")

        render_score_gauge(
            float(es2_p_success),
            title="es2 Model Score",
            subtitle="P(Success) — es2",
            key="es2_comparison_score_gauge",
        )

    # --------------------------------------
    # es3 Gauge
    # --------------------------------------

    with gauge_col2:

        st.markdown("### es3 — 8 Features")

        render_score_gauge(
            float(es3_p_success),
            title="es3 Model Score",
            subtitle="P(Success) — es3",
            key="es3_comparison_score_gauge",
        )

    # --------------------------------------
    # Wait for Gauge Animation
    # --------------------------------------

    # score_gauge.py 動畫時間約 6.5 秒
    # 額外保留 0.2 秒
    time.sleep(6.7)

    # ======================================
    # Prediction Results
    # ======================================

    st.divider()

    st.markdown("## Prediction Results")

    col_a, col_b = st.columns(2)

    with col_a:

        st.markdown("### es2 Prediction")

        render_prediction_result(
            es2_prediction,
            es2_p_not,
            es2_p_success,
            horizontal=False,
        )

    with col_b:

        st.markdown("### es3 Prediction")

        render_prediction_result(
            es3_prediction,
            es3_p_not,
            es3_p_success,
            horizontal=False,
        )

    # ======================================
    # Comparison
    # ======================================

    st.divider()

    st.markdown("## Comparison")

    if int(es2_prediction) == int(es3_prediction):

        st.info(
            "本次輸入下，es2 與 es3 產生相同的預測類別。"
            "這不代表兩個模型使用相同特徵或具有相同的預測行為。"
        )

    else:

        st.warning(
            "本次輸入下，es2 與 es3 產生不同的預測類別。"
            "由於兩個模型的 Feature Sets 與前處理流程不同，"
            "應將結果視為各自模型的獨立輸出。"
        )

    st.info(
        "es2 與 es3 目前採用獨立輸入及獨立模型，"
        "尚未建立 Feature Mapping。"
        "本頁比較的是同一次操作下兩個模型各自產生的預測結果，"
        "不是控制其他條件後的正式模型效能比較。"
    )

    # ======================================
    # Research Interpretation
    # ======================================

    st.markdown("## Research Interpretation")

    render_probability_disclaimer()

    # ======================================
    # Input Data Preview
    # ======================================

    with st.expander("View es2 Input DataFrame"):

        st.dataframe(
            es2_input,
            use_container_width=True,
        )

    with st.expander("View es3 Input DataFrame"):

        st.dataframe(
            es3_input,
            use_container_width=True,
        )

    with st.expander("View es2 Transformed Input Shape"):

        st.write(
            "es2 transformed input shape:",
            es2_transformed.shape,
        )


# ==========================================
# Footer
# ==========================================

render_footer()
