"""baseline schema

Tables as they were on main before Alembic (supabase/*.sql), moved into city_air.

Revision ID: 9238dbc18b3d
Revises:
Create Date: 2026-10-29 00:35:14.747610

"""
from typing import Sequence, Union

from alembic import op

revision: str = '9238dbc18b3d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Only our own connection (postgres) reaches these tables, never the Supabase API roles
    op.execute("""
        REVOKE ALL ON SCHEMA city_air FROM anon, authenticated
    """)

    op.execute("""
        CREATE TABLE city_air.pipeline_runs (
            run_id           BIGINT       GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            created_at       TIMESTAMPTZ  NOT NULL DEFAULT now(),
            started_at       TIMESTAMPTZ,
            ended_at         TIMESTAMPTZ,
            status           TEXT         NOT NULL DEFAULT 'pending',
            rows_extracted   INTEGER,
            rows_transformed INTEGER,
            rows_loaded      INTEGER,
            error_message    TEXT,

            CONSTRAINT pipeline_runs_status_check
                CHECK (status IN ('pending', 'running', 'success', 'failed'))
        )
    """)

    op.execute("""
        CREATE TABLE city_air.raw_air_quality (
            city         TEXT             NOT NULL,
            timestamp    TIMESTAMPTZ      NOT NULL,
            aqi          DOUBLE PRECISION,
            co           DOUBLE PRECISION,
            no           DOUBLE PRECISION,
            no2          DOUBLE PRECISION,
            o3           DOUBLE PRECISION,
            so2          DOUBLE PRECISION,
            pm2_5        DOUBLE PRECISION,
            pm10         DOUBLE PRECISION,
            nh3          DOUBLE PRECISION,
            retrieved_at TIMESTAMPTZ      NOT NULL,

            PRIMARY KEY (city, timestamp)
        )
    """)
    op.execute("""
        ALTER TABLE city_air.raw_air_quality ENABLE ROW LEVEL SECURITY
    """)

    op.execute("""
        CREATE TABLE city_air.gold_air_quality (
            city      TEXT        NOT NULL,
            timestamp TIMESTAMPTZ NOT NULL,
            aqi       NUMERIC,
            co        NUMERIC,
            no        NUMERIC,
            no2       NUMERIC,
            o3        NUMERIC,
            so2       NUMERIC,
            pm2_5     NUMERIC,
            pm10      NUMERIC,
            nh3       NUMERIC,
            category  TEXT,
            score     NUMERIC,

            PRIMARY KEY (city, timestamp)
        )
    """)


def downgrade() -> None:
    op.execute("""
        DROP TABLE city_air.gold_air_quality, city_air.raw_air_quality, city_air.pipeline_runs
    """)
