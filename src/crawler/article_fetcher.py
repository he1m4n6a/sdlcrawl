import yaml
from typing import List, Dict
from .base_crawler import RSSCrawler, HTMLCrawler, BaseCrawler
from utils.logger import get_logger
from config import config

class ArticleFetcher:
    """文章获取器"""
    
    def __init__(self, config_path: str = 'sources.yaml'):
        self.logger = get_logger('fetcher')
        # Config 已经在 main 中初始化，但这里我们还需要加载具体的 source.yaml
        # 或者我们可以把 sources.yaml 的内容也整合进 settings? 
        # 为了保持兼容性，我们还是读取 sources.yaml，但路径需要处理好
        self.sources_config = self._load_sources_config(config_path)
        
    def _load_sources_config(self, config_path: str) -> Dict:
        """加载源配置文件"""
        try:
            # 尝试在 src 目录下找
            import os
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            full_path = os.path.join(base_dir, config_path)
            
            self.logger.info(f"Loading sources from {full_path}")
            
            with open(full_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Failed to load sources config: {e}")
            return {}
    
    def fetch_all(self, max_articles: int = None) -> List[Dict]:
        """从所有源获取文章"""
        all_articles = []
        
        # 合并所有源
        all_sources = []
        all_sources.extend(self.sources_config.get('sources', []))
        all_sources.extend(self.sources_config.get('ai_security_sources', []))
        all_sources.extend(self.sources_config.get('china_quality_sources', []))
        # 移除中国源的自动合并逻辑
        
        # 根据源类型创建爬虫
        keywords = self.sources_config.get('keywords', {})
        
        # 统计
        success_count = 0
        fail_count = 0
        
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
                
                self.logger.info(f"Fetching from {source['name']}...")
                articles = crawler.fetch()
                
                # 过滤文章
                filtered = crawler._filter_by_keywords(articles, keywords)
                all_articles.extend(filtered)
                
                if filtered:
                    self.logger.info(f"✅ Fetched {len(filtered)} articles from {source['name']}")
                else:
                    self.logger.info(f"⚠️ No relevant articles from {source['name']}")
                
                success_count += 1
                
            except Exception as e:
                self.logger.error(f"❌ Error processing source {source['name']}: {e}")
                fail_count += 1
        
        self.logger.info(f"Fetch completed. Success sources: {success_count}, Failed: {fail_count}")
            
        # 限制数量
        if max_articles:
            all_articles = all_articles[:max_articles]
        
        self.logger.info(f"Total articles collected for processing: {len(all_articles)}")
        return all_articles
