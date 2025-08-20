"""
资金流向分析模块
提供代币资金流入流出分析
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class FlowAnalyzer:
    """资金流向分析器"""
    
    def __init__(self):
        # 主要交易所列表
        self.major_exchanges = [
            'binance', 'coinbase', 'kraken', 'kucoin', 'okx',
            'bybit', 'gate-io', 'huobi', 'bitfinex', 'bitstamp'
        ]
        
        # 主要ETF列表
        self.major_etfs = [
            'GBTC', 'ETHE', 'BITO', 'BITI', 'BTF', 'BITS'
        ]
    
    def analyze_volume_flow(self, price_change: float, volume_24h: float, 
                           price_volatility: float = None) -> Tuple[float, str, float]:
        """
        基于价格变化和交易量分析资金流向
        
        Args:
            price_change: 价格变化百分比
            volume_24h: 24小时交易量
            price_volatility: 价格波动性
            
        Returns:
            (流向金额, 颜色, 置信度)
        """
        try:
            # 计算资金流向金额
            # 基于价格变化幅度和交易量来估算资金流向
            if price_change > 0:
                # 价格上涨，估算流入金额
                # 流入金额 = 交易量 * 价格变化比例 * 流入系数
                inflow_ratio = min(abs(price_change) / 100.0, 0.3)  # 最大30%的交易量作为流入
                flow_amount = volume_24h * inflow_ratio
                color = "#27ae60"  # 绿色表示流入
            elif price_change < 0:
                # 价格下跌，估算流出金额
                # 流出金额 = 交易量 * 价格变化比例 * 流出系数
                outflow_ratio = min(abs(price_change) / 100.0, 0.3)  # 最大30%的交易量作为流出
                flow_amount = -volume_24h * outflow_ratio
                color = "#e74c3c"  # 红色表示流出
            else:
                # 价格无变化，资金流向平衡
                flow_amount = 0.0
                color = "#95a5a6"  # 灰色表示平衡
            
            # 计算置信度（基于价格变化幅度）
            confidence = min(abs(price_change) / 10.0, 1.0)
            
            return flow_amount, color, confidence
                
        except Exception as e:
            logger.error(f"分析交易量流向失败: {e}")
            return 0.0, "#95a5a6", 0.0
    
    def analyze_exchange_flow(self, exchange_data: Dict) -> Dict:
        """
        分析交易所资金流向
        
        Args:
            exchange_data: 交易所数据
            
        Returns:
            交易所流向分析结果
        """
        try:
            flow_analysis = {}
            
            for exchange, data in exchange_data.items():
                if exchange in self.major_exchanges:
                    # 分析交易所交易量变化
                    volume = data.get('volume', 0)
                    bid_volume = data.get('bid_volume', 0)
                    ask_volume = data.get('ask_volume', 0)
                    
                    if bid_volume > 0 and ask_volume > 0:
                        # 计算买卖比例
                        buy_ratio = bid_volume / (bid_volume + ask_volume)
                        
                        if buy_ratio > 0.6:
                            flow_analysis[exchange] = {
                                'flow': '流入',
                                'color': '#27ae60',
                                'confidence': buy_ratio,
                                'volume': volume
                            }
                        elif buy_ratio < 0.4:
                            flow_analysis[exchange] = {
                                'flow': '流出',
                                'color': '#e74c3c',
                                'confidence': 1 - buy_ratio,
                                'volume': volume
                            }
                        else:
                            flow_analysis[exchange] = {
                                'flow': '平衡',
                                'color': '#95a5a6',
                                'confidence': 0.5,
                                'volume': volume
                            }
            
            return flow_analysis
            
        except Exception as e:
            logger.error(f"分析交易所流向失败: {e}")
            return {}
    
    def analyze_etf_flow(self, etf_data: Dict) -> Dict:
        """
        分析ETF资金流向
        
        Args:
            etf_data: ETF数据
            
        Returns:
            ETF流向分析结果
        """
        try:
            etf_analysis = {}
            
            for etf, data in etf_data.items():
                if etf in self.major_etfs:
                    # 分析ETF资金流向
                    net_flow = data.get('net_flow', 0)
                    volume = data.get('volume', 0)
                    premium = data.get('premium', 0)
                    
                    if net_flow > 0:
                        etf_analysis[etf] = {
                            'flow': '流入',
                            'color': '#27ae60',
                            'confidence': min(abs(net_flow) / volume, 1.0) if volume > 0 else 0.5,
                            'amount': net_flow,
                            'premium': premium
                        }
                    elif net_flow < 0:
                        etf_analysis[etf] = {
                            'flow': '流出',
                            'color': '#e74c3c',
                            'confidence': min(abs(net_flow) / volume, 1.0) if volume > 0 else 0.5,
                            'amount': net_flow,
                            'premium': premium
                        }
                    else:
                        etf_analysis[etf] = {
                            'flow': '平衡',
                            'color': '#95a5a6',
                            'confidence': 0.5,
                            'amount': 0,
                            'premium': premium
                        }
            
            return etf_analysis
            
        except Exception as e:
            logger.error(f"分析ETF流向失败: {e}")
            return {}
    
    def get_comprehensive_flow(self, token_data: Dict) -> Dict:
        """
        获取综合资金流向分析
        
        Args:
            token_data: 代币数据
            
        Returns:
            综合流向分析结果
        """
        try:
            # 基础数据
            price_change_1h = token_data.get('change_1h', 0)
            price_change_24h = token_data.get('change_24h', 0)
            price_change_7d = token_data.get('change_7d', 0)
            volume_24h = token_data.get('volume_24h', 0)
            
            # 分析各时间段流向
            flow_1h, color_1h, conf_1h = self.analyze_volume_flow(price_change_1h, volume_24h / 24)
            flow_24h, color_24h, conf_24h = self.analyze_volume_flow(price_change_24h, volume_24h)
            flow_7d, color_7d, conf_7d = self.analyze_volume_flow(price_change_7d, volume_24h * 7)
            
            return {
                '1h': {
                    'flow': flow_1h,
                    'color': color_1h,
                    'confidence': conf_1h,
                    'price_change': price_change_1h,
                    'volume': volume_24h / 24
                },
                '24h': {
                    'flow': flow_24h,
                    'color': color_24h,
                    'confidence': conf_24h,
                    'price_change': price_change_24h,
                    'volume': volume_24h
                },
                '7d': {
                    'flow': flow_7d,
                    'color': color_7d,
                    'confidence': conf_7d,
                    'price_change': price_change_7d,
                    'volume': volume_24h * 7
                },
                'overall_sentiment': self._calculate_overall_sentiment(flow_1h, flow_24h, flow_7d)
            }
            
        except Exception as e:
            logger.error(f"获取综合流向分析失败: {e}")
            return {}
    
    def _calculate_overall_sentiment(self, flow_1h: float, flow_24h: float, flow_7d: float) -> str:
        """
        计算整体情绪
        
        Args:
            flow_1h: 1小时流向值
            flow_24h: 24小时流向值
            flow_7d: 7天流向值
            
        Returns:
            整体情绪
        """
        try:
            # 基于流向值计算情绪
            avg_flow = (flow_1h + flow_24h + flow_7d) / 3
            
            if avg_flow > 1.0:
                return "看涨"
            elif avg_flow < -1.0:
                return "看跌"
            else:
                return "中性"
                
        except Exception as e:
            logger.error(f"计算整体情绪失败: {e}")
            return "未知"
    
    def get_flow_summary(self, all_tokens_data: List[Dict]) -> Dict:
        """
        获取整体资金流向摘要
        
        Args:
            all_tokens_data: 所有代币数据
            
        Returns:
            流向摘要
        """
        try:
            total_inflow = 0
            total_outflow = 0
            inflow_tokens = []
            outflow_tokens = []
            
            for token in all_tokens_data:
                flow_analysis = self.get_comprehensive_flow(token)
                
                if flow_analysis.get('24h', {}).get('flow') == '流入':
                    total_inflow += flow_analysis['24h']['volume']
                    inflow_tokens.append(token['name'])
                elif flow_analysis.get('24h', {}).get('flow') == '流出':
                    total_outflow += flow_analysis['24h']['volume']
                    outflow_tokens.append(token['name'])
            
            return {
                'total_inflow': total_inflow,
                'total_outflow': total_outflow,
                'net_flow': total_inflow - total_outflow,
                'inflow_tokens': inflow_tokens[:5],  # 前5个流入代币
                'outflow_tokens': outflow_tokens[:5],  # 前5个流出代币
                'flow_ratio': total_inflow / (total_inflow + total_outflow) if (total_inflow + total_outflow) > 0 else 0.5
            }
            
        except Exception as e:
            logger.error(f"获取流向摘要失败: {e}")
            return {}
