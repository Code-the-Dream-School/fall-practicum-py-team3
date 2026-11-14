# Sprint 4 Reference: AWS, Lambda, and EventBridge

## The big idea

AWS product names sound grand, but the concepts are plain. They are the things on your laptop, running elsewhere. "The cloud" is a server in an AWS data center.

Google Cloud and Microsoft Azure sell equivalent products under other names. Learn the concept once and it carries across all three.

| Concept | AWS | Google Cloud | Azure |
|---|---|---|---|
| Serverless function | Lambda | Cloud Functions | Azure Functions |
| Secrets storage | SSM Parameter Store | Secret Manager | Key Vault |
| Scheduling / event routing | EventBridge | Cloud Scheduler / Eventarc | Event Grid / Logic Apps |
| Logs | CloudWatch Logs | Cloud Logging | Azure Monitor |

## Who does what

| Your instructor and mentors set up | You operate |
|---|---|
| The AWS account, budgets, and permissions | Lambda: test it, read logs, check settings |
| Secrets (API keys, database passwords) | EventBridge: create and manage schedules and rules |
| Code packaging with Docker | Your Python function code |

The rest of this document explains the setup, so you will know why things work as they do.

---

## Part 1: How your environment is set up

### Accounts

Every cloud uses the same model:

- **Root account:** the all-powerful account. It sets up billing and services and creates other accounts. After that, it is almost never used.
- **Admin accounts:** held by mentors. They control the permitted services and the budget.
- **User accounts:** held by you. They can run the services you have been given.
- **Roles (machine identities):** used by services to talk to each other. No human logs in with them.

### Least privilege

Each account receives only the permissions it needs. If an account is compromised, the damage stays small. For this reason you lack root access, and your Lambda can reach only the things it needs.

**What this means for you:** "Access Denied" is usually not a bug. It tells you to stay within your permissions. Tell a mentor which action failed, and they can adjust the permissions if appropriate.

### IAM

IAM (Identity and Access Management) decides who can do what. A **policy** lists the allowed actions on resources. Policies attach to accounts or roles, never directly to a person. A resource is anything that needs access control: data storage, server access, S3 access, and so on.

### Budgets

Budgets keep a mistake from becoming a surprise bill. Mentors set alerts. An alert notifies people but does not necessarily stop spending, so you must still avoid runaway usage (see "Staying cost-safe" below).

### SSM Parameter Store (secrets)

SSM stands for Systems Manager. Parameter Store is a secure dictionary. Values such as API keys and database credentials are stored there once, and your function reads them as it runs.

**What this means for you:** never paste a secret into your code, a test event, or Git. Your code asks Parameter Store for the secret at runtime. Your instructor creates the parameter and grants permission to read it.

### Serverless

A serverless function does not run on a computer all day. It runs only when needed:

1. Something triggers the function.
2. AWS starts an environment and runs your code.
3. The function finishes, and the environment shuts down.

You pay only for the time your code runs, which makes serverless cheap. "Serverless" does not mean no servers. It means you do not manage them.

---

## Part 2: Lambda

Lambda is AWS's serverless function product. You write a function, and Lambda runs it when triggered.

### Your function

Lambda calls a **handler**, a function that takes two inputs:

```python
def handler(event, context):
    # your logic here
    return {"status": "ok"}
```

- `event` is the JSON input that triggered the function.
- `context` describes the running function. You will rarely need it.

### How your code reaches Lambda

Lambda needs your code and the libraries it uses (pandas, requests, and so on). Docker packages them together. **Your instructor handles this step.** You need only the vocabulary:

- **Dockerfile:** a recipe describing the environment your code needs.
- **Image:** the finished, frozen package built from that recipe.
- **ECR:** the storage shelf where images are kept for Lambda to fetch.

The flow:

`Your Python code + requirements.txt -> Dockerfile -> Docker image -> ECR -> Lambda runs it`

**Important:** Lambda does not see a code change until someone builds a new image and updates the Lambda to use it. When a change "isn't showing up," this is usually the reason. Ask your instructor for your team's process.

### What you will do in Lambda

1. **Test it.** In the console, create a **test event** (a small JSON message) and click Test.
2. **Read the logs.** Everything your code prints, and every error, appears in **CloudWatch Logs**. Open the Monitor tab, then "View CloudWatch logs." When something fails, read the logs first. Sprint 5 covers CloudWatch in detail.
3. **Check the settings:** timeout, memory, and role. Ask before raising any of them, because they affect cost.

### Ways to trigger a Lambda

- **Manually** (the Test button)
- **Programmatically** (another service calls it)
- **On a schedule or event** (through EventBridge)

### Common problems

| What you see | Likely cause |
|---|---|
| Task timed out after 3 seconds | The default timeout is short. Ask a mentor about raising it modestly. |
| Access Denied | The role or your user lacks the permission. Report exactly which action failed. |
| Handler or entrypoint not found | The handler name does not match your file and function name. |
| Works on your laptop, fails in Lambda | The environment differs from your laptop's. Check the logs. |
| You changed code but nothing changed | No one has built and deployed a new image. |

---

## Part 3: EventBridge

EventBridge is a **routing service**. An **event** is a message that something happened. EventBridge receives events and sends them to **targets**, such as a Lambda. A schedule is one kind of event ("it's 1 AM").

### Key terms

- **Event:** a JSON message about something that happened, or a time that arrived.
- **Event bus:** where events arrive.
- **Rule:** matches events and sends them to a target.
- **Target:** what the rule triggers (our Lambda).

### Running a Lambda on a schedule

Choose a schedule and set the Lambda as the target. "Every day at 1 AM" looks like this:

- **Cron:** `cron(0 1 * * ? *)`, with the fields minute, hour, day-of-month, month, day-of-week, year.
- **Rate:** `rate(1 day)`, for fixed intervals.

Keep these points in mind:

- **The console offers two places to schedule.** *EventBridge Scheduler* is newer, supports time zones, and is usually the better choice. *Scheduled rules* are older and run in UTC only. You will see both. Use the one your instructor names.
- **AWS cron is not Linux cron.** It has six fields, and either day-of-month or day-of-week must be `?`.
- **Check the time zone.** 1 AM in UTC is not 1 AM where you are.
- **Check permissions.** EventBridge needs permission to invoke the Lambda. If the schedule exists but the Lambda never runs, tell a mentor. Missing permission is a common cause.
- **Timing is not exact to the second, and a run may occasionally repeat.** This is why the idempotent writes of Sprint 2 matter. If your function runs twice for the same time window, the second run should change nothing. Write every function so that a double run does no harm.

### Event example: the dashboard "Refresh" button

1. A user clicks **Refresh dashboard**.
2. The page calls a backend, such as an API in front of a Lambda. The browser never holds AWS credentials.
3. The backend sends an event to EventBridge, such as `{"source": "dashboard", "detail-type": "RefreshRequested"}`.
4. A rule matching that event routes it to the refresh Lambda.
5. The Lambda refreshes the data.

The same Lambda can also run nightly on a schedule. One function can have several triggers.

---

## Putting it together with your pipeline

Your Sprint 3 loading function can serve as the body of a Lambda. An hourly EventBridge schedule triggers it for incremental loading. For a backfill, invoke it manually with a wider time range in the test event. Because your writes are idempotent, an accidental double run is harmless.

---

## Staying cost-safe

- Keep schedules sensible. Running every minute is rarely necessary.
- **Disable or delete schedules** you no longer need.
- **Never let a Lambda trigger itself,** directly or through EventBridge. This is the classic runaway-bill loop.
- Ask before raising timeout or memory.
- If anything runs far more often than expected, tell a mentor at once.

---

## Quick glossary

| Term | Plain meaning |
|---|---|
| Root account | The all-powerful account, set up once and left alone |
| IAM | Who can do what |
| Policy | A document listing allowed actions |
| Role | An identity that services, not people, use to get permissions |
| Least privilege | Only the permissions needed |
| SSM Parameter Store | A secure place for secrets |
| Serverless | Compute that runs only when triggered |
| Lambda | AWS's serverless function product |
| Handler | The function Lambda calls first |
| Dockerfile / Image / ECR | Recipe / finished package / storage shelf |
| EventBridge | Routes events, including scheduled ones, to targets |
| CloudWatch Logs | Where your function's output and errors appear |
