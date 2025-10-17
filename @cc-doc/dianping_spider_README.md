# 大众点评餐厅评论分析系统

## 项目简介

本项目是一个基于Python的智能餐厅评论分析系统，专门用于抓取和分析大众点评网站上的餐厅评论。系统集成了网络爬虫、自然语言处理、数据可视化和Web界面等技术，能够自动获取餐厅评论、进行智能分析，并以词云图等形式直观展示分析结果。

### 主要功能

- 🕷️ **智能爬虫**: 自动抓取大众点评餐厅评论，支持自定义时间范围
- 🧠 **AI文本分析**: 使用NLP技术进行关键词提取、情感分析和标签分类
- ☁️ **词云可视化**: 生成精美的词云图，直观展示评论热点
- 🌐 **Web界面**: 提供用户友好的Web控制台
- 📊 **数据统计**: 多维度统计分析和图表展示

## 项目结构

```
dianping_spider/
├── main.py                    # 主程序入口
├── config.py                  # 配置文件
├── requirements.txt           # 依赖包列表
├── spiders/
│   └── dianping_spider.py     # 大众点评爬虫
├── utils/
│   ├── data_utils.py          # 数据管理工具
│   ├── text_analyzer.py       # 文本分析器
│   ├── wordcloud_generator.py # 词云生成器
│   └── stopwords.txt          # 中文停用词
├── web/
│   └── app.py                 # Flask Web应用
├── templates/
│   ├── index.html             # 首页模板
│   └── dashboard.html         # 控制台模板
├── static/
│   └── js/
│       └── dashboard.js       # 前端JavaScript
└── data/                      # 数据存储目录
```

## 技术栈

### 后端技术
- **Python 3.8+**: 主要开发语言
- **Selenium**: 网页自动化和动态内容抓取
- **BeautifulSoup**: HTML解析
- **Flask**: Web框架
- **jieba**: 中文分词
- **scikit-learn**: 机器学习算法
- **SnowNLP**: 中文情感分析

### 前端技术
- **HTML5/CSS3**: 页面结构和样式
- **Bootstrap 5**: 响应式UI框架
- **JavaScript ES6**: 前端逻辑
- **ECharts**: 数据可视化图表

### 数据处理
- **pandas**: 数据处理和分析
- **numpy**: 数值计算
- **matplotlib**: 图形绘制
- **wordcloud**: 词云图生成

## 安装和配置

### 1. 环境要求

- Python 3.8 或更高版本
- Chrome 浏览器 (用于Selenium WebDriver)
- 至少 4GB 内存

### 2. 安装依赖

```bash
# 克隆项目
git clone <项目地址>
cd dianping_spider

# 安装Python依赖
pip install -r requirements.txt

# 安装Chrome WebDriver (自动下载)
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
```

### 3. 配置设置

编辑 `config.py` 文件，根据需要调整配置：

```python
# 爬虫配置
SPIDER_CONFIG = {
    'DELAY_RANGE': (1, 3),  # 请求间隔
    'RETRY_TIMES': 3,       # 重试次数
    'TIMEOUT': 10,          # 超时时间
}

# 目标餐厅配置
RESTAURANT_CONFIG = {
    'name': '嫩牛家潮汕火锅',
    'city': '北京',
    'comment_months': 3,    # 抓取时间范围
}
```

## 使用指南

### 命令行模式

#### 1. 爬取评论
```bash
python main.py crawl "嫩牛家潮汕火锅" --city 北京 --months 3
```

#### 2. 分析评论
```bash
python main.py analyze data/comments_餐厅名_时间戳.json
```

#### 3. 生成词云
```bash
python main.py wordcloud data/comments_餐厅名_时间戳_analysis.json
```

#### 4. 运行完整流程
```bash
python main.py pipeline "嫩牛家潮汕火锅" --city 北京 --months 3
```

### Web界面模式

#### 启动Web服务器
```bash
python main.py web
```

然后在浏览器中访问 `http://localhost:5000`

#### Web界面功能
1. **数据爬取**: 在控制台输入餐厅信息，开始爬取
2. **智能分析**: 选择已爬取的数据文件进行分析
3. **词云生成**: 基于分析结果生成各类词云图
4. **结果展示**: 查看统计图表和分析结果
5. **文件管理**: 下载和管理数据文件

## 核心算法

### 1. 文本预处理
- 使用jieba进行中文分词
- 去除停用词和无意义词汇
- 文本清洗和标准化

### 2. 关键词提取
- TF-IDF算法计算词汇重要性
- 支持1-gram和2-gram词组
- 自定义词典优化分词效果

### 3. 情感分析
- 基于SnowNLP的情感倾向计算
- 三分类：正面、中性、负面
- 可调节的情感阈值

### 4. 标签分类
- 预定义标签类别（味道、服务、环境、价格等）
- 关键词匹配和统计
- 支持自定义标签类别

### 5. 词云生成
- 基于matplotlib和wordcloud库
- 支持中文字体渲染
- 多种样式和颜色方案

## 数据输出

### 1. 评论数据 (JSON格式)
```json
{
  "content": "评论内容",
  "rating": 4.5,
  "time": "2024-01-15",
  "username": "用户名",
  "tags": ["好吃", "新鲜"],
  "crawl_time": "2024-01-15T10:30:00"
}
```

### 2. 分析结果 (JSON格式)
```json
{
  "basic_stats": {
    "total_comments": 1000,
    "average_rating": 4.2,
    "unique_users": 950
  },
  "keywords": [["好吃", 0.8], ["新鲜", 0.7]],
  "sentiments": {
    "distribution": {"positive": 600, "neutral": 300, "negative": 100}
  },
  "labels": {
    "category_counts": {"味道": 500, "服务": 300}
  }
}
```

### 3. 词云图
- PNG格式的静态词云图
- 分类词云图（按标签分组）
- 交互式词云数据

## 高级特性

### 1. 反爬虫策略
- 随机User-Agent
- 动态延迟控制
- 模拟真实用户行为
- 请求重试机制

### 2. 数据管理
- 自动数据备份
- 文件版本控制
- 数据导入导出

### 3. 扩展性
- 模块化设计
- 可配置参数
- 插件化架构
- 支持自定义分析算法

## 注意事项

### 1. 合规使用
- 遵守网站robots.txt规则
- 合理控制爬取频率
- 仅用于学习和研究目的
- 不要进行商业用途

### 2. 性能优化
- 根据网络状况调整延迟
- 定期清理数据文件
- 监控内存使用情况

### 3. 错误处理
- 网络连接异常
- 页面结构变化
- 验证码和反爬虫机制

## 故障排除

### 常见问题

1. **ChromeDriver版本不匹配**
   ```bash
   # 重新安装WebDriver
   pip install --upgrade webdriver-manager
   ```

2. **中文字体显示问题**
   - 确保系统安装了中文字体
   - 修改config.py中的字体路径

3. **内存不足**
   - 减少爬取数量
   - 分批处理数据

4. **网络连接超时**
   - 增加超时时间设置
   - 检查网络连接

## 开发和贡献

### 本地开发

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装开发依赖
pip install -r requirements.txt
pip install -r dev-requirements.txt  # 如果有

# 运行测试
python -m pytest tests/
```

### 代码规范
- 遵循PEP 8编码规范
- 添加适当的文档字符串
- 编写单元测试
- 使用类型提示

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 联系方式

如有问题或建议，请提交Issue或Pull Request。

---

*本项目仅供学习研究使用，请遵守相关法律法规和网站使用条款。*