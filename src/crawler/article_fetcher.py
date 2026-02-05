import yaml
from typing import List, Dict
from .base_crawler import RSSCrawler, HTMLCrawler
from ..utils.logger import get_logger

class ArticleFetcher:
    """文章获取器"""
    
    def __init__(self, config_path: str = 'config/sources.yaml'):
        self.logger = get_logger('fetcher')
        self.config = self._load_config(config_path)
        
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return {}
    
    def fetch_all(self, max_articles: int = None) -> List[Dict]:
        """从所有源获取文章"""
        all_articles = []
        
        # 合并所有源
        all_sources = []
        all_sources.extend(self.config.get('sources', []))
        all_sources.extend(self.config.get('ai_security_sources', []))
        
        # 根据源类型创建爬虫
        for source in all_sources:
            if not source.get('enabled', True):
                continue
                
            try:
                if source.get('type') == 'rss':
                    crawler = RSSCrawler(source)
                elif source.get('type') == 'html':
                    crawler = HTMLCrawler(source)
                else:
                    self.logger.warning(f"Unknown source type: {source.get('type')}")
                    continue
                
                articles = crawler.fetch()
                all_articles.extend(articles)
                self.logger.info(f"Fetched {len(articles)} articles from {source['name']}")
                
            except Exception as e:
                self.logger.error(f"Error processing source {source['name']}: {e}")
        
        # 根据关键词过滤
        keywords = self.config.get('keywords', {})
        filtered_articles = []
        for article in all_articles:
            try:
                if crawler._filter_by_keywords([article], keywords):
                    filtered_articles.append(article)
            except:
                filtered_articles.append(article)
        
        # 限制数量
        if max_articles:
            filtered_articles = filtered_articles[:max_articles]
        
        self.logger.info(f"Total articles fetched: {len(filtered_articles)}")
        return filtered_articles
