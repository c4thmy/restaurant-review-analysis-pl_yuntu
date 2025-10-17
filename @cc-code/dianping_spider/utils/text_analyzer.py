import re
import jieba
import pandas as pd
from collections import Counter
from snownlp import SnowNLP
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import json
from datetime import datetime

from config import ANALYSIS_CONFIG
from utils.data_utils import clean_text, Logger


class TextProcessor:
    """文本预处理器"""

    def __init__(self):
        self.logger = Logger.setup(__name__)
        self.stopwords = self.load_stopwords()
        self.setup_jieba()

    def load_stopwords(self):
        """加载停用词"""
        stopwords = set()

        # 默认中文停用词
        default_stopwords = [
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
            '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
            '自己', '这', '那', '来', '可以', '还', '比较', '非常', '太', '挺', '真的',
            '真', '超', '蛮', '感觉', '觉得', '应该', '可能', '但是', '不过', '还是',
            '这个', '那个', '这样', '那样', '这里', '那里', '时候', '地方', '什么',
            '怎么', '为什么', '因为', '所以', '如果', '虽然', '但', '而且', '或者',
            '以及', '以后', '之前', '现在', '已经', '正在', '将要', '可能', '应该',
            '需要', '希望', '想要', '喜欢', '不喜欢', '满意', '不满意', '推荐', '不推荐'
        ]
        stopwords.update(default_stopwords)

        # 尝试从文件加载
        try:
            stopwords_file = ANALYSIS_CONFIG.get('STOPWORDS_FILE')
            if stopwords_file:
                with open(stopwords_file, 'r', encoding='utf-8') as f:
                    file_stopwords = [line.strip() for line in f if line.strip()]
                    stopwords.update(file_stopwords)
        except FileNotFoundError:
            self.logger.warning("停用词文件未找到，使用默认停用词")

        self.logger.info(f"加载了 {len(stopwords)} 个停用词")
        return stopwords

    def setup_jieba(self):
        """设置jieba分词"""
        # 添加自定义词典
        custom_words = [
            '潮汕火锅', '嫩牛家', '毛肚', '黄喉', '牛肉丸', '手打牛肉丸',
            '沙茶酱', '蘸料', '清汤', '牛骨汤', '服务员', '性价比',
            '好吃', '新鲜', '不错', '一般', '难吃', '太贵', '便宜',
            '环境', '装修', '氛围', '排队', '等位', '预约'
        ]

        for word in custom_words:
            jieba.add_word(word)

    def clean_and_segment(self, text):
        """清理和分词"""
        if not text:
            return []

        # 清理文本
        cleaned_text = clean_text(text)

        # 移除数字和单个字符
        cleaned_text = re.sub(r'\d+', '', cleaned_text)

        # 分词
        words = jieba.lcut(cleaned_text)

        # 过滤停用词和短词
        filtered_words = [
            word.strip() for word in words
            if word.strip() and
               len(word.strip()) >= ANALYSIS_CONFIG['MIN_WORD_LENGTH'] and
               word.strip() not in self.stopwords
        ]

        return filtered_words

    def extract_keywords(self, texts, top_k=None):
        """提取关键词"""
        if top_k is None:
            top_k = ANALYSIS_CONFIG['KEYWORD_TOP_K']

        # 预处理文本
        processed_texts = []
        for text in texts:
            words = self.clean_and_segment(text)
            processed_texts.append(' '.join(words))

        # 使用TF-IDF提取关键词
        try:
            vectorizer = TfidfVectorizer(
                max_features=top_k * 2,
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.8
            )

            tfidf_matrix = vectorizer.fit_transform(processed_texts)
            feature_names = vectorizer.get_feature_names_out()

            # 计算每个词的平均TF-IDF值
            mean_scores = np.mean(tfidf_matrix.toarray(), axis=0)

            # 获取top-k关键词
            top_indices = np.argsort(mean_scores)[::-1][:top_k]
            keywords = [(feature_names[i], mean_scores[i]) for i in top_indices]

            return keywords

        except Exception as e:
            self.logger.error(f"关键词提取失败: {e}")

            # 回退到简单词频统计
            all_words = []
            for text in texts:
                words = self.clean_and_segment(text)
                all_words.extend(words)

            word_freq = Counter(all_words)
            return word_freq.most_common(top_k)

    def analyze_sentiment(self, text):
        """情感分析"""
        if not text:
            return {'score': 0, 'label': 'neutral'}

        try:
            s = SnowNLP(text)
            score = s.sentiments

            # 根据阈值判断情感
            thresholds = ANALYSIS_CONFIG['SENTIMENT_THRESHOLD']
            if score >= thresholds['positive']:
                label = 'positive'
            elif score <= thresholds['negative']:
                label = 'negative'
            else:
                label = 'neutral'

            return {'score': score, 'label': label}

        except Exception as e:
            self.logger.warning(f"情感分析失败: {e}")
            return {'score': 0, 'label': 'neutral'}


class CommentAnalyzer:
    """评论分析器"""

    def __init__(self):
        self.processor = TextProcessor()
        self.logger = Logger.setup(__name__)

    def analyze_comments(self, comments):
        """分析评论数据"""
        if not comments:
            return {}

        self.logger.info(f"开始分析 {len(comments)} 条评论")

        # 基础统计
        stats = self.get_basic_stats(comments)

        # 提取所有评论文本
        texts = [comment.get('content', '') for comment in comments if comment.get('content')]

        # 关键词分析
        keywords = self.processor.extract_keywords(texts)

        # 情感分析
        sentiments = self.analyze_sentiments(comments)

        # 标签分类
        labels = self.categorize_labels(texts)

        # 时间分析
        time_analysis = self.analyze_time_trends(comments)

        results = {
            'basic_stats': stats,
            'keywords': keywords,
            'sentiments': sentiments,
            'labels': labels,
            'time_analysis': time_analysis,
            'analysis_time': datetime.now().isoformat()
        }

        self.logger.info("评论分析完成")
        return results

    def get_basic_stats(self, comments):
        """获取基础统计信息"""
        total_comments = len(comments)

        # 评分统计
        ratings = [comment.get('rating', 0) for comment in comments if comment.get('rating')]
        avg_rating = np.mean(ratings) if ratings else 0

        # 文本长度统计
        text_lengths = [len(comment.get('content', '')) for comment in comments]
        avg_length = np.mean(text_lengths) if text_lengths else 0

        # 用户统计
        users = [comment.get('username', '') for comment in comments if comment.get('username')]
        unique_users = len(set(users))

        return {
            'total_comments': total_comments,
            'average_rating': round(avg_rating, 2),
            'average_length': round(avg_length, 1),
            'unique_users': unique_users,
            'rating_distribution': dict(Counter(ratings))
        }

    def analyze_sentiments(self, comments):
        """分析情感分布"""
        sentiments = []

        for comment in comments:
            text = comment.get('content', '')
            sentiment = self.processor.analyze_sentiment(text)
            sentiments.append(sentiment)

        # 统计情感分布
        labels = [s['label'] for s in sentiments]
        scores = [s['score'] for s in sentiments]

        return {
            'distribution': dict(Counter(labels)),
            'average_score': round(np.mean(scores), 3) if scores else 0,
            'details': sentiments
        }

    def categorize_labels(self, texts):
        """标签分类"""
        categories = ANALYSIS_CONFIG['LABEL_CATEGORIES']
        category_counts = {category: 0 for category in categories}
        category_keywords = {category: Counter() for category in categories}

        for text in texts:
            words = self.processor.clean_and_segment(text)
            text_lower = text.lower()

            for category, keywords in categories.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        category_counts[category] += 1
                        category_keywords[category][keyword] += 1

        # 转换Counter为普通字典
        category_keywords = {
            category: dict(counter.most_common(10))
            for category, counter in category_keywords.items()
        }

        return {
            'category_counts': category_counts,
            'category_keywords': category_keywords
        }

    def analyze_time_trends(self, comments):
        """分析时间趋势"""
        time_data = []

        for comment in comments:
            time_str = comment.get('time', '')
            rating = comment.get('rating', 0)
            sentiment = self.processor.analyze_sentiment(comment.get('content', ''))

            time_data.append({
                'time': time_str,
                'rating': rating,
                'sentiment_score': sentiment['score'],
                'sentiment_label': sentiment['label']
            })

        return time_data

    def generate_wordcloud_data(self, analysis_results):
        """生成词云数据"""
        keywords = analysis_results.get('keywords', [])

        # 转换为词云格式
        wordcloud_data = []
        for keyword, score in keywords:
            wordcloud_data.append({
                'name': keyword,
                'value': int(score * 1000)  # 放大数值便于显示
            })

        return wordcloud_data

    def save_analysis(self, results, filename):
        """保存分析结果"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            self.logger.info(f"分析结果已保存到 {filename}")
        except Exception as e:
            self.logger.error(f"保存分析结果失败: {e}")


if __name__ == "__main__":
    # 测试代码
    sample_comments = [
        {'content': '火锅很好吃，牛肉新鲜，服务态度很好', 'rating': 5},
        {'content': '环境不错，但是价格有点贵', 'rating': 4},
        {'content': '味道一般，性价比不高', 'rating': 3}
    ]

    analyzer = CommentAnalyzer()
    results = analyzer.analyze_comments(sample_comments)
    print(json.dumps(results, ensure_ascii=False, indent=2))