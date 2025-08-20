#!/usr/bin/env python3
"""
TokenData - 加密货币市场数据分析工具
主应用程序入口
"""
import os
import sys
import logging
import argparse
from datetime import datetime
from dotenv import load_dotenv

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.analysis.market_analyzer import MarketAnalyzer
from src.data_sources.coingecko import CoinGeckoAPI
from src.data_sources.binance import BinanceAPI

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """设置环境变量"""
    # 从环境变量获取API密钥
    coingecko_api_key = os.getenv('COINGECKO_API_KEY')
    binance_api_key = os.getenv('BINANCE_API_KEY')
    binance_secret_key = os.getenv('BINANCE_SECRET_KEY')
    glassnode_api_key = os.getenv('GLASSNODE_API_KEY')
    
    return {
        'coingecko_api_key': coingecko_api_key,
        'binance_api_key': binance_api_key,
        'binance_secret_key': binance_secret_key,
        'glassnode_api_key': glassnode_api_key
    }

def print_market_data(analyzer: MarketAnalyzer, limit: int = 20):
    """打印市场数据"""
    print("\n" + "="*80)
    print("📊 加密货币市场数据")
    print("="*80)
    
    # 获取综合市场数据
    df = analyzer.get_comprehensive_market_data(limit)
    
    if df.empty:
        print("❌ 无法获取市场数据")
        return
    
    # 显示主要代币数据
    print(f"\n🏆 市值排名前{limit}的代币:")
    print("-" * 80)
    
    for _, row in df.head(10).iterrows():
        change_24h = row['change_24h']
        change_color = "🟢" if change_24h > 0 else "🔴" if change_24h < 0 else "⚪"
        
        print(f"{row['rank']:2d}. {row['name']:<15} ({row['symbol']:<5}) "
              f"${row['price']:>10,.2f} {change_color} {change_24h:>6.2f}% "
              f"成交量: ${row['volume_24h']:>12,.0f}")

def print_market_summary(analyzer: MarketAnalyzer):
    """打印市场概况"""
    print("\n" + "="*80)
    print("🌍 市场概况")
    print("="*80)
    
    summary = analyzer.get_market_summary()
    
    if 'global' in summary:
        global_data = summary['global']
        print(f"\n💰 全球市场总市值: ${global_data.get('total_market_cap', 0):,.0f}")
        print(f"📈 24小时总成交量: ${global_data.get('total_volume', 0):,.0f}")
        print(f"🔄 24小时市值变化: {global_data.get('market_cap_change_percentage_24h_usd', 0):.2f}%")
        print(f"🪙 活跃加密货币: {global_data.get('active_cryptocurrencies', 0):,}")
        print(f"🏢 活跃交易所: {global_data.get('active_exchanges', 0):,}")
    
    if 'trending' in summary:
        print(f"\n🔥 趋势代币:")
        for i, coin in enumerate(summary['trending'][:5], 1):
            print(f"  {i}. {coin['name']} ({coin['symbol']}) - 排名 #{coin['market_cap_rank']}")

def print_token_analysis(analyzer: MarketAnalyzer, coin_id: str):
    """打印单个代币分析"""
    print(f"\n" + "="*80)
    print(f"🔍 {coin_id.upper()} 详细分析")
    print("="*80)
    
    analysis = analyzer.get_token_analysis(coin_id)
    
    if not analysis:
        print(f"❌ 无法获取 {coin_id} 的数据")
        return
    
    if 'basic_info' in analysis:
        info = analysis['basic_info']
        print(f"\n📊 基本信息:")
        print(f"  名称: {info['name']}")
        print(f"  符号: {info['symbol']}")
        print(f"  当前价格: ${info['current_price']:,.2f}")
        print(f"  市值: ${info['market_cap']:,.0f}")
        print(f"  24小时成交量: ${info['volume_24h']:,.0f}")
        print(f"  24小时涨跌: {info['change_24h']:+.2f}%")
        print(f"  7天涨跌: {info['change_7d']:+.2f}%")
        print(f"  30天涨跌: {info['change_30d']:+.2f}%")
        print(f"  历史最高: ${info['ath']:,.2f}")
        print(f"  历史最低: ${info['atl']:,.2f}")
    
    if 'network_activity' in analysis:
        network = analysis['network_activity']
        print(f"\n🌐 网络活跃度:")
        print(f"  活跃地址数: {network.get('active_addresses', 0):,}")
        print(f"  新增地址数: {network.get('new_addresses', 0):,}")
        print(f"  交易数量: {network.get('transaction_count', 0):,}")
    
    if 'sentiment' in analysis:
        sentiment = analysis['sentiment']
        print(f"\n📈 市场情绪:")
        print(f"  NVT比率: {sentiment.get('nvt_ratio', 0):.2f}")
        print(f"  MVRV比率: {sentiment.get('mvrv_ratio', 0):.2f}")
        print(f"  恐惧贪婪指数: {sentiment.get('fear_greed_index', 0):.2f}")

def print_volume_analysis(analyzer: MarketAnalyzer):
    """打印交易量分析"""
    print("\n" + "="*80)
    print("📊 交易量分析")
    print("="*80)
    
    volume_df = analyzer.get_volume_analysis()
    
    if volume_df.empty:
        print("❌ 无法获取交易量数据")
        return
    
    print(f"\n主要代币交易量统计:")
    print("-" * 80)
    
    for _, row in volume_df.iterrows():
        symbol = row['symbol']
        current_vol = row['current_volume']
        avg_vol = row['avg_volume']
        change_24h = row['volume_change_24h']
        trend = row['volume_trend']
        
        trend_icon = "📈" if trend == "increasing" else "📉"
        change_icon = "🟢" if change_24h > 0 else "🔴" if change_24h < 0 else "⚪"
        
        print(f"{symbol:<10} 当前: {current_vol:>12,.0f} "
              f"平均: {avg_vol:>12,.0f} "
              f"{change_icon} {change_24h:>6.2f}% {trend_icon}")

def demo_mode():
    """演示模式"""
    print("🚀 TokenData 演示模式")
    print("正在初始化数据源...")
    
    # 设置环境
    env = setup_environment()
    
    # 创建分析器
    analyzer = MarketAnalyzer(
        coingecko_api_key=env['coingecko_api_key'],
        binance_api_key=env['binance_api_key'],
        binance_secret_key=env['binance_secret_key'],
        glassnode_api_key=env['glassnode_api_key']
    )
    
    try:
        # 显示市场数据
        print_market_data(analyzer, 20)
        
        # 显示市场概况
        print_market_summary(analyzer)
        
        # 显示主要代币分析
        major_coins = ['bitcoin', 'ethereum', 'binancecoin']
        for coin_id in major_coins:
            print_token_analysis(analyzer, coin_id)
        
        # 显示交易量分析
        print_volume_analysis(analyzer)
        
        print("\n" + "="*80)
        print("✅ 演示完成！")
        print("="*80)
        
    except Exception as e:
        logger.error(f"演示过程中出现错误: {e}")
        print(f"❌ 演示失败: {e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='TokenData - 加密货币市场数据分析工具')
    parser.add_argument('--demo', action='store_true', help='运行演示模式')
    parser.add_argument('--market', action='store_true', help='显示市场数据')
    parser.add_argument('--summary', action='store_true', help='显示市场概况')
    parser.add_argument('--token', type=str, help='分析特定代币 (例如: bitcoin)')
    parser.add_argument('--volume', action='store_true', help='显示交易量分析')
    parser.add_argument('--limit', type=int, default=20, help='显示代币数量限制')
    
    args = parser.parse_args()
    
    # 如果没有参数，运行演示模式
    if not any([args.demo, args.market, args.summary, args.token, args.volume]):
        demo_mode()
        return
    
    # 设置环境
    env = setup_environment()
    
    # 创建分析器
    analyzer = MarketAnalyzer(
        coingecko_api_key=env['coingecko_api_key'],
        binance_api_key=env['binance_api_key'],
        binance_secret_key=env['binance_secret_key'],
        glassnode_api_key=env['glassnode_api_key']
    )
    
    try:
        if args.demo:
            demo_mode()
        elif args.market:
            print_market_data(analyzer, args.limit)
        elif args.summary:
            print_market_summary(analyzer)
        elif args.token:
            print_token_analysis(analyzer, args.token)
        elif args.volume:
            print_volume_analysis(analyzer)
            
    except Exception as e:
        logger.error(f"执行过程中出现错误: {e}")
        print(f"❌ 执行失败: {e}")

if __name__ == "__main__":
    main()
