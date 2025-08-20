"""
CoinGecko API 数据源
提供免费的基础加密货币数据
"""
import requests
import pandas as pd
from typing import List, Dict, Optional
import time
import logging

logger = logging.getLogger(__name__)

class CoinGeckoAPI:
    """CoinGecko API 客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.api_key = api_key
        self.session = requests.Session()
        
        # 设置请求头
        if api_key:
            self.session.headers.update({
                'X-CG-API-KEY': api_key
            })
    
    def get_top_coins(self, limit: int = 100, currency: str = 'usd') -> List[Dict]:
        """
        获取市值排名前N的代币
        
        Args:
            limit: 返回的代币数量
            currency: 计价货币
            
        Returns:
            代币列表
        """
        try:
            url = f"{self.base_url}/coins/markets"
            params = {
                'vs_currency': currency,
                'order': 'market_cap_desc',
                'per_page': limit,
                'page': 1,
                'sparkline': False,
                'price_change_percentage': '24h,7d,30d'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"获取top coins失败: {e}")
            return []
    
    def get_coin_data(self, coin_id: str, currency: str = 'usd') -> Optional[Dict]:
        """
        获取单个代币的详细数据
        
        Args:
            coin_id: 代币ID (如 'bitcoin', 'ethereum')
            currency: 计价货币
            
        Returns:
            代币详细数据
        """
        try:
            url = f"{self.base_url}/coins/{coin_id}"
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
            
            return response.json()
            
        except Exception as e:
            logger.error(f"获取代币数据失败 {coin_id}: {e}")
            return None
    
    def get_exchange_rates(self, currency: str = 'usd') -> Dict:
        """
        获取汇率数据
        
        Args:
            currency: 基础货币
            
        Returns:
            汇率数据
        """
        try:
            url = f"{self.base_url}/exchange_rates"
            response = self.session.get(url)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"获取汇率失败: {e}")
            return {}
    
    def get_trending_coins(self) -> List[Dict]:
        """
        获取趋势代币
        
        Returns:
            趋势代币列表
        """
        try:
            url = f"{self.base_url}/search/trending"
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            return data.get('coins', [])
            
        except Exception as e:
            logger.error(f"获取趋势代币失败: {e}")
            return []
    
    def get_global_data(self) -> Dict:
        """
        获取全球市场数据
        
        Returns:
            全球市场数据
        """
        try:
            url = f"{self.base_url}/global"
            response = self.session.get(url)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"获取全球数据失败: {e}")
            return {}
    
    def get_coin_market_chart(self, coin_id: str, days: int = 30, currency: str = 'usd') -> Dict:
        """
        获取代币价格历史数据
        
        Args:
            coin_id: 代币ID
            days: 天数
            currency: 计价货币
            
        Returns:
            价格历史数据
        """
        try:
            url = f"{self.base_url}/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': currency,
                'days': days
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"获取价格历史失败 {coin_id}: {e}")
            return {}
    
    def get_exchanges(self, limit: int = 100) -> List[Dict]:
        """
        获取交易所列表
        
        Args:
            limit: 返回数量
            
        Returns:
            交易所列表
        """
        try:
            url = f"{self.base_url}/exchanges"
            params = {
                'per_page': limit
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"获取交易所列表失败: {e}")
            return []
