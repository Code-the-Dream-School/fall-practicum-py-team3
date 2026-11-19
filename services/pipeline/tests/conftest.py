"""Shared pytest fixtures and configuration for the pipeline test suite."""

import logging

import prefect


def _noop_decorator(*args, **kwargs):
    """No-op stand-in for @flow/@task so tests run without Prefect's runtime."""
    if len(args) == 1 and callable(args[0]) and not kwargs:
        return args[0]

    def wrapper(fn):
        return fn

    return wrapper


# Patch Prefect's decorators before any test module imports pipeline.orchestration.flow.
# This lets the flow run as plain Python: no ephemeral server, no task retries/backoff.
prefect.flow = _noop_decorator
prefect.task = _noop_decorator
prefect.get_run_logger = lambda: logging.getLogger("prefect.test")
