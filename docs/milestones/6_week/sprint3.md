# Sprint 3: Transform Raw Data into Useful Records

Welcome to **Sprint 3**!

This sprint is about turning the raw OpenWeather responses from Sprint 2 into clean, predictable records that the rest of the project can use. Each team's transformation will depend on its selected API and dashboard goal, but every team should be able to explain how its raw fields become useful application data.

By the end of Sprint 3, your team should be able to explain:

- what one transformed record represents
- how raw API fields map to the transformed output
- which fields are required, optional, renamed, or derived
- how timestamps, units, missing values, and repeated records are handled
- what the future database and dashboard will receive from the transform layer

## Start with the Sprint 2 handoff

Before writing transform code, review the team's:

- selected primary API and dashboard direction
- trimmed raw response sample
- raw response contract and extraction metadata
- location-input approach
- unanswered questions from the Sprint 2 handoff

Resolve unclear input assumptions before dividing the transform work. Use a representative raw payload from the team's selected API as the shared example throughout the sprint.

## Sprint 3 scope

This sprint focuses on **transforming data**. Teams should define the clean data shape that later stages need. This is where the team takes the diagrams built in Sprint 1 and turns them into real dashboard inputs that the system can use.

Supplementary integrations such as maps or geocoding may need their own transform path. Think about how the choices you make here will shape the Sprint 4 database schema and what the dashboard should later fetch from:

- Which transformed fields need to be stored in the database?
- Which fields are only useful for the dashboard and do not need to be persisted?
- Does this data become its own table, or does it belong in an existing one?
- What relationships between transformed records might the Sprint 4 schema need to model? Which fields might serve as keys or identifiers?
- Which pieces should the dashboard request directly, and which should be prepared ahead of time?

## Sprint 3 deliverables

### 1. Transform input and output contract — 3 points

Define what the transform receives and what it returns. Document the following, and update the existing process flow diagrams to show where the transform receives and returns data:

- the expected raw payload and extraction context
- the granularity of an output record, such as one location snapshot or one location at one timestamp
- how raw fields map to clean fields
- one example transformed record

This contract describes application data, not a final PostgreSQL schema.

### 2. Data dictionary — 3 points

The transform contract defines the input and output shape; the data dictionary explains each field in that output. For every transformed field, document:

- field name
- meaning or description
- data type
- unit or format, when applicable
- source field or transformation rule
- whether it is required or optional

#### Transform I/O contract compared with the data dictionary

A simple distinction is:

- transform I/O contract = the rulebook for the function
- data dictionary = the glossary for the transformed fields

For example, the transform contract might map the raw `dt` field to a required `observed_at` field. The data dictionary explains that `observed_at` represents the observation time, identifies its type and format, and notes how the application will use it.

### 3. Raw-to-clean transform implementation — 5 points

Submit the Python source file or files that perform the raw-to-clean transformation. The implementation must provide a callable function that:

- accepts a raw response and its location or request context
- reads the fields selected in the transform contract
- flattens nested API data when needed
- returns records in the agreed clean shape
- supports payloads containing one or many observations
- does not call the live API or write to the database

Keep API access, transformation, and future storage responsibilities separate so each layer can be tested independently. A reviewer should be able to pass a Sprint 2 raw response into the function and receive the record shape defined in deliverable 1.

### 4. Normalization rules table and implementation — 3 points

Submit a short table that lists each normalization or data-quality rule and shows how the transform handles it. Implement those rules in the transform code. Address the rules relevant to the team's selected API, including:

- timestamps and time zones
- measurement units
- numeric and text types
- missing required and optional fields
- duplicate or repeated observations
- meaningful labels or derived values, when useful to the dashboard

Do not add derived fields only because they are possible. Each field should support the agreed product or dashboard goal.

> **Tool tip:** If the transform performs calculations, consider placing reusable operations in a helper module such as an `operations.py` file. This keeps unit conversions, aggregations, moving averages, min-max scaling and other agreed derived values consistent and testable. See this [simple Python module example](https://www.plus2net.com/python/module-calculator.php#google_vignette) for the basic pattern.

#### Mentor and student consideration: Sprint 4 data-quality handoff

Data quality should be shared between the transform layer and PostgreSQL, with each layer handling what it does best. Depending on the team's Sprint 3 capacity, data quality can be deferred until Sprint 4.

- **Sprint 3 transform:** Convert units and types, standardize timestamps, rename or derive fields, and decide how malformed or missing API values are handled.
- **Sprint 4 database:** Enforce storage integrity with column types, `NOT NULL`, `CHECK`, `UNIQUE`, primary keys, and foreign keys.

Some rules belong in both places. For example, the transform can reject a missing required value, while a `NOT NULL` constraint protects the database if invalid data still reaches it.

### 5. Automated transform tests — 5 points

Submit automated tests that pass representative raw API responses through the transform and verify the resulting clean records. Reuse or adapt the sanitized samples and mocked responses created in Sprint 2; new fixture files are only needed when an additional test case requires them.

Include tests for at least:

- a representative successful response
- an empty response
- a response with missing optional fields
- a response with a missing or malformed required field
- repeated records or timestamps, when applicable

Tests should run without a live API key and should verify the clean output contract, not only that the function completes without an error.

> **Hint:** Postman's bread-and-butter is inspecting live API responses and confirming raw inputs used by the test suite. See the [Postman Installation & Usage Guide](../collaboration/Postman%20Installation%20&%20Usage%20Guide.pdf) if the team needs help capturing or checking a sample response.

## What to turn in

By the end of Sprint 3, submit:

1. The transform input and output contract.
2. The data dictionary.
3. The Python source files containing the raw-to-clean transform implementation.
4. The normalization and data quality rules table and the corresponding rules implemented in the transform.
5. The automated transform tests, using Sprint 2 response samples or any additional test inputs the team needs.

**Total: 19 story points**

## End-of-sprint checkpoint

Before closing Sprint 3, mentors should review the team's project documents with the entire group.

1. **Revisit earlier decisions.** Confirm that the Sprint 2 API choice, raw response contract, and dashboard direction still match what the team learned while transforming real payloads.
2. **Update the diagrams.** Revise the architecture and process flow diagrams to show the transform boundary, clean output, error paths, and planned handoff to storage.
3. **Maintain the working documents.** Update the product summary, input and data contracts, data dictionary, team working agreement, and other documentation when assumptions or team practices change.
4. **Confirm shared understanding.** Every team member should be able to trace a representative field from the raw response through the transform and into the clean output. Everyone should review and agree with the documented decisions.
5. **Record the updates.** Include documentation changes through the team's normal review workflow and summarize important open questions for Sprint 4.

These are living documents, not one-time submissions. As the project changes, the documentation should change with it.
