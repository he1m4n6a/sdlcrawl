import os
import json
from typing import List, Dict
from lark_oapi.api.bot.v1 import *
from lark_oapi import JSON
from ..utils.logger import get_logger

class LarkNotifier:
    """飞书通知器"""
    
    def __init__(self):
        self.logger = get_logger('notifier')
        self.app_id = os.getenv('LARK_APP_ID')
        self.app_secret = os.getenv('LARK_APP_SECRET')
        self.user_id = os.getenv('LARK_USER_ID')
        self.access_token = None
        
    def send_daily_report(self, articles: List[Dict]):
        """发送日报到飞书"""
        try:
            self._get_access_token()
            
            if not articles:
                message = "今日未获取到新的安全文章。"
                self._send_message(message)
                self.logger.info("Sent empty report to Lark")
                return
            
            # 构建富文本消息
            card_content = self._build_report_card(articles)
            self._send_card_message(card_content)
            
            self.logger.info(f"Sent daily report with {len(articles)} articles to Lark")
            
        except Exception as e:
            self.logger.error(f"Error sending report to Lark: {e}")
    
    def _get_access_token(self):
        """获取访问令牌"""
        from lark_oapi.api.auth.v3 import *
        
        client = Client(self.app_id, self.app_secret)
        request = GetAccessTokenRequest()
        
        response = client.auth.v3.tenant_access_token.internal_get(request)
        
        if response.code == 0:
            self.access_token = response.tenant_access_token
        else:
            raise Exception(f"Failed to get access token: {response.msg}")
    
    def _send_message(self, message: str):
        """发送文本消息"""
        client = Client(self.app_id, self.app_secret)
        request = SendTextRequest()
        request.user_id = self.user_id
        request.msg_type = 'text'
        request.content = json.dumps({'text': message})
        
        response = client.message.v4.user_message.send(request)
        
        if response.code != 0:
            raise Exception(f"Failed to send message: {response.msg}")
    
    def _send_card_message(self, card_content: dict):
        """发送卡片消息"""
        client = Client(self.app_id, self.app_secret)
        request = SendInteractiveRequest()
        request.user_id = self.user_id
        request.msg_type = 'interactive'
        request.card = card_content
        
        response = client.message.v4.user_message.send(request)
        
        if response.code != 0:
            raise Exception(f"Failed to send card message: {response.msg}")
    
    def _build_report_card(self, articles: List[Dict]) -> Dict:
        """构建报告卡片"""
        elements = [
            {
                "tag": "div",
                "text": {
                    "content": f"📊 今日安全文章日报（共 {len(articles)} 篇）",
                    "tag": "lark_md"
                }
            },
            {
                "tag": "hr"
            }
        ]
        
        for i, article in enumerate(articles[:10], 1):  # 最多显示10篇
            title = article.get('translated_title', article.get('title', ''))
            summary = article.get('summary', '')
            link = article.get('link', '')
            category = article.get('category', '')
            
            # 文章标题
            elements.append({
                "tag": "div",
                "text": {
                    "content": f"**{i}. {title}**",
                    "tag": "lark_md"
                }
            })
            
            # 分类标签
            if category:
                elements.append({
                    "tag": "div",
                    "text": {
                        "content": f"📁 分类: {category}",
                        "tag": "lark_md"
                    }
                })
            
            # 摘要
            if summary:
                elements.append({
                    "tag": "div",
                    "text": {
                        "content": f"📝 {summary}",
                        "tag": "lark_md"
                    }
                })
            
            # 关键点
            key_points = article.get('key_points', [])
            if key_points:
                points_text = '\n'.join([f"  • {point}" for point in key_points])
                elements.append({
                    "tag": "div",
                    "text": {
                        "content": f"🎯 关键点:\n{points_text}",
                        "tag": "lark_md"
                    }
                })
            
            # 原始链接
            if link:
                elements.append({
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "content": "查看原文",
                                "tag": "plain_text"
                            },
                            "type": "primary",
                            "url": link
                        }
                    ]
                })
            
            # 分隔线
            if i < min(len(articles), 10):
                elements.append({
                    "tag": "hr"
                })
        
        return {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "blue",
                "title": {
                    "content": "🛡️ SDL 安全日报",
                    "tag": "plain_text"
                }
            },
            "elements": elements
        }
