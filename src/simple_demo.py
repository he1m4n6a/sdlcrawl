#!/usr/bin/env python3
import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crawler.article_fetcher import ArticleFetcher
from utils.logger import get_logger

def main():
    """简化版主函数（不带AI翻译）"""
    logger = get_logger('demo')
    logger.info("Starting SDL Security News Crawler (Demo Mode)")
    
    try:
        max_articles = int(os.getenv('MAX_ARTICLES', 5))
        
        # 1. 获取文章
        logger.info("Fetching articles from sources...")
        fetcher = ArticleFetcher()
        articles = fetcher.fetch_all(max_articles=max_articles)
        
        if not articles:
            logger.warning("No articles fetched")
            return
        
        logger.info(f"Total articles fetched: {len(articles)}")
        
        # 2. 显示文章信息
        print("\n" + "="*80)
        print("SDL 安全文章日报")
        print("="*80 + "\n")
        
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article.get('title', 'N/A')}")
            print(f"   来源: {article.get('source', 'N/A')}")
            print(f"   分类: {article.get('category', 'N/A')}")
            print(f"   链接: {article.get('link', 'N/A')}")
            print(f"   发布时间: {article.get('published', 'N/A')}")
            print(f"   内容预览: {article.get('content', 'N/A')[:200]}...")
            print()
        
        # 3. 保存数据
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        data_file = os.path.join(data_dir, f"articles_{timestamp}.json")
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved articles to {data_file}")
        
    except Exception as e:
        logger.error(f"Error in main process: {e}")
        raise

if __name__ == '__main__':
    main()
