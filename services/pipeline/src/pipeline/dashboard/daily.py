import streamlit as st
import pandas as pd
from load_insight_dashboard import insight_to_dashboard as insight

def align_content(day, date, aqi, category):
    day_col, date_col, aqi_col, cat_col = st.columns([1,2,0.5,2])

    with day_col:
        st.markdown(str(day))

    with date_col: 
        st.markdown(str(date))
        
    with aqi_col:
        st.markdown(str(aqi))
        
    with cat_col:
        st.markdown(str(category))
         
    
def daily_summary():
    daily_df, city, date_df, category, days = insight()
    chosen_city = st.selectbox("",sorted(city.unique()),index=None, placeholder="Choose a city:")

    all_days = days
    
    with st.container(border=True):
        align_content("Daily","Date","AQI","Category")

    if chosen_city:
       selected_city = city == chosen_city
       new_daily = daily_df[selected_city] # selected_city is the mask
       new_date = date_df[selected_city]
       new_cat = category[selected_city]
          
       for day, date, daily, cat in zip(all_days, new_date, new_daily, new_cat):
            with st.container(border=True):
                align_content(day,date,daily,cat)