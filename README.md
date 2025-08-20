# TokenData - 加密货币市场数据分析工具

## 项目简介
TokenData 是一个专注于**免费数据源**的加密货币市场监控工具，提供小时级别的市场数据分析，包括：
- 🚀 **主流代币监控**：市值前50的代币价格、涨跌幅、交易量
- ⏰ **小时级数据**：1小时、24小时、7天价格变化
- 💰 **资金流向分析**：基于价格和交易量的资金流入流出分析
- 📊 **交易量分析**：各代币交易量趋势和变化（智能格式化显示）
- 🔥 **趋势监控**：热门代币和资金流向趋势
- 🏢 **交易所分布**：主要交易所交易量分布

## 🎯 免费方案优势
- ✅ **完全免费**：基于CoinGecko等免费API
- ⚡ **实时更新**：小时级别的数据更新
- 📈 **全面覆盖**：50+主流代币监控
- 🔄 **持续监控**：支持定时自动更新
- 🛠️ **易于扩展**：模块化设计，便于添加新功能

## 功能特性
- 🚀 实时价格和涨跌幅数据
- 📊 多交易所交易量聚合（智能格式化：B/M/K）
- 💰 资金流向分析（流入/流出金额显示）
- 📈 趋势代币监控
- 🔄 自动化数据更新
- ⏰ 小时级价格变化监控
- 📋 详细的数据来源和计算方法说明

## 安装和使用

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
创建 `.env` 文件并添加API密钥：
```
COINGECKO_API_KEY=your_api_key_here
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key
```

### 3. 运行主流代币监控器（推荐）
```bash
# 完整监控（默认显示前20个代币）
python token_monitor.py

# 查看前30个代币
python token_monitor.py --limit 30

# 查看涨幅榜
python token_monitor.py --gainers --limit 15

# 查看跌幅榜
python token_monitor.py --losers --limit 15

# 查询特定代币
python token_monitor.py --token bitcoin

# 持续监控（每5分钟更新）
python token_monitor.py --continuous --interval 300
```

### 4. 运行完整监控器
```bash
# 完整监控（包含更多功能）
python free_monitor.py

# 只显示市场数据
python free_monitor.py --market --limit 20

# 显示趋势代币
python free_monitor.py --trending

# 持续监控模式（每小时更新）
python free_monitor.py --continuous --interval 3600
```

### 5. 启动Web应用
```bash
# 启动Web界面（推荐）
python web_app.py

# 或使用启动脚本
python start_web.py
```
然后在浏览器中访问：**http://127.0.0.1:8050**

### 6. 测试功能
```bash
python test_basic.py
```

## 项目结构
```
tokendata/
├── src/
│   ├── data_sources/     # 数据源模块
│   ├── analysis/         # 数据分析模块
│   ├── visualization/    # 数据可视化
│   └── utils/           # 工具函数
├── data/                # 数据存储
├── config/              # 配置文件
└── tests/               # 测试文件
```

## 支持的代币
- Bitcoin (BTC)
- Ethereum (ETH)
- Binance Coin (BNB)
- Cardano (ADA)
- Solana (SOL)
- 以及其他主流代币

## 📚 相关文档

- **[Web应用使用指南](WEB_APP_GUIDE.md)** - Web界面详细使用说明
- **[资金流向分析指南](FLOW_ANALYSIS_GUIDE.md)** - 资金流向分析原理和方法
- **[数据来源说明](DATA_SOURCE_GUIDE.md)** - 详细的数据来源和计算方法

## 许可证
MIT License