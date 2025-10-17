#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
嫩牛家潮汕火锅深度数据分析工具
Deep Analysis Tool for Nenniu Chaoshan Hotpot

专门针对嫩牛家潮汕火锅品牌的全面数据分析
"""

import json
import requests
import time
from datetime import datetime
import os
import sys

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

def search_nenniu_stores(api_key):
    """搜索嫩牛家潮汕火锅在北京的所有门店"""

    print("🔍 开始搜索嫩牛家潮汕火锅在北京的门店...")

    # 多个关键词搜索确保全覆盖
    keywords = [
        "嫩牛家",
        "嫩牛家潮汕火锅",
        "嫩牛家火锅",
        "嫩牛家潮汕"
    ]

    all_stores = []

    for keyword in keywords:
        print(f"  正在搜索关键词: {keyword}")

        url = "https://restapi.amap.com/v3/place/text"
        params = {
            'key': api_key,
            'keywords': keyword,
            'city': '北京',
            'types': '050000',  # 餐饮服务
            'page': 1,
            'offset': 50,
            'output': 'json',
            'extensions': 'all'
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if data.get('status') == '1':
                pois = data.get('pois', [])

                for poi in pois:
                    # 只保留真正的嫩牛家门店
                    name = poi.get('name', '')
                    if '嫩牛家' in name:
                        store = {
                            'id': poi.get('id'),
                            'name': name,
                            'address': poi.get('address', ''),
                            'location': {
                                'lat': float(poi.get('location', '0,0').split(',')[1]) if poi.get('location') else 0,
                                'lng': float(poi.get('location', '0,0').split(',')[0]) if poi.get('location') else 0
                            },
                            'phone': poi.get('tel', ''),
                            'category': poi.get('type', ''),
                            'tags': poi.get('tag', '').split(';') if poi.get('tag') else [],
                            'district': poi.get('adname', ''),
                            'business_area': poi.get('business_area', ''),
                            'search_keyword': keyword,
                            'raw_data': poi
                        }
                        all_stores.append(store)

                print(f"    找到 {len(pois)} 家相关餐厅")
            else:
                print(f"    API返回错误: {data.get('info', '未知错误')}")

            time.sleep(0.5)  # 避免请求过频

        except Exception as e:
            print(f"    搜索 {keyword} 时出错: {e}")

    # 去重处理 - 基于餐厅ID去重
    unique_stores = {}
    for store in all_stores:
        store_id = store['id']
        if store_id not in unique_stores:
            unique_stores[store_id] = store

    final_stores = list(unique_stores.values())
    print(f"✅ 去重后总共找到 {len(final_stores)} 家嫩牛家门店")

    return final_stores

def analyze_store_distribution(stores):
    """分析门店分布策略"""

    print("\n📊 分析嫩牛家门店分布策略...")

    # 区域分布统计
    district_stats = {}
    business_area_stats = {}
    location_analysis = []

    for store in stores:
        # 区域统计
        district = store.get('district', '未知区域')
        district_stats[district] = district_stats.get(district, 0) + 1

        # 商圈统计
        business_area = store.get('business_area', '')
        if business_area:
            business_area_stats[business_area] = business_area_stats.get(business_area, 0) + 1

        # 位置详细分析
        location_info = {
            'name': store['name'],
            'district': district,
            'business_area': business_area,
            'address': store['address'],
            'coordinates': store['location']
        }
        location_analysis.append(location_info)

    # 门店命名模式分析
    naming_patterns = {}
    for store in stores:
        name = store['name']
        # 提取门店位置标识
        if '(' in name and ')' in name:
            location_tag = name.split('(')[1].split(')')[0]
            naming_patterns[location_tag] = naming_patterns.get(location_tag, 0) + 1

    distribution_analysis = {
        'total_stores': len(stores),
        'district_distribution': dict(sorted(district_stats.items(), key=lambda x: x[1], reverse=True)),
        'business_area_distribution': dict(sorted(business_area_stats.items(), key=lambda x: x[1], reverse=True)),
        'naming_patterns': dict(sorted(naming_patterns.items(), key=lambda x: x[1], reverse=True)),
        'store_locations': location_analysis,
        'coverage_analysis': {
            'districts_covered': len(district_stats),
            'business_areas_covered': len(business_area_stats),
            'average_stores_per_district': round(len(stores) / len(district_stats), 2) if district_stats else 0
        }
    }

    return distribution_analysis

def competitor_analysis(api_key):
    """竞品对比分析"""

    print("\n🥊 开始竞品对比分析...")

    # 主要火锅品牌竞品
    competitors = [
        "海底捞火锅",
        "呷哺呷哺",
        "小龙坎火锅",
        "巴奴毛肚火锅",
        "湊湊火锅",
        "大龙燚火锅",
        "蜀大侠火锅"
    ]

    competitor_data = {}

    for competitor in competitors:
        print(f"  正在分析竞品: {competitor}")

        url = "https://restapi.amap.com/v3/place/text"
        params = {
            'key': api_key,
            'keywords': competitor,
            'city': '北京',
            'types': '050000',
            'page': 1,
            'offset': 1,  # 只需要数量，不需要详细信息
            'output': 'json',
            'extensions': 'base'
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if data.get('status') == '1':
                count = int(data.get('count', 0))
                competitor_data[competitor] = {
                    'store_count': count,
                    'market_share_estimate': 0  # 后续计算
                }
                print(f"    {competitor}: {count} 家门店")
            else:
                print(f"    {competitor}: 查询失败")
                competitor_data[competitor] = {'store_count': 0, 'market_share_estimate': 0}

            time.sleep(0.3)

        except Exception as e:
            print(f"    分析 {competitor} 时出错: {e}")
            competitor_data[competitor] = {'store_count': 0, 'market_share_estimate': 0}

    # 计算市场份额估算
    total_competitor_stores = sum(data['store_count'] for data in competitor_data.values())

    if total_competitor_stores > 0:
        for competitor, data in competitor_data.items():
            data['market_share_estimate'] = round(data['store_count'] / total_competitor_stores * 100, 1)

    return competitor_data

def generate_business_insights(nenniu_analysis, competitor_data):
    """生成商业洞察"""

    print("\n💡 生成商业洞察...")

    nenniu_store_count = nenniu_analysis['total_stores']

    # 市场地位分析
    all_brands = dict(competitor_data)
    all_brands['嫩牛家潮汕火锅'] = {'store_count': nenniu_store_count}

    # 按门店数量排序
    brand_ranking = sorted(all_brands.items(), key=lambda x: x[1]['store_count'], reverse=True)

    # 找到嫩牛家的排名
    nenniu_rank = None
    for i, (brand, data) in enumerate(brand_ranking, 1):
        if brand == '嫩牛家潮汕火锅':
            nenniu_rank = i
            break

    # 选址策略分析
    district_dist = nenniu_analysis['district_distribution']
    top_districts = list(district_dist.items())[:3]

    # 扩张机会分析
    expansion_opportunities = []

    # 寻找门店密度较低但竞品较多的区域
    for competitor, data in competitor_data.items():
        if data['store_count'] > nenniu_store_count * 2:  # 竞品门店数量是嫩牛家的2倍以上
            expansion_opportunities.append({
                'opportunity_type': 'underserved_market',
                'description': f'{competitor}在北京有{data["store_count"]}家门店，显示该市场有较大需求',
                'recommendation': '考虑在热门商圈增加门店密度'
            })

    insights = {
        'market_position': {
            'total_stores': nenniu_store_count,
            'market_rank': nenniu_rank,
            'rank_description': f'在主要火锅品牌中排名第{nenniu_rank}位' if nenniu_rank else '排名待确定',
            'top_competitor': brand_ranking[0][0] if brand_ranking else None,
            'competitive_gap': brand_ranking[0][1]['store_count'] - nenniu_store_count if brand_ranking else 0
        },
        'location_strategy': {
            'primary_districts': top_districts,
            'coverage_breadth': nenniu_analysis['coverage_analysis']['districts_covered'],
            'strategy_type': '精品化选址' if nenniu_store_count < 10 else '规模化扩张',
            'density_analysis': nenniu_analysis['coverage_analysis']['average_stores_per_district']
        },
        'expansion_opportunities': expansion_opportunities,
        'brand_positioning': {
            'category': '潮汕火锅',
            'differentiation': '专业潮汕火锅，与传统四川火锅差异化竞争',
            'target_market': '追求正宗潮汕风味的消费者'
        }
    }

    return insights

def save_analysis_results(nenniu_stores, distribution_analysis, competitor_data, insights):
    """保存分析结果"""

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # 完整分析报告
    comprehensive_report = {
        'report_metadata': {
            'brand': '嫩牛家潮汕火锅',
            'analysis_city': '北京',
            'analysis_date': datetime.now().isoformat(),
            'data_source': '高德地图API',
            'report_type': '品牌深度分析报告'
        },
        'raw_data': {
            'store_details': nenniu_stores,
            'total_stores_found': len(nenniu_stores)
        },
        'distribution_analysis': distribution_analysis,
        'competitor_analysis': competitor_data,
        'business_insights': insights,
        'analysis_summary': {
            'key_findings': [
                f'嫩牛家在北京共有{len(nenniu_stores)}家门店',
                f'主要分布在{list(distribution_analysis["district_distribution"].keys())[:3]}',
                f'在火锅市场排名第{insights["market_position"]["market_rank"]}位' if insights["market_position"]["market_rank"] else '市场地位待确定'
            ]
        }
    }

    # 保存完整报告
    report_file = f'data/nenniu_comprehensive_analysis_北京_{timestamp}.json'
    os.makedirs('data', exist_ok=True)

    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(comprehensive_report, f, ensure_ascii=False, indent=2)

    print(f"📄 完整分析报告已保存: {report_file}")

    return comprehensive_report, report_file

def display_analysis_summary(report):
    """显示分析摘要"""

    print("\n" + "="*70)
    print("🎯 嫩牛家潮汕火锅深度分析报告")
    print("="*70)

    # 基本信息
    metadata = report['report_metadata']
    raw_data = report['raw_data']
    distribution = report['distribution_analysis']
    insights = report['business_insights']

    print(f"📊 分析概况:")
    print(f"  品牌: {metadata['brand']}")
    print(f"  城市: {metadata['analysis_city']}")
    print(f"  门店总数: {raw_data['total_stores_found']} 家")
    print(f"  分析时间: {metadata['analysis_date'][:19]}")

    # 门店分布
    print(f"\n🗺️ 门店分布分析:")
    print(f"  覆盖区域: {distribution['coverage_analysis']['districts_covered']} 个区")
    print(f"  平均密度: {distribution['coverage_analysis']['average_stores_per_district']} 家/区")

    print(f"\n📍 主要分布区域:")
    for district, count in list(distribution['district_distribution'].items())[:5]:
        percentage = round(count / raw_data['total_stores_found'] * 100, 1)
        print(f"  {district}: {count} 家 ({percentage}%)")

    if distribution['business_area_distribution']:
        print(f"\n🏢 热门商圈:")
        for area, count in list(distribution['business_area_distribution'].items())[:3]:
            print(f"  {area}: {count} 家门店")

    # 市场地位
    market_pos = insights['market_position']
    print(f"\n🏆 市场地位分析:")
    print(f"  市场排名: {market_pos['rank_description']}")
    if market_pos['top_competitor']:
        print(f"  领先品牌: {market_pos['top_competitor']}")
        print(f"  门店差距: {market_pos['competitive_gap']} 家")

    # 竞品对比
    competitor_data = report['competitor_analysis']
    print(f"\n🥊 主要竞品对比:")
    sorted_competitors = sorted(competitor_data.items(), key=lambda x: x[1]['store_count'], reverse=True)
    for brand, data in sorted_competitors[:5]:
        print(f"  {brand}: {data['store_count']} 家 ({data['market_share_estimate']}%)")

    # 门店详情展示
    print(f"\n🏪 门店详情样本:")
    for i, store in enumerate(raw_data['store_details'][:3], 1):
        print(f"  {i}. {store['name']}")
        print(f"     📍 {store['address']}")
        print(f"     📞 {store['phone'] if store['phone'] else '暂无电话'}")
        print(f"     🏢 {store['district']} {store['business_area']}")
        print()

    # 商业洞察
    brand_pos = insights['brand_positioning']
    print(f"💡 关键洞察:")
    print(f"  品牌定位: {brand_pos['category']} - {brand_pos['differentiation']}")
    print(f"  选址策略: {insights['location_strategy']['strategy_type']}")
    print(f"  目标市场: {brand_pos['target_market']}")

    if insights['expansion_opportunities']:
        print(f"\n🚀 扩张建议:")
        for opp in insights['expansion_opportunities'][:2]:
            print(f"  • {opp['description']}")

    return report

def main():
    """主函数"""

    print("="*70)
    print("🎯 嫩牛家潮汕火锅深度数据分析系统")
    print("="*70)
    print("正在启动分析引擎...")

    # 检查API密钥
    api_keys = load_api_keys()
    if 'amap' not in api_keys:
        print("❌ 错误: 未找到有效的高德地图API密钥")
        print("请确保在 api_keys_template.json 中配置了正确的密钥")
        return

    api_key = api_keys['amap']
    print(f"✅ API密钥加载成功: {api_key[:8]}...{api_key[-4:]}")

    try:
        # 第1步: 搜索嫩牛家门店
        print(f"\n{'='*50}")
        print("第1步: 搜索嫩牛家门店数据")
        print('='*50)
        nenniu_stores = search_nenniu_stores(api_key)

        if not nenniu_stores:
            print("❌ 未找到嫩牛家门店数据，分析终止")
            return

        # 第2步: 分析门店分布
        print(f"\n{'='*50}")
        print("第2步: 分析门店分布策略")
        print('='*50)
        distribution_analysis = analyze_store_distribution(nenniu_stores)

        # 第3步: 竞品分析
        print(f"\n{'='*50}")
        print("第3步: 竞品对比分析")
        print('='*50)
        competitor_data = competitor_analysis(api_key)

        # 第4步: 生成商业洞察
        print(f"\n{'='*50}")
        print("第4步: 生成商业洞察")
        print('='*50)
        insights = generate_business_insights(distribution_analysis, competitor_data)

        # 第5步: 保存和展示结果
        print(f"\n{'='*50}")
        print("第5步: 生成分析报告")
        print('='*50)
        report, report_file = save_analysis_results(
            nenniu_stores, distribution_analysis, competitor_data, insights
        )

        # 展示分析结果
        display_analysis_summary(report)

        print("\n" + "="*70)
        print("✅ 嫩牛家潮汕火锅深度分析完成!")
        print("="*70)
        print(f"📄 详细报告文件: {report_file}")
        print(f"📊 数据文件可用于进一步分析:")
        print(f"   python ccc-main.py analyze {report_file}")
        print("="*70)

    except KeyboardInterrupt:
        print("\n\n⚠️ 分析被用户中断")
    except Exception as e:
        print(f"\n❌ 分析过程出现错误: {e}")
        print("请检查网络连接和API密钥配置")

if __name__ == "__main__":
    main()