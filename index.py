#!/usr/bin/env python3
"""
TokenData - Cloudflare Pages入口文件
"""
import os
import sys
import logging
from datetime import datetime

import requests
import time

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objs as go

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化Dash应用
app = Dash(__name__, 
           title="TokenData - 主流代币监控",
           meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

# 全局数据存储
global_data = {
    'market_data': [],
    'global_summary': {},
    'last_update': None
}

class SimpleDataAggregator:
    """简化的数据聚合器，适合Cloudflare部署"""
    
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://api.coingecko.com/api/v3"
    
    def get_market_data(self, limit=50):
        """获取市场数据"""
        try:
            url = f"{self.base_url}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': limit,
                'page': 1,
                'sparkline': False
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if not data:
                return []
            
            # 处理数据，转换为字典列表
            processed_data = []
            for item in data:
                processed_item = {
                    'rank': item.get('market_cap_rank', 0),
                    'name': item.get('name', ''),
                    'symbol': item.get('symbol', ''),
                    'current_price': item.get('current_price', 0),
                    'market_cap': item.get('market_cap', 0),
                    'volume_24h': item.get('total_volume', 0),
                    'change_1h': float(item.get('price_change_percentage_1h_in_currency', 0) or 0),
                    'change_24h': float(item.get('price_change_percentage_24h_in_currency', 0) or 0),
                    'change_7d': float(item.get('price_change_percentage_7d_in_currency', 0) or 0)
                }
                processed_data.append(processed_item)
            
            return processed_data
            
        except Exception as e:
            logger.error(f"获取市场数据失败: {e}")
            return []
    
    def get_global_summary(self):
        """获取全球市场摘要"""
        try:
            url = f"{self.base_url}/global"
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            global_data = data.get('data', {})
            
            return {
                'total_market_cap': global_data.get('total_market_cap', {}).get('usd', 0),
                'total_volume': global_data.get('total_volume', {}).get('usd', 0),
                'market_cap_change_percentage_24h_usd': global_data.get('market_cap_change_percentage_24h_usd', 0),
                'bitcoin_dominance': global_data.get('market_cap_percentage', {}).get('btc', 0)
            }
            
        except Exception as e:
            logger.error(f"获取全球摘要失败: {e}")
            return {}

# 格式化函数
def format_number(value, decimals=2):
    """格式化数字"""
    try:
        if value is None or value == 0:
            return "0"
        
        if abs(value) >= 1e12:
            return f"{value/1e12:.{decimals}f}T"
        elif abs(value) >= 1e9:
            return f"{value/1e9:.{decimals}f}B"
        elif abs(value) >= 1e6:
            return f"{value/1e6:.{decimals}f}M"
        elif abs(value) >= 1e3:
            return f"{value/1e3:.{decimals}f}K"
        else:
            return f"{value:.{decimals}f}"
    except:
        return str(value)

def format_currency(value, decimals=2):
    """格式化货币"""
    try:
        if value is None or value == 0:
            return "$0"
        
        formatted = format_number(value, decimals)
        return f"${formatted}"
    except:
        return f"${value}"

def format_percentage(value, decimals=2):
    """格式化百分比"""
    try:
        if value is None:
            return "N/A"
        return f"{value:+.{decimals}f}%"
    except:
        return "N/A"

# 数据更新函数
def update_data():
    """更新数据"""
    logger.info("开始更新数据...")
    aggregator = SimpleDataAggregator()
    
    # 获取市场数据
    data = aggregator.get_market_data(50)
    if data:
        global_data['market_data'] = data
    
    # 获取全球摘要
    summary = aggregator.get_global_summary()
    if summary:
        global_data['global_summary'] = summary
    
    global_data['last_update'] = datetime.now()
    logger.info("数据更新完成")

# 初始化数据
update_data()

# 应用布局
app.layout = html.Div([
    # 标题
    html.H1("🚀 TokenData - 主流代币监控", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
    
    # 控制面板
    html.Div([
        html.Div([
            html.Label("显示数量:", style={'marginRight': '10px'}),
            dcc.Dropdown(
                id='limit-dropdown',
                options=[
                    {'label': '前10名', 'value': 10},
                    {'label': '前20名', 'value': 20},
                    {'label': '前50名', 'value': 50}
                ],
                value=20,
                style={'width': '120px', 'display': 'inline-block'}
            )
        ], style={'display': 'inline-block', 'marginRight': '20px'}),
        
        html.Button("🔄 刷新数据", id='refresh-btn', n_clicks=0,
                   style={'backgroundColor': '#3498db', 'color': 'white', 'border': 'none', 
                          'padding': '8px 16px', 'borderRadius': '4px', 'cursor': 'pointer'})
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    # 市场概况
    html.Div(id='market-summary', style={'marginBottom': '20px'}),
    
    # 代币表格
    html.Div(id='token-table', style={'marginBottom': '20px'}),
    
    # 自动刷新
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  # 5分钟
        n_intervals=0
    )
], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif'})

# 回调函数：更新市场概况
@callback(
    Output('market-summary', 'children'),
    [Input('refresh-btn', 'n_clicks'),
     Input('interval-component', 'n_intervals')]
)
def update_market_summary(n_clicks, n_intervals):
    if n_clicks > 0 or n_intervals > 0:
        update_data()
    
    summary = global_data['global_summary']
    if not summary:
        return html.Div("无法获取市场数据", style={'textAlign': 'center', 'color': '#e74c3c'})
    
    market_summary = [
        html.Div([
            html.H4("💰 总市值", style={'margin': '0', 'color': '#2c3e50'}),
            html.P(format_currency(summary.get('total_market_cap', 0)), 
                   style={'margin': '5px 0', 'fontSize': '18px', 'fontWeight': 'bold', 'color': '#27ae60'})
        ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#ecf0f1', 'borderRadius': '8px'}),
        
        html.Div([
            html.H4("📊 24h成交量", style={'margin': '0', 'color': '#2c3e50'}),
            html.P(format_currency(summary.get('total_volume', 0)), 
                   style={'margin': '5px 0', 'fontSize': '18px', 'fontWeight': 'bold', 'color': '#3498db'})
        ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#ecf0f1', 'borderRadius': '8px'}),
        
        html.Div([
            html.H4("🔄 24h变化", style={'margin': '0', 'color': '#2c3e50'}),
            html.P(f"{summary.get('market_cap_change_percentage_24h_usd', 0):+.2f}%", 
                   style={'margin': '5px 0', 'fontSize': '18px', 'fontWeight': 'bold', 
                          'color': '#27ae60' if summary.get('market_cap_change_percentage_24h_usd', 0) >= 0 else '#e74c3c'})
        ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#ecf0f1', 'borderRadius': '8px'}),
        
        html.Div([
            html.H4("₿ BTC主导", style={'margin': '0', 'color': '#2c3e50'}),
            html.P(f"{summary.get('bitcoin_dominance', 0):.2f}%", 
                   style={'margin': '5px 0', 'fontSize': '18px', 'fontWeight': 'bold', 'color': '#f39c12'})
        ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#ecf0f1', 'borderRadius': '8px'})
    ]
    
    # 添加数据说明
    data_info = html.Div([
        html.H4("📊 数据说明", style={'color': '#2c3e50', 'marginBottom': '10px'}),
        html.Div([
            html.P([
                html.Strong("数据来源："), "CoinGecko API（免费版）",
                html.Br(),
                html.Strong("更新频率："), "每5分钟自动更新",
                html.Br(),
                html.Strong("成交量数据："), "全网所有交易所24小时总交易量",
                html.Br(),
                html.Strong("价格数据："), "全网加权平均价格",
                html.Br(),
                html.Strong("覆盖范围："), "Binance、Coinbase、Kraken、KuCoin、OKX、Bybit、Gate.io、Huobi、Bitfinex、Bitstamp等",
                html.Br(),
                html.Strong("注意："), "基于免费数据源，分析结果仅供参考"
            ], style={'fontSize': '12px', 'color': '#7f8c8d', 'lineHeight': '1.4'})
        ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px', 'border': '1px solid #e9ecef'})
    ], style={'marginTop': '20px'})
    
    return market_summary + [data_info]

# 回调函数：更新代币表格
@callback(
    Output('token-table', 'children'),
    [Input('limit-dropdown', 'value'),
     Input('refresh-btn', 'n_clicks'),
     Input('interval-component', 'n_intervals')]
)
def update_token_table(limit, n_clicks, n_intervals):
    if n_clicks > 0 or n_intervals > 0:
        update_data()
    
    data = global_data['market_data']
    if not data:
        return html.Div("无法获取代币数据", style={'textAlign': 'center', 'color': '#e74c3c'})
    
    # 限制显示数量
    data_display = data[:limit]
    
    # 创建表格行
    rows = []
    for row in data_display:
        change_1h = row.get('change_1h', 0)
        change_24h = row.get('change_24h', 0)
        change_7d = row.get('change_7d', 0)
        
        # 变化颜色
        def get_change_color(change):
            if change is None:
                return '#95a5a6'
            return '#27ae60' if change > 0 else '#e74c3c' if change < 0 else '#95a5a6'
        
        # 计算交易量
        volume_24h = row.get('volume_24h', 0)
        volume_1h = volume_24h / 24  # 估算1小时交易量
        volume_7d = volume_24h * 7   # 估算7天交易量
        
        rows.append(html.Tr([
            html.Td(f"#{row['rank']}", style={'textAlign': 'center', 'fontWeight': 'bold'}),
            html.Td([
                html.Div(row['name'], style={'fontWeight': 'bold'}),
                html.Div(row['symbol'].upper(), style={'fontSize': '12px', 'color': '#7f8c8d'})
            ]),
            html.Td(format_currency(row['current_price'], 2), style={'textAlign': 'right', 'fontWeight': 'bold'}),
            html.Td(format_percentage(change_1h, 2), 
                   style={'textAlign': 'right', 'color': get_change_color(change_1h), 'fontWeight': 'bold'}),
            html.Td(format_percentage(change_24h, 2), 
                   style={'textAlign': 'right', 'color': get_change_color(change_24h)}),
            html.Td(format_percentage(change_7d, 2), 
                   style={'textAlign': 'right', 'color': get_change_color(change_7d)}),
            html.Td(format_currency(volume_1h, 2), style={'textAlign': 'right', 'fontSize': '12px'}),
            html.Td(format_currency(volume_24h, 2), style={'textAlign': 'right'}),
            html.Td(format_currency(volume_7d, 2), style={'textAlign': 'right', 'fontSize': '12px'}),
            html.Td(format_currency(row['market_cap'], 2), style={'textAlign': 'right'})
        ]))
    
    return html.Table([
        html.Thead(html.Tr([
            html.Th("排名", style={'textAlign': 'center'}),
            html.Th("代币", style={'textAlign': 'left'}),
            html.Th("价格", style={'textAlign': 'right'}),
            html.Th("1h变化", style={'textAlign': 'right'}),
            html.Th("24h变化", style={'textAlign': 'right'}),
            html.Th("7d变化", style={'textAlign': 'right'}),
            html.Th("1h成交量", style={'textAlign': 'right'}),
            html.Th("24h成交量", style={'textAlign': 'right'}),
            html.Th("7d成交量", style={'textAlign': 'right'}),
            html.Th("市值", style={'textAlign': 'right'})
        ], style={'backgroundColor': '#34495e', 'color': 'white'})),
        html.Tbody(rows)
    ], style={'width': '100%', 'borderCollapse': 'collapse', 'backgroundColor': 'white', 'borderRadius': '8px', 'overflow': 'hidden'})

# Cloudflare Pages适配
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
