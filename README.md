# 大众点评餐厅评论分析系统

一个功能完整的餐厅评论数据分析系统，支持数据爬取、文本分析、情感分析和可视化展示。

## 🚀 项目特点

- **双版本架构**: 基础版本和法律合规增强版本
- **智能文本分析**: 中文分词、情感分析、关键词提取
- **美观词云生成**: 支持多种颜色方案和自定义字体
- **Web界面**: 交互式数据展示和操作界面
- **合规性保护**: 内置隐私保护和使用限制机制

## 📋 功能概览

### 核心功能
- 🕷️ **智能爬虫**: 大众点评餐厅评论数据采集
- 📊 **文本分析**: 中文自然语言处理和情感分析
- ☁️ **词云可视化**: 多样化的词云图表生成
- 🌐 **Web界面**: Flask驱动的交互式网页应用
- 🔒 **合规检查**: 自动化的法律合规和隐私保护

### 技术栈
- **爬虫**: Selenium + BeautifulSoup4
- **文本分析**: jieba + scikit-learn + SnowNLP
- **可视化**: wordcloud + matplotlib + pyecharts
- **Web框架**: Flask
- **数据处理**: pandas + numpy

## 🛠️ 快速开始

### 环境要求
- Python 3.7+
- Chrome浏览器 (用于Selenium)
- Windows/Linux/macOS

### 安装依赖
```bash
cd @cc-code
pip install -r requirements.txt
```

### 基础使用

#### 1. 功能测试（推荐首次使用）
```bash
# 使用演示数据测试分析功能
python ccc-main.py analyze data/demo_comments.json

# 检查系统合规状态
python ccc-main.py compliance

# 查看所有可用命令
python ccc-main.py --help
```

#### 2. 完整工作流程
```bash
# 餐厅评论爬取 + 分析 + 词云生成
python ccc-main.py pipeline "餐厅名称" --city 北京 --months 1

# 启动Web界面
python ccc-main.py web
```

#### 3. 词云生成
```bash
# 基础词云生成
python ccc-enhanced_wordcloud.py

# 简化版词云（快速生成）
python ccc-enhanced_wordcloud_simple.py

# 数据优化版词云
python ccc-data_optimized_wordcloud.py
```

## 📁 项目结构

```
@cc-code/
├── ccc-main.py                     # 合规版主程序
├── dianping_spider/main.py         # 基础版主程序
├── ccc-config.py                   # 合规配置
├── config.py                       # 基础配置
├── dianping_spider/
│   ├── spiders/
│   │   ├── dianping_spider.py      # 基础爬虫
│   │   └── ccc-compliance_spider.py # 合规爬虫
│   ├── utils/
│   │   ├── text_analyzer.py        # 完整文本分析
│   │   ├── text_analyzer_simple.py # 简化文本分析
│   │   ├── wordcloud_generator.py  # 词云生成
│   │   ├── data_utils.py           # 数据工具
│   │   └── ccc-compliance_checker.py # 合规检查
│   └── web/
│       ├── app.py                  # 基础Web应用
│       └── ccc-compliance_app.py   # 合规Web应用
├── USER_AGREEMENT.md               # 用户协议
├── RESEARCH_PURPOSE.md             # 研究目的声明
└── requirements.txt                # 依赖包列表
```

## 🔧 配置说明

### 合规模式 (推荐)
启用完整的法律合规和数据保护功能：
- 用户协议确认
- 自动数据匿名化
- 严格频率限制 (10次/分钟)
- 30天数据保留期

### 基础模式
用于开发和测试：
- 无合规检查
- 完整功能访问
- 适用于研发环境

## 📊 使用示例

### 分析餐厅评论
```python
from dianping_spider.utils.text_analyzer import TextAnalyzer

analyzer = TextAnalyzer()
results = analyzer.analyze_comments(comments_data)
print(f"情感得分: {results['sentiment_score']}")
print(f"关键词: {results['keywords']}")
```

### 生成词云
```python
from dianping_spider.utils.wordcloud_generator import WordCloudGenerator

generator = WordCloudGenerator()
generator.generate_wordcloud(
    text_data,
    output_path="wordcloud.png",
    color_scheme="blue"
)
```

## ⚖️ 法律声明与合规

本项目严格遵循相关法律法规：
- ✅ 仅用于学习、研究、学术目的
- ✅ 自动数据匿名化处理
- ✅ 严格的访问频率控制
- ✅ 定期数据清理机制
- ❌ 禁止商业用途
- ❌ 禁止恶意数据采集

## 🧪 测试

```bash
# 快速功能测试
python test_simple.py

# 完整系统测试
python test_system.py

# 生产环境测试
python production_test.py
```

## 📈 性能优化建议

1. **数据处理**: 大数据集分批处理，避免内存溢出
2. **爬虫设置**: 合理设置请求间隔，避免IP封禁
3. **文本分析**: 使用简化版分析器提高处理速度
4. **资源管理**: 定期清理日志和临时文件

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🆘 常见问题

### Q: 首次运行遇到错误怎么办？
A: 请先运行 `python ccc-main.py analyze data/demo_comments.json` 进行功能测试

### Q: 如何配置API密钥？
A: 复制 `api_keys_template.json` 为 `api_keys.json` 并填入相应密钥

### Q: 爬虫被反爬怎么办？
A: 建议使用合规模式，系统会自动控制访问频率和行为模式

### Q: 词云生成失败？
A: 请检查是否安装了中文字体，或使用简化版词云生成器

---

## 📞 支持与反馈

如果您在使用过程中遇到问题或有建议，请：
- 提交 [Issue](https://github.com/your-username/your-repo/issues)
- 发送邮件至: your-email@example.com
- 查看详细文档: [项目Wiki](https://github.com/your-username/your-repo/wiki)

---

**⚠️ 重要提醒**: 请严格遵守相关法律法规，仅将本项目用于合法的学习和研究目的。