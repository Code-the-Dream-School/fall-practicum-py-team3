from pipeline.load.load_insight import load_insight
from pipeline.log import get_logger

logger = get_logger(__name__)


# Required by AWS Lambda: keep this func name and signature unchanged.
# Do not modify name or parameters.
# This handler is referenced in the dockerfile, so any
# changes here; must also be reflected in dockerfile.
def lambda_handler(event, context):

    try:

        logger.info("Starting insight load.")
        
        load_insight()

        logger.info("Insight load completed.")

        return {
            "statusCode": 200,
            "body": "Insight load completed successfully."    
        }

    except Exception:
        logger.exception("Daily insight load failed.")
        raise
