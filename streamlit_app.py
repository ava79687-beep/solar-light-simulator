import streamlit as st
import plotly.graph_objects as go

# 1. 全局配置：深色主题 + 白色字体
st.set_page_config(page_title="太阳能路灯配置对比模拟器", layout="wide")
st.markdown("""
    <style>
    /* 全局背景和字体 */
    .stApp {
        background-color: #1a1a1a;
        color: white;
    }
    /* 所有文本元素强制白色 */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown, .stMetric, .stSlider, .stButton {
        color: white !important;
    }
    /* 按钮样式 */
    .stButton>button {
        background-color: #3a3f58;
        color: white !important;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 16px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #4a517a;
    }
    /* 滑块样式 */
    .stSlider>div>div>div {
        background-color: #4169e1;
    }
    /* 信息卡片 */
    .info-card {
        background-color: #2d2d2d;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# 标题
st.title("太阳能路灯配置对比模拟器")

# ------------------- 方案定义 -------------------
# 每个方案包含：功率数据、耗电量、说明、计算公式
schemes = {
    "方案一：高性能": {
        "power": [100, 100, 100, 100, 100, 100, 30, 30, 30, 30, 30, 30],
        "wh": 78,
        "desc": "前6小时100%高亮，后6小时30%亮度，优先保证前半夜照明效果",
        "formula": """
        **日耗电量计算：**
        (100% × 6h + 30% × 6h) × 10W = (6 + 1.8) × 10W = 78 Wh
        """
    },
    "方案二：最优推荐": {
        "power": [90, 90, 90, 90, 40, 40, 40, 40, 40, 40, 40, 40],
        "wh": 66,
        "desc": "前4小时90%高亮，后8小时40%亮度，兼顾亮度与续航平衡",
        "formula": """
        **日耗电量计算：**
        (90% × 4h + 40% × 8h) × 10W = (3.6 + 3.2) × 10W = 68 Wh
        """
    },
    "方案三：最高性能": {
        "power": [80, 80, 80, 80, 80, 80, 40, 40, 40, 40, 40, 40],
        "wh": 72,
        "desc": "前6小时持续80%高亮，后6小时维持40%亮度，整体输出均匀",
        "formula": """
        **日耗电量计算：**
        (80% × 6h + 40% × 6h) × 10W = (4.8 + 2.4) × 10W = 72 Wh
        """
    }
}

# ------------------- 方案切换 -------------------
col1, col2, col3 = st.columns(3)
with col1:
    btn1 = st.button("方案一：高性能", key="btn1")
with col2:
    btn2 = st.button("方案二：最优推荐", key="btn2")
with col3:
    btn3 = st.button("方案三：最高性能", key="btn3")

# 默认选中方案三
if not (btn1 or btn2 or btn3):
    selected = "方案三：最高性能"
elif btn1:
    selected = "方案一：高性能"
elif btn2:
    selected = "方案二：最优推荐"
else:
    selected = "方案三：最高性能"

# ------------------- 显示方案信息和公式 -------------------
st.markdown(f"""
<div class="info-card">
    <h4>当前方案：{selected} | 预估日耗电量：{schemes[selected]['wh']} Wh</h4>
</div>
""", unsafe_allow_html=True)

# 显示计算公式
st.markdown(f"""
<div class="info-card">
    <h4 style="color: #a9bfff;">📐 耗电量计算公式</h4>
    {schemes[selected]['formula']}
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
