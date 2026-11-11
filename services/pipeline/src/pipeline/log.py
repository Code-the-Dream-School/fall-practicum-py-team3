"""Centralized logging helpers."""

import logging
import os

_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        # Example output: "2026-11-11 12:00:00,123 INFO pipeline.extract.extract: No air pollution records found."
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        logger.addHandler(handler)
    logger.setLevel(_LEVEL)
    return logger