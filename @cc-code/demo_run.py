#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
立即开始使用 - 简化演示版本
"""

import os
import sys
import json
from datetime import datetime
from collections import Counter
import re

def show_banner():
    print("=" * 50)
    print("  立即开始使用 - 评论分析系统演示")
    print("=" * 50)
    print()

def analyze_demo_data():
    """分析演示数据"""
    demo_file = 'data/demo_comments.json'

    if not os.path.exists(demo_file):
        print("错误: 演示数据文件不存在")
        return

    print("正在分析演示数据...")
    print()

    # 读取数据
    with open(demo_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    comments = data.get('comments', [])
    metadata = data.get('metadata', {})

    # 基础统计
    total_comments = len(comments)
    ratings = [c.get('rating', 0) for c in comments if c.get('rating')]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0

    print("【基础统计】")
    print(f"总评论数: {total_comments}")
    print(f"平均评分: {avg_rating:.2f}")
    print(f"隐私保护: {metadata.get('privacy_protected', '未知')}")
    print(f"数据匿名化: {metadata.get('anonymized', '未知')}")
    print()

    # 评论内容分析
    all_content = []
    all_tags = []

    for comment in comments:
        content = comment.get('content', '')
        tags = comment.get('tags', [])
        all_content.append(content)
        all_tags.extend(tags)

    # 提取关键词（简单版）
    words = []
    for content in all_content:
        # 提取中文词汇
        chinese_words = re.findall(r'[\u4e00-\u9fa5]{2,}', content)
        words.extend(chinese_words)

    word_freq = Counter(words)
    tag_freq = Counter(all_tags)

    print("【高频词汇】")
    for word, count in word_freq.most_common(8):
        print(f"{word}: {count}次")
    print()

    print("【用户标签】")
    for tag, count in tag_freq.most_common(6):
        print(f"{tag}: {count}次")
    print()

    # 简单情感分析
    positive_keywords = ['好', '不错', '推荐', '新鲜', '值得', '正宗']
    neutral_keywords = ['一般', '还行', '可以']
    negative_keywords = ['贵', '长', '差', '慢']

    sentiment_scores = {'positive': 0, 'neutral': 0, 'negative': 0}

    for content in all_content:
        for word in positive_keywords:
            if word in content:
                sentiment_scores['positive'] += 1
        for word in neutral_keywords:
            if word in content:
                sentiment_scores['neutral'] += 1
        for word in negative_keywords:
            if word in content:
                sentiment_scores['negative'] += 1

    total_sentiment = sum(sentiment_scores.values())
    if total_sentiment > 0:
        print("【情感分析】")
        for sentiment, count in sentiment_scores.items():
            percentage = count / total_sentiment * 100
            sentiment_name = {'positive': '正面', 'neutral': '中性', 'negative': '负面'}[sentiment]
            print(f"{sentiment_name}: {percentage:.1f}% ({count}个指标)")
    print()

    # 保存分析结果
    analysis_result = {
        'timestamp': datetime.now().isoformat(),
        'basic_stats': {
            'total_comments': total_comments,
            'average_rating': round(avg_rating, 2),
            'privacy_protected': metadata.get('privacy_protected', False)
        },
        'keywords': list(word_freq.most_common(10)),
        'tags': list(tag_freq.most_common(10)),
        'sentiment_analysis': sentiment_scores,
        'demo_analysis': True
    }

    # 保存到文件
    result_file = 'data/demo_analysis_result.json'
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, ensure_ascii=False, indent=2)

    print(f"分析结果已保存到: {result_file}")
    print()

    return analysis_result

def create_wordcloud_data():
    """创建词云数据"""
    print("正在生成词云数据...")
    print()

    # 读取分析结果
    try:
        with open('data/demo_analysis_result.json', 'r', encoding='utf-8') as f:
            analysis = json.load(f)
    except FileNotFoundError:
        print("请先运行分析功能")
        return

    # 生成词云数据
    keywords = analysis.get('keywords', [])
    tags = analysis.get('tags', [])

    # 合并关键词和标签
    wordcloud_items = []

    # 添加关键词
    for word, freq in keywords:
        wordcloud_items.append({
            'text': word,
            'size': freq * 8 + 16,  # 字体大小
            'frequency': freq,
            'type': 'keyword'
        })

    # 添加标签
    for tag, freq in tags:
        if tag not in [item['text'] for item in wordcloud_items]:  # 避免重复
            wordcloud_items.append({
                'text': tag,
                'size': freq * 6 + 14,
                'frequency': freq,
                'type': 'tag'
            })

    # 保存词云数据
    wordcloud_data = {
        'timestamp': datetime.now().isoformat(),
        'words': wordcloud_items,
        'max_size': max([item['size'] for item in wordcloud_items]) if wordcloud_items else 0,
        'total_words': len(wordcloud_items)
    }

    wordcloud_file = 'data/wordcloud_data.json'
    with open(wordcloud_file, 'w', encoding='utf-8') as f:
        json.dump(wordcloud_data, f, ensure_ascii=False, indent=2)

    print("【词云数据】")
    for item in wordcloud_items[:10]:
        print(f"{item['text']}: 大小{item['size']} (出现{item['frequency']}次)")
    print()

    print(f"词云数据已保存到: {wordcloud_file}")
    print()

    return wordcloud_data

def show_privacy_demo():
    """展示隐私保护功能"""
    print("【隐私保护演示】")
    print()

    # 读取演示数据
    with open('data/demo_comments.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 显示隐私保护特性
    sample_comment = data.get('comments', [{}])[0]

    print("原始评论示例:")
    print(f"  内容: {sample_comment.get('content', '')}")
    print(f"  评分: {sample_comment.get('rating', 0)}")
    print()

    print("隐私保护处理:")
    print(f"  用户ID: {sample_comment.get('user_id', '')} (已哈希化)")
    print(f"  时间: {sample_comment.get('time_period', '')} (已泛化)")
    print(f"  标记: privacy_protected = {sample_comment.get('privacy_protected', False)}")
    print()

    print("保护措施说明:")
    print("  - 真实用户名已转换为哈希ID")
    print("  - 具体时间已转换为时间段")
    print("  - 移除了可能的个人信息")
    print("  - 所有敏感数据已匿名化")
    print()

def show_file_results():
    """显示生成的文件"""
    print("【生成的文件】")
    print()

    files = [
        ('data/demo_comments.json', '演示评论数据'),
        ('data/demo_analysis_result.json', '分析结果'),
        ('data/wordcloud_data.json', '词云数据')
    ]

    for filepath, description in files:
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"[存在] {description}: {filepath} ({size} bytes)")
        else:
            print(f"[缺失] {description}: {filepath}")

    print()

def show_next_steps():
    """显示后续步骤"""
    print("【后续步骤】")
    print()
    print("1. 查看生成的JSON文件:")
    print("   type data\\demo_analysis_result.json")
    print("   type data\\wordcloud_data.json")
    print()
    print("2. 安装完整依赖包:")
    print("   pip install jieba wordcloud matplotlib selenium")
    print()
    print("3. 使用完整功能:")
    print("   python ccc-main.py --help")
    print()
    print("4. 尝试真实数据:")
    print("   python ccc-main.py pipeline \"餐厅名称\" --city 北京")
    print()

def main():
    """主函数"""
    show_banner()

    # 检查数据文件
    if not os.path.exists('data/demo_comments.json'):
        print("错误: 请先运行 python test_simple.py 创建演示数据")
        return

    try:
        # 展示隐私保护
        show_privacy_demo()

        # 运行分析
        print("=" * 30 + " 开始分析 " + "=" * 30)
        analysis_result = analyze_demo_data()

        # 生成词云数据
        print("=" * 30 + " 生成词云 " + "=" * 30)
        wordcloud_data = create_wordcloud_data()

        # 显示文件结果
        show_file_results()

        # 显示后续步骤
        show_next_steps()

        print("=" * 50)
        print("演示完成! 系统运行正常")
        print("=" * 50)

    except Exception as e:
        print(f"运行过程中出现错误: {e}")
        print("请检查数据文件是否存在")

if __name__ == '__main__':
    main()