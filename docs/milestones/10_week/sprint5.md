# Sprint 5: Run It, Watch It, and Wrap It Up

Welcome to **Sprint 5**, the final sprint!

**Goal: the pipeline runs end to end on AWS, and the team can show and explain it.**

This sprint is about making sure what you deployed is reliable, understanding what it costs (ideally nothing), and telling the story of the project. By the end, your data should flow from a scheduled AWS run, into the database, onto your dashboard, and into a demo.

## Sprint 5 mini-lesson

**Observability: logs, alarms, and dead-letter queues, plus optional CI/CD.** Your instructor will introduce how to tell whether a pipeline that runs without you is healthy, how to be told when it is not, and how failed events can be captured instead of lost.

By the end of Sprint 5, your team should be able to explain:

- how the team knows the pipeline is running correctly without watching it
- what happens when a run fails and how the team would find out
- what the pipeline costs to run and how the team confirmed it
- how to shut everything down and leave the account clean
- what changed between the local version and the AWS version, and what the team learned
- what the project can do today, and what it still can't

## Start with the Sprint 4 handoff

Before starting new work, review the team's:

- deployed Lambda functions, schedule, and CloudWatch logs
- deployment notes and runtime configuration
- Budgets alarm and account safety rails
- any Sprint 4 deliverables that were deferred
- unanswered questions from the Sprint 4 handoff

## Sprint 5 scope

This sprint focuses on **verifying, hardening, and presenting** the deployed pipeline. If verification reveals a real problem upstream, note it and make only the fixes needed to demo cleanly, rather than reopening earlier sprints' work. Finish deferred Sprint 4 items before starting new stretch work.

**Required and recommended tools:** the stretch items in this sprint each require a specific AWS service or tool, such as SNS or Slack for alerts, a dead-letter queue, GitHub Actions, a container Lambda, or AWS SAM, and only for teams that choose that item. None of them were taught in Python 100 or Python 200, so the mini-lesson and your mentors are your main support. See [Tools and Prior Coverage](../../tools_and_prior_coverage.md).

## Sprint 5 deliverables

### Must

#### 1. End-to-end run on AWS — 5 points

Show that the whole system works without your laptop in the loop. Confirm, and write down the steps to repeat, that:

- the EventBridge schedule triggers the Lambda
- the run appears in CloudWatch logs with a clear success or failure
- new data lands in the raw and gold tables in the database, and the `pipeline_runs` record reflects the run, if the team built it
- the dashboard displays the new data
- a second run does not create duplicate records

Include at least one non-happy-path check, such as a bad configuration value or a failed source request, and show what the team sees when it happens.

#### 2. Cost-teardown check — 3 points

Review what the project costs to run and confirm nothing is left running by accident. Document:

- every AWS resource the team created, and whether it is still needed
- the Budgets alarm status and the spending shown in the account
- what the team removed or paused once the project was complete, such as the schedule, Lambda functions, and any other resource created along the way
- how to recreate the deployment, if the team wants to run it again

Deleting resources is permanent, so confirm as a team, and with your mentor, before removing anything you may still need for the demo. Do the teardown after the demo is recorded or presented.

#### 3. Before-and-after writeup and final documentation — 5 points

Write the story of moving from a local pipeline to a cloud pipeline. Include:

- what the pipeline looked like at the end of Sprint 3 and what it looks like now
- what had to change to run on Lambda, and what stayed the same
- what surprised the team, what went wrong, and how the team fixed it
- what the pipeline costs and how it stays inside the free limits
- what the project can do today, and what is unfinished or out of scope

Update the project README or a handoff doc so someone outside the team can understand what was built and how to run it. Include the runtime settings and a short runbook for a walkthrough, from triggering a run to viewing the result.

#### 4. Final demo — 3 points

Present the working project to mentors: the dataset and the product, the data flow from source to dashboard, the move from local to AWS, how the team split the work, the hardest tradeoffs, and what the team would improve with more time. Every team member should present at least one part they personally built.

#### 5. Retrospective — 2 points

Hold a team retrospective and record the results. Discuss:

- what went well
- what did not go well
- what the team would change about how it worked together
- what each person learned, and what they want to learn next
- one thing you would tell a team starting this project

### Should

#### 6. Deferred Sprint 4 work — up to 8 points

Complete any Should deliverables that were deferred from Sprint 4, such as the enrichment Lambda or the basic CloudWatch alarm. Use the point values from Sprint 4.

#### 7. SNS or Slack failure alert — 3 points

Send a notification when a run fails (see [failure alerts](../../tools_and_prior_coverage.md#failure-alerts)), using SNS or a Slack alert. Document what triggers the alert, who receives it, and what the message tells the person receiving it. Confirm it works by causing a safe, controlled failure. Keep any webhook or topic details out of the repository.

### Could

#### 8. Dead-letter queue — 3 points

Add a [dead-letter queue](../../tools_and_prior_coverage.md#capturing-failed-events) so failed events are captured instead of lost. Document what ends up in the queue, how a teammate would inspect it, and how a failed event could be retried or discarded.

#### 9. ML classifier in a container Lambda — 5 points

If the team built the Sprint 3 ML classifier, deploy it as a Lambda packaged as a [container image](../../tools_and_prior_coverage.md#packaging-a-lambda-as-a-container), which allows larger dependencies than a standard package. Document how the image is built, how the model is loaded, and how the Lambda is triggered.

#### 10. Infrastructure as Code with AWS SAM — 5 points

Describe the team's Lambda functions, schedule, and related resources in an [AWS SAM](../../tools_and_prior_coverage.md#describing-infrastructure-as-code) template so the deployment can be recreated from a file instead of console clicks. Document how to deploy and remove it. Confirm a fresh deployment works before removing the manually created version.

## What to turn in

By the end of Sprint 5, submit:

1. The end-to-end verification notes.
2. The cost-teardown check.
3. The before-and-after writeup and final documentation.
4. The final demo.
5. The retrospective.
6. If completed, the deferred Sprint 4 work and the failure alert.
7. If completed, the dead-letter queue, container Lambda, and SAM template.

**Total: 18 core story points, plus up to 11 for the Should deliverables (up to 13 more for the Could)**

## End-of-sprint checkpoint

Before closing Sprint 5, mentors should review the team's project documents with the entire group.

1. **Revisit earlier decisions.** Confirm the finished project reflects the dataset choice from Sprint 1 and the data shapes from Sprints 1 and 2.
2. **Update the diagrams.** Revise the architecture and process flow diagrams one last time to show the full path from the AWS trigger through the dashboard.
3. **Maintain the working documents.** Update the README, runtime configuration notes, deployment notes, and any other documentation that no longer matches the finished project.
4. **Confirm the account is clean.** Together, review the AWS account and confirm the team has removed what it no longer needs and knows what remains.
5. **Confirm shared understanding.** Every team member should be able to walk through the full pipeline from schedule to dashboard and explain at least one part they personally built.
6. **Record the updates.** Include final documentation changes through the team's normal review workflow.

These are living documents. Even at the end of the practicum, they should describe the project as it actually is. Congratulations on taking a pipeline off your laptop and into the cloud!
