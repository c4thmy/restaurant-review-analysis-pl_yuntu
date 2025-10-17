# 官方API餐厅数据获取完整指南

## 🎯 概述

本指南详细介绍如何使用官方API接口合法获取餐厅数据，并进行完整的分析和可视化处理。

### 支持的官方API平台
- **高德地图 POI API** - 国内领先的位置服务
- **百度地图 Place API** - 全面的地点信息服务
- **腾讯位置服务 API** - 腾讯系生态位置服务

### 核心优势
✅ **完全合法** - 使用官方授权的API接口
✅ **数据质量高** - 官方维护的高质量数据
✅ **稳定可靠** - 企业级服务保障
✅ **功能丰富** - 支持多维度数据获取

---

## 🚀 快速开始

### 1. 环境准备

```bash
cd @cc-code

# 安装依赖包
pip install requests beautifulsoup4 jieba wordcloud matplotlib

# 确保目录结构完整
mkdir -p data logs backup
```

### 2. 申请API密钥

#### 高德地图API
1. 访问：https://lbs.amap.com/
2. 注册开发者账号
3. 创建应用
4. 申请"Web服务API"密钥
5. 配额：免费版每日30万次调用

#### 百度地图API
1. 访问：https://lbsyun.baidu.com/
2. 注册开发者账号
3. 创建应用
4. 申请"Place API"密钥
5. 配额：免费版每日10万次调用

#### 腾讯位置服务API
1. 访问：https://lbs.qq.com/
2. 注册开发者账号
3. 创建应用
4. 申请"WebService API"密钥
5. 配额：免费版每日1万次调用

### 3. 配置API密钥

编辑 `api_keys_template.json` 文件：

```json
{
  \"amap\": \"your_actual_amap_key_here\",
  \"baidu\": \"your_actual_baidu_ak_here\",
  \"tencent\": \"your_actual_tencent_key_here\"
}
```

### 4. 运行完整流程

```bash
# 方式1: 使用完整pipeline
python ccc-api_data_pipeline.py

# 方式2: 使用主程序集成
python ccc-main.py api-search \"火锅\" --city 北京

# 方式3: 分步执行
python ccc-official_api_client.py  # 获取数据
python ccc-main.py analyze data/api_restaurants_*.json  # 分析数据
python ccc-main.py wordcloud data/*_analysis.json  # 生成词云
```

---

## 📊 使用示例

### 示例1: 搜索特定类型餐厅

```python
from ccc_api_data_pipeline import OfficialAPIDataProcessor

# 初始化处理器
processor = OfficialAPIDataProcessor('api_keys_template.json')

# 搜索火锅店
results = processor.run_full_pipeline(
    keyword=\"火锅\",
    city=\"北京\",
    limit_per_platform=20
)

print(f\"找到餐厅数量: {results['summary']['total_found']}\")
```

### 示例2: 多城市数据对比

```python
cities = [\"北京\", \"上海\", \"广州\", \"深圳\"]
keyword = \"川菜\"

for city in cities:
    print(f\"正在搜索 {city} 的 {keyword} 餐厅...\")
    results = processor.run_full_pipeline(keyword, city, 15)
    print(f\"{city}: 找到 {len(results.get('restaurants', []))} 家餐厅\")
```

### 示例3: 特定品牌分析

```python
# 搜索知名餐厅品牌
brands = [\"海底捞\", \"西贝\", \"外婆家\", \"呷哺呷哺\"]

for brand in brands:
    results = processor.run_full_pipeline(
        keyword=brand,
        city=\"全国\",  # 某些API支持全国搜索
        limit_per_platform=50
    )
```

---

## 🔧 核心功能详解

### 1. 数据获取功能

#### MultiAPIRestaurantSearcher 类
- **功能**: 多平台并行搜索
- **支持**: 高德、百度、腾讯三大平台
- **特性**: 自动去重、结果合并、错误处理

```python
searcher = MultiAPIRestaurantSearcher(api_keys)
results = searcher.search_all_platforms(\"餐厅名\", \"城市\", limit=20)
```

#### 数据字段说明
```json
{
  \"id\": \"餐厅唯一标识\",
  \"name\": \"餐厅名称\",
  \"address\": \"详细地址\",
  \"location\": {\"lat\": 纬度, \"lng\": 经度},
  \"phone\": \"联系电话\",
  \"category\": \"餐厅类型\",
  \"rating\": \"评分(如有)\",
  \"tags\": [\"标签列表\"],
  \"source\": \"数据来源平台\"
}
```

### 2. 数据处理Pipeline

#### 完整处理流程
1. **数据获取** - 调用官方API获取餐厅信息
2. **格式转换** - 转换为统一的分析格式
3. **文本分析** - 提取关键词、分析情感倾向
4. **可视化** - 生成词云图和统计图表

#### OfficialAPIDataProcessor 类
```python
processor = OfficialAPIDataProcessor()

# 执行完整pipeline
results = processor.run_full_pipeline(
    keyword=\"搜索词\",
    city=\"城市名\",
    limit_per_platform=20
)
```

### 3. 分析和可视化

#### 支持的分析类型
- **基础统计**: 餐厅数量、分布、类型统计
- **地理分析**: 位置分布、区域密度
- **文本分析**: 餐厅名称关键词提取
- **标签分析**: 餐厅特色标签统计

#### 生成的可视化内容
- **整体词云**: 所有餐厅的关键词云图
- **分类词云**: 按餐厅类型分类的词云
- **统计图表**: 评分分布、类型占比等

---

## 📋 API限制和注意事项

### 调用限制

| 平台 | 免费额度 | 超限收费 | QPS限制 |
|------|----------|----------|---------|
| 高德地图 | 30万次/日 | ¥1-3/千次 | 200次/秒 |
| 百度地图 | 10万次/日 | ¥1-5/千次 | 100次/秒 |
| 腾讯地图 | 1万次/日 | ¥1-4/千次 | 50次/秒 |

### 使用建议

#### 1. 合理控制调用频率
```python
import time

# 在循环中添加延迟
for keyword in keywords:
    results = searcher.search_all_platforms(keyword, city)
    time.sleep(0.1)  # 避免超过QPS限制
```

#### 2. 缓存和去重
```python
# 避免重复搜索相同关键词
search_cache = {}
cache_key = f\"{keyword}_{city}\"

if cache_key not in search_cache:
    results = searcher.search_all_platforms(keyword, city)
    search_cache[cache_key] = results
```

#### 3. 错误处理和重试
```python
import random

def search_with_retry(keyword, city, max_retries=3):
    for attempt in range(max_retries):
        try:
            return searcher.search_all_platforms(keyword, city)
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = random.uniform(1, 3) * (attempt + 1)
                time.sleep(wait_time)
            else:
                raise e
```

---

## 🎨 高级功能

### 1. 自定义数据处理

#### 扩展分析器
```python
class CustomRestaurantAnalyzer(CommentAnalyzer):
    def analyze_restaurant_names(self, restaurants):
        \"\"\"分析餐厅名称特征\"\"\"
        names = [r['name'] for r in restaurants]
        # 自定义分析逻辑
        return analysis_results
```

#### 添加新的API平台
```python
class NewAPIClient:
    def search_restaurants(self, keyword, city):
        # 实现新平台的API调用
        pass

# 集成到现有框架
searcher.add_platform('new_platform', NewAPIClient())
```

### 2. 批量处理和调度

#### 批量搜索脚本
```python
def batch_search(keywords, cities):
    results = {}

    for keyword in keywords:
        for city in cities:
            key = f\"{keyword}_{city}\"
            try:
                result = processor.run_full_pipeline(keyword, city)
                results[key] = result
                print(f\"✅ 完成: {key}\")
            except Exception as e:
                print(f\"❌ 失败: {key} - {e}\")

    return results

# 使用示例
keywords = [\"火锅\", \"川菜\", \"粤菜\", \"湘菜\"]
cities = [\"北京\", \"上海\", \"广州\", \"深圳\"]
batch_results = batch_search(keywords, cities)
```

#### 定时任务集成
```python
import schedule

def daily_restaurant_update():
    \"\"\"每日餐厅数据更新\"\"\"
    keywords = [\"热门餐厅\", \"新开餐厅\"]
    for keyword in keywords:
        processor.run_full_pipeline(keyword, \"北京\")

# 设置定时任务
schedule.every().day.at(\"02:00\").do(daily_restaurant_update)
```

---

## 🔍 故障排除

### 常见问题及解决方案

#### 1. API密钥无效
**问题**: 返回认证失败错误
**解决**:
- 检查密钥是否正确配置
- 确认API服务是否已开通
- 检查应用配额是否用完

#### 2. 调用频率超限
**问题**: 返回QPS超限错误
**解决**:
```python
# 添加请求间隔
time.sleep(0.1)  # 每次请求间隔100ms

# 使用指数退避重试
def exponential_backoff_retry(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if \"rate limit\" in str(e).lower():
                wait_time = (2 ** i) + random.uniform(0, 1)
                time.sleep(wait_time)
            else:
                raise e
```

#### 3. 数据格式错误
**问题**: 返回数据格式与预期不符
**解决**:
```python
def safe_get_value(data, key, default=None):
    \"\"\"安全获取数据值\"\"\"
    try:
        return data.get(key, default) if isinstance(data, dict) else default
    except:
        return default

# 使用示例
name = safe_get_value(restaurant_data, 'name', '未知餐厅')
```

#### 4. 网络连接问题
**问题**: 请求超时或连接失败
**解决**:
```python
# 配置更长的超时时间
session.timeout = 30

# 使用代理或更换网络
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080'
}
session.proxies.update(proxies)
```

---

## 📈 性能优化

### 1. 并发处理
```python
import concurrent.futures
import threading

class ThreadSafeAPIClient:
    def __init__(self):
        self.lock = threading.Lock()
        self.request_count = 0

    def search_with_limit(self, keyword, city):
        with self.lock:
            self.request_count += 1
            if self.request_count > 100:  # 达到限制
                time.sleep(60)  # 等待1分钟
                self.request_count = 0

        return self.search_restaurants(keyword, city)

# 并发搜索
def concurrent_search(keyword_city_pairs):
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for keyword, city in keyword_city_pairs:
            future = executor.submit(client.search_with_limit, keyword, city)
            futures.append(future)

        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f\"并发搜索失败: {e}\")

    return results
```

### 2. 数据缓存
```python
import sqlite3
import json
from datetime import datetime, timedelta

class APIResultCache:
    def __init__(self, db_path='api_cache.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS api_cache (
                key TEXT PRIMARY KEY,
                data TEXT,
                timestamp DATETIME,
                expires_at DATETIME
            )
        ''')
        conn.close()

    def get_cached_result(self, keyword, city, max_age_hours=24):
        cache_key = f\"{keyword}_{city}\"
        conn = sqlite3.connect(self.db_path)

        cursor = conn.execute(
            'SELECT data FROM api_cache WHERE key = ? AND expires_at > ?',
            (cache_key, datetime.now())
        )

        result = cursor.fetchone()
        conn.close()

        if result:
            return json.loads(result[0])
        return None

    def cache_result(self, keyword, city, data, max_age_hours=24):
        cache_key = f\"{keyword}_{city}\"
        expires_at = datetime.now() + timedelta(hours=max_age_hours)

        conn = sqlite3.connect(self.db_path)
        conn.execute(
            'INSERT OR REPLACE INTO api_cache (key, data, timestamp, expires_at) VALUES (?, ?, ?, ?)',
            (cache_key, json.dumps(data), datetime.now(), expires_at)
        )
        conn.commit()
        conn.close()
```

---

## 🎯 最佳实践

### 1. 数据质量保证
- **数据验证**: 检查必要字段完整性
- **格式标准化**: 统一数据格式和编码
- **去重处理**: 避免重复数据影响分析

### 2. 合规使用
- **遵守API条款**: 严格按照各平台使用条款执行
- **合理使用频率**: 不超过平台限制，避免被封禁
- **数据用途声明**: 明确数据使用目的和范围

### 3. 系统稳定性
- **错误处理**: 完善的异常捕获和处理机制
- **日志记录**: 详细的操作日志便于问题排查
- **监控报警**: 及时发现并处理异常情况

### 4. 成本控制
- **预算管理**: 设置API调用预算和监控
- **智能缓存**: 避免重复调用相同数据
- **分级策略**: 根据重要性调整数据获取频率

---

## 📞 技术支持

### 官方文档链接
- [高德地图API文档](https://lbs.amap.com/api/webservice/guide/api/search)
- [百度地图API文档](https://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi)
- [腾讯位置服务API文档](https://lbs.qq.com/service/webService/webServiceGuide/webServiceSearch)

### 社区支持
- 官方技术论坛
- 开发者QQ群/微信群
- GitHub Issues

### 商业支持
- 企业级技术支持服务
- 定制化解决方案
- 专业培训服务

---

## 📄 附录

### A. API接口详细参数

#### 高德地图搜索参数
```
key: API密钥
keywords: 搜索关键词
city: 城市名称
types: POI类型代码
page: 页码
offset: 每页数量
extensions: 返回详情级别
```

#### 百度地图搜索参数
```
ak: API密钥
query: 搜索关键词
tag: 分类标签
region: 地域范围
page_num: 页码
page_size: 每页数量
scope: 检索结果详细程度
```

#### 腾讯地图搜索参数
```
key: API密钥
keyword: 搜索关键词
boundary: 地域范围
page_index: 页码
page_size: 每页数量
orderby: 排序方式
filter: 筛选条件
```

### B. 数据字段映射表

| 统一字段 | 高德地图 | 百度地图 | 腾讯地图 |
|---------|----------|----------|----------|
| id | id | uid | id |
| name | name | name | title |
| address | address | address | address |
| phone | tel | telephone | tel |
| location | location | location | location |
| category | type | tag | category |

### C. 错误代码对照表

| 错误类型 | 高德 | 百度 | 腾讯 | 处理建议 |
|---------|------|------|------|----------|
| 认证失败 | 10001 | 101 | 110 | 检查API密钥 |
| 配额不足 | 10003 | 302 | 109 | 购买配额或等待重置 |
| QPS超限 | 10004 | 4 | 121 | 降低请求频率 |
| 参数错误 | 20000 | 100 | 310 | 检查请求参数 |

---

*最后更新时间: 2024年10月16日*
*文档版本: v1.0*