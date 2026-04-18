import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.forecasting import forecast_temperature

# -------------------------------
# 🎨 PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Climate Analyzer", layout="wide")

# -------------------------------
# 🌙 CUSTOM DARK STYLE
# -------------------------------
st.markdown("""
    <style>
    body {background-color: #0e1117;}
    .metric-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #1c1f26;
        text-align: center;
        color: white;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌍 Climate Trend Analyzer")

# -------------------------------
# 📂 LOAD DATA
# -------------------------------
df = pd.read_csv("data/raw/climate_data.csv")
df['date'] = pd.to_datetime(df['date'])

# -------------------------------
# 🎛 SIDEBAR
# -------------------------------
st.sidebar.header("🔍 Filters")

start_date = st.sidebar.date_input("Start Date", df['date'].min())
end_date = st.sidebar.date_input("End Date", df['date'].max())

filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) &
                 (df['date'] <= pd.to_datetime(end_date))]

# -------------------------------
# 📊 METRICS
# -------------------------------
avg_temp = filtered_df['temperature'].mean()
max_temp = filtered_df['temperature'].max()
min_temp = filtered_df['temperature'].min()

mean = filtered_df['temperature'].mean()
std = filtered_df['temperature'].std()

filtered_df['anomaly'] = abs(filtered_df['temperature'] - mean) > 2 * std
anomaly_count = int(filtered_df['anomaly'].sum())

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='metric-box'>🌡 Avg Temp<br><b>{avg_temp:.2f}</b></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-box'>🔥 Max Temp<br><b>{max_temp:.2f}</b></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-box'>❄ Min Temp<br><b>{min_temp:.2f}</b></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='metric-box'>⚠️ Anomalies<br><b>{anomaly_count}</b></div>", unsafe_allow_html=True)

# -------------------------------
# 📈 TEMPERATURE TREND
# -------------------------------
st.subheader("📈 Temperature Trend")

fig1 = px.line(filtered_df, x='date', y='temperature',
               title="Temperature Over Time",
               template="plotly_dark")

st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# 🌧 RAINFALL
# -------------------------------
st.subheader("🌧 Rainfall Trend")

fig2 = px.line(filtered_df, x='date', y='rainfall',
               title="Rainfall Over Time",
               template="plotly_dark")

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# ⚠️ ANOMALIES
# -------------------------------
st.subheader("⚠️ Anomaly Detection")

fig3 = px.scatter(filtered_df, x='date', y='temperature',
                  color=filtered_df['anomaly'],
                  title="Temperature Anomalies",
                  template="plotly_dark")

st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# 📈 FORECAST
# -------------------------------
st.subheader("📈 Future Forecast (Next 30 Days)")

df_sorted = filtered_df.sort_values('date')
forecast = forecast_temperature(df_sorted)

st.line_chart(forecast)

# -------------------------------
# 🤖 AI INSIGHTS (AUTO ANALYSIS)
# -------------------------------
st.subheader("🤖 AI Climate Insights")

trend = "increasing 📈" if df['temperature'].iloc[-1] > df['temperature'].iloc[0] else "decreasing 📉"

insight_text = f"""
- Average Temperature: {avg_temp:.2f}°C  
- Maximum Temperature: {max_temp:.2f}°C  
- Minimum Temperature: {min_temp:.2f}°C  
- Overall Trend: {trend}  
- Total Anomalies Detected: {anomaly_count}  

📌 Interpretation:
Temperature shows a {trend} pattern over time. 
Anomalies indicate unusual climate behavior which may signal extreme weather events.
"""

st.success(insight_text)

# -------------------------------
# 📥 DOWNLOAD REPORT
# -------------------------------
st.subheader("📥 Download Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="climate_report.csv",
    mime="text/csv"
)

# -------------------------------
# 📋 TABLE
# -------------------------------
st.subheader("📋 Data Preview")
st.dataframe(filtered_df.tail(50))