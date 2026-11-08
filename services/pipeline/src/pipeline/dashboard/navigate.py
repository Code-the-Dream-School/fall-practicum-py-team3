import streamlit as st
import pandas as pd     # Used to work with tabular data
import numpy as np      # Helps generate random numbers
import plotly.express as px  # For interactive charts

# sample data for demo
np.random.seed(42) # setting a seed so results are consistent for each run

sample_data = {
    'Pollutants': ['CO', 'NO', 'NO2', 'O3', 'SO2', 'NH3', 'PM2.5', 'PM10'],
    'Raw': np.random.randint(100,500, size=8),
    'Gold': np.random.randint(100,500, size=8)
}

df = pd.DataFrame(sample_data)