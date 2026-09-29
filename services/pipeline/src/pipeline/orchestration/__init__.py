from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

from pipeline.common.config import settings
from pipeline.common.logging import get_logger
from pipeline.extract.cities import read_cities
from pipeline.extract.geocoding import geocode_city
from pipeline.extract.openweather_air_pollution import RawAirPollutionRecord, fetch_air_pollution_history
from pipeline.load.storage import PublishResult, publish_outputs
from pipeline.run_tracking import PipelineRunStatusUpdate, create_pipeline_run, update_pipeline_run_status
from pipeline.transform.openweather_air_pollution_transform import build_gold_from_raw_records


log = get_logger(__name__)


@dataclass(frozen=True)
class PipelineRunResult:
    pipeline_run_id: int
    run_id: str
    source: str
    history_hours: int
    raw_records: list[RawAirPollutionRecord]
    gold_path: Path | None
    azure_blob_path: str | None
    postgres_table: str | None
    rows: int


def ensure_output_directories() -> tuple[Path, Path]:
    raw_dir = Path(settings.raw_dir)
    gold_dir = Path(settings.gold_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    gold_dir.mkdir(parents=True, exist_ok=True)
    return raw_dir, gold_dir


def build_runtime_window(history_hours: int) -> tuple[datetime, datetime]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=history_hours)
    return start, end


def run_extract_stage(
    raw_dir: Path, start: datetime, end: datetime, run_id: str, pipeline_run_id: int
) -> tuple[list[RawAirPollutionRecord], int]:
    cities_path = Path(settings.cities_file) if settings.cities_source == "file" else None
    cities = read_cities(cities_path)
    raw_records: list[RawAirPollutionRecord] = []

    for city in cities:
        coords = geocode_city(
            raw_dir=raw_dir,
            city=city.city,
            country_code=city.country_code,
            state=city.state,
        )
        raw_record = fetch_air_pollution_history(
            raw_dir=raw_dir,
            city=city.city,
            country_code=city.country_code,
            lat=coords.lat,
            lon=coords.lon,
            start=start,
            end=end,
            run_id=run_id,
            pipeline_run_id=pipeline_run_id,
        )
        raw_records.append(raw_record)

    return raw_records, len(cities)


def run_transform_stage(raw_records: list[RawAirPollutionRecord]) -> pd.DataFrame:
    return build_gold_from_raw_records(raw_records=raw_records)


def run_load_stage(
    gold_df: pd.DataFrame, gold_dir: Path, table_name: str = "air_pollution_gold"
) -> PublishResult:
    return publish_outputs(gold_df=gold_df, gold_dir=gold_dir, table_name=table_name)


def run_pipeline_job(source: str = "openweather", history_hours: int | None = None) -> PipelineRunResult:
    resolved_history_hours = int(settings.history_hours if history_hours is None else history_hours)
    raw_dir, gold_dir = ensure_output_directories()
    start, end = build_runtime_window(resolved_history_hours)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    pipeline_run_id = create_pipeline_run(
        run_id=run_id,
        source=source,
        history_hours=resolved_history_hours,
        window_start_utc=start,
        window_end_utc=end,
    )

    log.info(
        "Pipeline starting",
        extra={
            "run_id": run_id,
            "pipeline_run_id": pipeline_run_id,
            "source": source,
            "history_hours": resolved_history_hours,
            "window_start_utc": start.isoformat(),
            "window_end_utc": end.isoformat(),
        },
    )
    city_count = 0
    raw_records: list[RawAirPollutionRecord] = []

    try:
        log.info(
            "Extract stage starting",
            extra={"run_id": run_id, "pipeline_run_id": pipeline_run_id, "source": source},
        )
        raw_records, city_count = run_extract_stage(
            raw_dir=raw_dir,
            start=start,
            end=end,
            run_id=run_id,
            pipeline_run_id=pipeline_run_id,
        )
        log.info(
            "Extract stage complete",
            extra={
                "run_id": run_id,
                "pipeline_run_id": pipeline_run_id,
                "city_count": city_count,
                "raw_response_count": len(raw_records),
            },
        )

        log.info(
            "Transform stage starting",
            extra={"run_id": run_id, "pipeline_run_id": pipeline_run_id, "raw_response_count": len(raw_records)},
        )
        gold_df = run_transform_stage(raw_records=raw_records)
        if not gold_df.empty:
            gold_df["pipeline_run_id"] = pipeline_run_id
        log.info(
            "Transform stage complete",
            extra={"run_id": run_id, "pipeline_run_id": pipeline_run_id, "gold_row_count": len(gold_df)},
        )

        log.info(
            "Load stage starting",
            extra={"run_id": run_id, "pipeline_run_id": pipeline_run_id, "gold_row_count": len(gold_df)},
        )
        publish_result = run_load_stage(gold_df=gold_df, gold_dir=gold_dir)
        log.info(
            "Load stage complete",
            extra={
                "run_id": run_id,
                "pipeline_run_id": pipeline_run_id,
                "postgres_table": publish_result.table_name,
                "gold_path": str(publish_result.gold_path) if publish_result.gold_path is not None else None,
                "azure_blob_path": publish_result.azure_blob_path,
                "rows": publish_result.rows,
            },
        )

        update_pipeline_run_status(
            run_id,
            PipelineRunStatusUpdate(
                status="succeeded",
                city_count=city_count,
                raw_response_count=len(raw_records),
                gold_row_count=len(gold_df),
                finished_at=datetime.now(timezone.utc),
            ),
        )

        result = PipelineRunResult(
            pipeline_run_id=pipeline_run_id,
            run_id=run_id,
            source=source,
            history_hours=resolved_history_hours,
            raw_records=raw_records,
            gold_path=publish_result.gold_path,
            azure_blob_path=publish_result.azure_blob_path,
            postgres_table=publish_result.table_name,
            rows=len(gold_df),
        )

        log.info(
            "Pipeline succeeded",
            extra={
                "run_id": run_id,
                "pipeline_run_id": result.pipeline_run_id,
                "city_count": city_count,
                "raw_response_count": len(raw_records),
                "gold_row_count": result.rows,
                "postgres_table": result.postgres_table,
                "gold_path": str(result.gold_path) if result.gold_path is not None else None,
                "azure_blob_path": result.azure_blob_path,
            },
        )
        return result
    except Exception as exc:
        log.exception(
            "Pipeline failed",
            extra={
                "run_id": run_id,
                "pipeline_run_id": pipeline_run_id,
                "source": source,
                "city_count": city_count or None,
                "raw_response_count": len(raw_records) or None,
            },
        )
        update_pipeline_run_status(
            run_id,
            PipelineRunStatusUpdate(
                status="failed",
                city_count=city_count or None,
                raw_response_count=len(raw_records) or None,
                error_message=str(exc),
                finished_at=datetime.now(timezone.utc),
            ),
        )
        raise
