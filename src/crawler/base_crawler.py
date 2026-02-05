from abc import ABC, abstractmethod
from typing import List, Dict, Optional
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
            
            should_exclude = any(kw in combined_text for kw in exclude_keywords)
            if should_exclude:
                continue
                
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
            # Fix SSL issues on Mac by using requests instead of urllib (via feedparser)
            response = requests.get(self.url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            articles = []
            
            if feed.bozo:
                print(f"Warning parsing feed {self.url}: {feed.bozo_exception}")

            for entry in feed.entries[:20]:
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
        if hasattr(entry, 'description'):
            return entry.description
        elif hasattr(entry, 'content') and entry.content:
            return entry.content[0].value
        elif hasattr(entry, 'summary'):
            return entry.summary
        return ''

class HTMLCrawler(BaseCrawler):
    """HTML 爬虫 - 支持中文网站"""
    
    def __init__(self, source_config: Dict):
        super().__init__(source_config)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
    def fetch(self) -> List[Dict]:
        """获取 HTML 文章列表"""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=30)
            response.encoding = response.apparent_encoding
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if 'anquanke.com' in self.url:
                return self._parse_anquanke(soup)
            elif 'freebuf.com' in self.url:
                return self._parse_freebuf(soup)
            elif 'kanxue.com' in self.url:
                return self._parse_kanxue(soup)
            elif 'sec-un.com' in self.url:
                return self._parse_secun(soup)
            elif 'hackdig.com' in self.url:
                return self._parse_hackdig(soup)
            else:
                return self._parse_generic(soup)
                
        except Exception as e:
            print(f"Error fetching from {self.name}: {e}")
            return []
    
    def _parse_anquanke(self, soup: BeautifulSoup) -> List[Dict]:
        """解析安全客"""
        articles = []
        for item in soup.select('.article-list-item')[:15]:
            try:
                title_elem = item.select_one('.article-title a')
                if not title_elem:
                    continue
                
                href = title_elem.get('href', '')
                if href and not href.startswith('http'):
                    href = 'https://www.anquanke.com' + href
                
                time_elem = item.select_one('.article-time')
                summary_elem = item.select_one('.article-summary')
                
                articles.append({
                    'source': self.name,
                    'category': self.category,
                    'title': title_elem.get_text().strip(),
                    'link': href,
                    'published': time_elem.get_text().strip() if time_elem else '',
                    'content': summary_elem.get_text().strip() if summary_elem else '',
                    'fetched_at': datetime.now().isoformat()
                })
            except:
                continue
        return articles
    
    def _parse_freebuf(self, soup: BeautifulSoup) -> List[Dict]:
        """解析 FreeBuf"""
        articles = []
        for item in soup.select('.news-item')[:15]:
            try:
                title_elem = item.select_one('h3 a')
                if not title_elem:
                    continue
                
                time_elem = item.select_one('.news-time')
                desc_elem = item.select_one('.news-desc')
                    
                articles.append({
                    'source': self.name,
                    'category': self.category,
                    'title': title_elem.get_text().strip(),
                    'link': title_elem.get('href', ''),
                    'published': time_elem.get_text().strip() if time_elem else '',
                    'content': desc_elem.get_text().strip() if desc_elem else '',
                    'fetched_at': datetime.now().isoformat()
                })
            except:
                continue
        return articles
    
    def _parse_kanxue(self, soup: BeautifulSoup) -> List[Dict]:
        """解析看雪论坛"""
        articles = []
        for item in soup.select('.list-item')[:10]:
            try:
                title_elem = item.select_one('.title a')
                if not title_elem:
                    continue
                
                href = title_elem.get('href', '')
                if href and not href.startswith('http'):
                    href = 'https://bbs.kanxue.com' + href
                
                date_elem = item.select_one('.date')
                summary_elem = item.select_one('.summary')
                    
                articles.append({
                    'source': self.name,
                    'category': self.category,
                    'title': title_elem.get_text().strip(),
                    'link': href,
                    'published': date_elem.get_text().strip() if date_elem else '',
                    'content': summary_elem.get_text().strip() if summary_elem else '',
                    'fetched_at': datetime.now().isoformat()
                })
            except:
                continue
        return articles
    
    def _parse_secun(self, soup: BeautifulSoup) -> List[Dict]:
        """解析安全头条"""
        articles = []
        for item in soup.select('.article-item')[:15]:
            try:
                title_elem = item.select_one('h3 a')
                if not title_elem:
                    continue
                
                time_elem = item.select_one('.time')
                summary_elem = item.select_one('.summary')
                    
                articles.append({
                    'source': self.name,
                    'category': self.category,
                    'title': title_elem.get_text().strip(),
                    'link': title_elem.get('href', ''),
                    'published': time_elem.get_text().strip() if time_elem else '',
                    'content': summary_elem.get_text().strip() if summary_elem else '',
                    'fetched_at': datetime.now().isoformat()
                })
            except:
                continue
        return articles
    
    def _parse_hackdig(self, soup: BeautifulSoup) -> List[Dict]:
        """解析互联网安全"""
        articles = []
        for item in soup.select('.post-item')[:15]:
            try:
                title_elem = item.select_one('.post-title a')
                if not title_elem:
                    continue
                
                date_elem = item.select_one('.post-date')
                excerpt_elem = item.select_one('.post-excerpt')
                    
                articles.append({
                    'source': self.name,
                    'category': self.category,
                    'title': title_elem.get_text().strip(),
                    'link': title_elem.get('href', ''),
                    'published': date_elem.get_text().strip() if date_elem else '',
                    'content': excerpt_elem.get_text().strip() if excerpt_elem else '',
                    'fetched_at': datetime.now().isoformat()
                })
            except:
                continue
        return articles
    
    def _parse_generic(self, soup: BeautifulSoup) -> List[Dict]:
        """通用 HTML 解析"""
        articles = []
        for link in soup.find_all('a', href=True)[:15]:
            href = link['href']
            title = link.get_text().strip()
            
            if len(title) > 10 and href.startswith('http'):
                articles.append({
                    'source': self.name,
                    'category': self.category,
                    'title': title,
                    'link': href,
                    'published': '',
                    'content': '',
                    'fetched_at': datetime.now().isoformat()
                })
                    
        return articles
