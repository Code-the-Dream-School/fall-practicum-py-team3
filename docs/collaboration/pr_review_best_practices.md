# City Air Tracker PR Review Best Practices

## Purpose

This guide helps reviewers give consistent, useful pull request feedback for the City Air Tracker repository.

It is project-specific on purpose. The best PR reviews do not only check style. They confirm that a change is safe for this codebase's pipeline, React dashboard, local development workflow, and documentation.

Use this guide together with the existing branch and pull request workflow materials in `docs/`.

## What a good review should do

A strong PR review should:

- confirm the change solves the stated problem
- look for behavior regressions, not only formatting issues
- check whether the change is understandable to the next contributor
- verify tests or manual checks are appropriate for the risk level
- call out missing docs, config notes, or rollout considerations

Good reviews are specific, kind, and actionable. If you request a change, explain what could break and what you want to see instead.

## Reviewer mindset

When reviewing this project, prioritize these questions:

1. Is the change correct?
2. Is it safe for the data pipeline and dashboard?
3. Can another contributor understand and maintain it?
4. Does it include enough validation for the level of risk?

That order matters more than personal style preferences.

## Recommended review flow

### 1. Start with the PR description

Before reading the diff, check whether the PR description explains:

- what changed
- why the change was needed
- how it was tested
- any follow-up work or known limitations

If the description is incomplete, ask for that context early. It makes the review faster and more accurate.

### 2. Review the change at the right level

Scan the changed files first, then review in layers:

- overall design or behavior change
- data flow impact
- edge cases and failure handling
- tests
- docs and developer experience

Avoid spending most of the review on naming or formatting if the behavior has not been validated yet.

### 3. Match the review to the type of change

Different parts of this repo need different review attention.

#### Pipeline changes

Focus on:

- correctness of extract, transform, and load behavior
- handling of API failures, retries, rate limiting, and missing data
- path and storage behavior for `data/raw` and `data/gold`
- timestamp handling, deduplication, and schema changes
- whether tests cover realistic input and output behavior

Relevant areas often include:

- `services/pipeline/run_pipeline.py`
- `services/pipeline/src/pipeline/common`
- `services/pipeline/src/pipeline/extract`
- `services/pipeline/src/pipeline/transform`
- `services/pipeline/src/pipeline/load`
- `services/pipeline/tests`

#### Dashboard changes

This branch uses a React dashboard served by `services/dashboard/server.py` and backed by PostgreSQL queries.

Focus on:

- whether the dashboard server still returns the expected payload shape
- loading, empty, and warning states
- whether metrics and labels still reflect the underlying dataset correctly
- whether tables and charts still work with current gold-schema fields
- whether the frontend remains usable after dashboard API or pipeline schema changes

Relevant areas often include:

- `services/dashboard/server.py`
- `services/dashboard/frontend/src`
- `services/dashboard/Dockerfile`
- `docker-compose.yml`

#### Infrastructure and developer workflow changes

Focus on:

- whether setup steps still work for local contributors
- Docker Compose impact
- environment variable changes
- backward compatibility for current README instructions
- whether docs were updated where contributors will look first

Relevant areas often include:

- `docker-compose.yml`
- `requirements.txt`
- `services/*/Dockerfile`
- `scripts/setup_venv.sh`
- `scripts/setup_venv.ps1`
- `README.md`
- `docs/`

## Project-specific review checklist

Use the sections below as a checklist, not as a requirement that every PR must touch every item.

### Behavior and correctness

- Does the PR do what the description claims?
- Are success and failure paths both handled?
- Are edge cases covered, such as empty data, missing files, duplicate records, or bad API responses?
- Does the change introduce assumptions that are not documented?

### Data and schema safety

- Does the shape of the gold dataset change?
- If fields are renamed, removed, or added, are downstream consumers updated?
- Are timestamp and timezone assumptions explicit?
- Could the change create duplicate rows, stale cache reads, or broken manifests?

For this branch, pay attention to fields used directly by the dashboard, such as:

- `geo_id`
- `ts`
- `aqi`
- `aqi_category`
- `pm2_5`
- `pm10`
- `risk_score`

### Testing

- Are there automated tests for the most important behavior?
- Do existing tests still describe the intended behavior?
- If automated tests are not practical, are manual verification steps clear and repeatable?
- Does the level of testing match the risk of the change?

For this project, examples of useful validation include:

- `pytest services/pipeline/tests -q`
- targeted test files for changed pipeline behavior
- `python -m pipeline.cli --source openweather --history-hours 72`
- `python services/dashboard/server.py`
- `docker compose up --build`
- verifying `/api/dashboard` returns the expected payload
- verifying the dashboard renders expected metrics and tables after a pipeline run

### Maintainability

- Is the code easy to follow without tracing too many files?
- Are helper functions, constants, and shared logic placed in the right layer?
- Is duplication introduced where an existing utility should be reused?
- Are comments and names helpful rather than noisy?

### Documentation and contributor impact

- Does the README need to change?
- Does a document in `docs/` need updating?
- If setup, environment variables, storage behavior, or local commands changed, are those instructions current?
- Will a new contributor know how to run or verify the feature?

## Writing useful review comments

Try to make each comment easy to act on. Good review comments usually include:

- the observed issue
- why it matters
- the requested change or question

Examples:

- "This changes the gold dataset fields surfaced through the dashboard API, but I do not see the React dashboard updated. Could this break the overview, trends, or compare views?"
- "The retry path handles 429 responses, but I do not see a test for exhausted retries. Can we add one?"
- "This adds a new environment variable. Please update the README setup section so local contributors do not miss it."

Avoid comments that only express taste unless the team has already agreed on a standard.

## Severity labels for feedback

It helps to signal how important a comment is. A simple approach:

- Blocker: must be fixed before merge because it can cause incorrect behavior, regressions, security issues, or broken workflows
- Major: strong recommendation because maintainability, test coverage, or clarity is meaningfully affected
- Minor: optional improvement or polish
- Question: request for clarification, not necessarily a required change

This reduces confusion and helps authors prioritize.

## What reviewers should look for in this repository

### Common risks in pipeline PRs

- silent schema drift in the gold dataset
- incorrect handling of UTC timestamps
- missing retry or rate-limit behavior around external calls
- accidental reliance on local-only file paths or state
- transforms that assume all raw records have the same shape

### Common risks in dashboard PRs

- React views that assume fields that no longer exist in the dashboard API payload
- pages that work with full data but fail with empty or partial data
- misleading metric labels or sort orders
- frontend/server assumptions drifting apart

### Common risks in docs and setup PRs

- instructions that only work on one operating system
- setup changes that update scripts but not the README
- Docker instructions that drift from local `venv` instructions

## Expectations for PR authors

Review quality improves when authors make review easier. Encourage PRs to include:

- a clear summary of the change
- screenshots for dashboard UI changes
- exact commands used for testing
- notes about schema, config, or environment changes
- focused diffs instead of unrelated cleanup

If a PR is too large to review safely, it is reasonable to ask for it to be split into smaller parts.

## Suggested merge checklist

Before approving, a reviewer should feel comfortable saying:

- I understand the goal of this change.
- I checked the parts of the system most likely to break.
- The testing is appropriate for the risk.
- The docs and setup instructions still make sense.
- I do not see an unresolved issue that should block merge.

## Keep reviews collaborative

PR review is a team quality practice, not a gatekeeping exercise.

Aim for feedback that is:

- direct
- respectful
- specific
- centered on the code and behavior

The goal is not only to catch bugs. It is also to help the project stay understandable and sustainable for the next contributor.
