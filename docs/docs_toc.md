# Docs Index

The `docs/` folder is organized by purpose so contributors can find the right starting point faster.

## Overview

Use these docs when you want an overview of the project expectations, and recommended tools/libraries.

- [Project Overview](./project_overview.md)
- [Tools and Prior Coverage](./tools_and_prior_coverage.md)

## Collaboration

Use these docs when onboarding to the repo, learning the workflow, reviewing pull requests, or reading team-facing project background material.

- [Github feature branch and PR guide](./collaboration/github_feature_branch_pr_guide.md)
- [PR review best practices](./collaboration/pr_review_best_practices.md)
- [How Github and JIRA are connected](./collaboration/how_github_and_jira_are_connected.md)
- [What is a data pipeline](./collaboration/what_is_a_data_pipeline.md)
- [Postman Installation & Guide (pdf)](./collaboration/Postman Installation & Usage Guide.pdf)

## Architecture

Use these docs when you want to understand system structure, data flow, or dashboard design.

- [Architecture diagrams (C4)](./architecture/README.md)
- [Architecture decision records](./adr/)
- [Glossary (CONTEXT.md)](../CONTEXT.md)

## Reference

Use these docs for field-level details, schemas, and API artifacts.

- [OpenWeather API Overview](./reference/openweather_api_overview.md)
- [OpenWeather Environmental API Reference](./reference/openweather_environmental_api_fields_reference.md)

## Milestones

| Sprint | Weeks | Focus |
|---|---|---|
| [1](milestones/10_week/sprint1.md) | 1–2 | Team setup, data contracts, and the extract layer |
| [2](milestones/10_week/sprint2.md) | 3–4 | PostgreSQL storage, idempotent loading, and the raw-to-gold transform |
| [3](milestones/10_week/sprint3.md) | 5–6 | LLM enrichment, an orchestrated flow, and a minimal dashboard |
| [4](milestones/10_week/sprint4.md) | 7–8 | AWS account safety, a deployed Lambda, and a schedule |
| [5](milestones/10_week/sprint5.md) | 9–10 | End-to-end run on AWS, cost teardown, and the final demo |

**Note: There is also a set of sprint milestones for a 6-week course in the milestones directory. Please ignore them.**
