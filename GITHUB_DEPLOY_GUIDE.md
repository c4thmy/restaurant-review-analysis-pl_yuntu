# GitHub 发布步骤指南

## 🚀 快速发布到GitHub

### 方法一：使用自动化脚本 (推荐)

1. **在GitHub上创建新仓库**：
   - 访问 https://github.com/new
   - Repository name: `restaurant-review-analysis` (或您喜欢的名称)
   - Description: `大众点评餐厅评论分析系统 - 智能爬虫、文本分析、词云生成`
   - 选择 Public 或 Private
   - ❌ **不要勾选** "Initialize this repository with a README"
   - 点击 "Create repository"

2. **配置发布脚本**：

   **Windows用户**:
   - 编辑 `github_deploy.bat` 文件
   - 修改这两行：
     ```batch
     set USER_NAME=your-github-username  # 改为您的GitHub用户名
     set REPO_NAME=restaurant-review-analysis  # 改为您的仓库名
     ```
   - 双击运行 `github_deploy.bat`

   **Linux/Mac用户**:
   - 编辑 `github_deploy.sh` 文件
   - 修改这两行：
     ```bash
     USER_NAME="your-github-username"  # 改为您的GitHub用户名
     REPO_NAME="restaurant-review-analysis"  # 改为您的仓库名
     ```
   - 运行：`bash github_deploy.sh`

### 方法二：手动执行命令

如果您偏好手动操作，请按顺序执行以下命令：

```bash
# 1. 添加远程仓库 (请替换YOUR_USERNAME和YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 2. 验证远程仓库设置
git remote -v

# 3. 推送代码到GitHub
git push -u origin master
```

## 📋 发布清单

在发布前，请确认：

- ✅ 项目代码已提交到本地Git仓库
- ✅ **运行安全检查**: `python security_check_simple.py`
- ✅ 确认无敏感信息泄露
- ✅ 在GitHub上创建了新的空仓库
- ✅ 获得了正确的仓库URL
- ✅ 有推送权限到该仓库
- ✅ 网络连接正常

### 🔒 重要：发布前安全检查

**必须运行安全检查脚本**：
```bash
python security_check_simple.py
```

如果发现任何敏感信息，请先修复后再发布。

## 🔧 故障排除

### 常见错误及解决方案：

1. **`remote origin already exists`**
   ```bash
   git remote remove origin
   git remote add origin https://github.com/USERNAME/REPO.git
   ```

2. **权限拒绝错误**
   - 检查GitHub用户名和仓库名是否正确
   - 确认您有该仓库的推送权限
   - 如果使用SSH，检查SSH密钥配置

3. **网络连接超时**
   - 检查网络连接
   - 尝试使用VPN或更换网络环境
   - 使用GitHub Desktop作为替代方案

4. **仓库不为空**
   - 确认GitHub仓库创建时没有初始化README
   - 或者先pull远程内容：`git pull origin master --allow-unrelated-histories`

## 🎯 发布后的操作

成功发布后，建议进行以下操作：

### 1. 完善仓库信息
- 添加详细的项目描述
- 设置仓库话题 (Topics)
- 配置仓库设置

### 2. 项目管理
- 创建Issues模板
- 设置Pull Request模板
- 配置GitHub Actions (如需要)

### 3. 文档完善
- 更新README.md中的安装和使用说明
- 添加贡献指南 (CONTRIBUTING.md)
- 创建Wiki页面

### 4. 版本管理
- 创建第一个Release版本
- 设置版本标签
- 编写更新日志

## 📞 获取帮助

如果遇到问题，可以：
- 查看GitHub官方文档
- 检查Git配置：`git config --list`
- 联系项目维护者

---

**祝您发布顺利！🎉**