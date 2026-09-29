# City Air Tracker Feature Branch PR Guide

## Purpose

This guide explains how work should move through feature branches and pull requests in the City Air Tracker project.

It focuses on how to:

- create a new development branch from `main`
- name branches in a consistent way
- push work to GitHub
- open and manage a pull request (PR)

Use this workflow for any feature, bug fix, or documentation update.

## Branching Model

In this repository, new work should start from the `main` branch.

Create a separate branch for each task. Do not commit new work directly to `main`.

Based on the branches already in this repo, the current naming pattern is:

```text
feature/AIR-###-short-description
```

Examples from this project:

- `feature/AIR-006-llm-7day-air-quality-forecasting`
- `feature/AIR-009-store-gold-parquet-dataset-in-azure-cloud-storage`
- `feature/AIR-009.4-docker-compose-azure`
- `feature/AIR-002.2-pr-review-and-data-pipeline-docs`

## Branch Naming Rules

Follow these rules when creating a branch:

1. Start with `feature/` for feature work.
2. Include the ticket or issue id, such as `AIR-010`.
3. Add a short lowercase description separated by hyphens.
4. Do not use spaces.
5. Keep the name specific enough that reviewers can understand the goal.

Recommended format:

```text
feature/AIR-010-add-dashboard-filter
```

## Create a New Development Branch

From the project root, run:

```bash
git switch main
git pull origin main
git switch -c feature/AIR-010-add-dashboard-filter
```

This does three things:

1. switches to `main`
2. updates your local `main` with the latest code from GitHub
3. creates and checks out your new branch

You can confirm your branch with:

```bash
git branch --show-current
```

## Work on Your Feature Branch

Make your code changes in your new branch. Commit small, meaningful updates instead of one very large commit.

A typical workflow looks like this:

```bash
git status
git add path/to/file1 path/to/file2
git commit -m "AIR-010 Add dashboard filter for city comparison"
```

Tips:

- Commit messages should explain what changed.
- Include the ticket id in the commit message when possible.
- Test your work before pushing.
- Keep your branch focused on one task or ticket.

## Push the Branch to GitHub

The first time you push a new branch, use:

```bash
git push -u origin feature/AIR-010-add-dashboard-filter
```

After that, you can usually push with:

```bash
git push
```

The `-u` option connects your local branch to the remote branch on GitHub so future pushes are simpler.

## Open a Pull Request on GitHub

After pushing your branch:

1. Go to the repository on GitHub.
2. GitHub will often show a `Compare & pull request` button for your recently pushed branch.
3. If it does not, open the `Pull requests` tab and choose `New pull request`.
4. Set the base branch to `main`.
5. Set the compare branch to your feature branch.

Before creating the PR, review the diff to make sure only your intended changes are included.

## What to Write in a Pull Request

A good PR should help reviewers understand the change quickly.

Include:

- a clear title
- a short summary of what changed
- why the change was needed
- testing notes
- screenshots if the change affects the dashboard UI

Example PR title:

```text
AIR-010 Add dashboard filter for city comparison
```

Example PR description:

```text
## Summary
- adds a city filter to the comparison page
- updates the data query to respect the selected city

## Testing
- ran the pipeline locally
- launched the dashboard locally
- verified the filter updates the displayed charts

## Issue
Closes #123
```

If your work is tied to a GitHub issue, reference the issue number in the PR body.
GitHub links PRs reliably through issue references such as:

- `Closes #32`
- `Related to #44`

## How to Review and Respond to Feedback

After you open a PR:

1. Reviewers may leave comments or request changes.
2. Make the requested updates on the same feature branch.
3. Commit and push again.
4. The PR updates automatically.

You do not need to open a new PR for review feedback if the work is part of the same change.

When feedback is addressed:

- reply to comments when useful
- mark conversations as resolved if your team uses that workflow
- re-request review if needed

## Keep Your Branch Up to Date

If `main` changes while your PR is still open, update your branch so merge conflicts are less likely.

One simple approach is:

```bash
git switch main
git pull origin main
git switch feature/AIR-010-add-dashboard-filter
git merge main
```

If Git reports conflicts:

1. open the conflicting files
2. choose the correct final code
3. save the files
4. stage the resolved files
5. commit the merge

Then push again:

```bash
git push
```

## Merge and Clean Up

When the PR is approved and checks pass:

1. merge the PR in GitHub using the method your team prefers
2. delete the branch on GitHub if it is no longer needed
3. clean up your local branch

Local cleanup:

```bash
git switch main
git pull origin main
git branch -d feature/AIR-010-add-dashboard-filter
```

## Common Mistakes to Avoid

- committing directly to `main`
- creating one branch for multiple unrelated tasks
- using vague branch names such as `feature/my-work`
- opening a PR with unrelated file changes
- waiting too long to sync with `main`
- ignoring review comments

## Quick Reference

Create a branch:

```bash
git switch main
git pull origin main
git switch -c feature/AIR-010-add-dashboard-filter
```

Commit work:

```bash
git add .
git commit -m "Add dashboard filter for city comparison"
```

Push to GitHub:

```bash
git push -u origin feature/AIR-010-add-dashboard-filter
```

Update branch with latest `main`:

```bash
git switch main
git pull origin main
git switch feature/AIR-010-add-dashboard-filter
git merge main
```

## Final Reminder

The safest team workflow for this repository is:

1. start from `main`
2. create one feature branch per task
3. use the `feature/AIR-###-short-description` pattern
4. push your branch to GitHub
5. open a PR into `main`
6. respond to review feedback in the same branch
7. merge only after review
