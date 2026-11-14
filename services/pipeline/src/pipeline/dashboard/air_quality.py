import streamlit as st
import pandas as pd
 
def air_quality_tab():    
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