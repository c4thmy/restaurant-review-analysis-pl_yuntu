# -*- coding: utf-8 -*-
"""
文本分析器（简化版）
Text Analyzer (Simplified)

提供中文评论的分析功能，不依赖外部库
"""

import re
import json
from datetime import datetime
from collections import Counter

class CommentAnalyzer:
    """评论分析器（简化版）"""

    def __init__(self):
        self.stop_words = self._load_stop_words()

    def _load_stop_words(self):
        """加载停用词"""
        default_stop_words = {
            '的', '了', '是', '我', '你', '他', '她', '它', '们', '这', '那',
            '有', '在', '也', '都', '就', '还', '会', '要', '可以', '没有',
            '很', '比较', '非常', '特别', '挺', '蛮', '还是', '觉得',
            '一个', '一些', '一点', '一下', '时候', '地方', '东西'
        }
        return default_stop_words

    def simple_chinese_tokenize(self, text):
        """简单的中文分词"""
        # 移除标点符号和数字
        text = re.sub(r'[^\u4e00-\u9fa5]', ' ', text)

        # 基于常见词汇进行简单分词
        words = []
        i = 0
        while i < len(text):
            # 尝试匹配2-4字的词汇
            for length in [4, 3, 2, 1]:
                if i + length <= len(text):
                    word = text[i:i+length]
                    if word and word not in self.stop_words:
                        words.append(word)
                        i += length
                        break
            else:
                i += 1

        return words

    def extract_keywords(self, text, top_n=10):
        """提取关键词"""
        # 简单分词
        words = self.simple_chinese_tokenize(text)

        # 过滤停用词和长度
        filtered_words = [
            word for word in words
            if len(word) >= 2 and word not in self.stop_words
        ]

        # 统计词频
        word_freq = Counter(filtered_words)
        return word_freq.most_common(top_n)

    def extract_phrases(self, text, max_length=6):
        """提取短语"""
        # 简单的短语提取
        sentences = re.split(r'[，。！？；]', text)
        phrases = []

        for sentence in sentences:
            sentence = sentence.strip()
            if 3 <= len(sentence) <= max_length:
                phrases.append(sentence)

        return list(set(phrases))

    def analyze_sentiment(self, text):
        """分析情感"""
        positive_words = {
            '好', '棒', '赞', '不错', '满意', '推荐', '喜欢', '美味',
            '新鲜', '干净', '热情', '优秀', '值得', '正宗', '地道'
        }

        negative_words = {
            '差', '坏', '烂', '难吃', '贵', '慢', '脏', '冷', '咸',
            '淡', '油腻', '失望', '一般', '不好', '排队', '等'
        }

        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)

        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'

    def generate_tags(self, keywords, phrases):
        """生成用户标签"""
        tags = []

        # 从关键词生成标签
        for word, freq in keywords:
            if freq >= 2:  # 频率>=2的词作为标签
                tags.append((word, freq))

        # 从短语中提取有价值的标签
        for phrase in phrases:
            # 简单的短语处理
            filtered_phrase = re.sub(r'[^\u4e00-\u9fa5]', '', phrase)
            if 2 <= len(filtered_phrase) <= 4 and filtered_phrase not in self.stop_words:
                tags.append((filtered_phrase, 1))

        # 去重并排序
        tag_dict = {}
        for tag, freq in tags:
            tag_dict[tag] = tag_dict.get(tag, 0) + freq

        return sorted(tag_dict.items(), key=lambda x: x[1], reverse=True)

    def analyze_comments(self, comments):
        """分析评论列表"""
        if not comments:
            return {
                "basic_stats": {
                    "total_comments": 0,
                    "average_rating": 0,
                    "privacy_protected": True
                },
                "keywords": [],
                "tags": [],
                "sentiment_analysis": {
                    "positive": 0,
                    "neutral": 0,
                    "negative": 0
                },
                "timestamp": datetime.now().isoformat()
            }

        # 基础统计
        total_comments = len(comments)
        ratings = [c.get('rating', 0) for c in comments if c.get('rating')]
        average_rating = sum(ratings) / len(ratings) if ratings else 0

        # 合并所有评论文本
        all_text = ' '.join([c.get('comment_text', '') for c in comments])

        # 提取关键词和短语
        keywords = self.extract_keywords(all_text, top_n=10)
        phrases = self.extract_phrases(all_text)

        # 生成标签
        tags = self.generate_tags(keywords, phrases[:10])

        # 情感分析
        sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
        for comment in comments:
            sentiment = self.analyze_sentiment(comment.get('comment_text', ''))
            sentiment_counts[sentiment] += 1

        return {
            "basic_stats": {
                "total_comments": total_comments,
                "average_rating": round(average_rating, 1),
                "privacy_protected": True
            },
            "keywords": keywords,
            "tags": tags,
            "sentiment_analysis": sentiment_counts,
            "timestamp": datetime.now().isoformat(),
            "demo_analysis": True
        }