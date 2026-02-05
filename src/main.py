#!/usr/bin/env python3
import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crawler.article_fetcher import ArticleFetcher
from translator.ai_translator import AITranslator
from notifier.lark_notifier import LarkNotifier
from utils.logger import get_logger

def main():
    """主函数"""
    load_dotenv()
    
    logger = get_logger('main')
    logger.info("Starting SDL Security News Crawler")
    
    try:
        # 获取配置
        max_articles = int(os.getenv('MAX_ARTICLES', 10))
        
        # 1. 获取文章
        logger.info("Fetching articles from sources...")
        fetcher = ArticleFetcher()
        articles = fetcher.fetch_all(max_articles=max_articles)
        
        if not articles:
            logger.warning("No articles fetched")
            return
        
        # 2. 翻译和总结
        logger.info("Translating and summarizing articles...")
        translator = AITranslator()
        processed_articles = []
        
        for i, article in enumerate(articles[:max_articles], 1):
            logger.info(f"Processing article {i}/{min(len(articles), max_articles)}: {article.get('title')}")
            processed = translator.translate_and_summarize(article)
            processed_articles.append(processed)
        
        # 3. 保存数据
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        data_file = os.path.join(data_dir, f"articles_{timestamp}.json")
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(processed_articles, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved articles to {data_file}")
        
        # 4. 发送到飞书
        logger.info("Sending report to Lark...")
        notifier = LarkNotifier()
        notifier.send_daily_report(processed_articles)
        
        logger.info("Daily report completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main process: {e}")
        raise

if __name__ == '__main__':
    main()
