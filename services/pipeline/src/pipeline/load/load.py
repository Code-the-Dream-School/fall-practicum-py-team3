from pipeline.log import get_logger

logger = get_logger(__name__)
import data_contracts.schemas as schemas
from pipeline.db import get_supabase_client
from pipeline.config import settings

from pipeline.extract.extract import extract as ext, City, CITIES, get_incremental_window, extract_incremental_window
from pipeline.run_tracking import start_run, finish_run, fail_run
from datetime import datetime, timezone

# Load raw data to db
def load_raw(ext):
    supabase = get_supabase_client()
    try:
        batch_size = 2000
        total = len(records)
        total_loaded = 0 # running count of rows saved
        for offset in range(0, total, batch_size): # starting indicies > each as offset
            batch = records[offset : offset + batch_size] # list slicing > sublist
            batch_number = offset // batch_size + 1 # integer division > +1 for ordinal
            print(
                f"Upserting batch {batch_number} "
                f"({len(batch)} of {total} rows) into raw_air_quality"
            )
            
            # Records are unique by city and timestamp.
            # Upsert updates existing records instead of creating duplicates.
            response = (
                supabase.table("raw_air_quality")
                .upsert(batch, on_conflict="city,timestamp")
                .execute()
            )
            total_loaded += len(response.data) # add batch's saved rows to count
            print(f"Upserted {len(response.data)} rows in batch {batch_number}")
            return total_loaded

        logger.info("Upserted %s rows into raw_air_quality", len(response.data))
        return len(response.data)

    except Exception as error:
        logger.exception("Failed to load raw air quality records: %s", error)
        raise

# incremental
def main_incremental():
    # get next extraction window
    window = get_incremental_window()

    if window is None:
        print("No new completed hours to extract.")
        return

    start, end = window

    window_start = datetime.fromtimestamp(
        start, timezone.utc
    ).isoformat()

    window_end = datetime.fromtimestamp(
        end, timezone.utc
    ).isoformat()

    run_id = start_run(
        run_mode="incremental",
        window_start=window_start,
        window_end=window_end
    )

    rows_extracted = 0
    rows_loaded = 0

    try:
        for name, coords in CITIES.items():
            extraction = extract_incremental_window(
                name, coords, start, end
            )

            records = extraction.to_raw_schema(name)

            rows_extracted += len(records)

            rows_loaded += load_raw(records)

            print(f"{name}: {len(records)} records extracted")

        finish_run(
            run_id,
            rows_extracted=rows_extracted,
            rows_loaded=rows_loaded,
            rows_transformed=0,
        )

        print("Incremental extraction and loading completed")

    except Exception as error:
        fail_run(
            run_id,
            error,
            rows_extracted=rows_extracted,
            rows_loaded=rows_loaded,
        )
        raise

def main():
    run_id = start_run(
        run_mode="backfill",
        window_start=datetime.fromtimestamp(
            1761350400, timezone.utc
        ).isoformat(),
        window_end=datetime.fromtimestamp(
            1792886400, timezone.utc
        ).isoformat(),
    )

    rows_loaded = 0

    try:
        for name, coords in CITIES.items():
            city = City(
                LAT=coords["LAT"],
                LON=coords["LON"],
                START=1761350400,
                END=1792886400
            )

            extraction = ext(city)
            records = extraction.to_raw_schema(name)

            print(f"{name} records: {len(records)}")

            rows_loaded += load_raw(records)

        finish_run(
            run_id,
            rows_extracted=0,
            rows_transformed=0,
            rows_loaded=rows_loaded,
        )

        print("Raw loading completed successfully.")

    except Exception as error:
        fail_run(
            run_id,
            error,
            rows_loaded=rows_loaded,
        )
        raise






if __name__ == "__main__":
    # !!! PLEASE READ BELOW !!!
    # run ONE mode at a time
    # main() = backfill (10-25-25 thru 10-25-26)
    # main_incremental() = new hourly data


    # main() # uncomment for backfill
    main_incremental() # uncomment for incremental
