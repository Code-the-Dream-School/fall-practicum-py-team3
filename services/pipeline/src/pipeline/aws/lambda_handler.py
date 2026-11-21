from pipeline.load.load_gold import load_gold
from pipeline.load.load_insight import load_insight
from pipeline.log import get_logger

logger = get_logger(__name__)


# Required by AWS Lambda: keep this func name and signature unchanged.
# Do not modify name or parameters.
# This handler is referenced in the dockerfile, so any
# changes here; must also be reflected in dockerfile.
def lambda_handler(event, context):

    try:
        # transform raw data and load gold table
        logger.info("Starting data transformation and load gold")
        load_gold()

        # load daily insight
        logger.info("Starting load daily_insight.")
        load_insight()

        logger.info("Daily insight loaded successfully.")

        return {"status": "ok"}

    except Exception:
        logger.exception("Daily pipeline failed.")
        raise
