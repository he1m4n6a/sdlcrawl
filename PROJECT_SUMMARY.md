# SDL 安全文章爬取系统 - 项目总结

## 项目概述

这是一个自动化爬取安全领域（特别是 SDL 和 AI 安全）相关文章的系统，能够：
- 自动从多个安全资讯源爬取文章
- 使用 AI 翻译英文文章并提取关键点
- 每日定时推送精美日报到飞书
- 自动保存文章数据供后续分析

## 核心功能

### 1. 多源爬取
支持 8 个主流安全资讯源：
- OWASP Blog (RSS)
- PortSwigger Blog (RSS) 
- The Hacker News (RSS)
- Krebs on Security (RSS)
- Google Security Blog (RSS)
- Microsoft Security Blog (RSS)
- OpenAI Security (RSS)
- Anthropic Safety (HTML)

### 2. 智能过滤
基于关键词自动筛选文章：
- **包含关键词**: SDL, security, AI, LLM, application security, DevSecOps, etc.
- **排除关键词**: advertisement, sponsored

### 3. AI 翻译和总结
- 自动检测英文文章
- 使用 GPT-3.5 翻译标题
- 提取 100-200 字摘要
- 生成 3-5 个关键点（每个 20-50 字）

### 4. 飞书推送
- 精美的飞书卡片格式
- 包含分类、标题、摘要、关键点
- 附带"查看原文"按钮
- 每日定时自动推送

### 5. 持久化存储
- JSON 格式保存
- 按时间戳命名
- 便于后续分析和查看

## 技术栈

### 后端
- Python 3.11
- requests - HTTP 请求
- feedparser - RSS 解析
- beautifulsoup4 - HTML 解析
- openai - AI 翻译和总结
- lark-oapi - 飞书推送
- pyyaml - 配置文件解析
- schedule - 定时任务

### 数据格式
```json
{
  "source": "PortSwigger Blog",
  "category": "Web Security",
  "title": "Article Title",
  "link": "https://...",
  "published": "Thu, 22 Jan 2026 15:18:00 GMT",
  "content": "Article content...",
  "translated_title": "翻译后的标题",
  "summary": "文章摘要...",
  "key_points": ["关键点1", "关键点2", "关键点3"],
  "fetched_at": "2026-02-05T12:21:55.282292"
}
```

## 运行效果

### 爬取统计
- 总计爬取: 101 篇文章
- 关键词过滤后: 10 篇相关文章
- 最终推荐: 3-5 篇高质量文章

### 输出示例

```
================================================================================
                    🛡️ SDL 安全日报
                  📊 今日文章: 3 篇
================================================================================

1. 如何使用 Burp AI 加速 Repeater 中的漏洞验证
   ───────────────────────────────────────────────────────────────────────────
   📁 分类: Web Security
   📝 摘要: 本文介绍了作者如何利用 Burp AI 工具显著加快了漏洞验证流程...
   🎯 关键点:
      • Burp AI 能够自动生成和验证 exploit 代码
      • 通过 AI 辅助减少了手动验证的时间
      • 实际测试中验证速度提升了 60%
   🔗 原文链接: https://portswigger.net/blog/...

================================================================================
            由 SDL 安全文章爬取系统自动生成
               生成时间: Thu, 22 Jan 2026 15:18:00 GMT
================================================================================
```

## 项目结构

```
.
├── config/
│   └── sources.yaml          # 资讯源配置
├── src/
│   ├── crawler/              # 爬虫模块
│   │   ├── base_crawler.py      # 爬虫基类
│   │   └── article_fetcher.py   # 文章获取器
│   ├── translator/           # AI 翻译模块
│   │   └── ai_translator.py     # AI 翻译器
│   ├── notifier/             # 飞书通知模块
│   │   └── lark_notifier.py     # 飞书通知器
│   ├── utils/                # 工具模块
│   │   └── logger.py           # 日志工具
│   ├── data/                # 保存的文章数据
│   │   ├── articles_20260205_120139.json
│   │   └── articles_20260205_122254.json
│   ├── logs/                # 日志文件
│   │   ├── main_20260205.log
│   │   ├── fetcher_20260205.log
│   │   └── translator_20260205.log
│   ├── main.py              # 主程序
│   ├── simple_demo.py       # 简化演示版（无AI）
│   ├── demo_with_translation.py  # 完整演示版（带翻译）
│   └── show_report.py      # 报告展示脚本
├── scheduler.py             # 定时调度器
├── requirements.txt          # Python 依赖
├── .env.example            # 环境变量示例
├── .env                    # 环境变量配置
├── README.md               # 项目说明
├── RUNNING_RESULTS.md       # 运行效果展示
└── PROJECT_SUMMARY.md      # 项目总结（本文件）
```

## 使用方法

### 1. 安装依赖
```bash
pip install --break-system-packages -r requirements.txt
```

### 2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入 API 密钥
```

必需配置：
- `OPENAI_API_KEY` - OpenAI API 密钥
- `LARK_APP_ID` - 飞书应用 ID
- `LARK_APP_SECRET` - 飞书应用密钥
- `LARK_USER_ID` - 你的飞书用户 ID

可选配置：
- `CRAWL_HOUR` - 爬取时间（默认 9）
- `MAX_ARTICLES` - 爬取数量限制（默认 10）

### 3. 运行方式

#### 简化演示版（无需 API）
```bash
cd src
python3 simple_demo.py
```

#### 完整版（需要 API 配置）
```bash
cd src
python3 main.py
```

#### 定时任务
```bash
python3 scheduler.py
```

### 4. 查看报告
```bash
cd src
python3 show_report.py          # 查看最新报告
python3 demo_with_translation.py  # 查看带翻译的演示报告
```

## 配置说明

### 资讯源配置 (config/sources.yaml)

```yaml
sources:
  - name: "PortSwigger Blog"
    type: "rss"
    url: "https://portswigger.net/blog/rss"
    category: "Web Security"
    enabled: true

ai_security_sources:
  - name: "OpenAI Security"
    type: "rss"
    url: "https://openai.com/blog/rss.xml"
    category: "AI Security"
    enabled: true

keywords:
  include:
    - "SDL"
    - "security"
    - "AI"
    - "LLM"
    - "application security"
  exclude:
    - "advertisement"
    - "sponsored"
```

## 日志输出

所有日志保存在 `src/logs/` 目录：
- `main_YYYYMMDD.log` - 主程序日志
- `fetcher_YYYYMMDD.log` - 爬虫日志
- `translator_YYYYMMDD.log` - 翻译器日志

## 实际运行结果

### 成功爬取的文章主题

1. **Burp AI 相关** (6 篇)
   - How I sped up exploit validation in Repeater using Burp AI
   - Functional PoCs in less than a minute? Julen Garrido Estévez puts Burp AI to the test
   - DAST without disruption: Burp Suite DAST winter update 2025
   - How to detect React2Shell with Burp Suite
   - Hacking with Burp AI in Chesspocalypse
   - Can Burp AI hack a website?

2. **其他安全主题** (4 篇)
   - PortSwigger x TryHackMe
   - The Hacker News 最新安全资讯
   - Google Security Blog 安全更新
   - Microsoft Security Blog 安全公告

## 优势

1. **自动化**: 无需手动查找，自动爬取最新文章
2. **智能化**: AI 翻译和关键点提取，快速了解核心内容
3. **个性化**: 基于关键词过滤，只推送相关内容
4. **便捷性**: 飞书推送，随时随地查看
5. **持续性**: 每日自动推送，持续产出

## 适用场景

- SDL 安全工程师的日常学习
- 安全团队的资讯分享
- AI 安全研究的前沿跟踪
- 渗透测试的工具更新
- DevSecOps 的最佳实践

## 未来扩展

1. **更多资讯源**: 添加更多安全博客和媒体
2. **更智能过滤**: 基于用户兴趣学习推荐
3. **多语言支持**: 支持更多语言的翻译
4. **数据统计**: 文章阅读统计和趋势分析
5. **协作功能**: 团队共享和评论

## 许可证

MIT License
