"""
Dynamic Model-estimated Score Gauge
動態模型估計分數儀表板。

輸入 0.0 到 1.0 的模型輸出分數，
指針左右擺動後，於約 6.5 秒內逐漸收斂至目標分數。
注意：模型輸出分數不一定等於經校準的真實成功機率。
"""

import html
import math
import streamlit as st


def render_score_gauge(
    score: float,
    title: str = "Dynamic Model-estimated Score Gauge（動態模型估計分數儀表板）",
    subtitle: str = "指針左右擺動後逐漸收斂至模型輸出分數；此分數不代表經校準的真實成功機率。",
    key: str = "model_score_gauge",
) -> None:
    """繪製具有約 6.5 秒收斂動畫的半圓儀表板。"""

    # 1. 驗證模型輸出分數
    try:
        score = float(score)
    except (TypeError, ValueError):
        st.warning("無法顯示儀表板：模型輸出分數不是有效數值。")
        return

    if not math.isfinite(score) or not 0.0 <= score <= 1.0:
        st.warning("無法顯示儀表板：分數必須介於 0 與 1 之間。")
        return

    # 2. 計算目標角度
    percentage = score * 100
    target_angle = 180 - percentage * 1.8

    # 3. 避免標題、說明文字及 key 破壞 HTML 結構
    safe_key = html.escape(str(key), quote=True)
    safe_title = html.escape(str(title))
    safe_subtitle = html.escape(str(subtitle))

    # 4. 建立 HTML、SVG 儀表及 JavaScript 動畫
    gauge_html = f"""
    <div id="{safe_key}" style="
        width:100%;
        box-sizing:border-box;
        background:#030718;
        border:1px solid rgba(139,155,190,.18);
        border-radius:16px;
        padding:20px 18px 18px;
        color:#F7F9FF;
        font-family:Inter,'Noto Sans TC','Microsoft JhengHei',sans-serif;
        text-align:center;
        overflow:hidden;
        box-shadow:0 12px 34px rgba(12,18,48,.15);
    ">

      <div style="
          font-size:clamp(16px,2vw,21px);
          font-weight:800;
          line-height:1.5;
          margin-bottom:5px;
      ">
        {safe_title}
      </div>

      <div style="
          color:#FF5964;
          font-size:13px;
          font-weight:700;
          line-height:1.7;
          margin-bottom:4px;
      ">
        {safe_subtitle}
      </div>

      <svg viewBox="0 0 600 330"
           role="img"
           aria-label="模型估計分數儀表"
           style="
               display:block;
               width:100%;
               max-width:700px;
               height:auto;
               margin:0 auto;
           ">

        <!-- 儀表底色 -->
        <path d="M 90 225 A 210 210 0 0 1 510 225"
              fill="none"
              stroke="#25334A"
              stroke-width="38"/>

        <!-- 低分區：紅色 -->
        <path d="M 90 225 A 210 210 0 0 1 139.5 76.5"
              fill="none"
              stroke="#F04452"
              stroke-width="30"/>

        <!-- 中間區：黃色 -->
        <path d="M 139.5 76.5 A 210 210 0 0 1 300 15"
              fill="none"
              stroke="#FFD21F"
              stroke-width="30"/>

        <!-- 高分區：藍色 -->
        <path d="M 300 15 A 210 210 0 0 1 510 225"
              fill="none"
              stroke="#12A9E8"
              stroke-width="30"/>

        <!-- 儀表刻度 -->
        <g stroke="#E7EDF9" stroke-width="3">
          <line x1="90" y1="225" x2="120" y2="225"/>
          <line x1="151.5" y1="76.5" x2="172.7" y2="97.7"/>
          <line x1="300" y1="15" x2="300" y2="45"/>
          <line x1="448.5" y1="76.5" x2="427.3" y2="97.7"/>
          <line x1="510" y1="225" x2="480" y2="225"/>
        </g>

        <!-- 儀表刻度標籤 -->
        <g fill="#E6ECF8" font-size="17" font-weight="800">
          <text x="90" y="258" text-anchor="middle">0%</text>
          <text x="300" y="20" text-anchor="middle">50%</text>
          <text x="510" y="258" text-anchor="middle">100%</text>
        </g>

        <!-- 動態指針：JavaScript 更新終點座標 -->
        <line id="gauge-needle"
              x1="300"
              y1="225"
              x2="445"
              y2="225"
              stroke="#FF3028"
              stroke-width="10"
              stroke-linecap="round">
          <title>Model output score</title>
        </line>

        <!-- 指針中心 -->
        <circle cx="300" cy="225" r="15" fill="#FF3028"/>
        <circle cx="300" cy="225" r="6" fill="#FF574F"/>

      </svg>

      <!-- 即時顯示百分比 -->
      <div id="gauge-percentage" style="
          font-size:clamp(42px,7vw,76px);
          font-weight:900;
          letter-spacing:-1.5px;
          line-height:1.05;
          color:#FFD21F;
          font-variant-numeric:tabular-nums;
          margin-top:-2px;
      ">
        0.00%
      </div>

      <!-- 即時顯示模型分數 -->
      <div style="
          color:#BFC9DA;
          font-size:13px;
          margin-top:10px;
          line-height:1.6;
      ">
        Model Output Score:
        <span id="gauge-score">0.000000</span>
      </div>

    </div>

    <script>
    (() => {{
      const root = document.getElementById("{safe_key}");
      if (!root) return;

      const needle = root.querySelector("#gauge-needle");
      const percentageText = root.querySelector("#gauge-percentage");
      const scoreText = root.querySelector("#gauge-score");

      const targetScore = {score:.10f};
      const targetAngle = {target_angle:.10f};

      const centerX = 300;
      const centerY = 225;
      const radius = 145;

      // 動畫總時間：6.5 秒
      const duration = 6500;

      // 初始左右擺動角度
      const startAmplitude = 55;

      // 左右擺動次數控制
      const oscillations = 3.2;

      let startTime = null;

      function animate(timestamp) {{
        if (startTime === null) {{
          startTime = timestamp;
        }}

        const elapsed = timestamp - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // 阻尼效果：逐漸減少左右擺動幅度
        const damping = Math.pow(1 - progress, 3);

        const oscillation =
          startAmplitude *
          damping *
          Math.cos(2 * Math.PI * oscillations * progress);

        let angle;

        if (progress >= 1) {{
          // 動畫結束時，精確停在預測分數對應角度
          angle = targetAngle;
        }} else {{
          angle = targetAngle + oscillation;
        }}

        // 限制指針在 0 到 180 度範圍
        angle = Math.max(0, Math.min(180, angle));

        // 將角度轉換為 SVG 指針終點座標
        const radians = angle * Math.PI / 180;

        const needleX =
          centerX + radius * Math.cos(radians);

        const needleY =
          centerY - radius * Math.sin(radians);

        needle.setAttribute("x2", needleX.toFixed(3));
        needle.setAttribute("y2", needleY.toFixed(3));

        // 依照目前指針位置更新數字
        const currentScore = (180 - angle) / 180;
        const currentPercentage = currentScore * 100;

        percentageText.textContent =
          currentPercentage.toFixed(2) + "%";

        scoreText.textContent =
          currentScore.toFixed(6);

        if (progress < 1) {{
          requestAnimationFrame(animate);
        }} else {{
          // 確保最後顯示值與模型原始輸出一致
          percentageText.textContent =
            (targetScore * 100).toFixed(2) + "%";

          scoreText.textContent =
            targetScore.toFixed(6);
        }}
      }}

      requestAnimationFrame(animate);
    }})();
    </script>
    """

    # 5. 在 Streamlit 顯示儀表板
    st.components.v1.html(
        gauge_html,
        height=470,
        scrolling=False,
    )
