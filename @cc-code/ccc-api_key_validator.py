#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API密钥验证工具
API Key Validation Tool

验证高德、百度、腾讯三大平台API密钥是否有效
并提供详细的测试报告和使用建议
"""

import requests
import json
import time
import sys
import os
from datetime import datetime

# 设置控制台编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

class APIKeyValidator:
    """API密钥验证器"""

    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 10
        self.results = {}

    def test_amap_api(self, api_key):
        """测试高德地图API"""
        print("🗺️ 测试高德地图API...")

        test_url = "https://restapi.amap.com/v3/place/text"
        params = {
            'key': api_key,
            'keywords': '麦当劳',
            'city': '北京',
            'types': '050000',
            'offset': 1,
            'page': 1,
            'extensions': 'base'
        }

        try:
            response = self.session.get(test_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get('status') == '1':
                count = data.get('count', 0)
                info = data.get('info', 'OK')
                return {
                    'status': 'success',
                    'message': f'API密钥有效，找到{count}个结果',
                    'info': info,
                    'quota_used': True,
                    'test_query': '麦当劳@北京'
                }
            else:
                error_code = data.get('infocode', 'unknown')
                error_msg = data.get('info', '未知错误')
                return {
                    'status': 'failed',
                    'message': f'API调用失败: {error_msg}',
                    'error_code': error_code,
                    'suggestion': self._get_amap_error_suggestion(error_code)
                }

        except requests.RequestException as e:
            return {
                'status': 'error',
                'message': f'网络请求失败: {e}',
                'suggestion': '请检查网络连接'
            }

    def test_baidu_api(self, api_key):
        """测试百度地图API"""
        print("🟦 测试百度地图API...")

        test_url = "https://api.map.baidu.com/place/v2/search"
        params = {
            'ak': api_key,
            'query': '肯德基',
            'tag': '美食',
            'region': '北京',
            'page_num': 0,
            'page_size': 1,
            'output': 'json',
            'scope': '1'
        }

        try:
            response = self.session.get(test_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 0:
                total = data.get('total', 0)
                message = data.get('message', 'success')
                return {
                    'status': 'success',
                    'message': f'API密钥有效，找到{total}个结果',
                    'info': message,
                    'quota_used': True,
                    'test_query': '肯德基@北京'
                }
            else:
                error_code = data.get('status', 'unknown')
                error_msg = data.get('message', '未知错误')
                return {
                    'status': 'failed',
                    'message': f'API调用失败: {error_msg}',
                    'error_code': error_code,
                    'suggestion': self._get_baidu_error_suggestion(error_code)
                }

        except requests.RequestException as e:
            return {
                'status': 'error',
                'message': f'网络请求失败: {e}',
                'suggestion': '请检查网络连接'
            }

    def test_tencent_api(self, api_key):
        """测试腾讯地图API"""
        print("🟢 测试腾讯地图API...")

        test_url = "https://apis.map.qq.com/ws/place/v1/search"
        params = {
            'key': api_key,
            'keyword': '星巴克',
            'boundary': 'region(北京,0)',
            'page_index': 1,
            'page_size': 1,
            'orderby': '_score'
        }

        try:
            response = self.session.get(test_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 0:
                count = data.get('count', 0)
                message = data.get('message', 'query ok')
                return {
                    'status': 'success',
                    'message': f'API密钥有效，找到{count}个结果',
                    'info': message,
                    'quota_used': True,
                    'test_query': '星巴克@北京'
                }
            else:
                error_code = data.get('status', 'unknown')
                error_msg = data.get('message', '未知错误')
                return {
                    'status': 'failed',
                    'message': f'API调用失败: {error_msg}',
                    'error_code': error_code,
                    'suggestion': self._get_tencent_error_suggestion(error_code)
                }

        except requests.RequestException as e:
            return {
                'status': 'error',
                'message': f'网络请求失败: {e}',
                'suggestion': '请检查网络连接'
            }

    def _get_amap_error_suggestion(self, error_code):
        """获取高德API错误建议"""
        suggestions = {
            '10001': '请检查API密钥是否正确',
            '10002': '请检查API密钥是否有效',
            '10003': '访问已超出日访问量限制',
            '10004': '单位时间内访问过于频繁',
            '10005': 'IP白名单出错，发送请求的服务器IP不在IP白名单内',
            '10006': '绑定域名出错',
            '10007': '数字签名未通过验证',
            '10008': 'MD5安全码未通过验证',
            '10009': '请求key与绑定平台不符',
            '10010': 'IP访问超限',
            '10011': '服务不支持https请求',
            '10012': '权限不足，服务请求被拒绝',
            '10013': 'Key被删除',
            '20000': '请求参数非法',
            '20001': '缺少必填参数',
            '20002': '请求协议非法',
            '20003': '其他未知错误'
        }
        return suggestions.get(error_code, '请查看高德地图API文档')

    def _get_baidu_error_suggestion(self, error_code):
        """获取百度API错误建议"""
        suggestions = {
            '1': '服务器内部错误',
            '2': '请求参数非法',
            '3': '权限校验失败',
            '4': '配额校验失败',
            '5': 'ak不存在或者非法',
            '101': '服务禁用',
            '102': '不通过白名单或者安全码不对',
            '200': '无权限',
            '201': '配额超限制',
            '202': '应用不存在，AK有误请检查再重试',
            '203': '应用被禁用',
            '210': '应用IP校验失败',
            '211': '应用SN校验失败',
            '220': '应用Referer校验失败',
            '230': '应用Timestamp校验失败',
            '240': '应用权限校验失败',
            '250': '用户权限校验失败',
            '251': '用户删除',
            '260': '服务不存在',
            '261': '服务被禁用',
            '301': '永久配额超限制',
            '302': '天配额超限制'
        }
        return suggestions.get(str(error_code), '请查看百度地图API文档')

    def _get_tencent_error_suggestion(self, error_code):
        """获取腾讯API错误建议"""
        suggestions = {
            '110': 'key格式错误',
            '111': 'key不存在',
            '112': 'key被删除',
            '113': 'key被禁用',
            '114': 'key权限不足',
            '121': '并发量超限',
            '122': '日访问量超限',
            '311': '请求参数信息有误',
            '310': '请求参数信息有误',
            '400': '服务器无法处理请求',
            '500': '服务器内部错误'
        }
        return suggestions.get(str(error_code), '请查看腾讯地图API文档')

    def load_api_keys(self, config_file='api_keys_template.json'):
        """加载API密钥配置"""
        try:
            if not os.path.exists(config_file):
                print(f"❌ 配置文件不存在: {config_file}")
                return None

            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 过滤掉说明字段和无效密钥
            api_keys = {}
            for platform, key in config.items():
                if not platform.startswith('_') and key and 'your_' not in str(key):
                    api_keys[platform] = key

            return api_keys

        except Exception as e:
            print(f"❌ 加载配置文件失败: {e}")
            return None

    def validate_all_keys(self, config_file='api_keys_template.json'):
        """验证所有API密钥"""
        print("="*60)
        print("API密钥验证工具")
        print("="*60)

        # 加载密钥配置
        api_keys = self.load_api_keys(config_file)
        if not api_keys:
            print("❌ 未找到有效的API密钥配置")
            print(f"请编辑 {config_file} 文件，填入您的API密钥")
            return

        print(f"📋 找到 {len(api_keys)} 个API密钥待验证")
        print(f"📁 配置文件: {config_file}")
        print()

        validation_results = {}

        # 验证高德地图API
        if 'amap' in api_keys:
            print("开始验证高德地图API...")
            result = self.test_amap_api(api_keys['amap'])
            validation_results['amap'] = result
            self._print_result('高德地图', result)
            time.sleep(0.5)  # 避免请求过于频繁

        # 验证百度地图API
        if 'baidu' in api_keys:
            print("\n开始验证百度地图API...")
            result = self.test_baidu_api(api_keys['baidu'])
            validation_results['baidu'] = result
            self._print_result('百度地图', result)
            time.sleep(0.5)

        # 验证腾讯地图API
        if 'tencent' in api_keys:
            print("\n开始验证腾讯地图API...")
            result = self.test_tencent_api(api_keys['tencent'])
            validation_results['tencent'] = result
            self._print_result('腾讯地图', result)

        # 生成验证报告
        self._generate_report(validation_results)

        return validation_results

    def _print_result(self, platform, result):
        """打印验证结果"""
        status = result['status']
        message = result['message']

        if status == 'success':
            print(f"✅ {platform}: {message}")
            if 'test_query' in result:
                print(f"   测试查询: {result['test_query']}")
        elif status == 'failed':
            print(f"❌ {platform}: {message}")
            if 'suggestion' in result:
                print(f"   建议: {result['suggestion']}")
        else:
            print(f"⚠️ {platform}: {message}")
            if 'suggestion' in result:
                print(f"   建议: {result['suggestion']}")

    def _generate_report(self, results):
        """生成验证报告"""
        print("\n" + "="*60)
        print("验证报告")
        print("="*60)

        successful_apis = []
        failed_apis = []

        for platform, result in results.items():
            if result['status'] == 'success':
                successful_apis.append(platform)
            else:
                failed_apis.append(platform)

        print(f"✅ 验证成功: {len(successful_apis)} 个")
        for platform in successful_apis:
            platform_names = {'amap': '高德地图', 'baidu': '百度地图', 'tencent': '腾讯地图'}
            print(f"   - {platform_names.get(platform, platform)}")

        if failed_apis:
            print(f"\n❌ 验证失败: {len(failed_apis)} 个")
            for platform in failed_apis:
                platform_names = {'amap': '高德地图', 'baidu': '百度地图', 'tencent': '腾讯地图'}
                print(f"   - {platform_names.get(platform, platform)}")

        # 使用建议
        print("\n📋 使用建议:")
        if successful_apis:
            print("1. 可以立即使用验证成功的API进行数据获取")
            print("2. 运行以下命令开始获取真实餐厅数据:")
            print("   python ccc-api_data_pipeline.py")

        if failed_apis:
            print("3. 对于验证失败的API，请检查:")
            print("   - API密钥是否正确")
            print("   - 账号是否完成实名认证")
            print("   - 服务是否已开通")
            print("   - 配额是否充足")

        # 保存报告
        report_data = {
            'validation_time': datetime.now().isoformat(),
            'results': results,
            'summary': {
                'successful_apis': successful_apis,
                'failed_apis': failed_apis,
                'total_tested': len(results)
            }
        }

        report_file = f"data/api_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs('data', exist_ok=True)

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        print(f"\n📄 详细报告已保存: {report_file}")

def main():
    """主函数"""
    validator = APIKeyValidator()

    # 检查配置文件是否存在
    config_file = 'api_keys_template.json'
    if not os.path.exists(config_file):
        print("❌ 配置文件不存在，正在创建模板...")

        # 创建配置文件模板
        template = {
            "amap": "your_amap_api_key_here",
            "baidu": "your_baidu_api_key_here",
            "tencent": "your_tencent_api_key_here",
            "_instructions": {
                "description": "请将上面的示例密钥替换为您申请的真实API密钥",
                "amap_guide": "高德地图: https://lbs.amap.com/",
                "baidu_guide": "百度地图: https://lbsyun.baidu.com/",
                "tencent_guide": "腾讯地图: https://lbs.qq.com/"
            }
        }

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, ensure_ascii=False, indent=2)

        print(f"✅ 已创建配置文件模板: {config_file}")
        print("请编辑此文件，填入您申请的API密钥，然后重新运行验证")
        return

    # 执行验证
    results = validator.validate_all_keys(config_file)

    if results:
        successful_count = sum(1 for r in results.values() if r['status'] == 'success')
        print(f"\n🎯 验证完成! 成功验证 {successful_count}/{len(results)} 个API密钥")

        if successful_count > 0:
            print("\n🚀 下一步: 运行真实数据获取")
            print("python ccc-api_data_pipeline.py")
        else:
            print("\n📋 请根据上述建议修复API密钥问题后重新验证")

if __name__ == "__main__":
    main()