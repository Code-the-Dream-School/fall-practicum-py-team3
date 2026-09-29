# Sprint 3: Enrich, Orchestrate, and Show the Data

Welcome to **Sprint 3**!

**Goal: one orchestrated flow runs the whole pipeline, and a dashboard shows the result.**

This sprint finishes the local phase of the practicum. Your team will add an LLM enrichment step, wrap the pipeline in a flow that can retry and log, and put a small dashboard on top of the gold data. Next sprint, the same stage functions are deployed to the cloud.

## Sprint 3 mini-lesson

**Backfill vs. incremental: why a pipeline runs two ways.** Your instructor will introduce the difference between loading history once and processing only new data on each run, and why a well-built pipeline supports both.

By the end of Sprint 3, your team should be able to explain:

- what the LLM adds to a gold record and how the team keeps that work from being repeated or wasted
- the difference between a backfill run and an incremental run in your pipeline
- what one run of the flow does, start to finish
- what happens when a step fails, and what is retried
- what the dashboard shows a user, and what a user sees when there is no data or something fails
- what the pipeline depends on that must be available outside your laptop, such as environment variables and secrets

## Start with the Sprint 2 handoff

Before writing new code, review the team's:

- gold table and data dictionary
- `pipeline_runs` records, if the team built run tracking
- idempotency rules for `load_raw()`
- unanswered questions from the Sprint 2 handoff

## Sprint 3 scope

This sprint focuses on **adding an enrichment stage, coordinating the pipeline, and presenting the data**. It is not the place to redesign extract, load, or transform. If a stage needs to change to fit the flow, make the smallest change that works and note the rest as a follow-up.

**LLM enrichment** (see [enriching data with an LLM](../../tools_and_prior_coverage.md#enriching-data-with-an-llm)) can use any LLM API your team is comfortable with. Python 200 introduces working with LLM APIs. Treat the LLM key as a secret, and keep costs low by testing with small batches.

**Orchestration** (see [orchestrating the pipeline with retries and logging](../../tools_and_prior_coverage.md#orchestrating-the-pipeline-with-retries-and-logging)): the project needs one entry point that runs the stages in order, retries what can be retried, and logs what happened. **Prefect** is recommended, since you built flows with it in Python 200 and it wraps existing Python functions without a custom scheduling loop. A plain Python runner with its own retry loop and logging also satisfies the deliverable. Whatever you choose, the flow calls the same `extract()`, `load_raw()`, and `transform()` functions from earlier sprints rather than duplicating their logic. Those functions stay independent of the orchestrator, so in Sprint 4 a Lambda handler can call them exactly as your flow does.

**Dashboard** (see [showing the data in a dashboard](../../tools_and_prior_coverage.md#showing-the-data-in-a-dashboard)): **Streamlit** with Plotly is recommended, since you used both in Python 100. Any framework that shows the data and handles empty and error states satisfies the deliverable.

**Tools this sprint:** an LLM API, Prefect, Streamlit, Plotly, and `scikit-learn` are all highly recommended, because they were taught explicitly in Python 100 or Python 200. Backfill runs were only briefly covered. See [Tools and Prior Coverage](../../tools_and_prior_coverage.md).

## Sprint 3 deliverables

### Must

#### 1. Enrichment contract — 3 points

Decide what the LLM adds to your data and document it before writing the code. Good enrichment produces something a rule-based transform cannot easily produce, such as a plain-language summary, a short explanation, or a classification of free text. Document:

- which gold records get enriched and which are skipped
- the fields the enrichment adds, with their types and allowed values
- the prompt or instructions the team uses, and where they are stored
- what should happen when the model returns something unusable, empty, or malformed

#### 2. LLM enrichment — 5 points

Implement enrichment as its own stage that reads gold records and writes the enriched results. It must be **incremental and idempotent**:

- only records that have not been enriched yet are sent to the LLM
- running it again does not repeat work or create duplicate results
- results record which model and prompt version produced them
- failures on one record do not stop the rest of the batch and are recorded clearly

Include automated tests with a mocked LLM response, so tests run without an API key and without cost.

#### 3. Backfill and incremental modes — 3 points

Make the pipeline able to run in two ways (see [backfill and incremental runs](../../tools_and_prior_coverage.md#backfill-and-incremental-runs)):

- **backfill:** process a specified history or window of data
- **incremental:** process only what is new since the last successful run

Document how each mode is chosen, and use the run records from Sprint 2 (or another documented approach) to decide what is new. Include a test or documented check showing that an incremental run after a backfill does not reprocess the same data.

#### 4. Orchestrated flow with retries and logging — 8 points

Wrap the pipeline in a flow (a Prefect `@flow` is recommended) that runs extract, load, transform, and enrichment in order. The flow should:

- accept the configuration a run needs, such as the mode and the inputs
- retry steps that are likely to fail temporarily, such as network calls, and not retry steps that will fail the same way every time
- log the start of the run, each stage boundary, success, and failure
- return or record a structured result, such as status and counts per stage
- avoid hiding or silently swallowing errors from any stage

A teammate who was not in the room should be able to read the logs from a failed run and tell which stage failed and why. Include tests or a documented manual check showing a successful run and at least one failure that is reported clearly.

#### 5. Minimal dashboard — 5 points

Build a small dashboard (Streamlit is recommended) that reads gold data from the database and shows:

- a useful summary view of the team's chosen data
- at least one chart or table that helps a user compare records or see change over time
- the LLM enrichment, where it makes sense to display it

Handle the common non-happy-path states clearly: no data yet, loading, and an error reaching the database. Keep database credentials out of the repository. Document how to run the dashboard locally.

### Should

#### 6. ML classifier as a second transform — 8 points

Train a small [machine learning classifier](../../tools_and_prior_coverage.md#training-a-machine-learning-classifier) on your gold data and integrate it into the pipeline as a second transform, sometimes called a "double transform." The classifier reads gold fields, predicts a label, and writes the prediction back. Document:

- what the classifier predicts and why it is useful
- which features it uses and where the labels come from
- how it was trained and evaluated, including how well it performs
- how predictions are stored and how the model is loaded at run time

The classifier does not need to be perfect. A simple, honest, explainable model is better than a complicated one. Python 200 covers scikit-learn and model evaluation.

### Could

#### 7. Dashboard polish and extra charts — 3 points

Improve the dashboard's clarity and usefulness with additional charts, filters, or layout changes. Make sure new views also handle empty and error states.

## What to turn in

By the end of Sprint 3, submit:

1. The enrichment contract.
2. The LLM enrichment stage and its tests.
3. The backfill and incremental modes.
4. The orchestrated flow, with retries, logging, and verification notes.
5. The dashboard and instructions for running it locally.
6. If completed, the ML classifier and its evaluation notes.
7. If completed, the dashboard polish.

**Total: 24 core story points, or 32 with the Should deliverable (35 with the Could)**

## End-of-sprint checkpoint

Before closing Sprint 3, mentors should review the team's project documents with the entire group.

1. **Revisit earlier decisions.** Confirm the gold data, enrichment, and dashboard still match the product goal from Sprint 1.
2. **Update the diagrams.** Revise the architecture and process flow diagrams to show the enrichment stage, the orchestrated flow, the two run modes, and the dashboard.
3. **Check the stage functions.** Confirm that `extract()`, `load_raw()`, `transform()`, and the enrichment stage each work when called on their own, without the flow, the dashboard, or local files. List the environment variables and secrets they need. This list is the starting point for Sprint 4.
4. **Maintain the working documents.** Update the README, runtime configuration notes, data dictionary, team working agreement, and other documentation when assumptions or team practices change.
5. **Confirm shared understanding.** Every team member should be able to walk through one full run of the flow and explain the difference between a backfill and an incremental run.
6. **Record the updates.** Include documentation changes through the team's normal review workflow and summarize important open questions for Sprint 4.
7. **Take a breather.** The important part of an agile project is making sure your team can reset and prepare for the next sprint in a sustainable way. Breathe. Watch a movie. Sleep. Rinse and repeat.

These are living documents, not one-time submissions. As the project changes, the documentation should change with it.
