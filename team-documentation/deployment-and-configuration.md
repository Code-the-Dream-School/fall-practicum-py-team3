# Deployment and configuration

How the pipeline is deployed to AWS Lambda, and what a teammate needs to reproduce or change it.

## AWS resources

| Resource            | Name                     | What it does                                                            |
| ------------------- | ------------------------ | ----------------------------------------------------------------------- |
| ECR repository      | fall-practicum-py-team3  | Stores the Docker image of the pipeline                                 |
| Lambda function     | city-air-tracker-etl     | Runs the pipeline from that image                                       |
| EventBridge trigger | TODO                     | Starts the Lambda (one time run for deployment)                         |
| CloudWatch alarm    | `<function-name>-errors` | Goes into ALARM if the Lambda has 1 or more errors in a 5 minute period |

Region: `us-east-2` (Ohio).

## Configuration and secrets

The Lambda needs these environment variables. Set them in the Lambda console (Configuration, Environment variables).

| Variable              | What it is           |
| --------------------- | -------------------- |
| `OPENWEATHER_API_KEY` | OpenWeather API key  |
| `SUPABASE_URL`        | Supabase project URL |
| `SUPABASE_KEY`        | Supabase key         |
| `OPENAI_API_KEY`      | OpenAI API key       |

Where they live:

- Local: in a `.env` file at the repo root. Copy `.env.example` and fill it in.
- Cloud: in the Lambda environment variables. The `.env` file is not baked into the image (it is listed in `.dockerignore`).

Safe to commit: `.env.example` (placeholders only).
Never commit: `.env`, AWS access keys, or any real key or URL value.

## Local vs Cloud runs

|                    | Local                                                                      | Cloud                                                         |
| ------------------ | -------------------------------------------------------------------------- | ------------------------------------------------------------- |
| How it runs        | `docker run -p 9000:8080 city-air-tracker:test` (built in Lambda emulator) | AWS Lambda runs the image from ECR                            |
| How it starts      | `curl` a test event to `localhost:9000`                                    | EventBridge trigger, or the Test button in the Lambda console |
| Settings come from | `.env` file                                                                | Lambda environment variables                                  |
| Logs               | Terminal                                                                   | CloudWatch Logs                                               |

See `docker_ecr_push.md` for the build, local test, and push steps.

## How to deploy

1. Build the image from the repo root: `docker build -t city-air-tracker:test .`
2. Push it to ECR (steps in `docker_ecr_push.md`).
3. Create or update the Lambda function from the ECR image.
4. Set the environment variables above.
5. Add the trigger.
6. Create the alarm: run `cloudwatch.py` with the Lambda's real function name.

## Handler

The Dockerfile `CMD` tells Lambda which function to run, in the form `package.file.function`.
Handler: `pipeline.aws.lambda_handler.lambda_handler`
