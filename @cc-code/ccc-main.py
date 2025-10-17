#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大众点评餐厅评论分析系统 - 合规版主程序
确保所有操作符合法律法规和伦理要求

法律声明：本工具仅供学习和研究使用
"""

import os
import sys
import argparse
import json
import time
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入合规配置
try:
    from ccc_config import RESTAURANT_CONFIG, WEB_CONFIG, COMPLIANCE_CONFIG
    from spiders.ccc_compliance_spider import create_compliance_spider
    from utils.ccc_compliance_checker import compliance_checker
    COMPLIANCE_MODE = True
    print("[OK] 合规模式已启用")
except ImportError:
    # 回退到基础模式
    from config import RESTAURANT_CONFIG, WEB_CONFIG
    from spiders.dianping_spider import DianpingSpider
    COMPLIANCE_MODE = False
    print("[WARN] 使用基础模式运行")

from utils.text_analyzer_simple import CommentAnalyzer
from utils.wordcloud_generator import WordCloudGenerator
from utils.data_utils import DataManager, Logger


def show_legal_notice():
    """显示法律声明"""
    notice = """
╔════════════════════════════════════════════════════════════════╗
║                         法律声明                                 ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  本软件仅供学习、研究和学术用途使用                                 ║
║                                                                ║
║  使用前请确认：                                                  ║
║  [OK] 已阅读并同意用户协议 (USER_AGREEMENT.md)                     ║
║  [OK] 已明确研究目的 (RESEARCH_PURPOSE.md)                        ║
║  [OK] 将遵守所有相关法律法规                                         ║
║  [OK] 不会将数据用于商业或非法目的                                   ║
║                                                                ║
║  注意事项：                                                      ║
║  - 系统内置频率限制和数据量限制                                   ║
║  - 所有数据将自动进行隐私保护处理                                 ║
║  - 数据保留期限为30天，请及时清理                                 ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""
    print(notice)


def check_compliance_files():
    """检查必要的合规文件"""
    required_files = [
        'USER_AGREEMENT.md',
        'RESEARCH_PURPOSE.md'
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"[ERROR] 缺少必要的合规文件: {', '.join(missing_files)}")
        print("请确保项目目录包含所有必要的法律文件")
        return False

    return True


def get_user_agreement():
    """获取用户协议确认"""
    if not COMPLIANCE_MODE:
        return True

    print("\n" + "="*60)
    print("使用条款确认")
    print("="*60)

    print("1. 您确认已阅读并理解用户协议 (USER_AGREEMENT.md) 吗？")
    print("2. 您确认使用目的仅限于学习和研究吗？")
    print("3. 您承诺遵守所有法律法规和网站使用条款吗？")
    print("4. 您理解数据将被匿名化处理且有保留期限吗？")

    while True:
        response = input("\n请输入 'yes' 表示同意，'no' 表示拒绝: ").lower().strip()
        if response == 'yes':
            return True
        elif response == 'no':
            print("[ERROR] 未同意使用条款，程序退出")
            return False
        else:
            print("请输入 'yes' 或 'no'")


def get_research_purpose():
    """获取研究目的"""
    print("\n请选择您的使用目的：")
    print("1. research - 学术研究")
    print("2. learning - 技术学习")
    print("3. academic - 课程作业")

    while True:
        choice = input("请输入选项编号 (1-3): ").strip()
        purpose_map = {
            '1': 'research',
            '2': 'learning',
            '3': 'academic'
        }

        if choice in purpose_map:
            purpose = purpose_map[choice]
            print(f"[OK] 使用目的: {purpose}")
            return purpose
        else:
            print("请输入有效的选项编号")


def crawl_comments(restaurant_name, city='北京', months=1, user_id=None, purpose='research'):
    """爬取评论"""
    logger = Logger.setup('main')
    logger.info(f"开始爬取 {restaurant_name} 的评论")

    try:
        if COMPLIANCE_MODE:
            # 使用合规爬虫
            spider = create_compliance_spider(user_id=user_id, purpose=purpose)
            comments = spider.run(restaurant_name, city, months)
        else:
            # 使用基础爬虫
            spider = DianpingSpider()
            comments = spider.run()

        return comments

    except Exception as e:
        logger.error(f"爬取失败: {e}")
        return []


def analyze_comments(comments_file):
    """分析评论"""
    logger = Logger.setup('main')
    logger.info(f"开始分析评论文件: {comments_file}")

    data_manager = DataManager()
    analyzer = CommentAnalyzer()

    try:
        # 加载评论数据
        data = data_manager.load_json(comments_file)

        if not data:
            logger.error("评论数据加载失败")
            return None

        # 处理数据格式（支持新的数据包格式）
        if isinstance(data, dict) and 'comments' in data:
            comments = data['comments']
            metadata = data.get('metadata', {})
            logger.info(f"加载数据包，包含 {len(comments)} 条评论")
        else:
            comments = data
            metadata = {}

        # 分析评论
        results = analyzer.analyze_comments(comments)

        # 添加元数据
        results['source_metadata'] = metadata
        results['analysis_compliance'] = {
            'privacy_protected': True,
            'anonymized': True,
            'retention_period': '30_days'
        }

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
            title="评论关键词云图（研究用途）",
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
            'timestamp': timestamp,
            'compliance_note': '图像用于学术研究，已移除个人信息'
        }

        logger.info("词云生成完成")
        return results

    except Exception as e:
        logger.error(f"词云生成失败: {e}")
        return None


def run_full_pipeline(restaurant_name, city='北京', months=1, user_id=None, purpose='research'):
    """运行完整流程"""
    logger = Logger.setup('main')
    logger.info("开始运行完整分析流程")

    # 限制参数
    months = min(months, 1)  # 最多1个月

    print(f"\n开始分析流程...")
    print(f"餐厅: {restaurant_name}")
    print(f"城市: {city}")
    print(f"时间范围: {months}个月")
    print(f"用户ID: {user_id}")
    print(f"目的: {purpose}")

    # 1. 爬取评论
    print("\n步骤 1/3: 爬取评论...")
    comments = crawl_comments(restaurant_name, city, months, user_id, purpose)
    if not comments:
        print("[ERROR] 爬取失败，流程终止")
        return

    print(f"[OK] 成功爬取 {len(comments)} 条评论")

    # 2. 分析评论
    print("\n步骤 2/3: 分析评论...")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_name = restaurant_name.replace(' ', '_').replace('/', '_')
    comments_file = f"data/comments_{safe_name}_{timestamp}.json"

    # 先保存评论数据
    data_manager = DataManager()
    data_manager.save_json(comments, comments_file)

    analysis_results = analyze_comments(comments_file)
    if not analysis_results:
        print("[ERROR] 分析失败，流程终止")
        return

    print("[OK] 评论分析完成")

    # 3. 生成词云
    print("\n步骤 3/3: 生成词云...")
    analysis_file = comments_file.replace('.json', '_analysis.json')
    wordcloud_results = generate_wordcloud(analysis_file)

    if wordcloud_results:
        print("[OK] 词云生成完成")
        print(f"[OK] 结果保存在 data 目录下")
    else:
        print("[WARN] 词云生成失败")

    print("\n" + "="*50)
    print("完整流程执行完成！")
    print("="*50)
    print("重要提醒：")
    print("- 所有数据已进行隐私保护处理")
    print("- 请仅将结果用于声明的研究目的")
    print("- 请在30天内删除相关数据文件")
    print("- 如需发表研究成果，请确保符合学术伦理要求")


def start_web_server():
    """启动Web服务器"""
    print("启动Web服务器...")
    print(f"访问地址: http://{WEB_CONFIG['host']}:{WEB_CONFIG['port']}")

    if COMPLIANCE_MODE:
        print("Web界面已启用合规模式")
        from web.ccc_compliance_app import create_app
    else:
        from web.app import create_app

    app = create_app()
    app.run(
        host=WEB_CONFIG['host'],
        port=WEB_CONFIG['port'],
        debug=WEB_CONFIG.get('debug', False)
    )


def check_data_retention():
    """检查数据保留期限"""
    if not os.path.exists('data'):
        return

    print("\n检查数据保留期限...")
    from datetime import timedelta

    expired_files = []
    for root, dirs, files in os.walk('data'):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                create_time = datetime.fromtimestamp(os.path.getctime(filepath))
                if (datetime.now() - create_time) > timedelta(days=30):
                    expired_files.append(filepath)
            except:
                continue

    if expired_files:
        print(f"[WARN] 发现 {len(expired_files)} 个超过保留期限的文件")
        print("建议删除以下文件：")
        for file in expired_files[:5]:  # 只显示前5个
            print(f"  - {file}")
        if len(expired_files) > 5:
            print(f"  ... 还有 {len(expired_files) - 5} 个文件")

        if input("\n是否自动删除过期文件？(y/N): ").lower() == 'y':
            for file in expired_files:
                try:
                    os.remove(file)
                    print(f"已删除: {file}")
                except:
                    print(f"删除失败: {file}")


def main():
    """主函数"""
    # 显示法律声明
    show_legal_notice()

    # 检查合规文件
    if COMPLIANCE_MODE and not check_compliance_files():
        return

    # 检查数据保留期限
    check_data_retention()

    parser = argparse.ArgumentParser(
        description='大众点评餐厅评论分析系统 (合规版)',
        epilog='本工具仅供学习和研究使用，请遵守相关法律法规'
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 爬取命令
    crawl_parser = subparsers.add_parser('crawl', help='爬取评论 (学术研究用)')
    crawl_parser.add_argument('restaurant', help='餐厅名称')
    crawl_parser.add_argument('--city', default='北京', help='城市名称')
    crawl_parser.add_argument('--months', type=int, default=1, choices=[1], help='时间范围（最多1个月）')

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
    pipeline_parser.add_argument('--months', type=int, default=1, choices=[1], help='时间范围（最多1个月）')

    # Web服务器命令
    web_parser = subparsers.add_parser('web', help='启动Web服务器')

    # 合规检查命令
    if COMPLIANCE_MODE:
        compliance_parser = subparsers.add_parser('compliance', help='生成合规报告')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 确保数据目录存在
    os.makedirs('data', exist_ok=True)
    os.makedirs('backup', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    # 获取用户同意
    if args.command in ['crawl', 'pipeline'] and COMPLIANCE_MODE:
        if not get_user_agreement():
            return

        purpose = get_research_purpose()
        user_id = f"user_{int(time.time())}"

        # 记录用户协议
        compliance_checker.record_user_agreement(user_id, purpose)
    else:
        purpose = 'research'
        user_id = None

    if args.command == 'crawl':
        comments = crawl_comments(args.restaurant, args.city, args.months, user_id, purpose)
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
        run_full_pipeline(args.restaurant, args.city, args.months, user_id, purpose)

    elif args.command == 'web':
        start_web_server()

    elif args.command == 'compliance' and COMPLIANCE_MODE:
        report = compliance_checker.generate_compliance_report()
        print("合规报告已生成")
        print(f"合规状态: {report['compliance_status']}")
        if report['recommendations']:
            print("建议:")
            for rec in report['recommendations']:
                print(f"  - {rec}")


if __name__ == '__main__':
    main()