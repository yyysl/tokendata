"""
Glassnode API 数据源
提供链上数据分析和资金流向信息
注意：需要付费API密钥
"""
import requests
import pandas as pd
from typing import List, Dict, Optional
import time
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class GlassnodeAPI:
    """Glassnode API 客户端"""
    
    def __init__(self, api_key: str):
        self.base_url = "https://api.glassnode.com/v1"
        self.api_key = api_key
        self.session = requests.Session()
        
        # 设置请求头
        self.session.headers.update({
            'X-API-KEY': api_key
        })
    
    def get_exchange_flows(self, asset: str = 'BTC', exchange: str = None, since: int = None, until: int = None) -> pd.DataFrame:
        """
        获取交易所资金流向数据
        
        Args:
            asset: 资产符号 (BTC, ETH等)
            exchange: 交易所名称
            since: 开始时间戳
            until: 结束时间戳
            
        Returns:
            资金流向数据DataFrame
        """
        try:
            url = f"{self.base_url}/metrics/transactions/transfers_volume_exchanges_net"
            params = {
                'a': asset,
                'f': 'JSON'
            }
            
            if exchange:
                params['e'] = exchange
            if since:
                params['s'] = since
            if until:
                params['u'] = until
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            df = pd.DataFrame(data)
            df['t'] = pd.to_datetime(df['t'], unit='s')
            
            return df
            
        except Exception as e:
            logger.error(f"获取交易所资金流向失败: {e}")
            return pd.DataFrame()
    
    def get_exchange_balance(self, asset: str = 'BTC', exchange: str = None) -> pd.DataFrame:
        """
        获取交易所余额数据
        
        Args:
            asset: 资产符号
            exchange: 交易所名称
            
        Returns:
            余额数据DataFrame
        """
        try:
            url = f"{self.base_url}/metrics/distribution/balance_exchanges"
            params = {
                'a': asset,
                'f': 'JSON'
            }
            
            if exchange:
                params['e'] = exchange
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            df = pd.DataFrame(data)
            df['t'] = pd.to_datetime(df['t'], unit='s')
            
            return df
            
        except Exception as e:
            logger.error(f"获取交易所余额失败: {e}")
            return pd.DataFrame()
    
    def get_whale_transactions(self, asset: str = 'BTC', threshold: int = 1000000) -> pd.DataFrame:
        """
        获取大额交易数据
        
        Args:
            asset: 资产符号
            threshold: 大额交易阈值（美元）
            
        Returns:
            大额交易数据DataFrame
        """
        try:
            url = f"{self.base_url}/metrics/transactions/transfers_volume_large"
            params = {
                'a': asset,
                'f': 'JSON',
                'threshold': threshold
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            df = pd.DataFrame(data)
            df['t'] = pd.to_datetime(df['t'], unit='s')
            
            return df
            
        except Exception as e:
            logger.error(f"获取大额交易数据失败: {e}")
            return pd.DataFrame()
    
    def get_network_activity(self, asset: str = 'BTC') -> Dict:
        """
        获取网络活跃度数据
        
        Args:
            asset: 资产符号
            
        Returns:
            网络活跃度数据
        """
        try:
            metrics = {}
            
            # 活跃地址数
            url = f"{self.base_url}/metrics/addresses/active_count"
            params = {'a': asset, 'f': 'JSON'}
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                metrics['active_addresses'] = data[-1]['v'] if data else 0
            
            # 新增地址数
            url = f"{self.base_url}/metrics/addresses/new_non_zero_count"
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                metrics['new_addresses'] = data[-1]['v'] if data else 0
            
            # 交易数量
            url = f"{self.base_url}/metrics/transactions/count"
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                metrics['transaction_count'] = data[-1]['v'] if data else 0
            
            return metrics
            
        except Exception as e:
            logger.error(f"获取网络活跃度失败: {e}")
            return {}
    
    def get_market_sentiment(self, asset: str = 'BTC') -> Dict:
        """
        获取市场情绪指标
        
        Args:
            asset: 资产符号
            
        Returns:
            市场情绪数据
        """
        try:
            sentiment = {}
            
            # NVT比率
            url = f"{self.base_url}/metrics/indicators/nvt"
            params = {'a': asset, 'f': 'JSON'}
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                sentiment['nvt_ratio'] = data[-1]['v'] if data else 0
            
            # MVRV比率
            url = f"{self.base_url}/metrics/indicators/mvrv"
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                sentiment['mvrv_ratio'] = data[-1]['v'] if data else 0
            
            # 恐惧贪婪指数
            url = f"{self.base_url}/metrics/indicators/fear_and_greed_index"
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                sentiment['fear_greed_index'] = data[-1]['v'] if data else 0
            
            return sentiment
            
        except Exception as e:
            logger.error(f"获取市场情绪失败: {e}")
            return {}
    
    def get_mining_data(self, asset: str = 'BTC') -> Dict:
        """
        获取挖矿数据
        
        Args:
            asset: 资产符号
            
        Returns:
            挖矿数据
        """
        try:
            mining_data = {}
            
            # 挖矿难度
            url = f"{self.base_url}/metrics/mining/difficulty_latest"
            params = {'a': asset, 'f': 'JSON'}
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                mining_data['difficulty'] = data[-1]['v'] if data else 0
            
            # 哈希率
            url = f"{self.base_url}/metrics/mining/hash_rate_mean"
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                mining_data['hash_rate'] = data[-1]['v'] if data else 0
            
            return mining_data
            
        except Exception as e:
            logger.error(f"获取挖矿数据失败: {e}")
            return {}
    
    def get_defi_metrics(self, asset: str = 'ETH') -> Dict:
        """
        获取DeFi指标（主要适用于ETH）
        
        Args:
            asset: 资产符号
            
        Returns:
            DeFi指标数据
        """
        try:
            defi_metrics = {}
            
            # 锁定在DeFi中的价值
            url = f"{self.base_url}/metrics/defi/total_value_locked_usd"
            params = {'a': asset, 'f': 'JSON'}
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                defi_metrics['tvl'] = data[-1]['v'] if data else 0
            
            # Gas价格
            url = f"{self.base_url}/metrics/fees/gas_price_mean"
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                defi_metrics['gas_price'] = data[-1]['v'] if data else 0
            
            return defi_metrics
            
        except Exception as e:
            logger.error(f"获取DeFi指标失败: {e}")
            return {}
