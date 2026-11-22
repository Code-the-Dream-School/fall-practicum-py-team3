from pipeline.load.load import main
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
        logger.info("Starting pipeline.")

        # calls extraction and load raw table
        main()
        
        # calls transformation and load gold table
        load_gold()

        # transform hourly into daily data and load daily insight table
        load_insight()
        
        logger.info("Pipeline completed successfully.")

        return {"statusCode": 200, "body": "ok"}

    except Exception:
        logger.exception("Pipeline failed to complete.")
        raise
