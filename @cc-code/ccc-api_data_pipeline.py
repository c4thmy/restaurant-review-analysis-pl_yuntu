#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
官方API数据完整处理pipeline
Official API Data Processing Pipeline

将官方API获取的餐厅数据与现有的分析系统集成
支持：数据获取 -> 数据分析 -> 词云生成 -> 结果展示的完整流程
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List

# 导入现有模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ccc_official_api_client import MultiAPIRestaurantSearcher
except ImportError:
    # 如果无法导入，使用本地类定义
    class MultiAPIRestaurantSearcher:
        def __init__(self, api_keys):
            self.api_keys = api_keys

        def search_all_platforms(self, keyword, city, limit_per_platform):
            # 返回演示数据
            return {
                'summary': {
                    'keyword': keyword,
                    'city': city,
                    'platforms_used': ['演示平台'],
                    'total_found': 15
                },
                'restaurants': [
                    {
                        'id': f'demo_{i}',
                        'name': f'{keyword}店{i}',
                        'address': f'{city}市示例区街道{i}号',
                        'location': {'lat': 39.9 + i*0.001, 'lng': 116.4 + i*0.001},
                        'phone': f'010-1234{i:04d}',
                        'category': keyword,
                        'rating': 4.0 + (i % 10) * 0.1,
                        'tags': [keyword, '美食'],
                        'source': 'demo'
                    }
                    for i in range(1, 16)
                ],
                'raw_count': 15,
                'deduplicated_count': 15
            }

        def save_results(self, results, filename=None):
            if not filename:
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                keyword = results['summary']['keyword'].replace(' ', '_')
                city = results['summary']['city']
                filename = f"data/demo_api_restaurants_{keyword}_{city}_{timestamp}.json"

            import os
            import json
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            print(f"演示数据已保存到: {filename}")
            return filename
from utils.text_analyzer_simple import CommentAnalyzer
from utils.wordcloud_generator import WordCloudGenerator
from utils.data_utils import DataManager, Logger

class OfficialAPIDataProcessor:
    """官方API数据处理器"""

    def __init__(self, api_keys_file: str = 'api_keys_template.json'):
        """
        初始化数据处理器

        Args:
            api_keys_file: API密钥配置文件路径
        """
        self.logger = Logger.setup('api_processor')
        self.data_manager = DataManager()
        self.api_keys = self.load_api_keys(api_keys_file)

        if self.api_keys:
            self.searcher = MultiAPIRestaurantSearcher(self.api_keys)
        else:
            self.searcher = None
            self.logger.warning("未找到有效API密钥，将使用演示模式")

    def load_api_keys(self, api_keys_file: str) -> Dict[str, str]:
        """加载API密钥"""
        try:
            if not os.path.exists(api_keys_file):
                self.logger.warning(f"API密钥文件不存在: {api_keys_file}")
                return {}

            with open(api_keys_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 过滤有效的API密钥
            valid_keys = {}
            for platform, key in config.items():
                if not platform.startswith('_') and key and 'your_' not in key:
                    valid_keys[platform] = key

            if valid_keys:
                self.logger.info(f"成功加载API密钥: {list(valid_keys.keys())}")
            else:
                self.logger.warning("未找到有效的API密钥")

            return valid_keys

        except Exception as e:
            self.logger.error(f"加载API密钥失败: {e}")
            return {}

    def search_restaurants(self, keyword: str, city: str, limit_per_platform: int = 20) -> str:
        """
        搜索餐厅数据

        Args:
            keyword: 搜索关键词
            city: 城市名称
            limit_per_platform: 每个平台的结果数量

        Returns:
            数据文件路径
        """
        self.logger.info(f"开始搜索餐厅: {keyword} in {city}")

        if self.searcher:
            # 使用真实API搜索
            results = self.searcher.search_all_platforms(keyword, city, limit_per_platform)
        else:
            # 使用演示数据
            results = self._create_demo_data(keyword, city)

        # 保存原始API数据
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_keyword = keyword.replace(' ', '_').replace('/', '_')
        api_data_file = f"data/api_restaurants_{safe_keyword}_{city}_{timestamp}.json"

        self.data_manager.save_json(results, api_data_file)
        self.logger.info(f"API数据已保存: {api_data_file}")

        return api_data_file

    def _create_demo_data(self, keyword: str, city: str) -> Dict:
        """创建演示数据"""
        self.logger.info("使用演示模式创建模拟数据")

        demo_restaurants = []
        for i in range(1, 21):  # 生成20家餐厅
            restaurant = {
                'id': f'demo_{keyword}_{i}',
                'name': f'{keyword}店{i}',
                'address': f'{city}市示例区示例街{i}号',
                'location': {
                    'lat': 39.9 + i * 0.001,
                    'lng': 116.4 + i * 0.001
                },
                'phone': f'010-1234{i:04d}',
                'category': keyword,
                'rating': 3.5 + (i % 10) * 0.15,
                'tags': [keyword, '美食', '聚餐'],
                'source': 'demo',
                'unique_id': f'demo_{i}',
                'demo_reviews': [
                    f'这家{keyword}店味道不错，服务很好',
                    f'环境优雅，{keyword}很正宗',
                    f'性价比很高，推荐这家{keyword}',
                    f'朋友聚餐的好地方，{keyword}很有特色',
                    f'下次还会再来，{keyword}质量很棒'
                ]
            }
            demo_restaurants.append(restaurant)

        return {
            'summary': {
                'keyword': keyword,
                'city': city,
                'timestamp': datetime.now().isoformat(),
                'platforms_used': ['演示数据'],
                'total_found': len(demo_restaurants)
            },
            'restaurants': demo_restaurants,
            'raw_count': len(demo_restaurants),
            'deduplicated_count': len(demo_restaurants)
        }

    def convert_to_comments_format(self, api_data_file: str) -> str:
        """
        将API数据转换为评论分析格式

        Args:
            api_data_file: API数据文件路径

        Returns:
            评论格式数据文件路径
        """
        self.logger.info("转换API数据为评论分析格式")

        # 加载API数据
        api_data = self.data_manager.load_json(api_data_file)
        if not api_data:
            raise ValueError("无法加载API数据文件")

        # 转换为评论格式
        comments = []
        comment_id = 1

        for restaurant in api_data['restaurants']:
            # 基础餐厅信息转换为"评论"
            restaurant_info = {
                'id': f'info_{comment_id}',
                'content': f"餐厅名称：{restaurant['name']}，地址：{restaurant['address']}，类型：{restaurant.get('category', '餐厅')}",
                'rating': restaurant.get('rating', 4.0),
                'user_id': 'system_info',
                'timestamp': datetime.now().isoformat(),
                'restaurant_id': restaurant['id'],
                'restaurant_name': restaurant['name'],
                'source': f"官方API_{restaurant.get('source', 'unknown')}",
                'tags': restaurant.get('tags', [])
            }
            comments.append(restaurant_info)
            comment_id += 1

            # 如果有演示评论，也添加进去
            if 'demo_reviews' in restaurant:
                for review_text in restaurant['demo_reviews']:
                    review = {
                        'id': f'review_{comment_id}',
                        'content': review_text,
                        'rating': restaurant.get('rating', 4.0) + (-0.5 + comment_id % 3 * 0.5),
                        'user_id': f'user_{comment_id % 100}',
                        'timestamp': datetime.now().isoformat(),
                        'restaurant_id': restaurant['id'],
                        'restaurant_name': restaurant['name'],
                        'source': 'demo_review',
                        'tags': restaurant.get('tags', [])
                    }
                    comments.append(review)
                    comment_id += 1

        # 创建评论数据包
        comments_data = {
            'metadata': {
                'total_comments': len(comments),
                'source': 'official_api',
                'keyword': api_data['summary']['keyword'],
                'city': api_data['summary']['city'],
                'generated_time': datetime.now().isoformat(),
                'api_platforms': api_data['summary']['platforms_used'],
                'data_type': 'restaurant_info_and_reviews'
            },
            'comments': comments
        }

        # 保存评论格式数据
        comments_file = api_data_file.replace('api_restaurants_', 'comments_')
        self.data_manager.save_json(comments_data, comments_file)
        self.logger.info(f"评论格式数据已保存: {comments_file}")

        return comments_file

    def run_full_pipeline(self, keyword: str, city: str, limit_per_platform: int = 20) -> Dict:
        """
        运行完整的数据处理pipeline

        Args:
            keyword: 搜索关键词
            city: 城市名称
            limit_per_platform: 每个平台的结果数量

        Returns:
            处理结果摘要
        """
        self.logger.info("开始运行完整数据处理pipeline")

        results = {
            'keyword': keyword,
            'city': city,
            'start_time': datetime.now().isoformat(),
            'steps': {},
            'files': {},
            'success': False
        }

        try:
            # 步骤1: 搜索餐厅数据
            print("📡 步骤 1/4: 搜索餐厅数据...")
            api_data_file = self.search_restaurants(keyword, city, limit_per_platform)
            results['files']['api_data'] = api_data_file
            results['steps']['search'] = {'status': 'success', 'file': api_data_file}
            print("✅ 餐厅数据搜索完成")

            # 步骤2: 转换数据格式
            print("🔄 步骤 2/4: 转换数据格式...")
            comments_file = self.convert_to_comments_format(api_data_file)
            results['files']['comments'] = comments_file
            results['steps']['convert'] = {'status': 'success', 'file': comments_file}
            print("✅ 数据格式转换完成")

            # 步骤3: 文本分析
            print("🧠 步骤 3/4: 执行文本分析...")
            analysis_file = self.analyze_comments(comments_file)
            results['files']['analysis'] = analysis_file
            results['steps']['analyze'] = {'status': 'success', 'file': analysis_file}
            print("✅ 文本分析完成")

            # 步骤4: 生成词云
            print("☁️ 步骤 4/4: 生成词云...")
            wordcloud_results = self.generate_wordcloud(analysis_file)
            results['files']['wordcloud'] = wordcloud_results
            results['steps']['wordcloud'] = {'status': 'success', 'results': wordcloud_results}
            print("✅ 词云生成完成")

            results['success'] = True
            results['end_time'] = datetime.now().isoformat()

            print("\n" + "="*60)
            print("🎉 完整pipeline执行成功!")
            print("="*60)
            print(f"📊 搜索关键词: {keyword}")
            print(f"📍 目标城市: {city}")
            print(f"📁 数据文件: {comments_file}")
            print(f"📈 分析文件: {analysis_file}")
            print(f"☁️ 词云文件: {wordcloud_results.get('overall', {}).get('file', 'N/A') if wordcloud_results else 'N/A'}")
            print("="*60)

        except Exception as e:
            self.logger.error(f"Pipeline执行失败: {e}")
            results['error'] = str(e)
            results['success'] = False
            print(f"❌ Pipeline执行失败: {e}")

        return results

    def analyze_comments(self, comments_file: str) -> str:
        """分析评论数据"""
        self.logger.info("开始分析评论数据")

        analyzer = CommentAnalyzer()
        data = self.data_manager.load_json(comments_file)

        if not data:
            raise ValueError("无法加载评论数据")

        # 提取评论内容
        comments = data.get('comments', [])
        results = analyzer.analyze_comments(comments)

        # 添加元数据
        results['source_metadata'] = data.get('metadata', {})
        results['analysis_time'] = datetime.now().isoformat()
        results['analysis_type'] = 'official_api_data'

        # 保存分析结果
        analysis_file = comments_file.replace('.json', '_analysis.json')
        self.data_manager.save_json(results, analysis_file)

        self.logger.info(f"分析结果已保存: {analysis_file}")
        return analysis_file

    def generate_wordcloud(self, analysis_file: str) -> Dict:
        """生成词云"""
        self.logger.info("开始生成词云")

        generator = WordCloudGenerator()
        analysis_data = self.data_manager.load_json(analysis_file)

        if not analysis_data:
            raise ValueError("无法加载分析数据")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 生成整体词云
        keywords = analysis_data.get('keywords', [])
        overall_result = generator.generate_wordcloud(
            keywords=keywords,
            title="官方API餐厅数据词云图",
            save_path=f"data/api_wordcloud_overall_{timestamp}.png"
        )

        # 生成分类词云
        category_keywords = analysis_data.get('labels', {}).get('category_keywords', {})
        category_results = generator.generate_category_wordclouds(
            category_keywords,
            save_dir=f"data/api_category_wordclouds_{timestamp}"
        )

        results = {
            'overall': overall_result,
            'categories': category_results,
            'timestamp': timestamp,
            'source': 'official_api_data'
        }

        self.logger.info("词云生成完成")
        return results

def main():
    """主函数 - 演示完整pipeline"""
    print("🏪 官方API餐厅数据完整处理pipeline")
    print("支持：数据获取 -> 分析 -> 词云生成")
    print("="*60)

    # 初始化处理器
    processor = OfficialAPIDataProcessor()

    # 运行演示pipeline
    print("🚀 开始演示完整处理流程...")

    # 使用示例参数
    keyword = "火锅"
    city = "北京"

    results = processor.run_full_pipeline(keyword, city, limit_per_platform=10)

    # 保存pipeline结果
    pipeline_file = f"data/pipeline_results_{keyword}_{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    processor.data_manager.save_json(results, pipeline_file)

    print(f"\n📋 Pipeline结果已保存: {pipeline_file}")

    if results['success']:
        print("\n💡 下一步操作建议:")
        print("1. 申请真实API密钥以获取实际数据")
        print("2. 修改搜索参数以适应您的需求")
        print("3. 将结果集成到您的应用中")
    else:
        print(f"\n❌ Pipeline执行失败: {results.get('error', '未知错误')}")

    return results

if __name__ == "__main__":
    main()