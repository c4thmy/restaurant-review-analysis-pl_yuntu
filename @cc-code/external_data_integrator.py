#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
外部数据源集成器
External Data Source Integrator

支持集成第三方工具获取的数据
"""

import json
import os
import pandas as pd
from datetime import datetime
from pathlib import Path

class ExternalDataIntegrator:
    """外部数据源集成器"""

    def __init__(self):
        self.supported_formats = ['json', 'csv', 'xlsx', 'txt']
        self.required_fields = ['comment_text', 'rating', 'date']

    def validate_data_format(self, data_file):
        """验证数据格式"""
        try:
            if data_file.endswith('.json'):
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            elif data_file.endswith('.csv'):
                data = pd.read_csv(data_file).to_dict('records')
            elif data_file.endswith('.xlsx'):
                data = pd.read_excel(data_file).to_dict('records')
            else:
                return False, "不支持的文件格式"

            # 检查必要字段
            if isinstance(data, list) and len(data) > 0:
                sample = data[0]
                missing_fields = [field for field in self.required_fields
                                if field not in sample]
                if missing_fields:
                    return False, f"缺少必要字段: {missing_fields}"

            return True, "数据格式验证通过"

        except Exception as e:
            return False, f"数据验证失败: {e}"

    def convert_to_standard_format(self, data_file, output_file=None):
        """转换为标准格式"""
        try:
            # 读取数据
            if data_file.endswith('.json'):
                with open(data_file, 'r', encoding='utf-8') as f:
                    raw_data = json.load(f)
            elif data_file.endswith('.csv'):
                raw_data = pd.read_csv(data_file).to_dict('records')
            elif data_file.endswith('.xlsx'):
                raw_data = pd.read_excel(data_file).to_dict('records')

            # 转换为标准格式
            standardized_data = []
            for item in raw_data:
                standard_item = {
                    "comment_id": item.get('id', f"ext_{len(standardized_data)}"),
                    "user_id_hash": f"external_user_{hash(str(item.get('user_id', 'anonymous'))) % 10000}",
                    "rating": self.normalize_rating(item.get('rating', 0)),
                    "comment_text": str(item.get('comment_text', '')),
                    "date": self.normalize_date(item.get('date', '')),
                    "restaurant_name": item.get('restaurant_name', '外部数据餐厅'),
                    "city": item.get('city', '未知城市'),
                    "privacy_protected": True,
                    "source": "external_tool"
                }
                standardized_data.append(standard_item)

            # 保存标准格式数据
            if not output_file:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = f"data/external_comments_{timestamp}.json"

            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(standardized_data, f, ensure_ascii=False, indent=2)

            return True, output_file, len(standardized_data)

        except Exception as e:
            return False, f"转换失败: {e}", 0

    def normalize_rating(self, rating):
        """标准化评分"""
        try:
            rating = float(rating)
            # 假设输入评分是1-5分制
            return max(1, min(5, rating))
        except:
            return 3  # 默认中等评分

    def normalize_date(self, date_str):
        """标准化日期"""
        try:
            # 尝试多种日期格式
            formats = ['%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d', '%Y-%m-%d %H:%M:%S']
            for fmt in formats:
                try:
                    parsed_date = datetime.strptime(str(date_str), fmt)
                    return parsed_date.strftime('%Y-%m-%d')
                except:
                    continue
            return datetime.now().strftime('%Y-%m-%d')
        except:
            return datetime.now().strftime('%Y-%m-%d')

    def filter_september_2025_data(self, data_file):
        """筛选2025年9月数据"""
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            filtered_data = []
            for item in data:
                date_str = item.get('date', '')
                if date_str.startswith('2025-09'):
                    filtered_data.append(item)

            # 保存筛选后的数据
            filtered_file = data_file.replace('.json', '_september_2025.json')
            with open(filtered_file, 'w', encoding='utf-8') as f:
                json.dump(filtered_data, f, ensure_ascii=False, indent=2)

            return True, filtered_file, len(filtered_data)

        except Exception as e:
            return False, f"筛选失败: {e}", 0

    def generate_data_report(self, data_file):
        """生成数据报告"""
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            report = {
                "数据概况": {
                    "总评论数": len(data),
                    "数据来源": "外部工具",
                    "处理时间": datetime.now().isoformat()
                },
                "评分分布": {},
                "时间分布": {},
                "餐厅分布": {}
            }

            # 统计评分分布
            ratings = [item.get('rating', 0) for item in data]
            for rating in [1, 2, 3, 4, 5]:
                report["评分分布"][f"{rating}分"] = ratings.count(rating)

            # 统计时间分布
            dates = [item.get('date', '')[:7] for item in data]  # 年-月
            date_counts = {}
            for date in dates:
                date_counts[date] = date_counts.get(date, 0) + 1
            report["时间分布"] = date_counts

            # 统计餐厅分布
            restaurants = [item.get('restaurant_name', '') for item in data]
            restaurant_counts = {}
            for restaurant in restaurants:
                restaurant_counts[restaurant] = restaurant_counts.get(restaurant, 0) + 1
            report["餐厅分布"] = restaurant_counts

            return report

        except Exception as e:
            return {"错误": f"报告生成失败: {e}"}

def create_integration_workflow():
    """创建数据集成工作流程"""
    integrator = ExternalDataIntegrator()

    print("=" * 60)
    print("外部数据源集成工作流程")
    print("=" * 60)

    print("\n[INFO] 支持的数据格式:")
    print("  - JSON格式 (.json)")
    print("  - CSV格式 (.csv)")
    print("  - Excel格式 (.xlsx)")

    print("\n[INFO] 必要的数据字段:")
    print("  - comment_text: 评论文本")
    print("  - rating: 评分 (1-5)")
    print("  - date: 日期 (YYYY-MM-DD)")

    print("\n[INFO] 可选的数据字段:")
    print("  - restaurant_name: 餐厅名称")
    print("  - city: 城市")
    print("  - user_id: 用户ID")

    print("\n[WORKFLOW] 集成步骤:")
    print("1. 使用外部工具获取数据")
    print("2. 将数据保存为支持的格式")
    print("3. 运行数据验证和转换")
    print("4. 筛选特定时间段数据")
    print("5. 集成到现有分析流程")

    return integrator

def main():
    """主函数 - 演示数据集成流程"""
    integrator = create_integration_workflow()

    # 创建示例数据文件说明
    example_data = {
        "示例数据格式": [
            {
                "comment_text": "味道很好，服务不错，环境也很舒适",
                "rating": 4.5,
                "date": "2025-09-15",
                "restaurant_name": "嫩牛家潮汕火锅(朝阳门店)",
                "city": "北京",
                "user_id": "user123"
            },
            {
                "comment_text": "价格有点贵，但是食材新鲜",
                "rating": 3.8,
                "date": "2025-09-20",
                "restaurant_name": "嫩牛家潮汕火锅(三里屯店)",
                "city": "北京",
                "user_id": "user456"
            }
        ]
    }

    # 保存示例数据格式
    os.makedirs('data', exist_ok=True)
    with open('data/example_external_data_format.json', 'w', encoding='utf-8') as f:
        json.dump(example_data, f, ensure_ascii=False, indent=2)

    print(f"\n[CREATED] 示例数据格式文件: data/example_external_data_format.json")
    print("\n[NEXT] 请按照示例格式准备您的数据文件，然后运行集成流程")

if __name__ == "__main__":
    main()