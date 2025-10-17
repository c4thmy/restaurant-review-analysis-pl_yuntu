#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高德API密钥配置向导
Amap API Key Configuration Guide

帮助用户一步步配置高德地图API密钥
"""

import json
import os
import sys

# 设置控制台编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

def configure_amap_key():
    """配置高德地图API密钥的交互式向导"""

    print("="*60)
    print("🗺️ 高德地图API密钥配置向导")
    print("="*60)

    print("恭喜您成功申请到高德地图API密钥！")
    print("现在让我们来配置它到系统中。")
    print()

    # 读取当前配置
    config_file = 'api_keys_template.json'
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ 配置文件不存在，正在创建...")
        config = {
            "amap": "your_amap_api_key_here",
            "baidu": "your_baidu_api_key_here",
            "tencent": "your_tencent_api_key_here"
        }

    print("📋 当前配置状态:")
    print(f"高德地图: {config.get('amap', 'your_amap_api_key_here')}")
    print(f"百度地图: {config.get('baidu', 'your_baidu_api_key_here')}")
    print(f"腾讯地图: {config.get('tencent', 'your_tencent_api_key_here')}")
    print()

    # 获取用户输入的API密钥
    print("请输入您的高德地图API密钥:")
    print("📝 提示：API密钥通常是32位字符，格式如: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6")
    print()

    while True:
        api_key = input("请粘贴您的高德API密钥: ").strip()

        if not api_key:
            print("❌ 密钥不能为空，请重新输入")
            continue

        if 'your_' in api_key or len(api_key) < 20:
            print("❌ 这似乎不是一个有效的API密钥，请检查后重新输入")
            continue

        # 显示密钥预览（隐藏部分字符保护隐私）
        if len(api_key) >= 8:
            preview = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
        else:
            preview = "*" * len(api_key)

        print(f"📋 您输入的密钥: {preview}")

        confirm = input("确认这个密钥正确吗？(y/n): ").lower()
        if confirm in ['y', 'yes', '是']:
            break
        else:
            print("请重新输入您的API密钥:")

    # 更新配置
    config['amap'] = api_key

    # 保存配置
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print("✅ 高德地图API密钥配置成功！")
    except Exception as e:
        print(f"❌ 保存配置失败: {e}")
        return False

    print()
    print("📁 配置已保存到:", config_file)
    print("🔑 高德地图API密钥已激活")
    print()

    return True

def test_amap_configuration():
    """测试高德API配置"""
    print("🧪 现在让我们测试一下您的API密钥是否工作正常...")
    print()

    try:
        # 导入验证工具
        import subprocess
        import sys

        print("正在验证API连接...")
        result = subprocess.run([sys.executable, 'ccc-api_key_validator.py'],
                              capture_output=True, text=True, encoding='utf-8')

        print("验证结果:")
        print(result.stdout)

        if "✅ 高德地图" in result.stdout:
            print("🎉 恭喜！您的高德地图API密钥验证成功！")
            return True
        else:
            print("⚠️ API密钥验证可能有问题，请检查:")
            print("1. 密钥是否正确复制")
            print("2. API服务是否已开通")
            print("3. 网络连接是否正常")
            return False

    except Exception as e:
        print(f"验证过程出现错误: {e}")
        print("您可以稍后手动运行: python ccc-api_key_validator.py")
        return False

def run_real_data_demo():
    """运行真实数据获取演示"""
    print("\n" + "="*60)
    print("🚀 准备运行真实数据获取演示")
    print("="*60)

    print("现在您可以使用真实的高德地图API获取餐厅数据了！")
    print()

    choice = input("是否现在就运行一个真实数据获取演示？(y/n): ").lower()

    if choice in ['y', 'yes', '是']:
        print("\n🔄 正在启动真实数据获取演示...")
        print("这将搜索北京的火锅餐厅，大约需要1-2分钟...")

        try:
            import subprocess
            import sys

            # 运行真实数据pipeline
            result = subprocess.run([sys.executable, 'ccc-api_data_pipeline.py'],
                                  encoding='utf-8')

            print("\n✅ 演示完成！")
            print("📁 请查看 data/ 目录下生成的真实餐厅数据文件")

        except Exception as e:
            print(f"演示运行出现错误: {e}")
            print("您可以稍后手动运行: python ccc-api_data_pipeline.py")
    else:
        print("\n💡 您可以随时运行以下命令获取真实数据:")
        print("python ccc-api_data_pipeline.py")

def show_next_steps():
    """显示后续步骤指导"""
    print("\n" + "="*60)
    print("🎯 后续步骤建议")
    print("="*60)

    print("您现在已经成功配置了高德地图API，可以进行以下操作:")
    print()

    print("1. 🧪 验证API密钥:")
    print("   python ccc-api_key_validator.py")
    print()

    print("2. 🚀 获取真实餐厅数据:")
    print("   python ccc-api_data_pipeline.py")
    print()

    print("3. 📊 分析已有数据:")
    print("   python ccc-main.py analyze data/api_restaurants_*.json")
    print()

    print("4. ☁️ 生成词云:")
    print("   python ccc-main.py wordcloud data/*_analysis.json")
    print()

    print("5. 🔧 自定义搜索:")
    print("   # 搜索特定城市的特定类型餐厅")
    print("   # 修改 ccc-api_data_pipeline.py 中的参数")
    print()

    print("💡 提示：如果您还想获得更多数据，可以继续申请:")
    print("- 百度地图API: https://lbsyun.baidu.com/ (10万次/日)")
    print("- 腾讯地图API: https://lbs.qq.com/ (1万次/日)")
    print()

    print("📚 详细文档:")
    print("- API使用指南: @doc/真实API模式完整使用指南.md")
    print("- 技术文档: @cc-doc/官方API餐厅数据获取完整指南.md")

def main():
    """主函数"""
    print("🎉 欢迎使用高德地图API配置向导！")
    print()

    # 步骤1: 配置API密钥
    if configure_amap_key():
        print("✅ 步骤1完成: API密钥配置成功")

        # 步骤2: 测试连接
        print("\n⏭️ 步骤2: 测试API连接")
        if test_amap_configuration():
            print("✅ 步骤2完成: API连接测试成功")

            # 步骤3: 运行演示
            print("\n⏭️ 步骤3: 真实数据演示")
            run_real_data_demo()

        else:
            print("⚠️ 步骤2: API连接测试遇到问题")
            print("建议检查密钥配置后重试")
    else:
        print("❌ 配置失败，请重试")

    # 显示后续步骤
    show_next_steps()

if __name__ == "__main__":
    main()