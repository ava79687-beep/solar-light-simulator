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

# ===================== 1. 基础参数输入区 =====================
st.subheader("📌 基础硬件参数")
col1, col2, col3 = st.columns(3)
with col1:
    lamp_power = st.number_input("灯具额定功率 (W)", min_value=20, max_value=200, value=80, step=5)
    batt_ah    = st.number_input("电池容量 (Ah)", min_value=10, max_value=200, value=60, step=2)
with col2:
    batt_volt  = st.selectbox("电池额定电压 (V)", [12.8, 25.6], index=0)
    panel_wp   = st.number_input("太阳能板功率 (Wp)", min_value=50, max_value=400, value=150, step=10)
with col3:
    total_light_h = st.number_input("整夜照明总时长 (h)", min_value=6, max_value=14, value=12, step=1)

st.markdown("---")

# ===================== 2. 三段智能调光设置 =====================
st.subheader("⚙️ 智能调光模式设置（12小时分段）")
c1, c2, c3 = st.columns(3)
with c1:
    t1_h = st.number_input("第一时段时长 (h)", min_value=1, max_value=6, value=2)
    t1_pct = st.number_input("第一时段功率占比 (%)", min_value=10, max_value=100, value=100)
with c2:
    t2_h = st.number_input("第二时段时长 (h)", min_value=2, max_value=8, value=4)
    t2_pct = st.number_input("第二时段功率占比 (%)", min_value=10, max_value=80, value=50)
with c3:
    t3_h = st.number_input("第三时段时长 (h)", min_value=2, max_value=10, value=6)
    t3_pct = st.number_input("第三时段功率占比 (%)", min_value=5, max_value=50, value=20)

# 校验时长总和
sum_t = t1_h + t2_h + t3_h
if sum_t != total_light_h:
    st.warning(f"⚠️ 三段时长总和 {sum_t}h 与总照明时长 {total_light_h}h 不一致，请调整！")

st.markdown("---")

# ===================== 3. 地区 & 效率 & 阴雨天自定义 =====================
st.subheader("🌍 地区日照 & 效率 & 阴雨天设置")
cc1, cc2, cc3 = st.columns(3)
with cc1:
    sun_hour = st.number_input("当地有效日照时长 (h)", min_value=3.0, max_value=7.0, value=5.0, step=0.1)
    cloudy_days = st.number_input("要求阴雨天保底续航天数", min_value=1.0, max_value=3.0, value=1.5, step=0.5)
with cc2:
    charge_eff = st.number_input("充电综合效率", min_value=0.6, max_value=0.95, value=0.80, step=0.01)
    dod_limit  = st.number_input("电池允许最大放电深度DOD", min_value=0.6, max_value=0.95, value=0.90, step=0.01)
with cc3:
    area_type = st.selectbox("地区类型", ["普通地区","多雨阴湿地区","高原强日照地区"], index=0)

st.markdown("---")

# ===================== 4. 核心自动计算 =====================
# 4.1 分段实际功率 & 日耗电量
p1_real = lamp_power * t1_pct / 100
p2_real = lamp_power * t2_pct / 100
p3_real = lamp_power * t3_pct / 100

daily_consume_wh = p1_real * t1_h + p2_real * t2_h + p3_real * t3_h

# 4.2 电池容量
batt_total_wh = batt_ah * batt_volt
batt_usable_wh = batt_total_wh * dod_limit

# 4.3 太阳能板日充电量
panel_daily_charge_wh = panel_wp * sun_hour * charge_eff

# 4.4 现有配置实际续航天数
actual_backup_days = batt_usable_wh / daily_consume_wh

# 4.5 满足阴雨天所需最小电池、最小光伏板
need_batt_wh = daily_consume_wh * cloudy_days / dod_limit
need_batt_ah = need_batt_wh / batt_volt

need_panel_whp = daily_consume_wh / (sun_hour * charge_eff)

# ===================== 5. 计算结果展示 =====================
st.markdown("""
<div class="result-box">
<h3>📊 实时计算结果</h3>
• 第一段实际功率：<b>%.1f W</b>  时长：%d h<br>
• 第二段实际功率：<b>%.1f W</b>  时长：%d h<br>
• 第三段实际功率：<b>%.1f W</b>  时长：%d h<br>
<hr>
• 灯具日均耗电量：<b>%.1f Wh/天</b><br>
• 电池总容量：<b>%.1f Wh</b>  可用容量(DOD=%.2f)：<b>%.1f Wh</b><br>
• 光伏板日充电能力：<b>%.1f Wh</b><br>
• 当前配置阴雨天实际续航：<b>%.2f 天</b>
</div>
""" % (p1_real,t1_h,p2_real,t2_h,p3_real,t3_h,
       daily_consume_wh,
       batt_total_wh,dod_limit,batt_usable_wh,
       panel_daily_charge_wh,
       actual_backup_days), unsafe_allow_html=True)

st.markdown("---")

# ===================== 6. 自动计算公式文本 =====================
formula_text = f"""
### 📐 全套计算公式
1. 分段实际功率：
- 第1段：{lamp_power}W × {t1_pct}% = {p1_real:.1f}W，工作{t1_h}h
- 第2段：{lamp_power}W × {t2_pct}% = {p2_real:.1f}W，工作{t2_h}h
- 第3段：{lamp_power}W × {t3_pct}% = {p3_real:.1f}W，工作{t3_h}h

2. 日均耗电量：
{daily_consume_wh:.1f} Wh = ({p1_real:.1f}×{t1_h}) + ({p2_real:.1f}×{t2_h}) + ({p3_real:.1f}×{t3_h})

3. 电池容量：
{batt_ah}Ah × {batt_volt}V = {batt_total_wh:.1f}Wh
可用容量 = {batt_total_wh:.1f} × {dod_limit:.2f} = {batt_usable_wh:.1f}Wh

4. 太阳能板日充电量：
{panel_wp}Wp × {sun_hour}h × {charge_eff:.2f} = {panel_daily_charge_wh:.1f}Wh

5. 阴雨天续航：
{actual_backup_days:.2f} 天 = {batt_usable_wh:.1f} ÷ {daily_consume_wh:.1f}

6. 满足{cloudy_days}天阴雨天所需最低配置：
- 需电池容量：{need_batt_wh:.1f}Wh → 对应 {batt_volt}V 需 {need_batt_ah:.1f}Ah
- 需光伏板功率：{need_panel_whp:.1f} Wp
"""

st.markdown(f"""
<div class="result-box">
<h3>📐 自动生成全套计算公式</h3>
{formula_text}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===================== 7. 标书专用正式报告（可直接复制给客户/投标） =====================
report = f"""
# 太阳能路灯配置测算报告
## 一、基础参数
- 灯具额定功率：{lamp_power} W
- 电池规格：{batt_volt}V / {batt_ah} Ah
- 太阳能板：{panel_wp} Wp
- 设计照明时长：{total_light_h} 小时
- 应用地区：{area_type}，有效日照 {sun_hour} h
- 设计阴雨天保底续航：{cloudy_days} 天

## 二、智能调光工作模式
1. 第一时段：{t1_h} 小时，输出功率 {t1_pct}%（{p1_real:.1f} W）
2. 第二时段：{t2_h} 小时，输出功率 {t2_pct}%（{p2_real:.1f} W）
3. 第三时段：{t3_h} 小时，输出功率 {t3_pct}%（{p3_real:.1f} W）

## 三、能耗与容量测算
- 日均工作耗电量：{daily_consume_wh:.1f} Wh
- 电池总储能：{batt_total_wh:.1f} Wh，按放电深度 {dod_limit:.2f} 可用容量 {batt_usable_wh:.1f} Wh
- 太阳能板日均充电量：{panel_daily_charge_wh:.1f} Wh
- 当前配置可连续阴雨天续航：{actual_backup_days:.2f} 天

## 四、配置评价与建议
"""

# 配置评价
if actual_backup_days >= cloudy_days and panel_daily_charge_wh >= daily_consume_wh:
    report += "✅ 现有配置满足设计要求，充电充足、阴雨天续航达标，可直接采用。"
elif actual_backup_days >= cloudy_days and panel_daily_charge_wh < daily_consume_wh:
    report += f"⚠️ 电池续航达标，但太阳能板充电不足，长期会亏电，建议加大光伏板至 {need_panel_whp:.0f}Wp 以上。"
elif actual_backup_days < cloudy_days and panel_daily_charge_wh >= daily_consume_wh:
    report += f"⚠️ 充电充足，但电池容量偏小，阴雨天续航不足，建议电池升级至 {need_batt_ah:.0f}Ah 以上。"
else:
    report += f"❌ 光伏板与电池均不满足设计要求，需同时加大太阳能板≥{need_panel_whp:.0f}Wp、电池≥{need_batt_ah:.0f}Ah。"

st.markdown(f"""
<div class="report-box">
<h3>📄 标书专用正式报告（可直接复制使用）</h3>
<pre style="white-space:pre-wrap; color:white !important;">{report}</pre>
</div>
""", unsafe_allow_html=True)
