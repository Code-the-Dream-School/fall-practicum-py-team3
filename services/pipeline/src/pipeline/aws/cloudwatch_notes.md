# CloudWatch Alarm Documentation

## What the alarm watches

The `lambda_handler-errors` alarm monitors the AWS Lambda `Errors` metric
in `us-east-2` (Ohio). It counts failed invocations for the function named
`lambda_handler`.

## Threshold

The alarm enters the `ALARM` state when CloudWatch records one or more
failed invocations in a single five-minute period.

## Who is notified

No one receives an automatic notification because no alarm action is
configured. Team members can check the alarm’s state and history under
CloudWatch → Alarms → lambda_handler-errors.