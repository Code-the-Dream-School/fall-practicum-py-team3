import boto3
from hello_world import lambda_handler as handler


def cloud_alarm(function_name, region):
    cloudwatch = boto3.client("cloudwatch", region_name=region)
    cloudwatch.put_metric_alarm(
        AlarmName=f"{function_name}-errors",
        Namespace="AWS/Lambda",
        MetricName="Errors",
        Dimensions=[{"Name": "FunctionName", "Value": function_name}],
        Statistic="Sum",  # Adds up all the errors during each period
        Period=300,  # Sets the length of each period in seconds 300 seconds = 5 minutes
        EvaluationPeriods=1,  # Tells CloudWatch that one 5 minute period is enough to trigger the alarm.
        Threshold=1,
        ComparisonOperator="GreaterThanOrEqualToThreshold",
    )


cloud_alarm(handler.__name__, "us-east-2")
print(f"CloudWatch accepted the alarm: {handler.__name__}-errors")
