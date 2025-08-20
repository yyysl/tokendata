#!/usr/bin/env python3
"""
简化的资金流向分析测试
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.analysis.flow_analyzer import FlowAnalyzer

def test_flow_analyzer():
    """测试资金流向分析器"""
    print("🧪 测试资金流向分析功能")
    print("=" * 50)
    
    try:
        # 创建分析器
        flow_analyzer = FlowAnalyzer()
        
        # 测试数据
        test_tokens = [
            {
                'name': 'Bitcoin',
                'symbol': 'BTC',
                'change_1h': 2.5,
                'change_24h': 5.8,
                'change_7d': 12.3,
                'volume_24h': 25000000000
            },
            {
                'name': 'Ethereum',
                'symbol': 'ETH',
                'change_1h': -1.2,
                'change_24h': -3.5,
                'change_7d': -8.7,
                'volume_24h': 15000000000
            },
            {
                'name': 'Solana',
                'symbol': 'SOL',
                'change_1h': 0.8,
                'change_24h': -1.2,
                'change_7d': 4.5,
                'volume_24h': 8000000000
            },
            {
                'name': 'Cardano',
                'symbol': 'ADA',
                'change_1h': -2.1,
                'change_24h': -5.3,
                'change_7d': -12.8,
                'volume_24h': 3000000000
            },
            {
                'name': 'Polkadot',
                'symbol': 'DOT',
                'change_1h': 1.5,
                'change_24h': 3.2,
                'change_7d': 7.8,
                'volume_24h': 2000000000
            }
        ]
        
        print("1. 测试单个代币资金流向分析...")
        
        for i, token in enumerate(test_tokens, 1):
            token_data = {
                'change_1h': token['change_1h'],
                'change_24h': token['change_24h'],
                'change_7d': token['change_7d'],
                'volume_24h': token['volume_24h']
            }
            
            flow_analysis = flow_analyzer.get_comprehensive_flow(token_data)
            
            print(f"   {i}. {token['name']} ({token['symbol']})")
            print(f"      价格变化: 1h={token_data['change_1h']:+.2f}%, 24h={token_data['change_24h']:+.2f}%, 7d={token_data['change_7d']:+.2f}%")
            print(f"      资金流向: 1h=${flow_analysis.get('1h', {}).get('flow', 0):,.2f}, 24h=${flow_analysis.get('24h', {}).get('flow', 0):,.2f}, 7d=${flow_analysis.get('7d', {}).get('flow', 0):,.2f}")
            print(f"      整体情绪: {flow_analysis.get('overall_sentiment', 'N/A')}")
            print()
        
        # 测试流向摘要
        print("2. 测试流向摘要...")
        flow_summary = flow_analyzer.get_flow_summary(test_tokens)
        
        if flow_summary:
            print(f"   总流入: ${flow_summary.get('total_inflow', 0):,.0f}")
            print(f"   总流出: ${flow_summary.get('total_outflow', 0):,.0f}")
            print(f"   净流向: ${flow_summary.get('net_flow', 0):,.0f}")
            print(f"   流向比例: {flow_summary.get('flow_ratio', 0):.2%}")
            print(f"   主要流入代币: {', '.join(flow_summary.get('inflow_tokens', [])[:3])}")
            print(f"   主要流出代币: {', '.join(flow_summary.get('outflow_tokens', [])[:3])}")
        
        print("\n" + "=" * 50)
        print("✅ 资金流向分析测试完成！")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def show_flow_examples():
    """显示资金流向分析示例"""
    print("\n📊 资金流向分析示例")
    print("=" * 50)
    
    try:
        flow_analyzer = FlowAnalyzer()
        
        # 示例数据
        examples = [
            {
                'name': '示例1: 强势上涨',
                'data': {'change_1h': 5.2, 'change_24h': 12.5, 'change_7d': 25.0, 'volume_24h': 1000000}
            },
            {
                'name': '示例2: 强势下跌',
                'data': {'change_1h': -3.8, 'change_24h': -8.2, 'change_7d': -15.5, 'volume_24h': 800000}
            },
            {
                'name': '示例3: 震荡整理',
                'data': {'change_1h': 0.5, 'change_24h': -1.2, 'change_7d': 2.8, 'volume_24h': 500000}
            }
        ]
        
        for example in examples:
            print(f"\n{example['name']}:")
            flow_analysis = flow_analyzer.get_comprehensive_flow(example['data'])
            
            print(f"  1h流向: {flow_analysis.get('1h', {}).get('flow', 'N/A')} (置信度: {flow_analysis.get('1h', {}).get('confidence', 0):.2f})")
            print(f"  24h流向: {flow_analysis.get('24h', {}).get('flow', 'N/A')} (置信度: {flow_analysis.get('24h', {}).get('confidence', 0):.2f})")
            print(f"  7d流向: {flow_analysis.get('7d', {}).get('flow', 'N/A')} (置信度: {flow_analysis.get('7d', {}).get('confidence', 0):.2f})")
            print(f"  整体情绪: {flow_analysis.get('overall_sentiment', 'N/A')}")
        
        print("\n" + "=" * 50)
        print("✅ 示例展示完成！")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ 示例展示失败: {e}")

def main():
    """主函数"""
    print("🚀 TokenData 资金流向分析测试（简化版）")
    print("=" * 50)
    
    # 测试资金流向分析
    if test_flow_analyzer():
        # 显示示例
        show_flow_examples()
        
        print("\n🎉 测试成功！资金流向分析功能正常")
        print("\n📱 现在你可以访问Web应用查看完整功能：")
        print("   http://127.0.0.1:8050")
    else:
        print("\n❌ 测试失败，请检查依赖安装")

if __name__ == "__main__":
    main()
