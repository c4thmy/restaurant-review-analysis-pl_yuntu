@echo off
REM GitHub 发布脚本 (Windows版本)
REM 使用方法:
REM 1. 在GitHub上创建新仓库
REM 2. 修改下面的USER_NAME和REPO_NAME变量
REM 3. 运行此脚本

REM ===== 配置区域 =====
set USER_NAME=your-github-username
set REPO_NAME=restaurant-review-analysis

REM ===== 脚本主体 =====
echo ========================================
echo GitHub 仓库发布脚本
echo ========================================

REM 检查Git状态
echo 检查Git状态...
git status

echo.
echo 当前配置:
echo GitHub用户名: %USER_NAME%
echo 仓库名称: %REPO_NAME%
echo 远程地址: https://github.com/%USER_NAME%/%REPO_NAME%.git

echo.
pause

REM 添加远程仓库
echo.
echo 添加远程仓库...
git remote add origin https://github.com/%USER_NAME%/%REPO_NAME%.git

REM 验证远程仓库
echo 验证远程仓库设置...
git remote -v

REM 推送到GitHub
echo.
echo 推送代码到GitHub...
git push -u origin master

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo 🎉 发布成功!
    echo ========================================
    echo 仓库地址: https://github.com/%USER_NAME%/%REPO_NAME%
    echo 请访问上述地址查看您的项目
    echo.
    echo 后续操作：
    echo - 可以编辑README.md添加项目描述
    echo - 在Settings中配置项目设置
    echo - 考虑添加Issues和Wiki页面
    echo ========================================
) else (
    echo.
    echo ❌ 推送失败，请检查：
    echo 1. GitHub仓库是否已创建
    echo 2. 用户名和仓库名是否正确
    echo 3. 是否有推送权限
    echo 4. 网络连接是否正常
)

pause