# How are Github and JIRA connected in practice?

## Definitions
Epic = the big goal (e.g. "Implement User Login"). You never code an epic directly; it's a container that tracks progress across many stories.
Story = a smaller piece of work that is typically a complete feature ("I can log in"). It's the natural unit of planning.
Subtask = optional. Only split a story into subtasks when it's too big to finish in one sitting. A small story is its own unit of work.
Branch/PR = the unit of doing. Whatever JIRA item you're actually working on (story or subtask), that's what gets one branch and one PR. The ticket ID in the branch name and PR title ties it all together. It lets tools, teammates, and future-you figure out why a code change exists.


## Diagram
+-------------------------+
|EPIC (JIRA):             |
|"User Login"             |
|(PROJ-10)                |
|The big goal. Nobody     |
|codes an epic directly.  |
+-------------------------+
             |
             | broken down into
             | STORIES
             |
       +------------------------------------------------------------+
       |                                                            |
       v                                                            v
+---------------------------------------------+             +-------------------------+
|STORY 1: PROJ-101                            |             |STORY 2: PROJ-104        |
|"As a user, I can                            |             |"As a user, I can        |
|log in"                                      |             |reset my password"       |
|                                             |             |                         |
|Too big for one sitting                      |             |Small -> NO subtasks     |
|-> split into SUBTASKS                       |             |needed                   |
+---------------------------------------------+             +-------------------------+
       |                              |                             |
       |                              |                             |
       |                              |                             |
       v                              v                             v
               split into subtasks, or work directly if small enough
+-------------------------+   +-------------------------+   +-------------------------+
|SUBTASK 1: PROJ-102      |   |SUBTASK 2: PROJ-103      |   |STORY 2 is itself the    |
|"Design login form UI"   |   |"Implement login API"    |   |unit of work (PROJ-104)  |
+-------------------------+   +-------------------------+   +-------------------------+
             |                             |                             |
             v                             v                             v
                       1 unit of work  =  1 branch  =  1 PR
+-------------------------+   +-------------------------+   +-------------------------+
|BRANCH:                  |   |BRANCH:                  |   |BRANCH:                  |
|feature/login-ui         |   |feature/login-api        |   |feature/password-reset   |
|(named for PROJ-102)     |   |(named for PROJ-103)     |   |(named for PROJ-104)     |
+-------------------------+   +-------------------------+   +-------------------------+
             |                             |                             |
             v                             v                             v
+-------------------------+   +-------------------------+   +-------------------------+
|PULL REQUEST:            |   |PULL REQUEST:            |   |PULL REQUEST:            |
|"Add login form UI       |   |"Add login API           |   |"Add password reset      |
| (PROJ-102)"             |   | endpoint (PROJ-103)"    |   | (PROJ-104)"             |
+-------------------------+   +-------------------------+   +-------------------------+
             |        all PRs, once approved, merge into main            |
             |                             |                             |
             +-----------------------------+-----------------------------+
             |
             v
+-------------------------+
|MAIN BRANCH ("main")     |
|The shared codebase.     |
|Every PR lands here      |
|after review + approval. |
+-------------------------+
