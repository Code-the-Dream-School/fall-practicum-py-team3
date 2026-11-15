import streamlit as st
import pandas as pd     
from daily import daily_summary as daily
from charts import  raw_gold_comparison as comp, measure_pollutants as mp
from air_quality import air_quality_tab as air

def show_daily():
    daily()
       
def show_air_quality():
   air()

def show_chart():   
    comp()
    mp()
    
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
                st.markdown("<h5 style='text-align: left;'>Please select an option.</h5>", unsafe_allow_html=True)
                        
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