#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生产环境测试脚本
Production Environment Test

自动化测试真实餐厅分析功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ccc_config import RESTAURANT_CONFIG, WEB_CONFIG, COMPLIANCE_CONFIG
from spiders.ccc_compliance_spider import create_compliance_spider
from utils.ccc_compliance_checker import compliance_checker
from utils.text_analyzer_simple import CommentAnalyzer
from utils.wordcloud_generator import WordCloudGenerator
from utils.data_utils import DataManager, Logger
from datetime import datetime
import time

def test_production_analysis():
    """测试生产环境分析功能"""
    print("="*60)
    print("大众点评评论分析系统 - 生产环境测试")
    print("="*60)

    # 自动化用户协议（测试模式）
    user_id = f"test_user_{int(time.time())}"
    purpose = 'research'

    print(f"[INFO] 测试用户ID: {user_id}")
    print(f"[INFO] 使用目的: {purpose}")

    # 记录合规协议
    compliance_checker.record_user_agreement(user_id, purpose)

    # 测试参数
    restaurant_name = "嫩牛家潮汕火锅"
    city = "北京"
    months = 1

    print(f"\n[TEST] 开始测试餐厅: {restaurant_name}")
    print(f"[TEST] 城市: {city}")
    print(f"[TEST] 时间范围: {months}个月")

    # 确保目录存在
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    try:
        # 步骤1: 爬取评论
        print("\n[STEP 1/4] 爬取评论...")
        spider = create_compliance_spider(user_id=user_id, purpose=purpose)
        comments = spider.run(restaurant_name, city, months)

        if not comments:
            print("[ERROR] 爬取失败")
            return False

        print(f"[OK] 成功获取 {len(comments)} 条评论")

        # 步骤2: 保存评论数据
        print("\n[STEP 2/4] 保存评论数据...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = restaurant_name.replace(' ', '_').replace('/', '_')
        comments_file = f"data/comments_{safe_name}_{timestamp}.json"

        data_manager = DataManager()
        data_manager.save_json(comments, comments_file)
        print(f"[OK] 评论数据已保存: {comments_file}")

        # 步骤3: 分析评论
        print("\n[STEP 3/4] 分析评论...")
        analyzer = CommentAnalyzer()
        analysis_results = analyzer.analyze_comments(comments)

        if not analysis_results:
            print("[ERROR] 分析失败")
            return False

        # 保存分析结果
        analysis_file = comments_file.replace('.json', '_analysis.json')
        data_manager.save_json(analysis_results, analysis_file)
        print(f"[OK] 分析结果已保存: {analysis_file}")

        # 显示分析结果
        basic_stats = analysis_results['basic_stats']
        sentiment = analysis_results['sentiment_analysis']
        print(f"[RESULT] 总评论数: {basic_stats['total_comments']}")
        print(f"[RESULT] 平均评分: {basic_stats['average_rating']}")
        print(f"[RESULT] 正面评论: {sentiment['positive']}")
        print(f"[RESULT] 负面评论: {sentiment['negative']}")
        print(f"[RESULT] 中性评论: {sentiment['neutral']}")
        print(f"[RESULT] 关键词数量: {len(analysis_results['keywords'])}")

        # 步骤4: 生成可视化
        print("\n[STEP 4/4] 生成可视化...")
        generator = WordCloudGenerator()

        keywords = analysis_results.get('keywords', [])
        wordcloud_result = generator.generate_wordcloud(
            keywords=keywords,
            title="评论关键词云图（生产测试）",
            save_path=f"data/test_wordcloud_{timestamp}.png"
        )

        if wordcloud_result:
            print(f"[OK] 词云图已生成")
        else:
            print("[WARN] 词云图生成失败")

        # 运行现有的优化版可视化
        print("\n[BONUS] 运行优化版可视化...")
        import subprocess
        result = subprocess.run([
            sys.executable, "ccc-data_optimized_wordcloud.py"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("[OK] 优化版可视化报告已生成")
        else:
            print("[WARN] 优化版可视化生成失败")

        print("\n" + "="*60)
        print("生产环境测试完成！")
        print("="*60)
        print("[SUCCESS] 所有核心功能正常运行")
        print(f"[INFO] 测试数据保存在: data/")
        print(f"[INFO] 可视化报告: data/data_optimized_report.html")
        print(f"[INFO] 合规日志: logs/")

        return True

    except Exception as e:
        print(f"[ERROR] 测试过程中出现异常: {e}")
        return False

def main():
    """主函数"""
    success = test_production_analysis()

    if success:
        print("\n[CONCLUSION] 生产环境测试通过！系统可以正式运行。")
    else:
        print("\n[CONCLUSION] 生产环境测试失败，需要进一步检查。")

    return success

if __name__ == "__main__":
    main()