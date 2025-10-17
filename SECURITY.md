# 🔒 数据安全和隐私保护指南

## ⚠️ 重要声明

为保护用户隐私和数据安全，本项目已采取以下措施：

### 🚫 已移除的敏感数据

1. **真实API密钥**: 所有真实的API密钥已被清理，仅保留模板文件
2. **个人手机号码**: 数据文件中的真实手机号码已被排除在Git跟踪之外
3. **敏感配置文件**: API密钥验证器等包含敏感信息的文件已移除

### 📁 .gitignore 保护规则

```gitignore
# 数据文件 - 排除所有实际数据
*.json
!*_template.json
!*_example.json
!package.json
!package-lock.json
!requirements.json
data/
*analysis*.json
*restaurant*.json
*comment*.json

# API密钥和敏感信息
api_keys.json
api_key.json
*_key.json
*_keys.json
*secret*.json
*config*.json
.env*
!.env.example
```

## 🛡️ 使用前安全检查

在使用本项目前，请运行安全检查：

```bash
# 运行安全检查脚本
python security_check_simple.py
```

## 📋 最佳实践

### 1. API密钥管理
- ✅ 使用环境变量存储真实API密钥
- ✅ 从模板文件复制并重命名为 `api_keys.json`
- ✅ 确保 `api_keys.json` 不被提交到版本控制
- ❌ 不要在代码中硬编码真实密钥

### 2. 数据处理
- ✅ 仅处理公开的餐厅信息
- ✅ 自动匿名化用户相关数据
- ✅ 定期清理敏感数据文件
- ❌ 不要存储或分享个人隐私信息

### 3. 发布到公开仓库
- ✅ 运行安全检查脚本
- ✅ 确认 .gitignore 规则正确
- ✅ 检查文档中无真实密钥示例
- ❌ 不要提交包含真实数据的文件

## 🔧 配置安全的开发环境

### 1. 创建环境变量文件
```bash
# 创建 .env 文件 (不会被Git跟踪)
cp .env.example .env
# 在 .env 中填入真实API密钥
```

### 2. 使用安全的配置方法
```python
import os
from dotenv import load_dotenv

load_dotenv()

api_keys = {
    "amap": os.getenv("AMAP_API_KEY"),
    "baidu": os.getenv("BAIDU_API_KEY"),
    "tencent": os.getenv("TENCENT_API_KEY")
}
```

### 3. 验证安全配置
```bash
# 检查环境变量是否正确设置
python -c "import os; print('AMAP_API_KEY' in os.environ)"
```

## 📞 报告安全问题

如果您发现任何安全问题或敏感数据泄露，请：

1. **不要**在公开的Issues中报告安全问题
2. 发送邮件至：security@your-domain.com (替换为您的邮箱)
3. 提供详细的问题描述和位置
4. 我们将在24小时内回复并处理

## 🏛️ 法律合规

本项目严格遵守数据保护法规：

- 仅用于学习、研究和学术目的
- 不收集、存储或处理个人隐私信息
- 遵循robots.txt和网站服务条款
- 实施适当的技术和组织措施保护数据

---

**最后更新**: 2025年10月17日
**版本**: 1.0