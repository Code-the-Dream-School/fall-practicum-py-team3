import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

response = (
    supabase.table("daily_insight").select("*").execute()
)
# Steps: 
# 1. create a dataframe of the insight table (review others code, 
# my code from Python 200, or search) 

def insight_to_dashboard():
    data = response.data
    df = pd.DataFrame(data)
   
    daily_df = df["aqi_24h_avg"]
    city_df = df["city"]
    
    return daily_df, city_df

if __name__ == "__main__":
    insight_to_dashboard()