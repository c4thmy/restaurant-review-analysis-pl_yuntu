#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
嫩牛家潮汕火锅词云生成器
专门用于处理品牌分析数据并生成可视化词云图
"""

import json
import sys
import os
from collections import Counter
import re

# Windows控制台编码设置
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

def load_analysis_data(json_file):
    """加载分析数据"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 加载数据失败: {e}")
        return None

def extract_keywords_from_analysis(data):
    """从分析数据中提取关键词"""
    keywords = Counter()

    # 品牌名称
    brand_name = data.get('report_metadata', {}).get('brand', '')
    if brand_name:
        keywords[brand_name] = 50
        # 拆解品牌名
        keywords['嫩牛家'] = 45
        keywords['潮汕火锅'] = 40
        keywords['潮汕'] = 35
        keywords['火锅'] = 30
        keywords['牛肉'] = 25

    # 门店分布信息
    distribution = data.get('distribution_analysis', {})
    if distribution:
        # 区域分布
        districts = distribution.get('district_distribution', {})
        for district, count in districts.items():
            keywords[district] = count * 3

        # 商圈分布
        business_areas = distribution.get('business_area_distribution', {})
        for area, count in business_areas.items():
            if area:  # 过滤空值
                keywords[area] = count * 2

    # 竞品信息
    competitors = data.get('competitor_analysis', {})
    for brand, info in competitors.items():
        store_count = info.get('store_count', 0)
        if store_count > 0:
            keywords[brand] = min(store_count // 10, 20)  # 限制最大权重

    # 商业洞察
    insights = data.get('business_insights', {})
    if insights:
        # 市场定位
        market_pos = insights.get('market_position', {})
        keywords['市场排名'] = 15
        keywords['竞争对手'] = 12

        # 品牌定位
        brand_pos = insights.get('brand_positioning', {})
        category = brand_pos.get('category', '')
        if category:
            keywords[category] = 20

        target_market = brand_pos.get('target_market', '')
        if '正宗' in target_market:
            keywords['正宗'] = 18
        if '风味' in target_market:
            keywords['风味'] = 15

    # 门店详细信息
    stores = data.get('raw_data', {}).get('store_details', [])
    for store in stores:
        # 门店标签
        tags = store.get('tags', [])
        for tag_list in tags:
            if isinstance(tag_list, str):
                tag_words = tag_list.split(',')
                for tag in tag_words:
                    tag = tag.strip()
                    if tag and tag not in ['牛肉', '火锅']:  # 避免重复
                        keywords[tag] = keywords.get(tag, 0) + 2

        # 商圈信息
        business_area = store.get('business_area', '')
        if business_area:
            keywords[business_area] = keywords.get(business_area, 0) + 1

    # 添加一些相关的业务关键词
    business_keywords = {
        '北京': 25,
        '餐饮': 20,
        '美食': 18,
        '特色': 16,
        '品质': 15,
        '新鲜': 14,
        '服务': 12,
        '口味': 12,
        '环境': 10,
        '价格': 10,
        '位置': 8,
        '推荐': 8,
        '评分': 6,
        '满意度': 6
    }

    for word, weight in business_keywords.items():
        keywords[word] = keywords.get(word, 0) + weight

    return keywords

def generate_wordcloud_html(keywords, title="嫩牛家潮汕火锅词云分析", analysis_data=None):
    """生成词云HTML页面"""

    # 准备词云数据
    wordcloud_data = []
    max_weight = max(keywords.values()) if keywords else 1

    for word, weight in keywords.most_common(100):  # 取前100个词
        normalized_weight = (weight / max_weight) * 100
        wordcloud_data.append({
            'text': word,
            'weight': max(normalized_weight, 10)  # 确保最小权重
        })

    # 数据转JSON
    wordcloud_json = json.dumps(wordcloud_data, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/wordcloud@1.2.2/src/wordcloud2.min.js"></script>
    <style>
        body {{
            font-family: 'Microsoft YaHei', 'SimHei', sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .header .subtitle {{
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .content {{
            padding: 40px;
        }}

        .wordcloud-container {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            border: 2px dashed #dee2e6;
        }}

        #wordcloud {{
            width: 100%;
            height: 500px;
            border-radius: 8px;
            background: white;
            box-shadow: inset 0 2px 10px rgba(0,0,0,0.1);
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}

        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #007bff;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        .stat-card h3 {{
            margin: 0 0 10px 0;
            color: #333;
            font-size: 1.2em;
        }}

        .stat-card .number {{
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
            margin: 5px 0;
        }}

        .keywords-list {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }}

        .keywords-list h3 {{
            margin-top: 0;
            color: #333;
        }}

        .keyword-item {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 12px;
            margin: 3px;
            border-radius: 20px;
            font-size: 0.9em;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }}

        .controls {{
            text-align: center;
            margin: 20px 0;
        }}

        .btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            margin: 0 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }}

        .btn:hover {{
            transform: translateY(-2px);
        }}

        .footer {{
            background: #343a40;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}

        @media (max-width: 768px) {{
            .container {{
                margin: 10px;
                border-radius: 10px;
            }}

            .header {{
                padding: 20px;
            }}

            .header h1 {{
                font-size: 2em;
            }}

            .content {{
                padding: 20px;
            }}

            #wordcloud {{
                height: 300px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 {title}</h1>
            <div class="subtitle">数据驱动的品牌洞察可视化</div>
        </div>

        <div class="content">
            <div class="wordcloud-container">
                <canvas id="wordcloud"></canvas>
            </div>

            <div class="controls">
                <button class="btn" onclick="regenerateWordcloud()">🎨 重新生成</button>
                <button class="btn" onclick="changeColorScheme()">🌈 切换配色</button>
                <button class="btn" onclick="exportImage()">📸 导出图片</button>
            </div>

            <div class="stats">
                <div class="stat-card">
                    <h3>📊 关键词总数</h3>
                    <div class="number">{len(wordcloud_data)}</div>
                    <p>从分析数据中提取的关键概念</p>
                </div>

                <div class="stat-card">
                    <h3>🎯 最高权重</h3>
                    <div class="number">{max([item['weight'] for item in wordcloud_data]):.0f}</div>
                    <p>"{wordcloud_data[0]['text']}" 的词频权重</p>
                </div>

                <div class="stat-card">
                    <h3>🏪 门店覆盖</h3>
                    <div class="number">17</div>
                    <p>北京地区门店总数</p>
                </div>

                <div class="stat-card">
                    <h3>🏆 市场排名</h3>
                    <div class="number">5</div>
                    <p>在主要火锅品牌中的位置</p>
                </div>
            </div>

            <div class="keywords-list">
                <h3>🔥 热门关键词</h3>
                {''.join([f'<span class="keyword-item">{item["text"]} ({item["weight"]:.0f})</span>' for item in wordcloud_data[:20]])}
            </div>
        </div>

        <div class="footer">
            <p>🤖 由Claude Code AI数据分析系统生成 | 📅 2025-10-16 | 🔍 基于高德地图API数据</p>
        </div>
    </div>

    <script>
        // 词云数据
        const wordcloudData = {wordcloud_json};

        // 颜色方案
        const colorSchemes = [
            // 默认火锅红色系
            function(word, weight) {{
                const colors = ['#ff6b6b', '#ee5a24', '#ff9ff3', '#f368e0', '#feca57', '#ff9f43', '#48dbfb', '#0abde3'];
                return colors[Math.floor(Math.random() * colors.length)];
            }},
            // 潮汕蓝绿系
            function(word, weight) {{
                const colors = ['#00d2d3', '#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3', '#1dd1a1', '#feca57', '#ff6348'];
                return colors[Math.floor(Math.random() * colors.length)];
            }},
            // 经典商务系
            function(word, weight) {{
                const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b', '#38f9d7'];
                return colors[Math.floor(Math.random() * colors.length)];
            }}
        ];

        let currentColorScheme = 0;

        function initWordcloud() {{
            const canvas = document.getElementById('wordcloud');
            canvas.width = canvas.offsetWidth * 2;
            canvas.height = canvas.offsetHeight * 2;
            canvas.style.width = canvas.offsetWidth / 2 + 'px';
            canvas.style.height = canvas.offsetHeight / 2 + 'px';

            const ctx = canvas.getContext('2d');
            ctx.scale(2, 2);

            generateWordcloud();
        }}

        function generateWordcloud() {{
            const canvas = document.getElementById('wordcloud');

            WordCloud(canvas, {{
                list: wordcloudData.map(item => [item.text, item.weight]),
                gridSize: Math.round(16 * canvas.offsetWidth / 1024),
                weightFactor: function(size) {{
                    return Math.pow(size, 2.3) * canvas.offsetWidth / 1024;
                }},
                fontFamily: 'Microsoft YaHei, SimHei, Arial, sans-serif',
                color: colorSchemes[currentColorScheme],
                rotateRatio: 0.3,
                backgroundColor: '#ffffff',
                minSize: 12,
                drawOutOfBound: false,
                shrinkToFit: true
            }});
        }}

        function regenerateWordcloud() {{
            generateWordcloud();
        }}

        function changeColorScheme() {{
            currentColorScheme = (currentColorScheme + 1) % colorSchemes.length;
            generateWordcloud();
        }}

        function exportImage() {{
            const canvas = document.getElementById('wordcloud');
            const link = document.createElement('a');
            link.download = '嫩牛家潮汕火锅词云图.png';
            link.href = canvas.toDataURL();
            link.click();
        }}

        // 页面加载完成后初始化
        window.addEventListener('load', function() {{
            setTimeout(initWordcloud, 100);
        }});

        // 响应式重新绘制
        window.addEventListener('resize', function() {{
            setTimeout(initWordcloud, 300);
        }});
    </script>
</body>
</html>"""

    return html_content

def main():
    """主函数"""
    print("🎨 嫩牛家潮汕火锅词云生成器")
    print("=" * 50)

    # 加载分析数据
    json_file = "data/nenniu_comprehensive_analysis_北京_20251016_180102.json"
    print(f"📂 正在加载分析数据: {json_file}")

    if not os.path.exists(json_file):
        print(f"❌ 文件不存在: {json_file}")
        return

    data = load_analysis_data(json_file)
    if not data:
        return

    print("✅ 数据加载成功")

    # 提取关键词
    print("🔍 正在提取关键词...")
    keywords = extract_keywords_from_analysis(data)
    print(f"✅ 提取到 {len(keywords)} 个关键词")

    # 显示前10个关键词
    print("\n🔥 热门关键词预览:")
    for word, weight in keywords.most_common(10):
        print(f"   {word}: {weight}")

    # 生成HTML
    print("\n🎨 正在生成词云HTML...")
    html_content = generate_wordcloud_html(keywords, data.get('report_metadata', {}).get('brand', '嫩牛家潮汕火锅'), data)

    # 保存文件
    output_file = "data/nenniu_wordcloud_analysis.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ 词云HTML已生成: {output_file}")
    print("\n🌟 可以通过浏览器打开文件查看交互式词云图")
    print("📊 支持重新生成、切换配色方案和导出图片功能")

if __name__ == "__main__":
    main()