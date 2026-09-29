# Sprint 0: Course and Team Preparation

Welcome to **Sprint 0**! 👋

This is your chance to meet your team, understand the City Air Tracker project, and refresh the skills you will use during the practicum. There are **no deliverables and no story points** for Sprint 0, but completing the preparation below will make Sprint 1 much easier.

> **Note:** Nothing needs to be turned in for Sprint 0. The goal is to arrive at Sprint 1 with your team, tools, repository, and expectations in place.

## The project you will build

City Air Tracker is a team-built batch data pipeline and web application. At a high level, your team will:

1. Read a list of global cities and geocode them into latitude and longitude.
2. Collect historical air pollution data from OpenWeather.
3. Transform raw API responses into a clean dataset.
4. Store application and pipeline data in PostgreSQL.
5. Serve the prepared data through a Python API to a React dashboard.

The project brings together ideas you have already practiced in Python 100, Python 200, and React. The goal is not only to build a working application, but also to practice planning work, reviewing code, discussing blockers, and connecting each person's work into one shared system.

## Suggested course review

Spend time reviewing the topics where you feel least confident:

- **[Python 100](https://classes.codethedream.org/course/python-100-v2/python-essentials-26.2):** functions, modules, classes, exceptions, virtual environments, Git, APIs, JSON, and CSV files
- **[Python 200](https://classes.codethedream.org/course/python-200-v1/python-ai-and-cloud-computing-26.2):** data cleaning and transformation, pandas, SQL, PostgreSQL, testing, and data analysis
- **React:** components, props, state, hooks, API requests, and loading, empty, and error states

You do not need to relearn every topic before Sprint 1. Identify your strongest areas, note where you need practice, and share both with your team.

## Project management

Agile is an approach to delivering work in small, adaptable increments; Scrum and Kanban are common ways to organize that work, while JIRA is the tool your team will use to plan and track it. Scrum emphasizes time-boxed sprints and regular team check-ins, while Kanban makes the flow and status of work visible on a board.

- [Jira Tutorial for Beginners | Atlassian Answered](https://www.youtube.com/watch?v=emidrJeUTaM&t=261s)
- [Agile vs Scrum vs Kanban](https://www.youtube.com/watch?v=9LCH8KuXXC8&t=168s)

## JIRA and story points

Your mentor will set up the team's JIRA project. At the start of each sprint, your group will turn the sprint milestone into smaller, clearly defined tasks and track them on the board.

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

Each team will include **4–5 students** and **1–2 mentors**. There are no assigned technical roles because the practicum is designed to give every student hands-on experience with every part of the project.

During Sprint 0, your group should:

- choose a student team lead to help coordinate communication, meetings, and progress
- consider choosing a scribe to capture meeting notes, decisions, blockers, and action items
- decide where the team will communicate between meetings
- schedule a weekly stand-up, or a second short check-in when useful

The Code the Dream week begins on **Wednesday** with the instructor session, so try to hold your main stand-up on Thursday or shortly afterward. Keep it brief: share what you completed, what you will work on next, and what is blocking you.

The team lead is a coordinator, not the only decision-maker or the owner of the most important work. Everyone should participate in planning, implementation, testing, review, and documentation throughout the practicum.

## Your mentors

Mentors will be intentionally hands-off at first so the team has room to make decisions and learn by doing. They will step in when students ask for help or when they foresee a problem, blocker, or delay that could put the project at risk.

Bring mentors clear questions, explain what the team has already tried, and involve them early when a blocker is affecting progress.

## Set up the team repository

One student should create the team's blank GitHub repository and connect the Code the Dream `city-air-tracker-student` repository as `upstream`. After the initial setup, every student should clone the new team repository and confirm that they can access it.

Follow the [Team repository setup instructions](../../README.md#team-repository-setup-sprint-0) in the project README.

## Sprint 0 preparation checklist

Before Sprint 1 begins, try to:

- review the project overview in this document and the project README
- refresh the course topics that need the most practice
- watch the short project management videos
- meet your teammates and mentors
- choose a team lead and, if useful, a scribe
- agree on a regular stand-up time beginning Wednesday
- confirm access to the team's JIRA project
- create and clone the team repository
- confirm that every team member can communicate with the group and raise blockers
