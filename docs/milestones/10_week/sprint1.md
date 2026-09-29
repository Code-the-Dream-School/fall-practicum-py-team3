# Sprint 1: Team Setup, Data Contracts, and the Extract Layer

Welcome to **Sprint 1**!

**Goal: the team is set up and pulling data.**

This sprint is about deciding how your team will work together, agreeing on what the pipeline will produce, and building the first working version of the extract layer. The contracts you write now will guide every sprint that follows.

## Before you begin: review the project overview

Before starting Sprint 1, read the [Project Overview](../../project_overview.md). It explains:

- what the practicum builds and how the two phases fit together
- how the five sprints are organized
- which required and recommended tools you will use
- what to review ahead of time from Python 100 and Python 200, including the **"A Preview of the Practicum's AWS Stack"** section of Python 200's `lessons/08_cloud_intro/02_cloud_landscape.md`, which introduces the AWS services you will use in Sprints 4–5
- how project management, story points, and the Must, Should, and Could tiers work
- how to set up your team, work with mentors, and create the team repository

Come back to the overview whenever you need a reminder of how the team is meant to work.

## Sprint 1 mini-lesson

**Working as a data team: contracts and the PR workflow.** Your instructor will introduce why data teams write down the shape of their data and the signatures of their functions before writing the code behind them, and how pull requests keep a shared codebase healthy.

By the end of Sprint 1, your team should be able to explain:

- which dataset the team chose and what question the product answers
- how data will move through the system
- what the raw and gold data shapes will look like, and why they are separate
- what `extract()` accepts, what it returns, and what happens when something goes wrong
- how the team will communicate, divide work, and review pull requests

## Choose a dataset

Choose one dataset as a team:

- **Air Quality (OpenWeather):** pollutant concentrations and air quality across cities. See the [OpenWeather API overview](../../reference/openweather_api_overview.md) for which free-access endpoints are in scope.
- **Earthquakes (USGS):** recent seismic events by magnitude, depth, and location.
- **Bike Share (GBFS):** station locations and live bike and dock availability.

Every option supports the same pipeline pattern, so no choice is easier or harder overall. Choose the one your team finds most interesting, since you will live with it for ten weeks. Focus on **one primary source**. A second data source may be scoped for later, but do not build it yet.

> **No payment is required for this practicum.** Every dataset above is available without a paid plan. If a website asks for credit-card information, stop and ask your mentor for help.

> **Food for thought:** Data security is not the focus of this practicum, but API keys should still be treated as secrets. Keep real keys out of the repository by using environment variables or a local `.env` file included in `.gitignore` (see [keeping secrets and settings out of the code](../../tools_and_prior_coverage.md#keeping-secrets-and-settings-out-of-the-code)). If a real key is ever committed, revoke it and generate a replacement. You will revisit secrets management in Sprint 4.

## Sprint 1 scope

This sprint focuses on **planning and extracting data**, not storing or transforming it. Your team will define the raw and gold data shapes on paper, but you do not need to create database tables or write the transform yet. Those come in Sprint 2.

**Tools this sprint:** `requests` for API calls, `pytest` for tests, `python-dotenv` for local secrets, and Pydantic or dataclasses for contracts are all highly recommended, because you used them in Python 100 or Python 200. Mocking API responses and caching were not covered before. See [Tools and Prior Coverage](../../tools_and_prior_coverage.md).

## Sprint 1 deliverables

### Must

#### 1. Dataset choice and product summary — 3 points

Write a short summary in your team's own words that explains:

- the dataset the team selected and why
- the question or problem the product is intended to answer
- the data the product needs
- what the extract, transform, and load stages will do
- how the prepared data will eventually support the dashboard

Use [`what_is_a_data_pipeline.md`](../../collaboration/what_is_a_data_pipeline.md) as background, but do not copy its wording.

#### 2. Team working agreement — 2 points

Write down how your team agrees to work together. At minimum, decide:

- where and when the team will communicate
- how tasks and responsibilities will be divided
- how blockers will be raised
- how quickly teammates should respond to review requests
- what must happen before a pull request can be merged
- how roles and learning opportunities will be shared or rotated

#### 3. Practice pull request — 2 points

Complete one low-risk pull request using the team's agreed workflow (see [working as a team with Git and pull requests](../../tools_and_prior_coverage.md#working-as-a-team-with-git-and-pull-requests)). The team working agreement or a small documentation improvement are good choices.

The pull request should:

- be created from a feature branch
- have a clear title and description
- be reviewed by at least one teammate
- receive at least one useful review comment or question
- address the feedback before it is approved and merged

Use the [`feature branch and PR guide`](../../collaboration/github_feature_branch_pr_guide.md) and [`PR review best practices`](../../collaboration/pr_review_best_practices.md) for support.

From this point on, all code and documentation should move through pull requests.

#### 4. Data contracts — 5 points

Document the agreements the rest of the pipeline will depend on (see [writing down data contracts](../../tools_and_prior_coverage.md#writing-down-data-contracts)):

- **Raw schema:** what one stored raw record looks like, including the source payload and the context kept with it, such as the request parameters and when the data was retrieved.
- **Gold schema:** the first draft of what one clean, analysis-ready record will represent, its granularity, and its main fields. This is a draft; you will finalize it in Sprint 2 when you build the transform.
- **Function signatures:** the name, inputs, outputs, and error behavior for `extract()`, `load_raw()`, and `transform()`. You are not implementing `load_raw()` or `transform()` yet, but agreeing on their signatures now lets teammates work in parallel later.
- **Design rule:** every stage function takes plain inputs and returns plain outputs. It does not depend on a particular orchestrator, dashboard, or laptop, and it reads secrets and settings from environment variables. Later sprints call these same functions from a flow, and then from AWS Lambda, without rewriting them.
- **Input configuration:** what the pipeline needs to know before it runs, such as a list of cities, a region, a time window, or a list of stations, and the team's initial rules for missing or invalid values.

Include one valid example of each record shape.

#### 5. `extract()` client — 5 points

Create a client or function that pulls data from the team's chosen source (see [calling a web API](../../tools_and_prior_coverage.md#calling-a-web-api)). It should:

- accept validated input and any other required request options
- keep authentication and request code in one testable boundary
- return the raw response without transforming its data fields
- keep enough context with the response for later work, such as the source, the request parameters, and when the data was retrieved
- handle empty results and unsuccessful responses clearly
- support [mocked responses](../../tools_and_prior_coverage.md#testing-without-calling-the-live-api) so tests do not repeatedly call the live API

#### 6. `extract()` tests — 3 points

Add [automated tests](../../tools_and_prior_coverage.md#automated-testing) with mocked responses, plus any short manual verification notes needed to demonstrate the extract flow. Cover at least:

- one successful end-to-end extract
- invalid input
- an empty, unsuccessful, or malformed response
- a missing API key or configuration value, when the source requires one

If the team makes a live test request, record the result without committing an API key or an unnecessarily large response file.

> **Hint:** Postman is a helpful way to inspect live API responses before writing the same request in Python. See the [Postman Installation & Usage Guide](../../collaboration/Postman%20Installation%20%26%20Usage%20Guide.pdf) if the team needs help capturing or checking a sample response.

### Should

#### 7. Caching for lookups — 3 points

Some pipelines repeat the same lookup many times, such as geocoding a city name, fetching station metadata, or requesting reference data that rarely changes. Add a simple [cache](../../tools_and_prior_coverage.md#caching-repeated-lookups) so the pipeline does not repeat a lookup it has already done. Document:

- what is cached and why
- where the cache lives
- when a cached value should be refreshed or considered stale

Include a test showing that a second lookup uses the cache instead of calling the source again. If your dataset has no repeated lookups, discuss with your mentor whether another cache candidate exists.

#### 8. Refined architecture diagram — 3 points

Create or refine a diagram of the system your team plans to build. Include:

- the input configuration
- the data source and `extract()`
- raw storage
- `transform()` and gold storage
- the orchestrated flow that will run the stages
- the dashboard
- the eventual AWS deployment, even if it is only a sketch

Show the major connections between these parts. The diagram is a plan, so it can change as the team learns more.

### Could

#### 9. Second data source scoped for later — 2 points

Write a short note describing one additional data source that could enrich the team's dataset, why it would help, and roughly what it would take to add. Do not build it. This is a planning artifact for a future sprint.

## What to turn in

By the end of Sprint 1, submit:

1. The dataset choice and product summary.
2. The team working agreement.
3. A link to the reviewed practice pull request.
4. The data contracts.
5. The `extract()` client and its tests.
6. If completed, the caching implementation, the refined architecture diagram, and the second-source note.

**Total: 20 core story points, or 26 with the Should deliverables (28 with the Could)**

> **Note:** Do not begin Sprint 2 work until the team agrees on the data contracts and how work will move through pull requests. If your team finishes early, start thinking about how raw records should be stored so that loading the same data twice does not create duplicates.
