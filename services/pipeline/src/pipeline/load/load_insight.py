import pandas as pd

from pipeline.insight_data import get_gold_records
from pipeline.load.load import supabase
from pipeline.run_tracking import start_run, finish_run, fail_run

def load_insight():
    run_id = start_run()
    rows_extracted = 0
    rows_transformed = 0
    rows_loaded = 0
    
    try:
        # retrieve gold records from supabase / already batched
        gold_records = get_gold_records(supabase)
        rows_extracted = len(gold_records)
        
        print(f"Fetched {len(gold_records)} gold records.")
        
        if not gold_records:
            print("No gold records to process.")
            finish_run(
                run_id,
                rows_extracted=rows_extracted,
                rows_transformed=rows_transformed,
                rows_loaded=rows_loaded,
            )
            return
        
        # format / filter:
        
        # convert records to a DF
        df = pd.DataFrame(gold_records)
        
        # convert timestamp to dt to work with and extract date
        df["_timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df["date"] = df["_timestamp"].dt.date
        
        # daily insight records
        daily_records = []
        
        # group by city and date (instead of timestamp, since its a daily table)
        for (city, date), group in df.groupby(["city", "date"]):
            
            # keep only days with 18+ hours
            if group["_timestamp"].nunique() < 18:
                continue
            
            # get the latest hourly record
            latest_record = group.loc[group["_timestamp"].idxmax()]
            
            # use its rolling 24hr aqi avg
            daily_average = int(round(latest_record["aqi_24h_avg"]))
            
            daily_records.append({
                "city": city,
                "timestamp": latest_record["timestamp"],
                "date": date.isoformat(),
                "category": latest_record["category"],
                "aqi_24h_avg": daily_average
            })
            
        rows_transformed = len(daily_records)
            
        if not daily_records:
            print("No daily records with at least 18 hours.")
            finish_run(
                run_id,
                rows_extracted=rows_extracted,
                rows_transformed=rows_transformed,
                rows_loaded=rows_loaded,
            )
            return
        
        print(f"Prepared {len(daily_records)} daily records.")
        
        # load daily records in batch of 500
        batch_size = 500
        
        for start in range(0, len(daily_records), batch_size):
            batch = daily_records[start:start + batch_size]
            
            supabase.table("daily_insight").upsert(
                batch,
                on_conflict="city,timestamp"
            ).execute()
            
            rows_loaded += len(batch)
            
        print(f"Loaded {len(daily_records)} daily insight records.")

        finish_run(
            run_id,
            rows_extracted=rows_extracted,
            rows_transformed=rows_transformed,
            rows_loaded=rows_loaded,
        )

    except Exception as error:
        fail_run(
            run_id,
            error,
            rows_extracted=rows_extracted,
            rows_transformed=rows_transformed,
            rows_loaded=rows_loaded,
        )
        print(f"Failed to load daily insight records: {error}.")
        raise

if __name__ == "__main__":
    load_insight()            
        