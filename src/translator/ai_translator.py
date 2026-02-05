import os
import time
from typing import Dict, List, Tuple
from openai import OpenAI, APIConnectionError, RateLimitError, APIStatusError
from utils.logger import get_logger
from config import config

class AITranslator:
    """AI 翻译器"""
    
    def __init__(self):
        self.logger = get_logger('translator')
        openai_conf = config.get('openai_config', {})
        api_key = openai_conf.get('api_key') or os.getenv('OPENAI_API_KEY')
        base_url = openai_conf.get('base_url')
        
        if not api_key:
            self.logger.warning("OPENAI_API_KEY not found in config or env!")
        
        # Initialize client with optional base_url
        client_args = {'api_key': api_key}
        if base_url:
            client_args['base_url'] = base_url
            
        self.client = OpenAI(**client_args)
        self.model = openai_conf.get('model', 'gpt-3.5-turbo')
        self.temperature = openai_conf.get('temperature', 0.7)
        
    def translate_and_summarize(self, article: Dict) -> Dict:
        """翻译并总结文章"""
        try:
            title = article.get('title', '')
            content = article.get('content', '') or article.get('summary', '') or ''
            
            if len(content) < 50:
                 return {
                    **article,
                    'translated_title': title,
                    'summary': content,
                    'key_points': []
                }
            
            system_prompt = "You are an expert in Secure Development Lifecycle (SDL) and DevSecOps. Analyze the following security article."
            user_prompt = f"""
Input Title: {title}
Input Content (Excerpt): {content[:3000]}

Please output a JSON object with the following keys:
1. "translated_title": The title translated to Simplified Chinese.
2. "summary": A concise summary in Simplified Chinese (100-200 words).
3. "key_points": A list of 3-5 key takeaways in Simplified Chinese.
4. "sdl_advice": A concise list (1-3 distinct points) on how toapply this knowledge to an SDL/DevSecOps process. If not relevant, leave empty. Write in Simplified Chinese.

Ensure the response is valid JSON.
"""
            
            result = self._call_openai_with_retry(system_prompt, user_prompt)
            
            if not result:
                return article
            
            # 解析结果 (Handle JSON response)
            import json
            try:
                data = json.loads(result)
                translated_title = data.get('translated_title', title)
                summary = data.get('summary', '')
                key_points = data.get('key_points', [])
                sdl_advice = data.get('sdl_advice', [])
            except json.JSONDecodeError:
                # Fallback to text parsing if not JSON
                translated_title, summary, key_points = self._parse_ai_response(result)
                sdl_advice = []
            
            return {
                **article,
                'translated_title': translated_title or title,
                'summary': summary,
                'key_points': key_points,
                'sdl_advice': sdl_advice
            }
            
        except Exception as e:
            self.logger.error(f"Error translating article {article.get('title', 'unknown')}: {e}")
            return article
            
    def _call_openai_with_retry(self, system_prompt: str, user_prompt: str, max_retries: int = 3) -> str:
        """带重试机制的 OpenAI 调用"""
        for attempt in range(max_retries):
            try:
                # Combined prompt strategy as requested by user
                messages = [
                    {"role": "user", "content": system_prompt + "\n" + user_prompt}
                ]
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=1000,
                    response_format={ "type": "json_object" },
                    timeout=30
                )
                return response.choices[0].message.content
            except RateLimitError:
                self.logger.warning(f"Rate limit hit, waiting... (Attempt {attempt+1}/{max_retries})")
                time.sleep(2 * (attempt + 1))
            except (APIConnectionError, APIStatusError) as e:
                self.logger.warning(f"OpenAI API Error: {e} (Attempt {attempt+1}/{max_retries})")
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Unexpected OpenAI error: {e}")
                break
                
        return ""
    
    def _parse_ai_response(self, response: str) -> Tuple[str, str, List[str]]:
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
                
            if line.startswith('TITLE:'):
                translated_title = line.replace('TITLE:', '').strip()
                continue
            elif line.startswith('SUMMARY:'):
                current_section = 'summary'
                summary = line.replace('SUMMARY:', '').strip()
                continue
            elif line.startswith('POINTS:'):
                current_section = 'keypoints'
                continue
                
            if current_section == 'summary' and not line.startswith('POINTS:'):
                 # Append to summary if multiline
                 if not summary:
                     summary = line
                 else:
                     summary += " " + line
            elif current_section == 'keypoints':
                # 清理序号
                clean_point = line.lstrip('0123456789.-、• ')
                if clean_point:
                    key_points.append(clean_point)
                    
        return translated_title, summary, key_points
