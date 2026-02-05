#!/usr/bin/env python3
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 模拟 AI 翻译结果
demo_articles = [
    {
        "source": "PortSwigger Blog",
        "category": "Web Security",
        "title": "How I sped up exploit validation in Repeater using Burp AI",
        "link": "https://portswigger.net/blog/how-i-sped-up-exploit-validation-in-repeater-using-burp-ai",
        "published": "Thu, 22 Jan 2026 15:18:00 GMT",
        "translated_title": "如何使用 Burp AI 加速 Repeater 中的漏洞验证",
        "summary": "本文介绍了作者如何利用 Burp AI 工具显著加快了漏洞验证流程，提高了渗透测试效率。",
        "key_points": [
            "Burp AI 能够自动生成和验证 exploit 代码",
            "通过 AI 辅助减少了手动验证的时间",
            "实际测试中验证速度提升了 60%",
            "适用于常见的 Web 漏洞类型验证"
        ]
    },
    {
        "source": "PortSwigger Blog",
        "category": "Web Security",
        "title": "Functional PoCs in less than a minute? Julen Garrido Estévez puts Burp AI to the test",
        "link": "https://portswigger.net/blog/functional-pocs-in-less-than-a-minute",
        "published": "Fri, 16 Jan 2026 00:00:00 GMT",
        "translated_title": "一分钟内生成可用的 PoC？Julen Garrido Estévez 测试 Burp AI",
        "summary": "渗透测试员分享了使用 Burp AI 快速生成功能验证代码的测试结果和经验。",
        "key_points": [
            "Burp AI 在特定场景下可在 30 秒内生成 PoC",
            "测试成功率达 75% 以上",
            "提供了优化的提示词模板",
            "分享了对 AI 工具的实用建议"
        ]
    },
    {
        "source": "PortSwigger Blog",
        "category": "Web Security",
        "title": "DAST without disruption: Burp Suite DAST winter update 2025",
        "link": "https://portswigger.net/blog/burp-suite-dast-winter-update-2025",
        "published": "Thu, 11 Dec 2025 13:09:30 GMT",
        "summary": "Burp Suite DAST 发布冬季更新，新增无干扰扫描功能，提高了对生产环境的友好性。",
        "key_points": [
            "新增无干扰扫描模式",
            "改进了 API 资产发现能力",
            "优化了认证处理机制",
            "支持更灵活的扫描窗口配置"
        ]
    }
]

def display_report(articles):
    """显示日报内容（完整版，带翻译和关键点）"""
    
    print("\n" + "="*80)
    print(" " * 20 + "🛡️ SDL 安全日报")
    print(" " * 18 + f"📊 今日文章: {len(articles)} 篇")
    print("="*80 + "\n")
    
    for i, article in enumerate(articles, 1):
        title = article.get('translated_title', article.get('title', 'N/A'))
        link = article.get('link', 'N/A')
        category = article.get('category', 'N/A')
        summary = article.get('summary', '')
        key_points = article.get('key_points', [])
        
        print(f"\n{i}. {title}")
        print(f"   {'─'*75}")
        
        if category:
            print(f"   📁 分类: {category}")
        
        if summary:
            print(f"   📝 摘要: {summary}")
        
        if key_points:
            print(f"   🎯 关键点:")
            for point in key_points:
                print(f"      • {point}")
        
        print(f"   🔗 原文链接: {link}")
        
        if i < len(articles):
            print()
    
    print("\n" + "="*80)
    print(" " * 12 + "由 SDL 安全文章爬取系统自动生成")
    print(" " * 15 + f"生成时间: {articles[0].get('published', 'N/A')}")
    print("="*80 + "\n")

if __name__ == '__main__':
    display_report(demo_articles)
