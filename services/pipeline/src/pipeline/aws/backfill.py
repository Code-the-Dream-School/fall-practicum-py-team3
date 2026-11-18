from pipeline.load.load import main
from pipeline.load.load_gold import load_gold
from pipeline.load.load_insight import load_insight
from pipeline.log import get_logger

logger = get_logger(__name__)

def run_backfill():
    logger.info("Starting backfill pipeline")
    
    # extract and load raw data
    logger.info("Starting extraction and then loading raw")
    main()
    
    # transform and load gold data
    logger.info("Starting gold data transformation and then loading")
    load_gold()
    
    # load daily insight
    logger.info("Starting daily insight loading")
    load_insight()
    
    logger.info("Backfill pipeline completed successfully.")
    
if __name__ == "__main__":
    run_backfill()