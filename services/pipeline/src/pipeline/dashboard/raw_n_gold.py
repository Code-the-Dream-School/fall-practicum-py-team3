import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

response1 = (
    supabase.table("raw_air_quality").select("*").execute()
)

response2 = (
    supabase.table("gold_air_quality").select("*").execute()
)

def raw_gold():
    raw_df = pd.DataFrame(response1.data)
    gold_df = pd.DataFrame(response2.data)
    pollutants = ['co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']

    comp = pd.DataFrame({
        'Raw': raw_df[pollutants].mean(),
        'Gold': gold_df[pollutants].mean()
    })

    comp = comp.rename_axis("Pollutants").reset_index()
    gold_category = gold_df["category"]
    
    return comp, gold_category

if __name__ == "__main__":
    raw_gold()