#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版Web演示界面
展示分析结果和词云数据
"""

import json
import os
from datetime import datetime

def create_html_report():
    """创建HTML报告"""

    # 读取分析结果
    try:
        with open('data/demo_analysis_result.json', 'r', encoding='utf-8') as f:
            analysis = json.load(f)
    except FileNotFoundError:
        print("请先运行 python demo_run.py 生成分析结果")
        return

    # 读取词云数据
    try:
        with open('data/wordcloud_data.json', 'r', encoding='utf-8') as f:
            wordcloud = json.load(f)
    except FileNotFoundError:
        print("词云数据文件不存在")
        wordcloud = {'words': []}

    # 生成HTML内容
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>大众点评评论分析结果 - 演示报告</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .section h2 {{
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #667eea;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        .wordcloud-container {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .word-item {{
            display: inline-block;
            margin: 5px 10px;
            padding: 8px 16px;
            background: #667eea;
            color: white;
            border-radius: 20px;
            font-weight: bold;
        }}
        .keyword-item {{
            background: #28a745;
        }}
        .tag-item {{
            background: #ffc107;
            color: #333;
        }}
        .sentiment-bar {{
            height: 30px;
            background: #e9ecef;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
            position: relative;
        }}
        .sentiment-positive {{
            height: 100%;
            background: #28a745;
            float: left;
        }}
        .sentiment-negative {{
            height: 100%;
            background: #dc3545;
            float: right;
        }}
        .privacy-notice {{
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .table th, .table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        .table th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        .demo-badge {{
            background: #17a2b8;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-left: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>大众点评评论分析报告</h1>
            <p>合规版系统演示 - 隐私保护数据分析</p>
            <span class="demo-badge">演示数据</span>
        </div>

        <div class="content">
            <!-- 隐私保护声明 -->
            <div class="privacy-notice">
                <h4>🔐 隐私保护声明</h4>
                <p>本报告使用的数据已进行完全匿名化处理，包括用户身份哈希化、时间信息泛化、敏感信息过滤等措施。所有数据处理符合隐私保护要求。</p>
            </div>

            <!-- 基础统计 -->
            <div class="section">
                <h2>📊 基础统计</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{analysis['basic_stats']['total_comments']}</div>
                        <div class="stat-label">总评论数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{analysis['basic_stats']['average_rating']}</div>
                        <div class="stat-label">平均评分</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">✅</div>
                        <div class="stat-label">隐私保护</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{len(analysis['keywords'])}</div>
                        <div class="stat-label">关键词数</div>
                    </div>
                </div>
            </div>

            <!-- 情感分析 -->
            <div class="section">
                <h2>😊 情感分析</h2>
                <p>基于关键词的情感倾向分析：</p>
                <div class="sentiment-bar">
                    <div class="sentiment-positive" style="width: {analysis['sentiment_analysis']['positive']/(analysis['sentiment_analysis']['positive']+analysis['sentiment_analysis']['negative'])*100 if (analysis['sentiment_analysis']['positive']+analysis['sentiment_analysis']['negative']) > 0 else 50}%"></div>
                    <div class="sentiment-negative" style="width: {analysis['sentiment_analysis']['negative']/(analysis['sentiment_analysis']['positive']+analysis['sentiment_analysis']['negative'])*100 if (analysis['sentiment_analysis']['positive']+analysis['sentiment_analysis']['negative']) > 0 else 50}%"></div>
                </div>
                <p>
                    正面情感: {analysis['sentiment_analysis']['positive']} 个指标 |
                    负面情感: {analysis['sentiment_analysis']['negative']} 个指标
                </p>
            </div>

            <!-- 关键词分析 -->
            <div class="section">
                <h2>🔍 关键词分析</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>关键词</th>
                            <th>出现次数</th>
                            <th>类型</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    # 添加关键词表格
    for keyword, count in analysis['keywords'][:10]:
        html_content += f"""
                        <tr>
                            <td>{keyword}</td>
                            <td>{count}</td>
                            <td><span style="background: #28a745; color: white; padding: 2px 6px; border-radius: 10px; font-size: 0.8em;">关键词</span></td>
                        </tr>
"""

    html_content += """
                    </tbody>
                </table>
            </div>

            <!-- 用户标签 -->
            <div class="section">
                <h2>🏷️ 用户标签</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>标签</th>
                            <th>出现次数</th>
                            <th>类型</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    # 添加标签表格
    for tag, count in analysis['tags'][:10]:
        html_content += f"""
                        <tr>
                            <td>{tag}</td>
                            <td>{count}</td>
                            <td><span style="background: #ffc107; color: #333; padding: 2px 6px; border-radius: 10px; font-size: 0.8em;">用户标签</span></td>
                        </tr>
"""

    html_content += """
                    </tbody>
                </table>
            </div>

            <!-- 词云展示 -->
            <div class="section">
                <h2>☁️ 词云数据</h2>
                <p>以下是生成的词云数据，字体大小反映词汇重要性：</p>
                <div class="wordcloud-container">
"""

    # 添加词云词汇
    for word_data in wordcloud['words'][:15]:
        word_type = 'keyword-item' if word_data['type'] == 'keyword' else 'tag-item'
        font_size = min(word_data['size'], 30)
        html_content += f"""
                    <span class="word-item {word_type}" style="font-size: {font_size-8}px;">
                        {word_data['text']} ({word_data['frequency']})
                    </span>
"""

    html_content += f"""
                </div>
                <p><small>显示了前15个高频词汇，总共生成了 {wordcloud['total_words']} 个词云数据点</small></p>
            </div>

            <!-- 技术说明 -->
            <div class="section">
                <h2>⚙️ 技术说明</h2>
                <ul>
                    <li><strong>数据来源</strong>: 演示数据，已完全匿名化处理</li>
                    <li><strong>分析时间</strong>: {analysis['timestamp']}</li>
                    <li><strong>隐私保护</strong>: 用户身份哈希化，时间信息泛化</li>
                    <li><strong>分析方法</strong>: 中文关键词提取 + 简单情感分析</li>
                    <li><strong>词云生成</strong>: 基于词频的可视化数据</li>
                    <li><strong>合规特性</strong>: 符合数据保护法规要求</li>
                </ul>
            </div>

            <!-- 系统信息 -->
            <div class="section">
                <h2>📋 系统信息</h2>
                <div class="privacy-notice">
                    <p><strong>大众点评餐厅评论分析系统 - 合规版</strong></p>
                    <p>版本: 1.0.0-compliance | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>本系统仅供学习和研究使用，严格遵守数据保护和隐私保护要求。</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

    # 保存HTML文件
    html_file = 'data/analysis_report.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML报告已生成: {html_file}")
    print("可以在浏览器中打开查看完整的可视化报告")

    return html_file

def main():
    """主函数"""
    print("正在生成HTML可视化报告...")
    print()

    if not os.path.exists('data/demo_analysis_result.json'):
        print("错误: 分析结果文件不存在")
        print("请先运行: python demo_run.py")
        return

    html_file = create_html_report()

    print()
    print("=" * 50)
    print("Web演示报告生成完成!")
    print("=" * 50)
    print()
    print("查看方法:")
    print(f"1. 双击打开文件: {html_file}")
    print("2. 或在浏览器中打开该文件")
    print("3. 查看完整的可视化分析报告")
    print()

if __name__ == '__main__':
    main()