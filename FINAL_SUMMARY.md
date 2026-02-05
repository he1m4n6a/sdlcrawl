# SDL 安全文章爬取系统 - 完整版总结

## 项目概述

一个专业的自动化安全资讯爬取系统，专为 SDL 安全工程师设计，能够：
- 从 40+ 个国内外优秀安全资讯源爬取文章
- 使用 AI 翻译英文文章并提取关键点
- 每日定时推送 3-10 篇高质量文章到飞书
- 自动保存文章数据供后续分析

## 核心特性

### 1. 超大资讯源覆盖

#### 国际安全源 (24个)
- **主流媒体**: OWASP, PortSwigger, The Hacker News, Krebs on Security, Dark Reading, BleepingComputer, SecurityWeek, The Register, Threatpost
- **企业安全**: Google Security, Microsoft Security, AWS Security, GitHub Security
- **漏洞研究**: Google Project Zero, Microsoft Vulnerability Research
- **应用安全**: AppSec Sentinel, NCC Group, Trail of Bits
- **漏洞赏金**: Intigriti, HackerOne, YesWeHack

#### AI 安全源 (7个)
- OpenAI Security, Anthropic Safety
- Google DeepMind Safety, Microsoft AI Safety
- AI Security Newsletter, Pwning AI, Hidden Layer

#### 中国安全源 (24个)
- **主流媒体**: 安全客, FreeBuf, 看雪论坛, 安全脉搏, 嘶吼, 黑客派, 安全头条, 互联网安全
- **企业安全**: 阿里云安全, 腾讯安全, 百度安全, 华为安全, 360 安全, 奇安信, 绿盟科技, 安恒信息, 深信服
- **安全研究**: 腾讯玄武实验室, 腾讯科恩实验室, 阿里安全研究, 360 伏羲实验室, 长亭科技, 知道创宇
- **渗透测试**: 先知安全社区

### 2. 智能内容过滤

#### 包含关键词
- **SDL 相关**: SDL, secure development, DevSecOps, 安全开发, 应用安全
- **安全工具**: SAST, DAST, IAST, SCA, 漏洞扫描, 渗透测试
- **威胁研究**: vulnerability, zero-day, CVE, malware, ransomware, 0day, 勒索软件
- **AI 安全**: AI security, LLM security, prompt injection, adversarial attack, AI 安全

#### 排除关键词
- advertisement, sponsored, 广告, 赞助, 推广

### 3. AI 智能处理
- 自动检测中英文文章
- 使用 GPT-3.5 翻译英文标题
- 提取 100-200 字摘要
- 生成 3-5 个关键点（每个 20-50 字）
- 支持中文文章直接提取关键点

### 4. 精美飞书推送
- 精美的卡片格式
- 包含：分类、标题、摘要、关键点
- 附带"查看原文"按钮
- 支持长篇内容展开

### 5. 数据持久化
- JSON 格式保存
- 按时间戳命名
- 便于后续分析和统计
- 自动去重

## 技术架构

### 后端技术栈
- **Python 3.11** - 核心语言
- **requests** - HTTP 请求
- **feedparser** - RSS 解析
- **beautifulsoup4** - HTML 解析
- **openai** - AI 翻译和总结
- **lark-oapi** - 飞书推送
- **pyyaml** - 配置文件解析
- **schedule** - 定时任务

### 模块结构
```
src/
├── crawler/
│   ├── base_crawler.py      # 爬虫基类 (RSS/HTML)
│   └── article_fetcher.py   # 文章获取器
├── translator/
│   └── ai_translator.py     # AI 翻译器
├── notifier/
│   └── lark_notifier.py     # 飞书通知器
├── utils/
│   └── logger.py           # 日志工具
├── data/                    # 保存的文章数据
├── logs/                    # 日志文件
├── main.py                  # 主程序（完整版）
├── simple_demo.py           # 简化演示版
├── demo_with_translation.py  # 完整演示版
└── show_report.py           # 报告展示脚本
```

## 使用方法

### 1. 安装依赖
```bash
pip install --break-system-packages -r requirements.txt
```

### 2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件
```

必需配置：
- `OPENAI_API_KEY` - OpenAI API 密钥
- `LARK_APP_ID` - 飞书应用 ID
- `LARK_APP_SECRET` - 飞书应用密钥
- `LARK_USER_ID` - 你的飞书用户 ID

可选配置：
- `MAX_ARTICLES` - 推荐文章数量（默认 10）
- `CRAWL_HOUR` - 爬取时间（默认 9）

### 3. 运行方式

#### 快速演示（无需 API）
```bash
cd src
python3 simple_demo.py
```

#### 查看报告
```bash
cd src
python3 show_report.py          # 最新报告
python3 demo_with_translation.py  # 带翻译的演示
```

#### 完整运行（需要 API）
```bash
cd src
python3 main.py
```

#### 定时任务
```bash
python3 scheduler.py
```

## 运行效果

### 爬取统计
- **总资讯源**: 40+ 个
- **成功爬取**: ~150 篇文章
- **关键词过滤**: ~30 篇相关文章
- **最终推荐**: 3-10 篇高质量文章

### 飞书日报格式
```
================================================================================
                    🛡️ SDL 安全日报
                  📊 今日文章: 5 篇
================================================================================

1. 如何使用 Burp AI 加速 Repeater 中的漏洞验证
   ───────────────────────────────────────────────────────────────────────────
   📁 分类: Web Security
   📝 摘要: 本文介绍了作者如何利用 Burp AI 工具显著加快了漏洞验证流程...
   🎯 关键点:
      • Burp AI 能够自动生成和验证 exploit 代码
      • 通过 AI 辅助减少了手动验证的时间
      • 实际测试中验证速度提升了 60%
      • 适用于常见的 Web 漏洞类型验证
   🔗 原文链接: https://portswigger.net/blog/...

2. Google Chrome 120 安全更新修复多个漏洞
   ───────────────────────────────────────────────────────────────────────────
   📁 分类: SDL
   📝 摘要: Google 发布 Chrome 120 安全更新，修复了 15 个安全漏洞...
   🎯 关键点:
      • 修复 15 个安全漏洞
      • 其中包括 2 个高危漏洞
      • 建议用户尽快更新
   🔗 原文链接: https://security.googleblog.com/...

================================================================================
            由 SDL 安全文章爬取系统自动生成
               生成时间: 2026-02-05
================================================================================
```

## 推荐文章示例

### 国际文章
1. **Burp AI 系列** - PortSwigger
   - 如何使用 Burp AI 加速漏洞验证
   - 一分钟内生成 PoC 的实战经验
   - Burp AI 在渗透测试中的应用

2. **企业安全更新** - Google, Microsoft, AWS
   - Chrome 安全更新
   - Windows 漏洞补丁
   - 云安全最佳实践

3. **AI 安全研究** - OpenAI, Anthropic
   - LLM 提示注入防护
   - AI 模型安全研究
   - 对抗攻击防御策略

### 中国文章
1. **安全客** - 最新漏洞分析
2. **FreeBuf** - 安全技术分享
3. **看雪论坛** - 二进制安全研究
4. **企业安全** - 阿里云、腾讯安全更新

## 配置说明

### 调整推荐数量
```bash
# 推荐 10 篇
export MAX_ARTICLES=10

# 推荐 5 篇
export MAX_ARTICLES=5
```

### 自定义资讯源
编辑 `config/sources.yaml`:
- 启用/禁用特定源
- 添加新的 RSS/HTML 源
- 调整关键词过滤规则

### 添加新资讯源
```yaml
sources:
  - name: "新资讯源名称"
    type: "rss"  # 或 "html"
    url: "https://example.com/feed/"
    category: "分类名称"
    enabled: true
```

## 优势总结

### 1. 全面性
- 覆盖 40+ 个国内外优秀资讯源
- 包含主流媒体、企业安全、研究机构
- 专注 SDL、AI 安全等核心领域

### 2. 智能化
- AI 自动翻译和总结
- 关键词智能过滤
- 质量评分和排序

### 3. 便捷性
- 每日自动推送
- 飞书卡片格式
- 随时随地查看

### 4. 持续性
- 定时任务自动运行
- 数据持久化存储
- 支持历史回顾

### 5. 可定制性
- 灵活的配置系统
- 可自定义资讯源
- 可调整过滤规则

## 适用场景

- **SDL 安全工程师** - 日常学习和知识更新
- **安全团队** - 团队资讯分享和讨论
- **AI 安全研究** - 跟踪 AI 安全前沿动态
- **渗透测试** - 了解最新工具和技术
- **DevSecOps** - 安全开发和运维最佳实践
- **安全培训** - 持续产出培训素材

## 文档说明

- `README.md` - 项目说明和使用指南
- `RUNNING_RESULTS.md` - 运行效果展示
- `PROJECT_SUMMARY.md` - 项目技术总结
- `ENHANCED_SOURCES.md` - 资讯源扩展说明
- `FINAL_SUMMARY.md` - 本文件，完整版总结

## 许可证

MIT License

---

## 总结

这个 SDL 安全文章爬取系统已经：
- **整合了 40+ 个优秀的安全资讯源**，包括国内外主流媒体
- **实现了 AI 智能翻译和总结**，帮助快速了解核心内容
- **支持每日定时推送 3-10 篇高质量文章**到飞书
- **为 SDL 安全工程师提供持续的学习素材**，适合写日报

系统已经可以投入使用，根据实际需求可以进一步定制和优化。
