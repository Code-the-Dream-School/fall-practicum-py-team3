# Supabase

Schema migrations live in `migrations/` as numbered `.sql` files with `-- up` / `-- down` sections.

## Apply
```sh
# via psql
psql "$DATABASE_URL" -f supabase/migrations/0001_create_pipeline_runs.sql
```
Or use the Supabase CLI: `supabase db push`.

## Schema
See `SCHEMA.md`.