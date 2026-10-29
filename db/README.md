# Database migrations

Every database (your personal Supabase, the team Supabase, and the CI database) gets its schema only from the files in `db/migrations/versions/`. Alembic records which files have run in `city_air.alembic_version`, so `alembic upgrade head` applies only what is missing. Why Alembic: [ADR 0002](../docs/adr/0002-alembic-for-schema-migrations.md).

Don't change tables in the Supabase SQL Editor or dashboard. Other databases won't get the change, and the next migration may fail.

## Setup

1. `pip install -r requirements.txt`
2. In Supabase: **Connect** → **Session pooler** → copy the URI. Put it in `.env` with your password filled in:
   ```
   SUPABASE_DB_URL=postgresql://postgres.<project-ref>:<password>@<pooler-host>:5432/postgres
   ```
   Use the session pooler, not "Direct connection": the direct one is IPv6-only and fails on many networks.
3. `alembic upgrade head`

All tables live in the `city_air` schema.

## Commands

Run from the repo root.

| Command | What it does |
|---|---|
| `alembic upgrade head` | Apply all pending migrations. Run after every pull. |
| `alembic current` | Show the revision your DB is at. |
| `alembic history` | List all migrations. |
| `alembic revision -m "add insights table"` | Create a new migration file. |
| `alembic upgrade head --sql` | Print the SQL without running it. |
| `alembic downgrade -1` | Undo your last migration. Dev DB only. |

## Writing a migration

```python
def upgrade() -> None:
    op.execute("""
        ALTER TABLE city_air.pipeline_runs ADD COLUMN trigger TEXT
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE city_air.pipeline_runs DROP COLUMN trigger
    """)
```

Rules:

- **Always write `city_air.<table>`**, so a reviewer never guesses the schema.
- **Never edit a migration that is on `main`.** Other databases already ran it and won't run it again. Write a new migration instead.
- **`downgrade()`**: write the inverse when it is clean. If the change can't be undone (dropped data, lossy type change), keep the generated `raise NotImplementedError`. Never use `pass`: it marks the migration undone while the tables stay.
- **Schema only.** Data such as `tracked_cities` is loaded by the pipeline, not by migrations.
- **Never downgrade the team database.** Fix a bad migration on `main` with a new one.

## "Found 2 Alembic heads" in CI

You and a teammate both added a migration after the same parent. Rebase on `main`, then set your file's `down_revision` to the revision ID that `alembic heads` shows for main's migration. Run `alembic heads` again: it should print one line.

## Reset your dev DB

If your DB is in a weird state, or you need to undo an irreversible migration, run this on **your own** Supabase only (SQL Editor or `psql "$SUPABASE_DB_URL"`):

```sql
DROP SCHEMA city_air CASCADE;
```

Then run `alembic upgrade head`.

## CI and deploy

- Every PR runs the `migrations` check: exactly one head, then all migrations on an empty Postgres. `main` requires it to pass, plus one approving review.
- Merging to `main` runs `alembic upgrade head` against the team Supabase (GitHub Environment `production`, secret `SUPABASE_DB_URL`).
