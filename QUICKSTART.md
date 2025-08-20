# TokenData 快速开始指南

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置API密钥（可选）
复制 `config.env.example` 为 `.env` 并填入你的API密钥：
```bash
cp config.env.example .env
```

**免费API密钥获取：**
- **CoinGecko**: https://www.coingecko.com/en/api/pricing
- **Binance**: https://www.binance.com/en/my/settings/api-management

### 3. 运行演示
```bash
python main.py
```

### 4. 测试功能
```bash
python test_basic.py
```

## 📊 功能演示

### 查看市场数据
```bash
python main.py --market --limit 20
```

### 查看市场概况
```bash
python main.py --summary
```

### 分析特定代币
```bash
python main.py --token bitcoin
```

### 查看交易量分析
```bash
python main.py --volume
```

## 🔧 高级功能

### 获取资金流向数据
如果你有Glassnode API密钥，可以获取更详细的链上数据：

```python
from src.data_sources.glassnode import GlassnodeAPI

api = GlassnodeAPI('your_api_key')
flows = api.get_exchange_flows('BTC')
print(flows)
```

### 自定义分析
```python
from src.analysis.market_analyzer import MarketAnalyzer

analyzer = MarketAnalyzer()
correlation = analyzer.get_price_correlation(['BTC/USDT', 'ETH/USDT'], days=30)
print(correlation)
```

## 📈 数据源说明

### 免费数据源
- **CoinGecko**: 基础价格、市值、交易量数据
- **Binance**: 实时交易数据、订单簿、K线数据

### 付费数据源
- **Glassnode**: 链上数据分析、资金流向、市场情绪
- **Santiment**: 社交情绪分析
- **Kaiko**: 多交易所聚合数据

## 🎯 使用场景

1. **市场监控**: 实时跟踪主流代币价格和交易量
2. **投资分析**: 分析代币基本面和技术指标
3. **资金流向**: 监控交易所资金流入流出
4. **情绪分析**: 了解市场情绪和趋势
5. **风险管理**: 通过相关性分析分散投资

## 🔍 数据指标说明

### 基础指标
- **价格**: 当前市场价格
- **市值**: 总市值排名
- **交易量**: 24小时交易量
- **涨跌幅**: 24小时、7天、30天涨跌幅

### 高级指标
- **NVT比率**: 网络价值与交易比率
- **MVRV比率**: 市值与已实现价值比率
- **恐惧贪婪指数**: 市场情绪指标
- **活跃地址数**: 网络活跃度指标

## 🛠️ 故障排除

### 常见问题

1. **API限制**: 免费API有请求频率限制，建议添加延时
2. **网络问题**: 确保网络连接正常
3. **数据延迟**: 某些数据可能有几分钟延迟

### 调试模式
```bash
python main.py --demo
```

## 📚 扩展开发

### 添加新数据源
1. 在 `src/data_sources/` 创建新的API客户端
2. 在 `MarketAnalyzer` 中集成新数据源
3. 更新主程序以支持新功能

### 自定义分析
1. 在 `src/analysis/` 添加新的分析模块
2. 实现自定义指标和算法
3. 集成到主程序中

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

MIT License
