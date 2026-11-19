import pandas as pd

from pipeline.db import get_supabase_client


def insight_to_dashboard():
    supabase = get_supabase_client()
    response = supabase.table("daily_insight").select("*").execute()
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
