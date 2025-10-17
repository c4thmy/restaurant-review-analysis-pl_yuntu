#!/bin/bash
# 大众点评评论分析系统 - 快速开始脚本

echo "=========================================="
echo "   大众点评餐厅评论分析系统"
echo "   Python爬虫 + AI分析 + 词云可视化"
echo "=========================================="

# 检查Python版本
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✓ Python环境检查: $python_version"
else
    echo "✗ 错误: 未找到Python3环境"
    echo "请安装Python 3.8或更高版本"
    exit 1
fi

# 检查Chrome浏览器
if command -v google-chrome &> /dev/null || command -v chromium-browser &> /dev/null; then
    echo "✓ Chrome浏览器检查: 已安装"
else
    echo "! 警告: 未检测到Chrome浏览器"
    echo "请安装Chrome浏览器以确保爬虫正常工作"
fi

# 创建虚拟环境
echo ""
echo "正在创建Python虚拟环境..."
python3 -m venv spider_env

# 激活虚拟环境
echo "激活虚拟环境..."
source spider_env/bin/activate

# 安装依赖
echo "安装Python依赖包..."
pip install --upgrade pip
pip install -r requirements.txt

# 创建必要目录
echo "创建项目目录..."
mkdir -p data backup static/images templates logs

echo ""
echo "=========================================="
echo "           安装完成！"
echo "=========================================="
echo ""
echo "使用方法："
echo ""
echo "1. 命令行模式:"
echo "   # 运行完整分析流程"
echo "   python main.py pipeline \"嫩牛家潮汕火锅\" --city 北京 --months 3"
echo ""
echo "   # 仅爬取评论"
echo "   python main.py crawl \"餐厅名称\" --city 城市 --months 时间范围"
echo ""
echo "   # 分析已有数据"
echo "   python main.py analyze data/comments_xxx.json"
echo ""
echo "   # 生成词云图"
echo "   python main.py wordcloud data/comments_xxx_analysis.json"
echo ""
echo "2. Web界面模式:"
echo "   python main.py web"
echo "   然后访问: http://localhost:5000"
echo ""
echo "3. 查看帮助:"
echo "   python main.py --help"
echo ""
echo "=========================================="
echo "注意事项："
echo "- 请遵守网站使用条款，合理使用爬虫"
echo "- 建议在网络状况良好时运行"
echo "- 首次运行会自动下载ChromeDriver"
echo "=========================================="