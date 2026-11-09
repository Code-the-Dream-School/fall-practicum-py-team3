import streamlit as st
import pandas as pd     # Used to work with tabular data
import numpy as np      # Helps generate random numbers
import plotly.express as px  # For interactive charts

# import loading file & do df = load_data()
# sample data for demo
np.random.seed(42) # setting a seed so results are consistent for each run

sample_data = {
    'Pollutants': ['CO', 'NO', 'NO2', 'O3', 'SO2', 'NH3', 'PM2.5', 'PM10'],
    'Raw': np.random.randint(100,500, size=8),
    'Gold': np.random.randint(100,500, size=8)
}

df = pd.DataFrame(sample_data)
st.title("Pollutant Comparisons Charts")

def measure_pollutants():
    st.subheader("Pollutants Measurements")
    st.markdown("Colored by Raw")
    pie_chart_raw = px.pie(df,names="Pollutants",values="Raw")
    st.plotly_chart(pie_chart_raw)

def raw_gold_comparison():
    st.subheader("Raw vs Gold")
    st.markdown("Colored by pollutants")
    bar_chart_raw = px.bar(df,x="Raw", y="Gold", barmode='group', color="Pollutants")
    st.plotly_chart(bar_chart_raw)