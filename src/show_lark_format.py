#!/usr/bin/env python3
"""
飞书日报格式展示 - 演示飞书推送的实际效果
"""

def show_lark_card_format():
    """展示飞书卡片的实际格式"""
    
    # 示例文章数据
    articles = [
        {
            "translated_title": "如何使用 Burp AI 加速 Repeater 中的漏洞验证",
            "source": "PortSwigger Blog",
            "category": "Web Security",
            "summary": "本文介绍了作者如何利用 Burp AI 工具显著加快了漏洞验证流程，提高了渗透测试效率。",
            "key_points": [
                "Burp AI 能够自动生成和验证 exploit 代码",
                "通过 AI 辅助减少了手动验证的时间",
                "实际测试中验证速度提升了 60%",
                "适用于常见的 Web 漏洞类型验证"
            ],
            "link": "https://portswigger.net/blog/how-i-sped-up-exploit-validation-in-repeater-using-burp-ai"
        },
        {
            "translated_title": "通过自动化代码审查提高应用安全性",
            "source": "Google Security Blog",
            "category": "SDL",
            "summary": "Google 分享了将自动化代码审查集成到开发流水线中，以尽早发现安全问题的方法。",
            "key_points": [
                "在 CI/CD 流水线中集成代码审查",
                "使用静态分析工具自动检测漏洞",
                "将安全左移到开发早期阶段",
                "显著减少安全债务"
            ],
            "link": "https://security.googleblog.com/2026/02/automated-code-review-security"
        },
        {
            "translated_title": "保护 LLM 免受提示注入攻击",
            "source": "OpenAI Security",
            "category": "AI Security",
            "summary": "OpenAI 讨论了保护大语言模型免受提示注入攻击和对抗输入的技术。",
            "key_points": [
                "识别提示注入攻击模式",
                "实施输入验证和过滤机制",
                "使用对抗训练提高模型鲁棒性",
                "监控和检测异常行为"
            ],
            "link": "https://openai.com/blog/prompt-injection-protection"
        }
    ]
    
    print("\n" + "="*80)
    print(" "*15 + "飞书日报推送格式展示")
    print("="*80 + "\n")
    
    # 展示 JSON 格式（实际发送的数据）
    print("【1】JSON 格式（实际发送到飞书的数据结构）\n")
    card_json = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "blue",
                "title": {
                    "content": "🛡️ SDL 安全日报",
                    "tag": "plain_text"
                },
                "subtitle": {
                    "content": f"今日精选 {len(articles)} 篇高质量文章",
                    "tag": "plain_text"
                }
            },
            "elements": build_card_elements(articles)
        }
    }
    
    import json
    print(json.dumps(card_json, ensure_ascii=False, indent=2))
    
    print("\n" + "="*80)
    print("【2】飞书 App 中的实际显示效果（模拟）\n")
    show_visual_format(articles)
    
    print("\n" + "="*80)
    print("【3】格式优化说明\n")
    show_optimization_tips()

def build_card_elements(articles):
    """构建卡片元素"""
    elements = []
    
    # 头部统计
    elements.extend([
        {
            "tag": "div",
            "text": {
                "content": f"📊 共爬取 150 篇文章 | 已为您推荐最相关的 {len(articles)} 篇",
                "tag": "lark_md"
            }
        },
        {"tag": "hr"}
    ])
    
    # 文章内容
    for i, article in enumerate(articles, 1):
        title = article.get('translated_title', '')
        source = article.get('source', 'N/A')
        category = article.get('category', 'N/A')
        summary = article.get('summary', '')
        key_points = article.get('key_points', [])
        link = article.get('link', '')
        
        elements.append({
            "tag": "div",
            "text": {
                "content": f"**{i}. {title}**",
                "tag": "lark_md"
            }
        })
        
        elements.append({
            "tag": "div",
            "fields": [
                {
                    "is_short": True,
                    "text": {
                        "content": f"📰 {source}",
                        "tag": "lark_md"
                    }
                },
                {
                    "is_short": True,
                    "text": {
                        "content": f"🏷️ {category}",
                        "tag": "lark_md"
                    }
                }
            ]
        })
        
        if summary:
            elements.append({
                "tag": "div",
                "text": {
                    "content": f"📝 {summary}",
                    "tag": "lark_md"
                }
            })
        
        if key_points:
            elements.append({
                "tag": "div",
                "text": {
                    "content": "🎯 **关键要点**",
                    "tag": "lark_md"
                }
            })
            
            for point in key_points[:4]:
                elements.append({
                    "tag": "div",
                    "text": {
                        "content": f"• {point}",
                        "tag": "lark_md"
                    }
                })
        
        if link:
            elements.append({
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "content": "🔗 查看原文",
                            "tag": "plain_text"
                        },
                        "type": "primary",
                        "url": link
                    }
                ]
            })
        
        if i < len(articles):
            elements.append({"tag": "hr"})
    
    # 底部
    elements.append({
        "tag": "div",
        "text": {
            "content": "✨ _由 SDL 安全文章爬取系统自动生成_",
            "tag": "lark_md"
        }
    })
    
    return elements

def show_visual_format(articles):
    """展示视觉格式"""
    border_line = "─" * 76
    
    for i, article in enumerate(articles, 1):
        title = article.get('translated_title', '')
        source = article.get('source', 'N/A')
        category = article.get('category', 'N/A')
        summary = article.get('summary', '')
        key_points = article.get('key_points', [])
        
        print(f"┌{'─'*75}┐")
        print(f"│ **{i}. {title}**")
        print(f"│ {border_line}")
        print(f"│ 📰 {source:<35}  🏷️ {category}")
        print(f"│")
        print(f"│ 📝 {summary}")
        print(f"│")
        if key_points:
            print(f"│ 🎯 **关键要点**")
            for point in key_points[:4]:
                print(f"│ • {point}")
        print(f"│")
        print(f"│ [ 🔗 查看原文 ]")
        print(f"└{'─'*75}┘")
        
        if i < len(articles):
            print()

def show_optimization_tips():
    """展示优化建议"""
    tips = [
        ("✅ 层次清晰", "使用不同的 emoji 和分隔线，信息层次分明"),
        ("✅ 视觉友好", "每篇文章控制在合理长度，避免信息过载"),
        ("✅ 交互便捷", "每篇文章都有醒目的'查看原文'按钮"),
        ("✅ 信息完整", "包含来源、分类、摘要、关键点等完整信息"),
        ("✅ 排版美观", "使用宽屏模式，适配不同设备"),
        ("✅ 响应式设计", "自动适配手机和桌面端显示"),
        ("✅ 表情丰富", "使用 emoji 增强可读性和趣味性"),
    ]
    
    for i, (title, desc) in enumerate(tips, 1):
        print(f"{i}. {title}")
        print(f"   {desc}")
    
    print("\n" + "="*80)
    print("对比：优化前 vs 优化后")
    print("="*80 + "\n")
    
    print("【优化前】")
    print("- 信息堆砌，没有层次")
    print("- 关键点使用缩进，不够醒目")
    print("- 分类标签混在文本中")
    print("- 没有来源标签，不易识别")
    print("- 按钮文字不够吸引")
    
    print("\n【优化后】")
    print("- 清晰的信息层次（标题、分类、摘要、关键点）")
    print("- 来源和分类使用独立的标签字段")
    print("- 关键点使用加粗标题")
    print("- 按钮使用 emoji，更加醒目")
    print("- 使用分隔线区分不同文章")
    print("- 底部添加系统标识，更专业")

if __name__ == '__main__':
    show_lark_card_format()
