import pandas as pd

from pipeline.db import get_supabase_client


def raw_gold():
    supabase = get_supabase_client()
    response1 = supabase.table("raw_air_quality").select("*").execute()
    response2 = supabase.table("gold_air_quality").select("*").execute()
    raw_df = pd.DataFrame(response1.data)
    gold_df = pd.DataFrame(response2.data)
    pollutants = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]

    comp = pd.DataFrame({"Raw": raw_df[pollutants].mean(), "Gold": gold_df[pollutants].mean()})

    comp = comp.rename_axis("Pollutants").reset_index()
    gold_category = gold_df["category"]

    return comp, gold_category


if __name__ == "__main__":
    raw_gold()
