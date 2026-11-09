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

def show_city():
    # extract city name using df["city"]
    st.markdown("City name", text_alignment="center")

# Daily will use aqi_24h_avg in the final version --> df["aqi_24h_avg"]
# Move to a new file (forecast.py)
def show_daily():
    days = ['Mon', 'Tue', 'Wed', 'Th', 'Fri', 'Sat', 'Sun']

    # Switch to python-lucide!
    for day in days:
        with st.container(border=True, horizontal=True):
            st.markdown(day)
            st.markdown("Icon")
            st.markdown("%")
            st.markdown("Condition")
            st.markdown("Temp 1")
            st.container(border=True)
            st.markdown("Temp 2")

# __________________________________________________________
# This can be anything I want - something about the pollutants like the drop down menu
# Move to a new file eventually  
          
def show_air_quality():
    st.markdown("Air quality", text_alignment="center")
    
# __________________________________________________________
# Move to charts.py -- function for each chart type? Examples: def show_raw_chart(df):
    # Raw pollutant measurements

# def show_comparison_chart(df):
    # Raw vs Gold comparison

# def show_trend_chart(df):
    # Pollutant trends over time
    
def show_chart():
    st.title("Pollutant Comparisons Charts")

    st.subheader("Pollutants vs Raw")
    st.markdown("Colored by Gold")
    bar_chart_raw = px.bar(df,x="Pollutants", y="Raw", barmode='group', color="Gold")
    st.plotly_chart(bar_chart_raw)

    st.subheader("Raw vs Gold")
    st.markdown("Colored by pollutants")
    bar_chart_raw = px.bar(df,x="Raw", y="Gold", barmode='group', color="Pollutants")
    st.plotly_chart(bar_chart_raw)
    
def show_chart():
    st.title("Pollutant Comparisons Charts")

    st.subheader("Pollutants vs Raw")
    st.markdown("Colored by Gold")
    bar_chart_raw = px.bar(df,x="Pollutants", y="Raw", barmode='group', color="Gold")
    st.plotly_chart(bar_chart_raw)

    st.subheader("Raw vs Gold")
    st.markdown("Colored by pollutants")
    bar_chart_raw = px.bar(df,x="Raw", y="Gold", barmode='group', color="Pollutants")
    st.plotly_chart(bar_chart_raw)
    
def center_nav():
    container = st.container(border=True)
        
    with container:
        left, center, right = st.columns([1,2,1])
        
        # options menu
        with center:
            options = ["City", "Daily", "Air Quality", "Chart"]
            selection = st.segmented_control(
                "Weather", options, label_visibility="collapsed"
            )
            if not selection:
                        st.markdown("Please select an option.", text_alignment="center")
                        
              # Account button
        with right:
            # st.space("small")
            account = st.button("Log in")  
            if account: 
                st.write(account)
                
        with left:
            left_container = st.container(border=True)
            with left_container:
                poll_list = ['CO', 'NO', 'NO2', 'O3', 'SO2', 'NH3', 'PM2.5', 'PM10']
                st.selectbox("View pollutants", options=poll_list)

                # can add facts for each pollutants
                
    # Dictionary
    air_nav = {
        "City": show_city,
        "Daily": show_daily,
        "Air Quality": show_air_quality,
        "Chart": show_chart
    }
    
    if selection:
        air_nav[selection]()