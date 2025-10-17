# 大众点评餐厅评论爬虫配置文件

# 爬虫配置
SPIDER_CONFIG = {
    # 请求头配置
    'HEADERS': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    },

    # 延迟配置
    'DELAY_RANGE': (1, 3),  # 请求间隔（秒）
    'RETRY_TIMES': 3,  # 重试次数
    'TIMEOUT': 10,  # 超时时间

    # 代理配置（可选）
    'USE_PROXY': False,
    'PROXY_LIST': [],

    # 数据存储配置
    'DATA_DIR': 'data',
    'BACKUP_DIR': 'backup',
}

# 目标餐厅配置
RESTAURANT_CONFIG = {
    'name': '嫩牛家潮汕火锅',
    'city': '北京',
    'keywords': ['嫩牛家', '潮汕火锅'],
    'comment_months': 3,  # 抓取最近几个月的评论
}

# 文本分析配置
ANALYSIS_CONFIG = {
    # 停用词文件
    'STOPWORDS_FILE': 'utils/stopwords.txt',

    # 关键词提取参数
    'KEYWORD_TOP_K': 100,
    'MIN_WORD_LENGTH': 2,

    # 情感分析配置
    'SENTIMENT_THRESHOLD': {
        'positive': 0.6,
        'negative': -0.1,
    },

    # 标签分类
    'LABEL_CATEGORIES': {
        '味道': ['好吃', '美味', '鲜美', '香', '甜', '辣', '清淡', '重口味', '口感', '味道'],
        '服务': ['服务', '态度', '热情', '周到', '贴心', '耐心', '专业', '效率'],
        '环境': ['环境', '装修', '氛围', '干净', '卫生', '舒适', '安静', '嘈杂'],
        '价格': ['价格', '便宜', '实惠', '性价比', '贵', '值得', '划算'],
        '食材': ['新鲜', '食材', '牛肉', '火锅', '蔬菜', '海鲜', '质量'],
    }
}

# 词云图配置
WORDCLOUD_CONFIG = {
    'width': 800,
    'height': 600,
    'max_words': 200,
    'font_path': None,  # 中文字体路径，可设置为思源黑体等
    'background_color': 'white',
    'colormap': 'viridis',
}

# Web展示配置
WEB_CONFIG = {
    'host': '127.0.0.1',
    'port': 5000,
    'debug': True,
}