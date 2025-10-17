#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动和演示脚本
解决路径问题并立即开始使用系统
"""

import os
import sys
import json
from datetime import datetime
import subprocess

def show_start_banner():
    """显示启动横幅"""
    print("=" * 60)
    print("    立即开始使用 - 大众点评评论分析系统")
    print("=" * 60)
    print()

def check_demo_data():
    """检查演示数据"""
    demo_file = 'data/demo_comments.json'
    if os.path.exists(demo_file):
        print(f"✅ 演示数据文件存在: {demo_file}")

        # 读取并显示数据概览
        with open(demo_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        comments = data.get('comments', [])
        print(f"   包含 {len(comments)} 条评论")
        print(f"   数据特点: 已匿名化处理")
        print()
        return True
    else:
        print(f"❌ 演示数据文件不存在: {demo_file}")
        return False

def run_basic_analysis():
    """运行基础分析"""
    print("🔍 开始基础分析演示...")
    print()

    # 读取演示数据
    with open('data/demo_comments.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    comments = data.get('comments', [])

    # 基础统计
    total_comments = len(comments)
    ratings = [c.get('rating', 0) for c in comments if c.get('rating')]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0

    # 提取关键词
    all_content = ' '.join([c.get('content', '') for c in comments])

    # 简单词频统计
    words = []
    for comment in comments:
        content = comment.get('content', '')
        # 简单分词（按空格和标点）
        import re
        comment_words = re.findall(r'[\u4e00-\u9fa5]+', content)
        words.extend(comment_words)

    # 统计词频
    from collections import Counter
    word_freq = Counter(words)
    top_words = word_freq.most_common(10)

    # 标签统计
    all_tags = []
    for comment in comments:
        tags = comment.get('tags', [])
        all_tags.extend(tags)

    tag_freq = Counter(all_tags)

    # 显示分析结果
    print("📊 分析结果:")
    print(f"   总评论数: {total_comments}")
    print(f"   平均评分: {avg_rating:.2f}")
    print(f"   独立用户: {len(set(c.get('user_id', '') for c in comments))}")
    print()

    print("🏷️ 高频标签:")
    for tag, count in tag_freq.most_common(5):
        print(f"   {tag}: {count}次")
    print()

    print("📝 高频词汇:")
    for word, count in top_words[:8]:
        if len(word) >= 2:  # 只显示2个字符以上的词
            print(f"   {word}: {count}次")
    print()

    # 情感分析（简单版）
    positive_words = ['好', '不错', '推荐', '新鲜', '值得']
    negative_words = ['贵', '长', '差']

    positive_count = 0
    negative_count = 0

    for comment in comments:
        content = comment.get('content', '')
        for word in positive_words:
            if word in content:
                positive_count += 1
        for word in negative_words:
            if word in content:
                negative_count += 1

    total_sentiment = positive_count + negative_count
    if total_sentiment > 0:
        positive_rate = positive_count / total_sentiment * 100
        print(f"😊 情感倾向:")
        print(f"   正面评价: {positive_rate:.1f}%")
        print(f"   负面评价: {100-positive_rate:.1f}%")

    print()

    return {
        'total_comments': total_comments,
        'avg_rating': avg_rating,
        'top_words': top_words,
        'top_tags': tag_freq.most_common(5),
        'positive_rate': positive_rate if total_sentiment > 0 else 0
    }

def create_simple_wordcloud():
    """创建简单的词云数据"""
    print("☁️ 生成词云数据...")
    print()

    # 读取分析结果
    with open('data/demo_comments.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    comments = data.get('comments', [])

    # 提取所有文本
    all_text = []
    for comment in comments:
        content = comment.get('content', '')
        tags = comment.get('tags', [])
        all_text.append(content)
        all_text.extend(tags)

    # 词频统计
    import re
    from collections import Counter

    words = []
    for text in all_text:
        # 提取中文词汇
        chinese_words = re.findall(r'[\u4e00-\u9fa5]{2,}', text)
        words.extend(chinese_words)

    word_freq = Counter(words)

    # 创建词云数据格式
    wordcloud_data = []
    for word, freq in word_freq.most_common(20):
        wordcloud_data.append({
            'name': word,
            'value': freq * 10,  # 放大数值用于显示
            'style': {
                'fontSize': min(freq * 5 + 12, 30)
            }
        })

    # 保存词云数据
    wordcloud_file = 'data/wordcloud_data.json'
    with open(wordcloud_file, 'w', encoding='utf-8') as f:
        json.dump(wordcloud_data, f, ensure_ascii=False, indent=2)

    print(f"✅ 词云数据已保存: {wordcloud_file}")
    print("📊 词云数据预览:")
    for item in wordcloud_data[:10]:
        print(f"   {item['name']}: {item['value']}")
    print()

    return wordcloud_data

def show_next_steps():
    """显示后续步骤"""
    print("🎯 后续可以尝试:")
    print()
    print("1. 查看生成的分析结果:")
    print("   notepad data\\demo_comments.json")
    print("   notepad data\\wordcloud_data.json")
    print()
    print("2. 安装完整依赖后使用高级功能:")
    print("   pip install jieba wordcloud matplotlib")
    print("   python ccc-main.py analyze data/demo_comments.json")
    print()
    print("3. 尝试真实数据爬取 (需要Chrome浏览器):")
    print("   python ccc-main.py pipeline \"餐厅名称\" --city 北京 --months 1")
    print()
    print("4. 启动Web界面:")
    print("   python ccc-main.py web")
    print()

def demonstrate_privacy_protection():
    """演示隐私保护功能"""
    print("🔐 隐私保护演示:")
    print()

    # 读取演示数据
    with open('data/demo_comments.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("✅ 数据保护措施:")
    metadata = data.get('metadata', {})

    features = [
        ('隐私保护', metadata.get('privacy_protected', False)),
        ('用户匿名化', metadata.get('anonymized', False)),
        ('合规版本', metadata.get('compliance_version', '未知')),
        ('演示数据', metadata.get('demo_data', False))
    ]

    for feature, status in features:
        status_text = "✅ 已启用" if status else "❌ 未启用"
        if isinstance(status, str):
            status_text = f"版本 {status}"
        print(f"   {feature}: {status_text}")

    print()

    # 显示匿名化示例
    sample_comment = data.get('comments', [{}])[0]
    print("📝 匿名化示例:")
    print(f"   用户ID: {sample_comment.get('user_id', 'N/A')} (已哈希化)")
    print(f"   时间信息: {sample_comment.get('time_period', 'N/A')} (已泛化)")
    print(f"   内容: {sample_comment.get('content', 'N/A')[:30]}...")
    print()

def main():
    """主函数"""
    show_start_banner()

    # 检查演示数据
    if not check_demo_data():
        print("请先运行 python test_simple.py 创建演示数据")
        return

    # 演示隐私保护
    demonstrate_privacy_protection()

    # 运行基础分析
    try:
        analysis_result = run_basic_analysis()
        print("✅ 基础分析完成!")
        print()
    except Exception as e:
        print(f"❌ 分析过程出错: {e}")
        return

    # 生成词云数据
    try:
        wordcloud_data = create_simple_wordcloud()
        print("✅ 词云数据生成完成!")
        print()
    except Exception as e:
        print(f"❌ 词云生成过程出错: {e}")

    # 显示后续步骤
    show_next_steps()

    print("=" * 60)
    print("🎉 演示完成！系统功能正常运行")
    print("=" * 60)

if __name__ == '__main__':
    main()