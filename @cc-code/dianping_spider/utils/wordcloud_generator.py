import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from wordcloud import WordCloud
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import json
import os
from collections import Counter

from config import WORDCLOUD_CONFIG
from utils.data_utils import Logger


# 设置matplotlib支持中文
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


class WordCloudGenerator:
    """词云图生成器"""

    def __init__(self):
        self.logger = Logger.setup(__name__)
        self.config = WORDCLOUD_CONFIG.copy()
        self.setup_font()

    def setup_font(self):
        """设置中文字体"""
        # 尝试寻找系统中的中文字体
        font_paths = [
            # Windows
            'C:/Windows/Fonts/simhei.ttf',
            'C:/Windows/Fonts/msyh.ttf',
            'C:/Windows/Fonts/simsun.ttc',
            # macOS
            '/System/Library/Fonts/Helvetica.ttc',
            '/System/Library/Fonts/PingFang.ttc',
            # Linux
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
        ]

        for font_path in font_paths:
            if os.path.exists(font_path):
                self.config['font_path'] = font_path
                self.logger.info(f"使用字体: {font_path}")
                break
        else:
            self.logger.warning("未找到中文字体，将使用默认字体")
            self.config['font_path'] = None

    def generate_wordcloud(self, keywords, title="词云图", save_path=None):
        """生成词云图"""
        if not keywords:
            self.logger.warning("关键词为空，无法生成词云")
            return None

        try:
            # 准备词频数据
            if isinstance(keywords, list):
                # 如果是[(word, score), ...]格式
                word_freq = {word: score for word, score in keywords}
            elif isinstance(keywords, dict):
                word_freq = keywords
            else:
                self.logger.error("不支持的关键词格式")
                return None

            # 创建词云对象
            wordcloud = WordCloud(
                width=self.config['width'],
                height=self.config['height'],
                font_path=self.config['font_path'],
                max_words=self.config['max_words'],
                background_color=self.config['background_color'],
                colormap=self.config['colormap'],
                relative_scaling=0.5,
                random_state=42
            ).generate_from_frequencies(word_freq)

            # 创建图表
            plt.figure(figsize=(12, 8))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(title, fontsize=16, pad=20)
            plt.tight_layout(pad=0)

            # 保存图片
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"词云图已保存到: {save_path}")

            # 转换为base64编码（用于web显示）
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode()
            buffer.close()

            plt.close()  # 关闭图表释放内存

            return {
                'image_base64': image_base64,
                'save_path': save_path,
                'word_count': len(word_freq)
            }

        except Exception as e:
            self.logger.error(f"生成词云图失败: {e}")
            return None

    def generate_category_wordclouds(self, category_data, save_dir="wordclouds"):
        """生成分类词云图"""
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        results = {}

        for category, keywords in category_data.items():
            if keywords:
                title = f"{category}相关词云"
                save_path = os.path.join(save_dir, f"{category}_wordcloud.png")

                result = self.generate_wordcloud(
                    keywords=keywords,
                    title=title,
                    save_path=save_path
                )

                if result:
                    results[category] = result
                    self.logger.info(f"生成{category}词云图成功")
                else:
                    self.logger.warning(f"生成{category}词云图失败")

        return results

    def generate_interactive_wordcloud(self, keywords, title="交互式词云"):
        """生成交互式词云数据（用于前端展示）"""
        if not keywords:
            return None

        # 准备数据
        if isinstance(keywords, list):
            word_data = [{'name': word, 'value': int(score * 1000)} for word, score in keywords]
        elif isinstance(keywords, dict):
            word_data = [{'name': word, 'value': int(score * 1000)} for word, score in keywords.items()]
        else:
            return None

        # 按值排序
        word_data.sort(key=lambda x: x['value'], reverse=True)

        return {
            'title': title,
            'data': word_data,
            'maxValue': max([item['value'] for item in word_data]) if word_data else 0,
            'minValue': min([item['value'] for item in word_data]) if word_data else 0
        }

    def create_comparison_wordcloud(self, data_sets, titles, save_path=None):
        """创建对比词云图"""
        if len(data_sets) != len(titles):
            self.logger.error("数据集数量与标题数量不匹配")
            return None

        try:
            fig, axes = plt.subplots(1, len(data_sets), figsize=(6 * len(data_sets), 6))

            if len(data_sets) == 1:
                axes = [axes]

            results = []

            for i, (keywords, title) in enumerate(zip(data_sets, titles)):
                if isinstance(keywords, list):
                    word_freq = {word: score for word, score in keywords}
                elif isinstance(keywords, dict):
                    word_freq = keywords
                else:
                    continue

                if not word_freq:
                    continue

                # 生成词云
                wordcloud = WordCloud(
                    width=400,
                    height=400,
                    font_path=self.config['font_path'],
                    max_words=100,
                    background_color='white',
                    colormap=plt.cm.Set3,
                    relative_scaling=0.5,
                    random_state=42
                ).generate_from_frequencies(word_freq)

                # 绘制
                axes[i].imshow(wordcloud, interpolation='bilinear')
                axes[i].set_title(title, fontsize=14)
                axes[i].axis('off')

                results.append({
                    'title': title,
                    'word_count': len(word_freq)
                })

            plt.tight_layout()

            # 保存
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"对比词云图已保存到: {save_path}")

            # 转换为base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode()
            buffer.close()

            plt.close()

            return {
                'image_base64': image_base64,
                'save_path': save_path,
                'results': results
            }

        except Exception as e:
            self.logger.error(f"生成对比词云图失败: {e}")
            return None

    def generate_trend_wordcloud(self, time_keywords, save_dir="trend_wordclouds"):
        """生成时间趋势词云"""
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        results = {}

        for time_period, keywords in time_keywords.items():
            if keywords:
                title = f"{time_period} 词云趋势"
                save_path = os.path.join(save_dir, f"trend_{time_period}.png")

                result = self.generate_wordcloud(
                    keywords=keywords,
                    title=title,
                    save_path=save_path
                )

                if result:
                    results[time_period] = result

        return results

    def save_wordcloud_data(self, data, filename):
        """保存词云数据"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.info(f"词云数据已保存到: {filename}")
        except Exception as e:
            self.logger.error(f"保存词云数据失败: {e}")


class WordCloudStyler:
    """词云样式定制器"""

    @staticmethod
    def get_color_schemes():
        """获取可用的颜色方案"""
        return {
            'default': 'viridis',
            'warm': 'Reds',
            'cool': 'Blues',
            'forest': 'Greens',
            'sunset': 'Oranges',
            'ocean': 'Blues',
            'rainbow': 'rainbow',
            'pastel': 'Pastel1',
            'dark': 'Dark2'
        }

    @staticmethod
    def create_custom_colormap(colors):
        """创建自定义颜色映射"""
        from matplotlib.colors import LinearSegmentedColormap
        return LinearSegmentedColormap.from_list("custom", colors)

    @staticmethod
    def get_preset_configs():
        """获取预设配置"""
        return {
            'business': {
                'width': 1200,
                'height': 800,
                'max_words': 200,
                'background_color': 'white',
                'colormap': 'Blues',
                'relative_scaling': 0.5
            },
            'artistic': {
                'width': 800,
                'height': 600,
                'max_words': 150,
                'background_color': 'black',
                'colormap': 'plasma',
                'relative_scaling': 0.6
            },
            'minimal': {
                'width': 600,
                'height': 400,
                'max_words': 100,
                'background_color': 'white',
                'colormap': 'Greys',
                'relative_scaling': 0.3
            }
        }


if __name__ == "__main__":
    # 测试代码
    test_keywords = [
        ('好吃', 0.8),
        ('新鲜', 0.7),
        ('服务', 0.6),
        ('环境', 0.5),
        ('价格', 0.4),
        ('推荐', 0.3)
    ]

    generator = WordCloudGenerator()
    result = generator.generate_wordcloud(
        keywords=test_keywords,
        title="测试词云",
        save_path="test_wordcloud.png"
    )

    if result:
        print("词云生成成功")
        print(f"图片路径: {result['save_path']}")
        print(f"词汇数量: {result['word_count']}")
    else:
        print("词云生成失败")