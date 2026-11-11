import streamlit as st
import pandas as pd     # Used to work with tabular data
from daily import daily_summary as daily
from charts import raw_gold_comparison as comp

# Either do pandas df here or create one function that can be used for multiple files!

def show_daily():
    daily()
       
def show_air_quality():
    with st.container(border=True):
        details = pd.read_csv("pollutants.csv").set_index("name",drop=False)
        select = st.selectbox("View pollutants", details["name"], index=None)
        
        if select in details.index:
            st.markdown("<u>Fact:</u>",unsafe_allow_html=True)
            st.write(details.loc[select,"what_it_does"])
            st.markdown("<u>Impact:</u>",unsafe_allow_html=True)
            st.write(details.loc[select,"air_pollution_impact"])
        else:
            st.info("Details haven’t been added for this option yet.")

def show_chart():   
    comp()
    # mp()
    
def center_nav():
    container = st.container(border=True)
        
    with container:
        left, center, right = st.columns([1,2,1])
        
        # options menu
        with center:
            options = ["Daily", "Air Quality", "Charts"]
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
        "Daily": show_daily,
        "Air Quality": show_air_quality,
        "Charts": show_chart
    }
    
    if selection:
        air_nav[selection]()