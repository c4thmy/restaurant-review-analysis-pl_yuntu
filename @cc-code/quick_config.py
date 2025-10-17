#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速API密钥配置工具
Quick API Key Configuration Tool

简单快速地配置API密钥
"""

import json
import os

def quick_configure_api_key(platform, api_key):
    """快速配置API密钥"""
    config_file = 'api_keys_template.json'

    # 读取现有配置
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {
            "amap": "your_amap_api_key_here",
            "baidu": "your_baidu_api_key_here",
            "tencent": "your_tencent_api_key_here"
        }

    # 更新指定平台的密钥
    config[platform] = api_key

    # 保存配置
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print(f"✅ {platform.upper()} API密钥配置成功！")
    print(f"📁 配置已保存到: {config_file}")

    return True

def show_current_config():
    """显示当前配置状态"""
    config_file = 'api_keys_template.json'

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        print("📋 当前API密钥配置状态:")
        print("-" * 40)

        platforms = {
            'amap': '高德地图',
            'baidu': '百度地图',
            'tencent': '腾讯地图'
        }

        for platform, name in platforms.items():
            key = config.get(platform, 'your_xxx_api_key_here')
            if 'your_' in key:
                status = "❌ 未配置"
            else:
                # 隐藏部分字符保护隐私
                hidden_key = key[:4] + "*" * (len(key) - 8) + key[-4:] if len(key) >= 8 else "*" * len(key)
                status = f"✅ 已配置 ({hidden_key})"

            print(f"{name:8}: {status}")

    except FileNotFoundError:
        print("❌ 配置文件不存在")

def main():
    """主函数 - 显示配置说明"""
    print("="*60)
    print("🔧 API密钥快速配置工具")
    print("="*60)

    show_current_config()

    print("\n📝 配置方法:")
    print("1. 手动编辑配置文件:")
    print("   编辑 api_keys_template.json")
    print("   将 'your_amap_api_key_here' 替换为您的真实密钥")

    print("\n2. 使用Python代码配置:")
    print("   from quick_config import quick_configure_api_key")
    print("   quick_configure_api_key('amap', '您的密钥')")

    print("\n3. 交互式配置:")
    print("   python configure_amap_key.py")

    print("\n✅ 配置完成后运行验证:")
    print("   python ccc-api_key_validator.py")

    print("\n🚀 开始获取真实数据:")
    print("   python ccc-api_data_pipeline.py")

if __name__ == "__main__":
    main()