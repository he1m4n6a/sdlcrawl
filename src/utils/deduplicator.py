import os
import json
import hashlib
from typing import List, Dict
from utils.logger import get_logger
from config import config

class Deduplicator:
    """文章去重器"""
    
    def __init__(self, history_file: str = "data/history.json"):
        self.logger = get_logger('deduplicator')
        self.history_file = history_file
        self.history = self._load_history()
        
    def _load_history(self) -> Dict[str, int]:
        """加载历史记录"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading history: {e}")
                return {}
        return {}
        
    def _save_history(self):
        """保存历史记录"""
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving history: {e}")

    def _get_article_hash(self, article: Dict) -> str:
        """计算文章的唯一哈希值"""
        # 优先使用 URL，如果没有则使用 标题+发布日期
        if article.get('link'):
            return hashlib.md5(article['link'].encode('utf-8')).hexdigest()
        
        unique_str = f"{article.get('title', '')}_{article.get('published', '')}"
        return hashlib.md5(unique_str.encode('utf-8')).hexdigest()

    def filter_new_articles(self, articles: List[Dict]) -> List[Dict]:
        """过滤掉已处理过的文章"""
        new_articles = []
        for article in articles:
            article_hash = self._get_article_hash(article)
            
            # 检查是否已存在
            if article_hash not in self.history:
                new_articles.append(article)
            else:
                self.logger.debug(f"Duplicate article skipped: {article.get('title')}")
                
        return new_articles

    def mark_as_processed(self, articles: List[Dict]):
        """将文章标记为已处理"""
        import time
        timestamp = int(time.time())
        
        updated = False
        for article in articles:
            article_hash = self._get_article_hash(article)
            if article_hash not in self.history:
                self.history[article_hash] = timestamp
                updated = True
        
        if updated:
            self._save_history()
