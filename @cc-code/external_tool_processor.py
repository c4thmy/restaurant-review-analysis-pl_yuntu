#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
外部工具数据处理器
External Tool Data Processor

专门处理从reqabl或其他工具获取的评论数据
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.text_analyzer_simple import CommentAnalyzer
from utils.data_utils import DataManager
from external_data_integrator import ExternalDataIntegrator

def process_external_data(data_file):
    """处理外部工具获取的数据"""
    print("=" * 60)
    print("外部工具数据处理流程")
    print("=" * 60)

    # 创建集成器
    integrator = ExternalDataIntegrator()
    data_manager = DataManager()
    analyzer = CommentAnalyzer()

    # 步骤1: 验证数据格式
    print("\n[STEP 1/6] 验证数据格式...")
    is_valid, message = integrator.validate_data_format(data_file)
    if not is_valid:
        print(f"[ERROR] {message}")
        return False

    print(f"[OK] {message}")

    # 步骤2: 转换为标准格式
    print("\n[STEP 2/6] 转换为标准格式...")
    success, output_file, count = integrator.convert_to_standard_format(data_file)
    if not success:
        print(f"[ERROR] {output_file}")
        return False

    print(f"[OK] 已转换 {count} 条评论数据")
    print(f"[INFO] 标准格式文件: {output_file}")

    # 步骤3: 筛选2025年9月数据
    print("\n[STEP 3/6] 筛选2025年9月数据...")
    success, filtered_file, filtered_count = integrator.filter_september_2025_data(output_file)
    if not success:
        print(f"[ERROR] {filtered_file}")
        print("[INFO] 使用全部数据继续处理")
        filtered_file = output_file
        filtered_count = count

    print(f"[OK] 筛选出 {filtered_count} 条2025年9月评论")

    # 步骤4: 生成数据报告
    print("\n[STEP 4/6] 生成数据质量报告...")
    report = integrator.generate_data_report(filtered_file)

    report_file = filtered_file.replace('.json', '_report.json')
    data_manager.save_json(report, report_file)
    print(f"[OK] 数据报告已生成: {report_file}")

    # 显示数据概况
    if "数据概况" in report:
        概况 = report["数据概况"]
        print(f"[INFO] 总评论数: {概况['总评论数']}")

    if "评分分布" in report:
        评分分布 = report["评分分布"]
        print(f"[INFO] 评分分布: {评分分布}")

    # 步骤5: 运行情感分析
    print("\n[STEP 5/6] 运行情感分析...")
    with open(filtered_file, 'r', encoding='utf-8') as f:
        comments_data = json.load(f)

    analysis_results = analyzer.analyze_comments(comments_data)

    analysis_file = filtered_file.replace('.json', '_analysis.json')
    data_manager.save_json(analysis_results, analysis_file)
    print(f"[OK] 分析结果已保存: {analysis_file}")

    # 显示分析结果
    basic_stats = analysis_results['basic_stats']
    sentiment = analysis_results['sentiment_analysis']
    print(f"[RESULT] 平均评分: {basic_stats['average_rating']}")
    print(f"[RESULT] 正面评论: {sentiment['positive']}")
    print(f"[RESULT] 负面评论: {sentiment['negative']}")
    print(f"[RESULT] 关键词数量: {len(analysis_results['keywords'])}")

    # 步骤6: 生成可视化报告
    print("\n[STEP 6/6] 生成可视化报告...")

    # 更新词云数据以便可视化系统使用
    wordcloud_data = {
        "timestamp": datetime.now().isoformat(),
        "words": [],
        "max_size": 30,
        "total_words": 0
    }

    # 转换关键词格式
    for keyword, freq in analysis_results['keywords']:
        wordcloud_data["words"].append({
            "text": keyword,
            "size": min(30, 20 + freq * 2),
            "frequency": freq,
            "type": "keyword"
        })

    # 转换标签格式
    for tag, freq in analysis_results['tags']:
        wordcloud_data["words"].append({
            "text": tag,
            "size": min(28, 18 + freq * 2),
            "frequency": freq,
            "type": "tag"
        })

    wordcloud_data["total_words"] = len(wordcloud_data["words"])

    # 保存词云数据
    wordcloud_file = "data/wordcloud_data.json"
    data_manager.save_json(wordcloud_data, wordcloud_file)

    # 运行可视化生成器
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "ccc-data_optimized_wordcloud.py"
        ], capture_output=True, text=True, cwd=".")

        if result.returncode == 0:
            print("[OK] 可视化报告已生成")
            print("[INFO] 查看报告: data/data_optimized_report.html")
        else:
            print("[WARN] 可视化生成出现问题，但数据分析已完成")

    except Exception as e:
        print(f"[WARN] 可视化生成失败: {e}")

    print("\n" + "=" * 60)
    print("外部数据处理完成！")
    print("=" * 60)
    print(f"[SUCCESS] 已处理 {filtered_count} 条评论")
    print(f"[FILES] 标准格式: {output_file}")
    print(f"[FILES] 筛选数据: {filtered_file}")
    print(f"[FILES] 分析结果: {analysis_file}")
    print(f"[FILES] 数据报告: {report_file}")

    return True

def create_sample_reqabl_data():
    """创建reqabl工具数据示例"""
    sample_data = [
        {
            "comment_text": "这家潮汕火锅真的很正宗，牛肉新鲜，手打牛肉丸特别好吃",
            "rating": 4.8,
            "date": "2025-09-05",
            "restaurant_name": "嫩牛家潮汕火锅(朝阳门店)",
            "city": "北京",
            "user_id": "dp_user_001",
            "shop_url": "https://www.dianping.com/shop/123456",
            "review_id": "rev_001"
        },
        {
            "comment_text": "环境很好，服务态度也不错，就是价格有点贵，不过食材确实新鲜",
            "rating": 4.2,
            "date": "2025-09-08",
            "restaurant_name": "嫩牛家潮汕火锅(三里屯店)",
            "city": "北京",
            "user_id": "dp_user_002",
            "shop_url": "https://www.dianping.com/shop/789012",
            "review_id": "rev_002"
        },
        {
            "comment_text": "沙茶酱味道很棒，火锅底料也很香，排队时间有点长但值得等待",
            "rating": 4.5,
            "date": "2025-09-12",
            "restaurant_name": "嫩牛家潮汕火锅(王府井店)",
            "city": "北京",
            "user_id": "dp_user_003",
            "shop_url": "https://www.dianping.com/shop/345678",
            "review_id": "rev_003"
        },
        {
            "comment_text": "整体还可以，但是性价比不高，同样的价格可以找到更好的选择",
            "rating": 3.2,
            "date": "2025-09-15",
            "restaurant_name": "嫩牛家潮汕火锅(西单店)",
            "city": "北京",
            "user_id": "dp_user_004",
            "shop_url": "https://www.dianping.com/shop/901234",
            "review_id": "rev_004"
        },
        {
            "comment_text": "菜品丰富，口感很棒，服务员很热情，环境也很舒适，推荐！",
            "rating": 4.7,
            "date": "2025-09-20",
            "restaurant_name": "嫩牛家潮汕火锅(CBD店)",
            "city": "北京",
            "user_id": "dp_user_005",
            "shop_url": "https://www.dianping.com/shop/567890",
            "review_id": "rev_005"
        }
    ]

    # 保存示例数据
    os.makedirs('data', exist_ok=True)
    sample_file = 'data/reqabl_sample_data.json'
    with open(sample_file, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)

    print(f"[CREATED] 示例数据文件: {sample_file}")
    return sample_file

def main():
    """主函数"""
    print("外部工具数据处理器")
    print("支持处理reqabl等工具获取的评论数据")
    print()

    # 检查是否有数据文件参数
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
        if os.path.exists(data_file):
            print(f"[INFO] 处理数据文件: {data_file}")
            process_external_data(data_file)
        else:
            print(f"[ERROR] 文件不存在: {data_file}")
    else:
        # 创建并处理示例数据
        print("[INFO] 未指定数据文件，创建示例数据进行演示")
        sample_file = create_sample_reqabl_data()
        print(f"[INFO] 使用示例数据: {sample_file}")
        print()
        process_external_data(sample_file)

        print("\n[USAGE] 使用您的数据文件:")
        print("python external_tool_processor.py your_data_file.json")

if __name__ == "__main__":
    main()