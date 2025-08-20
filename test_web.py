#!/usr/bin/env python3
"""
测试Web应用功能
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_sources.free_data_aggregator import FreeDataAggregator

def test_web_data():
    """测试Web应用所需的数据"""
    print("🧪 测试Web应用数据功能")
    print("=" * 50)
    
    try:
        aggregator = FreeDataAggregator()
        
        # 测试1: 获取市场数据
        print("1. 测试获取市场数据...")
        df = aggregator.get_hourly_market_data(limit=20)
        if not df.empty:
            print(f"   ✅ 成功获取 {len(df)} 个代币数据")
            print(f"   前5个代币: {', '.join(df['name'].head(5).tolist())}")
        else:
            print("   ❌ 无法获取市场数据")
            return False
        
        # 测试2: 获取全球市场数据
        print("2. 测试获取全球市场数据...")
        global_data = aggregator.get_global_market_data()
        if global_data:
            print(f"   ✅ 成功获取全球市场数据")
            print(f"   总市值: ${global_data.get('total_market_cap', 0):,.0f}")
            print(f"   24h成交量: ${global_data.get('total_volume', 0):,.0f}")
        else:
            print("   ❌ 无法获取全球市场数据")
        
        # 测试3: 获取趋势代币
        print("3. 测试获取趋势代币...")
        trending = aggregator.get_trending_coins()
        if trending:
            print(f"   ✅ 成功获取 {len(trending)} 个趋势代币")
            print(f"   前3个趋势代币: {', '.join([coin['name'] for coin in trending[:3]])}")
        else:
            print("   ❌ 无法获取趋势代币")
        
        print("\n" + "=" * 50)
        print("✅ Web应用数据测试完成！")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def show_sample_data():
    """显示示例数据"""
    print("\n📊 Web应用示例数据")
    print("=" * 50)
    
    try:
        aggregator = FreeDataAggregator()
        
        # 获取前10个代币数据
        df = aggregator.get_hourly_market_data(limit=10)
        
        if df.empty:
            print("❌ 无法获取数据")
            return
        
        print("前10个主流代币数据:")
        print("-" * 80)
        print(f"{'排名':<4} {'代币':<15} {'价格':<12} {'1h变化':<8} {'24h变化':<8}")
        print("-" * 80)
        
        for _, row in df.head(10).iterrows():
            change_1h = row.get('change_1h', 0)
            change_24h = row.get('change_24h', 0)
            
            # 变化颜色指示
            if change_1h is not None:
                if change_1h > 0:
                    change_icon = "🟢"
                elif change_1h < 0:
                    change_icon = "🔴"
                else:
                    change_icon = "⚪"
            else:
                change_icon = "⚪"
                change_1h = 0
            
            print(f"{row['rank']:<4} {row['name']:<15} ${row['price']:<11,.2f} "
                  f"{change_icon} {change_1h:<6.2f}% {change_24h:<6.2f}%")
        
        # 显示全球市场数据
        global_data = aggregator.get_global_market_data()
        if global_data:
            print(f"\n🌍 全球市场概况:")
            print(f"   总市值: ${global_data.get('total_market_cap', 0):,.0f}")
            print(f"   24h成交量: ${global_data.get('total_volume', 0):,.0f}")
            print(f"   24h变化: {global_data.get('market_cap_change_percentage_24h_usd', 0):+.2f}%")
            print(f"   BTC主导地位: {global_data.get('bitcoin_dominance', 0):.2f}%")
        
        print("\n" + "=" * 50)
        print("✅ 数据展示完成！")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ 数据展示失败: {e}")

def main():
    """主函数"""
    print("🚀 TokenData Web应用测试")
    print("=" * 50)
    
    # 测试数据功能
    if test_web_data():
        # 显示示例数据
        show_sample_data()
        
        print("\n🎉 测试成功！Web应用数据功能正常")
        print("\n📱 现在你可以启动Web应用：")
        print("   python3 web_app.py")
        print("   然后在浏览器中访问: http://127.0.0.1:8050")
    else:
        print("\n❌ 测试失败，请检查网络连接和依赖安装")

if __name__ == "__main__":
    main()
