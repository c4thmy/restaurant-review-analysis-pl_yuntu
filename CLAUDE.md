# CLAUDE.md

此文件为Claude Code (claude.ai/code)在处理此代码库时提供指导。

中文回答；将问答记录保存至@doc下；如果涉及代码修改，需保持原有工程文件不改变，将需要修改的代码文件复制到@cc-code下，在原代码文件名前增加ccc-前缀保存，然后将相关代码修改在@cc-code目录中对于文件中进行整合，同时将代码修改说明保存至@cc-doc下

## 项目概述

这是一个大众点评餐厅评论分析系统，包含两个版本：
- **基础版本** (`@cc-code/dianping_spider/`) - 原始功能实现
- **合规版本** (`@cc-code/ccc-*`) - 法律合规增强版，内置隐私保护和使用限制

核心功能包括：
1. 餐厅评论数据爬取
2. 中文文本分析和情感分析
3. 词云可视化生成
4. Web界面交互
5. 合规性检查和数据保护

## 常用命令

### 安装依赖
```bash
cd @cc-code
pip install -r requirements.txt
```

### 基础功能测试
```bash
# 测试分析功能（推荐首次使用）
python ccc-main.py analyze data/demo_comments.json

# 检查系统合规状态
python ccc-main.py compliance

# 查看命令帮助
python ccc-main.py --help
```

### 开发和调试
```bash
# 运行简单测试
python test_simple.py

# 运行系统测试
python test_system.py

# 生产环境测试
python production_test.py
```

### 完整工作流程
```bash
# 完整爬取+分析+词云流程
python ccc-main.py pipeline "餐厅名称" --city 北京 --months 1

# 启动Web界面
python ccc-main.py web

# 外部数据集成
python external_tool_processor.py
```

### 词云生成增强版本
```bash
# 基础词云生成
python ccc-enhanced_wordcloud.py

# 简化版词云
python ccc-enhanced_wordcloud_simple.py

# 数据优化版词云
python ccc-data_optimized_wordcloud.py
```

## 代码架构

### 核心设计模式

**双版本架构**:
- 基础版本 (`dianping_spider/main.py`) 提供完整功能
- 合规版本 (`ccc-main.py`) 增加法律合规检查和数据保护

**模块化组件**:
- `spiders/` - 爬虫模块，支持基础版和合规版
- `utils/` - 工具模块，包含文本分析、词云生成、数据管理
- `web/` - Web界面，Flask应用
- `config.py` vs `ccc-config.py` - 配置管理双版本

### 关键架构组件

#### 1. 爬虫系统
- **DianpingSpider** (`dianping_spider.py`): 基础爬虫，使用Selenium + BeautifulSoup
- **ComplianceSpider** (`ccc-compliance_spider.py`): 合规爬虫，内置频率限制和隐私保护
- **反爬策略**: User-Agent轮换、随机延迟、请求重试机制

#### 2. 文本分析引擎
- **CommentAnalyzer** (`text_analyzer_simple.py`): 简化版分析器，不依赖外部NLP库
- **TextAnalyzer** (`text_analyzer.py`): 完整版分析器，使用jieba、scikit-learn、SnowNLP
- **功能**: 中文分词、关键词提取、情感分析、标签生成

#### 3. 合规性框架
- **ComplianceChecker** (`ccc-compliance_checker.py`): 自动合规检查
- **DataProtection**: 用户信息匿名化、敏感信息过滤、时间泛化
- **AccessControl**: 频率限制、数据量限制、使用目的验证

#### 4. 可视化系统
- **WordCloudGenerator** (`wordcloud_generator.py`): 中文词云生成
- **支持**: 多种颜色方案、分类词云、字体自动检测
- **增强版本**: 提供多个优化版本满足不同需求

### 数据流架构

```
输入 → 爬虫模块 → 合规检查 → 数据清洗 → 文本分析 → 词云生成 → 结果输出
     ↓          ↓          ↓          ↓          ↓
   配置验证  → 频率控制 → 隐私保护 → 关键词提取 → 可视化 → Web展示/文件保存
```

### 配置管理体系

**合规配置** (`ccc-config.py`):
- `COMPLIANCE_CONFIG`: 使用限制、频率控制、数据保护
- `RATE_LIMITS`: 详细的访问频率限制
- `DATA_PROTECTION`: 隐私保护参数
- `LEGAL_CONFIG`: 法律合规设置

**功能配置** (`config.py`):
- `SPIDER_CONFIG`: 爬虫基础配置
- `ANALYSIS_CONFIG`: 文本分析参数
- `WORDCLOUD_CONFIG`: 词云生成设置
- `WEB_CONFIG`: Web服务配置

### 多模式运行机制

1. **合规模式** (COMPLIANCE_MODE=True):
   - 启动时显示法律声明
   - 要求用户协议确认
   - 自动数据保护处理
   - 严格频率和数量限制

2. **基础模式** (COMPLIANCE_M
ODE=False):
   - 回退到基础功能
   - 无合规检查
   - 适用于研发和测试

### 文件组织结构

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

## 开发注意事项

### 合规性要求
- 所有数据爬取必须通过合规检查
- 用户信息自动匿名化处理
- 严格遵守频率限制 (最多10次/分钟)
- 数据保留期限30天，需定期清理
- 仅允许学习、研究、学术用途

### 测试和调试
- 优先使用演示数据 (`data/demo_comments.json`) 进行功能测试
- 合规版本需要用户协议确认才能执行爬取
- 使用 `test_simple.py` 进行快速功能验证
- 生产测试使用 `production_test.py`

### 数据处理管道
1. **数据获取**: 爬虫 → JSON格式存储
2. **分析处理**: 加载数据 → 文本分析 → 结果保存
3. **可视化**: 词云生成 → 图片输出
4. **Web展示**: Flask服务 → 交互界面

### 错误处理策略
- 网络请求失败: 自动重试机制
- 数据解析错误: 日志记录 + 继续处理
- 合规检查失败: 立即停止操作
- 资源清理: 确保WebDriver和文件句柄正确关闭

### 性能优化建议
- 使用简化版文本分析器以提高处理速度
- 合理设置爬取间隔避免被封IP
- 定期清理日志和临时文件
- 监控内存使用，大数据集分批处理