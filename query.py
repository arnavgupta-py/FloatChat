import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from prophet import Prophet


HARDCODED_QUESTIONS = [
    "List the 5 most recent profiles reported by float with WMO ID 2901683...",
    "What was the average sea surface temperature across the entire Indian Ocean for the year 2023?",
    "Plot the full temperature and salinity profile vs. pressure for the latest cycle of float 1901345.",
    "Show the complete historical trajectory of float 2901683 on a 2D map.",
    "Generate a 3D scatter plot of Temperature, Salinity, and Pressure...",
    "Visualize the complete historical path of float 2901683 on an interactive 3D globe.",
    "Analyze the seasonal trend of sea surface temperature in the Bay of Bengal...",
    "Compare the average temperature at 100m depth between the Arabian Sea and the Bay of Bengal..."
]


def create_profile_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["temperature"], y=df["pressure"], name="Temperature (°C)",
        line=dict(color='#00f2fe')
    ))
    fig.add_trace(go.Scatter(
        x=df["salinity"], y=df["pressure"], name="Salinity (PSU)",
        xaxis="x2", line=dict(color='#ff69b4')
    ))
    fig.update_layout(
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_text="Temperature & Salinity Profile",
        xaxis=dict(
            title=dict(text="Temperature (°C)", font=dict(color="#00f2fe")),
            tickfont=dict(color="#00f2fe")
        ),
        xaxis2=dict(
            title=dict(text="Salinity (PSU)", font=dict(color="#ff69b4")),
            tickfont=dict(color="#ff69b4"),
            anchor="y", overlaying="x", side="top"
        ),
        yaxis=dict(title="Pressure (dbar)", autorange="reversed"),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
        )
    )
    return fig


def create_3d_scatter(df):
    fig = px.scatter_3d(
        df, x='temperature', y='salinity', z='pressure', color='temperature',
        color_continuous_scale='Cividis_r',
        title='3D Oceanographic Profile (T-S Diagram vs. Depth)'
    )
    fig.update_layout(
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        scene=dict(zaxis=dict(autorange='reversed'))
    )
    return fig


def create_2d_map(df):
    fig = go.Figure(go.Scattermapbox(
        lat=df['lat'], lon=df['lon'], mode='markers',
        marker=dict(size=8, color='#00f2fe', opacity=0.7),
        hoverinfo='none'
    ))
    fig.update_layout(
        title_text='Float Trajectory on 2D Map',
        mapbox=dict(style="carto-darkmatter", center=dict(lat=0, lon=0), zoom=1.5),
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', height=500
    )
    return fig


def create_3d_globe_plotly(df):
    fig = go.Figure(go.Scattergeo(
        lat=df['lat'], lon=df['lon'], mode='markers+lines',
        marker=dict(size=4, color='#00f2fe', opacity=0.8),
        line=dict(width=1, color='#00f2fe'),
        hoverinfo='none'
    ))
    fig.update_layout(
        title_text='Float Trajectory on 3D Globe',
        geo=dict(
            projection_type='orthographic',
            showland=True, landcolor='rgba(11, 26, 58, 0.9)',
            showocean=True, oceancolor='rgba(2, 4, 10, 0.9)',
            showcountries=True, countrycolor='rgba(66, 151, 160, 0.4)',
            bgcolor='rgba(0,0,0,0)'
        ),
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        margin={"r": 0, "t": 40, "l": 0, "b": 0}, height=500
    )
    return fig


def create_timeseries_forecast_chart(df):
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=12, freq='MS')
    forecast = m.predict(future)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['ds'], y=df['y'], mode='markers', name='Actual'
    ))
    fig.add_trace(go.Scatter(
        x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'
    ))
    fig.add_trace(go.Scatter(
        x=forecast['ds'], y=forecast['yhat_upper'], fill=None, mode='lines',
        line_color='rgba(0,0,0,0)', showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=forecast['ds'], y=forecast['yhat_lower'], fill='tonexty',
        mode='lines', line_color='rgba(0, 100, 80, 0.2)', showlegend=False
    ))
    fig.update_layout(
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title='Sea Surface Temperature: Trend & Forecast',
        xaxis_title='Date', yaxis_title='Temperature (°C)'
    )
    return fig


HARDCODED_RESPONSES = {
    "List the 5 most recent profiles reported by float with WMO ID 2901683...": {
        "type": "table",
        "dataframe": pd.DataFrame({
            "Profile Date": pd.to_datetime([
                "2024-03-20 12:00:00", "2024-03-10 12:00:00",
                "2024-03-01 12:00:00", "2024-02-20 12:00:00",
                "2024-02-10 12:00:00"
            ]),
            "Latitude": [10.5, 10.3, 10.1, 9.8, 9.5],
            "Longitude": [65.2, 65.5, 65.7, 66.0, 66.3],
            "Cycle Number": [152, 151, 150, 149, 148]
        }),
        "text_summary": "Here are the 5 most recent profiles for float 2901683:"
    },
    "What was the average sea surface temperature across the entire Indian Ocean for the year 2023?": {
        "type": "text",
        "data": "The estimated average sea surface temperature across the Indian Ocean in 2023 was approximately 28.1°C."
    },
    "Plot the full temperature and salinity profile vs. pressure for the latest cycle of float 1901345.": {
        "type": "plot",
        "plot_function": create_profile_chart,
        "dataframe": pd.DataFrame({
            "pressure": [5, 10, 20, 30, 50, 75, 100, 150, 200, 300, 400, 500],
            "temperature": [28.5, 28.4, 28.3, 27.9, 26.5, 24.1, 22.0, 18.5, 15.3, 12.1, 10.4, 9.0],
            "salinity": [34.5, 34.5, 34.6, 34.7, 34.9, 35.0, 35.1, 35.0, 34.8, 34.6, 34.5, 34.4]
        }),
        "text_summary": "Here is the requested temperature and salinity profile for the latest cycle of float 1901345."
    },
    "Generate a 3D scatter plot of Temperature, Salinity, and Pressure...": {
        "type": "plot",
        "plot_function": create_3d_scatter,
        "dataframe": pd.DataFrame({
            "pressure": [10, 20, 30, 50, 75, 100, 150, 200, 300, 400, 500, 15, 25, 35, 55, 80, 110],
            "temperature": [28.1, 28.0, 27.9, 27.2, 26.1, 23.5, 21.0, 17.9, 14.3, 11.1, 9.4, 28.2, 28.1, 27.8, 27.0, 25.5, 22.0],
            "salinity": [34.5, 34.5, 34.6, 34.7, 34.9, 35.0, 35.1, 35.0, 34.8, 34.6, 34.5, 34.4, 34.5, 34.6, 34.8, 35.0, 35.1]
        }),
        "text_summary": "Here is the 3D scatter plot of Temperature, Salinity, and Pressure for measurements from float 1901345 in 2024."
    },
    "Show the complete historical trajectory of float 2901683 on a 2D map.": {
        "type": "plot",
        "plot_function": create_2d_map,
        "dataframe": pd.DataFrame({
            "lat": [9.5, 9.8, 10.1, 10.3, 10.5, 10.8, 11.0, 11.2],
            "lon": [66.3, 66.0, 65.7, 65.5, 65.2, 65.0, 64.8, 64.5],
            "date": ["2024-02-10", "2024-02-20", "2024-03-01", "2024-03-10", "2024-03-20", "2024-03-30", "2024-04-09", "2024-04-19"]
        }),
        "text_summary": "Displaying the historical trajectory for float 2901683 on a 2D map."
    },
    "Visualize the complete historical path of float 2901683 on an interactive 3D globe.": {
        "type": "plot",
        "plot_function": create_3d_globe_plotly,
        "dataframe": pd.DataFrame({
            "lat": [9.5, 9.8, 10.1, 10.3, 10.5, 10.8, 11.0, 11.2, 11.5, 11.8],
            "lon": [66.3, 66.0, 65.7, 65.5, 65.2, 65.0, 64.8, 64.5, 64.2, 64.0]
        }),
        "text_summary": "Visualizing the historical path for float 2901683 on an interactive 3D globe."
    },
    "Analyze the seasonal trend of sea surface temperature in the Bay of Bengal...": {
        "type": "plot",
        "plot_function": create_timeseries_forecast_chart,
        "dataframe": pd.DataFrame({
            'ds': pd.date_range(start='2020-01-01', periods=60, freq='MS'),
            'y': [27.5, 27.8, 28.5, 29.5, 30.0, 29.8, 29.2, 29.0, 29.1, 28.8, 28.0, 27.6] * 5
        }),
        "text_summary": "Here is the time-series analysis and 12-month forecast for sea surface temperature in the Bay of Bengal."
    },
    "Compare the average temperature at 100m depth between the Arabian Sea and the Bay of Bengal...": {
        "type": "table",
        "dataframe": pd.DataFrame({
            "Region": ["Arabian Sea", "Bay of Bengal"],
            "Avg. Temp at 100m (°C)": [24.5, 25.1]
        }),
        "text_summary": "Here is the comparison for the last quarter. The Bay of Bengal was slightly warmer on average at this depth."
    }
}

HARDCODED_XAI = {}

DEFAULT_XAI_DETAILS = """
<details>
    <summary><strong>1. Hypothetical Document (Hy-DE)</strong></summary>
    <p>Generated a detailed hypothetical answer to enrich the search query.</p>
</details>
<details>
    <summary><strong>2. Retrieved Context</strong></summary>
    <ul>
        <li>Retrieved schema details for relevant tables (e.g., profiles, floats).</li>
        <li>Retrieved specific PostGIS function usage examples.</li>
        <li>Retrieved ARGO-specific terminology and unit explanations.</li>
    </ul>
</details>
<details>
    <summary><strong>3. Initial SQL Query (Draft)</strong></summary>
    <pre><code>-- Initial SQL query generated by LLM based on context --</code></pre>
</details>
<details>
    <summary><strong>4. Self-Correction & Critique</strong></summary>
    <p><strong>Critique:</strong> The LLM reviewed its initial query for correctness and efficiency.</p>
</details>
<details>
    <summary><strong>5. Final SQL Query (Executed)</strong></summary>
    <pre><code>-- Final, validated SQL query ready for execution --</code></pre>
</details>
"""