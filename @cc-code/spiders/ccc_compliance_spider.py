# -*- coding: utf-8 -*-
"""
合规爬虫创建器
Compliance Spider Creator

提供创建合规爬虫实例的工厂函数
"""

from datetime import datetime
import time
import hashlib

class ComplianceSpider:
    """合规爬虫类"""

    def __init__(self, user_id=None, purpose='research'):
        self.user_id = user_id or f"demo_user_{int(time.time())}"
        self.purpose = purpose
        self.start_time = datetime.now()

    def run(self, restaurant_name, city='北京', months=1):
        """运行爬虫（演示模式）"""
        print(f"[合规爬虫] 开始分析: {restaurant_name}")
        print(f"[合规爬虫] 城市: {city}")
        print(f"[合规爬虫] 用户ID: {self.user_id}")
        print(f"[合规爬虫] 用途: {self.purpose}")

        # 演示模式：返回模拟的评论数据
        demo_comments = [
            {
                "comment_id": f"demo_{i}",
                "user_id_hash": hashlib.md5(f"user_{i}".encode()).hexdigest()[:8],
                "rating": 4 + (i % 3),
                "comment_text": self._get_demo_comment(i),
                "date": "2025-10-15",
                "restaurant_name": restaurant_name,
                "city": city,
                "privacy_protected": True
            }
            for i in range(1, 6)  # 生成5条演示评论
        ]

        print(f"[合规爬虫] 完成分析，获得 {len(demo_comments)} 条评论")
        return demo_comments

    def _get_demo_comment(self, index):
        """获取演示评论内容"""
        demo_texts = [
            "味道很好，牛肉新鲜，推荐手打牛肉丸",
            "服务态度不错，环境也很干净，价格有点贵但是质量确实好",
            "火锅很正宗，沙茶酱味道不错，排队时间有点长",
            "新鲜食材，口感很棒，服务员很热情，值得推荐",
            "环境舒适，菜品丰富，就是人比较多需要等位"
        ]
        return demo_texts[index - 1] if index <= len(demo_texts) else f"演示评论内容 {index}"

def create_compliance_spider(user_id=None, purpose='research'):
    """创建合规爬虫实例"""
    return ComplianceSpider(user_id=user_id, purpose=purpose)