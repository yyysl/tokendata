# Cloudflare部署检查清单

## ✅ 部署前检查

### 1. 文件准备
- [ ] `app.py` - 主应用文件
- [ ] `requirements-cloudflare.txt` - 依赖文件
- [ ] `wrangler.toml` - Cloudflare配置文件
- [ ] `.gitignore` - Git忽略文件
- [ ] `deploy.sh` - 部署脚本

### 2. 代码检查
- [ ] 应用可以本地运行
- [ ] 数据获取功能正常
- [ ] 界面显示正确
- [ ] 错误处理完善

### 3. 依赖检查
- [ ] 所有依赖都在requirements-cloudflare.txt中
- [ ] 没有不必要的依赖
- [ ] 版本兼容性检查

## 🚀 部署步骤

### 方法一：GitHub部署（推荐）

#### 1. 推送代码到GitHub
```bash
git add .
git commit -m "准备部署到Cloudflare Pages"
git push origin main
```

#### 2. 登录Cloudflare Dashboard
1. 访问 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 登录账户

#### 3. 创建Pages项目
1. 选择 **Pages**
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

#### 5. 环境变量
```
PYTHON_VERSION: 3.9
```

#### 6. 部署
点击 **Save and Deploy**

### 方法二：CLI部署

#### 1. 安装Wrangler
```bash
npm install -g wrangler
```

#### 2. 登录
```bash
wrangler login
```

#### 3. 部署
```bash
./deploy.sh
```

## 🔍 部署后验证

### 1. 基本功能检查
- [ ] 页面可以正常加载
- [ ] 数据可以正常获取
- [ ] 界面显示正确
- [ ] 响应式设计正常

### 2. 功能测试
- [ ] 市场概况显示
- [ ] 代币表格显示
- [ ] 数据刷新功能
- [ ] 下拉选择功能

### 3. 性能检查
- [ ] 页面加载速度
- [ ] 数据更新速度
- [ ] 内存使用情况
- [ ] API调用频率

## 🐛 常见问题解决

### 构建失败
- 检查requirements-cloudflare.txt
- 查看构建日志
- 确认Python版本

### 应用无法访问
- 检查部署状态
- 查看错误日志
- 确认域名配置

### 数据加载失败
- 检查API限制
- 确认网络连接
- 查看浏览器控制台

## 📊 部署成功标志

### 1. 访问成功
- 可以通过 `https://tokendata.pages.dev` 访问
- 页面正常加载
- 没有JavaScript错误

### 2. 功能正常
- 市场数据正常显示
- 代币列表正常加载
- 自动更新功能正常

### 3. 性能良好
- 页面加载时间 < 3秒
- 数据更新延迟 < 5秒
- 响应式设计正常

## 🔄 更新部署

### 自动更新
- 推送代码到GitHub
- Cloudflare自动检测并部署
- 部署完成后自动更新

### 手动更新
```bash
./deploy.sh
```

## 📞 技术支持

如果遇到问题：
1. 查看Cloudflare Pages文档
2. 检查项目GitHub Issues
3. 查看部署日志
4. 联系技术支持

---

**部署完成后，你的TokenData应用就可以在全球范围内访问了！** 🌍
