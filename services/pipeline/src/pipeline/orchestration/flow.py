from __future__ import annotations
import sys
from pathlib import Path
from typing import Mapping
from prefect import flow, get_run_logger, task

PROJECT_ROOT = Path(__file__).resolve().parents[5]
PIPELINE_SRC = Path(__file__).resolve().parents[2]
for path in (PROJECT_ROOT, PIPELINE_SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from pipeline.extract.extract import (
    CITIES,
    END,
    START,
    City,
    RawAirQuality,
    extract,
    extract_all_windows,
)
from pipeline.load.load import load_raw
from pipeline.transform.transform import transform as transform_records
from schemas import GoldAirQuality

RAW_DIR = PIPELINE_SRC / "pipeline" / "extract" / "cities_raw"


# ---------------------------------------------------------------------------- #
@task(retries=2, retry_delay_seconds=10)
def extract_city(city_name: str, city: City) -> RawAirQuality:
    logger = get_run_logger()

    # cache
    cache_path = RAW_DIR / f"{city_name.lower().replace(' ', '_')}.json"
    if cache_path.exists():
        cached = RawAirQuality.model_validate_json(
            cache_path.read_text(encoding="utf-8")
        )
        parameters = cached.request_parameters
        if (
            parameters.lat == city.LAT
            and parameters.lon == city.LON
            and parameters.start == city.START
            and parameters.end == city.END
        ):
            logger.info(f"Using cached extract for {city_name}")
            return cached

    logger.info(f"Fetching extract for {city_name}")
    if city.START == START and city.END == END:
        extracted = extract_all_windows(city_name, {"LAT": city.LAT, "LON": city.LON})
    else:
        extracted = extract(city)

    # ensure dir exists > RawAirQuality to JSON > write as plain text
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(extracted.model_dump_json(), encoding="utf-8")
    return extracted


# ---------------------------------------------------------------------------- #
@task(retries=2, retry_delay_seconds=5)
def load_records(records: list[dict]) -> int:
    if not records:
        logger = get_run_logger()
        logger.error("Load stage received no records")
        raise ValueError("Load stage received no records")
    load_raw(records)
    return len(records)


# ---------------------------------------------------------------------------- #
@task(retries=2, retry_delay_seconds=5)
def transform(records: list[dict]) -> list[GoldAirQuality]:
    return transform_records(records)


# ---------------------------------------------------------------------------- #
@task(retries=2, retry_delay_seconds=5)
def enrich(records: list[dict]) -> list[dict]:
    return records


# ---------------------------------------------------------------------------- #
@flow(name="air-quality-pipeline", log_prints=True)
def run_pipeline(
    mode: str = "historical",
    # raw coordinate dicts or fully configured City (Pydantic model) objects
    inputs: Mapping[str, Mapping[str, float] | City] | None = None,
    start: int = START,
    end: int = END,
) -> dict:
    logger = get_run_logger()
    result_counts = {"extract": 0, "load": 0, "transform": 0, "enrichment": 0}
    stage = "configuration"

    try:
        logger.info("Pipeline starting", extra={"mode": mode})
        if not isinstance(mode, str) or not mode.strip():
            raise ValueError("mode must not be empty")
        if start >= end:
            raise ValueError("start must be earlier than end")

        city_inputs = CITIES if inputs is None else inputs
        if not city_inputs:
            raise ValueError("inputs must contain at least one city")

        logger.info("Configuration stage complete")

        # ---------------------------------------------------------------------------- #
        stage = "extract"
        logger.info("Extract stage starting")
        raw_records = []
        for city_name, city_input in city_inputs.items():
            city = (
                city_input
                if isinstance(city_input, City)
                else City(
                    LAT=city_input["LAT"],
                    LON=city_input["LON"],
                    START=start,
                    END=end,
                )
            )
            extracted = extract_city(city_name, city)
            records = extracted.to_raw_schema(city_name)
            logger.info(
                f"Extracted records for {city_name}",
                extra={"records": len(records)},
            )
            raw_records.extend(records)
        result_counts["extract"] = len(raw_records)
        logger.info(f"Extract stage complete - {len(raw_records)} records total")
        if not raw_records:
            raise ValueError("Extract completed without records")

        # ---------------------------------------------------------------------------- #
        stage = "load"
        logger.info("Load stage starting")
        result_counts["load"] = load_records(raw_records)
        logger.info("Load stage complete")

        # ---------------------------------------------------------------------------- #
        stage = "transform"
        logger.info("Transform stage starting")
        transformed_records = transform(raw_records)
        result_counts["transform"] = len(transformed_records)
        logger.info("Transform stage complete")

        # ---------------------------------------------------------------------------- #
        # stage = "enrichment"
        # logger.info("Enrichment stage starting")
        # enriched_records = enrich(transformed_records)
        # result_counts["enrichment"] = len(enriched_records)
        # logger.info("Enrichment stage complete")

        # ---------------------------------------------------------------------------- #
        result = {"status": "success", "mode": mode, "counts": result_counts}
        logger.info("Pipeline succeeded", extra=result)
        logger.info(f"Counts: {result_counts}")
        return result
    except Exception:
        logger.exception(f"Pipeline failed during {stage}", extra={"mode": mode})
        raise


if __name__ == "__main__":
    run_pipeline()
