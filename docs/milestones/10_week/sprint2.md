# Sprint 2: Store Raw Data and Transform It to Gold

Welcome to **Sprint 2**!

**Goal: the pipeline runs by hand, from source to gold table.**

This sprint gives the project a real database and turns raw records into clean, useful ones. By the end, your team should be able to run extract, load, and transform on your own machines and see raw and gold rows land in your PostgreSQL database, even when the same data is loaded twice.

## Sprint 2 mini-lesson

**The raw→gold pattern and idempotent writes.** Your instructor will introduce why pipelines keep untouched raw data separate from clean gold data, and why every write should be safe to repeat.

By the end of Sprint 2, your team should be able to explain:

- what tables exist and why
- how a raw record and a gold record are stored
- how the team decided on keys and uniqueness for each table
- what happens when the same data is loaded twice
- how raw fields become the gold fields, including the category and the score
- how to create the schema from an empty database

## Start with the Sprint 1 handoff

Before designing tables, review the team's:

- raw and gold schema drafts and function signatures
- input configuration rules
- `extract()` output and the sample responses used in its tests
- unanswered questions from Sprint 1

Resolve unclear field or key questions before writing any schema code.

## Sprint 2 scope

This sprint focuses on **persisting and transforming data**, not orchestrating the pipeline. Your team should be able to run `extract()`, `load_raw()`, and `transform()` by hand, or with a simple script, and see rows land in the database. Orchestration, enrichment, and the dashboard come in Sprint 3.

**Required:** the database must be PostgreSQL (see [storing data in a database](../../tools_and_prior_coverage.md#storing-data-in-a-database)).

**Recommended:** **Supabase**, a hosted PostgreSQL database that you used with `supabase-py` in Python 200. Sign up for a free project, use the connection details it provides, and keep them out of the repository just as you would an API key. Any other way of reaching Postgres also works, such as SQLAlchemy from Python 100, a Postgres driver with raw SQL, or a Postgres database you run yourself. A plain `.sql` script or a migration tool will each satisfy the schema deliverable. Pick what your team can explain and maintain.

**Tools this sprint:** upsert-based idempotent writes (Python 200), `pandas` for transforms (Python 100), and `pytest` (Python 200) are highly recommended. Migration tools and rolling aggregates were not covered before. See [Tools and Prior Coverage](../../tools_and_prior_coverage.md).

## Sprint 2 deliverables

### Must

#### 1. PostgreSQL schema — 5 points

Design and create the tables the pipeline needs, grouped into three areas:

- **raw:** the untouched source responses, matching the Sprint 1 raw contract
- **gold:** the clean, transformed records, matching the Sprint 1 gold contract as you finalize it in this sprint
- **logs:** the pipeline's own bookkeeping, such as run records (see deliverable 7)

For each table, document the primary key, any foreign keys, uniqueness rules, and which columns are required. Create the schema through a repeatable script or migration (see [creating and changing the database schema](../../tools_and_prior_coverage.md#creating-and-changing-the-database-schema)), so a teammate can start from an empty database and apply it without manually creating tables. Document how to run it.

> **Tool tip:** With a group of collaborators sharing one database, even a slight difference in schema, such as a column changing from a number to text, can break the pipeline. Make sure everyone applies schema changes the same way.

#### 2. Idempotent `load_raw()` — 5 points

Implement `load_raw()`, which writes the output of `extract()` to the raw table. It must be **idempotent** (see [idempotent writes](../../tools_and_prior_coverage.md#idempotent-writes)): running it twice with the same data leaves the database in the same state as running it once. The function should:

- decide what makes a raw record unique, and document that rule
- skip or update duplicates instead of inserting them again
- keep this layer responsible for writing only, without re-running extraction or transformation
- report clearly when a write fails, rather than hiding the error

#### 3. `transform()` to gold — 5 points

Implement `transform()` (see [cleaning and transforming records](../../tools_and_prior_coverage.md#cleaning-and-transforming-records)), which reads raw records and produces gold records in the agreed shape. It should:

- flatten nested source data when needed
- standardize timestamps, units, and data types
- handle missing or malformed values according to rules the team writes down
- add **a category** and **a score** derived from the raw fields
- avoid calling the live API

The category and the score should each support the product goal from Sprint 1. Some examples:

| Dataset | Example category | Example score |
|---|---|---|
| Air Quality | Air quality label (Good, Fair, Poor) | Index or pollutant-based risk value |
| Earthquakes | Magnitude class (minor, moderate, major) | Significance or impact value |
| Bike Share | Availability status (empty, low, healthy, full) | Percent of docks in use |

Do not add derived fields only because they are possible. Each field should support the agreed product goal.

#### 4. Load and transform tests — 3 points

Add automated tests that do not require a live API key or an unrelated database. Cover at least:

- a representative successful load and transform
- loading the same raw data twice without creating duplicates
- an empty input
- a missing or malformed required field
- the category and score for known inputs, including edge cases at their boundaries

Tests should verify the output contract, not only that the function completes without an error.

### Should

#### 5. Data dictionary — 3 points

For every field in the gold table, document:

- field name
- meaning or description
- data type
- unit or format, when applicable
- source field or transformation rule
- whether it is required or optional

The gold contract defines the shape of a record; the data dictionary explains each field in it.

#### 6. Rolling aggregates — 3 points

Add at least one [rolling or windowed value](../../tools_and_prior_coverage.md#rolling-aggregates) to the gold data, such as a moving average, a count over the last several observations, or a change from the previous reading. Document the window and what it helps a user understand, and add tests for it.

#### 7. Run tracking in `pipeline_runs` — 3 points

Add a `pipeline_runs` table in the logs area and write one record per run. At minimum, record when the run started and ended, its status, and counts of rows extracted, loaded, and transformed. When a run fails, the record should say so. This table is what future you will check first when the pipeline misbehaves.

### Could

#### 8. Richer derived fields — 2 points

Add one or two more derived fields that make the gold data more useful, such as a trend label, a comparison to a long-run average, or a flag for unusual values. Document each in the data dictionary and add tests.

## What to turn in

By the end of Sprint 2, submit:

1. The PostgreSQL schema and repeatable setup workflow.
2. The idempotent `load_raw()`.
3. `transform()` with the category and score.
4. The load and transform tests.
5. If completed, the data dictionary, rolling aggregates, and `pipeline_runs` tracking.
6. If completed, any richer derived fields.

**Total: 18 core story points, or 27 with the Should deliverables (29 with the Could)**

## End-of-sprint checkpoint

Before closing Sprint 2, mentors should review the team's project documents with the entire group. Use this same checkpoint at the end of every future sprint.

1. **Revisit earlier decisions.** Review every Sprint 1 deliverable and identify assumptions that changed during Sprint 2.
2. **Update the diagrams.** Revise the architecture diagram to show the raw, gold, and logs tables and the boundaries between extract, load, and transform.
3. **Maintain the other working documents.** Update the product summary, data contracts, data dictionary, team working agreement, and any other project documentation that no longer reflects how the team is working or what it is building.
4. **Reflect on the team process.** Discuss what the pull requests, reviews, meetings, communication, and blocker-handling revealed. Adjust the working agreement when the team finds a better way to collaborate.
5. **Confirm shared understanding.** Every team member should be able to trace a representative record from the source, through the raw table, into the gold table. Everyone should review and agree with the documented decisions.
6. **Record the updates.** Include documentation changes in a reviewed PR and summarize important open questions for Sprint 3.

These are living documents, not one-time submissions. As the project changes, the documentation should change with it.
