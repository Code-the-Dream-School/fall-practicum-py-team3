# First deploy of migrations (one time)

Done once by a repo admin when the Alembic PR (DREAM-29) merges. After this, the team database changes only through migrations.

## Before merging

1. **Environment**: GitHub → Settings → Environments → New environment `production`. Add the secret `SUPABASE_DB_URL` = the team Supabase session pooler URI (Connect → Session pooler), password filled in. Under deployment branches, allow only `main`.
2. **Branch protection**: Settings → Branches (or Rulesets) → rule for `main`:
   - Require a pull request with 1 approval.
   - Require the status check `migrations`. It shows up in the list once it has run on a PR.
3. **CI Postgres version**: run `select version();` in the team Supabase SQL Editor. If the major version isn't 17, change `postgres:17` in `.github/workflows/migrations.yml`.
4. **Pause writes**: ask the team not to run the pipeline against the team database until step 7.

## Merge and verify

5. Merge. The `Migrations` workflow runs the `Apply migrations to production` job. Its log should show `Running upgrade  -> 9238dbc18b3d, baseline schema`.
6. Check in the SQL Editor:
   ```sql
   SELECT version_num FROM city_air.alembic_version;  -- 9238dbc18b3d
   SELECT table_name FROM information_schema.tables WHERE table_schema = 'city_air' ORDER BY 1;
   -- alembic_version, gold_air_quality, pipeline_runs, raw_air_quality
   ```

## Wipe the old tables

7. The old tables in `public` are no longer used. List them first, then drop only those:
   ```sql
   SELECT tablename FROM pg_tables WHERE schemaname = 'public';
   DROP TABLE IF EXISTS public.pipeline_runs, public.raw_air_quality, public.gold_air_quality;
   ```
   Their data came from OpenWeather and is reloaded by a Backfill Run.

## Tell the team

8. Each teammate:
   - In `.env`: add `SUPABASE_DB_URL` (their own project's session pooler URI) and remove `SUPABASE_URL` and `SUPABASE_KEY`.
   - `pip install -r requirements.txt`, then `alembic upgrade head`.
   - Optionally drop the same old `public` tables in their own project.
