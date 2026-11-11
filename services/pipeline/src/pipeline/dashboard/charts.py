import streamlit as st
import pandas as pd     
import numpy as np      
import plotly.express as px  

from load_insight_dashboard import insight_to_dashboard as insight
from raw_n_gold import raw_gold as comparison

daily_df, city, date_df, insight_cat = insight()
comp, gold_category = comparison()

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
    
def measure_pollutants():
    st.subheader("Gold and Insight: Combined Categories")

    categories = pd.concat(
        [gold_category, insight_cat],
        ignore_index=True
    )

    counts = categories.value_counts().reset_index()
    counts.columns = ["Category", "Count"]

    fig = px.pie(counts, names="Category", values="Count")
    st.plotly_chart(fig)