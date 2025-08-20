#!/usr/bin/env python3
"""
TokenData 基本功能测试
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_sources.coingecko import CoinGeckoAPI
from src.data_sources.binance import BinanceAPI

def test_coingecko():
    """测试CoinGecko API"""
    print("🧪 测试 CoinGecko API...")
    
    try:
        api = CoinGeckoAPI()
        
        # 测试获取top coins
        coins = api.get_top_coins(limit=5)
        if coins:
            print(f"✅ 成功获取 {len(coins)} 个代币数据")
            for coin in coins[:3]:
                print(f"   - {coin['name']} ({coin['symbol'].upper()})")
        else:
            print("❌ 无法获取代币数据")
        
        # 测试获取比特币数据
        btc_data = api.get_coin_data('bitcoin')
        if btc_data:
            print("✅ 成功获取比特币详细数据")
        else:
            print("❌ 无法获取比特币数据")
            
    except Exception as e:
        print(f"❌ CoinGecko API 测试失败: {e}")

def test_binance():
    """测试Binance API"""
    print("\n🧪 测试 Binance API...")
    
    try:
        api = BinanceAPI()
        
        # 测试获取BTC/USDT ticker
        ticker = api.get_ticker('BTC/USDT')
        if ticker:
            print("✅ 成功获取BTC/USDT行情数据")
            print(f"   价格: ${ticker.get('last', 0):,.2f}")
            print(f"   24h变化: {ticker.get('percentage', 0):.2f}%")
        else:
            print("❌ 无法获取BTC/USDT数据")
        
        # 测试获取24小时统计
        stats = api.get_24hr_stats('BTC/USDT')
        if stats:
            print("✅ 成功获取24小时统计数据")
        else:
            print("❌ 无法获取24小时统计数据")
            
    except Exception as e:
        print(f"❌ Binance API 测试失败: {e}")

def test_market_analyzer():
    """测试市场分析器"""
    print("\n🧪 测试市场分析器...")
    
    try:
        from src.analysis.market_analyzer import MarketAnalyzer
        
        analyzer = MarketAnalyzer()
        
        # 测试获取综合市场数据
        df = analyzer.get_comprehensive_market_data(limit=5)
        if not df.empty:
            print(f"✅ 成功获取综合市场数据 ({len(df)} 个代币)")
        else:
            print("❌ 无法获取综合市场数据")
        
        # 测试获取市场概况
        summary = analyzer.get_market_summary()
        if summary:
            print("✅ 成功获取市场概况")
        else:
            print("❌ 无法获取市场概况")
            
    except Exception as e:
        print(f"❌ 市场分析器测试失败: {e}")

def main():
    """主测试函数"""
    print("🚀 TokenData 基本功能测试")
    print("=" * 50)
    
    test_coingecko()
    test_binance()
    test_market_analyzer()
    
    print("\n" + "=" * 50)
    print("✅ 测试完成！")

if __name__ == "__main__":
    main()
