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
    chosen_city = st.selectbox("City",sorted(city.unique()),index=None, placeholder="Choose a city:", label_visibility="collapsed")

    with st.container(border=True):
        align_content("Daily","Date","AQI","Category")

    if chosen_city:
        selected_city = city == chosen_city

        new_daily = daily_df[selected_city]
        new_date = date_df[selected_city]
        new_cat = category[selected_city]
        new_days = days[selected_city]

        # Pagination - 10 records per page
        records_per_page = 10
        total_pages = (len(new_daily) + records_per_page - 1) // records_per_page

        # Reserve the display area above the pagination
        records_container = st.container()

        # Pagination stays at the bottom
        pages = st.pagination(
            num_pages=total_pages,
            max_visible_pages=10,
            bind="query-params",
            key="selected_page"
        )

        start_idx = (pages - 1) * records_per_page
        end_idx = start_idx + records_per_page

        # Display only the records for the selected page
        with records_container:
            for day, date, daily, cat in zip(
                new_days.iloc[start_idx:end_idx],
                new_date.iloc[start_idx:end_idx],
                new_daily.iloc[start_idx:end_idx],
                new_cat.iloc[start_idx:end_idx]
            ):
                with st.container(border=True):
                    align_content(day, date, daily, cat)