import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import seasonal_decompose
from prophet import Prophet


def get_hardcoded_data():
    dates = pd.date_range(start='2020-01-01', periods=60, freq='MS')

    base_temp_arabian = 26 + np.sin(np.arange(60) * (2 * np.pi / 12)) * 2
    base_temp_bengal = 27 + np.sin(
        np.arange(60) * (2 * np.pi / 12) + np.pi / 6
    ) * 1.5

    trend = np.linspace(0, 0.5, 60)
    temp_arabian = (
        base_temp_arabian + trend + np.random.randn(60) * 0.2
    )
    temp_bengal = (
        base_temp_bengal + trend + np.random.randn(60) * 0.2
    )

    df_arabian = pd.DataFrame({
        'date': dates, 'region': 'Arabian Sea',
        'parameter': 'Sea Surface Temperature', 'value': temp_arabian
    })
    df_bengal = pd.DataFrame({
        'date': dates, 'region': 'Bay of Bengal',
        'parameter': 'Sea Surface Temperature', 'value': temp_bengal
    })

    return pd.concat([df_arabian, df_bengal], ignore_index=True)


def plot_decomposition(decomposition_result, parameter):
    fig = make_subplots(
        rows=4, cols=1,
        subplot_titles=("Observed", "Trend", "Seasonal", "Residual")
    )

    fig.add_trace(go.Scatter(
        x=decomposition_result.observed.index,
        y=decomposition_result.observed, mode='lines', name='Observed'
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=decomposition_result.trend.index,
        y=decomposition_result.trend, mode='lines', name='Trend'
    ), row=2, col=1)
    fig.add_trace(go.Scatter(
        x=decomposition_result.seasonal.index,
        y=decomposition_result.seasonal, mode='lines', name='Seasonal'
    ), row=3, col=1)
    fig.add_trace(go.Scatter(
        x=decomposition_result.resid.index,
        y=decomposition_result.resid, mode='markers', name='Residual'
    ), row=4, col=1)

    fig.update_layout(
        height=700, title_text=f"Time-Series Decomposition of {parameter}",
        showlegend=False
    )
    return fig


def plot_forecast(forecast_df, actual_df, parameter):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=actual_df['ds'], y=actual_df['y'], mode='markers', name='Actual Values'
    ))
    fig.add_trace(go.Scatter(
        x=forecast_df['ds'], y=forecast_df['yhat'], mode='lines',
        name='Forecast', line=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=forecast_df['ds'], y=forecast_df['yhat_upper'], fill=None,
        mode='lines', line=dict(color='lightblue'), showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=forecast_df['ds'], y=forecast_df['yhat_lower'], fill='tonexty',
        mode='lines', line=dict(color='lightblue'), showlegend=False
    ))

    fig.update_layout(
        title=f"12-Month Forecast for {parameter}",
        xaxis_title='Date', yaxis_title='Value'
    )
    return fig


def run_time_series_analysis(data, region, parameter):
    filtered_data = data[
        (data['region'] == region) & (data['parameter'] == parameter)
    ].copy()
    filtered_data.set_index('date', inplace=True)

    decomposition = seasonal_decompose(filtered_data['value'], model='additive')
    decomposition_fig = plot_decomposition(decomposition, parameter)

    prophet_df = filtered_data.reset_index().rename(
        columns={'date': 'ds', 'value': 'y'}
    )
    model = Prophet()
    model.fit(prophet_df)
    future = model.make_future_dataframe(periods=12, freq='MS')
    forecast = model.predict(future)
    forecast_fig = plot_forecast(forecast, prophet_df, parameter)

    return decomposition_fig, forecast_fig