import requests
import time
import random
import json
import re
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
from fake_useragent import UserAgent

from config import SPIDER_CONFIG, RESTAURANT_CONFIG


class DianpingSpider:
    """大众点评餐厅评论爬虫"""

    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.setup_logging()
        self.setup_session()
        self.driver = None

    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('spider.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_session(self):
        """设置请求会话"""
        headers = SPIDER_CONFIG['HEADERS'].copy()
        headers['User-Agent'] = self.ua.random
        self.session.headers.update(headers)

        # 设置重试策略
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        retry_strategy = Retry(
            total=SPIDER_CONFIG['RETRY_TIMES'],
            backoff_factor=1,
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
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument(f'--user-agent={self.ua.random}')

            # 设置无头模式（可选）
            # chrome_options.add_argument('--headless')

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            # 执行反检测脚本
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def search_restaurant(self, restaurant_name, city='北京'):
        """搜索餐厅"""
        self.setup_driver()

        try:
            # 访问大众点评搜索页面
            search_url = f"https://www.dianping.com/search/keyword/{city}/0_{restaurant_name}"
            self.logger.info(f"搜索餐厅: {search_url}")

            self.driver.get(search_url)
            time.sleep(random.uniform(2, 4))

            # 等待搜索结果加载
            wait = WebDriverWait(self.driver, 10)
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

                            # 获取其他信息
                            address_elem = item.find('span', class_='addr')
                            address = address_elem.get_text(strip=True) if address_elem else ''

                            rating_elem = item.find('span', class_='star')
                            rating = rating_elem.get('title', '') if rating_elem else ''

                            restaurants.append({
                                'name': name,
                                'url': urljoin('https://www.dianping.com', url),
                                'address': address,
                                'rating': rating
                            })
                    except Exception as e:
                        self.logger.warning(f"解析餐厅信息失败: {e}")
                        continue

            self.logger.info(f"找到 {len(restaurants)} 家餐厅")
            return restaurants

        except Exception as e:
            self.logger.error(f"搜索餐厅失败: {e}")
            return []

    def get_restaurant_comments(self, restaurant_url, months=3):
        """获取餐厅评论"""
        self.setup_driver()

        try:
            self.logger.info(f"获取餐厅评论: {restaurant_url}")
            self.driver.get(restaurant_url)
            time.sleep(random.uniform(2, 4))

            # 点击查看全部评论
            try:
                review_tab = self.driver.find_element(By.XPATH, "//a[contains(@href, '/review')]")
                review_url = review_tab.get_attribute('href')
                self.driver.get(review_url)
                time.sleep(random.uniform(2, 4))
            except:
                self.logger.warning("未找到评论页面链接")
                return []

            comments = []
            page = 1
            target_date = datetime.now() - timedelta(days=months * 30)

            while page <= 50:  # 限制最大页数防止无限循环
                self.logger.info(f"爬取第 {page} 页评论...")

                # 等待页面加载
                wait = WebDriverWait(self.driver, 10)
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

                comments.extend(page_comments)

                # 检查是否还有下一页
                try:
                    next_btn = self.driver.find_element(By.XPATH, "//a[@class='next']")
                    if 'disabled' in next_btn.get_attribute('class'):
                        break
                    next_btn.click()
                    time.sleep(random.uniform(2, 4))
                    page += 1
                except:
                    self.logger.info("没有下一页")
                    break

                # 随机延迟
                time.sleep(random.uniform(*SPIDER_CONFIG['DELAY_RANGE']))

            self.logger.info(f"共获取 {len(comments)} 条评论")
            return comments

        except Exception as e:
            self.logger.error(f"获取评论失败: {e}")
            return []

    def parse_comments_page(self, soup, target_date):
        """解析评论页面"""
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

                # 提取评分
                rating_elem = review.find('span', class_='item-rank-rst')
                rating = 0
                if rating_elem:
                    rating_class = rating_elem.get('class', [])
                    for cls in rating_class:
                        if cls.startswith('irr-star'):
                            rating = int(cls.split('irr-star')[1]) / 10
                            break

                # 提取时间
                time_elem = review.find('span', class_='time')
                review_time = ''
                if time_elem:
                    review_time = time_elem.get_text(strip=True)

                # 检查时间是否在范围内
                if review_time and not self.is_within_timerange(review_time, target_date):
                    continue

                # 提取用户信息
                user_elem = review.find('div', class_='dper-info')
                username = ''
                if user_elem:
                    name_elem = user_elem.find('a')
                    if name_elem:
                        username = name_elem.get_text(strip=True)

                # 提取标签
                tags = []
                tag_container = review.find('div', class_='review-tags')
                if tag_container:
                    for tag_elem in tag_container.find_all('span', class_='tag'):
                        tags.append(tag_elem.get_text(strip=True))

                comments.append({
                    'content': content,
                    'rating': rating,
                    'time': review_time,
                    'username': username,
                    'tags': tags,
                    'crawl_time': datetime.now().isoformat()
                })

            except Exception as e:
                self.logger.warning(f"解析单条评论失败: {e}")
                continue

        return comments

    def is_within_timerange(self, time_str, target_date):
        """检查时间是否在目标范围内"""
        try:
            # 解析时间字符串
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
                # 尝试解析具体日期
                date_match = re.findall(r'(\d{4}-\d{2}-\d{2})', time_str)
                if date_match:
                    review_date = datetime.strptime(date_match[0], '%Y-%m-%d').date()
                else:
                    return True  # 无法解析时默认包含

            return review_date >= target_date.date()

        except Exception as e:
            self.logger.warning(f"时间解析失败: {time_str}, {e}")
            return True

    def save_comments(self, comments, filename='comments.json'):
        """保存评论数据"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(comments, f, ensure_ascii=False, indent=2)
            self.logger.info(f"评论数据已保存到 {filename}")

            # 同时保存为CSV格式
            if comments:
                df = pd.DataFrame(comments)
                csv_filename = filename.replace('.json', '.csv')
                df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
                self.logger.info(f"评论数据已保存到 {csv_filename}")

        except Exception as e:
            self.logger.error(f"保存评论数据失败: {e}")

    def close(self):
        """关闭资源"""
        if self.driver:
            self.driver.quit()
        self.session.close()

    def run(self):
        """运行爬虫"""
        try:
            restaurant_name = RESTAURANT_CONFIG['name']
            city = RESTAURANT_CONFIG['city']
            months = RESTAURANT_CONFIG['comment_months']

            # 搜索餐厅
            restaurants = self.search_restaurant(restaurant_name, city)

            if not restaurants:
                self.logger.error("未找到目标餐厅")
                return

            # 选择最匹配的餐厅（通常是第一个）
            target_restaurant = restaurants[0]
            self.logger.info(f"选择餐厅: {target_restaurant['name']}")

            # 获取评论
            comments = self.get_restaurant_comments(target_restaurant['url'], months)

            if comments:
                # 保存数据
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"data/comments_{restaurant_name}_{timestamp}.json"
                self.save_comments(comments, filename)

                return comments
            else:
                self.logger.warning("未获取到评论数据")
                return []

        except Exception as e:
            self.logger.error(f"爬虫运行失败: {e}")
            return []
        finally:
            self.close()


if __name__ == "__main__":
    spider = DianpingSpider()
    comments = spider.run()
    print(f"成功获取 {len(comments)} 条评论")