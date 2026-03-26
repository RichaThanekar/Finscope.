# This is a copy of app.py for the multipage app structure
import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go
import os

# -------------------------------
# 1️⃣ App title
# -------------------------------
st.set_page_config(page_title="Inflation Forecast Dashboard", layout="wide")
st.title("📊 Inflation Forecast Dashboard")

# -------------------------------
# 2️⃣ Load Data
# -------------------------------
# Fix path - go up one directory from pages/ to find data/
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "df_all.xlsx")

try:
    df_all = pd.read_excel(data_path, parse_dates=['Month'])
    st.success(f"✅ Data loaded successfully: {len(df_all)} rows")
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.info(f"Looking for file at: {data_path}")
    st.stop()

# -------------------------------
# 3️⃣ Prepare data for Prophet
# -------------------------------
# Check if required column exists
if 'Combined Inflation (%)' not in df_all.columns:
    st.error(f"❌ Column 'Combined Inflation (%)' not found. Available columns: {df_all.columns.tolist()}")
    st.stop()

df_prophet = df_all[['Month', 'Combined Inflation (%)']].copy()
df_prophet['y'] = pd.to_numeric(df_prophet['Combined Inflation (%)'], errors='coerce')

# Check for NaN values
nan_count = df_prophet['y'].isna().sum()
if nan_count > 0:
    st.warning(f"⚠️ Found {nan_count} NaN values, filling forward...")
    
df_prophet['y'] = df_prophet['y'].ffill()
df_prophet = df_prophet.rename(columns={'Month': 'ds'})

# Remove any remaining NaN
df_prophet = df_prophet.dropna()

st.info(f"📊 Prepared {len(df_prophet)} data points for forecasting")

# Show data range for debugging
st.write(f"**Data range:** {df_prophet['y'].min():.2f}% to {df_prophet['y'].max():.2f}%")
st.write(f"**Date range:** {df_prophet['ds'].min().strftime('%Y-%m')} to {df_prophet['ds'].max().strftime('%Y-%m')}")

# -------------------------------
# 4️⃣ Initialize Prophet
# -------------------------------
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False,
    changepoint_prior_scale=0.5,  # More flexible to detect changes
    seasonality_mode='additive',   # Better for inflation
    seasonality_prior_scale=10.0    # Stronger seasonality
)
model.fit(df_prophet[['ds', 'y']])

# -------------------------------
# 5️⃣ Forecast next 12 months
# -------------------------------
future = model.make_future_dataframe(periods=12, freq='MS')
forecast = model.predict(future)

# Get fitted values for historical data
historical_len = len(df_prophet)
df_prophet['Fitted'] = forecast.loc[:historical_len-1, 'yhat'].values

# Split forecast into historical and future
forecast_future = forecast.iloc[historical_len:]

st.info(f"📈 Historical data: {historical_len} points | Future forecast: {len(forecast_future)} months")

# -------------------------------
# 6️⃣ Interactive Plotly Chart
# -------------------------------
fig = go.Figure()

# Actual
fig.add_trace(go.Scatter(
    x=df_prophet['ds'], y=df_prophet['y'],
    mode='127.0.0.1 refused to connect.127.0.0.1 refused to connect.s+markers', name='Actual',
    line=dict(color='#1f77b4', width=2),
    marker=dict(size=6)
))

# Fitted
fig.add_trace(go.Scatter(
    x=df_prophet['ds'], y=df_prophet['Fitted'],
    mode='lines', name='Fitted (Prophet)',
    line=dict(color='#2ca02c', dash='dash', width=2)
))

# Forecast (only future values)
fig.add_trace(go.Scatter(
    x=forecast_future['ds'], y=forecast_future['yhat'],
    mode='lines+markers', name='Forecast (Next 12 Months)',
    line=dict(color='#d62728', width=3),
    marker=dict(size=7)
))

# Confidence interval (only for future)
fig.add_trace(go.Scatter(
    x=list(forecast_future['ds']) + list(forecast_future['ds'][::-1]),
    y=list(forecast_future['yhat_lower']) + list(forecast_future['yhat_upper'][::-1]),
    fill='toself', fillcolor='rgba(214,39,40,0.15)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo="skip", showlegend=True, name='Forecast CI'
))

# Layout styling
fig.update_layout(
    title=dict(text='📈 Combined Inflation: Actual, Fitted & Forecast', x=0.5, xanchor='center'),
    xaxis_title='Month',
    yaxis_title='Combined Inflation (%)',
    hovermode='x unified',
    template="plotly_white",
    height=600,
    margin=dict(l=40, r=40, t=60, b=40),
    legend=dict(
        orientation="h", yanchor="bottom", y=-0.2,
        xanchor="center", x=0.5, font=dict(size=12)
    )
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 7️⃣ Forecasted values next 12 months
# -------------------------------
st.subheader("📅 Forecasted Combined Inflation for Next 12 Months")
forecast_12m = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(12)
forecast_12m = forecast_12m.rename(columns={
    'ds': 'Month',
    'yhat': 'Predicted',
    'yhat_lower': 'Lower CI',
    'yhat_upper': 'Upper CI'
})

st.dataframe(
    forecast_12m.style.format({
        'Predicted': "{:.2f}%",
        'Lower CI': "{:.2f}%",
        'Upper CI': "{:.2f}%"
    })
)