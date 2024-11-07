import streamlit as st
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from io import StringIO

def apply_forecasting(data):
    st.subheader("Select Forecasting Model")
    model_choice = st.selectbox("Choose a forecasting model", [
        "ARIMA", "Prophet", "Moving Average", "Exponential Smoothing", 
        "Linear Regression", "Random Forest", "Support Vector Regression (SVR)", "LSTM Neural Network"
    ])
    
    target_col = st.selectbox("Select target column for forecasting", data.select_dtypes(include=[np.number]).columns)

    if st.button("Run Model"):
        forecast = None  # Initialize forecast variable to hold results
        if model_choice == "ARIMA":
            order = st.text_input("ARIMA order (p,d,q)", "(1,1,1)")
            p, d, q = map(int, order.strip("()").split(","))
            model = ARIMA(data[target_col], order=(p, d, q))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=10)
            plot_forecast(forecast, "ARIMA Forecast", target_col)

        elif model_choice == "Prophet":
            df = data[["date", target_col]].rename(columns={"date": "ds", target_col: "y"})
            model = Prophet()
            model.fit(df)
            future = model.make_future_dataframe(periods=10)
            forecast = model.predict(future)["yhat"]
            plot_forecast(forecast, "Prophet Forecast", target_col)

        elif model_choice == "Moving Average":
            window = st.slider("Window size", 1, 20, 3)
            forecast = data[target_col].rolling(window=window).mean()
            plot_forecast(forecast, "Moving Average Forecast", target_col)

        elif model_choice == "Exponential Smoothing":
            seasonal_periods = st.slider("Seasonal Periods", 1, 12, 12)
            trend = st.selectbox("Trend Component", ["add", "mul", None])
            seasonal = st.selectbox("Seasonal Component", ["add", "mul", None])
            model = ExponentialSmoothing(data[target_col], trend=trend, seasonal=seasonal, seasonal_periods=seasonal_periods)
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=10)
            plot_forecast(forecast, "Holt-Winters Exponential Smoothing Forecast", target_col)

        elif model_choice == "Linear Regression":
            forecast = run_linear_regression(data, target_col)
            plot_forecast(forecast, "Linear Regression Forecast", target_col)

        elif model_choice == "Random Forest":
            forecast = run_random_forest(data, target_col)
            plot_forecast(forecast, "Random Forest Forecast", target_col)

        elif model_choice == "Support Vector Regression (SVR)":
            forecast = run_svr(data, target_col)
            plot_forecast(forecast, "Support Vector Regression Forecast", target_col)

        elif model_choice == "LSTM Neural Network":
            forecast = run_lstm(data, target_col)
            plot_forecast(forecast, "LSTM Neural Network Forecast", target_col)

        # Allow user to download forecast
        if forecast is not None:
            download_forecast(forecast, model_choice)

def plot_forecast(forecast, title, target_col):
    st.write(title)
    fig, ax = plt.subplots()
    ax.plot(forecast, label="Forecast")
    ax.set_xlabel("Time")
    ax.set_ylabel(target_col)
    ax.legend()
    st.pyplot(fig)

def download_forecast(forecast, model_choice):
    csv = forecast.to_csv(index=False)
    st.download_button("Download Forecast", csv, f"{model_choice}_forecast.csv", "text/csv")

# Linear Regression Forecast
def run_linear_regression(data, target_col):
    df = data.dropna(subset=[target_col]).reset_index()
    X = df.index.values.reshape(-1, 1)
    y = df[target_col].values
    model = LinearRegression()
    model.fit(X, y)
    future_X = np.arange(len(X), len(X) + 10).reshape(-1, 1)
    forecast = model.predict(future_X)
    return pd.Series(forecast)

# Random Forest Forecast
def run_random_forest(data, target_col):
    df = data.dropna(subset=[target_col]).reset_index()
    X = df.index.values.reshape(-1, 1)
    y = df[target_col].values
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)
    future_X = np.arange(len(X), len(X) + 10).reshape(-1, 1)
    forecast = model.predict(future_X)
    return pd.Series(forecast)

# Support Vector Regression Forecast
def run_svr(data, target_col):
    df = data.dropna(subset=[target_col]).reset_index()
    X = df.index.values.reshape(-1, 1)
    y = df[target_col].values
    model = SVR(kernel='rbf')
    model.fit(X, y)
    future_X = np.arange(len(X), len(X) + 10).reshape(-1, 1)
    forecast = model.predict(future_X)
    return pd.Series(forecast)

# LSTM Neural Network Forecast
def run_lstm(data, target_col):
    df = data.dropna(subset=[target_col]).reset_index()
    sequence_length = 10
    X, y = [], []
    for i in range(len(df) - sequence_length):
        X.append(df[target_col].values[i:i + sequence_length])
        y.append(df[target_col].values[i + sequence_length])
    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))  # Reshape for LSTM

    # Define LSTM model
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(sequence_length, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=10, verbose=0)

    # Forecasting future values
    last_sequence = df[target_col].values[-sequence_length:]
    forecast = []
    for _ in range(10):  # Forecast next 10 steps
        last_sequence = last_sequence.reshape((1, sequence_length, 1))
        next_value = model.predict(last_sequence, verbose=0)
        forecast.append(next_value[0, 0])
        last_sequence = np.append(last_sequence[0, 1:], next_value[0, 0])
    return pd.Series(forecast)
