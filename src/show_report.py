#!/usr/bin/env python3
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def display_report(articles):
    """显示日报内容（模拟飞书卡片格式）"""
    
    print("\n" + "="*80)
    print(" " * 25 + "SDL 安全日报")
    print(" " * 20 + f"（共 {len(articles)} 篇）")
    print("="*80 + "\n")
    
    for i, article in enumerate(articles, 1):
        title = article.get('title', 'N/A')
        link = article.get('link', 'N/A')
        category = article.get('category', 'N/A')
        content = article.get('content', 'N/A')
        
        print(f"\n{i}. {title}")
        print(f"   {'─'*70}")
        print(f"   📁 分类: {category}")
        print(f"   📝 摘要: {content[:150]}...")
        print(f"   🔗 原文链接: {link}")
        
        if i < len(articles):
            print()
    
    print("\n" + "="*80)
    print(" " * 15 + "由 SDL 安全文章爬取系统自动生成")
    print("="*80 + "\n")

if __name__ == '__main__':
    # 读取最新的数据文件
    data_dir = "data"
    files = sorted([f for f in os.listdir(data_dir) if f.startswith('articles_') and f.endswith('.json')])
    
    if not files:
        print("没有找到数据文件")
        sys.exit(1)
    
    latest_file = os.path.join(data_dir, files[-1])
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    display_report(articles)
