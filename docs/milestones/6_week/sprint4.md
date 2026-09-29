# Sprint 4: Persist Data to PostgreSQL

Welcome to **Sprint 4**!

This sprint is about giving the project a real database. Your team will take the raw response contract from Sprint 2 and the transform contract and data dictionary from Sprint 3, and turn them into PostgreSQL tables that the pipeline can write to and the dashboard can eventually read from.

By the end of Sprint 4, your team should be able to explain:

- what tables exist and why
- how a raw response and a transformed record are stored
- how the team decided on keys and uniqueness for each table
- what happens when the same data is loaded twice
- what a pipeline run record looks like and what it tracks
- how to create the schema from an empty database

## Start with the Sprint 3 handoff

Before designing tables, review the team's:

- transform input/output contract and data dictionary
- normalization and data-quality rules table, including any rules flagged for the database layer
- raw response contract and sample from Sprint 2
- unanswered questions from the Sprint 3 handoff

Resolve unclear field or key questions before writing migrations.

## Sprint 4 scope

This sprint focuses on **persisting data**, not orchestrating the pipeline or serving it to a dashboard. Your team should be able to run the extract, transform, and load steps by hand, or with a simple script, and see rows land in PostgreSQL. A shared pipeline runner, CLI entrypoint, and scheduling come in Sprint 5. The dashboard and API layer that reads this data comes in Sprint 6.

`requirements.txt` already includes a few packages suited to this sprint. None are required — use whatever tools your team is comfortable with — but each maps directly to a deliverable below:

- **`psycopg`** connects Python to PostgreSQL. You need a driver like this (or an equivalent) no matter how you build the schema or write records.
- **`sqlalchemy`** lets you define tables as Python code and query them without hand-writing every SQL statement. Useful for deliverable 1 (schema) and deliverable 3 (persistence), especially as the number of tables grows.
- **`alembic`** generates and applies schema migrations from SQLAlchemy table definitions, which is exactly what deliverable 2 (a repeatable bootstrap workflow) asks for.

A team could also write raw SQL and a plain `.sql` bootstrap script and satisfy every deliverable just as well. Pick what your team can explain and maintain.

## Sprint 4 deliverables

### 1. Database schema — 5 points

Design the PostgreSQL tables needed to persist the project's data, built directly from the Sprint 3 transform contract and data dictionary. At minimum, plan tables for:

- raw API responses, matching the Sprint 2 raw response contract
- transformed records, matching the Sprint 3 data dictionary
- any location or reference data the team's chosen API depends on, such as geocoded coordinates, if it is not already captured elsewhere
- pipeline run tracking (see deliverable 5)

For each table, document the primary key, any foreign keys, uniqueness rules, and which columns are required. Update the architecture diagram to show where these tables fit.

### 2. Migration or bootstrap workflow — 3 points

Create a repeatable workflow that builds the schema from deliverable 1, such as Alembic migrations or a plain `.sql` bootstrap script. A teammate should be able to start from an empty database and apply the schema without manually creating tables. Document how to run it.

> **Tool tip:** migrations are a very important piece of how your project will run smoothly, especially with a group of collaborators working through the same database schema. Even the slightest difference in schema (i.e. changing the datatype from num to char) can have drastic impacts on the ETL process. Ensure that the team is comfortable at this point on the migration method chosen and how to make new updates to the database once it is set.

### 3. Raw and transformed record persistence — 5 points

Implement the functions or module that write raw responses and transformed records to the database, matching the shapes defined in the Sprint 2 and Sprint 3 contracts. Keep this layer responsible for reading and writing only — it should not re-run extraction or transformation logic.

### 4. Record keys and upsert behavior — 3 points

Decide how each record type is uniquely identified, and implement update-or-insert (upsert) behavior so a repeated pipeline run updates existing rows instead of creating duplicates. Document what counts as a new record versus an updated one for your data.

### 5. Pipeline run tracking — 2 points

Track each pipeline run in the database: status (success or failure), start and end time, and useful counts such as raw responses stored and transformed rows written. Sprint 5's pipeline runner will build on this.

### 6. Storage tests and verification — 5 points

Add automated tests, or verification notes where a test is impractical, covering:

- writing a new raw response and a new transformed record
- re-running with the same input, confirming upsert does not create duplicates
- updating an existing record's values
- an empty or missing input
- applying the migration/bootstrap workflow to an empty database

### Optional: Archive or Parquet export — 5 points

Add a secondary export path, such as Parquet files, for raw or transformed records. Keep it secondary to the PostgreSQL path and document when it should run.

## What to turn in

By the end of Sprint 4, submit:

1. The database schema and updated architecture diagram.
2. The migration or bootstrap workflow.
3. The raw and transformed record persistence implementation.
4. The record key and upsert behavior, documented and implemented.
5. Pipeline run tracking.
6. Storage tests and verification notes.
7. If completed, the optional archive/Parquet export.
8. A short Sprint 5 handoff note describing how the pipeline runner should call these persistence functions.

**Total: 23 core story points, or 28 with the optional archive/Parquet export**

## End-of-sprint checkpoint

Before closing Sprint 4, mentors should review the team's project documents with the entire group.

1. **Revisit earlier decisions.** Confirm that the Sprint 2 API choice and Sprint 3 transform contract still match what the team learned while designing the schema.
2. **Update the diagrams.** Revise the architecture and process flow diagrams to show the database tables, the load boundary, and the planned handoff to the Sprint 5 pipeline runner.
3. **Maintain the working documents.** Update the data dictionary, normalization rules table, team working agreement, and other documentation when assumptions or team practices change.
4. **Confirm shared understanding.** Every team member should be able to trace a field from the raw response, through the transform, and into its stored table. Everyone should review and agree with the documented decisions.
5. **Record the updates.** Include documentation changes through the team's normal review workflow and summarize important open questions for Sprint 5.

These are living documents, not one-time submissions. As the project changes, the documentation should change with it.
