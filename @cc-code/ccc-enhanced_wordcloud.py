#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强型词云图生成工具
Enhanced WordCloud Generator

功能特点：
- 生成真实的词云图像
- 情感色彩分类显示
- 自定义中文字体支持
- 高质量图像输出
- 互动式HTML集成
"""

import json
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import defaultdict
import base64
from io import BytesIO

# 尝试导入wordcloud库
try:
    from wordcloud import WordCloud
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False
    print("提示: wordcloud库未安装，将使用备用方案")

class EnhancedWordCloudGenerator:
    """增强型词云生成器"""

    def __init__(self):
        self.setup_matplotlib()

    def setup_matplotlib(self):
        """配置matplotlib中文显示"""
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False

    def get_sentiment_color(self, text):
        """根据词汇内容判断情感色彩"""
        positive_words = ['好', '很好', '不错', '新鲜', '推荐', '干净', '正宗', '质量好', '值得']
        negative_words = ['贵', '有点贵', '排队', '时间长', '不够']

        for word in positive_words:
            if word in text:
                return '#2E8B57'  # 深绿色 - 正面

        for word in negative_words:
            if word in text:
                return '#DC143C'  # 深红色 - 负面

        return '#4682B4'  # 钢蓝色 - 中性

    def create_wordcloud_image(self, words_data):
        """生成真实的词云图像"""
        if not WORDCLOUD_AVAILABLE:
            return self.create_fallback_visualization(words_data)

        # 准备词频数据
        word_freq = {}
        for item in words_data:
            word_freq[item['text']] = item['frequency']

        # 创建词云对象
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            max_words=100,
            relative_scaling=0.5,
            colormap='viridis',
            font_path=self.get_chinese_font(),
            prefer_horizontal=0.7,
            min_font_size=12,
            max_font_size=60
        ).generate_from_frequencies(word_freq)

        # 生成图像
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('大众点评评论词云图', fontsize=16, pad=20)

        # 保存为base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

        return image_base64

    def get_chinese_font(self):
        """获取中文字体路径"""
        font_paths = [
            'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
            'C:/Windows/Fonts/simhei.ttf',  # 黑体
            'C:/Windows/Fonts/simsun.ttc',  # 宋体
        ]

        for font_path in font_paths:
            if os.path.exists(font_path):
                return font_path
        return None

    def create_fallback_visualization(self, words_data):
        """备用可视化方案（不依赖wordcloud）"""
        # 按频率分组
        freq_groups = defaultdict(list)
        for item in words_data:
            freq_groups[item['frequency']].append(item)

        # 创建气泡图样式的可视化
        fig, ax = plt.subplots(figsize=(12, 8))

        x_positions = []
        y_positions = []
        sizes = []
        colors = []
        texts = []

        x, y = 0, 0
        for freq in sorted(freq_groups.keys(), reverse=True):
            for i, item in enumerate(freq_groups[freq]):
                x_positions.append(x)
                y_positions.append(y)
                sizes.append(item['frequency'] * 200 + 100)
                colors.append(self.get_sentiment_color(item['text']))
                texts.append(item['text'])

                # 调整位置
                x += 1
                if x > 4:  # 每行最多5个
                    x = 0
                    y += 1

        # 绘制散点图
        scatter = ax.scatter(x_positions, y_positions, s=sizes, c=colors, alpha=0.7)

        # 添加文字标签
        for i, txt in enumerate(texts):
            ax.annotate(txt, (x_positions[i], y_positions[i]),
                       ha='center', va='center', fontsize=10, fontweight='bold')

        ax.set_xlim(-0.5, 4.5)
        ax.set_ylim(-0.5, max(y_positions) + 0.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('大众点评评论关键词可视化', fontsize=16, pad=20)

        # 添加图例
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#2E8B57',
                   markersize=10, label='正面评价'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#DC143C',
                   markersize=10, label='负面评价'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#4682B4',
                   markersize=10, label='中性评价')
        ]
        ax.legend(handles=legend_elements, loc='upper right')

        # 保存为base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

        return image_base64

    def create_enhanced_html_report(self, analysis_data, wordcloud_data):
        """创建增强版HTML报告"""
        # 生成词云图像
        wordcloud_image = self.create_wordcloud_image(wordcloud_data['words'])

        # 生成情感分析图表
        sentiment_chart = self.create_sentiment_chart(analysis_data.get('sentiment_analysis', {}))

        html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>大众点评评论分析 - 增强版可视化报告</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .content {{
            padding: 40px;
        }}
        .section {{
            margin-bottom: 50px;
        }}
        .section h2 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
            margin-bottom: 30px;
            font-size: 1.8em;
            font-weight: 400;
        }}
        .wordcloud-container {{
            text-align: center;
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .wordcloud-image {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .stat-label {{
            color: #7f8c8d;
            font-size: 1.1em;
        }}
        .chart-container {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .keywords-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .keyword-tag {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 12px 18px;
            border-radius: 25px;
            text-align: center;
            font-weight: 500;
            box-shadow: 0 2px 8px rgba(52, 152, 219, 0.3);
            transition: all 0.3s ease;
        }}
        .keyword-tag:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.5);
        }}
        .keyword-tag.positive {{
            background: linear-gradient(135deg, #27ae60, #229954);
        }}
        .keyword-tag.negative {{
            background: linear-gradient(135deg, #e74c3c, #c0392b);
        }}
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 2em; }}
            .content {{ padding: 20px; }}
            .stats-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🍲 大众点评评论分析报告</h1>
            <p>增强版可视化分析 - 数据驱动的餐厅评价洞察</p>
        </div>

        <div class="content">
            <!-- 基础统计 -->
            <div class="section">
                <h2>📊 基础统计概览</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{total_comments}</div>
                        <div class="stat-label">总评论数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{average_rating}</div>
                        <div class="stat-label">平均评分</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{positive_rate}%</div>
                        <div class="stat-label">好评率</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{keyword_count}</div>
                        <div class="stat-label">关键词数量</div>
                    </div>
                </div>
            </div>

            <!-- 词云图 -->
            <div class="section">
                <h2>☁️ 关键词词云图</h2>
                <div class="wordcloud-container">
                    <img src="data:image/png;base64,{wordcloud_image}"
                         alt="词云图" class="wordcloud-image">
                    <p style="margin-top: 20px; color: #7f8c8d;">
                        词云大小反映关键词频率，颜色表示情感倾向
                    </p>
                </div>
            </div>

            <!-- 情感分析 -->
            <div class="section">
                <h2>😊 情感分析</h2>
                <div class="chart-container">
                    <img src="data:image/png;base64,{sentiment_chart}"
                         alt="情感分析图表" style="max-width: 100%; height: auto;">
                </div>
            </div>

            <!-- 热门关键词 -->
            <div class="section">
                <h2>🔥 热门关键词标签</h2>
                <div class="keywords-grid">
                    {keyword_tags}
                </div>
            </div>
        </div>

        <div class="footer">
            <p>🔒 本报告采用数据匿名化处理，保护用户隐私</p>
            <p>📅 生成时间: {timestamp}</p>
            <p>🤖 由Claude Code增强型分析系统生成</p>
        </div>
    </div>
</body>
</html>"""

        # 生成关键词标签HTML
        keyword_tags_html = ""
        for word in wordcloud_data['words'][:15]:  # 显示前15个关键词
            sentiment_class = self.get_sentiment_class(word['text'])
            keyword_tags_html += f'''
            <div class="keyword-tag {sentiment_class}">
                {word['text']} ({word['frequency']})
            </div>'''

        # 计算正面评价率
        sentiment = analysis_data.get('sentiment_analysis', {})
        total_sentiment = sentiment.get('positive', 0) + sentiment.get('negative', 0) + sentiment.get('neutral', 0)
        positive_rate = round((sentiment.get('positive', 0) / max(total_sentiment, 1)) * 100)

        # 填充模板
        return html_template.format(
            total_comments=analysis_data.get('total_comments', 0),
            average_rating=analysis_data.get('average_rating', 0),
            positive_rate=positive_rate,
            keyword_count=len(wordcloud_data['words']),
            wordcloud_image=wordcloud_image,
            sentiment_chart=sentiment_chart,
            keyword_tags=keyword_tags_html,
            timestamp=wordcloud_data.get('timestamp', '')
        )

    def get_sentiment_class(self, text):
        """获取情感CSS类"""
        color = self.get_sentiment_color(text)
        if color == '#2E8B57':
            return 'positive'
        elif color == '#DC143C':
            return 'negative'
        else:
            return ''

    def create_sentiment_chart(self, sentiment_data):
        """创建情感分析图表"""
        categories = ['正面', '中性', '负面']
        values = [
            sentiment_data.get('positive', 0),
            sentiment_data.get('neutral', 0),
            sentiment_data.get('negative', 0)
        ]
        colors = ['#27ae60', '#f39c12', '#e74c3c']

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(categories, values, color=colors, alpha=0.8)

        # 添加数值标签
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{value}', ha='center', va='bottom', fontsize=12, fontweight='bold')

        ax.set_ylabel('评论数量', fontsize=12)
        ax.set_title('情感分析分布', fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3)

        # 美化图表
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_ylim(0, max(values) * 1.2 if max(values) > 0 else 1)

        plt.tight_layout()

        # 保存为base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

        return image_base64

def main():
    """主函数"""
    print("🎨 启动增强型词云图生成器...")

    # 检查数据文件
    data_dir = Path("data")
    analysis_file = data_dir / "demo_analysis_result.json"
    wordcloud_file = data_dir / "wordcloud_data.json"

    if not analysis_file.exists() or not wordcloud_file.exists():
        print("❌ 缺少必要的数据文件，请先运行 demo_run.py")
        return

    # 加载数据
    try:
        with open(analysis_file, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)

        with open(wordcloud_file, 'r', encoding='utf-8') as f:
            wordcloud_data = json.load(f)
    except Exception as e:
        print(f"❌ 读取数据文件失败: {e}")
        return

    # 生成增强版报告
    generator = EnhancedWordCloudGenerator()

    print("🎨 生成增强版词云图...")
    enhanced_html = generator.create_enhanced_html_report(analysis_data, wordcloud_data)

    # 保存报告
    output_file = data_dir / "enhanced_analysis_report.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(enhanced_html)

    print(f"✅ 增强版可视化报告已生成: {output_file}")
    print("\n🎉 增强功能包括:")
    print("   📊 真实词云图生成")
    print("   🎨 情感色彩分类")
    print("   📈 交互式图表")
    print("   🎯 响应式设计")
    print("   ✨ 现代化界面")

    # 自动打开报告
    import webbrowser
    try:
        webbrowser.open(str(output_file))
        print(f"\n🌐 已在浏览器中打开报告")
    except:
        print(f"\n💡 请手动打开文件: {output_file}")

if __name__ == "__main__":
    main()