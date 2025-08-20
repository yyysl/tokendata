"""
免费数据聚合器
整合多个免费数据源，提供小时级别的监控
"""
import requests
import pandas as pd
import time
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

class FreeDataAggregator:
    """免费数据聚合器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # 主流代币列表（市值前50）
        self.major_tokens = [
            'bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana',
            'ripple', 'polkadot', 'dogecoin', 'avalanche-2', 'polygon',
            'chainlink', 'uniswap', 'litecoin', 'cosmos', 'ethereum-classic',
            'stellar', 'monero', 'algorand', 'vechain', 'filecoin',
            'tron', 'eos', 'aave', 'tezos', 'neo',
            'iota', 'pancakeswap-token', 'crypto-com-chain', 'theta-token', 'bitcoin-cash',
            'flow', 'klaytn', 'fantom', 'the-graph', 'maker',
            'compound-governance-token', 'synthetix-network-token', 'dash', 'waves', 'decred',
            'zilliqa', 'qtum', 'nano', 'icon', 'omisego',
            '0x', 'basic-attention-token', 'enjincoin', 'siacoin', 'golem'
        ]
        
        # 主要交易所列表
        self.major_exchanges = [
            'binance', 'coinbase', 'kraken', 'kucoin', 'okx',
            'bybit', 'gate-io', 'huobi', 'bitfinex', 'bitstamp'
        ]
    
    def get_hourly_market_data(self, limit: int = 50) -> pd.DataFrame:
        """
        获取小时级别的市场数据
        
        Args:
            limit: 获取的代币数量
            
        Returns:
            市场数据DataFrame
        """
        try:
            # 使用CoinGecko免费API
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': limit,
                'page': 1,
                'sparkline': False,
                'price_change_percentage': '1h,24h,7d'
            }
            
            # 添加重试机制
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.session.get(url, params=params)
                    
                    if response.status_code == 429:
                        # API限制，等待后重试
                        wait_time = (attempt + 1) * 10  # 递增等待时间
                        logger.warning(f"API限制，等待 {wait_time} 秒后重试...")
                        time.sleep(wait_time)
                        continue
                    
                    response.raise_for_status()
                    break
                    
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries - 1:
                        raise e
                    wait_time = (attempt + 1) * 5
                    logger.warning(f"请求失败，等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
            
            data = response.json()
            if not data:
                logger.error("API返回空数据")
                return pd.DataFrame()
            
            df = pd.DataFrame(data)
            
            # 重命名列
            column_mapping = {
                'id': 'coin_id',
                'symbol': 'symbol',
                'name': 'name',
                'current_price': 'price',
                'market_cap': 'market_cap',
                'market_cap_rank': 'rank',
                'total_volume': 'volume_24h',
                'price_change_percentage_1h_in_currency': 'change_1h',
                'price_change_percentage_24h_in_currency': 'change_24h',
                'price_change_percentage_7d_in_currency': 'change_7d',
                'circulating_supply': 'circulating_supply',
                'total_supply': 'total_supply',
                'max_supply': 'max_supply',
                'ath': 'ath',
                'ath_change_percentage': 'ath_change_percent',
                'last_updated': 'last_updated'
            }
            
            df = df.rename(columns=column_mapping)
            df['last_updated'] = pd.to_datetime(df['last_updated'])
            df['timestamp'] = datetime.now()
            
            # 计算额外指标
            df['volume_market_cap_ratio'] = df['volume_24h'] / df['market_cap']
            df['price_ath_ratio'] = df['price'] / df['ath']
            
            return df
            
        except Exception as e:
            logger.error(f"获取小时级市场数据失败: {e}")
            return pd.DataFrame()
    
    def get_exchange_volume_distribution(self) -> Dict:
        """
        获取交易所交易量分布
        
        Returns:
            交易所交易量分布数据
        """
        try:
            url = "https://api.coingecko.com/api/v3/exchanges"
            params = {
                'per_page': 20,
                'page': 1
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            exchanges = response.json()
            
            distribution = {}
            for exchange in exchanges:
                distribution[exchange['id']] = {
                    'name': exchange['name'],
                    'trust_score': exchange.get('trust_score'),
                    'trade_volume_24h_btc': exchange.get('trade_volume_24h_btc'),
                    'trade_volume_24h_btc_normalized': exchange.get('trade_volume_24h_btc_normalized'),
                    'year_established': exchange.get('year_established'),
                    'country': exchange.get('country')
                }
            
            return distribution
            
        except Exception as e:
            logger.error(f"获取交易所交易量分布失败: {e}")
            return {}
    
    def get_token_exchange_data(self, coin_id: str) -> Dict:
        """
        获取代币在各交易所的数据
        
        Args:
            coin_id: 代币ID
            
        Returns:
            交易所数据
        """
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
            params = {
                'localization': False,
                'tickers': True,
                'market_data': True,
                'community_data': False,
                'developer_data': False,
                'sparkline': False
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # 提取交易所数据
            exchange_data = {}
            if 'tickers' in data:
                for ticker in data['tickers']:
                    exchange = ticker['market']['identifier']
                    if exchange in self.major_exchanges:
                        exchange_data[exchange] = {
                            'base': ticker['base'],
                            'target': ticker['target'],
                            'volume': ticker['volume'],
                            'converted_volume': ticker.get('converted_volume', {}),
                            'bid': ticker.get('bid'),
                            'ask': ticker.get('ask'),
                            'last': ticker.get('last'),
                            'timestamp': ticker.get('timestamp')
                        }
            
            return exchange_data
            
        except Exception as e:
            logger.error(f"获取代币交易所数据失败 {coin_id}: {e}")
            return {}
    
    def get_trending_coins(self) -> List[Dict]:
        """
        获取趋势代币（可能反映资金流向）
        
        Returns:
            趋势代币列表
        """
        try:
            url = "https://api.coingecko.com/api/v3/search/trending"
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            trending = []
            
            for coin in data.get('coins', []):
                item = coin['item']
                trending.append({
                    'id': item['id'],
                    'name': item['name'],
                    'symbol': item['symbol'],
                    'market_cap_rank': item['market_cap_rank'],
                    'price_btc': item['price_btc'],
                    'score': item['score']
                })
            
            return trending
            
        except Exception as e:
            logger.error(f"获取趋势代币失败: {e}")
            return []
    
    def get_global_market_data(self) -> Dict:
        """
        获取全球市场数据
        
        Returns:
            全球市场数据
        """
        try:
            url = "https://api.coingecko.com/api/v3/global"
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data:
                global_data = data['data']
                return {
                    'total_market_cap': global_data.get('total_market_cap', {}).get('usd'),
                    'total_volume': global_data.get('total_volume', {}).get('usd'),
                    'market_cap_percentage': global_data.get('market_cap_percentage'),
                    'market_cap_change_percentage_24h_usd': global_data.get('market_cap_change_percentage_24h_usd'),
                    'active_cryptocurrencies': global_data.get('active_cryptocurrencies'),
                    'active_exchanges': global_data.get('active_exchanges'),
                    'bitcoin_dominance': global_data.get('market_cap_percentage', {}).get('btc'),
                    'ethereum_dominance': global_data.get('market_cap_percentage', {}).get('eth')
                }
            
            return {}
            
        except Exception as e:
            logger.error(f"获取全球市场数据失败: {e}")
            return {}
    
    def get_hourly_price_changes(self, coin_ids: List[str] = None) -> pd.DataFrame:
        """
        获取小时级价格变化
        
        Args:
            coin_ids: 代币ID列表
            
        Returns:
            价格变化DataFrame
        """
        try:
            if not coin_ids:
                coin_ids = self.major_tokens[:20]  # 默认前20个
            
            price_changes = []
            
            for coin_id in coin_ids:
                try:
                    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
                    params = {
                        'vs_currency': 'usd',
                        'days': 1,
                        'interval': 'hourly'
                    }
                    
                    response = self.session.get(url, params=params)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    if 'prices' in data and len(data['prices']) >= 2:
                        # 计算小时变化
                        current_price = data['prices'][-1][1]
                        hour_ago_price = data['prices'][-2][1]
                        hour_change = ((current_price - hour_ago_price) / hour_ago_price) * 100
                        
                        price_changes.append({
                            'coin_id': coin_id,
                            'current_price': current_price,
                            'hour_ago_price': hour_ago_price,
                            'hour_change_percent': hour_change,
                            'timestamp': datetime.fromtimestamp(data['prices'][-1][0] / 1000)
                        })
                    
                    # 添加延时避免API限制
                    time.sleep(0.1)
                    
                except Exception as e:
                    logger.error(f"获取{coin_id}小时价格变化失败: {e}")
                    continue
            
            return pd.DataFrame(price_changes)
            
        except Exception as e:
            logger.error(f"获取小时价格变化失败: {e}")
            return pd.DataFrame()
    
    def get_volume_analysis(self, coin_ids: List[str] = None) -> pd.DataFrame:
        """
        获取交易量分析
        
        Args:
            coin_ids: 代币ID列表
            
        Returns:
            交易量分析DataFrame
        """
        try:
            if not coin_ids:
                coin_ids = self.major_tokens[:20]
            
            volume_data = []
            
            for coin_id in coin_ids:
                try:
                    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
                    params = {
                        'vs_currency': 'usd',
                        'days': 7,
                        'interval': 'daily'
                    }
                    
                    response = self.session.get(url, params=params)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    if 'total_volumes' in data and len(data['total_volumes']) >= 2:
                        volumes = [v[1] for v in data['total_volumes']]
                        current_volume = volumes[-1]
                        avg_volume = sum(volumes) / len(volumes)
                        volume_change = ((current_volume - volumes[-2]) / volumes[-2]) * 100 if len(volumes) > 1 else 0
                        
                        volume_data.append({
                            'coin_id': coin_id,
                            'current_volume': current_volume,
                            'avg_volume_7d': avg_volume,
                            'volume_change_24h': volume_change,
                            'volume_trend': 'increasing' if current_volume > avg_volume else 'decreasing'
                        })
                    
                    time.sleep(0.1)
                    
                except Exception as e:
                    logger.error(f"获取{coin_id}交易量分析失败: {e}")
                    continue
            
            return pd.DataFrame(volume_data)
            
        except Exception as e:
            logger.error(f"获取交易量分析失败: {e}")
            return pd.DataFrame()
