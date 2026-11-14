# Sprint 1 Reference: Pull Requests and Contracts First

Two practices run through this bootcamp and through nearly every professional engineering team:

1. Pull requests keep a shared codebase healthy.
2. Teams define the shape of their data and the signatures of their functions before they write the code.

The glossary at the end defines unfamiliar terms.

---

## Part 1: Pull Requests

A **codebase** is all the code for a project, kept in a shared place called a **repository**. On a team, many people work on different tasks in the same codebase at once. Their changes must be combined, or **merged**, into the main code in an orderly way. The **pull request (PR)** is the means.

A PR says: "I have made some changes. Please review them, and if they are good, add them to the main code."

### How a PR works

1. **Pick up a task.** Teams track work in tickets, such as "Add a column for signup date."
2. **Create a branch.** A branch is your own copy of the code. Changes made there affect no one else.
3. **Make your changes** and save them as commits.
4. **Open a pull request,** asking the team to review your branch and merge it into the main code.
5. **Get a review.** A teammate reads your changes, asks questions, and either approves them or requests fixes.
6. **Merge.** Once approved, your changes join the main code.

### Two ideas behind a PR

**Visibility.** A PR shows exactly what you changed, set against the existing code. Tests usually run automatically, so everyone can see whether the new code works and whether it broke anything that worked before.

**Review.** A PR is more than a request to merge; a teammate must approve it. The reviewer:

- reads the PR and asks questions;
- verifies that the change matches the ticket;
- learns what new code is entering the codebase.

Review keeps the whole team informed, even those not directly involved.

### Why PRs matter more as codebases grow

Everyone knows some parts of the code better than others, usually from having worked there. Review lets you draw on expertise you lack.

On a small project like those in this bootcamp, one person can hold the whole codebase in mind, and PRs may seem unnecessary. At a company, the code exceeds what any one person can understand. PRs keep the team informed.

### Tips for good PRs

- **Keep them small.** A PR that changes one thing is far easier to review than one that changes ten.
- **Write a clear title and description.** State what changed and why, and link the ticket.
- **Review your own PR first.** Read your changes before asking someone else to.
- **Treat review as conversation.** Comments concern the code, not the author. Everyone's PRs receive comments, senior engineers' included.

---

## Part 2: Contracts Before Code

Engineering teams, not data teams alone, agree on the shape of their data, their APIs, and their function signatures before writing the code behind them. Each term means something specific:

- **Shape of data:** the fields or columns the data has, and the type of each. A `users` table, for example, might have an `id` number and a `name` text field.
- **API:** a defined way for one program or team to request data or actions from another.
- **Function signature:** a function's name, its inputs, and its output.

An agreement on any of these is a **contract**.

### An analogy

Consider a restaurant menu. It tells customers what they may order and tells the kitchen what it must be able to make. The kitchen chooses *how* to cook each dish, but the menu comes first. A kitchen that changed the menu after customers had planned their meals would cause confusion.

### The core idea

Once built, an API that other teams depend on is hard to change. So the teams agree beforehand on its shape and structure. The agreement brings two benefits:

1. **No rework.** Both sides build knowing the shape is settled. Neither must change it later to satisfy the other.
2. **Parallel work.** Once the contract is agreed, both teams begin at once. Neither waits for the other to finish.

### Contracts make you think about the system

Writing the contract first makes you consider what you need, free of implementation detail. Ask:

- What do I need to build the workflows I want?
- Will what the other team provides suit the way I need to use it?
- Should I ask for something different?

A contract also opens early communication. It says: "This is how I intend to build." When both sides agree, they build.

### Example: the missing email column

Suppose one team builds a `users` table without an `email` column. Another team's notification service needs email addresses. If the teams never discuss what one can provide and the other needs, the gap appears late, after the table is built and the consumer is blocked.

The teams might instead agree first on this contract:

```sql
CREATE TABLE users (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL,   -- the notification service needs this
    created_at TIMESTAMP        -- nullable on purpose: older rows have no recorded signup time
);
```

Agreeing on the schema up front exposes the gap while it is cheap to fix. Adding a column to a plan takes seconds. Adding one to a built table that other systems use takes much longer.

### The same idea at every level

A contract may be:

- an HTTP API or endpoint;
- a database or table schema (the focus of this course);
- a data pipeline contract;
- a function signature.

The difference is scope. APIs and database schemas often span several teams. Function signatures usually stay within one team. Agreeing on a signature lets two people write related functions independently: you know how to call a function someone else is writing, and what it will return.

### Example: a function signature

Suppose you and a teammate split a task. They will write a function that calculates an order total; you will write the code that uses it. You first agree on this signature:

```python
def calculate_total(prices: list[float], tax_rate: float) -> float:
    """Return the sum of prices with tax applied."""
    ...
```

You now know the function's name, what to pass (a list of prices and a tax rate), and what comes back (a number). You can write and test your code today, though your teammate has not finished theirs.

### Where this appears in the bootcamp

In a data pipeline, table schemas *are* contracts. The raw table promises what the source sent. The gold table promises what the app can rely on. Defining these schemas before writing the loading code is the practice described above. You will use it from Sprint 2 on.

---

## Key Takeaways

- **PRs provide visibility and review.** Together they keep changes understood and the codebase shared.
- **Agree on contracts before writing code.** Settled schemas, APIs, and function signatures prevent rework and let people work in parallel.
- **Both practices matter more at scale.** They may feel like overhead on a small project. They become essential once the code exceeds what one person can hold in mind.

---

## Glossary

- **API:** A defined way for programs or teams to request data or actions from each other.
- **Branch:** A separate copy of the code, where changes leave the main code untouched.
- **Codebase:** All the code for a project.
- **Commit:** A saved snapshot of your changes.
- **Consumer:** A person, team, or program that uses data or a service another provides.
- **Contract:** An agreement on the shape of data, an API, or a function, made before it is built.
- **Endpoint:** A specific address in an API that receives requests.
- **Function signature:** A function's name, inputs, and output.
- **Merge:** To combine one set of changes with another, such as a branch with the main code.
- **Pull request (PR):** A request to review your changes and merge them into the main code.
- **Repository:** The shared place where a project's code is stored.
- **Schema:** The structure of a database table: its columns and the type of data each holds.
- **Ticket:** A written description of a task for the team to complete.
