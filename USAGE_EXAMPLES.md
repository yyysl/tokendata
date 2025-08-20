# TokenData 使用示例

## 🚀 快速开始

### 1. 完整市场监控
```bash
python free_monitor.py
```
这将显示：
- 全球市场概况
- 市值前20的代币数据
- 小时级价格变化
- 交易量分析
- 趋势代币
- 交易所分布

### 2. 只查看市场数据
```bash
python free_monitor.py --market --limit 30
```
显示市值前30的代币价格、涨跌幅和交易量

### 3. 监控趋势代币
```bash
python free_monitor.py --trending
```
显示当前热门代币，可能反映资金流向

### 4. 查看交易所分布
```bash
python free_monitor.py --exchanges
```
显示主要交易所的交易量分布

### 5. 全球市场概况
```bash
python free_monitor.py --global
```
显示总市值、成交量、比特币主导地位等

## 🔄 持续监控

### 每小时更新
```bash
python free_monitor.py --continuous --interval 3600
```

### 每30分钟更新
```bash
python free_monitor.py --continuous --interval 1800
```

### 每15分钟更新（注意API限制）
```bash
python free_monitor.py --continuous --interval 900
```

## 📊 数据分析示例

### 查看小时级价格变化
```bash
python free_monitor.py --hourly --limit 15
```
显示过去1小时内价格变化最大的15个代币

### 查看交易量分析
```bash
python free_monitor.py --volume --limit 20
```
显示交易量最大的20个代币及其趋势

## 🎯 实际使用场景

### 场景1：日常市场监控
```bash
# 每天早上查看市场概况
python free_monitor.py --global

# 查看主要代币表现
python free_monitor.py --market --limit 10
```

### 场景2：趋势跟踪
```bash
# 查看趋势代币
python free_monitor.py --trending

# 查看小时级变化
python free_monitor.py --hourly --limit 10
```

### 场景3：交易量分析
```bash
# 查看交易量异常的代币
python free_monitor.py --volume --limit 15
```

### 场景4：持续监控
```bash
# 后台持续监控（每小时更新）
nohup python free_monitor.py --continuous --interval 3600 > monitor.log 2>&1 &
```

## 📈 数据解读

### 价格变化指标
- 🟢 绿色：价格上涨
- 🔴 红色：价格下跌
- ⚪ 白色：价格持平

### 交易量趋势
- 📈 上升趋势：当前交易量高于7日平均
- 📉 下降趋势：当前交易量低于7日平均

### 趋势代币
- 热度分数越高，表示越受关注
- 可能反映资金流向和投资热点

## ⚠️ 注意事项

### API限制
- CoinGecko免费API有请求频率限制
- 建议监控间隔不少于15分钟
- 避免过于频繁的请求

### 数据延迟
- 免费API数据可能有几分钟延迟
- 价格数据仅供参考，交易时请以交易所为准

### 网络问题
- 确保网络连接稳定
- 如遇到API错误，程序会自动重试

## 🔧 自定义配置

### 修改监控代币数量
```bash
python free_monitor.py --market --limit 50  # 显示前50个代币
```

### 修改监控间隔
```bash
python free_monitor.py --continuous --interval 7200  # 每2小时更新
```

### 组合使用
```bash
# 显示前30个代币的市场数据，并持续监控
python free_monitor.py --market --limit 30 --continuous --interval 3600
```

## 📱 输出示例

### 市场数据输出
```
📊 小时级市场数据监控
====================================================================================================
⏰ 更新时间: 2024-01-15 14:30:00
----------------------------------------------------------------------------------------------------
排名 代币            价格         1h变化   24h变化   7d变化   成交量          市值
----------------------------------------------------------------------------------------------------
1    Bitcoin        $42,350.00   🟢 +2.15%  +5.20%  +12.30% $28,450,000,000 $830,000,000,000
2    Ethereum       $2,580.00    🟢 +1.85%  +3.45%  +8.90%  $15,230,000,000 $310,000,000,000
3    Binance Coin   $315.00      🔴 -0.50%  +2.10%  +6.70%  $2,100,000,000  $48,000,000,000
```

### 趋势代币输出
```
🔥 趋势代币 (可能反映资金流向)
============================================================
排名 代币            符号     市值排名  热度
------------------------------------------------------------
1    Bitcoin        BTC     #1       95.67
2    Ethereum       ETH     #2       87.23
3    Solana         SOL     #5       82.45
```

## 🚀 进阶用法

### 结合其他工具
```bash
# 将输出保存到文件
python free_monitor.py --market --limit 20 > market_data.txt

# 定时执行并发送通知
python free_monitor.py --market --limit 10 | mail -s "Market Update" your@email.com
```

### 数据分析
```bash
# 查看特定时间段的变化
python free_monitor.py --hourly --limit 50 | grep "Bitcoin"
```

这个免费方案为你提供了完整的市场监控能力，无需任何付费API即可开始使用！
