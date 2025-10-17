#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合规版系统测试脚本
用于演示系统功能，不实际进行网络爬取
"""

import os
import sys
import json
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def show_welcome():
    """显示欢迎信息"""
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║        大众点评餐厅评论分析系统 - 合规版测试                      ║")
    print("╠════════════════════════════════════════════════════════════════╣")
    print("║                                                                ║")
    print("║  本系统仅供学习、研究和学术用途使用                                 ║")
    print("║  包含完整的法律保护和隐私保护机制                                  ║")
    print("║                                                                ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()

def check_files():
    """检查必要文件"""
    print("📋 检查系统文件...")

    required_files = [
        'ccc-main.py',
        'ccc-config.py',
        'USER_AGREEMENT.md',
        'RESEARCH_PURPOSE.md',
        'requirements.txt'
    ]

    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (缺失)")
            missing_files.append(file)

    print()
    if missing_files:
        print(f"⚠️  缺少 {len(missing_files)} 个必要文件")
        return False
    else:
        print("✅ 所有必要文件完整")
        return True

def check_modules():
    """检查核心模块"""
    print("\n📦 检查核心模块...")

    modules = [
        ('dianping_spider/spiders', '爬虫模块'),
        ('dianping_spider/utils', '工具模块'),
        ('dianping_spider/web', 'Web模块'),
        ('dianping_spider/templates', '模板目录'),
    ]

    for path, name in modules:
        if os.path.exists(path):
            print(f"  ✅ {name}: {path}")
        else:
            print(f"  ⚠️  {name}: {path} (不存在)")

    print()

def check_config():
    """检查配置文件"""
    print("⚙️  检查合规配置...")

    try:
        # 尝试导入配置
        if os.path.exists('ccc-config.py'):
            with open('ccc-config.py', 'r', encoding='utf-8') as f:
                content = f.read()
                if 'COMPLIANCE_CONFIG' in content:
                    print("  ✅ 合规配置已启用")
                if 'RATE_LIMITS' in content:
                    print("  ✅ 频率限制配置存在")
                if 'DATA_PROTECTION' in content:
                    print("  ✅ 数据保护配置存在")
        else:
            print("  ⚠️  合规配置文件不存在")
    except Exception as e:
        print(f"  ❌ 配置检查失败: {e}")

    print()

def show_usage_examples():
    """显示使用示例"""
    print("🚀 使用示例:")
    print()
    print("1. 完整流程（推荐）:")
    print("   python ccc-main.py pipeline \"餐厅名称\" --city 北京 --months 1")
    print()
    print("2. 分步执行:")
    print("   python ccc-main.py crawl \"餐厅名称\" --city 北京")
    print("   python ccc-main.py analyze data/comments_xxx.json")
    print("   python ccc-main.py wordcloud data/comments_xxx_analysis.json")
    print()
    print("3. Web界面:")
    print("   python ccc-main.py web")
    print()
    print("4. 合规检查:")
    print("   python ccc-main.py compliance")
    print()

def demo_data_protection():
    """演示数据保护功能"""
    print("🔐 数据保护功能演示:")
    print()

    # 演示匿名化
    print("示例1: 用户信息匿名化")
    print("  原始: username='张三', phone='13812345678'")
    print("  处理后: user_id='a1b2c3d4', phone='[手机号]'")
    print()

    # 演示时间泛化
    print("示例2: 时间信息泛化")
    print("  原始: '2024-10-15 14:30:00'")
    print("  处理后: '一周内'")
    print()

    # 演示敏感信息过滤
    print("示例3: 敏感信息过滤")
    print("  原始: '我的邮箱是user@example.com'")
    print("  处理后: '我的邮箱是[邮箱]'")
    print()

def show_compliance_features():
    """显示合规特性"""
    print("✨ 核心合规特性:")
    print()
    print("🔒 严格限制:")
    print("  • 每分钟最多10次请求")
    print("  • 每天最多1000次请求")
    print("  • 单次最多500条评论")
    print("  • 时间范围限制1个月")
    print()
    print("🔒 隐私保护:")
    print("  • 用户信息自动匿名化")
    print("  • 敏感信息自动过滤")
    print("  • 时间信息泛化处理")
    print("  • 个人标识符移除")
    print()
    print("🔒 审计监控:")
    print("  • 完整操作日志记录")
    print("  • 自动合规报告生成")
    print("  • 违规行为实时预警")
    print("  • 数据保留期限管理")
    print()

def check_dependencies():
    """检查依赖包"""
    print("📚 检查Python依赖包...")

    required_packages = [
        'requests', 'beautifulsoup4', 'selenium', 'pandas',
        'jieba', 'wordcloud', 'flask', 'matplotlib'
    ]

    installed = []
    missing = []

    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            installed.append(package)
            print(f"  ✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"  ❌ {package} (未安装)")

    print()
    if missing:
        print(f"⚠️  缺少 {len(missing)} 个依赖包")
        print(f"   运行: pip install {' '.join(missing)}")
    else:
        print("✅ 所有依赖包已安装")

    return len(missing) == 0

def create_demo_data():
    """创建演示数据"""
    print("\n📊 创建演示数据...")

    demo_comments = [
        {
            "content": "味道很好，牛肉新鲜，推荐手打牛肉丸",
            "rating": 4.5,
            "time_period": "一周内",
            "user_id": "a1b2c3d4",
            "tags": ["好吃", "新鲜", "推荐"],
            "privacy_protected": True
        },
        {
            "content": "服务态度不错，环境也很干净",
            "rating": 4.0,
            "time_period": "一周内",
            "user_id": "e5f6g7h8",
            "tags": ["服务好", "干净"],
            "privacy_protected": True
        },
        {
            "content": "价格有点贵，但是质量确实好",
            "rating": 3.5,
            "time_period": "一个月内",
            "user_id": "i9j0k1l2",
            "tags": ["有点贵", "质量好"],
            "privacy_protected": True
        }
    ]

    # 创建data目录
    os.makedirs('data', exist_ok=True)

    # 保存演示数据
    demo_file = 'data/demo_comments.json'
    data_package = {
        'metadata': {
            'collection_time': datetime.now().isoformat(),
            'total_comments': len(demo_comments),
            'compliance_version': '1.0',
            'privacy_protected': True,
            'anonymized': True,
            'demo_data': True
        },
        'comments': demo_comments
    }

    with open(demo_file, 'w', encoding='utf-8') as f:
        json.dump(data_package, f, ensure_ascii=False, indent=2)

    print(f"  ✅ 演示数据已创建: {demo_file}")
    print(f"  📊 包含 {len(demo_comments)} 条示例评论")
    print()

def show_next_steps():
    """显示后续步骤"""
    print("📖 后续步骤:")
    print()
    print("1. 阅读法律文件:")
    print("   • USER_AGREEMENT.md - 用户协议")
    print("   • RESEARCH_PURPOSE.md - 研究目的声明")
    print()
    print("2. 安装依赖包:")
    print("   pip install -r requirements.txt")
    print()
    print("3. 开始使用:")
    print("   python ccc-main.py --help")
    print()
    print("4. 测试分析功能:")
    print("   python ccc-main.py analyze data/demo_comments.json")
    print()

def main():
    """主函数"""
    show_welcome()

    # 检查文件
    files_ok = check_files()

    # 检查模块
    check_modules()

    # 检查配置
    check_config()

    # 检查依赖
    deps_ok = check_dependencies()

    # 显示合规特性
    show_compliance_features()

    # 演示数据保护
    demo_data_protection()

    # 创建演示数据
    if files_ok:
        create_demo_data()

    # 显示使用示例
    show_usage_examples()

    # 显示后续步骤
    show_next_steps()

    # 总结
    print("="*70)
    if files_ok and deps_ok:
        print("✅ 系统检查完成，可以开始使用！")
    else:
        print("⚠️  系统检查发现问题，请按照提示修复后再使用")
    print("="*70)
    print()
    print("💡 提示: 使用前请务必阅读 USER_AGREEMENT.md 和 RESEARCH_PURPOSE.md")
    print()

if __name__ == '__main__':
    main()