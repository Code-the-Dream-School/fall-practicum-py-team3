from pipeline.load.load import main_incremental
from pipeline.load.load_gold import load_gold
from pipeline.load.load_insight import load_insight
from pipeline.log import get_logger

logger = get_logger(__name__)

def run_incremental():
    logger.info("Starting incremental pipeline")
    
    # extract and load new raw data
    logger.info("Starting extraction and then loading raw")
    main_incremental()
    
    # transform and load gold data
    logger.info("Starting gold data transformation and then loading")
    load_gold()
    
    # load daily insight
    logger.info("Starting daily insight loading")
    load_insight()
    
    logger.info("Incremental pipeline completed successfully.")
    
if __name__ == "__main__":
    run_incremental()