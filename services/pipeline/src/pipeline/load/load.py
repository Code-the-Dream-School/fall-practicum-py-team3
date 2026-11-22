from datetime import UTC, datetime

from pipeline.db import get_supabase_client
from pipeline.extract.extract import CITIES, City, extract_incremental_window, get_incremental_window
from pipeline.extract.extract import extract as ext
from pipeline.log import get_logger
from pipeline.run_tracking import fail_run, finish_run, start_run

logger = get_logger(__name__)


# Load raw data to db
def load_raw(records):
    supabase = get_supabase_client()
    try:
        batch_size = 2000
        total = len(records)
        total_loaded = 0
        for offset in range(0, total, batch_size):
            batch = records[offset : offset + batch_size]
            response = supabase.table("raw_air_quality").upsert(batch, on_conflict="city,timestamp").select().execute()
            total_loaded += len(response.data)
        logger.info("Upserted %s rows into raw_air_quality", total_loaded)
        return total_loaded
    except Exception as error:
        logger.exception("Failed to load raw air quality records: %s", error)
        raise


# incremental
def main_incremental():
    # get next extraction window
    window = get_incremental_window()

    if window is None:
        logger.info("No new completed hours to extract.")
        return

    start, end = window

    window_start = datetime.fromtimestamp(start, UTC).isoformat()

    window_end = datetime.fromtimestamp(end, UTC).isoformat()

    run_id = start_run(run_mode="incremental", window_start=window_start, window_end=window_end)

    rows_extracted = 0
    rows_loaded = 0

    try:
        for name, coords in CITIES.items():
            extraction = extract_incremental_window(name, coords, start, end)

            records = extraction.to_raw_schema(name)

            rows_extracted += len(records)

            rows_loaded += load_raw(records)

            logger.info("%s: %s records extracted", name, len(records))

        finish_run(
            run_id,
            rows_extracted=rows_extracted,
            rows_loaded=rows_loaded,
            rows_transformed=0,
        )

        logger.info("Incremental extraction and loading completed")

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
        window_start=datetime.fromtimestamp(1761350400, UTC).isoformat(),
        window_end=datetime.fromtimestamp(1792886400, UTC).isoformat(),
    )

    rows_loaded = 0

    try:
        for name, coords in CITIES.items():
            city = City(LAT=coords["LAT"], LON=coords["LON"], START=1761350400, END=1792886400)

            extraction = ext(city)
            records = extraction.to_raw_schema(name)

            logger.info("%s records: %s", name, len(records))

            rows_loaded += load_raw(records)

        finish_run(
            run_id,
            rows_extracted=0,
            rows_transformed=0,
            rows_loaded=rows_loaded,
        )

        logger.info("Raw loading completed successfully.")

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

    main()  # uncomment for backfill
    # main_incremental() # uncomment for incremental
