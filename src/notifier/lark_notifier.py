import os
import json
import requests
from typing import List, Dict
from utils.logger import get_logger

from config import config

class LarkNotifier:
    """飞书通知器 - 使用 Webhook 发送"""
    
    def __init__(self):
        self.logger = get_logger('notifier')
        lark_conf = config.get('lark_config', {})
        self.webhook_url = lark_conf.get('webhook_url') or os.getenv('LARK_WEBHOOK_URL')
        self.webhook_key = lark_conf.get('webhook_key') or os.getenv('LARK_WEBHOOK_KEY')
        
    def send_daily_report(self, articles: List[Dict]):
        """发送日报到飞书"""
        try:
            if not articles:
                self._send_message("今日未获取到新的安全文章。")
                self.logger.info("Sent empty report to Lark")
                return
            
            # 构建卡片消息
            card_content = self._build_report_card(articles)
            self._send_webhook(card_content)
            
            self.logger.info(f"Sent daily report with {len(articles)} articles to Lark")
            
        except Exception as e:
            self.logger.error(f"Error sending report to Lark: {e}")
    
    def _send_webhook(self, card_content: dict):
        """通过 Webhook 发送卡片消息"""
        if not self.webhook_url:
            raise Exception("LARK_WEBHOOK_URL not configured")
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        if self.webhook_key:
            headers['X-Lark-Request-Key'] = self.webhook_key
        
        payload = {
            "msg_type": "interactive",
            "card": card_content
        }
        
        response = requests.post(
            self.webhook_url,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"Webhook request failed: {response.text}")
            
        try:
            resp_json = response.json()
            if resp_json.get('code') != 0:
                raise Exception(f"Lark API Error: code={resp_json.get('code')}, msg={resp_json.get('msg')}")
        except ValueError:
            pass # Non-JSON response, rely on status code
    
    def _send_message(self, message: str):
        """发送简单文本消息"""
        self._send_webhook({
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "blue",
                "title": {
                    "content": "SDL 安全日报",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": message,
                        "tag": "lark_md"
                    }
                }
            ]
        })
    
    def _build_report_card(self, articles: List[Dict]) -> Dict:
        """构建精美的报告卡片"""
        elements = []
        
        # 头部统计信息
        elements.extend(self._build_header_elements(len(articles)))
        
        # 文章列表
        for i, article in enumerate(articles[:10], 1):
            elements.extend(self._build_article_elements(i, article))
            if i < min(len(articles), 10):
                elements.append({"tag": "hr"})
        
        # 底部信息
        elements.append(self._build_footer_elements())
        
        return {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "blue",
                "title": {
                    "content": "🛡️ SDL 安全日报",
                    "tag": "plain_text"
                },
                "subtitle": {
                    "content": f"今日精选 {len(articles)} 篇高质量文章",
                    "tag": "plain_text"
                }
            },
            "elements": elements
        }
    
    def _build_header_elements(self, total: int) -> List[Dict]:
        """构建头部元素"""
        return [
            {
                "tag": "div",
                "text": {
                    "content": f"📊 共爬取 {total} 篇文章 | 已为您推荐最相关的 {min(total, 10)} 篇",
                    "tag": "lark_md"
                }
            },
            {"tag": "hr"}
        ]
    
    def _build_article_elements(self, index: int, article: Dict) -> List[Dict]:
        """构建单篇文章元素"""
        title = article.get('translated_title', article.get('title', ''))
        link = article.get('link', '')
        category = article.get('category', 'N/A')
        summary = article.get('summary', '')
        key_points = article.get('key_points', [])
        source = article.get('source', 'N/A')
        
        elements = []
        
        # 序号和标题
        elements.append({
            "tag": "div",
            "text": {
                "content": f"**{index}. {title}**",
                "tag": "lark_md"
            }
        })
        
        # 来源和分类标签
        elements.append({
            "tag": "div",
            "fields": [
                {
                    "is_short": True,
                    "text": {
                        "content": f"📰 {source}",
                        "tag": "lark_md"
                    }
                },
                {
                    "is_short": True,
                    "text": {
                        "content": f"🏷️ {category}",
                        "tag": "lark_md"
                    }
                }
            ]
        })
        
        # 摘要（使用折叠卡片）
        if summary:
            elements.append({
                "tag": "div",
                "text": {
                    "content": f"📝 {summary}",
                    "tag": "lark_md"
                }
            })
        
        # 关键点（使用折叠卡片）
        if key_points:
            elements.append({
                "tag": "div",
                "text": {
                    "content": "🎯 **关键要点**",
                    "tag": "lark_md"
                }
            })
            
            for point in key_points[:4]:  # 最多显示4个关键点
                elements.append({
                    "tag": "div",
                    "text": {
                        "content": f"• {point}",
                        "tag": "lark_md"
                    }
                })
        
        # SDL 落地建议 (New Section)
        sdl_advice = article.get('sdl_advice', [])
        if sdl_advice:
             elements.append({
                "tag": "div",
                "text": {
                    "content": "🏗️ **SDL 落地场景**",
                    "tag": "lark_md"
                }
            })
             for point in sdl_advice:
                elements.append({
                    "tag": "div",
                    "text": {
                        "content": f"• {point}",
                        "tag": "lark_md"
                    }
                })
        
        # 查看原文按钮
        if link:
            elements.append({
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "content": "🔗 查看原文",
                            "tag": "plain_text"
                        },
                        "type": "primary",
                        "url": link
                    }
                ]
            })
        
        return elements
    
    def _build_footer_elements(self) -> Dict:
        """构建底部元素"""
        return {
            "tag": "div",
            "text": {
                "content": "✨ _由 SDL 安全文章爬取系统自动生成_",
                "tag": "lark_md"
            }
        }
