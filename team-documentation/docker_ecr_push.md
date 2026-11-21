# Build and push the Docker image to ECR

This builds the pipeline as an AWS Lambda container image and pushes it to our ECR repo.

## One-time setup

1. Install and start Docker Desktop.
2. Install the AWS CLI (check with `aws --version`).
3. Create an access key (IAM, your user, Security credentials) and run `aws configure`. Use region `us-east-2` and output `json`. Never commit or share your keys.

## Build

From the repo root:

```
docker build -t city-air-tracker:test .
```

## Test locally first

The base image has a built in Lambda emulator, so you can test before pushing. Docker Desktop must be running. If you changed any code or the handler name, rerun the build step first.

1. Start the container. Leave this terminal open, it keeps running:

```
docker run -p 9000:8080 city-air-tracker:test
```

2. In a second terminal, send it a test event:

```
curl.exe -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" -d "{}"
```

You should get back something like:

```
{"statusCode": 200, "body": "{\"message\": \"Hello from Lambda!\", \"received\": {}}"}
```

3. Stop the container with Ctrl+C in the first terminal. If you get a "port already in use" error next time, an old container is still running. Stop it in Docker Desktop.
