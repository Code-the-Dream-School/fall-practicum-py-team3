---
status: proposed
---

# Use Alembic with hand-written SQL for schema migrations

Every database (each teammate's personal Supabase, the team Supabase used by the AWS deployment, and the CI database) needs the same schema, built only from versioned files. We use Alembic with hand-written SQL in `op.execute`, with no ORM models or autogenerate. It is pip-installed, already a dependency, actively maintained, and catches parallel-branch conflicts before merge. Research and test results: [python-db-migration-tools.md](../reference/python-db-migration-tools.md).

## Considered Options

- **Supabase CLI**: native to Supabase, but it has no down migrations and is not pip-installable.
- **dbmate**: plain `.sql` files with up and down in one file, but it is a separate binary (brew, npm, Docker), and we don't know teammates' machines.
- **yoyo-migrations**: plain SQL and pip, but no release since 2024-08-10.
- **Jetbase**: SQL files and checksums, but pre-1.0 with one contributor. Its `postgres_schema` setting fails, and an out-of-order migration only errors on databases that already ran a newer one, which is after merge.
- **Alembic, SQL-only** (chosen): SQL lives in Python strings, and two branches adding revisions create "multiple heads".

## Consequences

- Connection: one `SUPABASE_DB_URL` (the Supabase session pooler URI, IPv4) replaces `SUPABASE_URL`/`SUPABASE_KEY`. It lives in local `.env` and the GitHub `production` Environment, never in committed files. `sqlalchemy>=2.1` is required so the plain `postgresql://` URI uses psycopg 3.
- App code (pipeline, dashboard) also connects directly to Postgres (psycopg, SQLAlchemy) instead of through the Supabase REST API (supabase-py). That way schema and data access use one connection, and the code carries over to any Postgres host.
- Layout: `alembic.ini` at the root, revisions in `db/migrations/` with dated filenames. Tables live in the `city_air` schema, as does `alembic_version`. Migrations use schema-qualified names, and app connections set `search_path=city_air`.
- Downs are optional. Write `downgrade()` when it is a clean inverse, otherwise `raise NotImplementedError`, never `pass`. Never downgrade the team database; fix forward with a new migration.
- Gates: a required `migrations` PR check (exactly one Alembic head, then `alembic upgrade head` on an empty Postgres matching Supabase's major version, with Supabase roles created) plus one approving review. Merging to `main` runs `alembic upgrade head` against the team database (`production` Environment, one run at a time).
- Dev reset: `DROP SCHEMA city_air CASCADE`, then `alembic upgrade head`.
- Migrations hold schema only. Seeding `tracked_cities` is separate.
- The team database is wiped once before the baseline migration. After that, it changes only through migrations.
