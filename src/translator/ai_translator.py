import os
from typing import Dict, List
from openai import OpenAI
from ..utils.logger import get_logger

class AITranslator:
    """AI 翻译器"""
    
    def __init__(self):
        self.logger = get_logger('translator')
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def translate_and_summarize(self, article: Dict) -> Dict:
        """翻译并总结文章"""
        try:
            title = article.get('title', '')
            content = article.get('content', '')
            
            if not content:
                # 如果没有内容，只翻译标题
                translated_title = self._translate_text(title)
                return {
                    **article,
                    'translated_title': translated_title,
                    'summary': '暂无详细内容',
                    'key_points': []
                }
            
            # 检测是否是英文
            is_english = self._is_english(title + content)
            
            if not is_english:
                # 非英文文章，直接提取关键点
                summary, key_points = self._extract_key_points(title, content)
                return {
                    **article,
                    'translated_title': title,
                    'summary': summary,
                    'key_points': key_points
                }
            
            # 英文文章，翻译并总结
            prompt = f"""
请分析以下安全文章，提供中文翻译和关键信息提取：

标题: {title}
内容: {content[:2000]}

请按以下格式输出：
1. 翻译标题
2. 文章摘要（100-200字）
3. 3-5个关键点（每个点20-50字）
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的安全专家，擅长翻译和总结安全技术文章。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            
            # 解析结果
            translated_title, summary, key_points = self._parse_ai_response(result)
            
            return {
                **article,
                'translated_title': translated_title or title,
                'summary': summary,
                'key_points': key_points
            }
            
        except Exception as e:
            self.logger.error(f"Error translating article: {e}")
            return article
    
    def _is_english(self, text: str) -> bool:
        """检测文本是否主要是英文"""
        if not text:
            return False
        english_chars = sum(1 for c in text if c.isalpha() and c.isascii())
        total_chars = sum(1 for c in text if c.isalpha())
        return total_chars > 0 and english_chars / total_chars > 0.7
    
    def _translate_text(self, text: str) -> str:
        """简单翻译"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "请将以下文本翻译成中文。"
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content
        except:
            return text
    
    def _extract_key_points(self, title: str, content: str) -> tuple:
        """提取关键点"""
        try:
            prompt = f"""
请分析以下文章，提取关键信息：

标题: {title}
内容: {content[:1500]}

请提供：
1. 文章摘要（100-200字）
2. 3-5个关键点（每个点20-50字）
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的安全专家，擅长总结文章关键信息。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            result = response.choices[0].message.content
            return self._parse_ai_response(result)
            
        except Exception as e:
            self.logger.error(f"Error extracting key points: {e}")
            return content, []
    
    def _parse_ai_response(self, response: str) -> tuple:
        """解析 AI 响应"""
        lines = response.strip().split('\n')
        translated_title = ''
        summary = ''
        key_points = []
        
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if '标题' in line or '翻译' in line:
                current_section = 'title'
                continue
            elif '摘要' in line:
                current_section = 'summary'
                continue
            elif '关键点' in line or '要点' in line:
                current_section = 'keypoints'
                continue
                
            if current_section == 'title' and not translated_title:
                translated_title = line
            elif current_section == 'summary' and not summary:
                summary = line
            elif current_section == 'keypoints' and line:
                # 清理序号
                clean_point = line.lstrip('0123456789.-、 ')
                if clean_point:
                    key_points.append(clean_point)
                    
        return translated_title, summary, key_points
