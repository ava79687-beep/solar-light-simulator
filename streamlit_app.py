import streamlit as st

# 深色主题 + 白色字体
st.set_page_config(page_title="太阳能自动计算器", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #121212; color: white; }
    h1, h2, h3, h4, h5, p, label, div, span { color: white !important; }
    .stSlider, .stNumberInput { background-color: #1e1e1e; }
    div[data-baseweb="input"] { background-color: #1e1e1e; color:white; }
    .css-1v0mbdj { background-color:#1e1e1e; }
    .result-box { background-color:#1e1e1e; padding:20px; border-radius:10px; margin-top:20px; }
</style>
""", unsafe_allow_html=True)

st.title("🌞 太阳能路灯自动配置计算器")
st.subheader("自由调节参数 → 自动生成全套公式与配置建议")

# --------------------------
# 可调节参数
# --------------------------
col1, col2 = st.columns(2)
with col1:
    power = st.number_input("💡 灯具功率 (W)", min_value=10, max_value=200, value=80, step=10)
    panel = st.number_input("☀️ 太阳能板 (Wp)", min_value=30, max_value=400, value=150, step=10)
with col2:
    battery_ah = st.number_input("🔋 电池容量 (Ah)", min_value=10, max_value=200, value=60, step=10)
    voltage = st.selectbox("🔌 电池电压 (V)", [12.8, 25.6], index=0)
    hours = st.number_input("⏱️ 照明时长 (H)", min_value=4, max_value=14, value=12, step=1)

st.markdown("---")

# --------------------------
# 自动计算
# --------------------------
battery_wh = battery_ah * voltage
daily_wh = power * hours
charge_wh = panel * 5 * 0.8  # 5小时日照 × 0.8效率
backup_days = battery_wh / daily_wh

# --------------------------
# 结果展示
# --------------------------
st.markdown(f"""
<div class="result-box">
<h3>📊 自动计算结果</h3>
<b>1. 日耗电量：</b> {daily_wh} Wh<br>
<b>2. 电池总容量：</b> {battery_wh} Wh<br>
<b>3. 日充电量（理论）：</b> {charge_wh} Wh<br>
<b>4. 续航天数：</b> {backup_days:.1f} 天<br>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --------------------------
# 计算公式（自动生成）
# --------------------------
st.markdown(f"""
<div class="result-box">
<h3>📐 计算公式</h3>
✅ 日耗电量 = 功率 × 时长 = {power}W × {hours}h = <b>{daily_wh} Wh</b><br>
✅ 电池容量 = {battery_ah}Ah × {voltage}V = <b>{battery_wh} Wh</b><br>
✅ 充电能力 = {panel}Wp × 5h × 0.8 = <b>{charge_wh} Wh</b><br>
✅ 续航天数 = {battery_wh}Wh ÷ {daily_wh}Wh = <b>{backup_days:.1f} 天</b>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --------------------------
# 自动配置建议
# --------------------------
advice = ""
if backup_days < 1:
    advice = "⚠️ 电池太小，续航不足1天，必须加大电池！"
elif 1 <= backup_days < 2:
    advice = "✅ 标准配置，续航1天左右，适合普通项目"
elif 2 <= backup_days < 3:
    advice = "🔥 优质配置，续航2天，适合政府/难民营/高要求项目"
else:
    advice = "⭐ 顶级配置，续航≥3天，暴雨无忧！"

charge_ok = "✅ 充电足够" if charge_wh >= daily_wh else "⚠️ 充电不足，需要加大太阳能板"

st.markdown(f"""
<div class="result-box">
<h3>🎯 自动配置建议</h3>
{charge_ok}<br>
{advice}
</div>
""", unsafe_allow_html=True)
