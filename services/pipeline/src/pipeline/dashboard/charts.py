import streamlit as st
import pandas as pd     
import numpy as np      
import plotly.express as px  

from load_insight_dashboard import insight_to_dashboard as insight
from raw_n_gold import raw_gold as comparison

comp = comparison()

def raw_gold_comparison():
    st.subheader("Raw vs Gold")
    st.markdown("Average pollutant levels by source")
    bar_chart_raw = px.bar(
        comp,
        x="Pollutants",
        y=["Raw", "Gold"],
        barmode="group"
    )
    st.plotly_chart(bar_chart_raw)
    
# def measure_pollutants():
#     st.subheader("Pollutants Measurements")
#     st.markdown("Colored by Raw")
#     pie_chart_raw = px.pie(df,names="Pollutants",values="Raw")
#     st.plotly_chart(pie_chart_raw)