# 飞书 Webhook 配置指南

## 配置步骤

### 1. 创建飞书机器人

1. 访问飞书开放平台: https://open.feishu.cn/
2. 点击"创建应用"
3. 填写应用信息：
   - **应用名称**: SDL 安全日报机器人
   - **应用描述**: 自动推送每日安全文章日报
   - **应用图标**: 上传安全相关的图标

### 2. 配置机器人权限

在"权限管理"页面，申请以下权限：

#### 必需权限
- `im:message` - 发送消息权限
- `im:message:group_at_msg` - 发送群组消息（如果需要发送到群）

### 3. 创建 Webhook

在"事件订阅"页面：

1. 点击"添加事件"
2. 选择订阅事件（可选，用于接收回调）:
   - 应用启用
   - 机器人加入群组
3. 点击"添加请求"配置 Webhook URL

#### Webhook URL 配置

如果你有服务器，可以配置 Webhook URL 来接收飞书的回调：
- 你的服务器 URL: `https://your-server.com/webhook`
- 验证 Token: 自定义验证密钥

### 4. 获取 Webhook URL（用于发送消息）

#### 方式 1: 使用飞书提供的 Webhook URL

1. 在飞书开放平台，找到你的应用
2. 进入"添加机器人"页面
3. 选择接收机器人的群组或个人
4. 系统会生成一个 Webhook URL，格式类似：
   ```
   https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx
   ```

#### 方式 2: 直接通过 API 发送（本系统使用的方式）

系统使用 Webhook URL 直接发送消息，无需订阅事件。配置方式：

**步骤**:
1. 在飞书开放平台找到你的应用
2. 复制 App ID 和 App Secret
3. 如果系统需要 Webhook URL，可以使用以下格式：
   ```
   https://open.feishu.cn/open-apis/bot/v2/hook/your-app-id
   ```

### 5. 配置环境变量

在 `.env` 文件中配置：

```env
# OpenAI API 配置
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# Lark Webhook 配置
LARK_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx
LARK_WEBHOOK_KEY=your_verification_key_here  # 可选

# 爬取配置
CRAWL_HOUR=9
MAX_ARTICLES=10
```

### 6. 将机器人添加到飞书

1. 在飞书 App 中找到"机器人"
2. 搜索你的机器人名称（"SDL 安全日报机器人"）
3. 点击"添加"
4. 选择接收机器人消息的群组或个人

### 7. 验证配置

运行系统测试：

```bash
cd src
python3 main.py
```

如果配置正确，你应该会在飞书中收到精美的日报消息。

## Webhook vs API 对比

### Webhook 方式（本系统）

**优点**:
- ✅ 配置简单，无需复杂的认证
- ✅ 发送速度快
- ✅ 不需要管理 Token 过期
- ✅ 适合自动化推送

**缺点**:
- ⚠️ 无法获取机器人消息发送状态
- ⚠️ 依赖 URL 不被泄露

### API 方式

**优点**:
- ✅ 可以获取发送状态和错误信息
- ✅ 支持更复杂的交互
- ✅ 更安全（需要认证）

**缺点**:
- ❌ 需要管理 Access Token
- ❌ Token 有过期时间，需要刷新
- ❌ 配置相对复杂

## 推送格式示例

### 飞书卡片效果

```
┌─────────────────────────────────────────┐
│  🛡️ SDL 安全日报                    │
│  今日精选 10 篇高质量文章        │
├─────────────────────────────────────────┤
│  📰 共爬取 150 篇文章              │
│  已为您推荐最相关的 10 篇           │
├─────────────────────────────────────────┤
│                                     │
│  **1. 如何使用 Burp AI 加速**       │
│  Repeater 中的漏洞验证               │
│  ─────────────────────────────         │
│  📰 PortSwigger                    │
│  🏷️ Web Security                   │
│                                     │
│  📝 本文介绍了作者如何利用 Burp AI   │
│  工具显著加快了漏洞验证流程，提高    │
│  了渗透测试效率。                   │
│                                     │
│  🎯 **关键要点**                   │
│  • Burp AI 能够自动生成和验证     │
│    exploit 代码                      │
│  • 通过 AI 辅助减少了手动验证    │
│    的时间                            │
│  • 实际测试中验证速度提升了 60%   │
│  • 适用于常见的 Web 漏洞类型验证  │
│                                     │
│  [ 🔗 查看原文 ]                    │
│                                     │
│  ─────────────────────────────         │
│                                     │
│  **2. 通过自动化代码审查提高**       │
│  应用安全性                           │
│  ─────────────────────────────         │
│  [ ... 其他文章 ... ]               │
│                                     │
├─────────────────────────────────────────┤
│  ✨ 由 SDL 安全文章爬取系统自动生成  │
└─────────────────────────────────────────┘
```

### 详细信息展示

每篇文章包含以下信息：

1. **序号和标题** - 清晰的文章编号和标题
2. **来源标签** - 📰 PortSwigger、📰 Google Security
3. **分类标签** - 🏷️ Web Security、🏷️ SDL、🏷️ AI Security
4. **摘要** - 📝 100-200 字的文章摘要
5. **关键要点** - 🎯 3-4 个关键点（使用列表格式）
6. **原文按钮** - 🔗 一键跳转到原文

### 优势特点

#### 1. 视觉层次清晰
- 使用不同的 emoji 区分不同类型的信息
- 使用分隔线区分文章
- 使用加粗突出标题和关键信息

#### 2. 信息密度适中
- 不会太长导致疲劳
- 每篇文章控制在 8-10 行
- 最多推荐 10 篇文章

#### 3. 交互友好
- 每篇文章都有"查看原文"按钮
- 按钮使用醒目的主色调（primary）
- 点击后直接跳转到原文链接

#### 4. 响应式设计
- 宽屏模式（wide_screen_mode）支持
- 适配不同屏幕尺寸
- 自动调整排版

## 测试命令

### 测试 Webhook 配置

```bash
cd src

# 测试空报告
python3 << PYEOF
from notifier.lark_notifier import LarkNotifier
notifier = LarkNotifier()
notifier.send_daily_report([])
PYEOF

# 测试单篇文章
python3 << PYEOF
from notifier.lark_notifier import LarkNotifier
article = {
    "translated_title": "测试文章标题",
    "source": "测试来源",
    "category": "测试分类",
    "summary": "这是一篇测试文章的摘要内容。",
    "key_points": ["关键点1", "关键点2", "关键点3"],
    "link": "https://example.com"
}
notifier = LarkNotifier()
notifier.send_daily_report([article])
PYEOF
```

### 测试完整日报

```bash
cd src
MAX_ARTICLES=3 python3 main.py
```

## 常见问题

### Q: Webhook URL 在哪里找到？
A: 
1. 在飞书开放平台找到你的应用
2. 进入"添加机器人"页面
3. 选择接收机器人的群组
4. 系统会显示 Webhook URL

### Q: 推送失败怎么办？
A:
1. 检查 Webhook URL 是否正确
2. 确认机器人已添加到接收消息的群组
3. 查看系统日志: `src/logs/notifier_*.log`
4. 确认网络连接正常

### Q: 如何修改推送时间？
A:
修改 `.env` 文件中的 `CRAWL_HOUR` 变量：
```env
CRAWL_HOUR=9  # 早上 9 点
```

### Q: 如何调整推荐文章数量？
A:
修改 `.env` 文件中的 `MAX_ARTICLES` 变量：
```env
MAX_ARTICLES=5  # 推荐 5 篇
```

### Q: 能否发送到多个群组？
A:
可以，配置多个 Webhook URL 或者在 `_send_webhook` 方法中循环发送：
```python
webhook_urls = [
    "https://open.feishu.cn/open-apis/bot/v2/hook/...",
    "https://open.feishu.cn/open-apis/bot/v2/hook/..."
]
for url in webhook_urls:
    self._send_webhook(card_content, url)
```

## 安全建议

1. **保护 Webhook URL**
   - 不要将 Webhook URL 提交到公开代码仓库
   - 使用环境变量或配置文件存储
   - 定期轮换 Webhook URL

2. **使用验证密钥**
   - 设置 `LARK_WEBHOOK_KEY` 验证请求来源
   - 在飞书 Webhook 配置中设置相同的验证密钥

3. **限制消息频率**
   - 避免频繁发送消息打扰用户
   - 设置合理的推送时间（如早上 9 点）
   - 提供免打扰模式

## 下一步优化

1. **添加交互功能**
   - 支持"已读"标记
   - 添加"收藏"按钮
   - 支持"分享"功能

2. **个性化推荐**
   - 基于用户阅读历史推荐
   - 支持用户设置感兴趣的分类
   - 记录用户阅读偏好

3. **数据分析**
   - 统计文章点击率
   - 分析用户阅读时长
   - 生成阅读习惯报告

---

如有问题，请参考飞书开放平台文档：
- Webhook 配置: https://open.feishu.cn/document/common-capabilities/message-card/construct-json/using-webhook
- 卡片消息: https://open.feishu.cn/document/common-capabilities/message-card/construct-json/
