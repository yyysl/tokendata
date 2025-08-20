#!/usr/bin/env python3
"""
快速测试脚本
验证主流代币监控功能
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_sources.free_data_aggregator import FreeDataAggregator

def test_basic_functionality():
    """测试基本功能"""
    print("🧪 测试主流代币监控功能")
    print("=" * 50)
    
    try:
        # 创建数据聚合器
        aggregator = FreeDataAggregator()
        
        # 测试1: 获取市场数据
        print("1. 测试获取市场数据...")
        df = aggregator.get_hourly_market_data(limit=5)
        if not df.empty:
            print(f"   ✅ 成功获取 {len(df)} 个代币数据")
            print(f"   前3个代币: {', '.join(df['name'].head(3).tolist())}")
        else:
            print("   ❌ 无法获取市场数据")
            return False
        
        # 测试2: 获取全球市场数据
        print("2. 测试获取全球市场数据...")
        global_data = aggregator.get_global_market_data()
        if global_data:
            print(f"   ✅ 成功获取全球市场数据")
            print(f"   总市值: ${global_data.get('total_market_cap', 0):,.0f}")
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
        
        # 测试4: 获取交易所数据
        print("4. 测试获取交易所数据...")
        exchanges = aggregator.get_exchange_volume_distribution()
        if exchanges:
            print(f"   ✅ 成功获取 {len(exchanges)} 个交易所数据")
            exchange_names = list(exchanges.keys())[:3]
            print(f"   前3个交易所: {', '.join(exchange_names)}")
        else:
            print("   ❌ 无法获取交易所数据")
        
        print("\n" + "=" * 50)
        print("✅ 基本功能测试完成！")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def show_sample_data():
    """显示示例数据"""
    print("\n📊 示例数据展示")
    print("=" * 50)
    
    try:
        aggregator = FreeDataAggregator()
        
        # 获取前10个代币数据
        df = aggregator.get_hourly_market_data(limit=10)
        
        if df.empty:
            print("❌ 无法获取数据")
            return
        
        print("前10个主流代币:")
        print("-" * 80)
        print(f"{'排名':<4} {'代币':<15} {'价格':<12} {'1h变化':<8} {'24h变化':<8}")
        print("-" * 80)
        
        for _, row in df.head(10).iterrows():
            change_1h = row.get('change_1h', 0)
            change_24h = row.get('change_24h', 0)
            
            # 变化指示器
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
        
        print("\n" + "=" * 50)
        print("✅ 数据展示完成！")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ 数据展示失败: {e}")

def main():
    """主函数"""
    print("🚀 TokenData 快速测试")
    print("=" * 50)
    
    # 测试基本功能
    if test_basic_functionality():
        # 显示示例数据
        show_sample_data()
        
        print("\n🎉 测试成功！你可以开始使用以下命令：")
        print("   python token_monitor.py          # 查看主流代币变化")
        print("   python token_monitor.py --gainers # 查看涨幅榜")
        print("   python token_monitor.py --token bitcoin # 查看比特币详情")
    else:
        print("\n❌ 测试失败，请检查网络连接和依赖安装")

if __name__ == "__main__":
    main()
