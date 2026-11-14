# Backfill and Incremental
The pipeline supports two run modes for extracting and loading hourly air quality data into the raw_air_quality table in Supabase.

## Backfill
- The large, historical 1 year extraction (10-25-25 - 10-25-26)
- Run the **<u>main()</u>** at the bottom of **<u>load.py</u>** script.

## Incremental
- The new hourly data to be extracted.
- Run **<u>main_incremental()</u>** at the bottom of **<u>load.py</u>** script to retrieve and load new records after the most recent successful run.

## Determining What Data is New
The **<u>get_last_successful_run()</u>** (in extract.py) retrieves the most recent successful backfill or incremental run with a recorded ending timestamp.

The **<u>get_incremental_window()</u>** function uses that timestamp to calculate the next extraction window:
- The next time is 1 hour after previous successful run's ending timestamp.
- The end time is the most recent completed hour.
- If no previous successful run exists, the function raises an error.
- If there are no new completed hours, the function returns None.

Successful and failed runs are recorded using start_run(), finish_run(), and fail_run().


