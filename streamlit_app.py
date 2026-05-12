import streamlit as st

# ===================== 页面全局样式 深色+白色字体 =====================
st.set_page_config(page_title="太阳能路灯专业配置计算器", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #121212; color: white; }
    h1, h2, h3, h4, h5, p, label, div, span, pre { color: white !important; }
    .stSlider, .stNumberInput, .stSelectbox { background-color: #1e1e1e; }
    div[data-baseweb="input"], div[data-baseweb="select"] { background-color: #1e1e1e; color:white; }
    .result-box { background-color:#1e1e1e; padding:20px; border-radius:10px; margin-top:15px; }
    .report-box { background-color:#1e1e1e; color:white !important; padding:20px; border-radius:10px; margin-top:15px; }
</style>
""", unsafe_allow_html=True)

st.title("🌞 太阳能路灯专业配置计算器（可自定义调光+标书报告）")

# ===================== 1. 基础硬件参数 =====================
st.subheader("📌 基础硬件参数")
col1, col2, col3 = st.columns(3)
with col1:
    lamp_power = st.number_input("灯具额定功率 (W)", min_value=20, max_value=200, value=80, step=5)
    batt_ah    = st.number_input("电池容量 (Ah)", min_value=10, max_value=200, value=60, step=2)
with col2:
    batt_volt  = st.selectbox("电池额定电压 (V)", [12.8, 25.6], index=0)
    panel_wp   = st.number_input("太阳能板功率 (Wp)", min_value=50, max_value=400, value=150, step=10)
with col3:
    total_light_h = st.number_input("照明总时长 (h)", min_value=4, max_value=14, value=10, step=1)

st.markdown("---")

# ===================== 2. 智能调光模式（自由时长，不强制12h） =====================
st.subheader("⚙️ 智能调光模式设置（自由时长，无强制限制）")
c1, c2, c3 = st.columns(3)
with c1:
    t1_h = st.number_input("第一时段时长 (h)", min_value=1, max_value=14, value=2)
    t1_pct = st.number_input("第一时段功率占比 (%)", min_value=10, max_value=100, value=100)
with c2:
    t2_h = st.number_input("第二时段时长 (h)", min_value=1, max_value=14, value=3)
    t2_pct = st.number_input("第二时段功率占比 (%)", min_value=10, max_value=80, value=50)
with c3:
    t3_h = st.number_input("第三时段时长 (h)", min_value=1, max_value=14, value=5)
    t3_pct = st.number_input("第三时段功率占比 (%)", min_value=5, max_value=50, value=20)

st.markdown("---")

# ===================== 3. 地区 & 效率 & 阴雨天 =====================
st.subheader("🌍 地区日照 & 效率 & 阴雨天设置")
cc1, cc2, cc3 = st.columns(3)
with cc1:
    sun_hour = st.number_input("当地有效日照时长 (h)", min_value=3.0, max_value=7.0, value=5.0, step=0.1)
    cloudy_days = st.number_input("要求阴雨天保底续航天数", min_value=1.0, max_value=5.0, value=1.5, step=0.5)
with cc2:
    charge_eff = st.number_input("充电综合效率", min_value=0.6, max_value=0.95, value=0.80, step=0.01)
    dod_limit  = st.number_input("电池允许最大放电深度DOD", min_value=0.6, max_value=0.95, value=0.90, step=0.01)
with cc3:
    area_type = st.selectbox("地区类型", ["普通地区","多雨阴湿地区","高原强日照地区"], index=0)

st.markdown("---")

# ===================== 4. 核心自动计算 =====================
p1_real = lamp_power * t1_pct / 100
p2_real = lamp_power * t2_pct / 100
p3_real = lamp_power * t3_pct / 100

daily_consume_wh = p1_real * t1_h + p2_real * t2_h + p3_real * t3_h

batt_total_wh = batt_ah * batt_volt
batt_usable_wh = batt_total_wh * dod_limit

panel_daily_charge_wh = panel_wp * sun_hour * charge_eff
actual_backup_days = batt_usable_wh / daily_consume_wh

need_batt_wh = daily_consume_wh * cloudy_days / dod_limit
need_batt_ah = need_batt_wh / batt_volt
need_panel_whp = daily_consume_wh / (sun_hour * charge_eff)

# ===================== 5. 实时计算结果 =====================
st.markdown(f"""
<div class="result-box">
<h3>📊 实时计算结果</h3>
• 第一段：{t1_h}h × {t1_pct}% → {p1_real:.1f}W<br>
• 第二段：{t2_h}h × {t2_pct}% → {p2_real:.1f}W<br>
• 第三段：{t3_h}h × {t3_pct}% → {p3_real:.1f}W<br>
<hr>
• 日均耗电量：<b>{daily_consume_wh:.1f} Wh</b><br>
• 电池可用容量：<b>{batt_usable_wh:.1f} Wh</b><br>
• 太阳能日充电：<b>{panel_daily_charge_wh:.1f} Wh</b><br>
• 实际续航：<b>{actual_backup_days:.2f} 天</b>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===================== 6. 计算公式 =====================
formula_text = f"""
### 📐 全套计算公式
1. 分段功率：
- {lamp_power}W × {t1_pct}% = {p1_real:.1f}W
- {lamp_power}W × {t2_pct}% = {p2_real:.1f}W
- {lamp_power}W × {t3_pct}% = {p3_real:.1f}W

2. 日耗电量：
({p1_real:.1f}×{t1_h}) + ({p2_real:.1f}×{t2_h}) + ({p3_real:.1f}×{t3_h}) = {daily_consume_wh:.1f}Wh

3. 电池可用容量：
{batt_ah}Ah × {batt_volt}V × {dod_limit:.2f} = {batt_usable_wh:.1f}Wh

4. 续航天数：
{batt_usable_wh:.1f} ÷ {daily_consume_wh:.1f} = {actual_backup_days:.2f}天
"""

st.markdown(f"""
<div class="result-box">
<h3>📐 自动生成计算公式</h3>
{formula_text}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===================== 7. 标书报告（深色背景） =====================
report = f"""
# 太阳能路灯配置测算报告
## 一、基础参数
- 灯具功率：{lamp_power}W
- 电池：{batt_volt}V {batt_ah}Ah
- 太阳能板：{panel_wp}Wp
- 照明总时长：{total_light_h}小时
- 应用地区：{area_type}
- 有效日照：{sun_hour}h
- 设计阴雨天续航：{cloudy_days}天

## 二、智能调光模式
1. 第1时段：{t1_h}小时 {t1_pct}% 功率 → {p1_real:.1f}W
2. 第2时段：{t2_h}小时 {t2_pct}% 功率 → {p2_real:.1f}W
3. 第3时段：{t3_h}小时 {t3_pct}% 功率 → {p3_real:.1f}W

## 三、能耗测算
- 日均耗电量：{daily_consume_wh:.1f}Wh
- 电池可用容量：{batt_usable_wh:.1f}Wh
- 日充电量：{panel_daily_charge_wh:.1f}Wh
- 实际续航：{actual_backup_days:.2f}天

## 四、配置建议
"""

if actual_backup_days >= cloudy_days and panel_daily_charge_wh >= daily_consume_wh:
    report += "✅ 配置完全满足要求！"
elif actual_backup_days >= cloudy_days:
    report += f"⚠️ 续航足够，但充电不足，建议太阳能板≥{need_panel_whp:.0f}Wp"
elif panel_daily_charge_wh >= daily_consume_wh:
    report += f"⚠️ 充电足够，但续航不足，建议电池≥{need_batt_ah:.0f}Ah"
else:
    report += f"❌ 需升级：太阳能板≥{need_panel_whp:.0f}Wp + 电池≥{need_batt_ah:.0f}Ah"

st.markdown(f"""
<div class="report-box">
<h3>📄 标书专用报告</h3>
<pre style="white-space:pre-wrap;">{report}</pre>
</div>
""", unsafe_allow_html=True)
