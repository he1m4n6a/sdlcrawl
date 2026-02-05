# 代码下载和使用指南

## 项目信息

**项目名称**: SDL 安全文章爬取系统  
**分支**: 260205-feat-sdl-security-news-crawler  
**最新提交**: ff754db - feat: optimize Lark notification with Webhook and improved format

## 下载方式

### 方法 1: Git Clone（推荐）

```bash
git clone https://github.com/he1m4n6a/sdlcrawl.git
cd sdlcrawl
git checkout 260205-feat-sdl-security-news-crawler
```

### 方法 2: 下载 ZIP

1. 访问: https://github.com/he1m4n6a/sdlcrawl
2. 点击 "Code" 按钮
3. 选择 "Download ZIP"
4. 解压到本地目录

### 方法 3: 使用 GitHub CLI

```bash
gh repo clone he1m4n6a/sdlcrawl
cd sdlcrawl
gh checkout 260205-feat-sdl-security-news-crawler
```

## 项目结构

```
sdlcrawl/
├── config/
│   └── sources.yaml              # 资讯源配置（40+ 个源）
├── src/
│   ├── crawler/
│   │   ├── base_crawler.py      # 爬虫基类（支持中英文）
│   │   └── article_fetcher.py   # 文章获取器
│   ├── translator/
│   │   └── ai_translator.py     # AI 翻译器
│   ├── notifier/
│   │   └── lark_notifier.py     # 飞书通知器（Webhook）
│   ├── utils/
│   │   └── logger.py           # 日志工具
│   ├── data/                    # 保存的文章数据
│   ├── logs/                    # 日志文件
│   ├── main.py                  # 主程序
│   ├── simple_demo.py           # 简化演示版
│   ├── demo_with_translation.py  # 完整演示版
│   └── show_lark_format.py     # 飞书格式展示
├── scheduler.py                 # 定时调度器
├── requirements.txt              # Python 依赖
├── .env.example                # 环境变量示例
└── README.md                   # 项目说明
```

## 快速开始

### 1. 安装依赖

```bash
pip install --break-system-packages -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的配置
```

**必需配置**:
- `OPENAI_API_KEY` - OpenAI API 密钥
- `LARK_WEBHOOK_URL` - 飞书 Webhook URL

**可选配置**:
- `MAX_ARTICLES` - 推荐文章数量（默认 10）
- `CRAWL_HOUR` - 爬取时间（默认 9）

### 3. 运行程序

#### 查看飞书格式展示

```bash
cd src
python3 show_lark_format.py
```

#### 运行简化演示（无需 API）

```bash
cd src
python3 simple_demo.py
```

#### 运行完整程序（需要配置 API）

```bash
cd src
python3 main.py
```

#### 运行定时任务

```bash
python3 scheduler.py
```

## 飞书 Webhook 配置

详细配置步骤请查看：`LARK_WEBHOOK_GUIDE.md`

### 快速配置步骤

1. 访问飞书开放平台: https://open.feishu.cn/
2. 创建应用，获取 App ID 和 App Secret
3. 在"添加机器人"页面获取 Webhook URL
4. 在 `.env` 中配置 `LARK_WEBHOOK_URL`
5. 将机器人添加到接收消息的群组

### 配置示例

```env
# OpenAI API
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# Lark Webhook
LARK_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx
LARK_WEBHOOK_KEY=your_verification_key

# 爬取配置
MAX_ARTICLES=10
CRAWL_HOUR=9
```

## 飞书日报推送格式

### 实际效果

运行后会推送精美的飞书日报，包含：

1. **头部信息**
   - 🛡️ SDL 安全日报标题
   - 今日精选 X 篇高质量文章
   - 📊 爬取统计信息

2. **文章列表**（最多 10 篇）

每篇文章包含：
   - **序号和标题** - 加粗显示
   - **来源和分类** - 使用独立字段 + emoji
     - 📰 PortSwigger Blog
     - 🏷️ Web Security
   - **摘要** - 📝 emoji + 100-200 字摘要
   - **关键要点** - 🎯 加粗标题 + 列表
     • 关键点 1
     • 关键点 2
     • 关键点 3
   - **原文按钮** - 🔗 emoji + 醒目按钮

3. **底部信息**
   - ✨ 系统标识

### JSON 格式示例

实际发送到飞书的 JSON 数据格式请运行：

```bash
cd src
python3 show_lark_format.py
```

## 优化亮点

### 1. 使用 Webhook 替代 API

**优势**:
- ✅ 配置简单，无需复杂的认证
- ✅ 无需管理 Access Token
- ✅ 发送速度快
- ✅ 降低维护成本

### 2. 格式可读性提升

**优化对比**:

| 项目 | 优化前 | 优化后 |
|------|--------|--------|
| 配置方式 | API + Token | Webhook URL |
| 标题显示 | "1. 标题" | "**1. 标题**" + 加粗 |
| 来源显示 | 混在文本中 | 📰 emoji + 独立字段 |
| 分类显示 | 混在文本中 | 🏷️ emoji + 独立字段 |
| 摘要显示 | 普通文本 | 📝 emoji + 换行 |
| 关键点 | 缩进列表 | 🎯 加粗标题 + 列表 |
| 按钮 | "查看原文" | "🔗 查看原文" |
| 分隔线 | 无 | ─────────── |

### 3. 视觉元素

```python
EMOJI_MAP = {
    "title": "🛡️",      # 安全日报
    "stats": "📊",      # 统计
    "source": "📰",      # 来源
    "category": "🏷️",   # 分类
    "summary": "📝",      # 摘要
    "keypoints": "🎯",   # 关键点
    "link": "🔗",       # 链接
    "check": "✅",       # 成功
    "system": "✨",      # 系统
}
```

## 资讯源覆盖

### 国际安全源 (24 个)
- OWASP Blog, PortSwigger, The Hacker News, Krebs on Security
- Dark Reading, BleepingComputer, SecurityWeek, The Register, Threatpost
- Google Security, Microsoft Security, AWS Security, GitHub Security
- Google Project Zero, Microsoft Vulnerability Research
- AppSec Sentinel, NCC Group, Trail of Bits
- Intigriti, HackerOne, YesWeHack

### AI 安全源 (7 个)
- OpenAI Security, Anthropic Safety
- Google DeepMind Safety, Microsoft AI Safety
- AI Security Newsletter, Pwning AI, Hidden Layer

### 中国安全源 (24 个)
- 安全客, FreeBuf, 看雪论坛, 安全脉搏, 嘶吼, 黑客派
- 安全头条, 互联网安全
- 阿里云安全, 腾讯安全, 百度安全, 华为安全, 360 安全
- 奇安信, 绿盟科技, 安恒信息, 深信服
- 腾讯玄武实验室, 腾讯科恩实验室, 阿里安全研究
- 360 伏羲实验室, 长亭科技, 知道创宇
- 先知安全社区

## 关键词过滤

### 包含关键词

**英文**:
- SDL 相关: SDL, secure development, DevSecOps, appsec
- 安全工具: SAST, DAST, IAST, SCA, AST
- 威胁研究: vulnerability, zero-day, CVE, exploit, malware, ransomware
- AI 安全: AI security, LLM security, prompt injection, adversarial attack

**中文**:
- SDL: 安全开发, 应用安全, 漏洞分析, 漏洞挖掘
- 威胁情报: 威胁情报, 恶意代码, 勒索软件, 0day
- 其他: 安全研究, 攻防演练, 云安全, 网络安全

### 排除关键词
- advertisement, sponsored, 广告, 赞助, 推广

## 文档列表

- `README.md` - 项目说明和使用指南
- `LARK_WEBHOOK_GUIDE.md` - 飞书 Webhook 详细配置指南
- `LARK_FORMAT_OPTIMIZATION.md` - 飞书格式优化总结
- `RUN_OUTPUT.md` - 实际运行输出示例
- `PROJECT_SUMMARY.md` - 项目技术总结
- `FINAL_SUMMARY.md` - 完整版总结
- `ENHANCED_SOURCES.md` - 资讯源扩展说明
- `PUSH_GUIDE.md` - Git 推送指南
- `DOWNLOAD_GUIDE.md` - 本文件，下载和使用指南

## 测试运行

### 测试飞书格式展示

```bash
cd src
python3 show_lark_format.py
```

这将显示：
1. 实际发送到飞书的 JSON 格式
2. 飞书 App 中的显示效果（模拟）
3. 格式优化说明

### 测试简化版

```bash
cd src
python3 simple_demo.py
```

这将：
1. 爬取 10 篇文章
2. 保存到 JSON 文件
3. 在终端显示日报格式

## 故障排除

### Q: Webhook 推送失败

A: 
1. 检查 `LARK_WEBHOOK_URL` 是否正确
2. 确认机器人已添加到接收消息的群组
3. 查看日志: `src/logs/notifier_*.log`
4. 检查网络连接

### Q: OpenAI API 调用失败

A:
1. 检查 `OPENAI_API_KEY` 是否有效
2. 确认 API 余额是否充足
3. 查看日志: `src/logs/translator_*.log`
4. 检查网络连接

### Q: 爬取不到文章

A:
1. 检查网络连接
2. 查看日志: `src/logs/fetcher_*.log`
3. 某些源可能暂时无法访问
4. 可以在 `config/sources.yaml` 中禁用该源

## 下一步

1. **配置飞书 Webhook**
   - 参考 `LARK_WEBHOOK_GUIDE.md`
   - 配置 Webhook URL
   - 测试推送功能

2. **配置 OpenAI API**
   - 获取 API Key
   - 填入 `.env` 文件
   - 测试翻译功能

3. **运行系统**
   - 选择合适的运行方式
   - 配置定时任务
   - 持续接收每日日报

## 总结

SDL 安全文章爬取系统已经：
- ✅ 整合 40+ 个国内外安全资讯源
- ✅ 实现智能关键词过滤
- ✅ 支持中英文混合处理
- ✅ 优化飞书推送格式（Webhook + 精美卡片）
- ✅ 提供完整的文档和示例

你可以直接下载并使用，只需简单配置即可开始接收每日安全文章日报！

---

祝你使用愉快！如有问题，请参考项目文档或提交 Issue。
