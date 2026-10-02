## Team repository setup

1. Set up SSH keys first. You can follow [Github's instructions](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).
Let your mentor know if you run into issues.

2. All team members should clone this repository:

```shell
git clone git@github.com:Code-the-Dream-School/fall-practicum-py-team3.git
cd fall-practicum-py-team3
git remote add upstream git@github.com:Code-the-Dream-School/city-air-tracker-student.git
```

3. You can confirm both remotes with:

```shell
git remote -v
```

`origin` should point to the team's repository. `upstream` should point to the Code the Dream starter repository.

```shell
origin  git@github.com:Code-the-Dream-School/fall-practicum-py-team3.git (fetch)
origin  git@github.com:Code-the-Dream-School/fall-practicum-py-team3.git (push)
upstream    git@github.com:Code-the-Dream-School/city-air-tracker-student.git (fetch)
upstream    git@github.com:Code-the-Dream-School/city-air-tracker-student.git (push)
```
