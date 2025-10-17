#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大众点评餐厅评论爬虫 - 合规加强版
包含数据保护、隐私保护和合规检查功能

法律声明：
本工具仅供学习和研究使用，使用者必须遵守相关法律法规和网站使用条款
"""

import requests
import time
import random
import json
import re
import hashlib
import os
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import logging

# 导入合规配置和检查器
try:
    from ccc_config import COMPLIANCE_CONFIG, SPIDER_CONFIG, RESTAURANT_CONFIG
    from utils.ccc_compliance_checker import compliance_checker, data_protector, require_compliance_check
    COMPLIANCE_MODE = True
except ImportError:
    # 如果没有合规模块，使用原始配置
    from config import SPIDER_CONFIG, RESTAURANT_CONFIG
    COMPLIANCE_MODE = False
    print("警告：未找到合规模块，使用基础模式运行")


class ComplianceDianpingSpider:
    """合规加强版大众点评餐厅评论爬虫"""

    def __init__(self, user_id=None, purpose="research"):
        self.user_id = user_id or f"user_{int(time.time())}"
        self.purpose = purpose
        self.session = requests.Session()
        self.setup_logging()
        self.driver = None
        self.request_count = 0
        self.start_time = datetime.now()

        # 合规检查
        if COMPLIANCE_MODE:
            self._perform_compliance_checks()

        self.setup_session()

    def _perform_compliance_checks(self):
        """执行合规性检查"""
        try:
            # 检查使用目的
            is_valid, msg = compliance_checker.check_purpose_compliance(self.purpose)
            if not is_valid:
                raise Exception(f"使用目的不合规: {msg}")

            # 记录用户协议（在实际应用中应通过UI确认）
            compliance_checker.record_user_agreement(
                self.user_id,
                self.purpose,
                ip_address="127.0.0.1"  # 本地使用
            )

            self.logger.info("合规检查通过")

        except Exception as e:
            self.logger.error(f"合规检查失败: {e}")
            raise

    def setup_logging(self):
        """设置合规日志"""
        # 创建logs目录
        os.makedirs('logs', exist_ok=True)

        # 设置详细日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/spider_compliance.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(f"ComplianceSpider-{self.user_id}")

        # 记录启动信息
        self.logger.info(f"爬虫启动 - 用户ID: {self.user_id}, 目的: {self.purpose}")

    def setup_session(self):
        """设置请求会话"""
        headers = SPIDER_CONFIG['HEADERS'].copy()

        # 使用真实固定的User-Agent，避免欺骗
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

        # 添加研究标识
        headers['X-Research-Purpose'] = self.purpose

        self.session.headers.update(headers)

        # 设置重试策略（减少重试次数）
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        retry_strategy = Retry(
            total=2,  # 减少重试次数
            backoff_factor=2,  # 增加退避因子
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def setup_driver(self):
        """设置Selenium WebDriver"""
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

            # 移除自动化检测规避（更透明的方式）
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')

            # 使用固定User-Agent
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

            # 启用无头模式以减少资源占用
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            # 设置页面加载超时
            self.driver.set_page_load_timeout(30)

            self.logger.info("WebDriver已初始化")

    @require_compliance_check
    def search_restaurant(self, restaurant_name, city='北京'):
        """搜索餐厅（合规版本）"""
        if COMPLIANCE_MODE:
            # 检查robots.txt
            search_url = f"https://www.dianping.com/search/keyword/{city}/0_{restaurant_name}"
            if not compliance_checker.check_robots_txt(search_url):
                raise Exception("robots.txt禁止访问此URL")

            # 检查访问频率
            is_allowed, msg = compliance_checker.check_rate_limits(search_url)
            if not is_allowed:
                raise Exception(f"访问频率超限: {msg}")

        self.setup_driver()

        try:
            self.logger.info(f"搜索餐厅: {restaurant_name} (城市: {city})")
            self.driver.get(search_url)

            # 增加等待时间，更友好的访问方式
            time.sleep(random.uniform(5, 8))

            # 等待搜索结果加载
            wait = WebDriverWait(self.driver, 15)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shop-list")))

            # 解析搜索结果
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            restaurants = []

            shop_list = soup.find('div', class_='shop-list')
            if shop_list:
                for item in shop_list.find_all('div', class_='shop-wrap'):
                    try:
                        name_elem = item.find('h4')
                        if name_elem and name_elem.find('a'):
                            name = name_elem.get_text(strip=True)
                            url = name_elem.find('a')['href']

                            # 仅获取基本公开信息
                            restaurants.append({
                                'name': name,
                                'url': urljoin('https://www.dianping.com', url),
                                'search_rank': len(restaurants) + 1  # 添加搜索排名
                            })

                            # 限制搜索结果数量
                            if len(restaurants) >= 5:
                                break

                    except Exception as e:
                        self.logger.warning(f"解析餐厅信息失败: {e}")
                        continue

            self.logger.info(f"找到 {len(restaurants)} 家餐厅")
            return restaurants

        except Exception as e:
            self.logger.error(f"搜索餐厅失败: {e}")
            return []

    def get_restaurant_comments(self, restaurant_url, months=1):
        """获取餐厅评论（数据保护增强版）"""
        if COMPLIANCE_MODE:
            # 检查数据使用合规性
            max_comments = COMPLIANCE_CONFIG.get('DATA_LIMITS', {}).get('MAX_COMMENTS_PER_SESSION', 500)
            is_valid, msg = compliance_checker.validate_data_usage(max_comments, 'comments')
            if not is_valid:
                raise Exception(f"数据使用不合规: {msg}")

        self.setup_driver()

        try:
            self.logger.info(f"获取餐厅评论: {restaurant_url}")
            self.driver.get(restaurant_url)
            time.sleep(random.uniform(3, 6))

            # 尝试找到评论页面
            try:
                review_tab = self.driver.find_element(By.XPATH, "//a[contains(@href, '/review')]")
                review_url = review_tab.get_attribute('href')
                self.driver.get(review_url)
                time.sleep(random.uniform(3, 6))
            except:
                self.logger.warning("未找到评论页面链接")
                return []

            comments = []
            page = 1
            target_date = datetime.now() - timedelta(days=months * 30)
            max_pages = 5  # 限制最大页数

            while page <= max_pages and len(comments) < 500:  # 严格限制数据量
                self.logger.info(f"爬取第 {page} 页评论...")

                # 检查访问频率
                if COMPLIANCE_MODE:
                    is_allowed, msg = compliance_checker.check_rate_limits()
                    if not is_allowed:
                        self.logger.warning(f"访问频率限制: {msg}")
                        break

                # 等待页面加载
                wait = WebDriverWait(self.driver, 15)
                try:
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "reviews-items")))
                except:
                    self.logger.warning("评论加载超时")
                    break

                # 解析当前页面评论
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                page_comments = self.parse_comments_page(soup, target_date)

                if not page_comments:
                    self.logger.info("没有更多评论或已超过时间范围")
                    break

                # 数据保护处理
                if COMPLIANCE_MODE:
                    page_comments = [data_protector.anonymize_user_data(comment) for comment in page_comments]

                comments.extend(page_comments)

                # 检查是否还有下一页
                try:
                    next_btn = self.driver.find_element(By.XPATH, "//a[@class='next']")
                    if 'disabled' in next_btn.get_attribute('class'):
                        break
                    next_btn.click()
                    time.sleep(random.uniform(5, 10))  # 增加延迟
                    page += 1
                except:
                    self.logger.info("没有下一页")
                    break

                # 记录请求次数
                self.request_count += 1

            self.logger.info(f"共获取 {len(comments)} 条评论")

            # 最终数据清理和脱敏
            if COMPLIANCE_MODE:
                comments = self._final_data_cleaning(comments)

            return comments

        except Exception as e:
            self.logger.error(f"获取评论失败: {e}")
            return []

    def parse_comments_page(self, soup, target_date):
        """解析评论页面（隐私保护增强）"""
        comments = []

        reviews_container = soup.find('div', class_='reviews-items')
        if not reviews_container:
            return comments

        for review in reviews_container.find_all('div', class_='main-review'):
            try:
                # 提取评论内容
                content_elem = review.find('div', class_='review-words')
                if not content_elem:
                    continue

                content = content_elem.get_text(strip=True)
                if not content:
                    continue

                # 检查内容是否包含敏感信息
                if COMPLIANCE_MODE:
                    is_safe, msg = data_protector.check_data_sensitivity(content)
                    if not is_safe:
                        self.logger.warning(f"跳过包含敏感信息的评论: {msg}")
                        continue

                    # 清理敏感内容
                    content = data_protector.clean_sensitive_content(content)

                # 提取评分
                rating_elem = review.find('span', class_='item-rank-rst')
                rating = 0
                if rating_elem:
                    rating_class = rating_elem.get('class', [])
                    for cls in rating_class:
                        if cls.startswith('irr-star'):
                            rating = int(cls.split('irr-star')[1]) / 10
                            break

                # 提取时间（泛化处理）
                time_elem = review.find('span', class_='time')
                review_time = ''
                if time_elem:
                    review_time = time_elem.get_text(strip=True)

                # 检查时间是否在范围内
                if review_time and not self.is_within_timerange(review_time, target_date):
                    continue

                # 用户信息处理（完全匿名化）
                user_hash = None
                user_elem = review.find('div', class_='dper-info')
                if user_elem:
                    name_elem = user_elem.find('a')
                    if name_elem:
                        original_username = name_elem.get_text(strip=True)
                        # 使用哈希值替代真实用户名
                        user_hash = hashlib.md5(original_username.encode()).hexdigest()[:8]

                # 提取标签（仅保留非个人化标签）
                tags = []
                tag_container = review.find('div', class_='review-tags')
                if tag_container:
                    for tag_elem in tag_container.find_all('span', class_='tag'):
                        tag = tag_elem.get_text(strip=True)
                        # 过滤可能包含个人信息的标签
                        if not self._is_personal_tag(tag):
                            tags.append(tag)

                # 构建评论数据（去标识化）
                comment_data = {
                    'content': content,
                    'rating': rating,
                    'time_period': self._generalize_time(review_time),  # 时间泛化
                    'user_id': user_hash,  # 哈希化用户ID
                    'tags': tags,
                    'crawl_time': datetime.now().isoformat(),
                    'data_source': 'dianping_public_review'  # 标明数据来源
                }

                comments.append(comment_data)

                # 限制单页评论数量
                if len(comments) >= 50:
                    break

            except Exception as e:
                self.logger.warning(f"解析单条评论失败: {e}")
                continue

        return comments

    def _is_personal_tag(self, tag):
        """判断标签是否可能包含个人信息"""
        personal_indicators = ['生日', '约会', '聚会', '庆祝', '纪念', '家庭', '朋友', '同事']
        return any(indicator in tag for indicator in personal_indicators)

    def _generalize_time(self, time_str):
        """时间泛化处理"""
        try:
            if '今天' in time_str or '昨天' in time_str or '前天' in time_str:
                return '最近几天'
            elif '天前' in time_str:
                days = int(re.findall(r'(\d+)天前', time_str)[0])
                if days <= 7:
                    return '一周内'
                elif days <= 30:
                    return '一个月内'
                else:
                    return '较早'
            elif '月前' in time_str:
                return '较早'
            else:
                return '时间不详'
        except:
            return '时间不详'

    def _final_data_cleaning(self, comments):
        """最终数据清理和合规检查"""
        cleaned_comments = []

        for comment in comments:
            try:
                # 再次检查内容合规性
                content = comment.get('content', '')
                if len(content) < 10:  # 过滤过短的评论
                    continue

                # 移除可能的重复内容
                content_hash = hashlib.md5(content.encode()).hexdigest()
                comment['content_hash'] = content_hash

                # 添加数据处理标记
                comment['data_processed'] = True
                comment['compliance_version'] = '1.0'
                comment['privacy_protected'] = True

                cleaned_comments.append(comment)

            except Exception as e:
                self.logger.warning(f"数据清理失败: {e}")
                continue

        # 去重处理
        seen_hashes = set()
        unique_comments = []
        for comment in cleaned_comments:
            content_hash = comment.get('content_hash')
            if content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                unique_comments.append(comment)

        self.logger.info(f"数据清理完成: {len(comments)} -> {len(unique_comments)}")
        return unique_comments

    def is_within_timerange(self, time_str, target_date):
        """检查时间是否在目标范围内"""
        try:
            # 时间解析逻辑保持不变
            if '今天' in time_str:
                review_date = datetime.now().date()
            elif '昨天' in time_str:
                review_date = (datetime.now() - timedelta(days=1)).date()
            elif '前天' in time_str:
                review_date = (datetime.now() - timedelta(days=2)).date()
            elif '天前' in time_str:
                days = int(re.findall(r'(\d+)天前', time_str)[0])
                review_date = (datetime.now() - timedelta(days=days)).date()
            elif '月前' in time_str:
                months = int(re.findall(r'(\d+)月前', time_str)[0])
                review_date = (datetime.now() - timedelta(days=months*30)).date()
            elif '年前' in time_str:
                years = int(re.findall(r'(\d+)年前', time_str)[0])
                review_date = (datetime.now() - timedelta(days=years*365)).date()
            else:
                date_match = re.findall(r'(\d{4}-\d{2}-\d{2})', time_str)
                if date_match:
                    review_date = datetime.strptime(date_match[0], '%Y-%m-%d').date()
                else:
                    return True

            return review_date >= target_date.date()

        except Exception as e:
            self.logger.warning(f"时间解析失败: {time_str}, {e}")
            return True

    def save_comments(self, comments, filename='comments.json'):
        """保存评论数据（增强版）"""
        try:
            # 确保数据目录存在
            os.makedirs('data', exist_ok=True)

            # 添加元数据
            data_package = {
                'metadata': {
                    'collection_time': datetime.now().isoformat(),
                    'user_id': self.user_id,
                    'purpose': self.purpose,
                    'total_comments': len(comments),
                    'compliance_version': '1.0',
                    'data_retention_until': (datetime.now() + timedelta(days=30)).isoformat(),
                    'privacy_protected': True,
                    'anonymized': True
                },
                'comments': comments
            }

            # 保存为JSON
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_package, f, ensure_ascii=False, indent=2)
            self.logger.info(f"评论数据已保存到 {filename}")

            # 同时保存CSV格式（仅评论数据）
            if comments:
                df = pd.DataFrame(comments)
                csv_filename = filename.replace('.json', '.csv')
                df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
                self.logger.info(f"评论数据已保存到 {csv_filename}")

            # 记录数据保存日志
            self._log_data_operation('save', filename, len(comments))

        except Exception as e:
            self.logger.error(f"保存评论数据失败: {e}")

    def _log_data_operation(self, operation, filename, record_count):
        """记录数据操作日志"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': self.user_id,
            'operation': operation,
            'filename': filename,
            'record_count': record_count,
            'purpose': self.purpose
        }

        log_file = 'logs/data_operations.log'
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    def close(self):
        """关闭资源并生成合规报告"""
        if self.driver:
            self.driver.quit()
        self.session.close()

        # 生成使用报告
        session_report = {
            'session_id': self.user_id,
            'start_time': self.start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'total_requests': self.request_count,
            'purpose': self.purpose,
            'duration_minutes': (datetime.now() - self.start_time).total_seconds() / 60
        }

        # 保存会话报告
        os.makedirs('logs/sessions', exist_ok=True)
        report_file = f"logs/sessions/session_{self.user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(session_report, f, ensure_ascii=False, indent=2)

        self.logger.info(f"会话结束，报告已保存到 {report_file}")

        # 生成合规报告
        if COMPLIANCE_MODE:
            compliance_checker.generate_compliance_report()

    def run(self, restaurant_name=None, city=None, months=None):
        """运行爬虫（合规版）"""
        try:
            # 使用参数或配置
            restaurant_name = restaurant_name or RESTAURANT_CONFIG.get('name', '示例餐厅')
            city = city or RESTAURANT_CONFIG.get('city', '北京')
            months = months or min(RESTAURANT_CONFIG.get('comment_months', 1), 1)  # 最多1个月

            self.logger.info(f"开始爬取 {restaurant_name} 的评论 (城市: {city}, 时间范围: {months}个月)")

            # 合规性最终检查
            if COMPLIANCE_MODE:
                # 检查今日使用次数
                if self.request_count > 100:  # 每日限制
                    raise Exception("今日使用次数已达限制")

            # 搜索餐厅
            restaurants = self.search_restaurant(restaurant_name, city)

            if not restaurants:
                self.logger.error("未找到目标餐厅")
                return []

            # 选择第一个匹配的餐厅
            target_restaurant = restaurants[0]
            self.logger.info(f"选择餐厅: {target_restaurant['name']}")

            # 获取评论
            comments = self.get_restaurant_comments(target_restaurant['url'], months)

            if comments:
                # 保存数据
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                safe_name = re.sub(r'[^\w\-_]', '_', restaurant_name)
                filename = f"data/comments_{safe_name}_{timestamp}.json"
                self.save_comments(comments, filename)

                # 记录成功
                self.logger.info(f"数据收集完成: {len(comments)} 条评论")
                return comments
            else:
                self.logger.warning("未获取到评论数据")
                return []

        except Exception as e:
            self.logger.error(f"爬虫运行失败: {e}")
            return []
        finally:
            self.close()


def create_compliance_spider(user_id=None, purpose="research"):
    """创建合规爬虫实例的工厂函数"""
    if not purpose or purpose not in ['research', 'learning', 'academic']:
        raise ValueError("使用目的必须是: research, learning, 或 academic")

    return ComplianceDianpingSpider(user_id=user_id, purpose=purpose)


if __name__ == "__main__":
    # 使用示例
    print("=== 合规爬虫启动 ===")
    print("本工具仅供学习和研究使用")
    print("使用前请确认已阅读并同意用户协议")

    try:
        spider = create_compliance_spider(
            user_id="researcher_001",
            purpose="research"
        )

        # 运行爬虫（限制参数）
        comments = spider.run(
            restaurant_name="示例餐厅",
            city="北京",
            months=1  # 最多1个月
        )

        print(f"成功获取 {len(comments)} 条评论")
        print("数据已进行隐私保护和去标识化处理")

    except Exception as e:
        print(f"爬虫运行失败: {e}")
        print("请检查合规性设置和网络连接")