#!/usr/bin/env python3
"""
TokenData 免费监控程序
专注于小时级别的市场监控
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

class FreeMarketMonitor:
    """免费市场监控器"""
    
    def __init__(self):
        self.aggregator = FreeDataAggregator()
    
    def print_hourly_market_data(self, limit: int = 20):
        """打印小时级市场数据"""
        print("\n" + "="*100)
        print("📊 小时级市场数据监控")
        print("="*100)
        print(f"⏰ 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 100)
        
        # 获取市场数据
        df = self.aggregator.get_hourly_market_data(limit)
        
        if df.empty:
            print("❌ 无法获取市场数据")
            return
        
        # 显示表头
        print(f"{'排名':<4} {'代币':<15} {'价格':<12} {'1h变化':<8} {'24h变化':<8} {'7d变化':<8} {'成交量':<15} {'市值':<15}")
        print("-" * 100)
        
        # 显示数据
        for _, row in df.head(limit).iterrows():
            # 格式化价格变化
            change_1h = row.get('change_1h', 0)
            change_24h = row.get('change_24h', 0)
            change_7d = row.get('change_7d', 0)
            
            # 选择变化指标（优先显示1小时变化）
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
            
            print(f"{row['rank']:<4} {row['name']:<15} ${row['price']:<11,.2f} "
                  f"{change_icon} {display_change:<6.2f}% "
                  f"{change_24h:<6.2f}% {change_7d:<6.2f}% "
                  f"${row['volume_24h']:<14,.0f} ${row['market_cap']:<14,.0f}")
    
    def print_exchange_distribution(self):
        """打印交易所分布"""
        print("\n" + "="*80)
        print("🏢 主要交易所交易量分布")
        print("="*80)
        
        distribution = self.aggregator.get_exchange_volume_distribution()
        
        if not distribution:
            print("❌ 无法获取交易所数据")
            return
        
        print(f"{'交易所':<15} {'信任度':<8} {'24h成交量(BTC)':<15} {'成立年份':<8} {'国家':<10}")
        print("-" * 80)
        
        for exchange_id, data in list(distribution.items())[:10]:
            volume_btc = data.get('trade_volume_24h_btc', 0)
            trust_score = data.get('trust_score', 'N/A')
            year = data.get('year_established', 'N/A')
            country = data.get('country', 'N/A')
            
            print(f"{data['name']:<15} {trust_score:<8} {volume_btc:<15,.0f} {year:<8} {country:<10}")
    
    def print_trending_coins(self):
        """打印趋势代币"""
        print("\n" + "="*60)
        print("🔥 趋势代币 (可能反映资金流向)")
        print("="*60)
        
        trending = self.aggregator.get_trending_coins()
        
        if not trending:
            print("❌ 无法获取趋势代币数据")
            return
        
        print(f"{'排名':<4} {'代币':<15} {'符号':<8} {'市值排名':<8} {'热度':<8}")
        print("-" * 60)
        
        for i, coin in enumerate(trending[:10], 1):
            rank = coin.get('market_cap_rank', 'N/A')
            score = coin.get('score', 0)
            
            print(f"{i:<4} {coin['name']:<15} {coin['symbol'].upper():<8} #{rank:<7} {score:<8.2f}")
    
    def print_global_summary(self):
        """打印全球市场概况"""
        print("\n" + "="*80)
        print("🌍 全球市场概况")
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
    
    def print_hourly_changes(self, limit: int = 10):
        """打印小时级价格变化"""
        print("\n" + "="*80)
        print("⏰ 小时级价格变化监控")
        print("="*80)
        
        changes_df = self.aggregator.get_hourly_price_changes()
        
        if changes_df.empty:
            print("❌ 无法获取小时价格变化数据")
            return
        
        # 按变化幅度排序
        changes_df = changes_df.sort_values('hour_change_percent', ascending=False)
        
        print(f"{'代币':<15} {'当前价格':<12} {'1小时前':<12} {'变化':<8} {'变化%':<8}")
        print("-" * 80)
        
        for _, row in changes_df.head(limit).iterrows():
            change = row['current_price'] - row['hour_ago_price']
            change_percent = row['hour_change_percent']
            
            if change_percent > 0:
                change_icon = "🟢"
            elif change_percent < 0:
                change_icon = "🔴"
            else:
                change_icon = "⚪"
            
            print(f"{row['coin_id']:<15} ${row['current_price']:<11,.2f} "
                  f"${row['hour_ago_price']:<11,.2f} {change_icon} {change_percent:<6.2f}%")
    
    def print_volume_analysis(self, limit: int = 10):
        """打印交易量分析"""
        print("\n" + "="*80)
        print("📊 交易量分析")
        print("="*80)
        
        volume_df = self.aggregator.get_volume_analysis()
        
        if volume_df.empty:
            print("❌ 无法获取交易量分析数据")
            return
        
        # 按当前交易量排序
        volume_df = volume_df.sort_values('current_volume', ascending=False)
        
        print(f"{'代币':<15} {'当前成交量':<15} {'7日平均':<15} {'变化%':<8} {'趋势':<8}")
        print("-" * 80)
        
        for _, row in volume_df.head(limit).iterrows():
            change = row['volume_change_24h']
            trend = row['volume_trend']
            
            if change > 0:
                change_icon = "🟢"
            elif change < 0:
                change_icon = "🔴"
            else:
                change_icon = "⚪"
            
            trend_icon = "📈" if trend == "increasing" else "📉"
            
            print(f"{row['coin_id']:<15} ${row['current_volume']:<14,.0f} "
                  f"${row['avg_volume_7d']:<14,.0f} {change_icon} {change:<6.2f}% {trend_icon}")
    
    def run_full_monitor(self, limit: int = 20):
        """运行完整监控"""
        print("🚀 TokenData 免费市场监控器")
        print("="*100)
        
        try:
            # 全球市场概况
            self.print_global_summary()
            
            # 小时级市场数据
            self.print_hourly_market_data(limit)
            
            # 小时级价格变化
            self.print_hourly_changes(10)
            
            # 交易量分析
            self.print_volume_analysis(10)
            
            # 趋势代币
            self.print_trending_coins()
            
            # 交易所分布
            self.print_exchange_distribution()
            
            print("\n" + "="*100)
            print("✅ 监控完成！")
            print("="*100)
            
        except Exception as e:
            logger.error(f"监控过程中出现错误: {e}")
            print(f"❌ 监控失败: {e}")
    
    def run_continuous_monitor(self, interval: int = 3600, limit: int = 20):
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
    parser = argparse.ArgumentParser(description='TokenData 免费市场监控器')
    parser.add_argument('--market', action='store_true', help='显示市场数据')
    parser.add_argument('--trending', action='store_true', help='显示趋势代币')
    parser.add_argument('--exchanges', action='store_true', help='显示交易所分布')
    parser.add_argument('--global', action='store_true', help='显示全球概况')
    parser.add_argument('--hourly', action='store_true', help='显示小时变化')
    parser.add_argument('--volume', action='store_true', help='显示交易量分析')
    parser.add_argument('--continuous', action='store_true', help='持续监控模式')
    parser.add_argument('--interval', type=int, default=3600, help='监控间隔(秒)')
    parser.add_argument('--limit', type=int, default=20, help='显示代币数量')
    
    args = parser.parse_args()
    
    monitor = FreeMarketMonitor()
    
    try:
        if args.continuous:
            monitor.run_continuous_monitor(args.interval, args.limit)
        elif args.market:
            monitor.print_hourly_market_data(args.limit)
        elif args.trending:
            monitor.print_trending_coins()
        elif args.exchanges:
            monitor.print_exchange_distribution()
        elif args.global:
            monitor.print_global_summary()
        elif args.hourly:
            monitor.print_hourly_changes(args.limit)
        elif args.volume:
            monitor.print_volume_analysis(args.limit)
        else:
            # 默认运行完整监控
            monitor.run_full_monitor(args.limit)
            
    except Exception as e:
        logger.error(f"执行过程中出现错误: {e}")
        print(f"❌ 执行失败: {e}")

if __name__ == "__main__":
    main()
