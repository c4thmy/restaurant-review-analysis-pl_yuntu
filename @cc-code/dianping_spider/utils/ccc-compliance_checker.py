#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合规性检查和限制机制模块
确保爬虫使用符合法律法规和伦理要求
"""

import os
import time
import json
import hashlib
import requests
from datetime import datetime, timedelta
from collections import defaultdict
from urllib.robotparser import RobotFileParser
import logging

try:
    from ccc_config import COMPLIANCE_CONFIG, LEGAL_CONFIG, SPIDER_CONFIG
except ImportError:
    # 如果新配置文件不存在，使用默认安全配置
    COMPLIANCE_CONFIG = {
        'RATE_LIMITS': {
            'MIN_DELAY': 5,
            'MAX_REQUESTS_PER_MINUTE': 6,
            'MAX_REQUESTS_PER_HOUR': 100,
            'MAX_REQUESTS_PER_DAY': 500,
        }
    }


class ComplianceChecker:
    """合规性检查器"""

    def __init__(self):
        self.logger = self._setup_logging()
        self.request_log = defaultdict(list)
        self.user_agreements = {}
        self.robots_cache = {}
        self.last_request_time = 0

    def _setup_logging(self):
        """设置合规日志"""
        logger = logging.getLogger('compliance')
        logger.setLevel(logging.INFO)

        # 创建日志目录
        os.makedirs('logs', exist_ok=True)

        # 文件处理器
        handler = logging.FileHandler('logs/compliance.log', encoding='utf-8')
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def check_purpose_compliance(self, stated_purpose):
        """检查使用目的是否合规"""
        allowed_purposes = COMPLIANCE_CONFIG.get('PURPOSE_LIMITATION', {}).get('ALLOWED_PURPOSES', [])
        forbidden_purposes = COMPLIANCE_CONFIG.get('PURPOSE_LIMITATION', {}).get('FORBIDDEN_PURPOSES', [])

        if stated_purpose.lower() in forbidden_purposes:
            self.logger.error(f"禁止的使用目的: {stated_purpose}")
            return False, f"使用目的'{stated_purpose}'不被允许"

        if stated_purpose.lower() not in allowed_purposes:
            self.logger.warning(f"未明确允许的使用目的: {stated_purpose}")
            return False, f"使用目的'{stated_purpose}'需要额外确认"

        self.logger.info(f"使用目的合规: {stated_purpose}")
        return True, "使用目的符合要求"

    def check_robots_txt(self, url):
        """检查并遵守robots.txt规则"""
        try:
            from urllib.parse import urljoin, urlparse
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

            if base_url in self.robots_cache:
                rp = self.robots_cache[base_url]
            else:
                robots_url = urljoin(base_url, '/robots.txt')
                rp = RobotFileParser()
                rp.set_url(robots_url)
                try:
                    rp.read()
                    self.robots_cache[base_url] = rp
                    self.logger.info(f"已加载robots.txt: {robots_url}")
                except Exception as e:
                    self.logger.warning(f"无法加载robots.txt: {e}")
                    return True  # 如果无法加载，默认允许

            # 检查是否允许访问
            user_agent = SPIDER_CONFIG.get('HEADERS', {}).get('User-Agent', '*')
            can_fetch = rp.can_fetch(user_agent, url)

            if not can_fetch:
                self.logger.error(f"robots.txt禁止访问: {url}")
                return False

            # 检查延迟要求
            crawl_delay = rp.crawl_delay(user_agent)
            if crawl_delay:
                min_delay = COMPLIANCE_CONFIG.get('RATE_LIMITS', {}).get('MIN_DELAY', 1)
                if crawl_delay > min_delay:
                    self.logger.info(f"robots.txt要求延迟: {crawl_delay}秒")
                    # 更新配置中的延迟设置
                    SPIDER_CONFIG['DELAY_RANGE'] = (crawl_delay, crawl_delay + 2)

            return True

        except Exception as e:
            self.logger.error(f"robots.txt检查失败: {e}")
            return False

    def check_rate_limits(self, url=None):
        """检查访问频率限制"""
        now = datetime.now()
        rate_limits = COMPLIANCE_CONFIG.get('RATE_LIMITS', {})

        # 检查最小延迟
        min_delay = rate_limits.get('MIN_DELAY', 3)
        if self.last_request_time > 0:
            elapsed = time.time() - self.last_request_time
            if elapsed < min_delay:
                wait_time = min_delay - elapsed
                self.logger.info(f"等待 {wait_time:.1f} 秒以遵守延迟限制")
                time.sleep(wait_time)

        # 记录请求时间
        domain = self._extract_domain(url) if url else 'default'
        self.request_log[domain].append(now)

        # 清理旧记录
        self._cleanup_old_requests(domain, now)

        # 检查各种时间窗口的限制
        checks = [
            ('MAX_REQUESTS_PER_MINUTE', 60, '分钟'),
            ('MAX_REQUESTS_PER_HOUR', 3600, '小时'),
            ('MAX_REQUESTS_PER_DAY', 86400, '天')
        ]

        for limit_key, seconds, unit in checks:
            max_requests = rate_limits.get(limit_key, float('inf'))
            if max_requests < float('inf'):
                recent_requests = [
                    req_time for req_time in self.request_log[domain]
                    if (now - req_time).total_seconds() <= seconds
                ]

                if len(recent_requests) >= max_requests:
                    self.logger.error(f"超过{unit}访问限制: {len(recent_requests)}/{max_requests}")
                    return False, f"超过每{unit}{max_requests}次的访问限制"

        self.last_request_time = time.time()
        return True, "访问频率符合要求"

    def _extract_domain(self, url):
        """提取域名"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return 'unknown'

    def _cleanup_old_requests(self, domain, now):
        """清理24小时前的请求记录"""
        cutoff = now - timedelta(days=1)
        self.request_log[domain] = [
            req_time for req_time in self.request_log[domain]
            if req_time > cutoff
        ]

    def verify_user_agreement(self, user_id, purpose):
        """验证用户协议同意"""
        agreement_key = hashlib.md5(f"{user_id}_{purpose}".encode()).hexdigest()

        if agreement_key not in self.user_agreements:
            self.logger.warning(f"用户未同意使用协议: {user_id}")
            return False, "需要先同意用户协议"

        agreement = self.user_agreements[agreement_key]
        if not agreement.get('accepted', False):
            return False, "用户协议未被接受"

        # 检查协议是否过期（30天）
        accepted_time = datetime.fromisoformat(agreement.get('timestamp', ''))
        if (datetime.now() - accepted_time).days > 30:
            self.logger.warning(f"用户协议已过期: {user_id}")
            return False, "用户协议已过期，需要重新同意"

        return True, "用户协议有效"

    def record_user_agreement(self, user_id, purpose, ip_address=None):
        """记录用户协议同意"""
        agreement_key = hashlib.md5(f"{user_id}_{purpose}".encode()).hexdigest()

        agreement_record = {
            'user_id': user_id,
            'purpose': purpose,
            'ip_address': ip_address,
            'timestamp': datetime.now().isoformat(),
            'accepted': True,
            'version': LEGAL_CONFIG.get('TERMS_OF_SERVICE', {}).get('version', '1.0')
        }

        self.user_agreements[agreement_key] = agreement_record

        # 保存到文件
        self._save_agreement_record(agreement_record)

        self.logger.info(f"用户协议记录: {user_id} - {purpose}")
        return True

    def _save_agreement_record(self, record):
        """保存协议记录到文件"""
        try:
            os.makedirs('logs/agreements', exist_ok=True)
            filename = f"logs/agreements/{record['user_id']}_{datetime.now().strftime('%Y%m%d')}.json"

            agreements = []
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    agreements = json.load(f)

            agreements.append(record)

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(agreements, f, ensure_ascii=False, indent=2)

        except Exception as e:
            self.logger.error(f"保存协议记录失败: {e}")

    def validate_data_usage(self, data_size, data_type):
        """验证数据使用是否合规"""
        # 数据量限制
        max_comments = COMPLIANCE_CONFIG.get('DATA_LIMITS', {}).get('MAX_COMMENTS_PER_SESSION', 500)

        if data_type == 'comments' and data_size > max_comments:
            self.logger.error(f"数据量超限: {data_size} > {max_comments}")
            return False, f"单次获取评论数量不能超过{max_comments}条"

        # 数据类型检查
        allowed_types = ['comments', 'ratings', 'basic_info']
        if data_type not in allowed_types:
            self.logger.error(f"不允许的数据类型: {data_type}")
            return False, f"不允许获取{data_type}类型的数据"

        return True, "数据使用符合要求"

    def check_data_retention(self, data_path):
        """检查数据保留期限"""
        try:
            if not os.path.exists(data_path):
                return True, "文件不存在"

            # 获取文件创建时间
            create_time = datetime.fromtimestamp(os.path.getctime(data_path))
            retention_days = LEGAL_CONFIG.get('DATA_PROCESSING', {}).get('retention_period_days', 30)

            if (datetime.now() - create_time).days > retention_days:
                self.logger.warning(f"数据超过保留期限: {data_path}")
                return False, f"数据已超过{retention_days}天保留期限，应当删除"

            return True, "数据保留期限符合要求"

        except Exception as e:
            self.logger.error(f"数据保留检查失败: {e}")
            return False, "数据保留检查失败"

    def generate_compliance_report(self):
        """生成合规报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'checks_performed': {
                'robots_txt_checked': len(self.robots_cache),
                'rate_limit_domains': len(self.request_log),
                'user_agreements': len(self.user_agreements),
            },
            'compliance_status': 'COMPLIANT',
            'recommendations': []
        }

        # 检查是否有违规记录
        violations = self._check_violations()
        if violations:
            report['compliance_status'] = 'VIOLATIONS_FOUND'
            report['violations'] = violations

        # 生成建议
        recommendations = self._generate_recommendations()
        report['recommendations'] = recommendations

        # 保存报告
        self._save_compliance_report(report)

        return report

    def _check_violations(self):
        """检查违规记录"""
        violations = []

        # 检查日志中的错误
        try:
            with open('logs/compliance.log', 'r', encoding='utf-8') as f:
                lines = f.readlines()
                error_lines = [line for line in lines if 'ERROR' in line]
                if error_lines:
                    violations.extend([line.strip() for line in error_lines[-10:]])  # 最近10条错误
        except FileNotFoundError:
            pass

        return violations

    def _generate_recommendations(self):
        """生成合规建议"""
        recommendations = []

        # 检查延迟设置
        current_delay = SPIDER_CONFIG.get('DELAY_RANGE', (1, 3))[0]
        min_required = COMPLIANCE_CONFIG.get('RATE_LIMITS', {}).get('MIN_DELAY', 3)

        if current_delay < min_required:
            recommendations.append(f"建议增加请求延迟至{min_required}秒以上")

        # 检查数据保留
        if os.path.exists('data'):
            old_files = []
            for root, dirs, files in os.walk('data'):
                for file in files:
                    filepath = os.path.join(root, file)
                    if os.path.getctime(filepath) < (datetime.now() - timedelta(days=30)).timestamp():
                        old_files.append(filepath)

            if old_files:
                recommendations.append(f"发现{len(old_files)}个超过保留期限的数据文件，建议及时清理")

        return recommendations

    def _save_compliance_report(self, report):
        """保存合规报告"""
        try:
            os.makedirs('logs/compliance_reports', exist_ok=True)
            filename = f"logs/compliance_reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)

            self.logger.info(f"合规报告已保存: {filename}")

        except Exception as e:
            self.logger.error(f"保存合规报告失败: {e}")


class DataProtector:
    """数据保护器"""

    def __init__(self):
        self.logger = logging.getLogger('data_protection')

    def anonymize_user_data(self, data):
        """匿名化用户数据"""
        if isinstance(data, dict):
            return self._anonymize_dict(data)
        elif isinstance(data, list):
            return [self.anonymize_user_data(item) for item in data]
        else:
            return data

    def _anonymize_dict(self, data_dict):
        """匿名化字典数据"""
        anonymized = data_dict.copy()

        # 移除或脱敏敏感字段
        sensitive_fields = ['username', 'user_id', 'phone', 'email', 'real_name']

        for field in sensitive_fields:
            if field in anonymized:
                if COMPLIANCE_CONFIG.get('DATA_PROTECTION', {}).get('ANONYMIZE_USERS', True):
                    anonymized[field] = self._hash_sensitive_data(str(anonymized[field]))

        # 移除时间戳中的精确时间，只保留日期
        if 'time' in anonymized:
            anonymized['time'] = self._generalize_time(anonymized['time'])

        return anonymized

    def _hash_sensitive_data(self, data):
        """对敏感数据进行哈希处理"""
        return hashlib.md5(data.encode()).hexdigest()[:8]

    def _generalize_time(self, time_str):
        """泛化时间信息"""
        try:
            # 只保留日期，移除具体时间
            if isinstance(time_str, str) and len(time_str) > 10:
                return time_str[:10]  # 只保留YYYY-MM-DD
            return time_str
        except:
            return time_str

    def check_data_sensitivity(self, text):
        """检查文本中的敏感信息"""
        import re

        sensitive_patterns = [
            (r'\d{11}', '手机号码'),
            (r'\d{3}-\d{4}-\d{4}', '电话号码'),
            (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '邮箱地址'),
            (r'\d{15}|\d{18}', '身份证号'),
            (r'\d{4}\s?\d{4}\s?\d{4}\s?\d{4}', '银行卡号'),
        ]

        found_sensitive = []
        for pattern, name in sensitive_patterns:
            if re.search(pattern, text):
                found_sensitive.append(name)

        if found_sensitive:
            self.logger.warning(f"发现敏感信息: {', '.join(found_sensitive)}")
            return False, f"文本包含敏感信息: {', '.join(found_sensitive)}"

        return True, "未发现敏感信息"

    def clean_sensitive_content(self, text):
        """清理文本中的敏感内容"""
        import re

        # 替换模式
        patterns = [
            (r'\d{11}', '[手机号]'),
            (r'\d{3}-\d{4}-\d{4}', '[电话]'),
            (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[邮箱]'),
            (r'\d{15}|\d{18}', '[身份证]'),
            (r'\d{4}\s?\d{4}\s?\d{4}\s?\d{4}', '[银行卡]'),
        ]

        cleaned_text = text
        for pattern, replacement in patterns:
            cleaned_text = re.sub(pattern, replacement, cleaned_text)

        return cleaned_text


# 全局合规检查器实例
compliance_checker = ComplianceChecker()
data_protector = DataProtector()


def require_compliance_check(func):
    """装饰器：要求合规检查"""
    def wrapper(*args, **kwargs):
        # 在函数执行前进行合规检查
        if not compliance_checker.check_rate_limits():
            raise Exception("访问频率超限，请稍后再试")

        return func(*args, **kwargs)

    return wrapper


def require_user_agreement(purpose):
    """装饰器：要求用户协议"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 这里应该检查用户是否已同意协议
            # 在Web界面中实现具体的检查逻辑
            return func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    # 测试合规检查器
    checker = ComplianceChecker()

    # 测试目的检查
    print("=== 目的合规检查 ===")
    result, msg = checker.check_purpose_compliance("research")
    print(f"研究目的: {result} - {msg}")

    result, msg = checker.check_purpose_compliance("commercial_scraping")
    print(f"商业爬取: {result} - {msg}")

    # 测试频率限制
    print("\n=== 频率限制检查 ===")
    for i in range(3):
        result, msg = checker.check_rate_limits("https://example.com")
        print(f"请求 {i+1}: {result} - {msg}")
        time.sleep(1)

    # 生成合规报告
    print("\n=== 合规报告 ===")
    report = checker.generate_compliance_report()
    print(f"合规状态: {report['compliance_status']}")
    print(f"建议: {report['recommendations']}")