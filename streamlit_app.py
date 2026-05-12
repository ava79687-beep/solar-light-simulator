import streamlit as st
import plotly.graph_objects as go

# ===================== 深色主题样式 =====================
st.set_page_config(page_title="太阳能路灯专业配置计算器", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #121212; color: white; }
    h1, h2, h3, h4, h5, p, label, div, span, pre { color: white !important; }
    .stSlider, .stNumberInput, .stSelectbox { background-color: #1e1e1e; }
    div[data-baseweb="input"], div[data-baseweb="select"] { background-color: #1e1e1e; color:white; }
    .result-box { background-color:#1e1e1e; padding:20px; border-radius:10px; margin-top:15px; }
    .report-box { background-color:#1e1e1e; color:white !important; padding:20px; border-radius:10px; margin-top:15px; }
    .ok-box { background-color:#0e3a24; padding:15px; border-radius:8px; margin-top:10px; }
    .warn-box { background-color:#3a2e0e; padding:15px; border-radius:8px; margin-top:10px; }
</style>
""", unsafe_allow_html=True)

st.title("太阳能路灯专业配置计算器（商用完整版）")

# ===================== 基础硬件参数 =====================
st.subheader("基础硬件参数")
col1, col2, col3 = st.columns(3)
with col1:
    lamp_power = st.number_input("灯具额定功率 (W)", min_value=20, max_value=200, value=80, step=5)
    batt_ah    = st.number_input("电池容量 (Ah)", min_value=10, max_value=200, value=60, step=2)
with col2:
    batt_volt  = st.selectbox("电池电压 (V)", [12.8, 25.6], index=0)
    panel_wp   = st.number_input("太阳能板 (Wp)", min_value=50, max_value=400, value=150, step=10)
with col3:
    total_light_h = st.number_input("照明总时长 (h)", min_value=4, max_value=14, value=10, step=1)

st.markdown("---")

# ===================== 智能调光模式设置 =====================
st.subheader("智能调光模式设置")
c1, c2, c3 = st.columns(3)
with c1:
    t1_h = st.number_input("第一时段 (h)", min_value=1, max_value=14, value=2)
    t1_pct = st.number_input("第一时段功率 (%)", min_value=10, max_value=100, value=100)
with c2:
    t2_h = st.number_input("第二时段 (h)", min_value=1, max_value=14, value=3)
    t2_pct = st.number_input("第二时段功率 (%)", min_value=10, max_value=80, value=50)
with c3:
    t3_h = st.number_input("第三时段 (h)", min_value=1, max_value=14, value=5)
    t3_pct = st.number_input("第三时段功率 (%)", min_value=5, max_value=50, value=20)

# ===================== 时长自动校验 =====================
sum_t = t1_h + t2_h + t3_h
st.markdown("---")
if sum_t != total_light_h:
    st.markdown(f"""<div class="warn-box">⚠️ 三段总时长：{sum_t}h → 与照明总时长 {total_light_h}h 不匹配，请修正！</div>""", unsafe_allow_html=True)
else:
    st.markdown(f"""<div class="ok-box">✅ 三段总时长：{sum_t}h → 匹配 {total_light_h}h，计算有效</div>""", unsafe_allow_html=True)

st.markdown("---")

# ===================== 地区 & 效率 & 阴雨天设置 =====================
st.subheader("地区 & 效率 & 阴雨天设置")
cc1, cc2, cc3 = st.columns(3)
with cc1:
    sun_hour = st.number_input("有效日照时长 (h)", min_value=3.0, max_value=7.0, value=5.0, step=0.1)
    cloudy_days = st.number_input("阴雨天续航天数", min_value=1.0, max_value=5.0, value=1.5, step=0.5)
with cc2:
    charge_eff = st.number_input("充电效率", min_value=0.6, max_value=0.95, value=0.80, step=0.01)
    dod_limit  = st.number_input("放电深度 DOD", min_value=0.6, max_value=0.95, value=0.90, step=0.01)
with cc3:
    area_type = st.selectbox("地区类型", ["普通地区","多雨阴湿地区","高原强日照地区"], index=0)

st.markdown("---")

# ===================== 核心自动计算 =====================
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

# ===================== 智能调光功率曲线图 =====================
st.subheader("智能调光功率曲线图")
hours_list = []
power_list = []
for i in range(t1_h):
    hours_list.append(f"{i+1}h")
    power_list.append(p1_real)
for i in range(t2_h):
    hours_list.append(f"{t1_h + i + 1}h")
    power_list.append(p2_real)
for i in range(t3_h):
    hours_list.append(f"{t1_h + t2_h + i + 1}h")
    power_list.append(p3_real)

fig = go.Figure(go.Bar(x=hours_list, y=power_list, marker_color="#4c84ff"))
fig.update_layout(
    plot_bgcolor="#121212", paper_bgcolor="#121212", font=dict(color="white"),
    xaxis_title="时间", yaxis_title="功率 (W)", height=380
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ===================== 电池续航 vs 充电对比图（已添加） =====================
st.subheader("⚖️ 电池续航与充电对比图")
compare_labels = ["日耗电量", "日充电量", "阴雨天所需电池", "现有可用电池"]
compare_values = [daily_consume_wh, panel_daily_charge_wh, need_batt_wh, batt_usable_wh]
colors = ["#ff4c4c", "#4cff4c", "#ffb34c", "#4c84ff"]

fig2 = go.Figure(go.Bar(x=compare_labels, y=compare_values, marker_color=colors))
fig2.update_layout(
    plot_bgcolor="#121212", paper_bgcolor="#121212", font=dict(color="white"),
    yaxis_title="Wh (瓦时)", height=380
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ===================== 实时计算结果 =====================
st.markdown(f"""
<div class="result-box">
<h3>实时计算结果</h3>
• 日均耗电量：<b>{daily_consume_wh:.1f} Wh</b><br>
• 电池可用容量：<b>{batt_usable_wh:.1f} Wh</b><br>
• 太阳能日充电：<b>{panel_daily_charge_wh:.1f} Wh</b><br>
• 实际阴雨天续航：<b>{actual_backup_days:.2f} 天</b>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===================== 自动计算公式 =====================
formula_text = f"""
### 全套自动计算公式
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
<h3>计算公式</h3>
{formula_text}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===================== 标书专用正式报告 =====================
report = f"""
太阳能路灯配置测算报告

一、基础参数
- 灯具功率：{lamp_power}W
- 电池：{batt_volt}V {batt_ah}Ah
- 太阳能板：{panel_wp}Wp
- 照明总时长：{total_light_h}小时
- 应用地区：{area_type}
- 有效日照：{sun_hour}h
- 设计阴雨天续航：{cloudy_days}天

二、智能调光模式
1. 第1时段：{t1_h}小时 {t1_pct}% → {p1_real:.1f}W
2. 第2时段：{t2_h}小时 {t2_pct}% → {p2_real:.1f}W
3. 第3时段：{t3_h}小时 {t3_pct}% → {p3_real:.1f}W

三、能耗测算
- 日均耗电量：{daily_consume_wh:.1f}Wh
- 电池可用容量：{batt_usable_wh:.1f}Wh
- 日充电量：{panel_daily_charge_wh:.1f}Wh
- 实际续航：{actual_backup_days:.2f}天

四、配置评价
"""

if actual_backup_days >= cloudy_days and panel_daily_charge_wh >= daily_consume_wh:
    report += "✅ 配置完全满足要求！"
elif actual_backup_days >= cloudy_days:
    report += f"⚠️ 续航足够，充电不足 → 建议太阳能板≥{need_panel_whp:.0f}Wp"
elif panel_daily_charge_wh >= daily_consume_wh:
    report += f"⚠️ 充电足够，续航不足 → 建议电池≥{need_batt_ah:.0f}Ah"
else:
    report += f"❌ 需升级：太阳能板≥{need_panel_whp:.0f}Wp + 电池≥{need_batt_ah:.0f}Ah"

# 显示报告（深色背景+白色文字，100%清晰）
st.subheader("标书专用正式报告")
st.markdown(f"""
<div class="report-box">
<pre style="white-space: pre-wrap; font-family: monospace; color: white !important;">{report}</pre>
</div>
""", unsafe_allow_html=True)

# 一键下载 TXT 报告（替代PDF，无需额外库）
st.download_button(
    label="下载报告（TXT文件）",
    data=report,
    file_name="太阳能路灯配置测算报告.txt",
    mime="text/plain"
)

st.markdown("---")
st.success("✅ 所有参数、图表、报告已自动更新完成！")
