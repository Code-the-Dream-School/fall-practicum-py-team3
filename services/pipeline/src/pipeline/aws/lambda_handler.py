from pipeline.log import get_logger
from pipeline.load.load import main_backfill
from pipeline.load.load_gold import load_gold
from pipeline.load.load_insight import load_insight

logger = get_logger(__name__)

def lambda_handler(event, context):
    
    try: 
        logger.info("Starting backfill pipeline")
        
        # extract/load raw data
        logger.info("Starting extraction and load raw")
        main_backfill()
        
        # transform/load gold data
        logger.info("Starting data transformation and load gold")
        load_gold()
        
        # load daily insight
        logger.info("Starting load daily insight")
        load_insight()
        
        logger.info("Backfill pipeline completed successfully.")
        
        return {
            "status": "ok"
        }
        
    except Exception as error:
        logger.exception("Failed to run pipeline.")
        raise