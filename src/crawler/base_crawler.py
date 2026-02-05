from abc import ABC, abstractmethod
from typing import List, Dict
from datetime import datetime
import feedparser
import requests
from bs4 import BeautifulSoup

class BaseCrawler(ABC):
    """爬虫基类"""
    
    def __init__(self, source_config: Dict):
        self.name = source_config.get('name')
        self.url = source_config.get('url')
        self.category = source_config.get('category', 'General')
        self.enabled = source_config.get('enabled', True)
        
    @abstractmethod
    def fetch(self) -> List[Dict]:
        """获取文章列表"""
        pass
    
    def _filter_by_keywords(self, articles: List[Dict], keywords: Dict) -> List[Dict]:
        """根据关键词过滤文章"""
        filtered = []
        include_keywords = [kw.lower() for kw in keywords.get('include', [])]
        exclude_keywords = [kw.lower() for kw in keywords.get('exclude', [])]
        
        for article in articles:
            title = article.get('title', '').lower()
            content = article.get('content', '').lower()
            combined_text = title + ' ' + content
            
            # 检查排除关键词
            should_exclude = any(kw in combined_text for kw in exclude_keywords)
            if should_exclude:
                continue
                
            # 检查包含关键词（如果有配置）
            if include_keywords:
                should_include = any(kw in combined_text for kw in include_keywords)
                if not should_include:
                    continue
                    
            filtered.append(article)
            
        return filtered
    
class RSSCrawler(BaseCrawler):
    """RSS 爬虫"""
    
    def __init__(self, source_config: Dict):
        super().__init__(source_config)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def fetch(self) -> List[Dict]:
        """获取 RSS 文章列表"""
        try:
            feed = feedparser.parse(self.url)
            articles = []
            
            for entry in feed.entries[:20]:  # 每次最多获取20条
                article = {
                    'source': self.name,
                    'category': self.category,
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'content': self._extract_content(entry),
                    'fetched_at': datetime.now().isoformat()
                }
                articles.append(article)
                
            return articles
            
        except Exception as e:
            print(f"Error fetching from {self.name}: {e}")
            return []
    
    def _extract_content(self, entry) -> str:
        """提取文章内容"""
        # 尝试从 description 或 content 中提取
        if hasattr(entry, 'description'):
            return entry.description
        elif hasattr(entry, 'content') and entry.content:
            return entry.content[0].value
        elif hasattr(entry, 'summary'):
            return entry.summary
        return ''

class HTMLCrawler(BaseCrawler):
    """HTML 爬虫"""
    
    def __init__(self, source_config: Dict):
        super().__init__(source_config)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def fetch(self) -> List[Dict]:
        """获取 HTML 文章列表"""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # 通用的文章链接提取逻辑
            for link in soup.find_all('a', href=True)[:20]:
                href = link['href']
                title = link.get_text().strip()
                
                if len(title) > 10 and href.startswith('http'):
                    article = {
                        'source': self.name,
                        'category': self.category,
                        'title': title,
                        'link': href,
                        'published': '',
                        'content': '',
                        'fetched_at': datetime.now().isoformat()
                    }
                    articles.append(article)
                    
            return articles
            
        except Exception as e:
            print(f"Error fetching from {self.name}: {e}")
            return []
