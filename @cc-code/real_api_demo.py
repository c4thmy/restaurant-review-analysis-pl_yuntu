#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实API数据获取演示
Real API Data Collection Demo

使用真实的高德地图API获取餐厅数据
"""

import json
import os
import sys
import requests
import time
from datetime import datetime

# 设置控制台编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

def load_api_keys():
    """加载API密钥"""
    try:
        with open('api_keys_template.json', 'r', encoding='utf-8') as f:
            config = json.load(f)

        api_keys = {}
        for platform, key in config.items():
            if not platform.startswith('_') and key and 'your_' not in str(key):
                api_keys[platform] = key

        return api_keys
    except Exception as e:
        print(f"加载API密钥失败: {e}")
        return {}

def search_restaurants_amap(api_key, keyword="火锅", city="北京", limit=20):
    """使用高德地图API搜索餐厅"""

    print(f"正在使用高德地图API搜索: {keyword} in {city}")

    url = "https://restapi.amap.com/v3/place/text"
    params = {
        'key': api_key,
        'keywords': keyword,
        'city': city,
        'types': '050000',  # 餐饮服务
        'page': 1,
        'offset': limit,
        'output': 'json',
        'extensions': 'all'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get('status') == '1':
            pois = data.get('pois', [])
            restaurants = []

            for poi in pois:
                restaurant = {
                    'id': poi.get('id'),
                    'name': poi.get('name'),
                    'address': poi.get('address'),
                    'location': {
                        'lat': float(poi.get('location', '0,0').split(',')[1]),
                        'lng': float(poi.get('location', '0,0').split(',')[0])
                    },
                    'phone': poi.get('tel'),
                    'category': poi.get('type'),
                    'tags': poi.get('tag', '').split(';') if poi.get('tag') else [],
                    'source': 'amap_real_api',
                    'district': poi.get('adname'),
                    'business_area': poi.get('business_area')
                }
                restaurants.append(restaurant)

            print(f"成功获取 {len(restaurants)} 家真实餐厅数据")
            return restaurants

        else:
            error_msg = data.get('info', '未知错误')
            print(f"API调用失败: {error_msg}")
            return []

    except Exception as e:
        print(f"请求失败: {e}")
        return []

def analyze_real_data(restaurants):
    """分析真实餐厅数据"""

    print("开始分析真实餐厅数据...")

    # 基础统计
    total_count = len(restaurants)
    has_phone = len([r for r in restaurants if r.get('phone')])

    # 地区分布
    districts = {}
    for restaurant in restaurants:
        district = restaurant.get('district', '未知区域')
        districts[district] = districts.get(district, 0) + 1

    # 商圈分布
    business_areas = {}
    for restaurant in restaurants:
        area = restaurant.get('business_area', '未知商圈')
        if area and area != '未知商圈':
            business_areas[area] = business_areas.get(area, 0) + 1

    # 分析结果
    analysis = {
        'basic_stats': {
            'total_restaurants': total_count,
            'has_phone_number': has_phone,
            'phone_coverage': round(has_phone / total_count * 100, 1) if total_count > 0 else 0
        },
        'district_distribution': districts,
        'business_area_distribution': dict(sorted(business_areas.items(), key=lambda x: x[1], reverse=True)[:10]),
        'sample_restaurants': restaurants[:5]  # 前5家作为样本
    }

    return analysis

def save_real_data(restaurants, analysis, keyword, city):
    """保存真实数据和分析结果"""

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # 保存原始餐厅数据
    restaurants_file = f"data/real_amap_restaurants_{keyword}_{city}_{timestamp}.json"
    restaurants_data = {
        'metadata': {
            'source': 'amap_real_api',
            'keyword': keyword,
            'city': city,
            'total_count': len(restaurants),
            'fetch_time': datetime.now().isoformat(),
            'api_platform': '高德地图官方API'
        },
        'restaurants': restaurants
    }

    os.makedirs('data', exist_ok=True)
    with open(restaurants_file, 'w', encoding='utf-8') as f:
        json.dump(restaurants_data, f, ensure_ascii=False, indent=2)

    # 保存分析结果
    analysis_file = f"data/real_amap_analysis_{keyword}_{city}_{timestamp}.json"
    analysis_data = {
        'metadata': restaurants_data['metadata'],
        'analysis': analysis,
        'analysis_time': datetime.now().isoformat()
    }

    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, ensure_ascii=False, indent=2)

    print(f"真实数据已保存: {restaurants_file}")
    print(f"分析结果已保存: {analysis_file}")

    return restaurants_file, analysis_file

def display_results(analysis):
    """显示分析结果"""

    print("\n" + "="*50)
    print("真实餐厅数据分析结果")
    print("="*50)

    stats = analysis['basic_stats']
    print(f"餐厅总数: {stats['total_restaurants']}")
    print(f"有电话号码: {stats['has_phone_number']} ({stats['phone_coverage']}%)")

    print(f"\n地区分布 (前5个):")
    for district, count in list(analysis['district_distribution'].items())[:5]:
        print(f"  {district}: {count}家")

    print(f"\n热门商圈 (前5个):")
    for area, count in list(analysis['business_area_distribution'].items())[:5]:
        print(f"  {area}: {count}家")

    print(f"\n样本餐厅:")
    for i, restaurant in enumerate(analysis['sample_restaurants'], 1):
        print(f"  {i}. {restaurant['name']}")
        print(f"     地址: {restaurant['address']}")
        print(f"     电话: {restaurant.get('phone', '未提供')}")
        print()

def main():
    """主函数"""

    print("="*50)
    print("真实API餐厅数据获取演示")
    print("="*50)

    # 加载API密钥
    api_keys = load_api_keys()

    if 'amap' not in api_keys:
        print("错误: 未找到有效的高德地图API密钥")
        print("请确保在 api_keys_template.json 中配置了正确的密钥")
        return

    print(f"使用高德地图API密钥: {api_keys['amap'][:8]}...{api_keys['amap'][-4:]}")

    # 搜索参数
    keyword = "火锅"
    city = "北京"
    limit = 20

    print(f"搜索参数: {keyword} @ {city}, 获取 {limit} 家餐厅")
    print()

    # 获取真实数据
    restaurants = search_restaurants_amap(api_keys['amap'], keyword, city, limit)

    if not restaurants:
        print("未获取到餐厅数据，请检查API密钥和网络连接")
        return

    # 分析数据
    analysis = analyze_real_data(restaurants)

    # 保存数据
    restaurants_file, analysis_file = save_real_data(restaurants, analysis, keyword, city)

    # 显示结果
    display_results(analysis)

    print("="*50)
    print("真实数据获取完成!")
    print("="*50)
    print("下一步可以:")
    print(f"1. 查看餐厅数据: {restaurants_file}")
    print(f"2. 查看分析结果: {analysis_file}")
    print("3. 使用其他工具进一步分析:")
    print(f"   python ccc-main.py analyze {restaurants_file}")

if __name__ == "__main__":
    main()