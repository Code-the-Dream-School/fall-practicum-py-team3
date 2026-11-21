# syntax=docker/dockerfile:1
FROM public.ecr.aws/lambda/python:3.12

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 

WORKDIR ${LAMBDA_TASK_ROOT}

# Install the libraries
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the pipeline code (includes the aws/lambda_handler.py)
COPY pyproject.toml . 
COPY services/pipeline/src/ services/pipeline/src/
RUN pip install .
# Handler: package.file.function (waiting for Sumna to confirm)
CMD ["pipeline.aws.hello_world.lambda_handler"]