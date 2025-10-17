#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全检查脚本 - GitHub发布前敏感信息检测
在发布到GitHub前自动检查并清理敏感数据
"""

import os
import re
import json
import glob
from pathlib import Path

class SecurityChecker:
    def __init__(self):
        self.issues = []
        self.patterns = {
            'api_key': [
                r'[\'"][a-f0-9]{32}[\'"]',  # 32位hex密钥
                r'[\'"][A-Za-z0-9]{20,}[\'"]',  # 20位以上字母数字密钥
                r'sk-[a-zA-Z0-9]{48}',  # OpenAI API密钥格式
                r'AIza[0-9A-Za-z_-]{35}',  # Google API密钥格式
            ],
            'access_token': [
                r'[\'"][\w-]{20,}[\'"].*token',
                r'token[\'\"]\s*:\s*[\'"][^\'\"]{20,}[\'"]',
            ],
            'password': [
                r'password\s*=\s*[\'"][^\'\"]{8,}[\'"]',
                r'passwd\s*=\s*[\'"][^\'\"]{8,}[\'"]',
            ],
            'email': [
                r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            ],
            'phone': [
                r'1[3-9]\d{9}',  # 中国手机号
                r'\+86\s*1[3-9]\d{9}',  # 带国家代码的手机号
            ]
        }

    def check_file(self, filepath):
        """检查单个文件"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            for category, patterns in self.patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # 跳过明显的示例和模板
                        if self.is_safe_content(match.group()):
                            continue

                        line_num = content[:match.start()].count('\n') + 1
                        self.issues.append({
                            'file': filepath,
                            'line': line_num,
                            'type': category,
                            'content': match.group()[:50] + '...' if len(match.group()) > 50 else match.group(),
                            'severity': self.get_severity(category)
                        })
        except Exception as e:
            print(f"警告: 无法读取文件 {filepath}: {e}")

    def is_safe_content(self, content):
        """判断是否为安全的示例内容"""
        safe_patterns = [
            'your_api_key_here',
            'your_.*_key_here',
            'demo_key',
            'test_key',
            'example_key',
            'placeholder',
            'replace_with',
            'sk-xxxxxxxx',
            'AIzaxxxxxxxx',
            'example@example.com',
            '13800138000',
            'useAutomationExtension',  # Chrome选项
        ]

        content_lower = content.lower()
        return any(pattern.lower() in content_lower for pattern in safe_patterns)

    def get_severity(self, category):
        """获取严重程度"""
        severity_map = {
            'api_key': 'HIGH',
            'access_token': 'HIGH',
            'password': 'CRITICAL',
            'email': 'MEDIUM',
            'phone': 'MEDIUM'
        }
        return severity_map.get(category, 'LOW')

    def scan_project(self, root_dir='.'):
        """扫描整个项目"""
        print("检查中: 开始安全扫描...")

        # 要检查的文件类型
        file_patterns = [
            '**/*.py',
            '**/*.json',
            '**/*.js',
            '**/*.ts',
            '**/*.yaml',
            '**/*.yml',
            '**/*.env*',
            '**/*.config',
            '**/*.conf',
            '**/*.md',
        ]

        # 要忽略的目录
        ignore_dirs = {
            '.git', '__pycache__', 'node_modules',
            '.venv', 'venv', 'env', 'build', 'dist'
        }

        for pattern in file_patterns:
            for filepath in glob.glob(os.path.join(root_dir, pattern), recursive=True):
                # 跳过忽略的目录
                if any(ignore_dir in filepath for ignore_dir in ignore_dirs):
                    continue

                if os.path.isfile(filepath):
                    self.check_file(filepath)

    def check_git_status(self):
        """检查Git状态，确保敏感文件没有被跟踪"""
        try:
            import subprocess
            result = subprocess.run(['git', 'ls-files'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                tracked_files = result.stdout.strip().split('\n')
                sensitive_files = [
                    f for f in tracked_files
                    if any(pattern in f.lower() for pattern in [
                        'api_key', 'secret', 'password', '.env'
                    ]) and not any(safe in f.lower() for safe in [
                        'template', 'example', 'sample'
                    ])
                ]

                if sensitive_files:
                    for f in sensitive_files:
                        self.issues.append({
                            'file': f,
                            'line': 0,
                            'type': 'git_tracked',
                            'content': '敏感文件被Git跟踪',
                            'severity': 'CRITICAL'
                        })
        except Exception:
            pass  # Git不可用时跳过

    def generate_report(self):
        """生成安全检查报告"""
        if not self.issues:
            print("结果: 安全检查通过！未发现敏感信息")
            return True

        print(f"警告: 发现 {len(self.issues)} 个潜在安全问题:")
        print("=" * 60)

        # 按严重程度分组
        by_severity = {}
        for issue in self.issues:
            severity = issue['severity']
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(issue)

        # 输出报告
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            if severity in by_severity:
                print(f"\n[{severity}] 级别问题:")
                for issue in by_severity[severity]:
                    print(f"  文件: {issue['file']}")
                    if issue['line'] > 0:
                        print(f"  行号: {issue['line']}")
                    print(f"  类型: {issue['type']}")
                    print(f"  内容: {issue['content']}")
                    print("  " + "-" * 40)

        return False

    def suggest_fixes(self):
        """提供修复建议"""
        print("\n修复建议:")
        print("1. 将真实API密钥移动到 .env 文件或环境变量中")
        print("2. 更新 .gitignore 文件，确保敏感文件不被跟踪")
        print("3. 使用配置模板文件，在README中说明如何配置")
        print("4. 考虑使用 git-secrets 工具防止敏感信息提交")

        # 如果有被Git跟踪的敏感文件，提供清理命令
        git_issues = [i for i in self.issues if i['type'] == 'git_tracked']
        if git_issues:
            print("\n紧急修复 - 移除已跟踪的敏感文件:")
            for issue in git_issues:
                print(f"git rm --cached {issue['file']}")
            print("git commit -m 'Remove sensitive files from tracking'")

def main():
    print("GitHub发布前安全检查")
    print("=" * 40)

    checker = SecurityChecker()

    # 扫描项目文件
    checker.scan_project()

    # 检查Git状态
    checker.check_git_status()

    # 生成报告
    is_safe = checker.generate_report()

    if not is_safe:
        checker.suggest_fixes()
        print("\n结论: 建议修复所有问题后再发布到GitHub")
        return 1
    else:
        print("结论: 项目已准备好发布到GitHub!")
        return 0

if __name__ == "__main__":
    exit(main())