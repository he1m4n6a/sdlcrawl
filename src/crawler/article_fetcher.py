import yaml
from typing import List, Dict
from .base_crawler import RSSCrawler, HTMLCrawler, BaseCrawler
from utils.logger import get_logger

class ArticleFetcher:
    """文章获取器"""
    
    def __init__(self, config_path: str = 'sources.yaml'):
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
        all_sources.extend(self.config.get('china_security_sources', []))
        
        # 根据源类型创建爬虫
        keywords = self.config.get('keywords', {})
        
        for source in all_sources:
            if not source.get('enabled', True):
                continue
                
            crawler = None
            try:
                if source.get('type') == 'rss':
                    crawler = RSSCrawler(source)
                elif source.get('type') == 'html':
                    crawler = HTMLCrawler(source)
                else:
                    self.logger.warning(f"Unknown source type: {source.get('type')}")
                    continue
                
                articles = crawler.fetch()
                
                # 过滤文章
                filtered = crawler._filter_by_keywords(articles, keywords)
                all_articles.extend(filtered)
                
                self.logger.info(f"Fetched {len(filtered)} articles from {source['name']}")
                
            except Exception as e:
                self.logger.error(f"Error processing source {source['name']}: {e}")
        
        # 限制数量
        if max_articles:
            all_articles = all_articles[:max_articles]
        
        self.logger.info(f"Total articles fetched: {len(all_articles)}")
        return all_articles
