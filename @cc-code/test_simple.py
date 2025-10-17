#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合规版系统测试和演示脚本
"""

import os
import sys
import json
from datetime import datetime

def show_welcome():
    """显示欢迎信息"""
    print("=" * 70)
    print("     大众点评餐厅评论分析系统 - 合规版测试")
    print("=" * 70)
    print()
    print("本系统仅供学习、研究和学术用途使用")
    print("包含完整的法律保护和隐私保护机制")
    print()
    print("=" * 70)
    print()

def check_system():
    """检查系统状态"""
    print("[检查系统文件]")
    print()

    files = {
        'ccc-main.py': '合规版主程序',
        'ccc-config.py': '合规配置文件',
        'USER_AGREEMENT.md': '用户协议',
        'RESEARCH_PURPOSE.md': '研究目的声明',
        'requirements.txt': '依赖包列表'
    }

    all_ok = True
    for file, desc in files.items():
        exists = os.path.exists(file)
        status = "[OK]" if exists else "[MISS]"
        print(f"  {status} {desc}: {file}")
        if not exists:
            all_ok = False

    print()
    return all_ok

def check_modules():
    """检查Python模块"""
    print("[检查Python依赖]")
    print()

    modules = [
        'requests', 'bs4', 'selenium', 'pandas',
        'jieba', 'wordcloud', 'flask', 'matplotlib'
    ]

    installed = []
    missing = []

    for module in modules:
        try:
            __import__(module)
            installed.append(module)
            print(f"  [OK] {module}")
        except ImportError:
            missing.append(module)
            print(f"  [MISS] {module}")

    print()
    if missing:
        print(f"缺少 {len(missing)} 个依赖包，运行以下命令安装:")
        print(f"pip install {' '.join(missing)}")
        print()

    return len(missing) == 0

def show_compliance_features():
    """显示合规特性"""
    print("[核心合规特性]")
    print()
    print("严格限制:")
    print("  - 每分钟最多10次请求")
    print("  - 每天最多1000次请求")
    print("  - 单次最多500条评论")
    print("  - 时间范围限制1个月")
    print()
    print("隐私保护:")
    print("  - 用户信息自动匿名化")
    print("  - 敏感信息自动过滤")
    print("  - 时间信息泛化处理")
    print("  - 个人标识符移除")
    print()
    print("审计监控:")
    print("  - 完整操作日志记录")
    print("  - 自动合规报告生成")
    print("  - 违规行为实时预警")
    print()

def create_demo_data():
    """创建演示数据"""
    print("[创建演示数据]")
    print()

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
        },
        {
            "content": "火锅很正宗，沙茶酱味道不错",
            "rating": 4.5,
            "time_period": "一周内",
            "user_id": "m3n4o5p6",
            "tags": ["正宗", "好吃"],
            "privacy_protected": True
        },
        {
            "content": "排队时间有点长，不过值得等待",
            "rating": 4.0,
            "time_period": "一个月内",
            "user_id": "q7r8s9t0",
            "tags": ["排队", "值得"],
            "privacy_protected": True
        }
    ]

    os.makedirs('data', exist_ok=True)

    demo_file = 'data/demo_comments.json'
    data_package = {
        'metadata': {
            'collection_time': datetime.now().isoformat(),
            'total_comments': len(demo_comments),
            'compliance_version': '1.0',
            'privacy_protected': True,
            'anonymized': True,
            'demo_data': True,
            'description': '演示数据，用于测试分析功能'
        },
        'comments': demo_comments
    }

    with open(demo_file, 'w', encoding='utf-8') as f:
        json.dump(data_package, f, ensure_ascii=False, indent=2)

    print(f"演示数据已创建: {demo_file}")
    print(f"包含 {len(demo_comments)} 条示例评论")
    print()

    return demo_file

def show_usage_examples():
    """显示使用示例"""
    print("[使用示例]")
    print()
    print("1. 完整流程（推荐新手）:")
    print("   python ccc-main.py pipeline \"餐厅名称\" --city 北京 --months 1")
    print()
    print("2. 分步执行（适合学习）:")
    print("   python ccc-main.py crawl \"餐厅名称\" --city 北京")
    print("   python ccc-main.py analyze data/comments_xxx.json")
    print("   python ccc-main.py wordcloud data/comments_xxx_analysis.json")
    print()
    print("3. Web界面（可视化操作）:")
    print("   python ccc-main.py web")
    print()
    print("4. 测试分析功能（使用演示数据）:")
    print("   python ccc-main.py analyze data/demo_comments.json")
    print()
    print("5. 合规检查:")
    print("   python ccc-main.py compliance")
    print()

def demo_privacy_protection():
    """演示隐私保护"""
    print("[数据保护演示]")
    print()

    examples = [
        ("用户信息匿名化",
         "原始: username='张三', phone='13812345678'",
         "处理后: user_id='a1b2c3d4', phone='[手机号]'"),

        ("时间信息泛化",
         "原始: '2024-10-15 14:30:00'",
         "处理后: '一周内'"),

        ("敏感信息过滤",
         "原始: '我的邮箱是user@example.com'",
         "处理后: '我的邮箱是[邮箱]'"),
    ]

    for title, before, after in examples:
        print(f"{title}:")
        print(f"  {before}")
        print(f"  {after}")
        print()

def show_legal_notice():
    """显示法律声明"""
    print("[重要法律声明]")
    print()
    print("使用前必读:")
    print("  1. USER_AGREEMENT.md - 详细的用户协议和使用条款")
    print("  2. RESEARCH_PURPOSE.md - 研究目的声明和伦理要求")
    print()
    print("使用限制:")
    print("  - 仅限学习、研究、学术用途")
    print("  - 禁止商业用途和数据转售")
    print("  - 必须遵守网站使用条款")
    print("  - 数据保留期限30天")
    print()

def show_next_steps():
    """显示后续步骤"""
    print("[后续步骤]")
    print()
    print("Step 1: 阅读法律文件")
    print("  cat USER_AGREEMENT.md")
    print("  cat RESEARCH_PURPOSE.md")
    print()
    print("Step 2: 安装依赖包（如果有缺失）")
    print("  pip install -r requirements.txt")
    print()
    print("Step 3: 测试分析功能")
    print("  python ccc-main.py analyze data/demo_comments.json")
    print()
    print("Step 4: 开始实际使用")
    print("  python ccc-main.py pipeline \"餐厅名称\" --city 北京 --months 1")
    print()

def main():
    """主函数"""
    show_welcome()

    # 检查系统
    files_ok = check_system()

    # 检查依赖
    deps_ok = check_modules()

    # 显示合规特性
    show_compliance_features()

    # 演示隐私保护
    demo_privacy_protection()

    # 创建演示数据
    if files_ok:
        demo_file = create_demo_data()
        print(f"提示: 可以使用演示数据测试分析功能")
        print(f"运行: python ccc-main.py analyze {demo_file}")
        print()

    # 显示使用示例
    show_usage_examples()

    # 显示法律声明
    show_legal_notice()

    # 显示后续步骤
    show_next_steps()

    # 总结
    print("=" * 70)
    if files_ok and deps_ok:
        print("[状态] 系统检查完成，可以开始使用！")
    else:
        print("[警告] 系统检查发现问题，请按照提示修复后再使用")
    print("=" * 70)
    print()
    print("提示: 使用 python ccc-main.py --help 查看所有可用命令")
    print()

if __name__ == '__main__':
    main()