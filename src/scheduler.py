import schedule
import time
import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import main
from utils.logger import get_logger
from config import config

def job():
    logger = get_logger('scheduler')
    logger.info(f"Starting scheduled crawl at {datetime.now()}")
    try:
        main()
        logger.info("Scheduled crawl finished successfully")
    except Exception as e:
        logger.error(f"Scheduled crawl failed: {e}")

if __name__ == "__main__":
    logger = get_logger('scheduler')
    
    # Get schedule time from config or default to 09:00
    schedule_time = config.get('schedule_time', "09:00")
    
    logger.info(f"Scheduler started. Task scheduled for {schedule_time} daily.")
    
    # Schedule the job
    schedule.every().day.at(schedule_time).do(job)
    
    # Also run once immediately on startup? Maybe optional.
    # job() 
    
    while True:
        schedule.run_pending()
        time.sleep(60)
