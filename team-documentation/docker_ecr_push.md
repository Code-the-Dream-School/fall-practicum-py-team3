# Build and push the Docker image to ECR

This builds the pipeline as an AWS Lambda container image and pushes it to our ECR repo.

## One-time setup

1. Install and start Docker Desktop.
2. Install the AWS CLI (check with `aws --version`).
4. Create an access key (IAM, your user, Security credentials) and run `aws configure`. Use region `us-east-2` and output `json`. Never commit or share your keys.

## Build

From the repo root:

```
docker build -t city-air-tracker:test .
```

## Log in, tag, and push

(coming after the first successful push)

## Check it worked

(coming after the first successful push)
