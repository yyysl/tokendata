# Cloudflare Pages 部署指南

## 🚀 部署到Cloudflare Pages

### 方法一：通过GitHub部署（推荐）

#### 1. 准备代码
确保你的代码已经推送到GitHub仓库，包含以下文件：
- `app.py` - 主应用文件
- `requirements-cloudflare.txt` - 依赖文件
- `wrangler.toml` - Cloudflare配置文件

#### 2. 登录Cloudflare Dashboard
1. 访问 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 登录你的账户

#### 3. 创建Pages项目
1. 在左侧菜单选择 **Pages**
2. 点击 **Create a project**
3. 选择 **Connect to Git**
4. 选择你的GitHub仓库

#### 4. 配置构建设置
```
Project name: tokendata
Production branch: main
Framework preset: None
Build command: pip install -r requirements-cloudflare.txt
Build output directory: .
Root directory: /
```

#### 5. 环境变量设置
在 **Environment variables** 中添加：
```
PYTHON_VERSION: 3.9
```

#### 6. 部署
点击 **Save and Deploy** 开始部署

### 方法二：通过Wrangler CLI部署

#### 1. 安装Wrangler CLI
```bash
npm install -g wrangler
```

#### 2. 登录Wrangler
```bash
wrangler login
```

#### 3. 部署项目
```bash
wrangler pages deploy .
```

## 📁 项目文件结构

```
tokendata/
├── app.py                    # 主应用文件
├── requirements-cloudflare.txt # Cloudflare依赖
├── wrangler.toml            # Cloudflare配置
├── src/                     # 源代码目录
│   ├── data_sources/        # 数据源模块
│   ├── analysis/           # 分析模块
│   └── utils/              # 工具模块
├── README.md               # 项目说明
└── CLOUDFLARE_DEPLOYMENT.md # 部署指南
```

## ⚙️ 配置说明

### wrangler.toml
```toml
name = "tokendata"
main = "app.py"
compatibility_date = "2024-01-01"

[env.production]
name = "tokendata-prod"

[env.staging]
name = "tokendata-staging"

[build]
command = "pip install -r requirements-cloudflare.txt"
```

### requirements-cloudflare.txt
```
dash==2.14.2
pandas==2.1.4
requests==2.31.0
plotly==5.17.0
```

## 🔧 部署后配置

### 1. 自定义域名（可选）
1. 在Pages项目设置中
2. 选择 **Custom domains**
3. 添加你的域名

### 2. 环境变量配置
如果需要，可以在项目设置中添加环境变量：
```
COINGECKO_API_KEY=your_api_key_here
```

### 3. 自动部署设置
- 每次推送到main分支会自动触发部署
- 可以在 **Deployments** 标签页查看部署历史

## 🌐 访问应用

部署成功后，你可以通过以下URL访问：
- **生产环境**: `https://tokendata.pages.dev`
- **预览环境**: `https://tokendata-staging.pages.dev`

## 📊 功能特性

### 已部署功能
- ✅ 主流代币实时监控
- ✅ 价格和涨跌幅显示
- ✅ 交易量数据（智能格式化）
- ✅ 市场概况
- ✅ 自动数据更新
- ✅ 响应式设计

### 数据来源
- **CoinGecko API**（免费版）
- **全网交易所数据聚合**
- **实时价格和交易量**

## 🔄 更新部署

### 自动更新
1. 推送代码到GitHub
2. Cloudflare自动检测并部署
3. 部署完成后自动更新

### 手动更新
```bash
# 重新部署
wrangler pages deploy .
```

## 🐛 故障排除

### 常见问题

#### 1. 构建失败
- 检查 `requirements-cloudflare.txt` 文件
- 确保所有依赖都正确列出
- 查看构建日志

#### 2. 应用无法访问
- 检查部署状态
- 查看错误日志
- 确认域名配置

#### 3. 数据加载失败
- 检查API限制
- 确认网络连接
- 查看浏览器控制台错误

### 调试方法
1. 查看Cloudflare Pages日志
2. 检查浏览器开发者工具
3. 测试API连接

## 📞 技术支持

如果遇到问题，可以：
1. 查看Cloudflare Pages文档
2. 检查项目GitHub Issues
3. 联系技术支持

---

**部署完成后，你的TokenData应用就可以在全球范围内访问了！** 🌍
