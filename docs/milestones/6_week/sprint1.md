# Sprint 1: Project Orientation and Team Workflow

Welcome to **Sprint 1**! 🎉

This sprint is about understanding the City Air Tracker project, deciding how your team will work together, and creating the planning artifacts that will guide implementation in later sprints.

By the end of Sprint 1, your team should be able to explain:

- what the product is intended to do
- how data will move through the system
- what major parts the team expects to build
- how the team will communicate, divide work, and review pull requests

## Sprint 1 deliverables

### 1. Product and data pipeline summary — 2 points

Write a short summary in your team's own words that explains:

- the problem City Air Tracker is intended to solve
- the data the product needs
- what the extract, transform, and load stages will do
- how the prepared data will eventually support the dashboard

Use [`what_is_a_data_pipeline.md`](../collaboration/what_is_a_data_pipeline.md) as background, but do not copy its wording.

### 2. Target architecture diagram — 5 points

Create a diagram of the system your team plans to build. Include:

- city input or configuration
- data extraction from OpenWeather
- data transformation
- PostgreSQL storage
- the dashboard API
- the React frontend
- any optional extension your team is considering

Show the major connections between these parts. The diagram is a plan, so it can change as the team learns more.

### 3. Planned runtime flow — 3 points

Create a flow diagram or written walkthrough that describes what should happen when the future pipeline runs. Include:

- where configuration enters the process
- the intended order of extract, transform, and load operations
- where data will be read and written
- where useful logging should occur
- what should happen when a step fails

### 4. City input contract — 2 points

Define the initial contract for the city input that will eventually feed the extract layer. Document:

- the purpose of the city configuration
- the required fields or columns
- one valid example
- the team's initial rules for missing or invalid values

This sprint requires the contract, not the implementation.

### 5. Practice pull request — 2 points

Complete one low-risk pull request using the team's agreed workflow. A planning artifact, the team working agreement, or a small documentation improvement are good choices.

The pull request should:

- be created from a feature branch
- have a clear title and description
- be reviewed by at least one teammate
- receive at least one useful review comment or question
- address the feedback before it is approved and merged

Use the [`feature branch and PR guide`](../collaboration/github_feature_branch_pr_guide.md) and [`PR review best practices`](../collaboration/pr_review_best_practices.md) for support.

### 6. Team working agreement — 2 points

Write down how your team agrees to work together. At minimum, decide:

- where and when the team will communicate
- how tasks and responsibilities will be divided
- how blockers will be raised
- how quickly teammates should respond to review requests
- what must happen before a pull request can be merged
- how roles and learning opportunities will be shared or rotated

## What to turn in

By the end of Sprint 1, submit:

1. A link to the reviewed practice pull request.
2. The product and data pipeline summary.
3. The target architecture diagram.
4. The planned runtime flow diagram or written walkthrough.
5. The city input contract.
6. The team working agreement.

**Total: 16 story points**

> **Note:** Sprint 1 is intentionally focused on planning and team workflow. Do not begin production feature work until the team agrees on the project direction, the city input contract, and how work will move through pull requests. If your team finishes early, start discussing city validation rules for Sprint 2.
