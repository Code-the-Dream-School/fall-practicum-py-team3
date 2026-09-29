# City Air Tracker

This repo contains a Code the Dream-friendly batch ETL project that:

1. Geocodes global cities to lat/lon
2. Pulls OpenWeather Air Pollution historical data
3. Transforms PostgreSQL-backed raw response records into a gold dataset
4. Writes the gold dataset to PostgreSQL
5. Serves a React dashboard backed by a Python API over PostgreSQL data

The pipeline uses DB-first gold persistence by default, with PostgreSQL as the primary gold-data target
City configuration, geocoding cache, and raw extract persistence are in PostgreSQL as runtime state.
The same PostgreSQL runtime path can target either local Docker/Postgres or managed Azure Database for PostgreSQL through environment configuration.

## Team repository setup (Sprint 0)

One student should complete the initial setup below. These instructions follow the repository setup used in the Code the Dream Python 100 homework repository.

1. Sign into your GitHub, and create a repository for your team's City Air Tracker project. It must be a public repository. Do not create a `.gitignore` or a `README.md`.
2. On your computer, clone the [`city-air-tracker-student`](https://github.com/Code-the-Dream-School/city-air-tracker-student) repository. (Do not clone the repository you just created.)
3. Change to the `city-air-tracker-student` directory you just cloned. Enter the following commands, replacing `team-repository-owner` and `team-repository-name` with the values for the repository your team created:

```shell
# if you use SSH authentication:
git remote set-url origin git@github.com:team-repository-owner/team-repository-name.git

# if you use token-based authentication:
git remote set-url origin https://github.com/team-repository-owner/team-repository-name

git remote add upstream https://github.com/Code-the-Dream-School/city-air-tracker-student
git push origin main
```

4. In the team's new GitHub repository, add every student and mentor on the team as a collaborator.
5. All other team members should clone the new team repository:

```shell
git clone https://github.com/team-repository-owner/team-repository-name.git
cd team-repository-name
git remote add upstream https://github.com/Code-the-Dream-School/city-air-tracker-student
```

Each team member can confirm both remotes with:

```shell
git remote -v
```

`origin` should point to the team's repository. `upstream` should point to the Code the Dream starter repository.

## Additional docs

Browse [Docs table of Contents](./docs/docs_toc.md) for the full categorized index.
