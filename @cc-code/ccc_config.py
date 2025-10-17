# -*- coding: utf-8 -*-
"""
配置文件 - 合规版本
Configuration for Compliance Mode

包含餐厅搜索、网络请求、合规控制等配置
"""

import os
from datetime import datetime

# 餐厅配置
RESTAURANT_CONFIG = {
    'default_city': '北京',
    'max_pages': 3,  # 限制页数，避免过度请求
    'max_comments_per_page': 10,  # 限制每页评论数
    'request_delay': 2,  # 请求间隔（秒）
    'timeout': 30,  # 请求超时
    'max_total_comments': 50,  # 总评论数限制
}

# Web界面配置
WEB_CONFIG = {
    'host': '127.0.0.1',
    'port': 5000,
    'debug': False,  # 生产环境关闭debug
    'max_upload_size': 10 * 1024 * 1024,  # 10MB
}

# 合规配置
COMPLIANCE_CONFIG = {
    'enabled': True,
    'legal_notice_required': True,
    'user_agreement_required': True,
    'purpose_declaration_required': True,

    # 频率限制
    'rate_limits': {
        'requests_per_minute': 10,
        'requests_per_hour': 100,
        'requests_per_day': 500,
        'max_concurrent_requests': 2
    },

    # 数据保护
    'data_protection': {
        'anonymize_usernames': True,
        'anonymize_user_ids': True,
        'hash_sensitive_data': True,
        'retention_days': 30,
        'auto_cleanup': True
    },

    # 用途限制
    'allowed_purposes': [
        'research',
        'learning',
        'academic'
    ],

    # robots.txt检查
    'robots_check': {
        'enabled': True,
        'respect_crawl_delay': True,
        'respect_user_agent': True
    },

    # 审计日志
    'audit_logging': {
        'enabled': True,
        'log_file': 'logs/compliance_audit.log',
        'log_level': 'INFO',
        'include_requests': True,
        'include_data_access': True
    }
}

# 用户代理配置
USER_AGENT_CONFIG = {
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'headers': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
}

# API配置
API_CONFIG = {
    'base_url': 'https://www.dianping.com',
    'search_endpoint': '/search/keyword',
    'shop_endpoint': '/shop',
    'review_endpoint': '/review_all',
    'max_retries': 3,
    'backoff_factor': 1,
}

# 数据存储配置
STORAGE_CONFIG = {
    'data_dir': 'data',
    'backup_dir': 'backup',
    'logs_dir': 'logs',
    'temp_dir': 'temp',
    'max_file_size': 100 * 1024 * 1024,  # 100MB
    'compression': True,
    'encryption': False,  # 可根据需要启用
}

# 分析配置
ANALYSIS_CONFIG = {
    'min_comment_length': 5,
    'max_comment_length': 1000,
    'stop_words_file': 'data/stop_words.txt',
    'sentiment_threshold': {
        'positive': 0.6,
        'negative': -0.6
    },
    'keyword_min_freq': 2,
    'max_keywords': 100,
    'categories': [
        '环境', '服务', '口味', '价格', '位置'
    ]
}

# 词云配置
WORDCLOUD_CONFIG = {
    'width': 800,
    'height': 600,
    'max_words': 100,
    'background_color': 'white',
    'colormap': 'viridis',
    'font_path': None,  # 系统会自动寻找中文字体
    'min_font_size': 12,
    'max_font_size': 100,
    'prefer_horizontal': 0.7,
    'relative_scaling': 0.5
}

# 合规验证函数
def validate_compliance_config():
    """验证合规配置"""
    errors = []

    # 检查必要的目录
    required_dirs = [
        STORAGE_CONFIG['data_dir'],
        STORAGE_CONFIG['logs_dir']
    ]

    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
            except Exception as e:
                errors.append(f"无法创建目录 {dir_path}: {e}")

    # 检查合规文件
    required_files = [
        'USER_AGREEMENT.md',
        'RESEARCH_PURPOSE.md'
    ]

    for file_path in required_files:
        if not os.path.exists(file_path):
            errors.append(f"缺少合规文件: {file_path}")

    return errors

# 获取当前配置摘要
def get_config_summary():
    """获取配置摘要"""
    return {
        'compliance_enabled': COMPLIANCE_CONFIG['enabled'],
        'max_comments': RESTAURANT_CONFIG['max_total_comments'],
        'rate_limit': COMPLIANCE_CONFIG['rate_limits']['requests_per_minute'],
        'data_retention': COMPLIANCE_CONFIG['data_protection']['retention_days'],
        'anonymization': COMPLIANCE_CONFIG['data_protection']['anonymize_usernames'],
        'audit_logging': COMPLIANCE_CONFIG['audit_logging']['enabled']
    }