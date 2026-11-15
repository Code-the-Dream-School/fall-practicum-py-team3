import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

response = (
    supabase.table("daily_insight").select("*").execute()
)

def insight_to_dashboard():
    data = response.data
    df = pd.DataFrame(data)
   
    daily_df = df["aqi_24h_avg"]
    city = df["city"]

    dates = pd.to_datetime(df["date"], utc=True)
    date_df = dates.dt.strftime("%B %d")
    days = dates.dt.day_name()
    
    category = df["category"]
    
    return daily_df, city, date_df, category, days

if __name__ == "__main__":
    insight_to_dashboard()