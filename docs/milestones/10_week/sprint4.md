# Sprint 4: Take the Pipeline to AWS

Welcome to **Sprint 4**!

**Goal: the pipeline runs in AWS on a schedule, with no laptop involved.**

This sprint begins the cloud phase. Your team will set up an AWS account with safety rails, call the ingest steps from a Lambda function, deploy it, and schedule it. Your database and dashboard stay where they are. The stage functions you built and tested in Sprints 1–3 do not change. They get a new caller.

## Sprint 4 mini-lessons

This sprint opens with two mini-lessons, one each week:

- **Week 7: Serverless and setting up a cloud account safely.** Your instructor will introduce the "ephemeral, triggered compute" model, where code runs only when something triggers it, and how to set up an AWS account so a mistake does not become a bill: Budgets, limited IAM permissions, and SSM Parameter Store for secrets.
- **Week 8: Packaging and deploying a Lambda, and scheduling with EventBridge.** Your instructor will introduce how a Python function and its dependencies become a deployable Lambda, and how EventBridge triggers it on a schedule.

By the end of Sprint 4, your team should be able to explain:

- what safety rails are in place on the AWS account and what each one protects against
- what "serverless" means, and what changes when the pipeline no longer runs on a machine you control
- how the code and its dependencies get from the repository into a Lambda
- where the Lambda gets its secrets and configuration
- how a scheduled run is triggered and where to find its logs
- how to confirm a run worked

## Start with the Sprint 3 handoff

Before creating any AWS resources, review the team's:

- list of laptop dependencies from the Sprint 3 checkpoint
- the orchestrated flow and the stage functions it calls
- runtime configuration notes and secrets
- unanswered questions from the Sprint 3 handoff

## Sprint 4 scope

This sprint focuses on **deploying and scheduling** the ingest stage. It is not the place to redesign extract, load, or transform. The Lambda handler calls the same stage functions your team already built and tested, exactly as the flow does. Your local flow (Prefect, if you used it) stays useful for local development and testing, but the scheduled run in AWS is triggered by EventBridge. If a stage function cannot run on its own, make the smallest fix that works and note it in your deployment notes.

**Required:** every AWS service in this sprint is required, since deploying to AWS is the point of the practicum. Python 200 gave you an orientation to Lambda, EventBridge, IAM, CloudWatch, and Parameter Store, but did not teach them hands-on, so the mini-lessons this sprint cover them. See [Tools and Prior Coverage](../../tools_and_prior_coverage.md).

> **Stay inside the safety rails.** Nothing in this practicum requires a paid AWS plan. Create the Budgets alarm before deploying anything. Do not create resources your team has not discussed, and do not share access keys or commit them to the repository. If something looks like it could cost money, stop and ask your mentor.

Decide as a team who owns the AWS account. Everyone should understand what is in it, and every student should get hands-on time with the console or command line, even if one person creates the account.

## Sprint 4 deliverables

### Must

#### 1. AWS account and safety rails — 5 points

Set up the AWS account the team will use and put safety measures in place before deploying anything (see [keeping the AWS account safe](../../tools_and_prior_coverage.md#keeping-the-aws-account-safe)). Include:

- a **Budgets alarm** that notifies the team well before spending becomes a concern
- a **limited IAM user or role** for day-to-day work, so the root account is not used for deployment
- secrets stored in **SSM Parameter Store** instead of code or environment files, including the database connection and any API keys
- a short document explaining what each safeguard does and who on the team can access what

#### 2. Lambda handler and packaging — 5 points

Write a Lambda handler (see [running code on demand](../../tools_and_prior_coverage.md#running-code-on-demand)) that calls the ingest steps, `extract()`, `load_raw()`, and `transform()`. The handler should:

- be thin, calling the existing stage functions instead of duplicating their logic
- read configuration and secrets from the Lambda's environment and SSM, not from local files
- return or log a structured result, such as status and counts per stage
- report failures clearly instead of swallowing them

Package the code and its dependencies in a form Lambda can run, and document how to rebuild the package. Include a way to test the handler locally, such as calling it with a sample event.

#### 3. Ingest Lambda deployed — 3 points

Deploy the Lambda to AWS and confirm it works when invoked by hand. Document the exact steps used to deploy it and the check used to confirm it wrote to the database, so a teammate can repeat them. Give the Lambda only the permissions it needs.

#### 4. Deployment notes and runtime configuration — 2 points

Write down everything a teammate needs to reproduce or change the deployment:

- the AWS resources created and what each does
- the configuration and secrets the Lambda needs, where they live, and which are safe to commit
- how the local and cloud runs differ
- known issues and open questions

### Should

#### 5. LLM enrichment as a second Lambda — 5 points

Deploy the enrichment stage from Sprint 3 as its own Lambda, so ingest and enrichment can run and fail independently. Document how the enrichment Lambda is triggered, such as by its own schedule, and how it decides which records to enrich. Keep its idempotent behavior from Sprint 3.

#### 6. A basic CloudWatch alarm — 3 points

Create at least one CloudWatch alarm that tells the team when something is wrong, such as when the Lambda reports errors. Document what the alarm watches, what threshold it uses, and who is notified.

### Could

#### 7. EventBridge schedule and CloudWatch logs — 5 points

Schedule the Lambda with EventBridge (see [scheduling a run](../../tools_and_prior_coverage.md#scheduling-a-run)), and use CloudWatch to see what happened (see [logs and alarms](../../tools_and_prior_coverage.md#logs-and-alarms)). Document:

- the schedule and why the team chose that frequency
- how a scheduled run differs from a manual invocation, if at all
- where to find the logs for a run, and what a healthy run and a failed run each look like
- how to pause or remove the schedule

Confirm the Lambda ran on its own by checking CloudWatch and the database, not only by trusting the schedule. Keep the schedule modest to stay within the free limits.

#### 8. CI/CD deploy via GitHub Actions — 5 points

Add a GitHub Actions workflow (see [deploying automatically](../../tools_and_prior_coverage.md#deploying-automatically)) that packages and deploys the Lambda when changes are merged to the main branch. Use GitHub's secrets for credentials, never the repository itself, and give the deploying identity only the permissions it needs. Document how the workflow runs and how to know if it failed.

## What to turn in

By the end of Sprint 4, submit:

1. The AWS account and safety rails documentation, showing the Budgets alarm, IAM setup, and where secrets are stored.
2. The Lambda handler and packaging instructions.
3. The deployed Ingest Lambda and verification notes.
4. The EventBridge schedule and CloudWatch log notes, including evidence of a scheduled run.
5. The deployment notes and runtime configuration.
6. If completed, the enrichment Lambda, CloudWatch alarm, and GitHub Actions workflow.

**Total: 15 core story points, or 23 with the Should deliverables (33 with the Could)**

## End-of-sprint checkpoint

Before closing Sprint 4, mentors should review the team's project documents with the entire group.

1. **Revisit earlier decisions.** Confirm the cloud design still matches the pipeline built in Sprints 1–3, and note any behavior that changed in the move to Lambda.
2. **Update the diagrams.** Revise the architecture and process flow diagrams to show EventBridge, the Lambda functions, SSM, CloudWatch, the database, and the dashboard.
3. **Check the account.** Together, review the Budgets alarm, IAM permissions, running schedules, and anything else the team created in AWS. Everyone should know what exists and why.
4. **Maintain the working documents.** Update the deployment notes, README, team working agreement, and other documentation when assumptions or team practices change.
5. **Confirm shared understanding.** Every team member should be able to trace one scheduled run from the EventBridge trigger through the Lambda, into the database, and onto the dashboard.
6. **Record the updates.** Include documentation changes through the team's normal review workflow and summarize important open questions and any deferred deliverables for Sprint 5.

These are living documents, not one-time submissions. As the project changes, the documentation should change with it.
