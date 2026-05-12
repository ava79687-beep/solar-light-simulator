import streamlit as st
import plotly.graph_objects as go

# 全局配置：深色主题 + 白色字体
st.set_page_config(page_title="太阳能路灯配置对比模拟器", layout="wide")
st.markdown("""
    <style>
    .stApp {background-color: #1a1a1a; color: white;}
    h1, h2, h3, h4, p, span, label, .stMarkdown, .stMetric, .stSlider, .stButton {color: white !important;}
    .stButton>button {
        background-color: #3a3f58; color: white !important; border-radius: 8px;
        padding: 10px 24px; font-size: 16px; border: none; width: 100%;
    }
    .stButton>button:hover {background-color: #4a517a;}
    .stSlider>div>div>div {background-color: #4169e1;}
    .info-card {background-color: #2d2d2d; padding: 15px; border-radius: 10px; margin: 10px 0;}
    .formula-box {background-color: #f0f0f0; color: black !important; padding: 15px; border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

# 标题
st.title("太阳能路灯配置对比模拟器")

# ------------------- 按你的标书定义3个方案 -------------------
schemes = {
    "方案一：卡线中标型（高性价比）": {
        "power": [100,100, 50,50,50,50, 20,20,20,20,20,20],
        "wh": 440,
        "desc": "主打价格优势，参数刚好跨过标书门槛，利用智能时控+雷达感应确保12小时亮灯。",
        "formula": """
        **1. 每日耗电量计算：**  
        (80W × 2h) + (40W × 4h) + (20W × 6h) = 160 + 160 + 120 = **440 Wh/天**  

        **2. 电池容量计算：**  
        440Wh ÷ 0.9（放电深度） = 488 Wh → 采用 12.8V 42Ah 磷酸铁锂电池（537Wh）

        **3. 太阳能板计算：**  
        440Wh ÷ (5h有效日照 × 0.8充电效率) = 110 Wp → 采用 110Wp 太阳能板  

        ✅ 最终配置：80W灯头 + 110Wp板 + 12.8V 42Ah电池
        """
    },
    "方案二：最优推荐型（平衡成本与可靠性）": {
        "power": [100,100,100,100, 50,50,50,50, 30,30,30,30],
        "wh": 576,
        "desc": "造价不高，但提供更长亮灯冗余和更高平均亮度，能抵抗1-2天阴雨天，适合难民营治安环境。",
        "formula": """
        **1. 每日耗电量计算：**  
        (80W × 4h) + (40W × 4h) + (24W × 4h) = 320 + 160 + 96 = **576 Wh/天**  

        **2. 电池容量计算：**  
        576Wh ÷ 0.9 = 640 Wh → 放大到768Wh（1.5天阴雨天续航）→ 12.8V 60Ah电池

        **3. 太阳能板计算：**  
        576Wh ÷ (5h × 0.8) = 144 Wp → 取整 150Wp  

        ✅ 最终配置：80W灯头 + 150Wp板 + 12.8V 60Ah电池
        """
    },
    "方案三：极致性能型（无视阴雨天）": {
        "power": [80,80,80,80,80,80, 40,40,40,40,40,40],
        "wh": 576,
        "desc": "二体式首选，支持2-3个连续阴雨天100%亮灯，适合预算充足或要求严苛的项目。",
        "formula": """
        **1. 每日耗电量计算：**  
        (64W × 6h) + (32W × 6h) = 384 + 192 = **576 Wh/天**  

        **2. 电池容量计算（2天续航）：**  
        (576Wh × 2天) ÷ 0.9 = 1280 Wh → 12.8V 100Ah电池

        **3. 太阳能板计算：**  
        需同时补充当日用电+亏空，建议 200Wp 太阳能板  

        ✅ 最终配置：80W灯头 + 200Wp板 + 12.8V 100Ah电池（二体式推荐）
        """
    }
}

# ------------------- 方案切换按钮 -------------------
col1, col2, col3 = st.columns(3)
with col1:
    btn1 = st.button("方案一：卡线中标型", key="btn1")
with col2:
    btn2 = st.button("方案二：最优推荐型", key="btn2")
with col3:
    btn3 = st.button("方案三：极致性能型", key="btn3")

# 默认选中方案三
if not (btn1 or btn2 or btn3):
    selected = "方案三：极致性能型（无视阴雨天）"
elif btn1:
    selected = "方案一：卡线中标型（高性价比）"
elif btn2:
    selected = "方案二：最优推荐型（平衡成本与可靠性）"
else:
    selected = "方案三：极致性能型（无视阴雨天）"

# ------------------- 显示方案信息 -------------------
st.markdown(f"""
<div class="info-card">
    <h3>当前方案：{selected} | 预估日耗电量：{schemes[selected]['wh']} Wh</h3>
</div>
""", unsafe_allow_html=True)

# 显示完整计算公式和配置
st.markdown(f"""
<div class="info-card">
    <h4 style="color: #a9bfff;">📐 耗电量 & 配置计算过程</h4>
    <div class="formula-box">
        {schemes[selected]['formula']}
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------- 12小时功率柱状图 -------------------
hours = [f"第{i}小时" for i in range(1,13)]
power_data = schemes[selected]["power"]

fig = go.Figure(data=[
    go.Bar(
        x=hours,
        y=power_data,
        marker_color="#a9bfff",
        text=[f"{p}%" for p in power_data],
        textposition="outside"
    )
])

fig.update_layout(
    title="输出功率(%)",
    yaxis=dict(range=[0, 100], tickvals=[0,20,40,60,80,100], color="white"),
    xaxis=dict(color="white"),
    plot_bgcolor="#1a1a1a",
    paper_bgcolor="#1a1a1a",
    font_color="white",
    title_font_color="white",
    bargap=0.2
)

st.plotly_chart(fig, use_container_width=True)

# ------------------- 运行逻辑说明 -------------------
st.markdown(f"""
<div class="info-card">
    <h4 style="color: #a9bfff;">运行逻辑策略 - {selected.split("：")[1]}</h4>
    <p>{schemes[selected]['desc']}</p>
</div>
""", unsafe_allow_html=True)

# ------------------- 电池寿命模拟器 -------------------
st.title("LiFePO4 电池消耗分析器")

# 放电深度滑块
dod = st.slider("放电深度 (DoD %)", min_value=0, max_value=100, value=77)
soc = 100 - dod

# 循环寿命估算（磷酸铁锂标准曲线）
if dod <= 20:
    cycle = 12000
elif dod <= 40:
    cycle = 10000 - (dod-20)*200
elif dod <= 60:
    cycle = 6000 - (dod-40)*100
elif dod <= 80:
    cycle = 4000 - (dod-60)*70
else:
    cycle = 2600 - (dod-80)*30
cycle = max(cycle, 2000)

# 电池状态显示
col1, col2, col3 = st.columns(3)
col1.metric("已完成放电", f"{dod}%")
col2.metric("剩余电量", f"{soc}%")
col3.metric("预估循环寿命", f"{cycle} 次")

# 寿命曲线
dod_list = list(range(0,101,20))
cycle_list = []
for d in dod_list:
    if d <= 20:
        c = 12000
    elif d <= 40:
        c = 10000 - (d-20)*200
    elif d <= 60:
        c = 6000 - (d-40)*100
    elif d <= 80:
        c = 4000 - (d-60)*70
    else:
        c = 2600 - (d-80)*30
    cycle_list.append(max(c, 2000))

battery_fig = go.Figure(data=[
    go.Scatter(
        x=dod_list,
        y=cycle_list,
        mode="lines+markers",
        line=dict(color="#a9bfff", width=3),
        fill='tozeroy',
        fillcolor="rgba(169, 191, 255, 0.2)"
    )
])

battery_fig.update_layout(
    title="循环寿命 (次)",
    yaxis=dict(color="white"),
    xaxis=dict(title="放电深度 DoD (%)", color="white"),
    plot_bgcolor="#1a1a1a",
    paper_bgcolor="#1a1a1a",
    font_color="white",
    title_font_color="white"
)

st.plotly_chart(battery_fig, use_container_width=True)
