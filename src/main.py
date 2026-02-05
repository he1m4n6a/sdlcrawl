import sys
import os
import json
import concurrent.futures
from datetime import datetime
from dotenv import load_dotenv

# Patch for Python 3.13 where cgi module is removed, but feedparser depends on it
if sys.version_info >= (3, 13):
    try:
        import cgi
    except ImportError:
        import types
        import email.message
        
        def parse_header(line):
            m = email.message.Message()
            m['content-type'] = line
            params = {}
            for param in m.get_params()[1:]:
                params[param[0]] = param[1]
            return m.get_content_type(), params

        cgi_mock = types.ModuleType('cgi')
        cgi_mock.parse_header = parse_header
        sys.modules['cgi'] = cgi_mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from crawler.article_fetcher import ArticleFetcher
from translator.ai_translator import AITranslator
from notifier.lark_notifier import LarkNotifier
from utils.logger import get_logger

def main():
    """主函数"""
    # Config is loaded automatically on import
    
    logger = get_logger('main')
    logger.info("Starting SDL Security News Crawler")
    
    try:
        # 获取配置
        max_articles = config.get('max_articles', 10)
        
        # 1. 获取文章
        # 1. 获取文章
        logger.info("Fetching articles from sources...")
        fetcher = ArticleFetcher()
        raw_articles = fetcher.fetch_all(max_articles=max_articles * 2) # Fetch more to allow for duplicates
        
        if not raw_articles:
            logger.warning("No articles fetched")
            return

        # 1.5 去重过滤
        from utils.deduplicator import Deduplicator
        deduplicator = Deduplicator()
        articles = deduplicator.filter_new_articles(raw_articles)
        
        logger.info(f"deduplication: {len(raw_articles)} raw -> {len(articles)} unique new articles")
        
        if not articles:
            logger.info("No new articles to process after deduplication")
            return
            
        # Limit to max_articles after deduplication
        articles = articles[:max_articles]
        
        # 2. 翻译和总结 (并行处理)
        logger.info("Translating and summarizing articles...")
        translator = AITranslator()
        processed_articles = []
        
        # 使用 ThreadPoolExecutor 并行处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # 提交任务
            future_to_article = {
                executor.submit(translator.translate_and_summarize, article): article 
                for article in articles
            }
            
            for future in concurrent.futures.as_completed(future_to_article):
                article = future_to_article[future]
                try:
                    processed = future.result()
                    processed_articles.append(processed)
                    logger.info(f"Processed: {article.get('title')[:30]}...")
                except Exception as exc:
                    logger.error(f"Article processing generated an exception: {exc}")
                    processed_articles.append(article) # Keep original if failed
        
        # 3. 保存数据
        data_dir = config.get('output_dir', 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        data_file = os.path.join(data_dir, f"articles_{timestamp}.json")
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(processed_articles, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved articles to {data_file}")

        # 3.5 标记为已处理
        deduplicator.mark_as_processed(processed_articles)
        
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
