#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大众点评评论分析系统 - 完整流程执行器（简化版）
Complete Workflow Executor (Simplified)

v1.0 转测版本
执行从数据分析到报告生成的完整流程
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

class CompleteWorkflowExecutor:
    """完整流程执行器"""

    def __init__(self):
        self.base_dir = Path(".")
        self.data_dir = self.base_dir / "data"
        self.steps_completed = []

    def print_header(self, title):
        """打印步骤标题"""
        print("=" * 60)
        print(f"[流程] {title}")
        print("=" * 60)

    def print_step(self, step_num, description):
        """打印步骤信息"""
        print(f"\n[步骤 {step_num}] {description}")
        print("-" * 40)

    def check_requirements(self):
        """检查系统要求"""
        self.print_step(1, "系统环境检查")

        # 检查Python版本
        python_version = sys.version_info
        print(f"[OK] Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")

        # 检查必要的文件
        required_files = [
            "demo_run.py",
            "ccc-data_optimized_wordcloud.py",
            "data/demo_analysis_result.json",
            "data/wordcloud_data.json"
        ]

        for file in required_files:
            if (self.base_dir / file).exists():
                print(f"[OK] 文件检查: {file}")
            else:
                print(f"[ERROR] 缺失文件: {file}")
                return False

        print("[SUCCESS] 系统环境检查通过")
        self.steps_completed.append("环境检查")
        return True

    def run_data_analysis(self):
        """运行数据分析"""
        self.print_step(2, "数据分析执行")

        try:
            # 运行演示数据分析
            result = subprocess.run([
                sys.executable, "demo_run.py"
            ], capture_output=True, text=True, cwd=self.base_dir)

            if result.returncode == 0:
                print("[OK] 数据分析执行成功")
                print("[INFO] 分析结果:")

                # 读取分析结果
                result_file = self.data_dir / "demo_analysis_result.json"
                if result_file.exists():
                    with open(result_file, 'r', encoding='utf-8') as f:
                        analysis_data = json.load(f)

                    basic_stats = analysis_data.get('basic_stats', {})
                    sentiment = analysis_data.get('sentiment_analysis', {})

                    print(f"   - 总评论数: {basic_stats.get('total_comments', 0)}")
                    print(f"   - 平均评分: {basic_stats.get('average_rating', 0)}")
                    print(f"   - 正面评论: {sentiment.get('positive', 0)}")
                    print(f"   - 负面评论: {sentiment.get('negative', 0)}")
                    print(f"   - 关键词数量: {len(analysis_data.get('keywords', []))}")
                    print(f"   - 标签数量: {len(analysis_data.get('tags', []))}")

                self.steps_completed.append("数据分析")
                return True
            else:
                print(f"[ERROR] 数据分析失败: {result.stderr}")
                return False

        except Exception as e:
            print(f"[ERROR] 数据分析异常: {e}")
            return False

    def generate_visualizations(self):
        """生成可视化报告"""
        self.print_step(3, "可视化报告生成")

        try:
            # 运行优化版词云生成器
            result = subprocess.run([
                sys.executable, "ccc-data_optimized_wordcloud.py"
            ], capture_output=True, text=True, cwd=self.base_dir)

            if result.returncode == 0:
                print("[OK] 可视化报告生成成功")

                # 检查生成的文件
                report_file = self.data_dir / "data_optimized_report.html"
                if report_file.exists():
                    file_size = report_file.stat().st_size / 1024  # KB
                    print(f"[INFO] 报告文件: data_optimized_report.html ({file_size:.1f} KB)")

                    # 检查报告内容
                    with open(report_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if "keyword-tag negative" in content:
                        print("[OK] 负面关键词标签正常显示")
                    else:
                        print("[WARN] 负面关键词标签可能未正确显示")

                    if "stat-value" in content:
                        print("[OK] 基础统计数据正常显示")
                    else:
                        print("[WARN] 基础统计数据可能未正确显示")

                self.steps_completed.append("可视化生成")
                return True
            else:
                print(f"[ERROR] 可视化生成失败: {result.stderr}")
                return False

        except Exception as e:
            print(f"[ERROR] 可视化生成异常: {e}")
            return False

    def validate_results(self):
        """验证结果"""
        self.print_step(4, "结果验证")

        validation_passed = True

        # 验证数据文件
        data_files = [
            "demo_analysis_result.json",
            "wordcloud_data.json",
            "data_optimized_report.html"
        ]

        for file in data_files:
            file_path = self.data_dir / file
            if file_path.exists():
                print(f"[OK] 数据文件: {file}")
            else:
                print(f"[ERROR] 缺失文件: {file}")
                validation_passed = False

        # 验证HTML报告内容
        report_file = self.data_dir / "data_optimized_report.html"
        if report_file.exists():
            with open(report_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查关键元素
            checks = [
                ("基础统计", "stat-value"),
                ("关键词标签", "keyword-tag"),
                ("正面标签", "keyword-tag positive"),
                ("负面标签", "keyword-tag negative"),
                ("词云图", "wordcloud-image"),
                ("情感分析", "sentiment_chart")
            ]

            for check_name, check_content in checks:
                if check_content in content:
                    print(f"[OK] {check_name}验证通过")
                else:
                    print(f"[ERROR] {check_name}验证失败")
                    validation_passed = False

        if validation_passed:
            print("[SUCCESS] 结果验证通过")
            self.steps_completed.append("结果验证")
        else:
            print("[ERROR] 结果验证失败")

        return validation_passed

    def open_results(self):
        """打开结果"""
        self.print_step(5, "打开结果展示")

        try:
            report_file = self.data_dir / "data_optimized_report.html"
            if report_file.exists():
                # 尝试打开HTML报告
                subprocess.run(['start', str(report_file)], shell=True, check=True)
                print("[OK] 可视化报告已在浏览器中打开")
                self.steps_completed.append("结果展示")
                return True
            else:
                print("[ERROR] 报告文件不存在")
                return False

        except Exception as e:
            print(f"[WARN] 自动打开失败: {e}")
            print(f"[INFO] 请手动打开文件: {report_file}")
            self.steps_completed.append("结果展示")
            return True

    def generate_summary(self):
        """生成执行总结"""
        self.print_step(6, "执行总结")

        print("[INFO] 完整流程执行情况:")

        all_steps = [
            "环境检查",
            "数据分析",
            "可视化生成",
            "结果验证",
            "结果展示"
        ]

        for step in all_steps:
            if step in self.steps_completed:
                print(f"[OK] {step}")
            else:
                print(f"[ERROR] {step}")

        success_rate = len(self.steps_completed) / len(all_steps) * 100
        print(f"\n[RESULT] 执行成功率: {success_rate:.1f}%")

        if success_rate == 100:
            print("[SUCCESS] 完整流程执行成功！")
            print("\n[FEATURES] 系统现在提供:")
            print("   • 准确的中文评论分析")
            print("   • 智能的情感分类")
            print("   • 平衡的关键词展示")
            print("   • 直观的可视化报告")
            print("   • 完整的数据洞察")

        return success_rate == 100

    def run_complete_workflow(self):
        """运行完整工作流程"""
        self.print_header("大众点评评论分析系统 - 完整流程执行")

        print("[START] 开始执行v1.0转测版本完整流程...")
        print(f"[INFO] 工作目录: {self.base_dir.absolute()}")
        print(f"[INFO] 开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # 执行各个步骤
        steps = [
            self.check_requirements,
            self.run_data_analysis,
            self.generate_visualizations,
            self.validate_results,
            self.open_results,
            self.generate_summary
        ]

        for step_func in steps:
            try:
                if not step_func():
                    print(f"\n[ERROR] 步骤 '{step_func.__name__}' 执行失败")
                    break
                time.sleep(1)  # 短暂等待
            except KeyboardInterrupt:
                print("\n[WARN] 用户中断执行")
                break
            except Exception as e:
                print(f"\n[ERROR] 步骤执行异常: {e}")
                break

        print(f"\n[INFO] 完成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

def main():
    """主函数"""
    executor = CompleteWorkflowExecutor()
    executor.run_complete_workflow()

if __name__ == "__main__":
    main()