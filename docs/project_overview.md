# Project Overview

Read this guide before Sprint 1 begins, and come back to it whenever you need a reminder of how the practicum works. It explains what your team will build, how the ten weeks are organized, what to review ahead of time, and how your team and mentors will work together.

## The project you will build

In this practicum, your team of four builds a batch data pipeline and takes it from your laptop to the cloud. The driving question for the whole project is:

> **How do you take a data pipeline off your laptop and make it run on its own in the cloud, reliably and for free?**

Your team will choose one dataset to work with. Each option follows the same overall pattern:

| Dataset | Source | What it offers |
|---|---|---|
| Air Quality | OpenWeather | Pollutant concentrations and air quality index values for cities around the world |
| Earthquakes | USGS | Recent seismic events with magnitude, depth, and location |
| Bike Share | GBFS | Station locations and live bike and dock availability |

The practicum has two phases:

1. **Local phase (Sprints 1–3, Weeks 1–6).** Build the pipeline on your own machines. Your pipeline will extract data from a public API, load it into a PostgreSQL database, transform it, enrich it with an LLM, run from a single orchestrated entry point, and show the results on a small dashboard. We recommend **Supabase** (hosted PostgreSQL), **Prefect** (orchestration), and **Streamlit** (dashboard), which you practiced in Python 100 and Python 200.
2. **Cloud phase (Sprints 4–5, Weeks 7–10).** Deploy the pipeline to **AWS Lambda**, triggered on a schedule by **EventBridge** and observed through **CloudWatch**. The pipeline you build in Sprints 1–3 is designed from the start to be called from anywhere, so moving to the cloud means giving it a new caller, not rewriting it. By the end, the pipeline runs on its own with no laptop involved.

### Required tools and recommended tools

Some tools in this practicum are **required**, because there is no alternative. The AWS services in Sprints 4–5 fall in this group, and so does PostgreSQL as the database. Other tools are **recommended**, because you used them in Python 100 or Python 200 but the project works just as well if your team chooses another way of meeting the same deliverable. Supabase, Prefect, and Streamlit are recommended tools.

See [Tools and Prior Coverage](tools_and_prior_coverage.md) for each concept, the recommended and alternative tools, the sprint that introduces it, and the lessons where you may have seen it before.

## Sprint structure

Each sprint lasts **two weeks** and opens with a mini-lesson from your instructor that introduces new content. Sprint 4 opens with two mini-lessons, one each week.

| Sprint | Weeks | Focus |
|---|---|---|
| [1](milestones/10_week/sprint1.md) | 1–2 | Team setup, data contracts, and the extract layer |
| [2](milestones/10_week/sprint2.md) | 3–4 | PostgreSQL storage, idempotent loading, and the raw-to-gold transform |
| [3](milestones/10_week/sprint3.md) | 5–6 | LLM enrichment, an orchestrated flow, and a minimal dashboard |
| [4](milestones/10_week/sprint4.md) | 7–8 | AWS account safety, a deployed Lambda, and a schedule |
| [5](milestones/10_week/sprint5.md) | 9–10 | End-to-end run on AWS, cost teardown, and the final demo |

## What to review before Sprint 1

The project brings together ideas you have already practiced in Python 100 and Python 200. You do not need to relearn every topic. Identify your strongest areas, note where you need practice, and share both with your team.

- **[Python 100](https://classes.codethedream.org/course/python-100-v2/python-essentials-26.2):** Git and pull requests, calling APIs with `requests`, pandas cleaning and transformation, SQL and SQLAlchemy, and dashboards with Streamlit and Plotly
- **[Python 200](https://classes.codethedream.org/course/python-200-v1/python-ai-and-cloud-computing-26.2):** pytest, Pydantic, working with LLM APIs, machine learning, Supabase, idempotent loading, and Prefect flows

The [Tools and Prior Coverage](tools_and_prior_coverage.md) guide lists the exact lessons for each topic, so you can jump straight to the ones you want to refresh.

### Read this Python 200 lesson: A Preview of the Practicum's AWS Stack

Python 200 does not teach AWS hands-on, and you will not need any AWS experience to begin. However, Python 200 does include a short orientation to the AWS services you will use in Sprints 4–5. It is not part of the graded curriculum, so it is easy to skim past. Please read it before Sprint 1:

- **Python 200 (branch `v3`):** `lessons/08_cloud_intro/02_cloud_landscape.md`, the section titled **"A Preview of the Practicum's AWS Stack"**

It explains, in plain language, what **Lambda**, **EventBridge**, **IAM**, **CloudWatch**, and **Parameter Store** each do. You will not set anything up from this lesson, but knowing the names and purposes now will make the Sprint 4 mini-lessons feel familiar instead of brand new.

## Project management

Agile is an approach to delivering work in small, adaptable increments; Scrum and Kanban are common ways to organize that work, while JIRA is the tool your team will use to plan and track it. Scrum emphasizes time-boxed sprints and regular team check-ins, while Kanban makes the flow and status of work visible on a board.

- [Jira Tutorial for Beginners | Atlassian Answered](https://www.youtube.com/watch?v=emidrJeUTaM&t=261s)
- [Agile vs Scrum vs Kanban](https://www.youtube.com/watch?v=9LCH8KuXXC8&t=168s)

### JIRA and story points

Your mentor will set up the team's JIRA project. At the start of each sprint, your group will turn the sprint milestone into smaller, clearly defined tasks and track them on the board.

Every sprint lists deliverables in three tiers:

- **Must:** the core deliverables every team completes. Story points for the sprint are totaled from these.
- **Should:** important work that most teams should complete if capacity allows. Anything deferred moves to the next sprint's backlog.
- **Could:** optional stretch work for teams that finish early. Do not start these until the Must items are done and reviewed.

Story points are relative estimates of a task's effort, complexity, and uncertainty. They are planning tools—not hours, grades, or measures of an individual's performance.

| Points | General meaning |
|---|---|
| 1 | Tiny change or documentation cleanup |
| 2 | Small, low-risk task |
| 3 | Focused task with clear boundaries |
| 5 | Moderate task touching more than one concern |
| 8+ | Large or uncertain work that should usually be split |

Aim for tasks worth no more than **2–3 story points**. If a milestone is larger, break it into multiple bite-sized tasks that can be completed, reviewed, and moved across the board independently.

## Team management

Each team will include **4 students** and **1–2 mentors**. There are no assigned technical roles because the practicum is designed to give every student hands-on experience with every part of the project. In your first days, your group should:

- choose a student team lead to help coordinate communication, meetings, and progress
- consider choosing a scribe to capture meeting notes, decisions, blockers, and action items
- decide where the team will communicate between meetings
- schedule a weekly stand-up, or a second short check-in when useful

The Code the Dream week begins on **Wednesday** with the instructor session, so try to hold your main stand-up on Thursday or shortly afterward. Keep it brief: share what you completed, what you will work on next, and what is blocking you. With two-week sprints, use the middle of each sprint as a checkpoint: are you on track to finish the Must items?

The team lead is a coordinator, not the only decision-maker or the owner of the most important work. Everyone should participate in planning, implementation, testing, review, and documentation throughout the practicum.

## Your mentors

Mentors will be intentionally hands-off at first so the team has room to make decisions and learn by doing. They will step in when students ask for help or when they foresee a problem, blocker, or delay that could put the project at risk.

Bring mentors clear questions, explain what the team has already tried, and involve them early when a blocker is affecting progress.

## Set up the team repository

One student should create the team's blank GitHub repository and connect the Code the Dream `city-air-tracker-student` repository as `upstream`. After the initial setup, every student should clone the new team repository and confirm that they can access it.

Follow the [Team repository setup instructions](../README.md#team-repository-setup-sprint-0) in the project README.

## Before Sprint 1 checklist

Before Sprint 1 begins, try to:

- read this overview
- read the AWS preview section of the Python 200 cloud landscape lesson
- refresh the course topics that need the most practice
- watch the short project management videos
- meet your teammates and mentors
- choose a team lead and, if useful, a scribe
- agree on a regular stand-up time beginning Wednesday
- confirm access to the team's JIRA project
- create and clone the team repository
- confirm that every team member can communicate with the group and raise blockers
- start thinking about which dataset your team would like to work with
