# SDL 安全文章爬取系统

自动化爬取安全领域（特别是 SDL 和 AI 安全）相关文章，自动翻译、总结关键点，并推送至飞书。

## 功能特点

- 多源爬取：支持 RSS 和 HTML 多种安全资讯源
- 智能过滤：基于关键词自动筛选相关文章
- AI 翻译：使用 GPT 自动翻译英文文章并提取关键点
- 自动推送：每日定时推送日报到飞书
- 持久化存储：自动保存处理后的文章数据

## 安装步骤

### 1. 安装 Python 依赖

```bash
pip install --break-system-packages -r requirements.txt
```

### 2. 配置环境变量

复制示例配置文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入以下配置：

```env
# OpenAI API 配置
OPENAI_API_KEY=your_openai_api_key_here

# Lark 飞书配置
LARK_APP_ID=your_lark_app_id_here
LARK_APP_SECRET=your_lark_app_secret_here
LARK_USER_ID=your_lark_user_id_here

# 可选: 爬取时间配置 (小时，24小时制)
CRAWL_HOUR=9

# 可选: 爬取数量限制
MAX_ARTICLES=10
```

### 3. 配置飞书机器人

创建飞书机器人并获取配置：

1. 登录飞书开放平台: https://open.feishu.cn/
2. 创建应用，获取 App ID 和 App Secret
3. 配置机器人权限：
   - `获取用户 ID`
   - `获取与发送单聊消息`
4. 获取你的 User ID

### 4. 配置 OpenAI API

注册 OpenAI 账号并获取 API Key: https://platform.openai.com/

## 使用方法

### 手动执行一次

```bash
python src/main.py
```

### 定时任务运行

```bash
python scheduler.py
```

调度器会在每天指定时间（默认为早上 9 点）自动执行爬取任务。

## 配置说明

### 资讯源配置

编辑 `config/sources.yaml` 文件添加或修改资讯源：

```yaml
sources:
  - name: "Source Name"
    type: "rss"  # 或 "html"
    url: "https://example.com/feed/"
    category: "Category"
    enabled: true
```

### 关键词过滤

在 `config/sources.yaml` 中配置过滤关键词：

```yaml
keywords:
  include:
    - "SDL"
    - "security"
    - "AI"
  exclude:
    - "advertisement"
```

## 项目结构

```
.
├── config/
│   └── sources.yaml          # 资讯源配置
├── data/
│   └── articles_*.json       # 保存的文章数据
├── logs/
│   └── *.log                 # 日志文件
├── src/
│   ├── crawler/              # 爬虫模块
│   ├── translator/           # 翻译模块
│   ├── notifier/             # 通知模块
│   ├── utils/                # 工具模块
│   └── main.py               # 主程序
├── scheduler.py              # 定时调度器
├── requirements.txt          # Python 依赖
├── .env                      # 环境变量配置
└── README.md                 # 本文件
```

## 注意事项

1. **API 限制**：OpenAI API 有调用次数限制，注意控制每日文章数量
2. **网络问题**：某些网站可能有反爬机制，遇到问题可调整 User-Agent
3. **时区设置**：定时任务使用系统时区，确保设置正确

## 许可证

MIT License
