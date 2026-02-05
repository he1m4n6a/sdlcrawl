import os
import yaml
import re
from typing import Any, Dict
from dotenv import load_dotenv

class Config:
    _instance = None
    _config = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        """加载配置"""
        load_dotenv()
        
        # 默认配置路径
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'settings.yaml')
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 解析环境变量替换 ${VAR}
                content = self._substitute_env_vars(content)
                self._config = yaml.safe_load(content)
        else:
            # Fallback defaults
            self._config = {
                "max_articles": int(os.getenv('MAX_ARTICLES', 10)),
                "log_level": "INFO",
                "output_dir": "data"
            }

    def _substitute_env_vars(self, content: str) -> str:
        """替换文本中的环境变量"""
        pattern = re.compile(r'\$\{([^}^{]+)\}')
        def replace(match):
            env_var = match.group(1)
            return os.getenv(env_var, '')
        return pattern.sub(replace, content)

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """获取配置项，支持点号访问 nested keys created by yaml load"""
        # 如果是简单的key
        if key in cls._instance._config:
            return cls._instance._config[key]
        
        # 支持 nested keys like 'openai_config.model'
        keys = key.split('.')
        value = cls._instance._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

# 全局单例
config = Config()
