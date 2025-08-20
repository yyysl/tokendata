#!/usr/bin/env python3
"""
主流代币变化监控器
专注于主流代币的价格变化监控
"""
import sys
import os
import time
import logging
from datetime import datetime, timedelta
import argparse

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_sources.free_data_aggregator import FreeDataAggregator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TokenMonitor:
    """主流代币监控器"""
    
    def __init__(self):
        self.aggregator = FreeDataAggregator()
        
        # 定义主流代币（市值前20）
        self.major_tokens = [
            'bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana',
            'ripple', 'polkadot', 'dogecoin', 'avalanche-2', 'polygon',
            'chainlink', 'uniswap', 'litecoin', 'cosmos', 'ethereum-classic',
            'stellar', 'monero', 'algorand', 'vechain', 'filecoin'
        ]
    
    def print_token_changes(self, limit: int = 20, show_volume: bool = True):
        """打印主流代币变化"""
        print("\n" + "="*120)
        print("📊 主流代币变化监控")
        print("="*120)
        print(f"⏰ 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 120)
        
        # 获取市场数据
        df = self.aggregator.get_hourly_market_data(limit)
        
        if df.empty:
            print("❌ 无法获取市场数据")
            return
        
        # 显示表头
        if show_volume:
            print(f"{'排名':<4} {'代币':<15} {'价格':<12} {'1h变化':<10} {'24h变化':<10} {'7d变化':<10} {'成交量':<15} {'市值':<15}")
            print("-" * 120)
        else:
            print(f"{'排名':<4} {'代币':<15} {'价格':<12} {'1h变化':<10} {'24h变化':<10} {'7d变化':<10}")
            print("-" * 80)
        
        # 显示数据
        for _, row in df.head(limit).iterrows():
            # 格式化价格变化
            change_1h = row.get('change_1h', 0)
            change_24h = row.get('change_24h', 0)
            change_7d = row.get('change_7d', 0)
            
            # 选择主要变化指标（优先显示1小时变化）
            display_change = change_1h if change_1h is not None else change_24h
            
            # 颜色指示器
            if display_change is not None:
                if display_change > 0:
                    change_icon = "🟢"
                elif display_change < 0:
                    change_icon = "🔴"
                else:
                    change_icon = "⚪"
            else:
                change_icon = "⚪"
                display_change = 0
            
            # 格式化输出
            if show_volume:
                print(f"{row['rank']:<4} {row['name']:<15} ${row['price']:<11,.2f} "
                      f"{change_icon} {display_change:<8.2f}% "
                      f"{change_24h:<8.2f}% {change_7d:<8.2f}% "
                      f"${row['volume_24h']:<14,.0f} ${row['market_cap']:<14,.0f}")
            else:
                print(f"{row['rank']:<4} {row['name']:<15} ${row['price']:<11,.2f} "
                      f"{change_icon} {display_change:<8.2f}% "
                      f"{change_24h:<8.2f}% {change_7d:<8.2f}%")
    
    def print_top_gainers(self, limit: int = 10):
        """打印涨幅最大的代币"""
        print("\n" + "="*80)
        print("🚀 涨幅榜 - 过去1小时")
        print("="*80)
        
        df = self.aggregator.get_hourly_market_data(50)  # 获取前50个代币
        
        if df.empty:
            print("❌ 无法获取数据")
            return
        
        # 按1小时涨幅排序
        df_sorted = df.sort_values('change_1h', ascending=False)
        
        print(f"{'排名':<4} {'代币':<15} {'价格':<12} {'1h涨幅':<10} {'24h涨幅':<10}")
        print("-" * 80)
        
        for i, (_, row) in enumerate(df_sorted.head(limit).iterrows(), 1):
            change_1h = row.get('change_1h', 0)
            change_24h = row.get('change_24h', 0)
            
            if change_1h and change_1h > 0:
                print(f"{i:<4} {row['name']:<15} ${row['price']:<11,.2f} "
                      f"🟢 +{change_1h:<7.2f}% +{change_24h:<7.2f}%")
    
    def print_top_losers(self, limit: int = 10):
        """打印跌幅最大的代币"""
        print("\n" + "="*80)
        print("📉 跌幅榜 - 过去1小时")
        print("="*80)
        
        df = self.aggregator.get_hourly_market_data(50)
        
        if df.empty:
            print("❌ 无法获取数据")
            return
        
        # 按1小时跌幅排序
        df_sorted = df.sort_values('change_1h', ascending=True)
        
        print(f"{'排名':<4} {'代币':<15} {'价格':<12} {'1h跌幅':<10} {'24h跌幅':<10}")
        print("-" * 80)
        
        for i, (_, row) in enumerate(df_sorted.head(limit).iterrows(), 1):
            change_1h = row.get('change_1h', 0)
            change_24h = row.get('change_24h', 0)
            
            if change_1h and change_1h < 0:
                print(f"{i:<4} {row['name']:<15} ${row['price']:<11,.2f} "
                      f"🔴 {change_1h:<7.2f}% {change_24h:<7.2f}%")
    
    def print_volume_leaders(self, limit: int = 10):
        """打印成交量最大的代币"""
        print("\n" + "="*80)
        print("📊 成交量榜 - 24小时")
        print("="*80)
        
        df = self.aggregator.get_hourly_market_data(50)
        
        if df.empty:
            print("❌ 无法获取数据")
            return
        
        # 按成交量排序
        df_sorted = df.sort_values('volume_24h', ascending=False)
        
        print(f"{'排名':<4} {'代币':<15} {'价格':<12} {'成交量':<15} {'市值':<15}")
        print("-" * 80)
        
        for i, (_, row) in enumerate(df_sorted.head(limit).iterrows(), 1):
            print(f"{i:<4} {row['name']:<15} ${row['price']:<11,.2f} "
                  f"${row['volume_24h']:<14,.0f} ${row['market_cap']:<14,.0f}")
    
    def print_market_summary(self):
        """打印市场概况"""
        print("\n" + "="*80)
        print("🌍 市场概况")
        print("="*80)
        
        global_data = self.aggregator.get_global_market_data()
        
        if not global_data:
            print("❌ 无法获取全球市场数据")
            return
        
        print(f"💰 总市值: ${global_data.get('total_market_cap', 0):,.0f}")
        print(f"📈 24小时成交量: ${global_data.get('total_volume', 0):,.0f}")
        print(f"🔄 24小时市值变化: {global_data.get('market_cap_change_percentage_24h_usd', 0):.2f}%")
        print(f"🪙 活跃加密货币: {global_data.get('active_cryptocurrencies', 0):,}")
        print(f"🏢 活跃交易所: {global_data.get('active_exchanges', 0):,}")
        print(f"₿ 比特币主导地位: {global_data.get('bitcoin_dominance', 0):.2f}%")
        print(f"Ξ 以太坊主导地位: {global_data.get('ethereum_dominance', 0):.2f}%")
    
    def print_specific_token(self, token_name: str):
        """打印特定代币的详细信息"""
        print(f"\n" + "="*80)
        print(f"🔍 {token_name.upper()} 详细信息")
        print("="*80)
        
        # 获取市场数据
        df = self.aggregator.get_hourly_market_data(100)  # 获取更多数据以找到目标代币
        
        if df.empty:
            print("❌ 无法获取数据")
            return
        
        # 查找目标代币
        token_data = None
        for _, row in df.iterrows():
            if (token_name.lower() in row['name'].lower() or 
                token_name.lower() in row['symbol'].lower() or
                token_name.lower() in row['coin_id'].lower()):
                token_data = row
                break
        
        if token_data is None:
            print(f"❌ 未找到代币: {token_name}")
            return
        
        # 显示详细信息
        change_1h = token_data.get('change_1h', 0)
        change_24h = token_data.get('change_24h', 0)
        change_7d = token_data.get('change_7d', 0)
        
        # 变化指示器
        def get_change_icon(change):
            if change is None:
                return "⚪"
            return "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
        
        print(f"📊 基本信息:")
        print(f"  名称: {token_data['name']}")
        print(f"  符号: {token_data['symbol'].upper()}")
        print(f"  排名: #{token_data['rank']}")
        print(f"  当前价格: ${token_data['price']:,.2f}")
        print(f"  市值: ${token_data['market_cap']:,.0f}")
        print(f"  24小时成交量: ${token_data['volume_24h']:,.0f}")
        
        print(f"\n📈 价格变化:")
        print(f"  1小时变化: {get_change_icon(change_1h)} {change_1h:+.2f}%")
        print(f"  24小时变化: {get_change_icon(change_24h)} {change_24h:+.2f}%")
        print(f"  7天变化: {get_change_icon(change_7d)} {change_7d:+.2f}%")
        
        print(f"\n📊 其他指标:")
        print(f"  流通供应量: {token_data.get('circulating_supply', 0):,.0f}")
        print(f"  总供应量: {token_data.get('total_supply', 0):,.0f}")
        print(f"  历史最高: ${token_data.get('ath', 0):,.2f}")
        print(f"  距离历史最高: {token_data.get('ath_change_percent', 0):.2f}%")
    
    def run_full_monitor(self, limit: int = 20):
        """运行完整监控"""
        print("🚀 主流代币变化监控器")
        print("="*120)
        
        try:
            # 市场概况
            self.print_market_summary()
            
            # 主流代币变化
            self.print_token_changes(limit)
            
            # 涨幅榜
            self.print_top_gainers(10)
            
            # 跌幅榜
            self.print_top_losers(10)
            
            # 成交量榜
            self.print_volume_leaders(10)
            
            print("\n" + "="*120)
            print("✅ 监控完成！")
            print("="*120)
            
        except Exception as e:
            logger.error(f"监控过程中出现错误: {e}")
            print(f"❌ 监控失败: {e}")
    
    def run_continuous_monitor(self, interval: int = 300, limit: int = 20):
        """运行持续监控"""
        print(f"🔄 启动持续监控 (间隔: {interval}秒)")
        
        while True:
            try:
                self.run_full_monitor(limit)
                print(f"\n⏰ 下次更新: {datetime.now() + timedelta(seconds=interval)}")
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n🛑 监控已停止")
                break
            except Exception as e:
                logger.error(f"持续监控错误: {e}")
                print(f"❌ 监控错误: {e}")
                time.sleep(60)  # 错误后等待1分钟再重试

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='主流代币变化监控器')
    parser.add_argument('--limit', type=int, default=20, help='显示代币数量')
    parser.add_argument('--gainers', action='store_true', help='显示涨幅榜')
    parser.add_argument('--losers', action='store_true', help='显示跌幅榜')
    parser.add_argument('--volume', action='store_true', help='显示成交量榜')
    parser.add_argument('--summary', action='store_true', help='显示市场概况')
    parser.add_argument('--token', type=str, help='显示特定代币信息')
    parser.add_argument('--continuous', action='store_true', help='持续监控模式')
    parser.add_argument('--interval', type=int, default=300, help='监控间隔(秒)')
    parser.add_argument('--simple', action='store_true', help='简化显示（不显示成交量）')
    
    args = parser.parse_args()
    
    monitor = TokenMonitor()
    
    try:
        if args.continuous:
            monitor.run_continuous_monitor(args.interval, args.limit)
        elif args.gainers:
            monitor.print_top_gainers(args.limit)
        elif args.losers:
            monitor.print_top_losers(args.limit)
        elif args.volume:
            monitor.print_volume_leaders(args.limit)
        elif args.summary:
            monitor.print_market_summary()
        elif args.token:
            monitor.print_specific_token(args.token)
        else:
            # 默认运行完整监控
            monitor.run_full_monitor(args.limit)
            
    except Exception as e:
        logger.error(f"执行过程中出现错误: {e}")
        print(f"❌ 执行失败: {e}")

if __name__ == "__main__":
    main()
