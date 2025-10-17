# -*- coding: utf-8 -*-
"""
词云生成器
WordCloud Generator

生成词云图像
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import Counter
import os
import base64
from io import BytesIO

class WordCloudGenerator:
    """词云生成器"""

    def __init__(self):
        self.setup_matplotlib()

    def setup_matplotlib(self):
        """配置matplotlib中文显示"""
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False

    def generate_wordcloud(self, keywords, title="词云图", save_path=None):
        """生成词云（气泡图形式）"""
        if not keywords:
            return None

        # 创建气泡图
        fig, ax = plt.subplots(figsize=(12, 8))

        words = [item[0] if isinstance(item, tuple) else item for item in keywords]
        frequencies = [item[1] if isinstance(item, tuple) else 1 for item in keywords]

        # 布局设置
        cols = 4
        x_positions = []
        y_positions = []
        sizes = []
        colors = []

        for i, (word, freq) in enumerate(zip(words, frequencies)):
            x = i % cols
            y = i // cols

            x_positions.append(x)
            y_positions.append(y)
            sizes.append(freq * 200 + 100)  # 基于频率的大小
            colors.append(f'C{i % 10}')  # 颜色循环

        # 绘制气泡
        scatter = ax.scatter(x_positions, y_positions, s=sizes, c=colors, alpha=0.7)

        # 添加文字标签
        for i, word in enumerate(words):
            ax.annotate(word, (x_positions[i], y_positions[i]),
                       ha='center', va='center', fontsize=10, fontweight='bold')

        ax.set_xlim(-0.5, cols-0.5)
        ax.set_ylim(-0.5, max(y_positions) + 0.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)

        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        # 转换为base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

        return {
            'image_base64': image_base64,
            'save_path': save_path,
            'word_count': len(words)
        }

    def generate_category_wordclouds(self, category_keywords, save_dir=None):
        """生成分类词云"""
        if save_dir:
            os.makedirs(save_dir, exist_ok=True)

        results = {}
        for category, keywords in category_keywords.items():
            save_path = os.path.join(save_dir, f"{category}.png") if save_dir else None
            result = self.generate_wordcloud(
                keywords,
                title=f"{category}相关词云",
                save_path=save_path
            )
            results[category] = result

        return results