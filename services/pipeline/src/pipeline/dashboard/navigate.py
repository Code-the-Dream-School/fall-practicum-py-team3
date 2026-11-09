import streamlit as st
# import pandas as pd     # Used to work with tabular data
from forecast import daily_forecast as daily
from charts import measure_pollutants as mp, raw_gold_comparison as comp

# Either do pandas df here or create one function that can be used for multiple files!

def show_city():
    # extract city name using df["city"]
    st.markdown("City name", text_alignment="center")

def show_daily():
    daily()

# __________________________________________________________
# This can be anything I want - something about the pollutants like the drop down menu
# Move to a new file eventually  
          
def show_air_quality():
    st.markdown("Air quality", text_alignment="center")
    with st.container(border=True):
        poll_list = ['CO', 'NO', 'NO2', 'O3', 'SO2', 'NH3', 'PM2.5', 'PM10']
        st.selectbox("View pollutants", options=poll_list)

        # can add facts for each pollutants

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