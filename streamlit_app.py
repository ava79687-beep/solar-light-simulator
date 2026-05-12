import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 设置页面配置
st.set_page_config(
    page_title="太阳能路灯智能模拟器",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 强制深色模式样式
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stSlider [data-baseweb="slider"] {
        width: 90%;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🌙 太阳能路灯系统模拟器")
    st.sidebar.header("⚙️ 系统参数配置")

    # --- 侧边栏控制 ---
    preset = st.sidebar.selectbox(
        "选择照明方案",
        ["标准节能模式", "全功率模式", "极低功耗模式"]
    )

    # 根据方案调整初始值
    defaults = {
        "标准节能模式": (60, 100, 10),
        "全功率模式": (100, 200, 12),
        "极低功耗模式": (30, 80, 8)
    }
    d_p, d_b, d_h = defaults[preset]

    led_power = st.sidebar.slider("LED 额定功率 (W)", 10, 300, d_p)
    battery_cap = st.sidebar.slider("电池容量 (Ah)", 20, 500, d_b)
    working_hours = st.sidebar.slider("每日工作时长 (h)", 4, 15, d_h)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔋 电池环境参数")
    env_temp = st.sidebar.slider("环境平均温度 (°C)", -20, 50, 25)
    dod = st.sidebar.slider("放电深度 (DoD %)", 10, 90, 80)

    # --- 核心逻辑计算 ---
    # 模拟功率损耗与转化
    system_voltage = 12.8  # 磷酸铁锂标准电压
    daily_consumption = (led_power * working_hours) / system_voltage # Ah
    days_autonomy = battery_cap * (dod / 100) / daily_consumption

    # 电池寿命模拟 (简易阿伦尼乌斯模型)
    # 基础循环次数 2000次，温度每升高10度寿命减半
    base_cycles = 2500 if dod < 50 else 2000
    temp_factor = 2 ** ((env_temp - 25) / 10) if env_temp > 25 else 1.0
    estimated_years = (base_cycles / temp_factor) / 365

    # --- 界面展示 ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("每日耗电量", f"{daily_consumption:.1f} Ah")
    col2.metric("阴雨天维持天数", f"{days_autonomy:.1f} 天")
    col3.metric("预计电池寿命", f"{estimated_years:.1f} 年")
    col4.metric("系统电压", f"{system_voltage} V")

    # --- 图表：24小时功率变化 ---
    st.subheader("📊 24小时实时功率模拟")
    
    hours = np.arange(24)
    # 模拟太阳能充电功率曲线 (正弦波)
    charge_power = np.where((hours > 6) & (hours < 18), 
                           (led_power * 1.5) * np.sin(np.pi * (hours - 6) / 12), 0)
    # 模拟路灯负载功率曲线
    load_power = np.where((hours >= 18) | (hours <= 18 - working_hours if 18-working_hours >=0 else 0), 
                          0, led_power)
    # 处理跨天逻辑
    load_power = np.zeros(24)
    for h in range(24):
        if h >= 18 or h < (18 + working_hours) % 24:
            if h >= 18 or h < (18 + working_hours - 24):
                load_power[h] = led_power

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hours, y=charge_power, name='光伏充电功率 (W)', line=dict(color='#FFA500', width=3)))
    fig.add_trace(go.Scatter(x=hours, y=load_power, name='路灯负载功率 (W)', line=dict(color='#00BFFF', width=3), fill='tozeroy'))
    
    fig.update_layout(
        template="plotly_dark",
        xaxis_title="时间 (24小时制)",
        yaxis_title="功率 (W)",
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- 下方详情 ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📋 仿真原始数据")
        df = pd.DataFrame({
            "时间 (时)": hours,
            "充电功率 (W)": charge_power.round(1),
            "负载功率 (W)": load_power.round(1)
        })
        st.dataframe(df, height=300, use_container_width=True)
    
    with c2:
        st.subheader("💡 系统建议")
        if days_autonomy < 3:
            st.warning("⚠️ 当前配置下，阴雨天储备不足，建议增大电池容量或降低功率。")
        else:
            st.success("✅ 系统配置稳健，能够应对连续3天的阴雨天气。")
            
        if env_temp > 40:
            st.error("🔥 环境温度过高，电池寿命将大幅缩减，请考虑增加散热或埋地处理。")
        
        st.info(f"配置摘要：该系统在 {dod}% 放电深度下，每日需补能约 {daily_consumption * system_voltage / 1000:.2f} kWh。")

if __name__ == "__main__":
    main()