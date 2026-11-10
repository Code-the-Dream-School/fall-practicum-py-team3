import streamlit as st
from load_insight_dashboard import insight_to_dashboard as insight

def daily_summary():
    daily_df, city, date_df, category = insight()
    
    st.selectbox("Current city:",city,index=None)
    
    #Use CSS to fix this!
    with st.container(border=True, horizontal=True):
         st.markdown("Day")
         st.space("small")
         st.markdown("Date")
         st.space("medium")
         st.markdown("AQI")
         st.markdown("Category")
         
    days = ['Mon', 'Tue', 'Wed', 'Th', 'Fri', 'Sat', 'Sun']

    # Switch to python-lucide!
    for day, date, daily, cat in zip(days, date_df, daily_df, category):
        with st.container(border=True, horizontal=True):
            st.markdown(day)
            st.space("small")
            
            st.markdown(str(date))
            st.space("small")
            st.markdown(str(daily))
            st.markdown(str(cat))