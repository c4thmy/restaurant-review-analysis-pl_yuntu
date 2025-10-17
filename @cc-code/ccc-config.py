# 大众点评餐厅评论爬虫配置文件
#
# 法律声明：本工具仅供学习和研究使用
# 使用者必须遵守相关法律法规和网站使用条款
#

import os
from datetime import datetime

# ============= 合规性配置 =============
COMPLIANCE_CONFIG = {
    # 使用限制
    'PURPOSE_LIMITATION': {
        'ALLOWED_PURPOSES': ['research', 'learning', 'academic'],  # 允许的使用目的
        'FORBIDDEN_PURPOSES': ['commercial_scraping', 'data_resale', 'competitive_intelligence'],  # 禁止的用途
    },

    # 频率限制
    'RATE_LIMITS': {
        'MIN_DELAY': 3,              # 最小请求间隔（秒）
        'MAX_REQUESTS_PER_MINUTE': 10,  # 每分钟最大请求数
        'MAX_REQUESTS_PER_HOUR': 200,   # 每小时最大请求数
        'MAX_REQUESTS_PER_DAY': 1000,   # 每天最大请求数
        'RESPECT_ROBOTS_TXT': True,      # 遵守robots.txt
    },

    # 数据保护
    'DATA_PROTECTION': {
        'ANONYMIZE_USERS': True,         # 匿名化用户信息
        'ENCRYPT_STORAGE': False,        # 加密存储（可选）
        'AUTO_DELETE_DAYS': 30,          # 自动删除数据天数
        'EXCLUDE_PERSONAL_INFO': True,   # 排除个人信息
    },

    # 使用条款确认
    'TERMS_ACCEPTANCE': {
        'REQUIRE_AGREEMENT': True,       # 要求用户同意条款
        'SHOW_DISCLAIMER': True,         # 显示免责声明
        'LOG_ACCEPTANCE': True,          # 记录用户同意
    }
}

# ============= 爬虫配置 =============
SPIDER_CONFIG = {
    # 请求头配置 - 模拟真实用户浏览器
    'HEADERS': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    },

    # 延迟配置 - 遵守网站负载
    'DELAY_RANGE': (5, 10),  # 增加请求间隔，减轻服务器负担
    'RETRY_TIMES': 2,        # 减少重试次数
    'TIMEOUT': 15,           # 增加超时时间，避免频繁重试
    'CONCURRENT_LIMIT': 1,   # 限制并发请求数

    # 合规性检查
    'CHECK_ROBOTS_TXT': True,     # 检查并遵守robots.txt
    'RESPECT_RATE_LIMITS': True,  # 遵守频率限制
    'USER_AGENT_ROTATION': False, # 不使用User-Agent轮换（避免误导）

    # 代理配置（建议不使用以保证透明性）
    'USE_PROXY': False,
    'PROXY_LIST': [],

    # 数据存储配置
    'DATA_DIR': 'data',
    'BACKUP_DIR': 'backup',
    'LOG_DIR': 'logs',
}

# ============= 目标配置 =============
RESTAURANT_CONFIG = {
    'name': '示例餐厅',  # 默认示例，避免直接指向特定商家
    'city': '北京',
    'keywords': [],
    'comment_months': 1,  # 限制为1个月，减少数据量
    'max_comments': 500,  # 限制最大评论数量
}

# ============= 文本分析配置 =============
ANALYSIS_CONFIG = {
    # 停用词文件
    'STOPWORDS_FILE': 'utils/stopwords.txt',

    # 关键词提取参数
    'KEYWORD_TOP_K': 50,   # 减少关键词数量
    'MIN_WORD_LENGTH': 2,

    # 情感分析配置
    'SENTIMENT_THRESHOLD': {
        'positive': 0.6,
        'negative': -0.1,
    },

    # 数据脱敏配置
    'ANONYMIZATION': {
        'REMOVE_USERNAMES': True,     # 移除用户名
        'REMOVE_PHONE_NUMBERS': True, # 移除电话号码
        'REMOVE_EMAIL': True,         # 移除邮箱
        'MASK_PERSONAL_INFO': True,   # 屏蔽个人信息
    },

    # 标签分类 - 仅保留非个人化标签
    'LABEL_CATEGORIES': {
        '口味体验': ['口味', '味道', '美味', '好吃', '鲜美'],
        '服务质量': ['服务', '态度', '热情', '周到', '专业'],
        '环境氛围': ['环境', '装修', '氛围', '舒适', '安静'],
        '性价比': ['价格', '实惠', '性价比', '值得', '划算'],
        '食材品质': ['新鲜', '食材', '品质', '质量'],
    }
}

# ============= 词云图配置 =============
WORDCLOUD_CONFIG = {
    'width': 800,
    'height': 600,
    'max_words': 100,  # 减少词汇数量
    'font_path': None,
    'background_color': 'white',
    'colormap': 'viridis',
    'exclude_personal_terms': True,  # 排除可能的个人相关词汇
}

# ============= Web展示配置 =============
WEB_CONFIG = {
    'host': '127.0.0.1',  # 仅本地访问
    'port': 5000,
    'debug': False,       # 生产环境关闭调试
    'show_disclaimer': True,  # 显示免责声明
    'require_agreement': True, # 要求用户同意条款
}

# ============= 法律合规配置 =============
LEGAL_CONFIG = {
    # 使用条款
    'TERMS_OF_SERVICE': {
        'version': '1.0',
        'last_updated': '2024-10-15',
        'acceptance_required': True,
    },

    # 数据处理限制
    'DATA_PROCESSING': {
        'retention_period_days': 30,      # 数据保留期限
        'auto_anonymize': True,           # 自动匿名化
        'encryption_at_rest': False,      # 静态加密（可选）
        'audit_logging': True,            # 审计日志
    },

    # 访问控制
    'ACCESS_CONTROL': {
        'require_authentication': False,  # 是否需要认证
        'log_user_actions': True,         # 记录用户操作
        'ip_rate_limiting': True,         # IP访问频率限制
    }
}

# ============= 功能开关 =============
FEATURE_FLAGS = {
    'ENABLE_BATCH_PROCESSING': False,    # 禁用批量处理
    'ENABLE_REAL_TIME_CRAWLING': False,  # 禁用实时爬取
    'ENABLE_API_ACCESS': False,          # 禁用API访问
    'ENABLE_DATA_EXPORT': True,          # 允许数据导出（仅用于研究）
    'ENABLE_COMMERCIAL_FEATURES': False, # 禁用商业功能
}

# ============= 监控和审计 =============
MONITORING_CONFIG = {
    'LOG_LEVEL': 'INFO',
    'LOG_RETENTION_DAYS': 30,
    'AUDIT_ALL_ACTIONS': True,
    'ALERT_ON_VIOLATIONS': True,
    'COMPLIANCE_REPORTING': True,
}

# ============= 环境检查 =============
def validate_environment():
    """验证运行环境是否符合合规要求"""
    checks = []

    # 检查目的声明
    if not os.path.exists('RESEARCH_PURPOSE.txt'):
        checks.append("缺少研究目的声明文件")

    # 检查用户协议
    if not os.path.exists('USER_AGREEMENT.txt'):
        checks.append("缺少用户协议文件")

    # 检查数据目录权限
    if not os.access('.', os.W_OK):
        checks.append("当前目录无写入权限")

    return checks

# ============= 默认免责声明 =============
DEFAULT_DISCLAIMER = """
法律声明和使用条款

1. 本工具仅供学习、研究和学术用途使用
2. 禁止用于任何商业目的或数据转售
3. 使用者必须遵守目标网站的使用条款和robots.txt规则
4. 使用者必须遵守所在地区的法律法规
5. 本工具开发者不承担因使用本工具产生的任何法律后果
6. 数据获取需遵循合理使用原则，不得对目标网站造成负担
7. 获取的数据仅可用于研究分析，不得泄露用户隐私信息
8. 使用者需要定期删除获取的数据，建议保留期不超过30天

继续使用本工具即表示您已阅读并同意上述条款。
"""

# ============= 版本信息 =============
VERSION_INFO = {
    'version': '1.0.0-research',
    'release_date': '2024-10-15',
    'license': 'Educational Use Only',
    'compliance_level': 'Research Grade',
}