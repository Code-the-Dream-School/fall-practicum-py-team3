import streamlit as st
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
    daily_df, city, date_df, category = insight()
    st.selectbox("Current city:",sorted(city.unique()),index=None)

    days = ['Mon', 'Tue', 'Wed', 'Th', 'Fri', 'Sat', 'Sun']
    
    with st.container(border=True):
        align_content("Daily","Date","AQI","Category")

    for day, date, daily, cat in zip(days, date_df, daily_df, category):
       with st.container(border=True):
        align_content(day,date,daily,cat)