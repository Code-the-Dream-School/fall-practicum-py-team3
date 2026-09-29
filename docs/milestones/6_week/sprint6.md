# Sprint 6: Build the Dashboard and Final Demo

Welcome to **Sprint 6**, the final core sprint!

This sprint turns the pipeline your team has been building into something a user can actually look at. By the end, your data should flow from the pipeline, into PostgreSQL, through a dashboard, and onto a screen you can demo.

By the end of Sprint 6, your team should be able to explain:

- which dashboard stack the team chose and why
- how the dashboard gets data out of PostgreSQL
- what the dashboard shows a user, and why those views matter
- what a user sees when there is no data yet, the dashboard is loading, or something fails
- how to walk through the full pipeline-to-dashboard flow locally
- what the project can do today, and what it still can't

## The dashboard pivot point

Choose one path as a team:

- **React frontend with a Python API — recommended:** A Vite/React UI backed by a small Python API that reads from PostgreSQL. This matches the project's reference implementation and gives the team practice building and connecting a real frontend/backend split.
- **Streamlit with Plotly:** An all-Python dashboard that queries PostgreSQL directly, with no separate frontend or API layer to build. Both packages are already in `requirements.txt`, and this path is a reasonable choice if the team wants to spend more of the sprint on data and views instead of frontend plumbing.

Either path can satisfy every deliverable below. Make sure the team aligns on this decision and is comfortable with what that is moving forward.

## Sprint 6 scope

This sprint focuses on **presenting** the data your pipeline already produces. If the dashboard reveals a real data problem upstream, note it and make only necessary fixes to demo cleanly, rather than reopening earlier sprints' work.

## Sprint 6 deliverables

### 1. Dashboard data-serving layer — 5 points

Build the piece that turns database rows into what the dashboard displays.

- **React path:** build one or more API endpoints that query PostgreSQL and return the fields the dashboard needs.
- **Streamlit path:** build the query functions the app's pages call directly. A separate network API is not required.

Either way, keep this layer's output shape stable enough that the interface (deliverable 2) doesn't need to know how the query was built.

### 2. Dashboard interface, states, and end-to-end verification — 11 points

Build the user-facing dashboard. It should show:

- a useful summary view of the team's chosen data (current conditions, forecast, or air quality, depending on the team's Sprint 2 API choice)
- city-level detail
- at least one view that helps a user compare cities or see change over time

Handle the common non-happy-path states clearly as part of the same interface: no data yet, the dashboard is loading, the data-serving layer returns an error, and data that looks stale or incomplete.

Then confirm the whole thing end-to-end against real pipeline output, not just sample data: trigger a pipeline run, confirm it lands in PostgreSQL, confirm the data-serving layer reads it, and confirm the dashboard displays it correctly, including at least one of the non-happy-path states above. Write down the exact steps used so another teammate can repeat the check.

### 3. Final project documentation — 5 points

Update the project README or a handoff doc so someone outside the team can understand what was built and what's still unfinished or out of scope. Include the runtime settings the dashboard needs to run locally, such as database connection details, the API/dashboard port, and any other environment variables.

Include a runbook for a local walkthrough: what to run, in what order, and what an audience should see, from triggering a pipeline run to viewing the result on the dashboard.

### 4. Final demo — 3 points

Present the working project to mentors: the product, the data flow from extract through the dashboard, how the team split the work, the hardest tradeoffs, and what the team would improve with more time.

## What to turn in

By the end of Sprint 6, submit:

1. The dashboard data-serving layer.
2. The dashboard interface, including empty/loading/error state handling and end-to-end verification notes.
3. Final project documentation, including runtime configuration notes and the runbook.
4. The final demo.

**Total: 26 story points**

## End-of-sprint checkpoint

Before closing Sprint 6, mentors should review the team's project documents with the entire group.

1. **Revisit earlier decisions.** Confirm the dashboard actually reflects the API choice from Sprint 2 and the data shape from Sprint 3 and Sprint 4.
2. **Update the diagrams.** Revise the architecture and process flow diagrams one last time to show the full path from extract through the dashboard.
3. **Maintain the working documents.** Update the README, runtime configuration notes, team working agreement, and any other documentation that no longer matches the finished project.
4. **Confirm shared understanding.** Every team member should be able to walk through the full pipeline-to-dashboard flow and explain at least one part they personally built.
5. **Record the updates.** Include final documentation changes through the team's normal review workflow.

These are living documents. Even at the end of the core practicum, they should describe the project as it actually is.
