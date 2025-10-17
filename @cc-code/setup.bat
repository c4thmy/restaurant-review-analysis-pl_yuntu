@echo off
chcp 65001 >nul
echo ==========================================
echo    大众点评餐厅评论分析系统
echo    Python爬虫 + AI分析 + 词云可视化
echo ==========================================

:: 检查Python版本
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ 错误: 未找到Python环境
    echo 请安装Python 3.8或更高版本
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version') do echo ✓ Python环境检查: %%i
)

:: 检查Chrome浏览器
where chrome >nul 2>&1
if %errorlevel% neq 0 (
    echo ! 警告: 未检测到Chrome浏览器
    echo 请安装Chrome浏览器以确保爬虫正常工作
) else (
    echo ✓ Chrome浏览器检查: 已安装
)

:: 创建虚拟环境
echo.
echo 正在创建Python虚拟环境...
python -m venv spider_env

:: 激活虚拟环境
echo 激活虚拟环境...
call spider_env\Scripts\activate.bat

:: 安装依赖
echo 安装Python依赖包...
python -m pip install --upgrade pip
pip install -r requirements.txt

:: 创建必要目录
echo 创建项目目录...
if not exist data mkdir data
if not exist backup mkdir backup
if not exist static\images mkdir static\images
if not exist templates mkdir templates
if not exist logs mkdir logs

echo.
echo ==========================================
echo            安装完成！
echo ==========================================
echo.
echo 使用方法：
echo.
echo 1. 命令行模式:
echo    # 运行完整分析流程
echo    python main.py pipeline "嫩牛家潮汕火锅" --city 北京 --months 3
echo.
echo    # 仅爬取评论
echo    python main.py crawl "餐厅名称" --city 城市 --months 时间范围
echo.
echo    # 分析已有数据
echo    python main.py analyze data\comments_xxx.json
echo.
echo    # 生成词云图
echo    python main.py wordcloud data\comments_xxx_analysis.json
echo.
echo 2. Web界面模式:
echo    python main.py web
echo    然后访问: http://localhost:5000
echo.
echo 3. 查看帮助:
echo    python main.py --help
echo.
echo ==========================================
echo 注意事项：
echo - 请遵守网站使用条款，合理使用爬虫
echo - 建议在网络状况良好时运行
echo - 首次运行会自动下载ChromeDriver
echo ==========================================
pause