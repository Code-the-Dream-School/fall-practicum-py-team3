# Tools and Prior Coverage

This guide lists the concepts your team will work with during the practicum, the tools or approaches we suggest for each, and where you may have seen them before. Concepts are listed in the order they are introduced in the project, and each header says which sprint introduces it.

## How to read this guide

Each row is labeled in one of these ways:

- **Required:** no alternative. The practicum is about this tool or service.
- **Highly recommended:** taught explicitly in Python 100 or Python 200. Your team already has practice with it, so it is the lowest-risk choice.
- **Recommended:** touched on in a course, or a reasonable choice that was not the focus of a lesson.
- **Alternative:** another way to meet the same deliverable. Using one is fine as long as your team can explain and maintain it.
- **Not covered before:** the concept was not taught in either course. It is introduced in the sprint's mini-lesson or learned on the fly.

Sprint deliverables are written in terms of the concept, such as "a PostgreSQL database" or "an orchestrated entry point," not a specific tool. Choosing a different approach than the recommended one never breaks the project.

**Where it was covered** points to a lesson you can revisit. Paths are relative to each course repository:

- **Python 100:** `python-for-data-analysis-v3`, branch `main`
- **Python 200:** `python-200-v1`, branch `v3`

---

## Working as a team with Git and pull requests
*Introduced in Sprint 1*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| Git feature branches and GitHub pull requests | Highly recommended | Python 100: `lessons/01 - Advanced Python and Regex/01_setting_up.md` and `CONTRIBUTING.md` |
| JIRA for planning and tracking | Required | Introduced in Sprint 1. Your mentor sets it up. |

## Calling a web API
*Introduced in Sprint 1*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| `requests` | Highly recommended | Python 100: `lessons/02 - Intro to Data Engineering with Pandas/02_loading_saving_data.md`. Python 200: `lessons/09_cloud_data/03_loading_pipeline.md` |
| `httpx` | Alternative | N/A |
| `urllib` (standard library) | Alternative | N/A |

## Keeping secrets and settings out of the code
*Introduced in Sprint 1, revisited in Sprint 4 on AWS*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| `.env` file with `python-dotenv` | Highly recommended | Python 200: `lessons/05_AI_intro/02_completions_api.md`, `lessons/09_cloud_data/01_connecting_supabase.md` |
| Operating-system environment variables set in your shell | Alternative | N/A |

## Writing down data contracts
*Introduced in Sprint 1*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| Pydantic models | Highly recommended | Python 200: `lessons/01_production_python/03_pydantic.md` |
| Dataclasses and type hints | Highly recommended | Python 200: `lessons/01_production_python/02_dataclasses_and_types.md` |
| `TypedDict` | Alternative | N/A |
| Plain dictionaries with a schema written in your docs | Alternative | N/A |

## Automated testing
*Introduced in Sprint 1, used in every sprint*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| `pytest` (fixtures, parametrize) | Highly recommended | Python 200: `lessons/01_production_python/04_pytest.md` |
| `unittest` (standard library) | Alternative | N/A |

## Testing without calling the live API
*Introduced in Sprint 1, reused for the LLM in Sprint 3*

The goal is that tests never depend on a live API, an API key, or a network connection. This concept was **not covered before** in Python 100 or Python 200.

| Tool or approach | Level | Where it was covered |
|---|---|---|
| Saved sample responses used as test inputs | Recommended | Not covered before. Postman, described in the project's collaboration docs, is one way to capture a sample. |
| `unittest.mock` | Alternative | N/A |
| `pytest`'s `monkeypatch` | Alternative | N/A |
| A hand-written fake client | Alternative | N/A |

## Caching repeated lookups
*Introduced in Sprint 1 (Should)*

This concept was **not covered before** in Python 100 or Python 200.

| Tool or approach | Level | Where it was covered |
|---|---|---|
| In-memory dictionary | Recommended | Not covered before |
| `functools.lru_cache` | Alternative | N/A |
| A JSON file on disk | Alternative | N/A |
| A database table | Alternative | N/A |

## Storing data in a database
*Introduced in Sprint 2*

Supabase and SQLAlchemy both help your code talk to a database, but they work at different levels. The database itself must be PostgreSQL. How your code reaches it is your team's choice.

| Tool or approach | Level | Where it was covered |
|---|---|---|
| PostgreSQL | Required | Python 200: `lessons/09_cloud_data/02_supabase_tables.md` (through Supabase) |
| Supabase (hosted Postgres) with `supabase-py` | Highly recommended | Python 200: `lessons/09_cloud_data/01_connecting_supabase.md`, `02_supabase_tables.md`, `03_loading_pipeline.md` |
| SQLAlchemy | Recommended | Python 100: `lessons/08 - Advanced SQL and Integration/04_sqlalchemy.md`. The lesson focuses on SQLite and only shows a Postgres URL. |
| `psycopg` (Postgres driver) with raw SQL | Recommended | Python 200 uses it only in an optional pgvector section: `lessons/06_AI_augmentation/03_llamaindex.md` |
| A Postgres database you run yourself | Alternative | N/A |

## Creating and changing the database schema
*Introduced in Sprint 2*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| SQL `CREATE TABLE` in the Supabase SQL editor | Highly recommended | Python 200: `lessons/09_cloud_data/02_supabase_tables.md` |
| SQL scripts kept in the repository | Recommended | Python 100: `lessons/07 - Databases and SQL/02_creating_populating_databases.md` covers the SQL, though not as a team workflow |
| Migration tools such as Alembic | Alternative | N/A. Optional, since a plain `.sql` script run in order satisfies the deliverable. |

## Idempotent writes
*Introduced in Sprint 2, reused for enrichment in Sprint 3*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| Upsert with `on_conflict` | Highly recommended | Python 200: `lessons/09_cloud_data/02_supabase_tables.md` ("Upsert"), `03_loading_pipeline.md`, `lessons/11_cloud_ETL/02_build_pipeline.md` |
| SQL `INSERT ... ON CONFLICT` | Alternative | N/A |
| Checking for an existing row before inserting | Alternative | N/A |

## Cleaning and transforming records
*Introduced in Sprint 2*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| `pandas` | Highly recommended | Python 100: `lessons/03 - Data Cleaning and Validation/` and `lessons/04 - Data Wrangling and Aggregation/` (including `04_derived_features.md`) |
| Plain Python lists and dictionaries | Alternative | N/A |

## Rolling aggregates
*Introduced in Sprint 2 (Should)*

Python 100 covers grouping and aggregation in `lessons/04 - Data Wrangling and Aggregation/01_grouping_aggregation.md`, but neither course covers rolling windows.

| Tool or approach | Level | Where it was covered |
|---|---|---|
| `pandas` `.rolling()` | Recommended | Not covered before |
| SQL window functions | Alternative | N/A |

## Enriching data with an LLM
*Introduced in Sprint 3*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| An LLM API (the courses use OpenAI) | Highly recommended | Python 200: `lessons/05_AI_intro/02_completions_api.md`, `lessons/10_llm_pipelines/03_llm_enrichment.md` |
| Another LLM provider your team can access at low or no cost | Alternative | N/A |

## Backfill and incremental runs
*Introduced in Sprint 3*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| Incremental processing (only new records) | Recommended | Python 200: `lessons/10_llm_pipelines/03_llm_enrichment.md`, `lessons/11_cloud_ETL/02_build_pipeline.md` |
| Backfill (processing a history window) | Recommended | Python 200 mentions it briefly in `lessons/10_llm_pipelines/02_ml_inference.md`. Taught in the Sprint 3 mini-lesson. |

## Orchestrating the pipeline with retries and logging
*Introduced in Sprint 3*

You need one entry point that runs the pipeline in order, retries what can be retried, and logs what happened.

| Tool or approach | Level | Where it was covered |
|---|---|---|
| Prefect (`@flow`, `@task`, retries, run logger) | Highly recommended | Python 200: `lessons/10_llm_pipelines/04_orchestration.md`, `lessons/11_cloud_ETL/01_prefect_revisited.md`, `02_build_pipeline.md` |
| A plain Python runner with your own retry loop | Alternative | N/A |
| Python's `logging` module | Alternative | N/A |

## Showing the data in a dashboard
*Introduced in Sprint 3*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| Streamlit | Highly recommended | Python 100: `lessons/09 - Interactive Visualization and Dashboards/02_streamlit.md` |
| Plotly (charts) | Highly recommended | Python 100: `lessons/09 - Interactive Visualization and Dashboards/01_plotly.md` |
| Another framework that shows the data and handles empty and error states | Alternative | N/A |

## Training a machine learning classifier
*Introduced in Sprint 3 (Should)*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| `scikit-learn` | Highly recommended | Python 200: `lessons/02_ML_intro/02_scikit_learn.md`, `lessons/03_ML_classification`, `lessons/10_llm_pipelines/01_double_transform.md`, `02_ml_inference.md` |
| PyTorch | Alternative | Python 200 covers PyTorch in its deep learning lessons |

---

The rest of this guide has no alternatives, because deploying to AWS is the point of the practicum. The only choice is between SNS and Slack for failure alerts. Python 200 gives an orientation only, in `lessons/08_cloud_intro/02_cloud_landscape.md` ("A Preview of the Practicum's AWS Stack"). It does not teach these hands-on, so the mini-lessons introduce them.

## Keeping the AWS account safe
*Introduced in Sprint 4*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| AWS Budgets | Required | Not covered before |
| IAM (limited users and roles) | Required | Orientation only: the Python 200 lesson above |
| SSM Parameter Store for secrets | Required | Orientation only: the Python 200 lesson above |

## Running code on demand
*Introduced in Sprint 4*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| AWS Lambda (handler and packaging) | Required | Orientation only: the Python 200 lesson above. `lessons/11_cloud_ETL/03_production_ready.md` also compares a Prefect flow to a Lambda handler. |

## Scheduling a run
*Introduced in Sprint 4*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| EventBridge schedule | Required | Orientation only: the Python 200 lesson above |

## Logs and alarms
*Introduced in Sprint 4 (alarms are Should)*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| CloudWatch logs | Required | Orientation only: the Python 200 lesson above |
| CloudWatch alarms | Required if the team completes it | Orientation only: the Python 200 lesson above |

## Deploying automatically
*Introduced in Sprint 4 (Could)*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| GitHub Actions (CI/CD) | Required if the team completes it | Not covered before |

## Failure alerts
*Introduced in Sprint 5 (Should)*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| SNS | Required (choose SNS or Slack) | Not covered before |
| A Slack alert | Required (choose SNS or Slack) | Not covered before |

## Capturing failed events
*Introduced in Sprint 5 (Could)*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| Dead-letter queue | Required if the team completes it | Only named in a comparison table: Python 200 `lessons/11_cloud_ETL/03_production_ready.md` |

## Packaging a Lambda as a container
*Introduced in Sprint 5 (Could)*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| Container image Lambda | Required if the team completes it | Not covered before. Python 200 uses Docker only in an optional section of `lessons/06_AI_augmentation/03_llamaindex.md`. |

## Describing infrastructure as code
*Introduced in Sprint 5 (Could)*

| Tool or approach | Level | Where it was covered |
|---|---|---|
| AWS SAM | Required if the team completes it | Not covered before |
