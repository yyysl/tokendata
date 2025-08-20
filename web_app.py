#!/usr/bin/env python3
"""
TokenData Web应用
基于Dash的Web界面，展示主流代币变化数据
"""
import sys
import os
import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import threading
import time

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_sources.free_data_aggregator import FreeDataAggregator
from src.analysis.flow_analyzer import FlowAnalyzer
from src.utils.formatter import format_currency, format_percentage, format_flow_value

# 初始化Dash应用
app = dash.Dash(__name__, title="TokenData - 主流代币监控")
app.config.suppress_callback_exceptions = True

# 全局数据存储
global_data = {
    'market_data': pd.DataFrame(),
    'global_summary': {},
    'trending_coins': [],
    'last_update': None
}

# 数据聚合器
aggregator = FreeDataAggregator()
flow_analyzer = FlowAnalyzer()

def update_data():
    """更新数据"""
    try:
        # 获取市场数据
        market_data = aggregator.get_hourly_market_data(limit=50)
        global_data['market_data'] = market_data
        
        # 获取全球市场数据
        global_summary = aggregator.get_global_market_data()
        global_data['global_summary'] = global_summary
        
        # 获取趋势代币
        trending = aggregator.get_trending_coins()
        global_data['trending_coins'] = trending
        
        global_data['last_update'] = datetime.now()
        
    except Exception as e:
        print(f"数据更新失败: {e}")

# 初始化数据
update_data()

# 应用布局
app.layout = html.Div([
    # 标题栏
    html.Div([
        html.H1("🚀 TokenData - 主流代币监控", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
        html.Div([
            html.Span("最后更新: ", style={'fontWeight': 'bold'}),
            html.Span(id='last-update', style={'color': '#7f8c8d'}),
            html.Button("🔄 刷新", id='refresh-btn', n_clicks=0, 
                       style={'marginLeft': '20px', 'padding': '8px 16px', 'backgroundColor': '#3498db', 'color': 'white', 'border': 'none', 'borderRadius': '4px', 'cursor': 'pointer'})
        ], style={'textAlign': 'center', 'marginBottom': '30px'})
    ]),
    
    # 市场概况卡片
    html.Div([
        html.Div([
            html.H3("🌍 市场概况", style={'textAlign': 'center', 'color': '#2c3e50'}),
            html.Div(id='market-summary', style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))', 'gap': '15px'})
        ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 10px rgba(0,0,0,0.1)', 'marginBottom': '20px'})
    ]),
    
    # 主要内容区域
    html.Div([
        # 主流代币表格
        html.Div([
            html.H3("📊 主流代币变化", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
            html.Div([
                html.Label("显示数量: ", style={'marginRight': '10px'}),
                dcc.Dropdown(
                    id='limit-dropdown',
                    options=[
                        {'label': '前10个', 'value': 10},
                        {'label': '前20个', 'value': 20},
                        {'label': '前30个', 'value': 30},
                        {'label': '前50个', 'value': 50}
                    ],
                    value=20,
                    style={'width': '120px', 'display': 'inline-block'}
                )
            ], style={'textAlign': 'center', 'marginBottom': '20px'}),
            html.Div(id='token-table', style={'overflowX': 'auto'})
        ])
    ]),
    
    # 自动刷新间隔
    dcc.Interval(
        id='interval-component',
        interval=300000,  # 5分钟刷新一次
        n_intervals=0
    )
], style={'backgroundColor': '#f8f9fa', 'minHeight': '100vh', 'padding': '20px'})

# 回调函数：更新最后更新时间
@callback(
    Output('last-update', 'children'),
    [Input('refresh-btn', 'n_clicks'),
     Input('interval-component', 'n_intervals')]
)
def update_last_update(n_clicks, n_intervals):
    if n_clicks > 0 or n_intervals > 0:
        update_data()
    if global_data['last_update']:
        return global_data['last_update'].strftime('%Y-%m-%d %H:%M:%S')
    return "未更新"

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
            html.P(format_currency(summary.get('total_market_cap', 0), 2), style={'margin': '5px 0', 'fontSize': '18px', 'fontWeight': 'bold', 'color': '#27ae60'})
        ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#ecf0f1', 'borderRadius': '8px'}),
        
        html.Div([
            html.H4("📈 24h成交量", style={'margin': '0', 'color': '#2c3e50'}),
            html.P(format_currency(summary.get('total_volume', 0), 2), style={'margin': '5px 0', 'fontSize': '18px', 'fontWeight': 'bold', 'color': '#3498db'})
        ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#ecf0f1', 'borderRadius': '8px'}),
        
        html.Div([
            html.H4("🔄 24h变化", style={'margin': '0', 'color': '#2c3e50'}),
            html.P(format_percentage(summary.get('market_cap_change_percentage_24h_usd', 0), 2), 
                   style={'margin': '5px 0', 'fontSize': '18px', 'fontWeight': 'bold', 
                          'color': '#27ae60' if summary.get('market_cap_change_percentage_24h_usd', 0) >= 0 else '#e74c3c'})
        ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#ecf0f1', 'borderRadius': '8px'}),
        
        html.Div([
            html.H4("₿ BTC主导", style={'margin': '0', 'color': '#2c3e50'}),
            html.P(f"{summary.get('bitcoin_dominance', 0):.2f}%", style={'margin': '5px 0', 'fontSize': '18px', 'fontWeight': 'bold', 'color': '#f39c12'})
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
                html.Strong("资金流向："), "基于全网价格变化和交易量的估算",
                html.Br(),
                html.Strong("流向公式："), "流向金额 = 全网交易量 × 价格变化比例 × 系数（最大30%）",
                html.Br(),
                html.Strong("正值表示流入，负值表示流出"),
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
    
    df = global_data['market_data']
    if df.empty:
        return html.Div("无法获取代币数据", style={'textAlign': 'center', 'color': '#e74c3c'})
    
    # 限制显示数量
    df_display = df.head(limit)
    
    # 创建表格行
    rows = []
    for _, row in df_display.iterrows():
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
        
        # 使用资金流向分析器
        token_data = {
            'change_1h': change_1h,
            'change_24h': change_24h,
            'change_7d': change_7d,
            'volume_24h': volume_24h
        }
        
        flow_analysis = flow_analyzer.get_comprehensive_flow(token_data)
        
        # 获取流向数据
        flow_1h_amount = flow_analysis.get('1h', {}).get('flow', 0)
        flow_1h_color = flow_analysis.get('1h', {}).get('color', '#95a5a6')
        flow_24h_amount = flow_analysis.get('24h', {}).get('flow', 0)
        flow_24h_color = flow_analysis.get('24h', {}).get('color', '#95a5a6')
        flow_7d_amount = flow_analysis.get('7d', {}).get('flow', 0)
        flow_7d_color = flow_analysis.get('7d', {}).get('color', '#95a5a6')
        
        rows.append(html.Tr([
            html.Td(f"#{row['rank']}", style={'textAlign': 'center', 'fontWeight': 'bold'}),
            html.Td([
                html.Div(row['name'], style={'fontWeight': 'bold'}),
                html.Div(row['symbol'].upper(), style={'fontSize': '12px', 'color': '#7f8c8d'})
            ]),
            html.Td(format_currency(row['price'], 2), style={'textAlign': 'right', 'fontWeight': 'bold'}),
            html.Td(format_percentage(change_1h, 2), 
                   style={'textAlign': 'right', 'color': get_change_color(change_1h), 'fontWeight': 'bold'}),
            html.Td(format_percentage(change_24h, 2), 
                   style={'textAlign': 'right', 'color': get_change_color(change_24h)}),
            html.Td(format_percentage(change_7d, 2), 
                   style={'textAlign': 'right', 'color': get_change_color(change_7d)}),
            html.Td(format_currency(volume_1h, 2), style={'textAlign': 'right', 'fontSize': '12px'}),
            html.Td(format_currency(volume_24h, 2), style={'textAlign': 'right'}),
            html.Td(format_currency(volume_7d, 2), style={'textAlign': 'right', 'fontSize': '12px'}),
            html.Td(format_currency(flow_1h_amount, 2), style={'textAlign': 'center', 'color': flow_1h_color, 'fontWeight': 'bold'}),
            html.Td(format_currency(flow_24h_amount, 2), style={'textAlign': 'center', 'color': flow_24h_color}),
            html.Td(format_currency(flow_7d_amount, 2), style={'textAlign': 'center', 'color': flow_7d_color, 'fontSize': '12px'})
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
            html.Th("1h流向", style={'textAlign': 'center'}),
            html.Th("24h流向", style={'textAlign': 'center'}),
            html.Th("7d流向", style={'textAlign': 'center'})
        ], style={'backgroundColor': '#34495e', 'color': 'white'})),
        html.Tbody(rows)
    ], style={'width': '100%', 'borderCollapse': 'collapse', 'backgroundColor': 'white', 'borderRadius': '8px', 'overflow': 'hidden'})



if __name__ == '__main__':
    print("🚀 启动TokenData Web应用...")
    print("📱 访问地址: http://127.0.0.1:8050")
    print("🔄 数据每5分钟自动更新")
    print("=" * 50)
    
    # 启动应用
    app.run_server(debug=True, host='127.0.0.1', port=8050)
