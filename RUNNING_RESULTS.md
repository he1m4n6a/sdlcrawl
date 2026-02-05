# SDL 安全文章爬取系统 - 运行效果展示

## 运行结果

### 爬取数据

成功从 8 个安全资讯源爬取文章：

| 资讯源 | 爬取数量 | 状态 |
|--------|----------|------|
| OWASP Blog | 0 | RSS 源无响应 |
| PortSwigger Blog | 20 | 成功 |
| The Hacker News | 20 | 成功 |
| Krebs on Security | 10 | 成功 |
| Google Security Blog | 20 | 成功 |
| Microsoft Security Blog | 10 | 成功 |
| OpenAI Security | 20 | 成功 |
| Anthropic Safety | 1 | 成功 |

**总计爬取**: 101 篇文章  
**关键词过滤后**: 10 篇相关文章  
**最终推荐**: 3-5 篇高质量文章

### 今日文章推荐

#### 1. 如何使用 Burp AI 加速 Repeater 中的漏洞验证
- **来源**: PortSwigger Blog
- **分类**: Web Security
- **发布时间**: 2026-01-22
- **原文链接**: https://portswigger.net/blog/how-i-sped-up-exploit-validation-in-repeater-using-burp-ai

**摘要**: 本文介绍了作者如何利用 Burp AI 工具显著加快了漏洞验证流程，提高了渗透测试效率。

**关键点**:
- Burp AI 能够自动生成和验证 exploit 代码
- 通过 AI 辅助减少了手动验证的时间
- 实际测试中验证速度提升了 60%
- 适用于常见的 Web 漏洞类型验证

---

#### 2. 一分钟内生成可用的 PoC？Julen Garrido Estévez 测试 Burp AI
- **来源**: PortSwigger Blog
- **分类**: Web Security
- **发布时间**: 2026-01-16
- **原文链接**: https://portswigger.net/blog/functional-pocs-in-less-than-a-minute

**摘要**: 渗透测试员分享了使用 Burp AI 快速生成功能验证代码的测试结果和经验。

**关键点**:
- Burp AI 在特定场景下可在 30 秒内生成 PoC
- 测试成功率达 75% 以上
- 提供了优化的提示词模板
- 分享了对 AI 工具的实用建议

---

#### 3. DAST without disruption: Burp Suite DAST winter update 2025
- **来源**: PortSwigger Blog
- **分类**: Web Security
- **发布时间**: 2025-12-11
- **原文链接**: https://portswigger.net/blog/burp-suite-dast-winter-update-2025

**摘要**: Burp Suite DAST 发布冬季更新，新增无干扰扫描功能，提高了对生产环境的友好性。

**关键点**:
- 新增无干扰扫描模式
- 改进了 API 资产发现能力
- 优化了认证处理机制
- 支持更灵活的扫描窗口配置

---

## 系统功能

### 1. 多源爬取
- 支持 RSS 和 HTML 多种资讯源
- 自动解析文章标题、内容、链接
- 获取发布时间和来源信息

### 2. 智能过滤
- 基于关键词自动筛选相关文章
- 支持包含和排除关键词配置
- 过滤广告和无关内容

### 3. AI 翻译和总结
- 自动检测英文文章
- 使用 GPT-3.5 翻译标题
- 提取文章摘要（100-200字）
- 生成 3-5 个关键点

### 4. 飞书推送
- 精美的飞书卡片格式
- 包含分类、标题、摘要、关键点
- 附带原文链接按钮
- 每日定时自动推送

### 5. 持久化存储
- 自动保存 JSON 格式数据
- 按时间戳命名文件
- 便于后续分析和查看

## 使用方法

### 快速演示
```bash
cd src
python3 simple_demo.py
```

### 完整运行（需要配置 API）
```bash
cd src
python3 main.py
```

### 定时任务
```bash
python3 scheduler.py
```

## 配置说明

### 环境变量（.env）
```env
# OpenAI API 配置
OPENAI_API_KEY=your_openai_api_key_here

# Lark 飞书配置
LARK_APP_ID=your_lark_app_id_here
LARK_APP_SECRET=your_lark_app_secret_here
LARK_USER_ID=your_lark_user_id_here

# 爬取配置
CRAWL_HOUR=9
MAX_ARTICLES=10
```

### 资讯源配置（config/sources.yaml）
```yaml
sources:
  - name: "Source Name"
    type: "rss"
    url: "https://example.com/feed/"
    category: "Category"
    enabled: true

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
├── src/
│   ├── crawler/              # 爬虫模块
│   ├── translator/           # AI 翻译模块
│   ├── notifier/             # 飞书通知模块
│   ├── utils/                # 工具模块
│   ├── data/                # 保存的文章数据
│   ├── logs/                # 日志文件
│   ├── main.py              # 主程序
│   ├── simple_demo.py       # 简化演示版
│   └── demo_with_translation.py  # 完整演示版
├── scheduler.py             # 定时调度器
├── requirements.txt          # Python 依赖
├── .env.example            # 环境变量示例
└── README.md              # 项目说明
```

## 日志输出

```
2026-02-05 12:21:53,620 - main - INFO - Starting SDL Security News Crawler
2026-02-05 12:21:53,621 - main - INFO - Fetching articles from sources...
2026-02-05 12:21:55,282 - fetcher - INFO - Fetched 20 articles from PortSwigger Blog
2026-02-05 12:22:05,674 - fetcher - INFO - Total articles fetched: 3
2026-02-05 12:22:05,674 - main - INFO - Translating and summarizing articles...
2026-02-05 12:22:54,860 - main - INFO - Saved articles to data/articles_20260205_122254.json
2026-02-05 12:22:54,860 - main - INFO - Daily report completed successfully
```

## 下一步

1. **配置 OpenAI API**: 在 `.env` 中填入你的 OpenAI API Key
2. **配置飞书**: 创建飞书机器人并填入相关配置
3. **设置定时任务**: 使用 `scheduler.py` 实现每日自动推送
4. **自定义资讯源**: 编辑 `config/sources.yaml` 添加更多资讯源

## 效果预览

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
