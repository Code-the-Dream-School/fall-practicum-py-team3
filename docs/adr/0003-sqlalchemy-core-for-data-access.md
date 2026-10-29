---
status: proposed
---

# Use SQLAlchemy Core for data access

The pipeline and dashboard read and write Postgres directly through SQLAlchemy Core, not through the Supabase REST API (supabase-py). Tables are reflected from the database, so the Alembic migrations ([ADR 0002](0002-alembic-for-schema-migrations.md)) stay the only schema definition. Core keeps the chained `table → insert/update/select → execute` style the team knows from supabase-py, and it is already a dependency and taught in Python 100.

## Considered Options

- **supabase-py**: what the course teaches. But it needs separate API credentials (`SUPABASE_URL`/`SUPABASE_KEY`) next to the migration URL. It only reaches schemas exposed in each project's dashboard, so the tables would sit in the API-exposed `public` schema and need RLS. It also only works with Supabase.
- **Raw SQL with psycopg**: no abstraction, but SQL strings in Python are new for the team.
- **SQLAlchemy ORM / SQLModel**: model classes repeat every column already defined in the migrations, so the two drift. Upserts drop back to Core anyway.
- **SQLAlchemy Core with reflected tables** (chosen).

## Consequences

- One connection setting, `SUPABASE_DB_URL`, for code and migrations. The code works on any Postgres host, not only Supabase.
- `pipeline.db` provides `engine()` and `table(name)`. `table(name)` replaces `supabase.table(name)`. Usage is in `db/README.md`.
- Reflection needs the table to exist, so `alembic upgrade head` must run before the code uses a new table or column.
