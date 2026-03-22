import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go

# Load data
df_all = pd.read_excel("data/df_all.xlsx", parse_dates=['Month'])
print(f"Loaded {len(df_all)} rows")
print(f"Columns: {df_all.columns.tolist()}")
print(f"\nFirst 10 rows:")
print(df_all.head(10))
print(f"\nLast 10 rows:")
print(df_all.tail(10))

# Prepare for Prophet
df_prophet = df_all[['Month', 'Combined Inflation (%)']].copy()
df_prophet['y'] = pd.to_numeric(df_prophet['Combined Inflation (%)'], errors='coerce')
df_prophet['y'] = df_prophet['y'].ffill()
df_prophet = df_prophet.rename(columns={'Month': 'ds'})
df_prophet = df_prophet.dropna()

print(f"\n\nProphet data prepared: {len(df_prophet)} points")
print(df_prophet.head(10))
print(f"\nY values stats:")
print(f"Min: {df_prophet['y'].min()}")
print(f"Max: {df_prophet['y'].max()}")
print(f"Mean: {df_prophet['y'].mean()}")
print(f"Std: {df_prophet['y'].std()}")

# Check if data is constant or linear
y_values = df_prophet['y'].values
if len(set(y_values)) == 1:
    print("\n⚠️ WARNING: All Y values are the same!")
elif y_values[-1] - y_values[0] == 0:
    print("\n⚠️ WARNING: No variation in data!")
else:
    print(f"\n✓ Data has variation: range = {y_values.max() - y_values.min()}")

# Train Prophet
print("\n\nTraining Prophet model...")
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False,
    changepoint_prior_scale=1.0,
    seasonality_mode='multiplicative'
)
model.add_seasonality(name='monthly', period=12, fourier_order=8)
model.fit(df_prophet[['ds', 'y']])

print("✓ Model trained successfully")

# Make prediction
future = model.make_future_dataframe(periods=12, freq='MS')
forecast = model.predict(future)

print(f"\nForecast shape: {forecast.shape}")
print(f"Forecast columns: {forecast.columns.tolist()}")

# Check fitted values
historical_len = len(df_prophet)
fitted_values = forecast.iloc[:historical_len]['yhat'].values

print(f"\nFitted values stats:")
print(f"Min: {fitted_values.min()}")
print(f"Max: {fitted_values.max()}")
print(f"Mean: {fitted_values.mean()}")

# Check if fitted values are linear
if len(set(fitted_values.round(2))) < 10:
    print("\n⚠️ WARNING: Fitted values appear to be nearly constant!")
else:
    print(f"\n✓ Fitted values have {len(set(fitted_values.round(2)))} unique values")

# Compare actual vs fitted
print("\n\nFirst 10 actual vs fitted:")
comparison = pd.DataFrame({
    'Date': df_prophet['ds'].iloc[:10],
    'Actual': df_prophet['y'].iloc[:10],
    'Fitted': fitted_values[:10]
})
print(comparison)

print("\n\nLast 10 actual vs fitted:")
comparison = pd.DataFrame({
    'Date': df_prophet['ds'].iloc[-10:].values,
    'Actual': df_prophet['y'].iloc[-10:].values,
    'Fitted': fitted_values[-10:]
})
print(comparison)

# Future forecast
forecast_future = forecast.iloc[historical_len:]
print(f"\n\nFuture forecast (12 months):")
print(forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head(12))
