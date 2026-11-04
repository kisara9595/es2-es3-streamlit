import sys
import json
import time
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

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
setup_page("es2 Prediction | App Success Prediction", "📱")

page_header(
    "📱 es2 Prediction",
    "11 App Features",
    "Prediction results are model estimates, "
    "not guarantees of real-world app success.",
)

st.write(
    "使用研究中已建立的 Preprocessing Pipeline "
    "與 Tuned Decision Tree 進行 App Success Classification。"
)


# ==========================================
# Load Formal Model Artifacts
# ==========================================
MODEL_DIR = BASE_DIR / "es2" / "models"
DATA_DIR = BASE_DIR / "es2" / "data"

PREPROCESSOR_PATH = MODEL_DIR / "preprocessor.pkl"
MODEL_PATH = MODEL_DIR / "tuned_decision_tree.pkl"
FEATURE_METADATA_PATH = DATA_DIR / "feature_metadata.json"

for path, label in [
    (PREPROCESSOR_PATH, "Preprocessor"),
    (MODEL_PATH, "Model"),
    (FEATURE_METADATA_PATH, "Feature Metadata"),
]:
    if not path.exists():
        st.error(f"找不到 {label}：{path}")
        st.stop()

try:
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(MODEL_PATH)

    with open(FEATURE_METADATA_PATH, "r", encoding="utf-8") as f:
        feature_metadata = json.load(f)

except Exception as e:
    st.error("Model 或 Feature Metadata 載入失敗。")
    st.exception(e)
    st.stop()

st.success("Model and feature metadata loaded successfully.")

if "all_research_features" not in feature_metadata:
    st.error("feature_metadata.json 缺少 'all_research_features' Key。")
    st.stop()

research_features = feature_metadata["all_research_features"]

if len(research_features) != 11:
    st.warning(
        f"目前 Metadata 中的 Research Features 數量為 "
        f"{len(research_features)}，預期為 11。"
    )

category_values = feature_metadata.get("category_values", {})


def get_category_values(feature_name):
    """從 feature_metadata.json 取得 categorical feature 的實際類別值。"""
    values = category_values.get(feature_name, [])
    return [] if values is None else values


def select_or_text(label, feature_name):
    """有類別值時使用下拉選單，否則使用文字輸入。"""
    options = get_category_values(feature_name)

    if options:
        return st.selectbox(label, options=options)

    return st.text_input(label)


# ==========================================
# Target Definition
# ==========================================
st.divider()
render_target_definition()
st.divider()


# ==========================================
# App Feature Inputs
# ==========================================
st.markdown("## App Feature Inputs")
st.write("請輸入 11 個可於早期取得的 App Features。")

with st.form("es2_prediction_form"):

    col1, col2, col3 = st.columns(3)

    with col1:
        category = select_or_text("Category", "Category")

    with col2:
        size_mb = st.number_input(
            "Size_MB",
            min_value=0.0,
            value=50.0,
            step=0.1,
        )

    with col3:
        size_varies = st.number_input(
            "Size_Varies",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=1.0,
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        app_type = select_or_text("Type", "Type")

    with col2:
        price = st.number_input(
            "Price",
            min_value=0.0,
            value=0.0,
            step=0.01,
        )

    with col3:
        content_rating = select_or_text(
            "Content Rating",
            "Content Rating",
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        genre_primary = select_or_text(
            "Genre_Primary",
            "Genre_Primary",
        )

    with col2:
        genre_secondary = select_or_text(
            "Genre_Secondary",
            "Genre_Secondary",
        )

    with col3:
        android_min_version = st.number_input(
            "Android_Min_Version",
            min_value=0.0,
            value=8.0,
            step=0.1,
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        android_varies = st.number_input(
            "Android_Varies",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=1.0,
        )

    with col2:
        ad_supported = select_or_text(
            "Ad Supported",
            "Ad Supported",
        )

    submitted = st.form_submit_button(
        "Predict App Success",
        use_container_width=True,
    )


# ==========================================
# Prediction
# ==========================================
if submitted:

    input_data = {
        "Category": category,
        "Size_MB": size_mb,
        "Size_Varies": size_varies,
        "Type": app_type,
        "Price": price,
        "Content Rating": content_rating,
        "Genre_Primary": genre_primary,
        "Genre_Secondary": genre_secondary,
        "Android_Min_Version": android_min_version,
        "Android_Varies": android_varies,
        "Ad Supported": ad_supported,
    }

    input_df = pd.DataFrame(
        [input_data],
        columns=research_features,
    )

    # --------------------------------------
    # Preprocessing
    # --------------------------------------
    try:
        X_transformed = preprocessor.transform(input_df)

    except Exception as e:
        st.error("Preprocessing failed.")
        st.exception(e)
        st.stop()

    # --------------------------------------
    # Model Prediction
    # --------------------------------------
    try:
        predicted_class = model.predict(X_transformed)[0]

    except Exception as e:
        st.error("Model prediction failed.")
        st.exception(e)
        st.stop()

    # --------------------------------------
    # Model Output Probabilities
    # --------------------------------------
    p_not, p_success = None, None

    if hasattr(model, "predict_proba"):
        try:
            p_not, p_success = get_class_probabilities(
                model,
                X_transformed,
            )

        except Exception:
            p_not, p_success = None, None

    st.divider()

    # ======================================
    # Gauge First, Results After Animation
    # ======================================
    if p_not is not None and p_success is not None:

        # 先顯示儀表，不立即顯示 Prediction Results
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
            key="es2_model_score_gauge",
        )

        # 等待動畫完成。
        # score_gauge.py 的動畫時間設定為 6500 毫秒；
        # 這裡多保留 0.2 秒，避免結果過早出現。
        time.sleep(6.7)

        # 指針動畫完成後，才顯示預測結果
        st.divider()
        st.markdown("## Prediction Results")

        render_prediction_result(
            predicted_class,
            p_not,
            p_success,
        )

    else:
        # 模型沒有可用的預測分數時，不等待動畫
        st.markdown("## Prediction Results")

        if int(predicted_class) == 1:
            st.success("Prediction Result: Success")
        else:
            st.warning("Prediction Result: Not Success")

        st.metric(
            "Predicted Class",
            int(predicted_class),
        )

        st.info(
            "目前模型未提供可用的 Model Output Score，"
            "因此無法顯示儀表板。"
        )

    # ======================================
    # Research Interpretation
    # ======================================
    st.markdown("## Research Interpretation")

    st.write(
        f"模型將此 App 分類為 Success = {int(predicted_class)}。"
        "此結果表示依據研究中納入的 11 個 "
        "early-available App Features，"
        f"此 Decision Tree 模型將該輸入樣本分類至 "
        f"Success = {int(predicted_class)}。"
    )

    if p_not is not None and p_success is not None:
        render_probability_disclaimer()

    st.info(
        "研究限制：本模型的整體 Test Set 預測能力仍有限，"
        "因此單筆預測結果應視為模型分類結果，"
        "不應解釋為 App 成功的保證或因果關係。"
    )

    # ======================================
    # Input Data and Transformed Shape
    # ======================================
    with st.expander("View Input DataFrame"):
        st.dataframe(
            input_df,
            use_container_width=True,
        )

    with st.expander("View Transformed Input Shape"):
        st.write(
            "Transformed Feature Count:",
            X_transformed.shape[1],
        )


# ==========================================
# Model Details
# ==========================================
st.divider()
st.markdown("## Model Details")

with st.expander("Model Information"):

    st.write("Model:", type(model).__name__)
    st.write("Preprocessor:", type(preprocessor).__name__)

    if hasattr(model, "n_features_in_"):
        st.write(
            "Model Input Features:",
            model.n_features_in_,
        )

    if hasattr(model, "classes_"):
        st.write(
            "Classes:",
            model.classes_.tolist(),
        )

    for attr in [
        "max_depth",
        "min_samples_leaf",
        "min_samples_split",
        "class_weight",
    ]:
        if hasattr(model, attr):
            st.write(
                f"{attr}:",
                getattr(model, attr),
            )


with st.expander("Research Features Used by This Model"):

    for i, feature in enumerate(research_features, start=1):
        st.write(f"{i}. {feature}")


render_footer()
