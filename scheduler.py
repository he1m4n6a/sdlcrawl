#!/usr/bin/env python3
import os
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from src.main import main
from src.utils.logger import get_logger

def run_scheduled_task():
    """执行定时任务"""
    logger = get_logger('scheduler')
    logger.info(f"Scheduled task started at {datetime.now()}")
    
    try:
        main()
    except Exception as e:
        logger.error(f"Scheduled task failed: {e}")

def main():
    """调度器主函数"""
    load_dotenv()
    logger = get_logger('scheduler')
    
    # 获取配置的爬取时间
    crawl_hour = int(os.getenv('CRAWL_HOUR', 9))
    
    # 设置定时任务
    schedule.every().day.at(f"{crawl_hour:02d}:00").do(run_scheduled_task)
    
    logger.info(f"Scheduler started. Will run daily at {crawl_hour:02d}:00")
    logger.info("Press Ctrl+C to stop")
    
    try:
        # 首次立即执行一次
        run_scheduled_task()
        
        # 持续运行
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
            
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.error(f"Scheduler error: {e}")
        raise

if __name__ == '__main__':
    main()
