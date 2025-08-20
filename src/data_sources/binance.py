"""
Binance API 数据源
提供实时交易数据和资金流向信息
"""
import ccxt
import pandas as pd
from typing import List, Dict, Optional
import time
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class BinanceAPI:
    """Binance API 客户端"""
    
    def __init__(self, api_key: Optional[str] = None, secret_key: Optional[str] = None):
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot'
            }
        })
    
    def get_ticker(self, symbol: str = 'BTC/USDT') -> Optional[Dict]:
        """
        获取单个交易对的行情数据
        
        Args:
            symbol: 交易对符号
            
        Returns:
            行情数据
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker
        except Exception as e:
            logger.error(f"获取ticker失败 {symbol}: {e}")
            return None
    
    def get_tickers(self, symbols: List[str] = None) -> Dict:
        """
        获取多个交易对的行情数据
        
        Args:
            symbols: 交易对列表，如果为None则获取所有
            
        Returns:
            行情数据字典
        """
        try:
            if symbols:
                tickers = {}
                for symbol in symbols:
                    ticker = self.get_ticker(symbol)
                    if ticker:
                        tickers[symbol] = ticker
                return tickers
            else:
                return self.exchange.fetch_tickers()
        except Exception as e:
            logger.error(f"获取tickers失败: {e}")
            return {}
    
    def get_ohlcv(self, symbol: str, timeframe: str = '1d', limit: int = 100) -> pd.DataFrame:
        """
        获取K线数据
        
        Args:
            symbol: 交易对符号
            timeframe: 时间框架
            limit: 数据条数
            
        Returns:
            OHLCV数据DataFrame
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            logger.error(f"获取OHLCV失败 {symbol}: {e}")
            return pd.DataFrame()
    
    def get_order_book(self, symbol: str, limit: int = 20) -> Optional[Dict]:
        """
        获取订单簿数据
        
        Args:
            symbol: 交易对符号
            limit: 深度
            
        Returns:
            订单簿数据
        """
        try:
            order_book = self.exchange.fetch_order_book(symbol, limit)
            return order_book
        except Exception as e:
            logger.error(f"获取订单簿失败 {symbol}: {e}")
            return None
    
    def get_recent_trades(self, symbol: str, limit: int = 100) -> List[Dict]:
        """
        获取最近交易记录
        
        Args:
            symbol: 交易对符号
            limit: 交易记录数量
            
        Returns:
            交易记录列表
        """
        try:
            trades = self.exchange.fetch_trades(symbol, limit=limit)
            return trades
        except Exception as e:
            logger.error(f"获取交易记录失败 {symbol}: {e}")
            return []
    
    def get_24hr_stats(self, symbol: str = None) -> Dict:
        """
        获取24小时统计信息
        
        Args:
            symbol: 交易对符号，如果为None则获取所有
            
        Returns:
            24小时统计数据
        """
        try:
            if symbol:
                stats = self.exchange.fetch_ticker(symbol)
                return {
                    'symbol': symbol,
                    'price_change': stats['change'],
                    'price_change_percent': stats['percentage'],
                    'volume': stats['quoteVolume'],
                    'high': stats['high'],
                    'low': stats['low']
                }
            else:
                # 获取主要代币的24小时数据
                major_symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'SOL/USDT']
                stats = {}
                for sym in major_symbols:
                    ticker = self.get_ticker(sym)
                    if ticker:
                        stats[sym] = {
                            'price_change': ticker['change'],
                            'price_change_percent': ticker['percentage'],
                            'volume': ticker['quoteVolume'],
                            'high': ticker['high'],
                            'low': ticker['low']
                        }
                return stats
        except Exception as e:
            logger.error(f"获取24小时统计失败: {e}")
            return {}
    
    def get_funding_rate(self, symbol: str) -> Optional[float]:
        """
        获取资金费率（仅适用于永续合约）
        
        Args:
            symbol: 交易对符号
            
        Returns:
            资金费率
        """
        try:
            # 切换到永续合约模式
            self.exchange.options['defaultType'] = 'swap'
            funding_rate = self.exchange.fetch_funding_rate(symbol)
            # 切换回现货模式
            self.exchange.options['defaultType'] = 'spot'
            return funding_rate
        except Exception as e:
            logger.error(f"获取资金费率失败 {symbol}: {e}")
            return None
    
    def get_exchange_info(self) -> Dict:
        """
        获取交易所信息
        
        Returns:
            交易所信息
        """
        try:
            info = self.exchange.load_markets()
            return {
                'symbols': list(info.keys()),
                'currencies': list(self.exchange.currencies.keys()),
                'timeframes': self.exchange.timeframes
            }
        except Exception as e:
            logger.error(f"获取交易所信息失败: {e}")
            return {}
    
    def get_volume_analysis(self, symbol: str, days: int = 7) -> Dict:
        """
        获取交易量分析
        
        Args:
            symbol: 交易对符号
            days: 分析天数
            
        Returns:
            交易量分析数据
        """
        try:
            # 获取历史K线数据
            ohlcv = self.get_ohlcv(symbol, '1d', days)
            
            if ohlcv.empty:
                return {}
            
            # 计算交易量统计
            volume_stats = {
                'symbol': symbol,
                'current_volume': ohlcv['volume'].iloc[-1],
                'avg_volume': ohlcv['volume'].mean(),
                'max_volume': ohlcv['volume'].max(),
                'min_volume': ohlcv['volume'].min(),
                'volume_change_24h': (ohlcv['volume'].iloc[-1] - ohlcv['volume'].iloc[-2]) / ohlcv['volume'].iloc[-2] * 100 if len(ohlcv) > 1 else 0,
                'volume_trend': 'increasing' if ohlcv['volume'].iloc[-1] > ohlcv['volume'].mean() else 'decreasing'
            }
            
            return volume_stats
            
        except Exception as e:
            logger.error(f"获取交易量分析失败 {symbol}: {e}")
            return {}
