# Sprint 5: Wire Up the Pipeline Runtime

Welcome to **Sprint 5**!

Up to this point, extract, transform, and load have mostly been exercised as separate pieces. This sprint connects them into one repeatable pipeline that can be triggered by hand or on a schedule, with enough logging that a teammate can tell what happened during any given run.

By the end of Sprint 5, your team should be able to explain:

- what one call to the shared runner does, start to finish
- how the runner reports success and failure
- how to trigger a run manually from the command line
- what the logs show for a healthy run versus a failed run
- how a scheduled run is configured and triggered
- what needs to be set before a run works outside your own machine

## Sprint 5 scope

This sprint focuses on **coordinating and running** the pipeline that already exists — it is not the place to redesign extract, transform, or load. If a stage's behavior needs to change to fit the runner, make the smallest change that works and note the rest as a follow-up.

`prefect` is already listed in `requirements.txt`. It's a good fit for deliverable 4 (a scheduler entrypoint) because it can wrap an existing Python function as a scheduled, observable flow without your team writing a custom scheduling loop. It is not required — a `cron` entry, a GitHub Actions schedule, or your own lightweight scheduler loop can satisfy the same deliverable just as well. Whatever your team picks, it should call the shared runner from deliverable 1 rather than duplicate its logic.

If the team is short on time, prioritize the shared runner, the CLI path, and logging first. The scheduler entrypoint depends on those being solid, so it's the right place to slow down rather than rush.

## Sprint 5 deliverables

### 1. Shared pipeline runner — 8 points

Build a reusable runner that calls extract, transform, and load in order for a given run. The runner should:

- accept whatever configuration a run needs, such as the list of locations
- call each stage in sequence and stop or report clearly when a stage fails
- return a structured result describing what happened, such as status and counts per stage
- avoid hiding or silently swallowing errors from any stage

Include automated tests proving the runner calls stages in the correct order, that a full successful run returns the expected result shape, and that at least one failure case (such as a stage raising an error) is reported clearly instead of crashing silently or continuing as if nothing happened.

### 2. Manual CLI entrypoint — 3 points

Provide a command-line way to trigger a run through the shared runner, for example `python -m services.pipeline.run_pipeline`. Preserve whatever manual run path already existed, but route it through the runner instead of calling extract, transform, and load separately.

Verify, with a test or a documented manual check, that the CLI actually triggers a run and surfaces a failure clearly rather than failing silently.

### 3. Runtime logging — 3 points

Add log messages around pipeline start, each stage boundary, success, and failure. A teammate who was not in the room should be able to read the logs from a failed run and tell which stage failed and why.

### 4. Scheduler entrypoint and schedule configuration — 5 points

Add an entrypoint that a scheduler can call to trigger a run, wrapping the shared runner rather than reimplementing it. Document how the schedule itself should be configured: run frequency, any history or lookback window, and where that configuration lives.

Confirm the entrypoint actually works by triggering a scheduled or automated-style run and checking its status, logs, and the resulting effect in the database. Document the exact check the team used so a teammate can repeat it.

### 5. Runtime configuration and secrets guidance — 2 points

Document the environment variables and settings a run needs, such as database connection details and the API key. Note what is safe to commit, what must stay out of the repository, and how local runs and scheduled runs should each be configured.

## What to turn in

By the end of Sprint 5, submit:

1. The shared pipeline runner, with its tests.
2. The manual CLI entrypoint, with its verification notes.
3. Runtime logging around each stage.
4. The scheduler entrypoint, schedule configuration notes, and validation that a triggered run worked.
5. Runtime configuration and secrets guidance.

**Total: 21 story points**

## End-of-sprint checkpoint

Before closing Sprint 5, mentors should review the team's project documents with the entire group.

1. **Maintain the working documents.** Update the runtime configuration notes, team working agreement, and other documentation when assumptions or team practices change.
2. **Confirm shared understanding.** Every team member should be able to trace a manual run and a scheduled run through the same shared runner. Everyone should review and agree with the documented decisions.
3. **Record the updates.** Include documentation changes through the team's normal review workflow and summarize important open questions for Sprint 6.
4. **Take a breather.** If it wasn't said before, the important part of an agile project is making sure your team can reset and prep for the next sprint in a sustainable way. Breath. Watch a movie. Sleep. Rinse-and-Repeat.

These are living documents, not one-time submissions. As the project changes, the documentation should change with it.
