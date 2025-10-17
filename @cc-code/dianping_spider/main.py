#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大众点评餐厅评论分析系统
主程序入口
"""

import os
import sys
import argparse
import json
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import RESTAURANT_CONFIG, WEB_CONFIG
from spiders.dianping_spider import DianpingSpider
from utils.text_analyzer import CommentAnalyzer
from utils.wordcloud_generator import WordCloudGenerator
from utils.data_utils import DataManager, Logger
from web.app import create_app


def crawl_comments(restaurant_name, city='北京', months=3):
    """爬取评论"""
    logger = Logger.setup('main')
    logger.info(f"开始爬取 {restaurant_name} 的评论")

    spider = DianpingSpider()
    try:
        # 更新配置
        RESTAURANT_CONFIG['name'] = restaurant_name
        RESTAURANT_CONFIG['city'] = city
        RESTAURANT_CONFIG['comment_months'] = months

        comments = spider.run()
        return comments

    except Exception as e:
        logger.error(f"爬取失败: {e}")
        return []
    finally:
        spider.close()


def analyze_comments(comments_file):
    """分析评论"""
    logger = Logger.setup('main')
    logger.info(f"开始分析评论文件: {comments_file}")

    data_manager = DataManager()
    analyzer = CommentAnalyzer()

    try:
        # 加载评论数据
        comments = data_manager.load_json(comments_file)
        if not comments:
            logger.error("评论数据加载失败")
            return None

        # 分析评论
        results = analyzer.analyze_comments(comments)

        # 保存分析结果
        analysis_file = comments_file.replace('.json', '_analysis.json')
        data_manager.save_json(results, analysis_file)

        logger.info(f"分析完成，结果保存到: {analysis_file}")
        return results

    except Exception as e:
        logger.error(f"分析失败: {e}")
        return None


def generate_wordcloud(analysis_file):
    """生成词云"""
    logger = Logger.setup('main')
    logger.info(f"开始生成词云: {analysis_file}")

    data_manager = DataManager()
    generator = WordCloudGenerator()

    try:
        # 加载分析数据
        analysis_data = data_manager.load_json(analysis_file)
        if not analysis_data:
            logger.error("分析数据加载失败")
            return None

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 生成总体词云
        keywords = analysis_data.get('keywords', [])
        overall_result = generator.generate_wordcloud(
            keywords=keywords,
            title="评论关键词云图",
            save_path=f"data/wordcloud_overall_{timestamp}.png"
        )

        # 生成分类词云
        category_keywords = analysis_data.get('labels', {}).get('category_keywords', {})
        category_results = generator.generate_category_wordclouds(
            category_keywords,
            save_dir=f"data/category_wordclouds_{timestamp}"
        )

        results = {
            'overall': overall_result,
            'categories': category_results,
            'timestamp': timestamp
        }

        logger.info("词云生成完成")
        return results

    except Exception as e:
        logger.error(f"词云生成失败: {e}")
        return None


def run_full_pipeline(restaurant_name, city='北京', months=3):
    """运行完整流程"""
    logger = Logger.setup('main')
    logger.info("开始运行完整分析流程")

    # 1. 爬取评论
    print("步骤 1/3: 爬取评论...")
    comments = crawl_comments(restaurant_name, city, months)
    if not comments:
        print("爬取失败，流程终止")
        return

    print(f"成功爬取 {len(comments)} 条评论")

    # 2. 分析评论
    print("步骤 2/3: 分析评论...")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    comments_file = f"comments_{restaurant_name}_{timestamp}.json"

    data_manager = DataManager()
    data_manager.save_json(comments, comments_file)

    analysis_results = analyze_comments(comments_file)
    if not analysis_results:
        print("分析失败，流程终止")
        return

    print("评论分析完成")

    # 3. 生成词云
    print("步骤 3/3: 生成词云...")
    analysis_file = comments_file.replace('.json', '_analysis.json')
    wordcloud_results = generate_wordcloud(analysis_file)

    if wordcloud_results:
        print("词云生成完成")
        print(f"结果保存在 data 目录下")
    else:
        print("词云生成失败")

    print("完整流程执行完成！")


def start_web_server():
    """启动Web服务器"""
    print("启动Web服务器...")
    print(f"访问地址: http://{WEB_CONFIG['host']}:{WEB_CONFIG['port']}")

    app = create_app()
    app.run(
        host=WEB_CONFIG['host'],
        port=WEB_CONFIG['port'],
        debug=WEB_CONFIG['debug']
    )


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='大众点评餐厅评论分析系统')

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 爬取命令
    crawl_parser = subparsers.add_parser('crawl', help='爬取评论')
    crawl_parser.add_argument('restaurant', help='餐厅名称')
    crawl_parser.add_argument('--city', default='北京', help='城市名称')
    crawl_parser.add_argument('--months', type=int, default=3, help='时间范围（月）')

    # 分析命令
    analyze_parser = subparsers.add_parser('analyze', help='分析评论')
    analyze_parser.add_argument('file', help='评论文件路径')

    # 词云命令
    wordcloud_parser = subparsers.add_parser('wordcloud', help='生成词云')
    wordcloud_parser.add_argument('file', help='分析结果文件路径')

    # 完整流程命令
    pipeline_parser = subparsers.add_parser('pipeline', help='运行完整流程')
    pipeline_parser.add_argument('restaurant', help='餐厅名称')
    pipeline_parser.add_argument('--city', default='北京', help='城市名称')
    pipeline_parser.add_argument('--months', type=int, default=3, help='时间范围（月）')

    # Web服务器命令
    web_parser = subparsers.add_parser('web', help='启动Web服务器')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 确保数据目录存在
    os.makedirs('data', exist_ok=True)
    os.makedirs('backup', exist_ok=True)

    if args.command == 'crawl':
        comments = crawl_comments(args.restaurant, args.city, args.months)
        print(f"爬取完成，获得 {len(comments)} 条评论")

    elif args.command == 'analyze':
        results = analyze_comments(args.file)
        if results:
            print("分析完成")
            print(f"总评论数: {results['basic_stats']['total_comments']}")
            print(f"平均评分: {results['basic_stats']['average_rating']}")
        else:
            print("分析失败")

    elif args.command == 'wordcloud':
        results = generate_wordcloud(args.file)
        if results:
            print("词云生成完成")
        else:
            print("词云生成失败")

    elif args.command == 'pipeline':
        run_full_pipeline(args.restaurant, args.city, args.months)

    elif args.command == 'web':
        start_web_server()


if __name__ == '__main__':
    main()