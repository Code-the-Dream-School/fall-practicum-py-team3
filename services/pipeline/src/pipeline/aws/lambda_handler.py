from pipeline.log import get_logger
from pipeline.aws.backfill import run_backfill
from pipeline.aws.incremental import run_incremental

logger = get_logger(__name__)

def lambda_handler(event, context):
    mode = event.get("mode")
    
    logger.info("Lambda triggered with mode: %s", mode)
    
    if mode == "backfill":
        run_backfill()
        
    elif mode == "incremental":
        run_incremental()
        
    else:
        raise ValueError(f"Invalid pipeline mode: {mode}")
    
    logger.info("Lambda execution completed successfully.")
    
    return {
        "status": "ok",
        "mode": mode
    }