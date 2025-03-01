import streamlit as st
import pandas as pd
import numpy as np
import random

# --- Data Generation (Replace with your actual data loading) ---

def generate_dummy_agriculture_data(years, months):
    data = []
    for year in years:
        for month in months:
            data.append({
                'Year': year,
                'Month': month,
                'Crop_Yield': random.uniform(100, 500),
                'Fertilizer_Usage': random.uniform(50, 200),
                'Pesticide_Usage': random.uniform(10, 50)
            })
    return pd.DataFrame(data)

def generate_dummy_weather_data(years, months):
    data = []
    for year in years:
        for month in months:
            data.append({
                'Year': year,
                'Month': month,
                'Temperature': random.uniform(20, 35),
                'Rainfall': random.uniform(0, 300),
            })
    return pd.DataFrame(data)

years = list(range(2014, 2024))
months = list(range(1, 13))

agriculture_data = generate_dummy_agriculture_data(years, months)
weather_data = generate_dummy_weather_data(years, months)

# --- Streamlit Frontend ---

st.title("Santa Cruz Agriculture and Weather Data (2014-2023)")

# --- Data Selection ---

st.sidebar.header("Data Selection")
selected_year = st.sidebar.selectbox("Select Year", years)
selected_month = st.sidebar.selectbox("Select Month", months)

# --- Filtering Data ---

filtered_agriculture = agriculture_data[
    (agriculture_data['Year'] == selected_year) & (agriculture_data['Month'] == selected_month)
]

filtered_weather = weather_data[
    (weather_data['Year'] == selected_year) & (weather_data['Month'] == selected_month)
]

# --- Displaying Data ---

st.header("Agriculture Data")
if not filtered_agriculture.empty:
    st.dataframe(filtered_agriculture)
else:
    st.write("No agriculture data available for the selected year and month.")

st.header("Weather Data")
if not filtered_weather.empty:
    st.dataframe(filtered_weather)
else:
    st.write("No weather data available for the selected year and month.")

# --- Time Series Plots ---

st.header("Time Series Plots")

# Agriculture Time Series
st.subheader("Agriculture Trends")

if not agriculture_data.empty:
    try:
        grouped_agriculture = agriculture_data.groupby(['Year', 'Month'])['Crop_Yield'].mean().reset_index() #reset index added
        grouped_agriculture['Date'] = pd.to_datetime(grouped_agriculture['Year'].astype(str) + '-' + grouped_agriculture['Month'].astype(str), format='%Y-%m') #creates date column
        st.line_chart(grouped_agriculture.set_index('Date')['Crop_Yield'])

        grouped_fert = agriculture_data.groupby(['Year', 'Month'])['Fertilizer_Usage'].mean().reset_index()
        grouped_fert['Date'] = pd.to_datetime(grouped_fert['Year'].astype(str) + '-' + grouped_fert['Month'].astype(str), format='%Y-%m')
        st.line_chart(grouped_fert.set_index('Date')['Fertilizer_Usage'])

        grouped_pest = agriculture_data.groupby(['Year', 'Month'])['Pesticide_Usage'].mean().reset_index()
        grouped_pest['Date'] = pd.to_datetime(grouped_pest['Year'].astype(str) + '-' + grouped_pest['Month'].astype(str), format='%Y-%m')
        st.line_chart(grouped_pest.set_index('Date')['Pesticide_Usage'])

    except KeyError as e:
        st.error(f"Error plotting agriculture data: {e}")
else:
    st.write("No agriculture data to plot.")

# Weather Time Series
st.subheader("Weather Trends")

if not weather_data.empty:
    try:
        grouped_weather_temp = weather_data.groupby(['Year', 'Month'])['Temperature'].mean().reset_index()
        grouped_weather_temp['Date'] = pd.to_datetime(grouped_weather_temp['Year'].astype(str) + '-' + grouped_weather_temp['Month'].astype(str), format='%Y-%m')
        st.line_chart(grouped_weather_temp.set_index('Date')['Temperature'])

        grouped_weather_rain = weather_data.groupby(['Year', 'Month'])['Rainfall'].mean().reset_index()
        grouped_weather_rain['Date'] = pd.to_datetime(grouped_weather_rain['Year'].astype(str) + '-' + grouped_weather_rain['Month'].astype(str), format='%Y-%m')
        st.line_chart(grouped_weather_rain.set_index('Date')['Rainfall'])

    except KeyError as e:
        st.error(f"Error plotting weather data: {e}")
else:
    st.write("No weather data to plot.")

# --- Overall Data Display ---
st.header("Overall Data")
st.subheader("Agriculture Data (Last 10 Years)")
st.dataframe(agriculture_data)

st.subheader("Weather Data (Last 10 Years)")
st.dataframe(weather_data)

# --- Instructions for Running ---

st.markdown("""
**Instructions:**

1.  **Save:** Save this code as a Python file (e.g., `santacruz_data_app.py`).
2.  **Install Libraries:** If you don't have them, install the necessary libraries:
    ```bash
    pip install streamlit pandas numpy
    ```
3.  **Run:** Open your terminal, navigate to the directory where you saved the file, and run:
    ```bash
    streamlit run santacruz_data_app.py
    ```
4.  **Replace Dummy Data:** **Crucially**, replace the `generate_dummy_agriculture_data` and `generate_dummy_weather_data` functions with your actual data loading logic. You'll likely read data from CSV files, databases, or APIs.
5.  **Adjust Parameters:** Modify the parameter names (`Crop_Yield`, `Temperature`, etc.) and data ranges to match your real data.
""")