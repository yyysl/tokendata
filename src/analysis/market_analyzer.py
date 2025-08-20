"""
市场数据分析器
整合多个数据源，提供综合分析
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import logging
from datetime import datetime, timedelta

from ..data_sources.coingecko import CoinGeckoAPI
from ..data_sources.binance import BinanceAPI
from ..data_sources.glassnode import GlassnodeAPI

logger = logging.getLogger(__name__)

class MarketAnalyzer:
    """市场数据分析器"""
    
    def __init__(self, 
                 coingecko_api_key: Optional[str] = None,
                 binance_api_key: Optional[str] = None,
                 binance_secret_key: Optional[str] = None,
                 glassnode_api_key: Optional[str] = None):
        
        # 初始化数据源
        self.coingecko = CoinGeckoAPI(coingecko_api_key)
        self.binance = BinanceAPI(binance_api_key, binance_secret_key)
        self.glassnode = GlassnodeAPI(glassnode_api_key) if glassnode_api_key else None
        
        # 主流代币列表
        self.major_tokens = {
            'bitcoin': 'BTC',
            'ethereum': 'ETH', 
            'binancecoin': 'BNB',
            'cardano': 'ADA',
            'solana': 'SOL',
            'ripple': 'XRP',
            'polkadot': 'DOT',
            'dogecoin': 'DOGE',
            'avalanche-2': 'AVAX',
            'polygon': 'MATIC'
        }
    
    def get_comprehensive_market_data(self, limit: int = 50) -> pd.DataFrame:
        """
        获取综合市场数据
        
        Args:
            limit: 获取的代币数量
            
        Returns:
            综合市场数据DataFrame
        """
        try:
            # 获取CoinGecko数据
            coins_data = self.coingecko.get_top_coins(limit)
            
            if not coins_data:
                logger.error("无法获取CoinGecko数据")
                return pd.DataFrame()
            
            # 转换为DataFrame
            df = pd.DataFrame(coins_data)
            
            # 重命名列
            column_mapping = {
                'id': 'coin_id',
                'symbol': 'symbol',
                'name': 'name',
                'current_price': 'price',
                'market_cap': 'market_cap',
                'market_cap_rank': 'rank',
                'total_volume': 'volume_24h',
                'price_change_percentage_24h': 'change_24h',
                'price_change_percentage_7d_in_currency': 'change_7d',
                'price_change_percentage_30d_in_currency': 'change_30d',
                'circulating_supply': 'circulating_supply',
                'total_supply': 'total_supply',
                'max_supply': 'max_supply',
                'ath': 'ath',
                'ath_change_percentage': 'ath_change_percent',
                'last_updated': 'last_updated'
            }
            
            df = df.rename(columns=column_mapping)
            
            # 添加时间戳
            df['last_updated'] = pd.to_datetime(df['last_updated'])
            df['timestamp'] = datetime.now()
            
            # 计算额外指标
            df['volume_market_cap_ratio'] = df['volume_24h'] / df['market_cap']
            df['price_ath_ratio'] = df['price'] / df['ath']
            
            return df
            
        except Exception as e:
            logger.error(f"获取综合市场数据失败: {e}")
            return pd.DataFrame()
    
    def get_token_analysis(self, coin_id: str) -> Dict:
        """
        获取单个代币的详细分析
        
        Args:
            coin_id: 代币ID
            
        Returns:
            代币分析数据
        """
        try:
            analysis = {}
            
            # 获取CoinGecko详细数据
            coin_data = self.coingecko.get_coin_data(coin_id)
            if coin_data:
                analysis['basic_info'] = {
                    'name': coin_data.get('name'),
                    'symbol': coin_data.get('symbol', '').upper(),
                    'current_price': coin_data.get('market_data', {}).get('current_price', {}).get('usd'),
                    'market_cap': coin_data.get('market_data', {}).get('market_cap', {}).get('usd'),
                    'volume_24h': coin_data.get('market_data', {}).get('total_volume', {}).get('usd'),
                    'price_change_24h': coin_data.get('market_data', {}).get('price_change_percentage_24h'),
                    'price_change_7d': coin_data.get('market_data', {}).get('price_change_percentage_7d'),
                    'price_change_30d': coin_data.get('market_data', {}).get('price_change_percentage_30d'),
                    'ath': coin_data.get('market_data', {}).get('ath', {}).get('usd'),
                    'atl': coin_data.get('market_data', {}).get('atl', {}).get('usd'),
                    'circulating_supply': coin_data.get('market_data', {}).get('circulating_supply'),
                    'total_supply': coin_data.get('market_data', {}).get('total_supply'),
                    'max_supply': coin_data.get('market_data', {}).get('max_supply')
                }
            
            # 获取Binance数据（如果可用）
            symbol = f"{coin_data.get('symbol', '').upper()}/USDT" if coin_data else None
            if symbol:
                binance_data = self.binance.get_ticker(symbol)
                if binance_data:
                    analysis['binance_data'] = {
                        'bid': binance_data.get('bid'),
                        'ask': binance_data.get('ask'),
                        'bid_volume': binance_data.get('bidVolume'),
                        'ask_volume': binance_data.get('askVolume'),
                        'vwap': binance_data.get('vwap'),
                        'previous_close': binance_data.get('previousClose'),
                        'change': binance_data.get('change'),
                        'percentage': binance_data.get('percentage'),
                        'average': binance_data.get('average'),
                        'base_volume': binance_data.get('baseVolume'),
                        'quote_volume': binance_data.get('quoteVolume')
                    }
            
            # 获取Glassnode数据（如果可用）
            if self.glassnode and coin_id in self.major_tokens:
                asset = self.major_tokens[coin_id]
                
                # 网络活跃度
                network_activity = self.glassnode.get_network_activity(asset)
                if network_activity:
                    analysis['network_activity'] = network_activity
                
                # 市场情绪
                sentiment = self.glassnode.get_market_sentiment(asset)
                if sentiment:
                    analysis['sentiment'] = sentiment
                
                # 挖矿数据（仅适用于BTC）
                if asset == 'BTC':
                    mining_data = self.glassnode.get_mining_data(asset)
                    if mining_data:
                        analysis['mining_data'] = mining_data
                
                # DeFi指标（仅适用于ETH）
                if asset == 'ETH':
                    defi_metrics = self.glassnode.get_defi_metrics(asset)
                    if defi_metrics:
                        analysis['defi_metrics'] = defi_metrics
            
            return analysis
            
        except Exception as e:
            logger.error(f"获取代币分析失败 {coin_id}: {e}")
            return {}
    
    def get_market_summary(self) -> Dict:
        """
        获取市场概况
        
        Returns:
            市场概况数据
        """
        try:
            summary = {}
            
            # 获取全球市场数据
            global_data = self.coingecko.get_global_data()
            if global_data and 'data' in global_data:
                data = global_data['data']
                summary['global'] = {
                    'total_market_cap': data.get('total_market_cap', {}).get('usd'),
                    'total_volume': data.get('total_volume', {}).get('usd'),
                    'market_cap_percentage': data.get('market_cap_percentage'),
                    'market_cap_change_percentage_24h_usd': data.get('market_cap_change_percentage_24h_usd'),
                    'active_cryptocurrencies': data.get('active_cryptocurrencies'),
                    'active_exchanges': data.get('active_exchanges')
                }
            
            # 获取趋势代币
            trending = self.coingecko.get_trending_coins()
            if trending:
                summary['trending'] = [
                    {
                        'name': coin['item']['name'],
                        'symbol': coin['item']['symbol'],
                        'market_cap_rank': coin['item']['market_cap_rank'],
                        'price_btc': coin['item']['price_btc']
                    }
                    for coin in trending[:10]  # 取前10个
                ]
            
            # 获取主要代币的24小时数据
            major_symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'SOL/USDT']
            major_stats = self.binance.get_24hr_stats()
            if major_stats:
                summary['major_tokens_24h'] = major_stats
            
            return summary
            
        except Exception as e:
            logger.error(f"获取市场概况失败: {e}")
            return {}
    
    def get_volume_analysis(self, symbols: List[str] = None) -> pd.DataFrame:
        """
        获取交易量分析
        
        Args:
            symbols: 交易对列表
            
        Returns:
            交易量分析DataFrame
        """
        try:
            if not symbols:
                symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'SOL/USDT']
            
            volume_data = []
            for symbol in symbols:
                volume_stats = self.binance.get_volume_analysis(symbol)
                if volume_stats:
                    volume_data.append(volume_stats)
            
            return pd.DataFrame(volume_data)
            
        except Exception as e:
            logger.error(f"获取交易量分析失败: {e}")
            return pd.DataFrame()
    
    def get_price_correlation(self, symbols: List[str] = None, days: int = 30) -> pd.DataFrame:
        """
        计算价格相关性
        
        Args:
            symbols: 交易对列表
            days: 分析天数
            
        Returns:
            相关性矩阵DataFrame
        """
        try:
            if not symbols:
                symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'SOL/USDT']
            
            # 获取历史价格数据
            price_data = {}
            for symbol in symbols:
                ohlcv = self.binance.get_ohlcv(symbol, '1d', days)
                if not ohlcv.empty:
                    price_data[symbol] = ohlcv['close']
            
            if not price_data:
                return pd.DataFrame()
            
            # 创建价格DataFrame
            df = pd.DataFrame(price_data)
            
            # 计算相关性
            correlation_matrix = df.corr()
            
            return correlation_matrix
            
        except Exception as e:
            logger.error(f"计算价格相关性失败: {e}")
            return pd.DataFrame()
    
    def get_market_indicators(self) -> Dict:
        """
        获取市场指标
        
        Returns:
            市场指标数据
        """
        try:
            indicators = {}
            
            # 获取主要代币数据
            major_coins = ['bitcoin', 'ethereum', 'binancecoin']
            
            for coin_id in major_coins:
                coin_data = self.coingecko.get_coin_data(coin_id)
                if coin_data:
                    market_data = coin_data.get('market_data', {})
                    indicators[coin_id] = {
                        'price': market_data.get('current_price', {}).get('usd'),
                        'market_cap': market_data.get('market_cap', {}).get('usd'),
                        'volume_24h': market_data.get('total_volume', {}).get('usd'),
                        'change_24h': market_data.get('price_change_percentage_24h'),
                        'change_7d': market_data.get('price_change_percentage_7d'),
                        'change_30d': market_data.get('price_change_percentage_30d'),
                        'ath': market_data.get('ath', {}).get('usd'),
                        'ath_change_percent': market_data.get('ath_change_percentage', {}).get('usd'),
                        'atl': market_data.get('atl', {}).get('usd'),
                        'atl_change_percent': market_data.get('atl_change_percentage', {}).get('usd')
                    }
            
            return indicators
            
        except Exception as e:
            logger.error(f"获取市场指标失败: {e}")
            return {}
