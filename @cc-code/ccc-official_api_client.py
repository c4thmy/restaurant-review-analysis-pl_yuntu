#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
官方API餐厅数据获取系统
Official API Restaurant Data Collection System

支持多个主流地图平台的官方API接口：
- 高德地图 POI API
- 百度地图 Place API
- 腾讯位置服务 API

完全合法，数据质量高，适合商业和学术使用
"""

import requests
import json
import time
import hashlib
from datetime import datetime
from urllib.parse import urlencode
import os
from typing import Dict, List, Optional

class OfficialAPIConfig:
    """官方API配置类"""

    def __init__(self):
        self.apis = {
            'amap': {
                'name': '高德地图API',
                'base_url': 'https://restapi.amap.com/v3',
                'endpoints': {
                    'poi_search': '/place/text',
                    'poi_detail': '/place/detail'
                },
                'key_required': True,
                'doc_url': 'https://lbs.amap.com/api/webservice/guide/api/search'
            },
            'baidu': {
                'name': '百度地图API',
                'base_url': 'https://api.map.baidu.com',
                'endpoints': {
                    'poi_search': '/place/v2/search',
                    'poi_detail': '/place/v2/detail'
                },
                'key_required': True,
                'doc_url': 'https://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi'
            },
            'tencent': {
                'name': '腾讯位置服务API',
                'base_url': 'https://apis.map.qq.com/ws',
                'endpoints': {
                    'poi_search': '/place/v1/search',
                    'poi_detail': '/place/v1/detail'
                },
                'key_required': True,
                'doc_url': 'https://lbs.qq.com/service/webService/webServiceGuide/webServiceSearch'
            }
        }

class RestaurantAPIClient:
    """餐厅数据API客户端"""

    def __init__(self, api_keys: Dict[str, str] = None):
        """
        初始化API客户端

        Args:
            api_keys: API密钥字典 {'amap': 'your_key', 'baidu': 'your_key', 'tencent': 'your_key'}
        """
        self.config = OfficialAPIConfig()
        self.api_keys = api_keys or {}
        self.session = requests.Session()
        self.setup_session()

    def setup_session(self):
        """设置请求会话"""
        self.session.headers.update({
            'User-Agent': 'RestaurantDataAnalysis/1.0 (Educational Use)',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def search_restaurants_amap(self, keyword: str, city: str, page: int = 1, limit: int = 20) -> Dict:
        """
        使用高德地图API搜索餐厅

        Args:
            keyword: 搜索关键词（餐厅名称或类型）
            city: 城市名称
            page: 页码
            limit: 每页结果数量
        """
        if 'amap' not in self.api_keys:
            raise ValueError("请先配置高德地图API密钥")

        params = {
            'key': self.api_keys['amap'],
            'keywords': keyword,
            'city': city,
            'types': '050000',  # 餐饮服务类型
            'page': page,
            'offset': limit,
            'output': 'json',
            'extensions': 'all'
        }

        url = f"{self.config.apis['amap']['base_url']}{self.config.apis['amap']['endpoints']['poi_search']}"

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            if data.get('status') == '1':
                return self._format_amap_results(data)
            else:
                print(f"高德API错误: {data.get('info', '未知错误')}")
                return {'restaurants': [], 'total': 0}

        except Exception as e:
            print(f"高德API请求失败: {e}")
            return {'restaurants': [], 'total': 0}

    def search_restaurants_baidu(self, keyword: str, city: str, page: int = 1, limit: int = 20) -> Dict:
        """
        使用百度地图API搜索餐厅

        Args:
            keyword: 搜索关键词
            city: 城市名称
            page: 页码
            limit: 每页结果数量
        """
        if 'baidu' not in self.api_keys:
            raise ValueError("请先配置百度地图API密钥")

        params = {
            'ak': self.api_keys['baidu'],
            'query': keyword,
            'tag': '美食',
            'region': city,
            'page_num': page - 1,  # 百度从0开始
            'page_size': limit,
            'output': 'json',
            'scope': '2'  # 返回详细信息
        }

        url = f"{self.config.apis['baidu']['base_url']}{self.config.apis['baidu']['endpoints']['poi_search']}"

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            if data.get('status') == 0:
                return self._format_baidu_results(data)
            else:
                print(f"百度API错误: {data.get('message', '未知错误')}")
                return {'restaurants': [], 'total': 0}

        except Exception as e:
            print(f"百度API请求失败: {e}")
            return {'restaurants': [], 'total': 0}

    def search_restaurants_tencent(self, keyword: str, city: str, page: int = 1, limit: int = 20) -> Dict:
        """
        使用腾讯位置服务API搜索餐厅

        Args:
            keyword: 搜索关键词
            city: 城市名称
            page: 页码
            limit: 每页结果数量
        """
        if 'tencent' not in self.api_keys:
            raise ValueError("请先配置腾讯地图API密钥")

        params = {
            'key': self.api_keys['tencent'],
            'keyword': keyword,
            'boundary': f'region({city},0)',
            'page_index': page,
            'page_size': limit,
            'orderby': '_score',
            'filter': 'category=美食'
        }

        url = f"{self.config.apis['tencent']['base_url']}{self.config.apis['tencent']['endpoints']['poi_search']}"

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            if data.get('status') == 0:
                return self._format_tencent_results(data)
            else:
                print(f"腾讯API错误: {data.get('message', '未知错误')}")
                return {'restaurants': [], 'total': 0}

        except Exception as e:
            print(f"腾讯API请求失败: {e}")
            return {'restaurants': [], 'total': 0}

    def _format_amap_results(self, data: Dict) -> Dict:
        """格式化高德API结果"""
        restaurants = []

        for poi in data.get('pois', []):
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
                'rating': None,  # 高德API不直接提供评分
                'tags': poi.get('tag', '').split(';') if poi.get('tag') else [],
                'source': 'amap',
                'raw_data': poi
            }
            restaurants.append(restaurant)

        return {
            'restaurants': restaurants,
            'total': int(data.get('count', 0)),
            'source': 'amap'
        }

    def _format_baidu_results(self, data: Dict) -> Dict:
        """格式化百度API结果"""
        restaurants = []

        for poi in data.get('results', []):
            restaurant = {
                'id': poi.get('uid'),
                'name': poi.get('name'),
                'address': poi.get('address'),
                'location': {
                    'lat': poi.get('location', {}).get('lat'),
                    'lng': poi.get('location', {}).get('lng')
                },
                'phone': poi.get('telephone'),
                'category': poi.get('detail_info', {}).get('tag'),
                'rating': poi.get('detail_info', {}).get('overall_rating'),
                'tags': [],
                'source': 'baidu',
                'raw_data': poi
            }
            restaurants.append(restaurant)

        return {
            'restaurants': restaurants,
            'total': int(data.get('total', 0)),
            'source': 'baidu'
        }

    def _format_tencent_results(self, data: Dict) -> Dict:
        """格式化腾讯API结果"""
        restaurants = []

        for poi in data.get('data', []):
            restaurant = {
                'id': poi.get('id'),
                'name': poi.get('title'),
                'address': poi.get('address'),
                'location': {
                    'lat': poi.get('location', {}).get('lat'),
                    'lng': poi.get('location', {}).get('lng')
                },
                'phone': poi.get('tel'),
                'category': poi.get('category'),
                'rating': None,  # 腾讯API不直接提供评分
                'tags': [],
                'source': 'tencent',
                'raw_data': poi
            }
            restaurants.append(restaurant)

        return {
            'restaurants': restaurants,
            'total': int(data.get('count', 0)),
            'source': 'tencent'
        }

class MultiAPIRestaurantSearcher:
    """多API餐厅搜索器"""

    def __init__(self, api_keys: Dict[str, str]):
        """
        初始化多API搜索器

        Args:
            api_keys: 各平台API密钥
        """
        self.client = RestaurantAPIClient(api_keys)
        self.available_apis = [api for api in api_keys.keys() if api_keys[api]]

    def search_all_platforms(self, keyword: str, city: str, limit_per_platform: int = 20) -> Dict:
        """
        在所有可用平台搜索餐厅

        Args:
            keyword: 搜索关键词
            city: 城市名称
            limit_per_platform: 每个平台的结果数量限制
        """
        all_results = []
        summary = {
            'keyword': keyword,
            'city': city,
            'timestamp': datetime.now().isoformat(),
            'platforms_used': [],
            'total_found': 0
        }

        print(f"开始搜索餐厅: {keyword} in {city}")
        print(f"可用API平台: {', '.join(self.available_apis)}")
        print("="*50)

        # 高德地图API
        if 'amap' in self.available_apis:
            print("🔍 正在搜索高德地图...")
            amap_results = self.client.search_restaurants_amap(keyword, city, limit=limit_per_platform)
            all_results.extend(amap_results['restaurants'])
            summary['platforms_used'].append(f"高德地图({len(amap_results['restaurants'])}条)")
            print(f"✅ 高德地图: 找到 {len(amap_results['restaurants'])} 家餐厅")
            time.sleep(0.1)  # 避免请求过于频繁

        # 百度地图API
        if 'baidu' in self.available_apis:
            print("🔍 正在搜索百度地图...")
            baidu_results = self.client.search_restaurants_baidu(keyword, city, limit=limit_per_platform)
            all_results.extend(baidu_results['restaurants'])
            summary['platforms_used'].append(f"百度地图({len(baidu_results['restaurants'])}条)")
            print(f"✅ 百度地图: 找到 {len(baidu_results['restaurants'])} 家餐厅")
            time.sleep(0.1)

        # 腾讯位置服务API
        if 'tencent' in self.available_apis:
            print("🔍 正在搜索腾讯地图...")
            tencent_results = self.client.search_restaurants_tencent(keyword, city, limit=limit_per_platform)
            all_results.extend(tencent_results['restaurants'])
            summary['platforms_used'].append(f"腾讯地图({len(tencent_results['restaurants'])}条)")
            print(f"✅ 腾讯地图: 找到 {len(tencent_results['restaurants'])} 家餐厅")
            time.sleep(0.1)

        # 去重处理
        deduplicated_results = self._deduplicate_restaurants(all_results)
        summary['total_found'] = len(deduplicated_results)

        print("="*50)
        print(f"🎯 搜索完成!")
        print(f"📊 总计找到: {len(all_results)} 条原始结果")
        print(f"🔄 去重后: {len(deduplicated_results)} 家餐厅")
        print(f"📍 涵盖平台: {', '.join(summary['platforms_used'])}")

        return {
            'summary': summary,
            'restaurants': deduplicated_results,
            'raw_count': len(all_results),
            'deduplicated_count': len(deduplicated_results)
        }

    def _deduplicate_restaurants(self, restaurants: List[Dict]) -> List[Dict]:
        """餐厅数据去重"""
        seen = set()
        deduplicated = []

        for restaurant in restaurants:
            # 使用名称和地址的组合作为唯一标识
            key = f"{restaurant['name']}_{restaurant['address']}"
            key_hash = hashlib.md5(key.encode()).hexdigest()

            if key_hash not in seen:
                seen.add(key_hash)
                restaurant['unique_id'] = key_hash
                deduplicated.append(restaurant)

        return deduplicated

    def save_results(self, results: Dict, filename: str = None):
        """保存搜索结果"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            keyword = results['summary']['keyword'].replace(' ', '_')
            city = results['summary']['city']
            filename = f"data/official_api_restaurants_{keyword}_{city}_{timestamp}.json"

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"💾 结果已保存到: {filename}")
        return filename

def create_api_keys_template():
    """创建API密钥配置模板"""
    template = {
        "amap": "your_amap_api_key_here",
        "baidu": "your_baidu_api_key_here",
        "tencent": "your_tencent_api_key_here"
    }

    with open('@cc-code/api_keys_template.json', 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)

    print("📋 API密钥模板已创建: @cc-code/api_keys_template.json")
    print("请根据模板配置您的API密钥")

def demo_with_test_keys():
    """使用测试密钥进行演示"""
    print("🧪 官方API餐厅搜索演示")
    print("注意：这里使用的是演示用的API调用，请替换为您的真实API密钥")
    print("="*60)

    # 演示API密钥（实际使用时需要替换为真实密钥）
    demo_keys = {
        'amap': 'demo_amap_key',
        'baidu': 'demo_baidu_key',
        'tencent': 'demo_tencent_key'
    }

    # 创建搜索器
    searcher = MultiAPIRestaurantSearcher(demo_keys)

    # 模拟搜索结果（因为使用的是演示密钥）
    mock_results = {
        'summary': {
            'keyword': '火锅',
            'city': '北京',
            'timestamp': datetime.now().isoformat(),
            'platforms_used': ['高德地图(演示)', '百度地图(演示)', '腾讯地图(演示)'],
            'total_found': 15
        },
        'restaurants': [
            {
                'id': f'demo_restaurant_{i}',
                'name': f'示例火锅店{i}',
                'address': f'北京市朝阳区示例街道{i}号',
                'location': {'lat': 39.9 + i*0.01, 'lng': 116.4 + i*0.01},
                'phone': f'010-1234567{i}',
                'category': '火锅',
                'rating': 4.0 + (i % 10) * 0.1,
                'tags': ['火锅', '川菜', '聚餐'],
                'source': 'demo',
                'unique_id': f'demo_{i}'
            }
            for i in range(1, 16)
        ],
        'raw_count': 45,
        'deduplicated_count': 15
    }

    # 保存演示结果
    filename = searcher.save_results(mock_results)

    print("\n📝 演示完成! 要使用真实API:")
    print("1. 申请各平台的API密钥")
    print("2. 配置api_keys_template.json文件")
    print("3. 运行 python ccc-official_api_client.py")

    return filename

def main():
    """主函数"""
    print("🍽️ 官方API餐厅数据获取系统")
    print("支持高德、百度、腾讯三大平台官方API")
    print("="*60)

    # 创建API密钥模板
    create_api_keys_template()

    # 运行演示
    demo_file = demo_with_test_keys()

    print(f"\n📖 使用说明:")
    print("1. 申请API密钥:")
    print("   - 高德地图: https://lbs.amap.com/")
    print("   - 百度地图: https://lbsyun.baidu.com/")
    print("   - 腾讯地图: https://lbs.qq.com/")
    print("2. 配置密钥到 api_keys_template.json")
    print("3. 运行真实搜索")

    return demo_file

if __name__ == "__main__":
    main()