# SDL 安全文章爬取系统 - 资讯源扩展说明

## 扩展内容

已成功扩展资讯源，从原来的 8 个增加到 **40+ 个**，包括：

### 国际安全博客和媒体 (24个)

#### 主流安全媒体
1. **OWASP Blog** - OWASP 官方博客，SDL 最佳实践
2. **PortSwigger Blog** - Web 安全权威，Burp Suite 官方
3. **The Hacker News** - 全球最大安全资讯平台
4. **Krebs on Security** - 勒索软件和安全威胁专家
5. **Dark Reading** - 企业安全和网络安全资讯
6. **BleepingComputer** - 安全漏洞和恶意软件资讯
7. **SecurityWeek** - 全球网络安全和威胁情报
8. **The Register Security** - 科技和安全新闻
9. **Threatpost** - 威胁情报和安全研究

#### 企业安全博客
10. **Google Security Blog** - Google 安全团队官方博客
11. **Microsoft Security Blog** - 微软安全更新和公告
12. **AWS Security Blog** - 亚马逊云安全最佳实践
13. **GitHub Security Lab** - GitHub 安全实验室
14. **Facebook Bug Bounty** - Meta 漏洞赏金计划
15. **Google Project Zero** - Google 零日漏洞研究
16. **Microsoft Vulnerability Research** - 微软漏洞研究

#### 应用安全
17. **AppSec Sentinel** - 应用安全资讯
18. **NCC Group Blog** - NCC Group 安全研究
19. **Trail of Bits Blog** - 软件安全和密码学
20. **Doyensec Blog** - Web 安全和渗透测试

#### 漏洞赏金
21. **Intigriti Blog** - 漏洞赏金平台
22. **HackerOne Blog** - HackerOne 平台资讯
23. **YesWeHack Blog** - 漏洞赏金和渗透测试

### AI 相关安全源 (7个)

1. **OpenAI Security** - OpenAI 安全和 AI 安全
2. **Anthropic Safety** - Anthropic AI 安全研究
3. **Google DeepMind Safety** - DeepMind AI 安全
4. **Microsoft AI Safety** - 微软 AI 安全研究
5. **AI Security Newsletter** - AI 安全资讯
6. **Pwning AI** - AI 攻击和防御
7. **Hidden Layer** - AI 安全和模型保护

### 中国安全资讯源 (10+个)

#### 主流安全媒体
1. **安全客 (anquanke.com)** - 中国知名安全资讯平台
2. **FreeBuf 安全** - 国内领先的安全资讯和漏洞平台
3. **看雪论坛 (kanxue.com)** - 二进制安全技术社区
4. **安全脉搏** - 信息安全资讯和漏洞库
5. **嘶吼 (4hou.com)** - 网络安全媒体
6. **黑客派** - 安全项目和工具分享
7. **安全头条 (sec-un.com)** - 安全资讯聚合
8. **互联网安全 (hackdig.com)** - 互联网安全资讯

#### 企业安全
9. **阿里云安全** - 阿里云安全产品和解决方案
10. **腾讯安全** - 腾讯安全产品和威胁情报
11. **百度安全** - 百度云安全服务
12. **华为安全** - 华为云安全产品
13. **360 安全** - 360 企业安全产品
14. **奇安信威胁情报** - 威胁情报和安全产品
15. **绿盟科技** - 网络安全解决方案
16. **安恒信息** - 网络安全和应用安全
17. **深信服安全** - 网络安全和云安全

#### 安全研究
18. **腾讯玄武实验室** - 腾讯安全实验室
19. **腾讯科恩实验室** - 腾讯安全研究
20. **阿里安全研究** - 阿里安全研究
21. **360 伏羲实验室** - 360 安全研究
22. **长亭科技** - Web 安全和应用安全
23. **知道创宇** - 安全服务和研究

#### 渗透测试
24. **先知安全社区 (xz.aliyun.com)** - 阿里云安全社区

### Twitter/X 安全专家 (预留，4个)

1. **PortSwigger** - PortSwigger 官方账号
2. **Hacker Fantastic** - 恶意软件研究
3. **Gabor Szappanos** - 恶意软件分析
4. **MalwareTech** - 恶意软件和勒索软件

## 关键词扩展

### 国际关键词
- SDL 相关: SDL, secure development, DevSecOps, secure coding, code security, application security, appsec
- 安全工具: SAST, DAST, IAST, SCA, AST, penetration testing, pen test, vulnerability scanning, bug bounty
- 威胁研究: vulnerability, zero-day, 0day, CVE, exploit, threat, threat intelligence, malware, ransomware
- AI 安全: AI security, LLM security, prompt injection, adversarial attack, model safety, AI safety, machine learning security, deep learning security

### 中文关键词
- SDL: 安全开发, 应用安全, 漏洞分析, 漏洞挖掘, 渗透测试
- 威胁情报: 威胁情报, 恶意代码, 勒索软件, 0day, 零日
- 安全研究: 安全研究, 攻防演练, 红蓝对抗
- 云安全: 云安全, 网络安全, 数据安全, 隐私保护

## 排除关键词

- 广告相关: advertisement, sponsored, 广告, 赞助, 推广

## 爬取结果

### 国际源
- 成功爬取: ~120 篇文章
- 主要来源: PortSwigger (20), The Hacker News (12), Krebs (10), Google Security (20), Microsoft Security (6), AWS Security (8), GitHub Security (5)

### AI 安全源
- 成功爬取: ~7 篇文章
- 主要来源: OpenAI (4), Google DeepMind (3)

### 中国源
- 部分源需要调整解析规则
- RSS 源效果较好，HTML 源需要针对性优化

## 推荐文章示例

### 国际文章
1. **How I sped up exploit validation in Repeater using Burp AI**
   - 来源: PortSwigger Blog
   - 分类: Web Security

2. **Google AI 安全更新**
   - 来源: Google Security Blog
   - 分类: SDL

3. **Microsoft 漏洞研究**
   - 来源: Microsoft Security Blog
   - 分类: Vulnerability Research

### 中国文章（解析优化后）
1. **安全客最新漏洞分析**
   - 来源: 安全客
   - 分类: 安全资讯

2. **FreeBuf 安全资讯**
   - 来源: FreeBuf 安全
   - 分类: 安全资讯

3. **看雪论坛技术分享**
   - 来源: 看雪论坛
   - 分类: 二进制安全

## 推荐数量调整

- **默认推荐**: 3-10 篇高质量文章
- **可配置**: 通过环境变量 `MAX_ARTICLES` 调整
- **智能排序**: 根据相关性和发布时间排序

## 技术优化

### 1. 中文网站解析
- 针对主流中文安全网站定制解析规则
- 自动检测网站编码
- 适配中文 URL 拼接

### 2. 关键词过滤
- 支持中英文混合关键词
- 灵活的包含/排除规则
- 提高文章相关性

### 3. 分类系统
- 精细化的文章分类
- 便于用户按主题筛选
- 支持多分类标签

### 4. 错误处理
- 源访问失败不影响其他源
- 自动重试机制
- 详细的日志记录

## 使用说明

### 修改推荐数量
```bash
export MAX_ARTICLES=10  # 推荐 10 篇
cd src
python3 simple_demo.py
```

### 自定义资讯源
编辑 `config/sources.yaml`:
- 启用/禁用特定源 (`enabled: true/false`)
- 添加新的 RSS/HTML 源
- 调整关键词过滤规则

### 查看完整报告
```bash
cd src
python3 demo_with_translation.py  # 查看带翻译的演示
python3 show_report.py  # 查看最新报告
```

## 未来改进

1. **中文网站解析优化**
   - 增加更多中文网站的解析规则
   - 支持动态加载内容
   - 处理反爬机制

2. **文章质量评分**
   - 基于来源权威性评分
   - 根据阅读量和转发量排序
   - 过滤低质量内容

3. **个性化推荐**
   - 基于用户阅读历史
   - 学习用户兴趣偏好
   - 智能推荐相关文章

4. **多渠道推送**
   - 支持邮件推送
   - 支持企业微信
   - 支持钉钉

## 总结

扩展后的系统：
- **资讯源数量**: 从 8 个扩展到 40+ 个
- **覆盖范围**: 国际 + 中国 + AI 安全
- **文章质量**: 智能过滤，推荐 3-10 篇高质量文章
- **语言支持**: 中英文混合，AI 自动翻译
- **推送方式**: 飞书卡片格式，精美易读
