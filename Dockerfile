# syntax=docker/dockerfile:1
FROM public.ecr.aws/lambda/python:3.12

ENV PYTHONDONTWRITEBYTECODE=1

# Install the libraries
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Copy the pipeline code (includes the aws/lambda_handler.py)
COPY services/pipeline/src/pipeline ${LAMBDA_TASK_ROOT}/pipeline

# Handler: package.file.function (waiting for Sumna to confirm)
CMD ["pipeline.aws.lambda_handler.lambda_handler"]