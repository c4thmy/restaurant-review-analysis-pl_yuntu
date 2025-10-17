#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
官方API餐厅数据获取测试工具
Test tool for Official API Restaurant Data Collection

测试版本，修复了字符编码问题，可以直接运行演示
"""

import json
import os
import sys
from datetime import datetime

# 设置控制台编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

def create_demo_api_data():
    """创建演示API数据"""
    print("创建演示API数据...")

    demo_data = {
        "summary": {
            "keyword": "火锅",
            "city": "北京",
            "timestamp": datetime.now().isoformat(),
            "platforms_used": ["高德地图(演示)", "百度地图(演示)", "腾讯地图(演示)"],
            "total_found": 15
        },
        "restaurants": []
    }

    # 生成15家餐厅数据
    for i in range(1, 16):
        restaurant = {
            "id": f"demo_restaurant_{i}",
            "name": f"火锅店{i}",
            "address": f"北京市朝阳区示例街道{i}号",
            "location": {
                "lat": 39.9 + i * 0.001,
                "lng": 116.4 + i * 0.001
            },
            "phone": f"010-1234{i:04d}",
            "category": "火锅",
            "rating": 4.0 + (i % 10) * 0.1,
            "tags": ["火锅", "川菜", "聚餐"],
            "source": "demo_api",
            "unique_id": f"demo_{i}"
        }
        demo_data["restaurants"].append(restaurant)

    demo_data["raw_count"] = len(demo_data["restaurants"])
    demo_data["deduplicated_count"] = len(demo_data["restaurants"])

    return demo_data

def convert_to_comments_format(api_data):
    """将API数据转换为评论格式"""
    print("转换数据格式为评论分析格式...")

    comments = []
    comment_id = 1

    for restaurant in api_data["restaurants"]:
        # 餐厅基本信息转为"评论"
        info_comment = {
            "id": f"info_{comment_id}",
            "content": f"餐厅名称：{restaurant['name']}，地址：{restaurant['address']}，类型：{restaurant['category']}",
            "rating": restaurant.get("rating", 4.0),
            "user_id": "system_info",
            "timestamp": datetime.now().isoformat(),
            "restaurant_id": restaurant["id"],
            "restaurant_name": restaurant["name"],
            "source": f"官方API_{restaurant.get('source', 'unknown')}",
            "tags": restaurant.get("tags", [])
        }
        comments.append(info_comment)
        comment_id += 1

        # 添加几条模拟评论
        sample_reviews = [
            f"这家{restaurant['name']}味道不错，环境也很好",
            f"{restaurant['name']}的服务很到位，菜品新鲜",
            f"朋友聚餐选择{restaurant['name']}，大家都很满意",
            f"{restaurant['name']}性价比很高，推荐试试"
        ]

        for review_text in sample_reviews[:2]:  # 每家餐厅2条评论
            review = {
                "id": f"review_{comment_id}",
                "content": review_text,
                "rating": restaurant.get("rating", 4.0) + (-0.5 + comment_id % 3 * 0.5),
                "user_id": f"user_{comment_id % 100}",
                "timestamp": datetime.now().isoformat(),
                "restaurant_id": restaurant["id"],
                "restaurant_name": restaurant["name"],
                "source": "demo_review",
                "tags": restaurant.get("tags", [])
            }
            comments.append(review)
            comment_id += 1

    comments_data = {
        "metadata": {
            "total_comments": len(comments),
            "source": "official_api_demo",
            "keyword": api_data["summary"]["keyword"],
            "city": api_data["summary"]["city"],
            "generated_time": datetime.now().isoformat(),
            "api_platforms": api_data["summary"]["platforms_used"],
            "data_type": "restaurant_info_and_reviews"
        },
        "comments": comments
    }

    return comments_data

def simple_text_analysis(comments_data):
    """简化的文本分析"""
    print("执行简化文本分析...")

    comments = comments_data["comments"]
    total_comments = len(comments)

    # 基础统计
    ratings = [c.get("rating", 4.0) for c in comments]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0

    # 简单关键词提取
    all_text = " ".join([c.get("content", "") for c in comments])

    # 常见餐厅相关词汇
    keywords = []
    food_words = ["火锅", "味道", "服务", "环境", "菜品", "新鲜", "性价比", "推荐", "聚餐", "满意"]

    for word in food_words:
        if word in all_text:
            count = all_text.count(word)
            keywords.append({"word": word, "count": count, "weight": count * 0.1})

    # 情感分析（简化版）
    positive_words = ["不错", "很好", "满意", "推荐", "新鲜"]
    negative_words = ["不好", "差", "难吃", "贵"]

    positive_count = sum(all_text.count(word) for word in positive_words)
    negative_count = sum(all_text.count(word) for word in negative_words)

    sentiment = {
        "positive": positive_count,
        "negative": negative_count,
        "neutral": total_comments - positive_count - negative_count
    }

    analysis_results = {
        "basic_stats": {
            "total_comments": total_comments,
            "average_rating": round(avg_rating, 2),
            "rating_distribution": {
                "5.0": len([r for r in ratings if r >= 4.5]),
                "4.0": len([r for r in ratings if 3.5 <= r < 4.5]),
                "3.0": len([r for r in ratings if 2.5 <= r < 3.5]),
                "2.0": len([r for r in ratings if 1.5 <= r < 2.5]),
                "1.0": len([r for r in ratings if r < 1.5])
            }
        },
        "keywords": keywords,
        "sentiment": sentiment,
        "labels": {
            "category_keywords": {
                "口味": [{"word": "味道", "weight": 0.8}, {"word": "菜品", "weight": 0.7}],
                "服务": [{"word": "服务", "weight": 0.9}],
                "环境": [{"word": "环境", "weight": 0.8}],
                "价格": [{"word": "性价比", "weight": 0.6}]
            }
        },
        "source_metadata": comments_data["metadata"],
        "analysis_time": datetime.now().isoformat(),
        "analysis_type": "official_api_demo"
    }

    return analysis_results

def save_json_file(data, filename):
    """保存JSON文件"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"文件已保存: {filename}")
    return filename

def main():
    """主函数 - 演示完整流程"""
    print("="*50)
    print("官方API餐厅数据处理演示")
    print("="*50)

    try:
        # 确保数据目录存在
        os.makedirs('data', exist_ok=True)

        # 步骤1: 创建演示API数据
        print("\n步骤 1/4: 创建演示API数据...")
        api_data = create_demo_api_data()

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        api_file = save_json_file(api_data, f"data/demo_api_restaurants_火锅_北京_{timestamp}.json")
        print(f"成功创建 {len(api_data['restaurants'])} 家餐厅数据")

        # 步骤2: 转换数据格式
        print("\n步骤 2/4: 转换数据格式...")
        comments_data = convert_to_comments_format(api_data)
        comments_file = save_json_file(comments_data, f"data/demo_comments_火锅_北京_{timestamp}.json")
        print(f"成功转换为 {len(comments_data['comments'])} 条评论数据")

        # 步骤3: 文本分析
        print("\n步骤 3/4: 执行文本分析...")
        analysis_results = simple_text_analysis(comments_data)
        analysis_file = save_json_file(analysis_results, f"data/demo_comments_火锅_北京_{timestamp}_analysis.json")
        print(f"分析完成，平均评分: {analysis_results['basic_stats']['average_rating']}")

        # 步骤4: 简化的结果展示
        print("\n步骤 4/4: 结果展示...")
        print("="*50)
        print("分析结果摘要:")
        print(f"  总评论数: {analysis_results['basic_stats']['total_comments']}")
        print(f"  平均评分: {analysis_results['basic_stats']['average_rating']}")
        print(f"  关键词数: {len(analysis_results['keywords'])}")

        print("\n主要关键词:")
        for kw in analysis_results['keywords'][:5]:
            print(f"  - {kw['word']}: 出现{kw['count']}次")

        print("\n情感分析:")
        sentiment = analysis_results['sentiment']
        print(f"  正面: {sentiment['positive']}")
        print(f"  中性: {sentiment['neutral']}")
        print(f"  负面: {sentiment['negative']}")

        print("\n="*50)
        print("演示完成! 生成的文件:")
        print(f"  API数据: {api_file}")
        print(f"  评论数据: {comments_file}")
        print(f"  分析结果: {analysis_file}")
        print("="*50)

        print("\n下一步建议:")
        print("1. 申请真实API密钥替换演示数据")
        print("2. 使用 python ccc-main.py analyze 分析实际数据")
        print("3. 集成到您的应用系统中")

        return {
            "success": True,
            "api_file": api_file,
            "comments_file": comments_file,
            "analysis_file": analysis_file,
            "summary": analysis_results['basic_stats']
        }

    except Exception as e:
        print(f"\n错误: 演示执行失败 - {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    main()