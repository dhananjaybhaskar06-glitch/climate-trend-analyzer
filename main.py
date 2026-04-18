print("🚀 Script started")

import pandas as pd
import os

from src.anomaly import detect_anomalies
from src.visualization import plot_anomalies

os.makedirs("outputs/plots", exist_ok=True)

print("📂 Loading data...")
df = pd.read_csv("data/raw/climate_data.csv")

print("📅 Processing date...")
df['date'] = pd.to_datetime(df['date'])

print("📊 Detecting anomalies...")
df = detect_anomalies(df)

print("📈 Plotting anomalies...")
plot_anomalies(df)

print("✅ DONE: Anomaly graph saved")