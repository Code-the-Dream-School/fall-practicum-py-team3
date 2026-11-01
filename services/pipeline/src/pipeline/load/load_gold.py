from pipeline.transform.transform import REQUIRED, transform
from pipeline.load.load import supabase


def load_gold():
    try:
        # supabase only does 1000 records; so using batches
        raw_records = []
        start = 0
        batch_size = 1000
        
        while True:
            response = (
                supabase.table("raw_air_quality")
                .select("*")
                .order("city")
                .order("timestamp")
                .range(start, start + batch_size -1)
                .execute()
            )
        
            batch = response.data or []
            raw_records.extend(batch)
        
            if len(batch) < batch_size:
                break
        
            start += batch_size
            
        print(f"Fetched {len(raw_records)} raw records.")

        # transform rejects the whole batch if any row is missing a required
        # value, so drop incomplete rows first and report how many were skipped
        complete_records = [
            record for record in raw_records
            if all(record.get(field) is not None for field in REQUIRED)
        ]
        skipped = len(raw_records) - len(complete_records)
        if skipped:
            print(f"Skipped {skipped} raw records with missing values.")
        raw_records = complete_records
        
        if not raw_records:
            print("No raw records to transform.")
            return
        
        # transform raw records into gold records
        gold_records = transform(raw_records)
        
        if not gold_records:
            print("No gold records to load.")
            return
        
        # keep one record per city and timestamp/remove duplicates
        unique_records = {}
        
        for record in gold_records:
            key = (record.city, record.timestamp)
            unique_records[key] = record
            
        gold_records = list(unique_records.values())
        
        # convert GoldAirQuality models to dictionaries
        gold_records = [
            record.model_dump(mode="json")
            for record in gold_records
        ]
        
        # upsert gold records in batches of 500
        batch_size = 500
        
        for start in range(0, len(gold_records), batch_size):
            batch = gold_records[start:start + batch_size]
            supabase.table("gold_air_quality").upsert(
                batch, on_conflict="city,timestamp"
            ).execute()
        
        print(f"Loaded {len(gold_records)} gold records.")
        
    except Exception as error:
        print(f"Failed to load gold air quality records: {error}.")
        raise
        
if __name__ == "__main__":
    load_gold()
        
            
        