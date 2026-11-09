import streamlit as st

# Daily will use aqi_24h_avg in the final version --> df["aqi_24h_avg"]
# Load in df from load_data()
def daily_summary():
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