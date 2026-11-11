import streamlit as st
import pandas as pd     # Used to work with tabular data
from pathlib import Path

from pipeline.config import PROJECT_ROOT
from daily import daily_summary as daily
from charts import measure_pollutants as mp, raw_gold_comparison as comp

# Either do pandas df here or create one function that can be used for multiple files!

def show_city():
    # extract city name using df["city"]
    st.markdown("City name", text_alignment="center")

def show_daily():
    daily()
       
def show_air_quality():
    with st.container(border=True):
        details = pd.read_csv(PROJECT_ROOT / "config" / "pollutants.csv").set_index("name", drop=False)
        select = st.selectbox("View pollutants", details["name"], index=None)
        
        if select in details.index:
            st.markdown("<u>Fact:</u>",unsafe_allow_html=True)
            st.write(details.loc[select,"what_it_does"])
            st.markdown("<u>Impact:</u>",unsafe_allow_html=True)
            st.write(details.loc[select,"air_pollution_impact"])
        else:
            st.info("Details haven’t been added for this option yet.")

def show_chart():
    mp()
    comp()
    
def center_nav():
    container = st.container(border=True)
        
    with container:
        left, center, right = st.columns([1,2,1])
        
        # options menu
        with center:
            options = ["City", "Daily", "Air Quality", "Charts"]
            selection = st.segmented_control(
                "Weather", options, label_visibility="collapsed"
            )
            if not selection:
                        st.markdown("Please select an option.", text_alignment="center")
                        
        # Account button
        with right:
            account = st.button("Log in")  
            if account: 
                st.write(account)
                
    # Dictionary
    air_nav = {
        "City": show_city,
        "Daily": show_daily,
        "Air Quality": show_air_quality,
        "Charts": show_chart
    }
    
    if selection:
        air_nav[selection]()