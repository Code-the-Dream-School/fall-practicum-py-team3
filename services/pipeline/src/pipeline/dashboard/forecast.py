import streamlit as st

def daily_forecast():
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